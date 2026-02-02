# Node class for singly linked list
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.index_in_array = -1  # track node position in auxiliary array

# Singly linked list with O(1) insert, remove, and get
class FSLL:
    def __init__(self):
        self.head = None
        self.nodes_array = []  # array to quickly find nodes by index

    def get(self, i):
        """Return value at logical index i in O(1)"""
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")
        return self.nodes_array[i].value

    def insert_at(self, i, value):
        """Insert value at logical index i in O(1)"""
        if i < 0 or i > len(self.nodes_array):
            raise IndexError("Invalid index")

        new_node = Node(value)
        # Always insert new node at head (O(1))
        new_node.next = self.head
        self.head = new_node

        # Add to array
        new_node.index_in_array = len(self.nodes_array)
        self.nodes_array.append(new_node)

        # Swap in array if inserting not at the end
        last_index = len(self.nodes_array) - 1
        if i != last_index:
            target_node = self.nodes_array[i]
            # Swap positions in array
            self.nodes_array[i], self.nodes_array[last_index] = new_node, target_node
            # Update indices
            new_node.index_in_array = i
            target_node.index_in_array = last_index

    def remove_at(self, i):
        """Remove node at logical index i in O(1)"""
        if i < 0 or i >= len(self.nodes_array):
            raise IndexError("Invalid index")

        target = self.nodes_array[i]
        head_node = self.head

        # Swap values with head if needed
        if target != head_node:
            target.value, head_node.value = head_node.value, target.value
            # Update array references for swapped nodes
            self.nodes_array[head_node.index_in_array] = target
            target.index_in_array = head_node.index_in_array

        # Remove head node
        self.head = self.head.next

        # Update array: swap last node into removed position
        last_index = len(self.nodes_array) - 1
        if i != last_index:
            last_node = self.nodes_array[last_index]
            self.nodes_array[i] = last_node
            last_node.index_in_array = i

        self.nodes_array.pop()

# Print linked list (physical view)
def print_linked_list(FSLL):
    curr = FSLL.head
    print("Linked list:", end=" ")
    while curr:
        print(curr.value, end=" -> ")
        curr = curr.next
    print("None")

# Print array view (logical view)
def print_array(FSLL):
    print("Array view: ", [node.value for node in FSLL.nodes_array])

# Main program
def main():
    my_list = FSLL()

    while True:
        print("\nMenu:")
        print("1 - Insert")
        print("2 - Get")
        print("3 - Remove")
        print("4 - Print List")
        print("5 - Exit")
        choice = input("Choose: ")

        if choice == "1":
            val = input("Value to insert: ")
            print(f"Valid indices: 0 to {len(my_list.nodes_array)} (use {len(my_list.nodes_array)} to append)")
            try:
                idx = int(input("Insert at index: "))
                my_list.insert_at(idx, val)
                print(f"Inserted '{val}' at index {idx}")
                print_array(my_list)
                print_linked_list(my_list)
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            if not my_list.nodes_array:
                print("List is empty")
                continue
            try:
                idx = int(input(f"Index to get (0-{len(my_list.nodes_array)-1}): "))
                print("Value:", my_list.get(idx))
                print_array(my_list)
                print_linked_list(my_list)
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
                print_array(my_list)
                print_linked_list(my_list)
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
