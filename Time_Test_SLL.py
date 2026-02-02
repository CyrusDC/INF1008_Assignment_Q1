import time
import random
import matplotlib.pyplot as plt
import numpy as np

# ---------------- NORMAL SLL ----------------
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class NormalSLL:
    def __init__(self):
        self.head = None

    def insert_at(self, i, value):
        new_node = Node(value)
        if i == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            curr = self.head
            for _ in range(i - 1):
                curr = curr.next
            new_node.next = curr.next
            curr.next = new_node

    def remove_at(self, i):
        if i == 0:
            self.head = self.head.next
        else:
            curr = self.head
            for _ in range(i - 1):
                curr = curr.next
            curr.next = curr.next.next

    def get(self, i):
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.value

# ---------------- FAST SLL ----------------
class FastNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.index_in_array = -1

class FastSLL:
    def __init__(self):
        self.head = None
        self.nodes_array = []

    def insert_at(self, i, value):
        new_node = FastNode(value)
        new_node.next = self.head
        self.head = new_node

        new_node.index_in_array = len(self.nodes_array)
        self.nodes_array.append(new_node)

        last_index = len(self.nodes_array) - 1
        if i != last_index:
            node_at_target = self.nodes_array[i]
            self.nodes_array[i] = new_node
            self.nodes_array[last_index] = node_at_target
            new_node.index_in_array = i
            node_at_target.index_in_array = last_index

    def remove_at(self, i):
        target = self.nodes_array[i]
        head_node = self.head

        if target != head_node:
            target.value, head_node.value = head_node.value, target.value
            self.nodes_array[head_node.index_in_array] = target
            target.index_in_array = head_node.index_in_array

        self.head = self.head.next

        last_index = len(self.nodes_array) - 1
        if i != last_index:
            last_node = self.nodes_array[last_index]
            self.nodes_array[i] = last_node
            last_node.index_in_array = i
        self.nodes_array.pop()

    def get(self, i):
        return self.nodes_array[i].value

# ---------------- HELPER: MOVING AVERAGE ----------------
def smooth(y, window=5):
    return np.convolve(y, np.ones(window)/window, mode='valid')

# ---------------- EXPERIMENT ----------------
sizes = list(range(10, 5000, 20))
normal_insert, normal_remove, normal_get = [], [], []
fast_insert, fast_remove, fast_get = [], [], []

TRIALS = 20  # repeat to smooth randomness

for n in sizes:
    normal = NormalSLL()
    fast = FastSLL()

    # Build initial lists
    for i in range(n):
        normal.insert_at(0, i)
        fast.insert_at(0, i)

    # -------- NORMAL SLL RANDOM TEST --------
    total_insert, total_remove, total_get = 0, 0, 0
    for _ in range(TRIALS):
        idx = random.randint(0, n-1)
        start = time.perf_counter()
        normal.insert_at(idx, 999)
        total_insert += time.perf_counter() - start

        idx = random.randint(0, n)
        start = time.perf_counter()
        normal.remove_at(idx)
        total_remove += time.perf_counter() - start

        idx = random.randint(0, n-1)
        start = time.perf_counter()
        _ = normal.get(idx)
        total_get += time.perf_counter() - start

    normal_insert.append(total_insert / TRIALS)
    normal_remove.append(total_remove / TRIALS)
    normal_get.append(total_get / TRIALS)

    # -------- FAST SLL RANDOM TEST --------
    total_insert, total_remove, total_get = 0, 0, 0
    for _ in range(TRIALS):
        idx = random.randint(0, n-1)
        start = time.perf_counter()
        fast.insert_at(idx, 999)
        total_insert += time.perf_counter() - start

        idx = random.randint(0, n)
        start = time.perf_counter()
        fast.remove_at(idx)
        total_remove += time.perf_counter() - start

        idx = random.randint(0, n-1)
        start = time.perf_counter()
        _ = fast.get(idx)
        total_get += time.perf_counter() - start

    fast_insert.append(total_insert / TRIALS)
    fast_remove.append(total_remove / TRIALS)
    fast_get.append(total_get / TRIALS)

# Apply smoothing
normal_insert_s = smooth(normal_insert)
normal_remove_s = smooth(normal_remove)
normal_get_s = smooth(normal_get)
fast_insert_s = smooth(fast_insert)
fast_remove_s = smooth(fast_remove)
fast_get_s = smooth(fast_get)
sizes_s = sizes[len(sizes)-len(normal_insert_s):]

# ---------------- GRAPH 1: NORMAL SLL ----------------
plt.figure(figsize=(8,6))
plt.plot(sizes_s, normal_insert_s, label="Insert (Random) O(n)")
plt.plot(sizes_s, normal_remove_s, label="Remove (Random) O(n)")
plt.plot(sizes_s, normal_get_s, label="Get (Random) O(n)")
plt.title("Normal SLL — Random Operations (Smoothed)")
plt.xlabel("Number of Nodes (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

# ---------------- GRAPH 2: FAST SLL ----------------
plt.figure(figsize=(8,6))
plt.plot(sizes_s, fast_insert_s, label="Insert (Random) O(1)")
plt.plot(sizes_s, fast_remove_s, label="Remove (Random) O(1)")
plt.plot(sizes_s, fast_get_s, label="Get (Random) O(1)")
plt.title("Fast SLL — Random Operations (Smoothed)")
plt.xlabel("Number of Nodes (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

# ---------------- GRAPH 3: COMPARISON ----------------
plt.figure(figsize=(10,7))
plt.plot(sizes_s, normal_insert_s, label="Normal Insert O(n)")
plt.plot(sizes_s, fast_insert_s, label="Fast Insert O(1)")
plt.plot(sizes_s, normal_remove_s, label="Normal Remove O(n)")
plt.plot(sizes_s, fast_remove_s, label="Fast Remove O(1)")
plt.plot(sizes_s, normal_get_s, label="Normal Get O(n)")
plt.plot(sizes_s, fast_get_s, label="Fast Get O(1)")
plt.title("Random Index Operations: Normal vs Fast SLL (Smoothed)")
plt.xlabel("Number of Nodes (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()
