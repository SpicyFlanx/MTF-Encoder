# Mattias Park
# V00897015
# SENG 265 Assignment 2

import sys
import os
import time
import binascii

MAGIC_BYTEARRAY = bytearray([0xba,0x5e,0xba,0x11])

def write_magic_number(mtf):
    # 0xba  0x5e 0xba 0x11
    mtf.write(MAGIC_BYTEARRAY)

def encode_main():

    # Open input, output files
    try:
        i = open(sys.argv[1])
        filename = sys.argv[1].split(".")[0]
        o = open(filename + ".mtf", "wb")
    except:
        print("I/O Error! probably")
        sys.exit()

    write_magic_number(o)
    wordlist = []

    for line in i:
            splitline = line.split()
            # Tokenize the line
            for word in splitline:
                # do the stuff
                if word in wordlist:
                    # Word already in list: fetch index, move to front
                    n = wordlist.index(word) + 1
                    o.write(bytes([128 + n])) # write mtf symbol
                    wordlist.remove(word)
                    wordlist.insert(0, word)
                else: 
                    # Word doesn't appear: add to list
                    wordlist.insert(0, word)
                    n = len(wordlist) # seems like a hack but hey, it works
                    o.write(bytes([128 + n]))
                    o.write(word.encode('ascii')) # Write the word in the mtf
            o.write('\n'.encode('ascii'))

    i.close()
    o.close()
    sys.exit()

         
def decode_main():

    # Open input, output files
    try:
        i = open(sys.argv[1], 'rb')
        filename = sys.argv[1].split(".")[0]
        o = open(filename + ".txt", "w+")
    except:
        print("I/O Error! probably")
        sys.exit()

    # Check for magic num
    if i.read(4) != MAGIC_BYTEARRAY:
        print("Not a valid mtf file- check the magic number?")
        sys.exit()

    wordlist = []
    nextbyte = i.read(1)

    while nextbyte != b'':
        # First byte will be mtf symbol byte, and loop invariant should make
        # this land on such a byte in each loop

        # Deal with newlines
        if nextbyte == b'\n':
            o.write('\n')
            nextbyte = i.read(1)

        elif int.from_bytes(nextbyte, sys.byteorder) - 128 > len(wordlist):
            # Word we haven't yet encountered
            nextbyte = i.read(1)
            word = ''

            while ( 
                    (int.from_bytes(nextbyte, sys.byteorder) < 129) 
                    & (nextbyte != b'') & (nextbyte != b'\n')
                  ): # Read until another symbol char, or a newline, or EOF

                word += nextbyte.decode('ascii')
                nextbyte = i.read(1)

            o.write(word)
            if (nextbyte != b'') & (nextbyte != b'\n'):
                o.write(' ') # Add a space only between words
            wordlist.append(word)

        else:
            # Word already encountered
            # Resolve symbol into index on wordlist
            n = len(wordlist) - (int.from_bytes(nextbyte, sys.byteorder) - 128)
            word = wordlist[n]
            wordlist.remove(word) # Do the MTF stuff
            wordlist.append(word)
            o.write(word)
            nextbyte = i.read(1) 
            if (nextbyte != b'') & (nextbyte != b'\n'):
                o.write(' ') # Add a space only between words

    i.close()
    o.close()
    sys.exit()


command = os.path.basename(__file__)
if __name__ == "__main__" and command == "text2mtf.py":
  	encode_main()

elif __name__ == "__main__" and command == "mtf2text.py":
    decode_main()



