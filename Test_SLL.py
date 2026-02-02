import time
import sys
import matplotlib.pyplot as plt
import random

sys.setrecursionlimit(20000)

class FastNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.array_index = -1

class FastSLL:
    def __init__(self):
        self.head = None
        self.lookup = []

    # O(1) Insert at Head
    def insert(self, value):
        new_node = FastNode(value)
        new_node.next = self.head
        self.head = new_node
        new_node.array_index = len(self.lookup)
        self.lookup.append(new_node)

    # O(1) Insert at Specific Index (Displacement)
    def insert_at(self, i, value):
        if i < 0 or i > len(self.lookup): return
        self.insert(value) # Add to head/end first
        
        last_idx = len(self.lookup) - 1
        if i != last_idx:
            # Swap with target
            self.lookup[i], self.lookup[last_idx] = self.lookup[last_idx], self.lookup[i]
            self.lookup[i].array_index = i
            self.lookup[last_idx].array_index = last_idx

    # O(1) Get
    def get(self, i):
        return self.lookup[i].value

    # O(1) Delete at Head
    def delete(self):
        if not self.head: return
        self.remove_at(0) 

    # O(1) Remove at Specific Index (Swap-and-Pop)
    def remove_at(self, i):
        if i < 0 or i >= len(self.lookup): return
        target = self.lookup[i]
        head = self.head
        
        # Swap values with head
        if target is not head:
            target.value, head.value = head.value, target.value
            head_idx = head.array_index
            self.lookup[head_idx] = target
            target.array_index = head_idx
        
        # Delete head
        self.head = self.head.next
        
        # Swap array hole with last
        last_idx = len(self.lookup) - 1
        if i != last_idx:
            last = self.lookup[last_idx]
            self.lookup[i] = last
            last.array_index = i
        self.lookup.pop()


class StandardNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class StandardSLL:
    def __init__(self):
        self.head = None
        self.size = 0

    # O(1) Insert at Head
    def insert(self, value):
        new_node = StandardNode(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    # O(N) Insert at Index i
    def insert_at(self, i, value):
        if i == 0: 
            self.insert(value)
            return
        curr = self.head
        for _ in range(i - 1):
            if curr is None: return
            curr = curr.next
        new_node = StandardNode(value)
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    # O(N) Get
    def get(self, i):
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.value

    # O(1) Delete at Head
    def delete(self):
        if self.head:
            self.head = self.head.next
            self.size -= 1

    # O(N) Remove at Index i
    def remove_at(self, i):
        if i == 0:
            self.delete()
            return
        curr = self.head
        for _ in range(i - 1):
            curr = curr.next
        if curr and curr.next:
            curr.next = curr.next.next
            self.size -= 1


def run_dense_comparison():
    max_size = 5000
    sizes = list(range(1, max_size + 1))
    
    # Data storage structure
    metrics = {
        "insert_head": {"fast": [], "std": []},
        "insert_at":   {"fast": [], "std": []},
        "get":         {"fast": [], "std": []},
        "delete_head": {"fast": [], "std": []},
        "delete_at":   {"fast": [], "std": []}
    }

    print(f"Benchmarking every size from 1 to {max_size}...")
    
    fast_list = FastSLL()
    std_list = StandardSLL()
    
    for n in sizes:
        # Grow lists to size n (using fast head insert)
        fast_list.insert(n)
        std_list.insert(n)
        
        target = n // 2 # Test middle index
        
        # INSERT HEAD (Should be fast for both)
        t0 = time.perf_counter()
        fast_list.insert(999)
        metrics["insert_head"]["fast"].append((time.perf_counter() - t0) * 1000)
        # Cleanup (remove the item we just added so size stays 'n')
        fast_list.delete() 
        
        t0 = time.perf_counter()
        std_list.insert(999)
        metrics["insert_head"]["std"].append((time.perf_counter() - t0) * 1000)
        std_list.delete()

        # INSERT AT MIDDLE (Fast vs Slow)
        t0 = time.perf_counter()
        fast_list.insert_at(target, 888)
        metrics["insert_at"]["fast"].append((time.perf_counter() - t0) * 1000)
        fast_list.remove_at(target) # Cleanup
        
        t0 = time.perf_counter()
        std_list.insert_at(target, 888)
        metrics["insert_at"]["std"].append((time.perf_counter() - t0) * 1000)
        std_list.remove_at(target) # Cleanup

        # GET MIDDLE (Fast vs Slow)
        t0 = time.perf_counter()
        fast_list.get(target)
        metrics["get"]["fast"].append((time.perf_counter() - t0) * 1000)
        
        t0 = time.perf_counter()
        std_list.get(target)
        metrics["get"]["std"].append((time.perf_counter() - t0) * 1000)

        # DELETE HEAD (Should be fast for both)
        # Temporarily add dummy node to delete
        fast_list.insert(0); std_list.insert(0)
        
        t0 = time.perf_counter()
        fast_list.delete()
        metrics["delete_head"]["fast"].append((time.perf_counter() - t0) * 1000)
        
        t0 = time.perf_counter()
        std_list.delete()
        metrics["delete_head"]["std"].append((time.perf_counter() - t0) * 1000)

        # DELETE AT MIDDLE (Fast vs Slow)
        # Temporarily insert dummy at target to delete
        fast_list.insert_at(target, 777)
        std_list.insert_at(target, 777)
        
        t0 = time.perf_counter()
        fast_list.remove_at(target)
        metrics["delete_at"]["fast"].append((time.perf_counter() - t0) * 1000)
        
        t0 = time.perf_counter()
        std_list.remove_at(target)
        metrics["delete_at"]["std"].append((time.perf_counter() - t0) * 1000)

    return sizes, metrics

# Plotting
sizes, metrics = run_dense_comparison()

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
ax_list = axes.flatten()

ops_map = [
    ("insert_head", "Insert (Head)"),
    ("insert_at",   "Insert At (Middle)"),
    ("get",         "Get (Middle)"),
    ("delete_head", "Delete (Head)"),
    ("delete_at",   "Delete At (Middle)")
]

dot_size = 2
alpha_val = 0.5

for i, (key, title) in enumerate(ops_map):
    ax = ax_list[i]
    
    # Scatter plot for dense data
    ax.scatter(sizes, metrics[key]["fast"], s=dot_size, alpha=alpha_val, label="Fast SLL (O(1))", color="blue")
    ax.scatter(sizes, metrics[key]["std"], s=dot_size, alpha=alpha_val, label="Standard SLL (O(N))", color="orange")
    
    ax.set_title(title)
    ax.set_xlabel("List Size (N)")
    ax.set_ylabel("Time (ms)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)

# Remove empty 6th subplot
fig.delaxes(ax_list[5])

plt.tight_layout()
plt.savefig('dense_all_operations_1000.png')
print("Benchmark Complete. Graph saved as 'dense_all_operations_1000.png'")
plt.show()