import time

def sieve_of_eratosthenes(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

start_time = time.time()
primes = sieve_of_eratosthenes(10000)
end_time = time.time()

print(f'Sieve Method Time: {end_time - start_time:.6f} seconds')
print(f'Found {len(primes)} prime numbers')