"""RugGuard AI — Token Scam & Honeypot Detector configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY", "")
POLYGONSCAN_API_KEY = os.getenv("POLYGONSCAN_API_KEY", "")
SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY", "")

GROQ_MODEL = "openai/gpt-oss-20b"

CHAINS = {
    "ethereum": {
        "chain_id": 1,
        "name": "Ethereum",
        "explorer_api": "https://api.etherscan.io/api",
        "explorer_url": "https://etherscan.io",
        "native_currency": "ETH",
        "api_key_env": "ETHERSCAN_API_KEY",
    },
    "bsc": {
        "chain_id": 56,
        "name": "BNB Smart Chain",
        "explorer_api": "https://api.bscscan.com/api",
        "explorer_url": "https://bscscan.com",
        "native_currency": "BNB",
        "api_key_env": "BSCSCAN_API_KEY",
    },
    "polygon": {
        "chain_id": 137,
        "name": "Polygon",
        "explorer_api": "https://api.polygonscan.com/api",
        "explorer_url": "https://polygonscan.com",
        "native_currency": "MATIC",
        "api_key_env": "POLYGONSCAN_API_KEY",
    },
    "solana": {
        "chain_id": 101,
        "name": "Solana",
        "explorer_api": "https://api.solscan.io",
        "explorer_url": "https://solscan.io",
        "native_currency": "SOL",
        "api_key_env": "SOLSCAN_API_KEY",
    },
}

API_TIMEOUT = 10
