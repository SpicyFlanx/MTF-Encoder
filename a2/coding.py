import sys
import os
import time
import binascii

def write_magic_number(mtf):
    # 0xba  0x5e 0xba 0x11
    # this code basically copied from: 
    # https://github.com/gordillo99/Python-MTF-Encoder/blob/master/mtfcoding2.py
    num = bytearray()
    num.append(0xba)
    num.append(0x5e)
    num.append(0xba)
    num.append(0x11)
    mtf.write(num)

def encode_main():

    # Get output filename, create output file with .mtf
    filename = sys.argv[1].split(".")[0]
    o = open(filename + ".mtf", "wb")
    write_magic_number(o)
    wordlist = []
    # out = b''
    # outarr = array('B')

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

         

def decode_main():

    filename = sys.argv[1].split(".")[0]
    o = open(filename + ".txt", "w+")
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



