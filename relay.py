#! /usr/bin/env python3
## Relays information to both `print` and logfile.

def config(filename="program.log", level="INFO"):
    return filename, level

def relay(msg):
    print(msg)
    logging.info(msg)
