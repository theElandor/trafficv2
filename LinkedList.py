from collections import defaultdict
class ListNode:
    def __init__(self, val="", next=None):
        self.val = val
        self.next = next
        self.occ = []
