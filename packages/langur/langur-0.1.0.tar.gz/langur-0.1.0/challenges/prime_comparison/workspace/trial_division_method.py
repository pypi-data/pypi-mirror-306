import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_primes_trial_division(n):
    return [i for i in range(n + 1) if is_prime(i)]

start_time = time.time()
primes = find_primes_trial_division(10000)
end_time = time.time()

print(f'Trial Division Method Time: {end_time - start_time:.6f} seconds')
print(f'Found {len(primes)} prime numbers')