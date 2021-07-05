import os

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __gt__(self, other):
        return self.freq > other.freq

class Heap():
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)

        self.sift_down(0, len(self.heap) - 1)

    def pop(self):
        last = self.heap.pop()
        if self.heap:
            pop_item = self.heap[0]
            self.heap[0] = last
            self.sift_up(0)
            return pop_item
        return last

    def sift_down(self, start, position):
        new_item = self.heap[position]
        while position > start:
            parent_index = (position - 1) >> 1
            parent = self.heap[parent_index]
            if new_item < parent:
                self.heap[position] = parent
                position = parent_index
                continue
            
            break
        self.heap[position] = new_item

    def sift_up(self, position):
        end = len(self.heap)
        start = position
        newitem = self.heap[position]

        child = 2 * position + 1    
        while child < end:

            right = child + 1
            if right < end and not self.heap[child] < self.heap[right]:
                child = right

            self.heap[position] = self.heap[child]
            position = child
            child = 2 * position + 1

        self.heap[position] = newitem
        self.sift_down(start, position)


class Huffman:

    def __init__(self, file):
        self.heap = Heap()
        self.file = file
        self.codes = {}
        self.reverse_codes = {}

    def create_freq_dict(self, input):
        freq = {}
        for char in input:
            if char not in freq:
                freq[char] = 0
            freq[char] += 1
        return freq

    def make_heap(self, freq):
        for key in freq:
            node = HeapNode(key, freq[key])
            self.heap.push(node)
            
    def merge(self):
        while len(self.heap.heap) > 1:
            first_node = self.heap.pop()
            second_node = self.heap.pop()

            merged_node = HeapNode(None, first_node.freq + second_node.freq)

            merged_node.left = first_node
            merged_node.right = second_node

            self.heap.push(merged_node)

    def code_helper(self, node, curr):
        if node is None:
            return 
        
        if node.char is not None:
            self.codes[node.char] = curr
            self.reverse_codes[curr] = node.char
        
        self.code_helper(node.left, curr + "0")
        self.code_helper(node.right, curr + "1")

    def get_codes(self):
        root = self.heap.pop()
        curr = ""
        self.code_helper(root, curr)

    def create_encoding(self, text):
        encoded = ""
        for char in text:
            encoded += self.codes[char]
        return encoded

    def add_padding(self, encoded_result):
        padding = 8 - len(encoded_result) % 8
        for i in range(padding):
            encoded_result += "0"
        padding_info = "{0:08b}".format(padding)

        encoded_result = padding_info + encoded_result

        return encoded_result

    def get_binary_arr(self, padded_result):
        binary_arr = bytearray()
        
        for i in range(0, len(padded_result), 8):
            byte = padded_result[i:i+8]
            binary_arr.append(int(byte, 2))
        
        return binary_arr

    def huffman_compress(self):
        filename, file_extension = os.path.splitext(self.file)
        output_location = filename + ".bin"

        with open(self.file, "r") as in_file, open(output_location, "wb") as out_file:
            input = in_file.read().rstrip()

            freq = self.create_freq_dict(input)

            self.make_heap(freq)
            self.merge()
            self.get_codes()

            encoded_result = self.create_encoding(input)

            padded_result = self.add_padding(encoded_result)

            binary_arr = self.get_binary_arr(padded_result)

            out_file.write(bytes(binary_arr))
            
    def remove_padding(self, bits):
        padding_info = bits[:8]

        padding = int(padding_info, 2)

        bits = bits[8:]
        encoded_result = bits[:-1 * padding]

        return encoded_result

    def decode(self, encoded_result):
        curr = ""
        decoded_result = ""

        for bit in encoded_result:
            curr += bit
            if curr in self.reverse_codes:
                char = self.reverse_codes[curr]
                decoded_result += char
                curr = ""
        
        return decoded_result

    def huffman_decompress(self, file_location):
        filename, file_extension = os.path.splitext(file_location)
        out_file = filename + "_decompressed.txt"

        with open(file_location, "rb") as in_file, open(out_file, "w+") as output:
            total_bits = ""

            byte = in_file.read(1)
            
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, "0")
                total_bits += bits
                byte = in_file.read(1)

            encoded_result = self.remove_padding(total_bits)

            decoded_result = self.decode(encoded_result)

            output.write(decoded_result)
