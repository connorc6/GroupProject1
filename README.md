**Team Contribution Statement**

**Connor:** I, Connor Carey, certify that I have contributed to this project in a meaningful manner with work that is my own. My primary focus was on Part C (LinkedRequestList), Part E (Sorting), Design Review, minor contributions across other parts, and compiling/cleaning up the final deliverables.

**Shreya:** I, Shreya Shahi, certify that I have contributed to this project in a meaningful manner with work that is my own. During this project I focused on the implementation of ArrayRequestlist class, the interface, Search(linear and binary), and Performance Experiment.  

**Kristena:** I, Kristena Pederson, certify that I have contributed to this project in a meaningful manner with work that is my own. During this project, my primary focus was on the development of Part F (Dataset and Demonstration), Part H (Complexity Analysis), Part K (Workload Profiles), and the README.


**README**

**CU Maintenance Request System**

**(1) Team Members - Group 3**


*   Connor Carey
*   Shreya Shahi
*   Kristena Pederson

**(2) Project Overview**

This project implements a campus maintenance request system using two custom data structures: a dynamic array and a linked list.

Each maintenance request contains a request ID, building, category, priority, reported time, and status.

The project includes methods for adding, removing, accessing, searching, and sorting maintenance requests. We also test both data structures and compare their performance using our assigned workload.

**(3) How to Run the Project**
1. Download all project files into a single folder.
2. Run the code cells in order, starting with the MaintenanceRequest class.
3. Run the dynamic array and linked-list implementation.
4. Run the testing and demonstration cells.
5. Run Part K to generate the workload and compare the performance of both structures.
6. Open the analysis notebook. Run the cells to view demonstrations, complexity analysis and benchmark results.

**(4) Major Classes and Files**

|**File**|**Purpose**|
|---|---|
| maintenance_request.py| Defines the MaintenanceRequest class, which stores information about each request.|
|design_review.md | Contains the team's original design review and decisions.|
|workload.py| Generates and replays the assigned workload and measures performance.|
|array_request_list.py| Contains the custom dynamic array implementation.|
|linked_request_list.py| Contains the linked list implementation.|
|algorithms.py| Contains the searching and sorting algorithms|
|test_project.py| Contains tests for the projects methods and data structures.|
|analysis.ipynb|Contains the demonstrations, complexity, analysis, workload results, and discussion.|
|README.md| Provides instructions and explains the projects design.|
|Team Contribution Statement| Descrives each team member's contribution.|

**(5) Important Design Decisions**

**Dynamic Array:** We created a dynamic array that stores maintenance requests and increases its capcity when needed. It allows direct access to a request by index. Inserting or removing requests may require shifting elements.

**Linked List:** We created a linked list where each node stores a maintenance request and a reference to the next node. The list maintains head, tail, and size information. This makes removing the first request effecient, but accessing a specific index requires moving through the nodes.

**Unique Request IDs:** Both of the implementations check for duplicate IDs before adding a request. this helps prevent teh same request ID from being stored more than once.

**Searching and Sorting:** The project includes linear search, binary search, first occurence search, insertion sort, and merge sort. Binary search is used when the relevant requests are already sorted.

**Performance Comparision:** Our group used the same generated workload for both implementations and compared the median execution time from five seperate runs.

**(6) Assumptions**

- `findById` returns the request, or `None` if missing; position-returning searches return `-1`.
- `reported_time` is an integer; smaller means older. Priority 1 is the most urgent.
- Priority sorts are not run on the ID-sorted array (they would break its ordering).
- [Initial dataset and seed used; sizes used in benchmarks and why you adjusted any.]

**(7) Changes from design_review.md:**

- switched 'ArrayRequestList' to utilize the same 'check_index' function as the linked lists after a non-integer insert index corrupted the array.
_____________________________________________________________________
**Failure-Mode Analysis**

**1. Test Plan** - We tested both the dynamic array and singly linked list using maintenance requests from different campus buildings. Our tests for this included:



*   **Normal Cases:** Adding, inserting, removing, and searching for requests
*   **Boundary Cases:** Empty structures, one request, two requests, and mutliple requests. We also tested insertion and removal at the beginning, middle, and end.
*   **Invalid Cases:** Duplicate request IDs, negative index, out-of-range index, and noninteger index

We also tested the dynamic array after resizing to make sure the requests were not lost or placed in the wrong order.

**2. Possible Failure**  - in ArrayRequestList.insertAt, a non-integer like 1.2 passes the range check. So, elements will shift afterwards, but then fail when it tried to store the data and receives a TypeError. The exception is raised, but the array has been changed.

**3. Invariant** - One request has been duplicated and request has been overwritten and the contents no longer match what was stored.

**4.Input and Test Used to Detect the Failure** - trying to insertAt(1.2, request). Checking the last element is what shows this failure because the shift overwrites it.

**5. Initially Failing Test During Development** - "insertAt(1.2, request)"

**6. What We Learned** - to validate arguments (type, range, duplicates) before changing anything else. Using the same helper function to check for errors.







