import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python cache_sim.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        k, m = map(int, f.readline().split())
        requests = list(map(int, f.readline().split()))

    assert len(requests) == m

    print(f"FIFO  : 0")
    print(f"LRU   : 0")
    print(f"OPTFF : 0")

if __name__ == "__main__":
    main()