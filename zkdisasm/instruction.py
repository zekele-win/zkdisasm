#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
Instruction-related classes for EVM bytecode disassembly.

This module defines the Instruction class, which represents an individual EVM bytecode
instruction, as well as the MissingInstruction class for handling unknown opcodes,
and the InstructionFactory class for creating instructions based on opcodes.

Classes:
    - Instruction: Represents a single bytecode instruction.
    - MissingInstruction: Represents a missing or unknown instruction.
    - InstructionFactory: A factory class for creating instructions based on opcodes.
"""

from typing import Iterator
from zkdisasm.config import instruction_table


class Instruction:
    """
    Represents an EVM bytecode instruction.

    Attributes:
        opcode (int): The opcode value of the instruction.
        name (str): The human-readable name of the instruction.
        operands (int): Number of bytes used as operands.
        pops (int): Number of values the instruction pops from the stack.
        pushs (int): Number of values the instruction pushes onto the stack.
        gas (int): Gas cost of the instruction.
        operand (Optional[int]): Parsed operand value (if any).
        pc (Optional[int]): Program counter address in bytecode (set externally).
    """

    def __init__(
        self, opcode: int, name: str, operands: int, pops: int, pushs: int, gas: int
    ):
        """
        Initialize a new Instruction instance.

        Args:
            opcode (int): The opcode of the instruction (e.g., 0x60 for PUSH1).
            name (str): The human-readable name of the instruction (e.g., "PUSH1").
            operands (int): Number of operand bytes following the opcode.
            pops (int): Number of stack values this instruction pops.
            pushs (int): Number of stack values this instruction pushes.
            gas (int): Estimated gas cost of the instruction.
        """
        self.opcode = opcode
        self.name = name
        self.operands = operands
        self.pops = pops
        self.pushs = pushs
        self.gas = gas

        self.operand: int | None = None
        self.pc: int | None = None

    @property
    def size(self):
        """
        Returns the total size of the instruction in bytes (opcode + operands).

        Returns:
            int: Instruction size in bytes.
        """
        return 1 + self.operands

    def parse(self, bytecode_iter: Iterator[int]):
        """
        Parses the operand bytes from the bytecode iterator if required.

        Args:
            bytecode_iter (Iterator[int]): Iterator over the remaining bytecode bytes.
        """
        if self.operands:
            operand = 0
            for _ in range(self.operands):
                operand <<= 8
                operand |= next(bytecode_iter)
            self.operand = operand

    def __str__(self):
        """
        Returns a string representation of the instruction.

        Format:
            <pc>: <name padded> <operand (hex, if any)>

        Returns:
            str: A human-readable string of the instruction.
        """
        text = f"{self.pc:04x}:" if self.pc is not None else "????:"
        text += f" {(self.name + ' '*9)[:9]}"
        if self.operands:
            text += f" 0x%0{self.operands*2}x" % self.operand
        return text


class MissingInstruction(Instruction):
    """
    Represents an instruction with an unknown or undefined opcode.
    """

    def __init__(self, opcode):
        """
        Initialize a MissingInstruction for an unknown opcode.

        Args:
            opcode (int): The unknown opcode not found in the instruction table.
        """
        super().__init__(opcode, "MISSING", 0, 0, 0, 0)


class InstructionFactory:
    """
    A factory for creating Instruction objects based on EVM opcode values.

    Attributes:
        config_dict (Dict[int, Tuple]): Mapping from opcode to instruction metadata tuple.
    """

    def __init__(self):
        """
        Initialize the instruction factory.

        Builds a dictionary from the opcode to its metadata tuple, based on the
        global `instruction_table` loaded from configuration.
        """
        self.config_dict = {item[0]: item for item in instruction_table}

    def create(self, opcode: int) -> Instruction:
        """
        Creates an Instruction instance for the given opcode.

        Args:
            opcode (int): The opcode to create an instruction for.

        Returns:
            Instruction: An Instruction or MissingInstruction instance.
        """
        config = self.config_dict.get(opcode)
        return Instruction(*config) if config else MissingInstruction(opcode)
