# Mattias Park
# V00897015
# SENG 265 Assignment 2

import sys
import os
import time
import binascii

MAGIC_BYTEARRAY = bytearray([0xba,0x5e,0xba,0x12])
MAGIC_BYTEARRAY_OLD = bytearray([0xba,0x5e,0xba,0x11])

def write_magic_number(mtf):
    # 0xba  0x5e 0xba 0x11
    mtf.write(MAGIC_BYTEARRAY)

def encode(filename):

    def write_mtf_symbols(n):
        if n < 121:
            # case 1: 1-120
            o.write(bytes([128 + n])) # write mtf symbol
        elif n > 120 and n < 376:
            #case 2: 121 - 375
            o.write(bytes([121 + 128]))
            o.write(bytes([n - 121]))   
        elif n > 375:
            #case 3: 376 - 65912
            o.write(bytes([122 + 128]))
            o.write(bytes([(n - 376) // 256]))
            o.write(bytes([(n - 376) % 256]))

    try:
        i = open(filename)
        file_base_name = filename.split(".")[0]
        o = open(file_base_name + ".mtf", "wb")
    except:
        print("I/O error! probably")
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
                    write_mtf_symbols(n)
                    wordlist.remove(word)
                    wordlist.insert(0, word)
                else: 
                    # Word doesn't appear: add to list
                    wordlist.insert(0, word)
                    n = len(wordlist) # seems like a hack but hey, it works
                    write_mtf_symbols(n)
                    o.write(word.encode('ascii')) # Write the word in the mtf
            o.write('\n'.encode('ascii'))

    i.close()
    o.close()
    sys.exit()


def decode(filename):

    # Open input, output files
    try:
        i = open(filename, 'rb')
        file_base_name = filename.split(".")[0]
        o = open(file_base_name + ".txt", "w+")
    except:
        print("I/O Error! probably")
        sys.exit()

    # Check for magic num
    magicnum = i.read(4)
    if magicnum != MAGIC_BYTEARRAY and magicnum != MAGIC_BYTEARRAY_OLD:
        print("Not a valid mtf file- check the magic number?")
        sys.exit()

    wordlist = []
    nextbyte = i.read(1)

    while nextbyte != b'':
        # First byte will be mtf symbol byte, and loop invariant should make
        # this land on such a byte in each loop


        coded_int = int.from_bytes(nextbyte, sys.byteorder)
        # print("Words: " + str(len(wordlist)))
        # print("durr " + str(coded_int))

        # Deal with newlines
        if nextbyte == b'\n':
            o.write('\n')
            nextbyte = i.read(1)

        # case 2
        elif coded_int == 249:
            # There will be two byes of encoded chars
            nextbyte = i.read(1)
            if int.from_bytes(nextbyte, sys.byteorder) + 121 > len(wordlist):
                # new word
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
                # not new word
                n = len(wordlist) - (int.from_bytes(nextbyte, sys.byteorder) + 121)
                word = wordlist[n]
                wordlist.remove(word)
                wordlist.append(word)
                o.write(word)
                nextbyte = i.read(1)
                if (nextbyte != b'') & (nextbyte != b'\n'):
                    o.write(' ') # Add a space only between words

        # Case 3
        elif coded_int == 250:
            # Three bytes of encoded chars
            # print("Case 3")

            firstbyte = int.from_bytes(i.read(1), sys.byteorder)
            secondbyte = int.from_bytes(i.read(1), sys.byteorder)
            # Get the code from bytes by doing some cheeky math
            code = (firstbyte * 256) + 376
            code += secondbyte

            
            if code <= len(wordlist): # Not a new word
                # Get the word from the list and print
                n = len(wordlist) - code
                # print("Accessing " + str(n))
                word = wordlist[n]
                o.write(word)
                # Do the MTF stuff
                wordlist.remove(word)
                wordlist.append(word)
                nextbyte = i.read(1) # advance to next code byte
                if (nextbyte != b'') & (nextbyte != b'\n'):
                    o.write(' ')

            else: # new word
                nextbyte = i.read(1) # Read first byte of word
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

        # Case 1
        else:
            # print(coded_int - 128) 
            # print(len(wordlist))

            if coded_int - 128 > len(wordlist):
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
                n = len(wordlist) - (coded_int - 128)
                # print("attempting to access wordlist index " + str(n))
                word = wordlist[n]
                wordlist.remove(word) # Do the MTF stuff
                wordlist.append(word)
                o.write(word)
                nextbyte = i.read(1) 
                if (nextbyte != b'') & (nextbyte != b'\n'):
                    o.write(' ') # Add a space only between words

        '''
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
            wordlist.append(word) '''

        '''
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
        '''
    i.close()
    o.close()
    sys.exit()