def check_index(index, n, allow_end):
    """Helper function. TypeError for non-int (bool included), IndexError for out of range."""
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("Index must be an integer")
    upper = n if allow_end else n - 1
    if index < 0 or index > upper:
        raise IndexError(f"index {index} out of range for size {n}")

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
