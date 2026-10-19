# Kristena

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
