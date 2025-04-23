#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
Disassembler for EVM bytecode.

This module contains the Disassembler class that is responsible for parsing
and disassembling Ethereum bytecode into human-readable assembly instructions.

Classes:
    - Disassembler: Main class for parsing and disassembling bytecode.
"""

from typing import Iterator, Generator
from zkdisasm.instruction import Instruction, InstructionFactory


class Disassembler:
    """
    Disassembles Ethereum bytecode into human-readable instructions.

    Uses the InstructionFactory to create instructions from bytecodes,
    then parses them and yields each instruction with its corresponding program counter (pc).
    """

    def __init__(self):
        self.instruction_factory = InstructionFactory()

    def parse_one(self, bytecode_iter: Iterator[int], pc: int) -> Instruction:
        """
        Parse one bytecode instruction.

        Args:
            bytecode_iter: An iterator over the bytecode to disassemble.
            pc: The program counter (position) of the current instruction in the bytecode.

        Returns:
            An Instruction object representing the disassembled instruction.
            If no more instructions are found, returns None.
        """
        try:
            opcode = next(bytecode_iter)
        except StopIteration:
            return None

        instruction = self.instruction_factory.create(opcode)
        instruction.parse(bytecode_iter)
        instruction.pc = pc
        return instruction

    def parse_all(self, bytecode_iter: Iterator[int]) -> Generator[Instruction]:
        """
        Parse all bytecode instructions and yield them one by one.

        Args:
            bytecode_iter: An iterator over the bytecode to disassemble.

        Yields:
            Instruction objects for each parsed instruction.
        """
        pc = 0
        while True:
            instruction = self.parse_one(bytecode_iter, pc)
            if not instruction:
                return
            pc += instruction.size
            yield instruction

    def disassemble(self, bytecode: str) -> list[Instruction]:
        """
        Disassemble the provided Ethereum bytecode string.

        Args:
            bytecode: A hexadecimal string representing the bytecode (with '0x' prefix).

        Returns:
            A list of Instruction objects representing the disassembled instructions.
        """
        result = []
        bytecode = iter(bytes.fromhex(bytecode[2:]))
        for instruction in self.parse_all(bytecode):
            result.append(instruction)
        return result
