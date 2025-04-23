#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
__main__.py

Command-line interface for zkDisasm.

Allows users to disassemble EVM bytecode from:
- Raw hex string
- Local file
- Live on-chain contract (via address)

Usage:
    python -m zkdisasm -t --text <hex_string>
    python -m zkdisasm -f --file <path_to_file>
    python -m zkdisasm -c --chain <contract_address>
"""

import argparse
from zkdisasm import bytecode_loader
from zkdisasm.disassembler import Disassembler


def parse_args() -> str:
    """
    Parse command-line arguments and return EVM bytecode hex string.

    Returns:
        str: EVM bytecode in hex format (0x-prefixed).
    """
    parser = argparse.ArgumentParser(description="EVM bytecode disassembler.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", help="Disassemble from hex-string text.")
    group.add_argument("-f", "--file", help="Disassemble from hex-string file.")
    group.add_argument("-c", "--chain", help="Disassemble from chain address.")

    args = parser.parse_args()
    if args.text:
        return args.text
    if args.file:
        return bytecode_loader.from_file(args.file)
    if args.chain:
        return bytecode_loader.from_chain(args.chain)


if __name__ == "__main__":
    bytecode = parse_args()
    for instruction in Disassembler().disassemble(bytecode):
        print(instruction)
