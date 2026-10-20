from RequestList import RequestList

def check_index(index, n, allow_end):
    """Helper function. TypeError for non-int (bool included), IndexError for out of range."""
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("Index must be an integer")
    upper = n if allow_end else n - 1
    if index < 0 or index > upper:
        raise IndexError(f"index {index} out of range for size {n}")

class Node:

    def __init__(self, request):
        self.request = request
        self.next = None

class LinkedRequestList(RequestList):

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def linearSearchById(self, request_id):
      current = self.head
      position = 0
      while current is not None:
          if current.request.request_id == request_id:
              return position
          current = current.next
          position += 1
      return -1

    def check_duplicate(self, request):
        # check for duplicate ID, raise value error if same ID is found in database
        if self.findById(request.request_id) is not None:
            raise ValueError(f"duplicate request_id: {request.request_id}")

    def push(self, request):
        self.check_duplicate(request)
        node = Node(request)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def append(self, request):
        self.check_duplicate(request)
        node = Node(request)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def count(self):
        # size is updated with push, append and insert at. Just need to return self.size
        return self.size

    def node_walk(self, index):
        # points to node at desired index
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def getAt(self, index):
        check_index(index, self.size, allow_end=False)
        return self.node_walk(index).request

    def insertAt(self, index, request):
        check_index(index, self.size, allow_end=True)
        if index == 0:
            self.push(request)
        elif index == self.size:
            self.append(request)
        else:
            # push and append already check for duplicate, only need duplicate call for insertion outside of head and tail
            self.check_duplicate(request)
            prev = self.node_walk(index - 1)
            node = Node(request)
            node.next = prev.next
            prev.next = node
            self.size += 1

    def removeAt(self, index):
        check_index(index, self.size, allow_end=False)
        if index == 0:
            removed = self.head
            self.head = removed.next
            if self.head is None:
                self.tail = None
        else:
            prev = self.node_walk(index - 1)
            removed = prev.next
            prev.next = removed.next
            if removed is self.tail:
                self.tail = prev
        self.size -= 1
        return removed.request

    def findById(self, request_id):
        current = self.head
        while current is not None:
            if current.request.request_id == request_id:
                return current.request
            current = current.next
        return None

    def __len__(self):
        return self.size

    def __str__(self):
        list_contents = []
        if self.head is None:
            return 'None'
        else:
            current = self.head
            list_contents.append(str(current.request) + ' → ')
            while (current.next):
                current = current.next
                list_contents.append(str(current.request) + ' → ')
            list_contents.append('None')
            return ''.join(list_contents)
