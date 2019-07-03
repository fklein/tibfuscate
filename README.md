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

Examples
--------
Obfuscation and deobfuscation is usually handled automatically. The mode of operation is
determined by the prefix `#!`:

    $ ./tibfuscate.py MyPassword
    #!10j0I3q9WdlPSY/9+PPBvjoR3p0Nmuz9RhWhJywfL1o=
    
    $ ./tibfuscate.py '#!djaYLqbo5cXlQsP8yHh+qvh2rI6cEwfJz6CvhgGJmjcktOoJT9xBBMqJ+O+hHiTP'
    SuperSecretPassword

Otherwise forced obfuscation or deobfuscation may be required:

    $ ./tibfuscate.py --obfuscate '#!ObfuscateMe'
    #!j7yoWd6iyeC0KpKMbHnFq1/+MLSzP2h3pxOu+rT/WgSbh/2LzavMwg==
    
    $ ./tibfuscate.py --deobfuscate '10j0I3q9WdlPSY/9+PPBvjoR3p0Nmuz9RhWhJywfL1o='
    MyPassword

Reading from standard input can be achieved by either implicitly by providing no input or
explicitly by specifing `-`. Input is read line-by-line, meaning this can also be used in an
interactive fashion:

    $ ./tibfuscate.py -
    MyPassword
    #!yH/4lYxgS4vLnb/aSF4CfEBfu5KDn9iJj5Bqm3F5NdA=
    #!djaYLqbo5cXlQsP8yHh+qvh2rI6cEwfJz6CvhgGJmjcktOoJT9xBBMqJ+O+hHiTP
    SuperSecretPassword

    $ PW=secret
    $ ./tibfuscate.py <<< $PW
    #!BUx7VmItFDL6V+6xPW+IK7/6kQAcXrpY
    
    $ echo '#!BUx7VmItFDL6V+6xPW+IK7/6kQAcXrpY' | ./tibfuscate.py
    secret

    $ ./tibfuscate.py <<ENDINPUT
    > #!yH/4lYxgS4vLnb/aSF4CfEBfu5KDn9iJj5Bqm3F5NdA=
    > secret
    > ENDINPUT
    MyPassword
    #!9jLNJPQKUbjtT3aAIXJFOeqrXii26lW8

    $ cat > plain.txt
    MyPassword
    #!AnotherPassword
    secret
    $
    $ ./tibfuscate.py --obfuscate < plain.txt > obfus.txt
    $ cat obfus.txt
    #!7Vi72SGmXl/6htZ6YDemTGSGia0XbBqSu4wIocIqPUE=
    #!H6vwKzmAMMlQ7UlFTQTde+/O4TWTuWU1lP5jrnNeV5KI/LhlKEkTLkHDrHFQchB1
    #!ecVpqAKH+Ii7p/eo3r3lCUD/zkm5Tc28
    $
    $ ./tibfuscate.py < obfus.txt
    MyPassword
    #!AnotherPassword
    secret
