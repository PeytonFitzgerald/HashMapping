# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def get_head(self):
        return self.head

    def get_size(self):
        return self.size

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function;
        self.size = 0

    def get_capacity(self):
        """
        :return: Capacity of the list
        """
        return self.capacity

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        for index in range(self.capacity):
            self._buckets[index].head = None
            self._buckets[index].size = 0

    def get_index(self, key):
        """
        Gets an index associated with a key
        :param key: Key to find index for
        :return: Index
        """
        return self._hash_function(key) % self.capacity

    def get_chain(self, index):
        """
        Gets the linked list at a given index
        :param index: index to get linked list
        :return: linked list at the given index
        """
        return self._buckets[index]

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # calculate the index for the key
        index = self._hash_function(key) % self.capacity
        # use the index to find that location in the list
        location = self._buckets[index]
        # see if the linked list at that location contains the key
        found_value = location.contains(key)
        if found_value:
            # if its found, return the value associated with that key
            return found_value.value
        else:
            return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # store capacity and bucket list, and then change the data member capacity to the new one / data member
        # bucket to the new one
        original_capacity = self.capacity
        old_buckets = self._buckets
        self.capacity = capacity

        self._buckets = []
        for index in range(capacity):
            # fill the new list with linked lists objects
            self._buckets.append(LinkedList())
        for pot_link_index in range(original_capacity):
            if old_buckets[pot_link_index].size != 0:
                # loop through old hashmap, for each that has a chain present (so size >0), get the head of thatl ist
                current = old_buckets[pot_link_index].head
                while current is not None:
                    # traverse the linked list and calculate a new hash value for each key/
                    new_index = self._hash_function(current.key) % self.capacity
                    location = self._buckets[new_index]
                    # put that key/value pair into the new hashmap using the newly calculated index
                    location.add_front(current.key, current.value)
                    current = current.next


    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # get the index for the given key
        index = self._hash_function(key) % self.capacity
        if self._buckets[index].size == 0:
            # if nothing is at that index, simply add it there and increase size by one
            self.size += 1
            self._buckets[index].add_front(key, value)
        else:
            # get the list at that location, see what it contains
            node_found = self._buckets[index].contains(key)
            if node_found:
                # if the key is already there, change the value associated with it
                node_found.value = value
            else:
                # otherwise, simply add
                self.size += 1
                self._buckets[index].add_front(key, value)


    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # get the index for the given key
        index = self._hash_function(key) % self.capacity
        # get that location in our list
        node_found = self._buckets[index].contains(key)
        if node_found:
            # if the passed key is there, remove it, and then decrement the size by 1
            self._buckets[index].remove(key)
            self.size -= 1

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # get the index for the given key
        index = self._hash_function(key) % self.capacity
        # get the list at the location
        list_location = self._buckets[index]
        if list_location.contains(key):
            # if the value is found, return True
            return True
        else:
            # otherwise, return False
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # initialize a counter
        counter = 0
        for linked_list_index in range(self.capacity):
            # for each list, increment the counter if the size is greater than 0
            if self._buckets[linked_list_index].size == 0:
                counter += 1
        return counter


    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return float(self.size / self.capacity)

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out



'''
keys = [i for i in range(1, 5000, 13)]

print(keys)

m_func1 = HashMap(1000, hash_function_1)
m_func2 = HashMap(1000, hash_function_2)

for key in keys:
    m_func1.put(str(key), key * 42)
    m_func2.put(str(key), key * 42)
print(m_func1.empty_buckets(), m_func1.size, m_func1.capacity)
print(m_func2.empty_buckets(), m_func2.size, m_func2.capacity)
print(m_func1.table_load())
print(m_func2.table_load())

keys = [i for i in range(1, 1000, 13)]
for key in keys:
    m.put(str(key), key * 42)
print(m.size, m.capacity)
for capacity in range(111, 1000, 117):
    m.resize_table(capacity)
    result = True
    for key in keys:
        result = result and m.contains_key(str(key))
        result = result and not m.contains_key(str(key + 1))
    print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
'''