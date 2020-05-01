# -*- coding: utf-8 -*-
"""
Created on April 11, 2020.

@author: Camilo Martínez
"""
from timeit import default_timer as timer

class SortingAlgorithm:
    
    @staticmethod
    def swap(array: list, i: int, j: int):
        temp = array[i]
        array[i] = array[j]
        array[j] = temp
        
    @staticmethod
    def less(array: list, i: int, j: int):
        return array[i] < array[j]
    
    @staticmethod
    def show_features(best_case: str, average_case: str, worst_case: str, memory: str, stable: bool):
        print("\tBest case: " + best_case)
        print("\tAverage case: " + average_case)
        print("\tWorst case: " + worst_case)
        print("\tMemory: " + memory)
        stable_str = 'no' if not stable else 'yes'
        print("\tStable: " + stable_str)

class HeapSort(SortingAlgorithm):

    @classmethod
    def sort(cls, array: list):
        print("Heapsort features:\n")
        cls.show_features('n log n', 'n log n', 'n log n', '1', False)
        print("\nInitial heap construction:\n")
        
        start = timer()
        
        i = int((len(array) - 2)/2) 
        j = 0
        while i >= 0:
            cls.heapify(array, i, len(array) - 1)
            if j > 0:
                print("\tHeap " + str(j) + ": " + str(array)[1:-1])
            i -= 1
            j += 1
            
        end = timer()    
        heap_construction_time = (end - start)*1000
        
        print("")
        
        print("Sorting:\n")
        
        start = timer()

        i = len(array) - 1
        j = 1
        while i > 0:
            cls.swap(array, 0, i)
            cls.heapify(array, 0, i-1)
            print("\tHeap " + str(j) + ": " + str(array[:-j])[1:-1])
            i -= 1
            j += 1
        
        end = timer()    
        sorting_time = (end - start)*1000
        total_time = heap_construction_time + sorting_time
        
        print("\nSorted array: " + str(array)[1:-1] + '\n')
        print("Running time estimates:\n")
        print("\tTime taken build the initial heap: {:.6} ms".format(heap_construction_time))
        print("\tTime taken to sort: {:.6} ms".format(sorting_time))
        print("\tTotal time: {:.6} ms".format(total_time))
        
    @staticmethod
    def heapify(array: list, i: int, m: int):
        while (2*i + 1 <= m):
            j = 2*i + 1
            if j < m:
                if array[j] < array[j+1]:
                    j += 1
            
            if HeapSort.less(array, i, j):
                HeapSort.swap(array, i, j)
                i = j
            else:
                i = m    

class SelectionSort(SortingAlgorithm):

    @classmethod
    def sort(cls, array: list) -> None:
        print("Selectionsort features:\n")
        cls.show_features('n log n', 'n log n', 'n log n', '1', False)
        print("\nSorting:\n")
        
        start = timer()

        k = 1
        for i in range(1, len(array)):
            j = i
            while j > 0 and cls.less(array, j, j-1):
                cls.swap(array, j, j-1)
                print("Array " + str(k) + ": " + str(array)[1:-1])
                j -= 1
                k += 1

        end = timer()    
        sorting_time = (end - start)*1000
        print("\nSorted array: " + str(array)[1:-1] + '\n')
        print("Running time estimates:\n")
        print("\tTime taken to sort: {:.6} ms".format(sorting_time))
        print("")
