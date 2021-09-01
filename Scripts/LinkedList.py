class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
    
    def setNext(self, node):
        self.next = node
        
    def __repr__(self):
        return self.val
    
##################################### Linked List code


class LinkedList:
    def __init__(self):
        self.head = None
        
    #Iterator
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            
    def __repr__(self):
        nodes = []
        for node in self:
            nodes.append(node.val)
        return str(nodes)
        # return nodes
    
    def add_to_tail(self, node):
        if self.head == None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.setNext(node)
        
    def add_to_head(self, node):
        if self.head == None:
            self.head = node
            return
        else:
            node.setNext(self.head)
            self.head = node
            return
        