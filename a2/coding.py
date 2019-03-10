import sys
import os
#from tokenize import tokenize, STRING

def write_magic_number(mtf):
    pass

def encode_main():

    # Get output filename, create output file with .mtf
    filename = sys.argv[1].split(".")[0]
    o = open(filename + ".mtf")
    wordlist = []

    while True:
         try:
            line = [i.readline().split()]
            # Read and tokenize a line
            for word in line:
                # do the stuff
                if not (word in wordlist):
                    wordlist.insert(0, word) # Prepend word onto wordlist
                    print(len(wordlist) + " " + "word")
                else: 
                    print(wordlist.index(word) + 1)

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



