"""
Implements the Linked List data structure. 

In a linked list, each node stores both a value and a reference
to the next node in the array. The first node is called the head.
The list ends when the final nodes points to None. This final node
is called the tail.

This implementation keeps track of both the length and the tail node.

Space complexity: O(n), with O(n) extra space
Time complexity:
    Arbitrary indexing or mutating: O(n)
    Known indexing or mutating: O(1)
"""

from typing import Any, Optional, Iterable
from functools import wraps

class LinkedListNode():
    """
    An individual node of a linked list.

    Attributes:
        value: the value to be stored in this node
        next: the next linked list node
    """

    def __init__(self, value: Any, next: Optional["LinkedListNode"] = None) -> None:
        self.value = value
        self.next = next

    def __str__(self):
        return f"LinkedListNode with value {self.value}"

    def __repr__(self):
        return self.__str__()

class LinkedList():
    """
    A linked list.

    Attributes:
        length: how many nodes are contained in the list
        head: the first LinkedListNode in the list
        tail: the last LinkedListNode in the list.
    """

    def __init__(self, *values: Optional[Iterable[Any]]) -> None:
        self._head = LinkedListNode(None) # sentinel node
        self._tail = self._head
        self._length = 0
        prev_node = self._head
        for val in values:
            node = LinkedListNode(val)
            prev_node.next = node
            prev_node = node
            self._length += 1
        # prev_node.next = self._tail
        self._tail = prev_node

    @staticmethod
    def index_into(force_pos_range=True, min_index_offset = 0, max_index_offset = 0):
        """
        Decorator to call the function once we have
        reached the proper index node.
        Default of indices allowed is (-len) to (+len), lower inclusive and 
        upper exclusive.
        """
        def decorator(func):

            @wraps(func)
            def wrapper(self, index: Optional[int] = 0, *args, **kwargs) -> None:
                min_index = -self._length + min_index_offset
                max_index = self._length + max_index_offset
                if not isinstance(index, int):
                    raise TypeError("Index into LinkedList must be an integer.")
                if not min_index <= index < max_index: 
                    raise IndexError("LinkedList index out of range.")
                if force_pos_range and index < 0: index += self._length
                return func(self, index, *args, **kwargs)

            return wrapper

        return decorator

    def _retrieve_node(self, index):
        """
        Returns the node found at `index` and the node at
        `index-1` as a tuple.
        """
        prev_node = self._head
        node = self._head.next
        for _ in range(index):
            prev_node = node
            node = node.next
        return prev_node, node

    def _bring_index_in_range(self, index):
        """
        If index is negative, returns the equivalent positive index.
        """
        return index if index >= 0 else index + self._length

    def __str__(self):
        """
        Returns a string representation of the LinkedList.
        Idential to __repr__.
        """
        return self.__repr__()

    def __repr__(self):
        """
        Returns a string representation of the LinkedList.
        Identical to __str__.
        """
        out = self.__class__.__name__ + "("
        node = self._head.next
        for idx in range(self._length):
            out += str(node.value)
            node = node.next
            if idx < self._length - 1: out += ", "
        out += ")"
        return out

    @index_into()
    def __getitem__(self, index: int, *args, **kwargs) -> Any:
        """
        Returns the value at the specified node.
        """
        _, node = self._retrieve_node(index)
        return node.value

    @index_into()
    def __setitem__(self, index: int, val: Any) -> None:
        """
        Sets the value at the specified node to `val`.
        """
        _, node = self._retrieve_node(index)
        node.value = val

    @index_into()
    def __delitem__(self, index: int) -> None:
        """
        Removes the value at the specified node and reroutes the pointers to
        stitch the LinkedList back together.
        """
        prev_node, node = self._retrieve_node(index)
        next_node = node.next
        prev_node.next = next_node
        self._length -= 1
        del self

    def __len__(self) -> int:
        """
        Returns the length of the LinkedList.
        """
        return self._length

    def __length_hint__(self):
        return NotImplemented

    def __iter__(self):
        """
        Returns a generator to iterate over the LinkedList.
        """
        node = self._head.next
        for _ in range(self._length):
            yield node.value
            node = node.next

    def _require_same_type(func):
        """
        Decorator for comparison functions, requires that both
        types are a LinkedList.
        """
        @wraps(func)
        def wrapper(self, other, *args, **kwargs):
            if not isinstance(other, self.__class__):
                name = self.__class__.__name__
                raise TypeError(f"Can only compare {name} to a {name}")
            return func(self, other, *args, **kwargs)

        return wrapper

    @_require_same_type
    def __eq__(self, other: "LinkedList") -> bool:
        """
        Magic method to implement the == and != binary operators.
        Checks for equality. Equality is defined as the value in each
        node for both Linked Lists being equal.
        """
        if len(self) != len(other):
            return False
        for self_val, other_val in zip(self, other):
            if self_val != other_val:
                return False
        return True

    # todo: the other ordering methods. 
    
    @_require_same_type
    def __lt__(self, other: "LinkedList") -> bool:
        """
        Magic method to implement the < and >= binary operators.
        Checks if the first list is less than the second list, element wise,
        in order. In other words, it compares the first element, and if they are
        equal, moves to the second, etc. 
        If every element is equal, it will check if the second list is longer
        than the first.
        Note that __ge__ is implemented by default by Python. It is just
        this function but with the arguments switched around.
        """
        for self_val, other_val in zip(self, other):
            if self_val == other_val:
                continue
            return self_val < other_val 
        return len(self) < len(other)

    @_require_same_type
    def __le__(self, other: "LinkedList") -> bool:
        """
        Magic method to implement the <= and > binary operators.
        Checks element wise in order, and if the lists are of equal length,
        checks if the second list has a length greater than or equal to the first.
        For more detail, see the documentation of __lt__.
        """
        for self_val, other_val in zip(self, other):
            if self_val == other_val:
                continue
            return self_val < other_val
        return len(self) <= len(other)

    @index_into()
    def pop(self, index: int) -> Any: 
        """
        Removes the node at the specified index and returns its value.
        Note that because of how decorators work, the type hints / autocomplete
        are probably lying to you.

        Args:
            index: optional int, the index of the node to remove and return.
                If blank, default is 0 (i.e. the first node of the list).

        Returns:
            the value at the specified node.
        """
        prev_node, node = self._retrieve_node(index)
        next_node = node.next
        prev_node.next = next_node
        out = node.value
        del node 
        self._length -= 1
        return out

    def append(self, value: Any) -> None:
        """
        Adds a new node to the end of the LinkedList with value `value`.

        Args:
            value: any type, the data to be stored in the node

        Returns: none
        """
        new_node = LinkedListNode(value)
        self._tail.next = new_node
        self._tail = new_node
        self._length += 1

    def extend(self, other: "LinkedList") -> None:
        """
        Extends the LinkedList with each value in `other`, in order.
        Note that it creates a copies of all the nodes in `other` and mutates itself.

        Args:
            other: the LinkedList to add to the end of the current one

        Returns: none
        """
        for val in other:
            self.append(val)

    def count(self, value: Any) -> int:
        """
        Counts how many times `value` occurs in the list.

        Args:
            self
            value: any type, the data to look for. Uses == comparison.

        Returns:
            an integer representing how many times `value` occurs.
        """
        out = 0
        for val in self:
            if val == value:
                out += 1
        return out

    def index(self, value: Any) -> int:
        """
        Returns the index of the first occurence of `value` in the LinkedList.
        If `value` was not found, raises a ValueError.

        Args:
            value: any type, the data to look for.

        Returns:
            an integer representing the located index.
        """
        for idx, val in enumerate(self):
            if val == value:
                return idx
        raise ValueError("Value was not found in LinkedList.")

    @index_into(max_index_offset=1)
    def insert(self, index: int, value: Any) -> None:
        """
        Inserts `value` into the LinkedList at position `index`. Note that because
        of function decorators, autocomplete/typehints may lie to you.

        Args:
            index: int, the index to insert the value at.
            value: any, the value to insert.

        Returns: none
        """
        if index == self._length:
            self.append(value)
            return
        prev_node, node = self._retrieve_node(index)
        new_node = LinkedListNode(value, node)
        prev_node.next = new_node
        self._length += 1
        # we won't actually insert into the end of the list, so everything is okay

    def remove(self, value: Any) -> None:
        """
        Removes the first occurence of `value` in the LinkedList. If the value
        is not found, raises a ValueError.

        Args:
            value: any, the data to look for.

        Returns: none
        """
        for idx, val in enumerate(self):
            if val == value:
                del self[idx]
                return
        raise ValueError("Value was not found in LinkedList.")

    def copy(self) -> "LinkedList":
        """
        Returns a copy of the LinkedList.

        Args: none

        Returns: a LinkedList object with the same values as the original.
        """
        out = self.__class__(*(self))
        return out

    @_require_same_type
    def __add__(self, other: "LinkedList") -> "LinkedList":
        """
        Magic method to implement the + binary operator.
        Concatenates two lists and returns a new list, leaving both original
        lists alone.

        Args:
            other: the second LinkedList to concatenate to.

        Returns: a LinkedList with the values of the original (self) LinkedList,
            followed by the values of the second LinkedList.
        """
        out = self.__class__(*(self))
        out.extend(other)
        return out

    def __mul__(self, times: int) -> "LinkedList":
        """
        Magic method to implement the * binary operator.
        Extends the original list `times` times. Note that this is merely a shallow
        copy, so the new nodes maintain the same reference value as the old ones 
        (although they aren't the same nodes!)
        If `times` is nonpositive, returns an empty LinkedList.

        Args:
            times: int, the multiplication factor.

        Returns: a new LinkedList with the values of the original repeated
        `times` times.
        """
        if not isinstance(times, int):
            raise TypeError("Can only multiply LinkedList by an integer.")
        if times <= 0:
            return self.__class__()
        out = self.__class__(*(self))
        for _ in range(times-1):
            out.extend(self)
        return out



