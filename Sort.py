""" Quicksort Implementation following CLRS"""


class Sort:

    @staticmethod
    def quicksort(arr, p, r):
        if p < r:
            q = Sort.partition(arr, p, r)
            Sort.quicksort(arr, p, q-1)
            Sort.quicksort(arr, q+1, r)
        return arr

    @staticmethod
    def partition(arr, p, r):
        x = arr[r]      # A[r] is the pivot element about which to partition the subarray A[p . . r]
        i = p - 1
        # j = p
        for j in range(p, r):
            if arr[j] <= x:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]  # swap elements
        arr[i+1], arr[r] = arr[r], arr[i+1]
        return i + 1
