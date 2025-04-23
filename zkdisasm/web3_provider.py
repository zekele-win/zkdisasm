#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""
web3_provider.py

Initializes and provides a Web3 instance using an Ethereum JSON-RPC endpoint
configured via environment variable NODE_URL (loaded from a .env file).

This module allows other parts of the application to obtain a shared Web3 provider.
"""

import os
from dotenv import load_dotenv
import web3

# Load environment variables from .env file
load_dotenv()


def get() -> web3.Web3:
    """
    Create and return a Web3 instance using the NODE_URL from environment variables.

    Returns:
        web3.Web3: A Web3 instance connected to the specified Ethereum JSON-RPC endpoint.

    Raises:
        RuntimeError: If NODE_URL is not defined in the environment.
    """
    node_url = os.getenv("NODE_URL")
    if not node_url:
        raise RuntimeError("NODE_URL not defined in environment variables.")

    return web3.Web3(
        web3.Web3.HTTPProvider(node_url, cacheable_requests={"eth_chainId"})
    )
