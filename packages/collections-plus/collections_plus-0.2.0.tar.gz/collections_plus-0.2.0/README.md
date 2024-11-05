# collections-plus
A Python library implementing various data structures.

## Installation
You can install this package using `pip`:
```
pip install collections-plus
```
and import the library with
```python
import collections_plus
```
Please note that this code is in a pre-alpha state and will
likely contain bugs. 

## Basic Usage and Examples

Currently, collections-plus supports [Linked Lists](https://en.wikipedia.org/wiki/Linked_list) 
and Doubly Linked Lists.
Briefly speaking, a linked list is a data structure where each node stores both a value
and a pointer to the next node. This makes insertions and removals near the start very fast,
at the expense of slower indexing. A doubly linked list is similar, but nodes store pointers
to the previous nodes as well. This allows us to pop quickly from both sides, not just the start.

### Linked Lists

To create a Linked List, first import the class:
```python
from collections_plus import LinkedList
```
Then, you can create a Linked List like so:
```python
my_llist = LinkedList(1, 2, 3, "pi", 4)
```
Or, if you have an existing list, you can unpack it:
```python
sample_list = [1, 4, 3, 4]
sample_ll = LinkedList(*sample_list)
```
LinkedLists support most things you can do with a good old Python list. For instance,
you can index into, mutate, and delete nodes (unfortunately, slicing is not implemented
as of version 0.2.0):
```python
indexed = my_llist[1] # indexed = 2
my_llist[2] = "approx pi" # sets value to "approx pi"
del my_llist[1] 
print(my_llist) # LinkedList(1, "approx pi", "pi" 4)
```
Notably, you can `pop`, `append`, and `insert`:
```python
sample_ll.pop() # returns 1
print(sample_ll) # LinkedList(4, 3, 4)
sample_ll.pop(2) # returns 4
print(sample_ll) # LinkedList(4, 3)
sample_ll.append("game")
print(sample_ll) # LinkedList(4, 3, 'game')
sample_ll.insert(0, "lost")
print(sample_ll) # LinkedList('lost', 4, 3, 'game')
```
Generally, `pop`, `append`, and `insert` will most often be used to implement
a FILO or FIFO queue. Please note that `insert(-1, val)` is not equivalent to
`append(val)` - the value is inserted *before* the index. To insert to the end,
use `append` or `insert(len(llist), val)`.

You can also iterate over a linked list directly:
```python
for val in sample_ll:
    print(val) # will print 'lost', '4', '3', 'game'
```

This package also supports a variety of other functions that work very similar
to their equivalents for default lists:

- `len(llist)`
- `llist.extend(other)`
- `llist.count(val)`
- `llist.index(val)`
- `llist.remove(val)`
- `llist.copy()`
- Binary comparators `==`, `!=`, `<`, `<=`, `>`, `>=`
- Operators `+` and `*`

### Doubly Linked Lists

To create a Doubly Linked List, import and create similarly:

```python
from collections_plus import DoublyLinkedList

array = ['agent', 'blind', 'cross', 'door', 'entendre']
my_dll = DoublyLinkedList(*array)
```

Doubly linked lists support everything that linked lists support. However,
they also come with a few additional methods `lpop`, `rpop`, and `lappend`
(primarily to make implementing a queue easier):

```python
first = my_dll.lpop() # first = 'agent'
second = my_dll.lpop() # second = 'blind'
last = my_dll.rpop() # last = 'entendre'
my_dll.lappend('bass')
my_dll.append('edged')
print(my_dll) # DoublyLinkedList('bass', 'cross', 'door', 'edged')
```

In addition, because a doubly linked list keeps tracks of pointers
in both directions, you can quickly traverse the list backwards 
(as opposed to a singly linked list, which will be slower):

```python
for val in reversed(my_dll):
    print(val) # prints 'edged', 'door', 'cross', 'bass'
```

## Roadmap:

Data structures that are planned:

- Min and max heaps
- Priority queue
- Circularly linked lists
- Binary trees
- AVL tree
- Trie/Prefix tree
- Graphs
- Segment tree
- Disjoint set union




