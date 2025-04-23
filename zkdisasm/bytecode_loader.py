#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
bytecode_loader.py

This module provides utility functions for loading EVM bytecode either from local files
or directly from an Ethereum-compatible blockchain via Web3.

Functions:
- from_file(filepath: str) -> str:
    Loads raw bytecode from a local file.

- from_chain(address: str) -> str:
    Fetches deployed contract bytecode from the blockchain using Web3.
"""

from pathlib import Path
import web3
from zkdisasm import web3_provider


def from_file(filepath: str) -> str:
    """
    Load EVM bytecode from a local file.

    Args:
        filepath (str): Path to the file containing bytecode (in hex format, starting with "0x").

    Returns:
        str: The bytecode content as a string.

    Raises:
        FileNotFoundError: If the file path is invalid.
        UnicodeDecodeError: If the file cannot be decoded with UTF-8.
    """
    with open(Path(filepath).resolve(), encoding="utf8") as f:
        return f.read()


def from_chain(address: str) -> str:
    """
    Fetch on-chain bytecode for a given contract address using Web3.

    Args:
        address (str): The Ethereum address (can be checksummed or not).

    Returns:
        str: The bytecode string prefixed with "0x", or empty string if not found.

    Raises:
        web3.exceptions.Web3Exception: If provider is misconfigured or network errors occur.
    """
    address = web3.Web3.to_checksum_address(address)
    w3 = web3_provider.get()
    return "0x" + w3.eth.get_code(address).hex()
