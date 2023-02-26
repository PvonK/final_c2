""" ToDo ☐☑:

    ☑ agregar hilos a quicksort
    ☑ agregar hilos a mergesort

"""
import concurrent.futures as fut
import time



class Quicksort():
    def __init__(self, toSort=[]):
        self.toSort = toSort
        self.time = 0

    def partition_nomt(self, toSort):

        pivot = toSort.pop(-1)

        L = [i for i in toSort if i[1] < pivot[1]]
        R = [i for i in toSort if i[1] >= pivot[1]]

        return L, R, [pivot]

    def sort_nomt(self, toSort):
        low = 0
        high = len(toSort)-1

        L = toSort
        P=[]
        R=[]

        if low < high:

            L, R, P = self.partition_nomt(toSort)

            L = self.sort_nomt(L)
            R = self.sort_nomt(R)

        return L+P+R


    def partition(self, toSort):

        pivot = toSort.pop(-1)

        L=[]
        R=[]
        for i in toSort:
            if i[1] < pivot[1]:
                L.append(i)
            else:
                R.append(i)

        return L, R, [pivot]

    def _sort(self, toSort):
        hilos = fut.ThreadPoolExecutor(max_workers=50)

        low = 0
        high = len(toSort)-1

        L = toSort
        P=[]
        R=[]

        if low < high:

            L, R, P = self.partition(toSort)

            L=hilos.submit(self._sort, L)
            R=hilos.submit(self._sort, R)

            L=L.result()
            R=R.result()

        return L+P+R

    def sort(self, toSort):
        time_start = time.perf_counter()
        r=self._sort(toSort)
        time_end = time.perf_counter()
        self.time = time_end-time_start
        return r, time_end-time_start


    def __str__(self):
        return "quicksort"


class Bubble():
    def __init__(self, toSort=[]):
        self.toSort=toSort
        self.time = 0

    def sort(self, toSort=None):
        time_start = time.perf_counter()
        if toSort==None: toSort = self.toSort
        self.toSort = toSort

        n = len(self.toSort)

        for i in range(n-1):
            for j in range(0, n-i-1):
                if self.toSort[j][1] > self.toSort[j + 1][1]:
                    self.toSort[j], self.toSort[j + 1] = self.toSort[j + 1], self.toSort[j]

        time_end = time.perf_counter()
        self.time = time_end-time_start
        return self.toSort, time_end-time_start

    def __str__(self):
        return "bubble"


class Mergesort():
    def __init__(self, toSort=[]):
        self.toSort = toSort
        self.time = 0

    def sort(self, toSort):
        time_start = time.perf_counter()
        r=self._sort(toSort)
        time_end = time.perf_counter()
        self.time = time_end-time_start
        return r, time_end-time_start

    def sort_nomt(self, arr):
        left = 0
        right = len(arr)-1
        if left < right:

            middle = right//2

            L = arr[:middle+1]
            R = arr[middle+1:]

            left_arr = self.sort(L)
            right_arr = self.sort(R)

            arr = self.merge(left_arr, right_arr)

        return arr

    def _sort(self, arr):

        hilos = fut.ThreadPoolExecutor(max_workers=50)

        if 0 < len(arr)-1:

            middle = (len(arr)-1)//2

            L = arr[:middle+1]
            R = arr[middle+1:]

            left_fut = hilos.submit(self._sort, L)
            right_fut = hilos.submit(self._sort, R)

            arr = self.merge(arr, left_fut.result(), right_fut.result()) # pense crear un hilo aca pero es innecesario (ya es un hilo independiente)

        return arr


    def merge(self,arr, L, R):

        n1 = len(L)
        n2 = len(R)

        i = 0
        j = 0
        k = 0

        while i < n1 and j < n2:
            if L[i][1] <= R[j][1]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
        return arr

    def __str__(self):
        return "mergesort"
