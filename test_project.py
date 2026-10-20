class MaintenanceRequest:

    def __init__(self, request_id, building, category, priority, reported_time, status):
        self.request_id = request_id
        self.building = building
        self.category = category
        self.priority = priority
        self.reported_time = reported_time
        self.status = status

    def __str__(self):
        return (f"#{self.request_id} {self.building} {self.category} "
                f"P{self.priority} t={self.reported_time} {self.status}")


class ArrayRequestList:

    def __init__(self, initial_capacity=4):
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be at least 1")
        self.capacity = initial_capacity
        self.data = [None] * self.capacity
        self.size = 0

    def linearSearchById(self, request_id):
      for i in range(self.size):
          if self.data[i].request_id == request_id:
              return i
      return -1

    def _resize(self, new_capacity):

        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def insertAt(self, index, request):

        if index < 0 or index > self.size:
            raise IndexError("index out of range")


        for i in range(self.size):
            if self.data[i].request_id == request.request_id:
                raise ValueError("duplicate request_id")


        if self.size == self.capacity:
            self._resize(self.capacity * 2)


        i = self.size
        while i > index:
            self.data[i] = self.data[i - 1]
            i = i - 1


        self.data[index] = request
        self.size = self.size + 1

    def push(self, request):
        self.insertAt(0, request)

    def append(self, request):
        self.insertAt(self.size, request)

    def count(self):
        return self.size

    def getAt(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        return self.data[index]

    def removeAt(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        removed = self.data[index]


        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]

        self.data[self.size - 1] = None
        self.size = self.size - 1
        return removed

    def findById(self, request_id):
        for i in range(self.size):
            if self.data[i].request_id == request_id:
                return self.data[i]
        return None

    def __len__(self):
        return self.size

    def __str__(self):
        if self.size == 0:
            return "(empty)"
        result = ""
        for i in range(self.size):
            if i > 0:
                result = result + "\n"
            result = result + str(self.data[i])
        return result


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

class LinkedRequestList:

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
            list_contents.append(str(current.data) + ' → ')
            while (current.next):
                current = current.next
                list_contents.append(str(current.data) + ' → ')
            list_contents.append('None')
            return ''.join(list_contents)



# Create reproducible dataset of campus maintenance requests
# row contains: (request_id, building, categoy, priority, reported_time, status)

sample_requests = [
    (1001, "CASE", "HVAC", 1, 900, "open"),
    (1002, "ECNW", "plumbing", 2, 815, "in progress"),
    (1003, "ECCR", "electrical", 1, 830, "open"),
    (1004, "AERO", "cleaning", 4, 845, "closed"),
    (1005, "ATLAS", "lighting", 3, 900, "open"),
    (1006, "NORLIN", "plumbing", 2, 915, "open"),
    (1007, "CASE", "HVAC", 3, 930, "in progress"),
    (1008, "ECNW", "elevator", 1, 945, "open"),
    (1009, "ECCR", "cleaning", 4, 1000, "closed"),
    (1010, "ATLAS", "electrical", 2, 1015, "open")
]

print("This dataset created with", len(sample_requests), "requests")


# Kristena

# populate the array and linked list

array_requests = ArrayRequestList()
linked_requests = LinkedRequestList()

# adding 10 maintenance requests to both structures

for row in sample_requests:

  request_for_array = MaintenanceRequest(
      row[0], row[1], row[2], row[3], row[4], row[5])

  request_for_linked = MaintenanceRequest(
      row[0], row[1], row[2], row[3], row[4], row[5])

  array_requests.append(request_for_array)
  linked_requests.append(request_for_linked)

# check both structures contain 10 requests

assert array_requests.count() == 10
assert linked_requests.count() == 10

# check requests stored in correct order

for i in range(10):
  assert array_requests.getAt(i).request_id == sample_requests[i][0]
  assert linked_requests.getAt(i).request_id == sample_requests[i][0]

print("Both structures have successfully loaded the dataset")



from re import M
# Kristena

# demonstrate insertion operations

array_test = ArrayRequestList()
linked_test = LinkedRequestList()

# run the same test on both structures

for structure in [array_test, linked_test]:
  assert structure.count() == 0

  # add first additional request
  structure.append(MaintenanceRequest(1012, "CASE", "HVAC", 1, 800,
                                      "open"))

  # test structure with 1 element
  assert structure.count() == 1
  assert structure.getAt(0).request_id == 1012

  # add second additional request
  structure.append(MaintenanceRequest(1013, "ECNW", "plumbing", 2, 815,
                   "open"))

  # test structure with 2 elements
  assert structure.count() == 2

  # insert at the beginning with push()and test
  structure.push(MaintenanceRequest(1011, "ECCR", "electrical", 1, 830,
                                    "open"))
  assert structure.getAt(0).request_id == 1011

  # insert in the middle with insertAt()and test
  structure.insertAt(2, MaintenanceRequest(1014, "AERO", "cleaning", 4, 845,
                                        "open"))
  assert structure.getAt(2).request_id == 1014

  # insert at the end with insertAt() and test
  structure.insertAt(structure.count(),MaintenanceRequest(
      1015, "ATLAS", "lighting", 3, 900, "open"))
  assert structure.getAt(structure.count() - 1).request_id == 1015

  # check final order of 5 additional requests
  assert structure.count() == 5

  assert structure.getAt(0).request_id == 1011
  assert structure.getAt(1).request_id == 1012
  assert structure.getAt(2).request_id == 1014
  assert structure.getAt(3).request_id == 1013
  assert structure.getAt(4).request_id == 1015

print("The insertion tests passed for both structures")

# Kristena

# demonstrate removal operations

for structure in [array_test, linked_test]:

  # removal at the beginning and test
  removed = structure.removeAt(0)

  assert removed.request_id == 1011
  assert structure.count() == 4

  # removal in the middle and test
  removed = structure.removeAt(1)

  assert removed.request_id == 1014
  assert structure.count() == 3

  # remove at the end and test
  removed = structure.removeAt(structure.count()-1)

  assert removed.request_id == 1015
  assert structure.count() == 2

  # additional removal tests to verify structure

  # verify which request are left in set
  assert structure.getAt(0). request_id == 1012
  assert structure.getAt(1).request_id == 1013

  # remove remaining requests to make empty structure and confirm empty
  structure.removeAt(0)
  structure.removeAt(0)

  assert structure.count() == 0

print("All removal tests have passed for both structures")


# Kristena

# successful and unsuccessful searches

for structure in [array_requests, linked_requests]:

  # search for valid request that exists and test
  found = structure.findById(1003)

  assert found is not None
  assert found.request_id == 1003

  # search for an request that does not exist and test

  missing = structure.findById(2026)

  assert missing is None

  # confirm searches did not change structure
  assert structure.count() == 10

print("The Search tests passed for both structures")

# Kristena

# test for duplicate request IDs

for structure in [array_requests, linked_requests]:

  original_count = structure.count()

  # attempt to add a request with an ID that already exists

  try:
    structure.append(
        MaintenanceRequest(1003, "CASE", "HVAS", 1, 1000, "open"))

  except ValueError:
    pass

  else:
    assert False, "Duplicate request ID was accepted"

  assert structure.count() == original_count

print("The duplicate ID tests passed for both structures")


# Kristena

# test for invalid index

for structure in [array_requests, linked_requests]:

  # test negative index for getAt()

  try:
    structure.getAt(-1)

  except IndexError:
    pass

  else:
    assert False, "Negative index was accepted"

  # test out-of-range index for getAt()

  try:
    structure.getAt(95)

  except IndexError:
    pass

  else:
      assert False, "Out-of-range index was accepted"

  # test noninteger index for getAt()

  try:
    structure.getAt(3.5)

  except TypeError:
    pass

  else:
    assert False, "Noninteger index was accepted"

  # test negative index for removeAt()

  try:
    structure.removeAt(-1)

  except IndexError:
    pass

  else:
    assert False, "Negative removal index was accepted"

  # test out-of-range index for removeAt()

  try:
      structure.removeAt(95)

  except IndexError:
    pass

  else:
    assert False, "Out-of-range removal index was accepted"

  # test noninteger index for removeAt()

  try:
    structure.removeAt(3.5)

  except TypeError:
    pass

  else:
    assert False, "Noninteger removal index was accepted"

  # test negative index for insertAt()

  try:
    structure.insertAt(
        -1, MaintenanceRequest(2050, "CASE", "HVAC", 2, 1000, "open"))

  except IndexError:
    pass

  else:
    assert False, "negative insertion index was accepted"

  # test out-of-range index for insertAt()

  try:
    structure.insertAt(
        95, MaintenanceRequest(2095, "CASE", "HVAC", 2, 1000, "open"))

  except IndexError:
    pass

  else:
    assert False, "Out-of-range insertion index was accepted"

  # test noninteger index for insertAt()

  try:
    structure.insertAt(
        3.5, MaintenanceRequest(2095, "CASE", "HVAC", 2, 1000, "open"))

  except TypeError:
    pass

  else:
    assert False, "Noninteger insertion index was accepted"

# test to confirm invalid operations did not change the structure

  assert structure.count() == 10
  assert structure.getAt(0).request_id == 1001
  assert structure.getAt(9).request_id == 1010

print("Invalid index tests passed for both structures")


# Kristena

# test behavior after resizing the array

# Create new array with capacity 2

resize_test = ArrayRequestList(2)

assert resize_test.capacity == 2
assert resize_test.count() == 0

# Add 5 new requests to make the array resize

for i in range(5):
  resize_test.append(MaintenanceRequest(
      2000 + i, "CASE", "HVAC", 2, 900 + i, "open"))

# Test to confirm all 5 new were added

assert resize_test.count() == 5

# Test to confirm the capacity increased

assert resize_test.capacity >= 5

# Test to confirm the requests remain in the correct order

for i in range(5):
  assert resize_test.getAt(i).request_id == 2000 + i

# Test behavior after resizing (insertion)

resize_test.insertAt(2,
                     MaintenanceRequest(2010,
                                        "NORLIN", "plumbing", 1, 1000, "open"))

assert resize_test.getAt(2).request_id == 2010
assert resize_test.count() == 6

# Test behavior after resizing (removal)

removed = resize_test.removeAt(2)

assert removed.request_id == 2010
assert resize_test.count() == 5

# Test to confirm original requests still in correct order

for i in range(5):
  assert resize_test.getAt(i).request_id == 2000 + i

print("All dynamic array resizing tests passed")
