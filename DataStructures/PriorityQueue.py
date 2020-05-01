# -*- coding: utf-8 -*-
"""
Created on April 11, 2020.

@author: Camilo Martínez
"""

class PriorityQueue: 
    def __init__(self, capacity: int, __max__: bool = True) -> None: 
        self.queue = [None] * capacity
        self.__max__ = __max__
        
    def __str__(self) -> str: 
        return ' '.join([str(i) for i in self.queue if i is not None]) 
  
    def isEmpty(self) -> bool: 
        return len(self.queue) == 0
  
    def insert(self, data) -> None: 
        if self.isEmpty():
            self.queue[0] = data
        else:
            i = len(self.queue) - 1
            while i >= 0:
                if self.queue[i] is not None:
                    if self.__max__:
                        if data > self.queue[i]:
                            self.queue[i+1] = self.queue[i]
                        else:
                            break
                    else:
                        if data < self.queue[i]:
                            self.queue[i+1] = self.queue[i]
                        else:
                            break
                i -= 1
            self.queue[i+1] = data
        
    def poll(self) -> object: 
        item = self.queue[0] 
        del self.queue[0]
        return item 