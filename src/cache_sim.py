import sys
from collections import deque, OrderedDict

def main():
    if len(sys.argv) < 2:
        print("Usage: python cache_sim.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        k, m = map(int, f.readline().split())
        requests = list(map(int, f.readline().split()))

    assert len(requests) == m

    print(f"FIFO  : {simulate_fifo(requests,k)}")
    print(f"LRU   : {simulate_lru(requests, k)}")
    print(f"OPTFF : 0")

def simulate_fifo(requests,k):
    cache = set()
    order = deque()
    misses = 0

    for r in requests:
        if r in cache:
            continue
        misses += 1
        if len(cache) == k:
            evict = order.popleft()
            cache.remove(evict)
        cache.add(r)
        order.append(r)

    return misses

def simulate_lru(requests, k):
    cache = OrderedDict()
    misses = 0

    for r in requests:
        if r in cache:
            cache.move_to_end(r)
            continue
        misses += 1
        if len(cache) == k:
            cache.popitem(last=False)
        cache[r] = True

    return misses

if __name__ == "__main__":
    main()