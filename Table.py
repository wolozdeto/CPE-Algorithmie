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
        i = 0
        while i < len(self.table):
            pos = self._rehash(key, i)
            if self.table[pos] is None:
                self.table[pos] = (key, value)
                self.size += 1
                if i > 0:
                    self.rehash_count += 1
                return
            elif self.table[pos][0] == key:
                self.table[pos] = (key, value)
                return
            else:
                i += 1
        raise Exception('Table is full')

    def delete(self, key):
        """
        Deletes a key-value pair from the table

        :param key: key to delete
        """
        i = 0
        while i < len(self.table):
            pos = self._rehash(key, i)
            if self.table[pos] is None:
                return
            elif self.table[pos][0] == key:
                self.table[pos] = None
                self.size -= 1
                return
            else:
                i += 1

    def exist(self, key):
        """
        Checks if a key exists in the table

        :param key: key to check
        :return: True if key exists, False otherwise
        """
        i = 0
        while i < len(self.table):
            pos = self._rehash(key, i)
            if self.table[pos] is None:
                return False
            elif self.table[pos][0] == key:
                return True
            else:
                i += 1
        return False

    def value(self, key):
        """
        Returns the value associated with a key

        :param key: key to check
        :return: value associated with key
        """
        i = 0
        while i < len(self.table):
            pos = self._rehash(key, i)
            if self.table[pos] is None:
                return None
            elif self.table[pos][0] == key:
                return self.table[pos][1]
            else:
                i += 1
        return None

    def union(self, other_table):
        """
        Returns a new table that is the union of the current table and the other table

        :param other_table: other table to union with
        :return: new table that is the union of the current table and the other table
        """
    def union(self, other_table):
        union_table = Table(len(self.table), self.hash_func, self.rehash_type)
        for pos in range(len(self.table)):
            if self.table[pos] is not None:
                union_table.insert(self.table[pos][0], self.table[pos][1])
        for pos in range(len(other_table.table)):
            if other_table.table[pos] is not None:
                union_table.insert(other_table.table[pos][0], other_table.table[pos][1])
        return union_table


def test_table(size=5, hash_func=lambda x: x % 5, rehash_type='linear'):
    # Create table with size 5, hash function f(x) = x % 5, and linear rehashing
    table = Table(size, hash_func, rehash_type)

    # Insert key/value pairs
    for i in range(5):
        table.insert(i, i)
    assert table.size == 5
    assert table.rehash_count == 0
    assert table.table == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

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

    # Check union of two tables
    table2 = Table(size, hash_func, rehash_type)
    for i in range(5):
        table2.insert(i, 4-i)
    union_table = table.union(table2)
    print(union_table.table)


test_table(size=5, hash_func=lambda x: x % 5, rehash_type='linear')
