from huffman_compressor import *
import os

def main():
    filename = input("Enter a filename: ")
    huffman = Huffman(filename)
    huffman.huffman_compress()
    filename, extension = os.path.splitext(filename)
    huffman.huffman_decompress(filename + ".bin")

if __name__ == "__main__":
    main()