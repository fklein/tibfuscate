#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is loosely based on: https://github.com/maaaaz/tibcopasswordrevealer


"""A utility for obfuscating and deobfuscating TIBCO passwords"""


import argparse
import os
import sys
import base64

from Crypto.Cipher import DES3


OBFUSCATION_PREFIX = '#!'
OBFUSCATION_KEY = bytes([
    28, 167, 155, 145, 91, 143, 26, 186, 98, 176, 233, 203,
    138, 93, 173, 239, 28, 167, 155, 145, 91, 143, 26, 186
])


def obfuscate(plaintext):
    pw = plaintext.encode('UTF-16LE')
    iv = os.urandom(8)
    cipher = DES3.new(OBFUSCATION_KEY, DES3.MODE_CBC, iv)
    pad = lambda b: b + bytes([8 - len(b) % 8] * (8 - len(b) % 8))
    data = iv + cipher.encrypt(pad(pw))
    return OBFUSCATION_PREFIX + base64.b64encode(data).decode()


def deobfuscate(obfuscated):
    if obfuscated.startswith(OBFUSCATION_PREFIX):
        data = base64.b64decode(obfuscated[len(OBFUSCATION_PREFIX):])
    else:
        data = base64.b64decode(obfuscated)
    iv = data[:8]
    pw = data[8:]
    cipher = DES3.new(OBFUSCATION_KEY, DES3.MODE_CBC, iv)
    unpad = lambda b: b[:-ord(b[-1:])]
    password = unpad(cipher.decrypt(pw))
    return password.decode('UTF-16LE')


def _normalize(str):
    return " ".join(str.split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        '-o', '--obfuscate',
        action='store_true', dest='force_obfuscate',
        help=_normalize("""Force obfuscation of input"""))
    action.add_argument(
        '-d', '--deobfuscate',
        action='store_true', dest='force_deobfuscate',
        help=_normalize("""Force deobfuscation of input"""))
    parser.add_argument(
        'input',
        nargs='?',
        action='store',
        metavar='INPUT',
        help=_normalize(
            """The input to process. If no input or "-" is specified, input is
            read line-by-line from standard input.
            By default, the mode of operation is determined by the input:
            All input prefixed with "#!" is deobfuscated. Anything else is
            obfuscated."""))
    args = parser.parse_args()

    def process(text):
        if args.force_obfuscate:
            print(obfuscate(text))
        elif args.force_deobfuscate:
            print(deobfuscate(text))
        elif text.startswith(OBFUSCATION_PREFIX):
            print(deobfuscate(text))
        else:
            print(obfuscate(text))

    if args.input is None or args.input == "-":
        for line in sys.stdin:
            process(line.rstrip('\r\n'))
    else:
        process(args.input)
            

if __name__ == "__main__":
    main()
