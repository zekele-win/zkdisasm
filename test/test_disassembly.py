#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
test_disassembly.py

End-to-end test for zkDisasm.

This test loads expected disassembly results from test_data directories and compares
them against the actual output from the Disassembler class.

Each test case is stored in:
  ./test/test_data/bytecodes/<test_name>/
    - bytecode.txt : raw hex-encoded bytecode
    - asmcode.txt  : expected disassembly output
"""

import re
from pathlib import Path
from zkdisasm.disassembler import Disassembler


def data_from_file(filepath: str) -> str:
    """
    Read file content as a UTF-8 string.

    Args:
        filepath (str): Path to file.

    Returns:
        str: Contents of the file.
    """
    with open(filepath, encoding="utf8") as f:
        return f.read()


def parse_asmcode(asmcode) -> list[tuple[str, str, str | None]]:
    """
    Parse expected disassembled ASM lines into structured format.

    Args:
        asmcode (str): Expected disassembled instructions as string.

    Returns:
        list[tuple[int, str, int | None]]: Parsed [(pc, name, operand)] list.
    """
    result = []

    lines = asmcode.split("\n")
    pattern = r"^\s*(0x[0-9a-fA-F]+):\s*([a-zA-Z0-9_]+)(?:\s+(0x[0-9a-fA-F]+))?\s*$"
    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Invalid ASM line format on line {i + 1}: {line}")

        pc_hex, name, operand_hex = match.groups()
        pc = int(pc_hex, base=16)
        operand = int(operand_hex, base=16) if operand_hex else None

        result.append((pc, name, operand))

    return result


def test_should_pass_with_test_data():
    """
    Run disassembly tests on each test_data/<case>/ directory.

    Compares output of Disassembler().disassemble(bytecode) with expected ASM output.
    """
    print()
    directory = Path("./test/test_data/bytecodes")
    for subdir in [subdir for subdir in directory.iterdir() if subdir.is_dir()]:
        print(f"  - {subdir.name}")

        bytecode_filepath = subdir.resolve() / "bytecode.txt"
        asm_filepath = subdir.resolve() / "asmcode.txt"

        bytecode = data_from_file(bytecode_filepath)
        asmcode = data_from_file(asm_filepath)

        actual_result = Disassembler().disassemble(bytecode)
        expected_result = parse_asmcode(asmcode)

        assert len(actual_result) == len(expected_result)
        for i, instruction in enumerate(actual_result):
            pc, name, operand = expected_result[i]
            assert (
                instruction.pc == pc
            ), f"{subdir.name}: PC mismatch at {i}: {instruction.pc} != {pc}"
            assert (
                instruction.name == name
            ), f"{subdir.name}: name mismatch at {i}: {instruction.name} != {name}"
            assert (
                instruction.operand == operand
            ), f"{subdir.name}: operand mismatch at {i}: {instruction.operand} != {operand}"
