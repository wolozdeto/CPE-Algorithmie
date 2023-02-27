class Table:
    def __init__(self, table_size, hash_func, rehash_type):
        """
        Constructor for Table class

        :param table_size: size of the table
        :param hash_func: hash function to use
        :param rehash_type: rehash type to use
        """
        self.table = [None] * table_size
        self.hash_func = hash_func
        self.rehash_type = rehash_type
        self.size = 0
        self.rehash_count = 0

    def _rehash(self, key, i):
        """
        Rehash function to use for collision resolution

        :param key: key to rehash
        :param i: iteration number
        :return: rehashed key
        """
        if self.rehash_type == 'linear':
            return (key + i) % len(self.table)
        elif self.rehash_type == 'quadratic':
            return (key + i ** 2) % len(self.table)
        elif self.rehash_type == 'double':
            h1 = self.hash_func(key)
            h2 = 1 + (key % (len(self.table) - 1))
            return (h1 + i * h2) % len(self.table)

    def insert(self, key, value):
        """
        Inserts a key-value pair into the table

        :param key: key to insert
        :param value: value to insert
        :return: True if successful, False otherwise
        """
        pos = self.hash_func(key)
        if self.table[pos] is None or self.table[pos] == value:
            self.table[pos] = value
            self.size += 1
            return True
        else:
            for key in self.table:
                if key is None:
                    self.table[pos] = value
                    self.size += 1
                    return True
            raise Exception('Table is full')

    def delete(self, key):
        """
        Deletes a key-value pair from the table

        :param key: key to delete
        """
        pos = self.hash_func(key)
        if self.table[pos] is None:
            return False
        self.table[pos] = None
        self.size -= 1
        return True

    def exist(self, key):
        """
        Checks if a key exists in the table

        :param key: key to check
        :return: True if key exists, False otherwise
        """
        pos = self.hash_func(key)
        if self.table[pos] is None:
            return False
        return self.table[pos] is not None

    def value(self, key):
        """
        Returns the value associated with a key

        :param key: key to check
        :return: value associated with key
        """
        pos = self.hash_func(key)
        return self.table[pos]

    def union(self, other_table):
        """
        Returns a new table that is the union of the current table and the other table

        :param other_table: other table to union with
        :return: new table that is the union of the current table and the other table
        """
        union_table = Table(len(self.table), self.hash_func, self.rehash_type)
        for i in range(self.size):
            if self.table[i] is not None:
                union_table.insert(i, self.table[i])
            if other_table.table[i] is not None:
                union_table.insert(i, other_table.table[i])
        return union_table

    def intersection(self, other_table):
        """
        Returns a new table that is the intersection of the current table and the other table

        :param other_table: other table to intersect with
        :return: new table that is the intersection of the current table and the other table
        """
        intersection_table = Table(len(self.table), self.hash_func, self.rehash_type)
        for i in range(self.size):
            if self.table[i] is not None and other_table.table[i] is not None:
                intersection_table.insert(i, self.table[i])
        return intersection_table

    def display(self):
        """
        Displays the table
        """
        print('Table: {}'.format(self.table))


def test_table(size=5, hash_func=lambda x: x % 5, rehash_type='linear'):
    """
    Tests the Table class

    :param size: size of table
    :param hash_func: hash function to use
    :param rehash_type: rehash function to use
    """
    # Create table with size 5, hash function f(x) = x % 5, and linear rehashing
    table = Table(size, hash_func, rehash_type)

    # Insert key/value pairs
    for i in range(5):
        table.insert(i, i)
    assert table.size == 5
    assert table.rehash_count == 0
    assert table.table == [0, 1, 2, 3, 4]

    # Delete key/value pairs
    for i in range(5):
        table.delete(i)
    assert table.size == 0
    assert table.rehash_count == 0
    assert table.table == [None, None, None, None, None]

    # Check if key exists
    for i in range(5):
        table.insert(i, i)
        assert table.exist(i) is True
    assert table.size == 5
    assert table.rehash_count == 0

    # Check value of key
    for i in range(5):
        assert table.value(i) == i

    # Check union of two tables
    table2 = Table(size, hash_func, rehash_type)
    for i in range(1, 6):
        table2.insert(i, i)
    union_table = table.union(table2)
    union_table.display()

    # Check intersection of two tables
    intersection_table = table2.intersection(table)
    intersection_table.display()


test_table(size=5, hash_func=lambda x: x % 5, rehash_type='linear')
