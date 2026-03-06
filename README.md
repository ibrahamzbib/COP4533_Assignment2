# Cache Eviction Simulator
Student : Ibrahim Zbib (UFID: 79090242)


## Requirements:
Python 3.x - no external libraries required


## How to run:
```
python src/cache_sim.py <input_file>
```
#### EXAMPLE:
```
python src/cache_sim.py data/example.in
```
#### EXPECTED OUTPUT:
```
FIFO  : 8
LRU   : 8
OPTFF : 6
```

## How to run tests:
```
python tests/test_cache.py
```
#### EXPECTED OUTPUT:
```
test_evicts_oldest_inserted (TestFIFO) ... ok
test_hit_not_counted_as_miss (TestFIFO) ... ok
test_evicts_least_recently_used (TestLRU) ... ok
test_hit_not_counted_as_miss (TestLRU) ... ok
test_evicts_farthest_next_use (TestOPTFF) ... ok
test_evicts_never_used_again (TestOPTFF) ... ok
test_hit_not_counted_as_miss (TestOPTFF) ... ok

Ran 7 tests in 0.001s

OK
```
## Input Format:
```
k m
r1 r2 r3 ... rm

k = cache capacity (k >= 1)
m = number of requests
r1 ... rm = space-separated sequence of integer item IDs
```
## Output Format:
```
FIFO  : <number_of_misses>
LRU   : <number_of_misses>
OPTFF : <number_of_misses>
```
### Assumptions

Input is well-formed and matches the specified format exactly.
All request IDs are integers
k >= 1 and m >= 1
The second line contains exactly m space-separated integer



## Written Component

### Question 1: Empirical Comparison
| Input File | k | m   | FIFO | LRU | OPTFF |
|------------|---|-----|------|-----|-------|
| file1.in   | 4 | 100 | 54   | 60  | 35    |
| file2.in   | 5 | 150 | 112  | 109 | 75    |
| file3.in   | 3 | 200 | 200  | 200 | 102   |



#### Does OPTFF always have the fewest misses?
Yes, in all three files OPTFF had the fewest misses. This is expected since OPTFF is an optimal offline algorithm — it knows the full request sequence in advance, so no other policy can beat it on a fixed input.

#### How does FIFO compare to LRU?
It depends on the input. In file1, FIFO outperformed LRU (54 vs 60) because the access pattern had high reuse of older items, which LRU was too quick to evict. In file2 the result flipped — LRU beat FIFO (109 vs 112) because with a larger item pool, recently used items were more likely to be requested again soon. File3 was the most interesting case: both policies missed on every single request (200/200). The sequence cycles through 5 distinct items with only k=3 cache slots, so the working set always exceeds capacity and both policies thrash continuously regardless of their eviction choice. Overall, neither FIFO nor LRU is strictly better than the other — performance depends entirely on the access pattern.


### Question 2: Bad Sequence for LRU and FIFO

Such a sequence exists. It works as a bad sequence for both LRU and FIFO:
**Sequence (k = 3):** `1 2 3 4 1 2 3 4 1 2 3 4`

| Policy | Misses |
|--------|--------|
| FIFO   | 12     |
| LRU    | 12     |
| OPTFF  | 6      |

OPTFF incurs strictly fewer misses than both FIFO LRU on this sequence.

**Reasoning:**
The sequence cycles through 4 distinct items with a cache that only holds 3. LRU misses on every single request — 12 out of 12. The reason is that LRU always evicts the item that was least recently used, which in a strict cycle is always the item that comes next. At step 3 for example, the cache is {1,2,3} and item 1 is the LRU. LRU evicts it - but item 1 is the very next thing requested at step 4. This pattern repeats for the entire sequence with no way out.

OPTFF gets 6 misses by doing the opposite — at each eviction it keeps the items needed soonest and drops the one needed latest. At step 3, the cache is {1,2,3} and item 4 is requested. OPTFF sees that item 3's next use (step 6) is farther away than item 1 (step 4) and item 2 (step 5), so it evicts 3 instead. This lets steps 4 and 5 be hits rather than misses, cutting the total in half.



### Question 3: Prove OPTFF is Optimal
Claim: For any fixed request sequence, OPTFF incurs no more cache misses than any offline algorithm A.

Proof:
Let the request sequence be r_1, r_2, ..., r_m with cache capacity k, and let A be any offline algorithm that knows the full sequence. We will transform A into OPTFF step by step without ever increasing its miss count. This gives us misses(OPTFF) <= misses(A).
Find the first step t where A and OPTFF make a different eviction decision. Both must have a miss at step t — if one had a hit and the other a miss, the one with the hit is already doing at least as well and we can move forward. So both have a full cache and must evict something. For example:

OPTFF evicts item x, with next use at time f_x (the farthest, possibly never)
A evicts item y ≠ x, with next use at time f_y, where f_y <= f_x

Now construct A' which is identical to A except at step t it evicts x instead of y, matching OPTFF. We need to show misses(A') <= misses(A).
After step t, A' has y but not x, while A has x but not y. Consider what happens between t and f_x:

Between t and f_y: the only difference is A' has y and A has x. Any request for y is a miss for A but a hit for A'. Any request for x would be a miss for A' — but since f_x >= f_y, x is not requested before f_y, so A' never pays that cost.
At step f_y: both A and A' have y in cache, so they handle it identically. The caches have now reconciled.
From f_y onward: both algorithms are back in the same state. No further difference in misses.

So misses(A') <= misses(A), and A' now agrees with OPTFF at one more step than A did. Applying this argument repeatedly across every step where A differs from OPTFF, we fully convert A into OPTFF without ever increasing the miss count. Therefore:
    
      
      misses(OPTFF) <= misses(A)

for any offline algorithm A on any fixed request sequence. 