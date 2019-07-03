tibfuscate
==========

A utility for obfuscating and deobfuscating TIBCO passwords.

This is partially based on https://github.com/maaaaz/tibcopasswordrevealer

Usage
-----
    usage: tibfuscate.py [-h] [-o | -d] [INPUT]
    
    positional arguments:
       INPUT              The input to process. If no input or "-" is specified,
                          input is read line-by-line from standard input. By
                          default, the mode of operation is determined by the
                          input: All input prefixed with "#!" is deobfuscated.
                          Anything else is obfuscated.
    
    optional arguments: 
      -h, --help         show this help message and exit  
      -o, --obfuscate    Force obfuscation of input 
      -d, --deobfuscate  Force deobfuscation of input  
