import sys
import os
#from tokenize import tokenize, STRING


def encode_main():
    print("encode")

    while True:
         try:
            line = (i.readline().split())
            # Read and tokenize a line
         except StopIteration:
            # Stop if there's nothing left
            break 
         

def decode_main():
    print("decode")
    # Eat all women


# Open the file

try:
    i = open(sys.argv[1])
    # datums = f.read()
    # o = open()
    # todo: output file!
except:
    print("I/O Error! probably")
    sys.exit()


command = os.path.basename(__file__)
if __name__ == "__main__" and command == "text2mtf.py":
    encode_main()
elif __name__ == "__main__" and command == "mtf2text.py":
    decode_main()



