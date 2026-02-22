import heapq 
from dataclasses import dataclass 

# alta freq -> menos bits
# baixa freq -> mais bits


@dataclass
class Node:
    char: str
    freq: int
    left = None 
    right = None 

    def __lt__(self, other):
        return self.freq < other.freq 
    

def build_huffman_tree(chars, freq):
    priority_tree = []

    for char, f in zip(chars, freq):
        node = Node(char, f)
        priority_tree.append(node)

    heapq.heapify(priority_tree)

    while len(priority_tree) > 1:
        left = heapq.heappop(priority_tree)
        right = heapq.heappop(priority_tree)

        parent = Node(None, left.freq + right.freq)

        parent.left = left
        parent.right = right 

        heapq.heappush(priority_tree, parent)

    root = priority_tree[0]

    return root

def generate_codes(node, prefix="", codes={}):
    if node is None:
        return 

    if node.char is not None:
        codes[node.char] = prefix 

    generate_codes(node.left, prefix + "0", codes)
    generate_codes(node.right, prefix + "1", codes)

    return codes

def get_frequency(content: str):
    freqs = {}
    for char in content:
        if char in freqs:
            freqs[char] += 1
        else:
            freqs[char] = 1

    return freqs 

def compress(texto, codes):
    bits = ""
    for char in texto:
        bits += codes[char]
    return bits

def decompress(bits, root):
    resultado = ""
    node = root
    for bit in bits:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        
        if node.char is not None:  
            resultado += node.char
            node = root  
    return resultado

def main():
    texto = "aaaAAAbBBczz"
    freqs = get_frequency(texto)
    chars = list(freqs.keys())
    freq = list(freqs.values())
    
    root = build_huffman_tree(chars, freq)
    codes = generate_codes(root)
    print(codes)
    
    compressed = compress(texto, codes)
    print(f"Original: {len(texto) * 8} bits")
    print(f"Comprimido: {len(compressed)} bits")
    print(compressed)

    print(decompress(compressed, root))

if __name__ ==  "__main__":
    main()
