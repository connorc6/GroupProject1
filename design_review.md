# Design Review: Campus Maintenance Requests

**Team 3**

> **Timing note (edit or remove before committing):** *This document was written after a first working implementation of both structures existed, not before it. It describes the design the code follows. Differences between this design and the final code, if any, are listed in the README.*

## 1. Representation

**`MaintenanceRequest`** holds `request_id`, `building`, `category`, `priority` (1 Urgent to 4 Low), `reported_time` (an integer, smaller means older), and `status`. It has no ordering of its own; each sort chooses its key.

**`ArrayRequestList` (dynamic array).** A Python list used only as a fixed-capacity buffer (`[None] * capacity`), plus `size` and `capacity`. Request *i* is `data[i]`. Everything else is hand-written: growth, copying, shifting for insert and delete, and size tracking. No banned list operations are used.

**`LinkedRequestList` (singly linked list).** `Node` objects holding a request and a `next` reference. The list stores `head`, `tail`, and a cached `size`.

**Shared interface.** Both expose `push`, `append`, `count`, `getAt`, `insertAt`, `removeAt`, `findById`, and `__str__`. Methods return results and never print. Index rules come from one shared check:
- Non-integer indexes (booleans included) raise `TypeError`; out-of-range integers raise `IndexError`.
- `getAt` and `removeAt` accept `0 <= index < n`; `insertAt` accepts `0 <= index <= n`.
- A duplicate `request_id` on any insertion raises `ValueError`.
- A failed operation leaves the structure unchanged, so every check runs **before** anything is modified.

## 2. Invariants

**Array**
- `0 <= size <= capacity == len(data)`.
- `data[0:size]` holds requests in logical order; `data[size:capacity]` is all `None`.
- Resizing replaces the buffer and `capacity` together, so they never disagree.

**Linked list**
- Starting at `head` and following `next` visits exactly `size` nodes.
- `tail` is the last node (`tail.next is None`).
- `head is None` exactly when `tail is None` and `size == 0`.

**Both:** all `request_id` values are unique. **`SortedArrayRequestList`** (used for binary search by ID) also keeps IDs strictly increasing, and every insertion path is checked against that. The priority sorts must not be run on it, because they would break this invariant.

## 3. Key decisions and alternatives

| Decision | Chosen | Alternatives considered | Why |
|---|---|---|---|
| Array growth | Double capacity when full; initial capacity 4; no shrinking on removal | Grow by a fixed amount; shrink when mostly empty | Doubling makes appends amortized O(1); fixed growth would make it O(n) overall. Shrinking adds a policy to justify and gains little here. |
| Linked-list tail | Keep a `tail` reference | `head` only | `append` skips the walk. Cost: `removeAt` and the sorts must keep `tail` correct (including when the last node is removed or the list empties). |
| Linked-list size | Cache `size` | Count by walking | `count()` and the index check become O(1). Cost: every insert and remove must update it. |
| Duplicate IDs | Linear scan before every insertion, in both structures | An ID set or hash index | A separate index would add memory and complexity and may conflict with the storage rules. The scan is simple and correct, but makes **every insertion O(n)**, including `append` and `push`. |
| Binary search | A subclass that keeps IDs sorted | Sort on demand; search an unsorted array | Guarantees the precondition instead of assuming it. |
| Sorting | Insertion sort by priority; merge sort by `reported_time`; both stable | Selection or quick sort | The assignment specifies these algorithms. Using `<=` on ties keeps equal keys in their original order. |
| Linked merge sort | Split with slow and fast pointers and relink nodes | Copy to a Python list, sort, rebuild | The assignment forbids converting to a list. Relinking needs only O(log n) stack space. |

## 4. Expected complexity (worst case, for this implementation)

| Operation | Array | Linked list | Dominant cost |
|---|---|---|---|
| `getAt` | O(1) | O(n) | Array computes the slot; the list walks from `head` |
| `findById` | O(n) | O(n) | Scan |
| `push` | O(n) | O(n) | Duplicate scan; the array also shifts; the list links in O(1) |
| `append` | O(n) | O(n) | Duplicate scan (the O(1) write or tail link is not the bottleneck) |
| `insertAt`, `removeAt` | O(n) | O(n) | Array shifts; list walks to the predecessor, then relinks in O(1) |
| `count` | O(1) | O(1) | Stored size |
| Binary search (sorted array) | O(log n) | not applicable | Each probe is O(1) only on an array |
| Insertion sort | O(n²) | O(n²) | Best case is already sorted for the array, but reverse-sorted for the linked list (it scans from the head) |
| Merge sort | O(n log n) | O(n log n) | Extra space: O(n) array buffer; O(log n) recursion for the list |

## 5. Planned tests

- **Normal:** insert, remove, and search on both structures.
- **Boundary:** empty, one element, two elements; insert and remove at the beginning, middle, and end; insertion into an empty structure.
- **Invalid:** negative, out-of-range, non-integer, and boolean indexes for all three indexed methods; duplicate IDs; each with an assertion that the structure is unchanged afterward.
- **Array resizing:** behavior before and after growth, and order preserved.
- **Searches:** returned position asserted (not just "found"), a trace on IDs that differ from their indexes, missing values below, between, and above the data, and first occurrence with duplicate priorities.
- **Sorts:** exact resulting order, stability on ties, nothing lost or duplicated, and the structure still usable afterward (`append` after a sort checks `tail`).

## 6. Major risks and how we address them

1. **Off-by-one in the index contract** (`insertAt` allows `n`, `getAt` does not). One shared check function and boundary tests at `-1`, `n`, and `n + 1`.
2. **Corrupting a structure during a failed operation.** Validation and the duplicate check run before any shifting or relinking; a regression test covers a non-integer insert index.
3. **Stale `head` or `tail`** after removals and sorts. Tests check `append` immediately after removing the last node and after each sort.
4. **Stale references or non-`None` slots past `size`** in the array. `removeAt` clears the vacated slot, and a test checks it.
5. **Infinite recursion in merge sort.** An explicit base case, and tests on empty, one-element, and two-element inputs.
6. **Instability** from using `<` instead of `<=`. Tests with repeated priorities and timestamps.
7. **Binary search on unsorted data** silently returning wrong answers. A sorted subclass and a test demonstrating the failure mode.
8. **The O(n) duplicate check hiding structural differences.** `append` and `push` are O(n) in both structures, which can mask the linked list's `tail` advantage in benchmarks. We analyze and measure this explicitly.
