# 🛡️ RugGuard AI

Token Scam & Honeypot Detector — Powered by 4 AI Agents.

Paste any token contract address and get an instant risk score backed by automated security analysis and AI-generated plain-language explanations.

![Deploy](https://img.shields.io/badge/deploy-Streamlit_Cloud-FF4B4B?logo=streamlit)

## What It Does

RugGuard AI runs **4 specialized analysis agents** against a token contract and combines their findings into a **0–100 risk score**:

| Agent | What It Checks |
|---|---|
| 🔍 **Contract Auditor** | Honeypot detection, minting authority, blacklist functions, owner privileges |
| 💧 **Liquidity Agent** | LP lock status, liquidity depth, trading volume, FDV |
| 👥 **Holder Agent** | Whale concentration, deployer holdings, total holder count |
| 🌐 **Social Agent** | Website/Twitter/Telegram presence, CoinGecko listing, token age, scam patterns |

An AI model (Groq / Llama) then explains the findings in plain language.

## Supported Chains

| Chain | Explorer |
|---|---|
| Ethereum | Etherscan |
| BNB Smart Chain | BscScan |
| Polygon | PolygonScan |
| Solana | Solscan |

## How to Use

1. Open the app on [Streamlit Cloud](https://rug-guard-ai.streamlit.app/) (or run locally)
2. Select a blockchain from the dropdown
3. Paste a **token contract address** (not a wallet or profile address) — you can paste a bare address or an explorer URL:
   - `https://etherscan.io/address/0x5CF00327Edb646632BB69f1D3C38224685AEEb31`
   - `https://bscscan.com/token/0x55d398326f99059ff775485246999027b3197955`
   - `https://solscan.io/account/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
4. Click **🔍 Analyze Token**

> **Note:** Transaction hashes (`/tx/` URLs) are **not** contract addresses. The app will tell you if you pasted a tx hash and guide you to the correct contract address.

## Demo Tokons

Click the demo buttons to load well-known tokens:
- **USDT (Ethereum)** — `0xdAC17F958D2ee523a2206206994597C13D831ec7`

## Risk Score Guide

| Score | Verdict |
|---|---|
| 80–100 | 🚨 SCAM — DO NOT BUY |
| 60–79 | ⚠️ HIGH RISK |
| 40–59 | 🟡 CAUTION |
| 20–39 | 🟢 LOW RISK |
| 0–19 | ✅ LIKELY SAFE |

## Tech Stack

- **Frontend**: Streamlit
- **Data Sources**: GoPlusLabs, DexScreener, Honeypot.is, CoinGecko
- **AI**: Groq (Llama 3)
- **Deployment**: Streamlit Cloud

## Disclaimer

⚠️ RugGuard AI is for **educational and informational purposes only**. It does NOT constitute financial advice. Always do your own research (DYOR) before interacting with any token.
