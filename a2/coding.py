import sys
import os
#from tokenize import tokenize, STRING

def write_magic_number(mtf):
    pass

def encode_main():

    # Get output filename, create output file with .mtf
    filename = sys.argv[1].split(".")[0]
    o = open(filename + ".mtf", "w+")
    wordlist = []

    while True:
         try:
            line = [i.readline().split()]
            print(line)
            # Read and tokenize a line
            for word in line:
            	print(word)
                # do the stuff
                if word in wordlist:
                    print(wordlist.index(word) + 1)
                else: 
                    wordlist.insert(0, word) # Prepend word onto wordlist
                    n = str(len(wordlist))
                    print(n + " " + "word")

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
'''
elif __name__ == "__main__" and command == "ayylmao.py":
	print("ayylmao")
	encode_main()
'''



