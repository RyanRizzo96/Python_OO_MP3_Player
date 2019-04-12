
""" Quicksort Implementation following CLRS"""


class Sort:
    my_list = [2, 8, 7, 1, 3, 5, 6, 4]

    def quicksort_title(arr, p, r):
        if p < r:
            q = Sort.partition(arr, p, r)
            Sort.quicksort_title(arr, p, q-1)
            Sort.quicksort_title(arr, q+1, r)

    def quicksort_artist(arr, p, r):
        if p < r:
            q = Sort.partition(arr, p, r)
            Sort.quicksort_artist(arr, p, q-1)
            Sort.quicksort_artist(arr, q+1, r)

    def quicksort_album(arr, p, r):
        if p < r:
            q = Sort.partition(arr, p, r)
            Sort.quicksort_album(arr, p, q-1)
            Sort.quicksort_album(arr, q+1, r)

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


Sort.quicksort_title(Sort.my_list, 0, len(Sort.my_list)-1)

for i in range(len(Sort.my_list)):
    print(Sort.my_list[i])
