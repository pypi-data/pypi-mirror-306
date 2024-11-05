'''
General connector cognitive worker - binds real-world connectors to the Langur cognitive system.
'''

from abc import ABC
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type
import inspect
from pydantic import BaseModel, Field
from langur.actions import ActionContext, ActionNode
from langur.graph.node import Node
from langur.util.schema import schema_from_function
from langur.util.model_builder import create_dynamic_model
from langur.workers.worker import STATE_DONE, STATE_SETUP, Worker
from langur.util.registries import ActionNodeRegistryFilter, action_node_type_registry

def action(
    fn: Optional[Callable] = None,
    tags: Optional[List[str]] = None,
    extra_context: Optional[Callable[[Dict[str, Any], Optional[ActionContext]], str]] = None
):
    """
    Decorator that can be used either as @action or @action(kw1=...)

    extra_context: An additional function to return more context whenever this action is being executed.
    - The fields of this function need to match the fields of the action, except each needs a None default!
    - Should return a str which serves as context for the LLM when deciding on inputs for the action.
    """
    #print("tags:", tags)
    tags = tags if tags else []
    def _register_model(func: Callable[[Any], Any]):
        schema = schema_from_function(func)
        #print(f"{schema.name} json_schema:", schema.json_schema)
        #print(f"{schema.name} fields:", schema.fields_dict)
        
        if "ctx" in schema.fields_dict and "ctx" not in schema.json_schema["properties"]:
            if schema.is_async:
                async def execute(self, ctx: ActionContext):
                    result = await func(self=ctx.conn, ctx=ctx, **self.inputs)
                    return f"Executed action {schema.name} with inputs {self.inputs}, result:\n{result}"
            else:
                async def execute(self, ctx: ActionContext):
                    result = func(self=ctx.conn, ctx=ctx, **self.inputs)
                    return f"Executed action {schema.name} with inputs {self.inputs}, result:\n{result}"
        else:
            if schema.is_async:
                async def execute(self, ctx: ActionContext):
                    result = await func(self=ctx.conn, **self.inputs)
                    return f"Executed action {schema.name} with inputs {self.inputs}, result:\n{result}"
            else:
                async def execute(self, ctx: ActionContext):
                    result = func(self=ctx.conn, **self.inputs)
                    return f"Executed action {schema.name} with inputs {self.inputs}, result:\n{result}"
        
        func_dict = {"execute": execute}    

        if extra_context is not None:
            extra_schema = schema_from_function(extra_context)
            if "ctx" in extra_schema.fields_dict and "ctx" not in extra_schema.json_schema["properties"]:
                def extra_context_wrapper(self, ctx: ActionContext):
                    #return extra_context(self=ctx.conn, ctx=ctx, inputs=self.inputs)
                    return extra_context(self=ctx.conn, ctx=ctx, **self.inputs)
            else:
                def extra_context_wrapper(self, ctx: ActionContext):
                    return extra_context(self=ctx.conn, **self.inputs)
                    #return extra_context(self=ctx.conn, ctx=ctx, inputs=self.inputs)
            
            func_dict["extra_context"] = extra_context_wrapper
        
        action_node_subtype = create_dynamic_model(
            schema.name,
            {
                "definition": (ClassVar[str], schema.description),
                #"input_schema": (ClassVar[dict[str, Any]], schema.json_schema["properties"])#TODO
                "input_schema": (ClassVar[dict[str, Any]], schema.baml_types)
            },
            func_dict,
            ActionNode
        )
        
        connector_class_name = func.__qualname__.split('.')[0]
        action_node_type_registry.register(
            connector_class_name=connector_class_name,
            action_cls=action_node_subtype,
            tags=tags
        )
        
        return func

    # Handle @action case
    if fn is not None:
        _register_model(fn)
        return fn
    # Handle @action(kw1=...) case  
    def decorator(func):
        _register_model(func)
        return func
    return decorator


class ConnectorOverview(Node):
    content: str

    tags: ClassVar[list[str]] = ["observable"]

    def observe(self) -> str:
        return self.content

class Connector(Worker, ABC):
    '''
    Generic Connector. Can subclass to implement own
    '''
    #action_node_types: ClassVar[list[Type[ActionNode]]]
    action_filter: ActionNodeRegistryFilter = Field(default_factory=ActionNodeRegistryFilter)

    def overview(self) -> str | None:
        '''
        For connectors that have context that is helpful to have constantly available,
        can return it here. Try to keep this brief as it enters the context of many prompts.
        '''
        return None

    async def cycle(self):
        overview = self.overview()
        has_overview = overview is not None
        connector_overview_node_id = self.__class__.__name__

        if has_overview:
            # Every cycle, update the content of the overview node
            overview_node: ConnectorOverview = self.cg.query_node_by_id(connector_overview_node_id)
            if not overview_node:
                # If not exists, create it
                overview_node = ConnectorOverview(id=connector_overview_node_id, content=overview)
                self.cg.add_node(overview_node)
            overview_node.content = overview
        
        if self.state == STATE_SETUP:
            self.state = STATE_DONE
    
    def enable(self, *tags: str, names: List[str] = None):
        '''
        Make actions with certain names or tags available to the agent.
        Mutates the connector but returns self for convenient chaining.
        '''
        self.action_filter.enable_actions(names=names, tags=tags)
        return self

    def disable(self, *tags: str, names: List[str] = None):
        '''
        Make actions with certain names or tags unavailable to the agent.
        Mutates the connector but returns self for convenient chaining.
        '''
        self.action_filter.disable_actions(names=names, tags=tags)
        return self
    
    def list_actions(self) -> List[str]:
        return [typ.action_type_name() for typ in self.get_action_node_types()]

    def get_action_node_types(self) -> List[Type['ActionNode']]:
        return action_node_type_registry.get_action_node_types(
            self.__class__.__name__,
            self.action_filter
        )