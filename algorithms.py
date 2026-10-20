'''
Insertion sort on a linked list ranked by priority 1 through 4 with 1 being high
priority, 4 is lower. Takes nodes off the original chain and compares against
an empty chain. Sorting happens as the new chain is scanned with each link,
and nodes are placed based on priority.
'''
def insertionSortLinked(linked_list):
    # compare against empty chain
    sorted_head = None
    # grab first element of ll
    current = linked_list.head
    while current is not None:
        next_node = current.next
        priority = current.request.priority
        # first pass fill new sorted list with head, after this ensure priority takes precedence so head is always high priority
        if sorted_head is None or priority < sorted_head.request.priority:
            current.next = sorted_head
            sorted_head = current
        # future passes, scan starts at head. compares current node priority and stops when priority critera met
        else:
            sorted_node_scan = sorted_head
            # find node in sorted where priority criteria is met
            while sorted_node_scan.next is not None and sorted_node_scan.next.request.priority <= priority:
                sorted_node_scan = sorted_node_scan.next
            # point current to the next of the scanned node
            current.next = sorted_node_scan.next
            # point scanned node at current
            sorted_node_scan.next = current
        # move to next node
        current = next_node
    # after sorting, update head and tail
    linked_list.head = sorted_head
    # grab tail, then return sorted list
    tail = sorted_head
    while tail is not None and tail.next is not None:
        tail = tail.next
    linked_list.tail = tail
    return linked_list


'''
Standard insertion sort on a dynamic array where sort precedence is set
by priority. Priority 1 takes precedence, 4 is weakest.
'''
def insertionSortArray(array):
    # grab buffer
    data = array.data
    for i in range(1, array.size):
        # compare current against sorted array
        current = data[i]
        j = i - 1

        # ensure sort happens when priority criteria are met
        while j >= 0 and current.priority < data[j].priority:
            data[j + 1] = data[j]
            j -= 1
        # drop current into gap
        data[j + 1] = current

    return array


'''
Merge sort on linked list.
Using two pointers, fast and slow, to divide list. Fast moves two steps,
slow moves one. When fast reaches the endpoint, slow has the midpoint.
Oldest request appears first. Three functions total:
1. mergeSortLinked(ll) is the wrapper. Calls mergeSortNodes(ll) to sort
the initially unsorted list.
2. mergeSortNodes(ll) takes a linked_list and sorts the nodes by recursive
calls and halving the chain. Once complete, calls mergeNodes(left, right) to
link nodes back together.
3. mergeNodes(left, right) takes a left and right set of nodes and merges them
back together

'''
def mergeSortLinked(linked_list):
    # sort chain, grab head of sorted list
    linked_list.head = mergeSortNodes(linked_list.head)
    # walk through nodes to the end
    scan = linked_list.head
    while scan is not None and scan.next is not None:
        scan = scan.next
    # set tail and return sorted list
    linked_list.tail = scan
    return linked_list

# sort nodes
def mergeSortNodes(head):
    # base case
    if head is None or head.next is None:
        return head
    # set pointers
    fast = head.next
    slow = head
    # find end of list with fast
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
    # slow helps find midpoint, set halves here
    second_half = slow.next
    # break the link
    slow.next = None
    # call recursively
    left = mergeSortNodes(head)
    right = mergeSortNodes(second_half)

    # relink the nodes
    return mergeNodes(left, right)


# relinks nodes after splitting
def mergeNodes(left, right):
    # left empty only return right
    if left is None:
        return right
    # right empty only return left
    if right is None:
        return left
    # left reported earlier than right, set head left and advance left node by one
    if left.request.reported_time <= right.request.reported_time:
        head = left
        left = head.next
    # right reported earlier than left, set head right and advance right node by one
    else:
        head = right
        right = right.next
    # node with earliest reporting time found. save to attach to next node that meets reporting criteria
    last = head

    # relink nodes until one chain is empty
    while left is not None and right is not None:
        # left reported earlier than right, link left node to last
        if left.request.reported_time <= right.request.reported_time:
            # lefts front node is older or equal, attach to last. move left to next node
            last.next = left
            left = left.next
        else:
            # rights front node is older, attach to last. move right to next node
            last.next = right
            right = right.next
        # move last to node we just linked
        last = last.next

    # if left still has values, these are newer reports. attach to last node. otherwise, right has newer reports
    if left is not None:
        last.next = left
    else:
        last.next = right

    return head


'''
Standard merge sort with added condition of placing requests with earlier reporting time in front of others
'''
def mergeSortArray(array):
    n = array.size
    # base case
    if n < 2:
        return array
    temp = [None] * n
    mergeSortRange(array.data, temp, 0, n)
    return array


def mergeSortRange(data, temp, low, high):
    # base case, already sorted
    if high - low < 2:
        return
    mid = (low + high) // 2

    # split array recursively
    mergeSortRange(data, temp, low, mid)
    mergeSortRange(data, temp, mid, high)

    # i reads left half, j reads right half, k writes position in temp
    i = low
    j = mid
    k = low

    # scan left and right
    while i < mid and j < high:
        # if left reported earlier than right, insert to temp
        if data[i].reported_time <= data[j].reported_time:
            temp[k] = data[i]
            i += 1
        else:
            temp[k] = data[j]
            j += 1

        k += 1

    # copy leftover data
    while i < mid:
        temp[k] = data[i]
        i += 1
        k += 1
    while j < high:
        temp[k] = data[j]
        j += 1
        k += 1

    # store sorted data
    for k in range(low, high):
        data[k] = temp[k]
