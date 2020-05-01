# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:44:49 2020

@author: Camilo Martínez
"""
from DataStructures.PriorityQueue import PriorityQueue
from EntryManager import EntryManager

# Entry manager. Required to handle user input.
Entry_Manager = EntryManager(__file__)

class Checker:
    
    @staticmethod
    def show_sequence(priority_queue_type: str, sequence: list) -> None:
        n = len(sequence)
        is_max_pq = True if priority_queue_type == 'max' else False
        pq = PriorityQueue(n, is_max_pq)

        for i in sequence:        
            print('\t' + str(i) + ": ", end='')
            deleted_item = None
            if i != '*':
                pq.insert(i)
            else:
                deleted_item = pq.poll()

            print(pq, end='')
            c = len(str(pq))
            if deleted_item is not None:
                if pq.isEmpty():
                    print("[]", end='')

                print(" "*(2*n - c) + "Deleted item: " + str(deleted_item))
            else:
                print("")

def main():
    print("*Remember '*' means a call to .poll(), which deletes either the max- or minimum priority element*\n")
    pq_type = Entry_Manager.get_str_input("Define your priority queue", ["max", "min"], "max")
    sequence_str = input("Input your sequence: ")
    sq = [char for char in sequence_str]
    print("\nResults:\n")
    Checker.show_sequence(pq_type, sq)
