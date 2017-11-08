# Written by Daniel Yang for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        odds = LinkedList()
        evens = LinkedList()
        
        i = self.head
        while i:
            if i.value%2:
                odds.append(i)
            else:
                evens.append(i)
            i = i.next_node
        if len(odds) == 0 or len(evens) == 0:
            return
        i = odds.head
        while i.next_node:
            i.value.next_node = i.next_node.value
            i = i.next_node
        i.value.next_node = evens.head.value
        i = evens.head
        while i.next_node:
            i.value.next_node = i.next_node.value
            i = i.next_node
        i.value.next_node = None
        self.head = odds.head.value