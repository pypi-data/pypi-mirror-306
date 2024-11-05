"""
Implements the Doubly Linked List data structure. 

Similar to a Linked List, but each node stores a pointer to
both the next node *and* the previous node. This allows for fast
popping and appending at both ends, rather than only popping
at the front.

The terminology for head and tail are the same. 

Just like the Linked List, we keep track of the length dynamically.

Space complexity: O(n), with ~2*n extra space
Time complexity:
    Arbitrary indexing or mutating: O(n)
    Known indexing or mutating from either end: O(1)
"""

from typing import Any, Optional, Iterable
from .linked_list import LinkedList, LinkedListNode
from functools import wraps

class DoublyLinkedListNode(LinkedListNode):
    """
    An individual node of a doubly linked list.

    Attributes:
        value: the value to be stored in this node
        next: the next linked list node
        prev: the previous linked list node
    """

    def __init__(self, 
                 value: Any, 
                 next: Optional["LinkedListNode"] = None,
                 prev: Optional["LinkedListNode"] = None) -> None:
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        return f"DoublyLinkedListNode with value {self.value}"

class DoublyLinkedList(LinkedList):
    """
    Implementation of the Doubly Linked List.

    Attributes:
        self._head: sentinel node with .next pointing to first node
        self._tail: sentinel node with .prev pointing to last node
        self._length: dynamically updated length
    """

    def __init__(self, *values: Optional[Iterable[Any]]) -> None:
        self._head = DoublyLinkedListNode(None) # sentinel node
        self._tail = DoublyLinkedListNode(None) # sentinel node
        self._length = 0
        prev_node = self._head
        for val in values:
            node = DoublyLinkedListNode(val, prev=prev_node)
            prev_node.next = node
            prev_node = node
            self._length += 1
        prev_node.next = self._tail
        self._tail.prev = prev_node

    def _retrieve_node(self, index):
        """
        Returns the node found at `index`.
        """
        # forwards direction
        if index <= self._length // 2:
            node = self._head.next
            for _ in range(index):
                node = node.next
            return node
        # backwards direction
        node = self._tail
        for _ in range(self._length - index):
            node = node.prev
        return node

    @LinkedList.index_into()
    def __getitem__(self, index: int, *args, **kwargs) -> Any:
        """
        Magic method for indexing.
        Returns the value of the specified node.
        """
        node = self._retrieve_node(index)
        return node.value

    @LinkedList.index_into()
    def __setitem__(self, index: int, value: Any, *args, **kwargs) -> None:
        """
        Magic method for assignment into an index.
        Sets the value of the specified node to `value`.
        """
        node = self._retrieve_node(index)
        node.value = value

    @LinkedList.index_into()
    def __delitem__(self, index: int, *args, **kwargs) -> None:
        """
        Magic method for the del keyword.
        Deletes the specified node.
        """
        node = self._retrieve_node(index)
        node.prev.next = node.next
        node.next.prev = node.prev
        self._length -= 1
        del node

    @LinkedList.index_into(max_index_offset=1)
    def insert(self, index: int, value: Any):
        """
        Inserts a node with value `value` at position `index`. 
        The node is inserted before the node with position `index`.
        Returns none.
        """
        node = self._retrieve_node(index)
        new_node = DoublyLinkedListNode(value, next=node, prev=node.prev)
        node.prev.next = new_node
        node.prev = new_node
        self._length += 1
        
    def __reverse__(self):
        node = self._tail.prev
        for _ in range(self._length):
            yield node.value
            node = node.prev

    @LinkedList.index_into()
    def pop(self, index: int) -> Any:
        """
        Removes the specified node from the list and returns its value.
        """
        node = self._retrieve_node(index)
        val = node.value
        node.prev.next = node.next
        node.next.prev = node.prev
        self._length -= 1
        del node
        return val

    def lpop(self):
        """
        Removes the first node from the list and returns its value.
        """
        if self._length <= 0:
            raise IndexError("Cannot pop from empty DoubleLinkedList.")
        node = self._head.next
        val = node.value
        node.next.prev = self._head
        self._head.next = node.next
        self._length -= 1
        del node
        return val

    def rpop(self):
        """
        Removes the last node from the list and returns its value.
        """
        if self._length <= 0:
            raise IndexError("Cannot pop from empty DoubleLinkedList.")
        node = self._tail.prev
        val = node.value
        node.prev.next = self._tail
        self._tail.prev = node.prev
        self._length -= 1
        del node
        return val

    def append(self, value: Any) -> None:
        """
        Adds a node with value `value` at the end of the list.
        """
        node = self._tail
        new_node = DoublyLinkedListNode(value, next=node, prev=node.prev)
        node.prev.next = new_node
        node.prev = new_node
        self._length += 1

    def lappend(self, value: Any) -> None:
        node = self._head 
        new_node = DoublyLinkedListNode(value, next=node.next, prev=node)
        node.next.prev = new_node
        node.next = new_node
        self._length += 1
