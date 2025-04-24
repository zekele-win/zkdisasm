# zkDisasm

This is a simple disassembler for Ethereum Virtual Machine (EVM) bytecode, designed for educational purposes. This tool helps users understand how EVM bytecode works by disassembling it into human-readable assembly instructions.

## Usage

To run the disassembler:

```bash
python -m zkdisasm --help
```

## Test

Run tests using pytest:

```bash
pytest test
```

## Project Structure

```bash
.
├── LICENSE               # Project license file
├── pytest.ini            # Configuration file for pytest
├── README.md             # Project README file
├── requirements.txt      # Python dependencies
├── test                  # Directory containing test files
│   └── test_disassembly.py # Unit tests for disassembler functionality
└── zkdisasm              # Main package directory
    ├── __init__.py       # Initialization for the zkdisasm package
    ├── __main__.py       # Entry point for the disassembler
    ├── bytecode_loader.py # Loads and parses raw bytecode
    ├── config.py         # Configuration settings (e.g., default options)
    ├── disassembler.py   # Main logic for disassembling bytecode
    ├── instruction.py    # Defines EVM instructions and opcodes
    └── web3_provider.py  # Web3 provider to interact with Ethereum network
```

## References

- [EVM Codes](https://www.evm.codes/?fork=cancun) - Interactive Ethereum Virtual Machine Opcodes Reference
- [pyevmasm](https://github.com/crytic/pyevmasm) - Ethereum Virtual Machine (EVM) Disassembler and Assembler
