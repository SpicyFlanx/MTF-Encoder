import sys
import os
import time
import binascii

MAGIC_BYTEARRAY = bytearray([0xba,0x5e,0xba,0x11])

def write_magic_number(mtf):
    # 0xba  0x5e 0xba 0x11
    # this code basically copied from: 
    # https://github.com/gordillo99/Python-MTF-Encoder/blob/master/mtfcoding2.py
    '''
    num = bytearray()
    num.append(0xba)
    num.append(0x5e)
    num.append(0xba)
    num.append(0x11)
    mtf.write(num)
    '''
    mtf.write(MAGIC_BYTEARRAY)

def encode_main():

    # Open input file
    try:
        i = open(sys.argv[1])
        filename = sys.argv[1].split(".")[0]
        o = open(filename + ".mtf", "wb")
    except:
        print("I/O Error! probably")
        sys.exit()

    # Get output filename, create output file with .mtf

    write_magic_number(o)
    wordlist = []

    for line in i:
            splitline = line.split()
            # Tokenize the line
            for word in splitline:
                # do the stuff
                if word in wordlist:
                    # Word appears: fetch index, move to front
                    n = wordlist.index(word) + 1
                    o.write(bytes([128 + n])) # write ascii char
                    wordlist.remove(word)
                    wordlist.insert(0, word)
                else: 
                    # Word doesn't appear: add to list
                    wordlist.insert(0, word)
                    n = len(wordlist) # seems like a hack but hey, it works
                    o.write(bytes([128 + n]))
                    o.write(word.encode('ascii'))

    i.close()
    o.close()
    sys.exit()

         

def decode_main():

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

        # Check if it's a new word
        if int.from_bytes(nextbyte, sys.byteorder) - 128 > len(wordlist):
            # Yes, it is
            nextbyte = i.read(1)
            word = ''
            while (int.from_bytes(nextbyte, sys.byteorder) < 129) & (nextbyte != b''):
                word += nextbyte.decode('ascii')
                nextbyte = i.read(1)
            print(word + " " + str(len(wordlist)))
            wordlist.append(word)
        else:
            # No, it isn't
            print(int.from_bytes(nextbyte, sys.byteorder))
            nextbyte = i.read(1)
    


        '''
        if int.from_bytes(nextbyte, sys.byteorder) >= 129:
            
            nextbyte = i.read(1)
            while int.from_bytes(nextbyte, sys.byteorder) < 129:
                word += nextbyte.decode('ascii')
                nextbyte = i.read(1)
        '''

        # print(int.from_bytes(nextbyte, sys.byteorder))
        # print(nextbyte)
        # nextbyte = i.read(1)

    '''
    print(MAGIC_BYTEARRAY)
    n = i.read(4)
    print(n)
    print(MAGIC_BYTEARRAY == n)

    num = bytearray
    for i in range(4):
        num.append()
    '''
    print(wordlist)

# Open the file


# Delete this one!
'''
try:
    i = open(sys.argv[1])
except:
    print("I/O Error! probably")
    sys.exit()
'''

decode_main()

'''
command = os.path.basename(__file__)
if __name__ == "__main__" and command == "text2mtf.py":
  	encode_main()

elif __name__ == "__main__" and command == "mtf2text.py":
    decode_main()
'''

'''
elif __name__ == "__main__" and command == "ayylmao.py":
    print("ayylmao")
    encode_main()
'''



