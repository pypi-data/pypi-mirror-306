# collections-plus
A Python library implementing various data structures.

## Installation
You can install this package using `pip`:
```
pip install collections-plus
```
and import the library with
```python3
import collections_plus
```
Please note that this code is in a pre-alpha state and will
likely contain bugs. 

## Basic Usage and Examples

Currently, collections-plus supports [Linked Lists](https://en.wikipedia.org/wiki/Linked_list). 
Briefly speaking, a linked list is a data structure where each node stores both a value
and a pointer to the next node. This makes insertions and removals near the start very fast,
at the expense of slower indexing.

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
as of version 0.1.0):
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
a FILO or FIFO queue. Please note that `insert(-1, val)` will also be slower than
`append(val)` because of the linked list structure.

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


