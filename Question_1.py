# Node class for singly linked list
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.index_in_array = -1  # keep track of where the node is in the array

# Fast singly linked list with O(1) insert, remove, and get
class FastSLL:
    def __init__(self):
        self.head = None
        self.nodes_array = []  # array to quickly find nodes by index

    # Get value at index i in O(1)
    def get(self, i):
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")
        return self.nodes_array[i].value

    # Insert value at index i
    def insert_at(self, i, value):
        if i < 0 or i > len(self.nodes_array):
            raise IndexError("Invalid index")

        new_node = Node(value)

        # Always add new node at head of linked list
        new_node.next = self.head
        self.head = new_node

        # Add node reference to the array
        new_node.index_in_array = len(self.nodes_array)
        self.nodes_array.append(new_node)

        # If inserting not at the end, swap in array so logical index is correct
        last_index = len(self.nodes_array) - 1
        if i != last_index:
            node_at_target = self.nodes_array[i]
            self.nodes_array[i] = new_node
            self.nodes_array[last_index] = node_at_target
            new_node.index_in_array = i
            node_at_target.index_in_array = last_index

    # Remove node at index i
    def remove_at(self, i):
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")

        target = self.nodes_array[i]
        head_node = self.head

        # Swap values with head if needed
        if target != head_node:
            target.value, head_node.value = head_node.value, target.value
            self.nodes_array[head_node.index_in_array] = target
            target.index_in_array = head_node.index_in_array

        # Remove the head node
        self.head = self.head.next

        # Update array
        last_index = len(self.nodes_array) - 1
        if i != last_index:
            last_node = self.nodes_array[last_index]
            self.nodes_array[i] = last_node
            last_node.index_in_array = i
        self.nodes_array.pop()

# Helper to print linked list
def print_linked_list(sll):
    curr = sll.head
    print("Linked list:", end=" ")
    while curr:
        print(curr.value, end=" -> ")
        curr = curr.next
    print("None")

# Helper to print array view
def print_array(sll):
    print("Array view: ", [node.value for node in sll.nodes_array])

# Main program
def main():
    my_list = FastSLL()

    while True:
        print("\nMenu:")
        print("1 - Insert")
        print("2 - Get")
        print("3 - Remove")
        print("4 - Show list")
        print("5 - Exit")
        choice = input("Choose: ")

        if choice == "1":
            val = input("Value to insert: ")
            print(f"Valid indices: 0 to {len(my_list.nodes_array)} (use {len(my_list.nodes_array)} to append)")
            try:
                idx = int(input("Insert at index: "))
                my_list.insert_at(idx, val)
                print(f"Inserted '{val}' at index {idx}")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            if not my_list.nodes_array:
                print("List is empty")
                continue
            try:
                idx = int(input(f"Index to get (0-{len(my_list.nodes_array)-1}): "))
                print("Value:", my_list.get(idx))
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            if not my_list.nodes_array:
                print("List is empty")
                continue
            try:
                idx = int(input(f"Index to remove (0-{len(my_list.nodes_array)-1}): "))
                val = my_list.get(idx)
                my_list.remove_at(idx)
                print(f"Removed '{val}'")
            except Exception as e:
                print("Error:", e)

        elif choice == "4":
            print_array(my_list)
            print_linked_list(my_list)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
