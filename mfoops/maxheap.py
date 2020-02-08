from collections import defaultdict
from heapq import heapify, heappush, heappop

class MaxHeap:
    def __init__(self, init=[]):
        self._deleted = defaultdict(int)
        self._heap = [-x for x in init]
        heapify(self._heap)

    def max(self):
        top = heappop(self._heap)
        while self._deleted[top]:
            self._deleted[top] -= 1
            top = heappop(self._heap)
        if top in self._deleted:
            del self._deleted[top]
        heappush(self._heap, top)
        return -top

    def add(self, val):
        heappush(self._heap, -val)

    def remove(self, val):
        self._deleted[-val] += 1
