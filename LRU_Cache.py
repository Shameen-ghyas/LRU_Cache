import tkinter as tk
from tkinter import font, messagebox

class DLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.right = None
        self.left = None

    def insert(self, node):  # function to insert a node
        p = self
        q = node
        r = p.right
        p.right = q
        q.left = p
        q.right = r
        if r is not None:
            r.left = q

    def delete(self):    # function to delete a node
        p = self.left
        q = self
        r = self.right
        if p is not None:
            p.right = r
        if r is not None:
            r.left = p
        if p is None:
            return r
        return p

class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.head = DLNode(0, 0)
        self.tail = DLNode(0, 0)
        self.head.right = self.tail
        self.tail.left = self.head
        self.cache = {}
        self.misses = 0
        self.accesses = 0
        self.hits = 0


    def get(self, key):   # function to retrieve a key
        self.accesses += 1
        if key in self.cache:
            node = self.cache[key]
            node.delete()
            self.head.insert(node)
            return node.value
        else:
            self.misses += 1
            return -1

    def put(self, key, value):  # function to put a key-value pair
        self.accesses += 1
        if key in self.cache:
            self.hits+=1
            node = self.cache[key]
            node.value = value
            node.delete()
            self.head.insert(node)
        else:
            self.misses += 1
            if len(self.cache) == self.capacity:
                lru_node = self.tail.left
                lru_node.delete()
                self.cache.pop(lru_node.key)
            new_node = DLNode(key, value)
            self.head.insert(new_node)
            self.cache[key] = new_node

    def traverse(self):    # function to traverse the lru cache
        current = self.head.right
        items = []
        while current != self.tail:
            items.append((current.key, current.value))
            current = current.right
        return items

    def miss_rate(self):  # function to calculate miss rate
        if self.accesses == 0:
            return "0%"
        return f'{round((self.misses / self.accesses) * 100, 2)}%'

# Testing LRU Cache and calculating miss rate
def generate_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes


def test_lru_cache():
    capacity = 50
    lru_cache = LRU(capacity)

    for i in range(50):
        lru_cache.put(i, i)
    print("No. of accesses:", lru_cache.accesses)
    print("No. of misses:",lru_cache.misses)
    print("Initial Miss Rate:",lru_cache.miss_rate())

    for i in range(1, 50, 2):
        lru_cache.get(i)
    print("\nNo. of accesses:", lru_cache.accesses)
    print("No. of misses:", lru_cache.misses)
    print("odd miss rate:", lru_cache.miss_rate())

    prime_keys = generate_primes(100)
    for key in prime_keys:
        lru_cache.put(key, key)
    print("\nNo. of accesses:", lru_cache.accesses)
    print("No. of misses:", lru_cache.misses)
    print("Final miss rate:", lru_cache.miss_rate())

test_lru_cache()

# Testing LRU cache functionality
print("\nTESTING LRU CACHE")
lru_cache = LRU(2)
lru_cache.put(1, 1)  # cache is {1=1}
lru_cache.put(2, 2)  # cache is {1=1, 2=2}
print(lru_cache.get(1))  # returns 1
lru_cache.put(3, 3)  # evicts key 2, cache is {1=1, 3=3}
print(lru_cache.get(2))  # returns -1 (not found)
lru_cache.put(4, 4)  # evicts key 1, cache is {4=4, 3=3}
print(lru_cache.get(1))  # returns -1 (not found)
print(lru_cache.get(3))  # returns 3
print(lru_cache.get(4))  # returns 4

print("Miss rate:", lru_cache.miss_rate())

class LRUCacheGUI:
    def __init__(self, root, capacity):
        self.lru_cache = LRU(capacity)
        root.title("LRU Cache")
        root.geometry("800x500")
        root.configure(bg="#f5e6cc")
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        label_font = font.Font(family="Helvetica", size=10)
        button_font = font.Font(family="Helvetica", size=9, weight="bold")
        self.title_label = tk.Label(root, text="LRU Cache", font=title_font, bg="#f5e6cc", fg="#3b3a36")
        self.title_label.pack(pady=5)
        self.key_label = tk.Label(root, text="Key:", font=label_font, bg="#f5e6cc", fg="#3b3a36")
        self.key_label.pack()
        self.key_entry = tk.Entry(root, font=label_font, width=10)
        self.key_entry.pack(pady=2)
        self.value_label = tk.Label(root, text="Value:", font=label_font, bg="#f5e6cc", fg="#3b3a36")
        self.value_label.pack()
        self.value_entry = tk.Entry(root, font=label_font, width=10)
        self.value_entry.pack(pady=2)
        self.put_button = tk.Button(root, text="Put", font=button_font, command=self.put_value, bg="#d4a373",fg="white")
        self.put_button.pack(pady=5)
        self.get_button = tk.Button(root, text="Get", font=button_font, command=self.get_value, bg="#d4a373",fg="white")
        self.get_button.pack(pady=5)
        self.canvas = tk.Canvas(root, width=700, height=150, bg="#fdf3e7")
        self.canvas.pack(pady=5)
        self.miss_rate_label = tk.Label(root, text="Miss Rate: 0%", font=label_font, bg="#f5e6cc", fg="#3b3a36")
        self.miss_rate_label.pack(pady=5)
        
    def put_value(self):
        try:
            key = int(self.key_entry.get())
            value = int(self.value_entry.get())
            self.lru_cache.put(key, value)
            self.update_canvas()
            self.update_miss_rate()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for key and value.")

    def get_value(self):
        try:
            key = int(self.key_entry.get())
            result = self.lru_cache.get(key)
            if result == -1:
                messagebox.showinfo("Key Not Found", f"Key {key} not found in cache.")
            self.update_canvas()
            self.update_miss_rate()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for key.")

    def update_canvas(self):
        self.canvas.delete("all")
        items = self.lru_cache.traverse()
        x, y = 10, 50
        for key, value in items:
            self.canvas.create_rectangle(x, y, x + 50, y + 30, fill="#d4a373", outline="#3b3a36")
            self.canvas.create_text(x + 25, y + 15, text=f"{key}:{value}", fill="white")
            x += 70

    def update_miss_rate(self):
        miss_rate = self.lru_cache.miss_rate()
        self.miss_rate_label.config(text=f"Miss Rate: {miss_rate}")

root = tk.Tk()
gui = LRUCacheGUI(root, capacity=15)
root.mainloop()
