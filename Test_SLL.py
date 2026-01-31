import time
import matplotlib.pyplot as plt

# --- Your SLL implementation (already defined above) ---
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.index_in_array = -1

class SLL:
    def __init__(self):
        self.head = None
        self.nodes_array = []

    def get(self, i):
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")
        return self.nodes_array[i].value

    def insert_at(self, i, value):
        if i < 0 or i > len(self.nodes_array):
            raise IndexError("Invalid index")

        new_node = Node(value)
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
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")

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


# --- Traditional singly linked list ---
class LLNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class NormalSLL:
    def __init__(self):
        self.head = None
        self.size = 0

    def get(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Invalid index")
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.value

    def insert_at(self, i, value):
        if i < 0 or i > self.size:
            raise IndexError("Invalid index")
        new_node = LLNode(value)
        if i == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(i-1):
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node
        self.size += 1

    def remove_at(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Invalid index")
        if i == 0:
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(i-1):
                prev = prev.next
            prev.next = prev.next.next
        self.size -= 1


# --- Benchmark function ---
def benchmark(n=800):
    sll = SLL()
    normal = NormalSLL()

    # Benchmark insert
    start = time.time()
    for i in range(n):
        sll.insert_at(len(sll.nodes_array), f"val{i}")
    sll_insert_time = time.time() - start

    start = time.time()
    for i in range(n):
        normal.insert_at(i, f"val{i}")  # worst-case insert at end
    normal_insert_time = time.time() - start

    # Benchmark get
    start = time.time()
    for i in range(n):
        _ = sll.get(i)
    sll_get_time = time.time() - start

    start = time.time()
    for i in range(n):
        _ = normal.get(i)
    normal_get_time = time.time() - start

    # Benchmark remove
    start = time.time()
    for i in range(n-1, -1, -1):
        sll.remove_at(i)
    sll_remove_time = time.time() - start

    start = time.time()
    for i in range(n-1, -1, -1):
        normal.remove_at(i)
    normal_remove_time = time.time() - start

    return {
        "SLL": [sll_insert_time, sll_get_time, sll_remove_time],
        "NormalSLL": [normal_insert_time, normal_get_time, normal_remove_time]
    }


# --- Run benchmark and plot ---
results = benchmark(800)

labels = ["Insert", "Get", "Remove"]
x = range(len(labels))

plt.figure(figsize=(8,6))
plt.bar([i-0.2 for i in x], results["SLL"], width=0.4, label="Custom SLL")
plt.bar([i+0.2 for i in x], results["NormalSLL"], width=0.4, label="Normal SLL")
plt.xticks(x, labels)
plt.ylabel("Execution time (seconds)")
plt.title("Benchmark: Custom SLL vs Normal Singly Linked List (n=800)")
plt.legend()
plt.show()