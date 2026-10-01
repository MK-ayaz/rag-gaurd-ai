# PRD: RugGuard AI — Token Scam & Honeypot Detector

## 1. PROJECT OVERVIEW

### 1.1 What is RugGuard AI?
RugGuard AI is a multi-agent AI platform that analyzes any cryptocurrency token contract address and returns an instant "Scam Risk Score" (0-100) with detailed explanations. It protects users from honeypots, rug-pulls, and scam tokens.

### 1.2 Target Users
- Crypto beginners who want to check if a token is safe before buying
- DeFi users who want to verify new token launches
- Crypto communities who want to share scam reports

### 1.3 Core Value Proposition

"Never get rugged again. Paste a token address, get an instant safety report powered by 4 AI agents."

### 1.4 Key Principle

This project is for EDUCATION and PROTECTION only. It does NOT provide financial advice, trading signals, or investment recommendations.

---

## 2. TECH STACK (100% FREE)

### 2.1 Frontend
- **Framework:** Streamlit (Python)
- **Charts:** Plotly (free, bundled with Streamlit)
- **Icons:** streamlit-emoji (free)
- **Styling:** Custom CSS via st.markdown()

### 2.2 Backend / AI Agents
- **Language:** Python 3.11+
- **HTTP Requests:** `requests` library
- **Agent Orchestration:** Custom Python classes (NO LangChain — keep it simple and free)
- **AI Reasoning:** Groq API (free tier) using Llama 3 8B
  - API Key: Get free at https://console.groq.com
  - Model: `llama3-8b-8192`
  - Rate limit: ~14,400 requests/day on free tier

### 2.3 Data APIs (ALL FREE, NO KEY NEEDED FOR MOST)

| API | Endpoint | Key Needed? |
|-----|----------|-------------|
| GoPlusLabs | `https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={address}` | ❌ No |
| DexScreener | `https://api.dexscreener.com/latest/dex/tokens/{address}` | ❌ No |
| Honeypot.is | `https://api.honeypot.is/v2/IsHoneypot?address={address}` | ❌ No |
| Etherscan | `https://api.etherscan.io/api` | ✅ Free key |
| BscScan | `https://api.bscscan.com/api` | ✅ Free key |
| CoinGecko | `https://api.coingecko.com/api/v3` | ❌ No |

### 2.4 Deployment
- **Platform:** Streamlit Community Cloud (100% free)
- **Repo:** GitHub (public repo, free)
- **Domain:** Auto-generated `*.streamlit.app` URL

### 2.5 Project Structure

```text
ruguard-ai/
├── PRD.md
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── app.py                # Main Streamlit entry point
├── config.py             # API keys, chain configs
├── agents/
│   ├── init.py
│   ├── orchestrator.py   # Main orchestrator agent
│   ├── contract_auditor.py # Agent 1: Contract code analysis
│   ├── liquidity_agent.py # Agent 2: LP lock & liquidity
│   ├── holder_agent.py   # Agent 3: Holder distribution
│   ├── social_agent.py   # Agent 4: Social & scam reports
│   └── ai_explainer.py   # AI agent: Plain-language summary
├── services/
│   ├── init.py
│   ├── goplus_service.py    # GoPlusLabs API wrapper
│   ├── dexscreener_service.py # DexScreener API wrapper
│   ├── honeypot_service.py  # Honeypot.is API wrapper
│   ├── etherscan_service.py # Etherscan/BscScan API wrapper
│   └── groq_service.py      # Groq LLM API wrapper
├── models/
│   ├── init.py
│   └── risk_report.py       # Pydantic data models
├── ui/
│   ├── init.py
│   ├── dashboard.py         # Main dashboard layout
│   ├── risk_gauge.py        # Circular risk score gauge
│   ├── agent_cards.py       # Individual agent result cards
│   └── styles.py            # Custom CSS
└── utils/
    ├── init.py
    ├── validators.py        # Address validation
    └── formatters.py        # Number/address formatting
```

---

## 3. CHAIN CONFIGURATION

Supported chains (start with these 3 for MVP):

```python
CHAINS = {
    "ethereum": {
        "chain_id": 1,
        "name": "Ethereum",
        "explorer_api": "https://api.etherscan.io/api",
        "explorer_url": "https://etherscan.io",
        "native_currency": "ETH"
    },
    "bsc": {
        "chain_id": 56,
        "name": "BNB Smart Chain",
        "explorer_api": "https://api.bscscan.com/api",
        "explorer_url": "https://bscscan.com",
        "native_currency": "BNB"
    },
    "polygon": {
        "chain_id": 137,
        "name": "Polygon",
        "explorer_api": "https://api.polygonscan.com/api",
        "explorer_url": "https://polygonscan.com",
        "native_currency": "MATIC"
    }
}
```

---

## 4. AGENT SPECIFICATIONS

### 4.1 Agent 1: Contract Auditor Agent

**File:** `agents/contract_auditor.py`

**Purpose:** Analyze the token's smart contract code for malicious patterns.

**Data Sources:**
- GoPlusLabs API → `token_security` endpoint
- Etherscan/BscScan API → `getsourcecode` endpoint

**Checks to Perform:**

```python
contract_checks = {
    "is_honeypot": bool,          # Can users sell the token?
    "is_mintable": bool,          # Can owner mint infinite tokens?
    "can_take_back_ownership": bool,  # Can owner reclaim ownership?
    "has_owner_change_balance": bool, # Can owner change balances?
    "has_hidden_owner": bool,     # Is owner hidden/renounced?
    "is_proxy": bool,             # Is it a proxy contract?
    "has_self_destruct": bool,    # Can contract self-destruct?
    "is_open_source": bool,       # Is source code verified?
    "has_blacklist_function": bool, # Can owner blacklist users?
    "has_trading_cooldown": bool, # Is there a sell cooldown?
    "sell_tax": float,            # Sell tax percentage
    "buy_tax": float,             # Buy tax percentage
}
```

**Risk Scoring:**

```python
def calculate_contract_risk(checks) -> int:  # Returns 0-100
    risk = 0
    if checks["is_honeypot"]: risk += 40
    if checks["is_mintable"]: risk += 15
    if checks["can_take_back_ownership"]: risk += 15
    if checks["has_owner_change_balance"]: risk += 10
    if checks["has_hidden_owner"]: risk += 5
    if checks["has_blacklist_function"]: risk += 5
    if checks["sell_tax"] > 10: risk += 5
    if checks["buy_tax"] > 10: risk += 5
    if not checks["is_open_source"]: risk += 10
    return min(risk, 100)
```

**API Call Example (GoPlusLabs):**

```http
GET https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=0x...
```

**Response fields to extract:**

```json
{
  "result": {
    "0x...": {
      "is_honeypot": "0",
      "is_mintable": "0",
      "owner_address": "0x...",
      "can_take_back_ownership": "0",
      "owner_change_balance": "0",
      "hidden_owner": "0",
      "selfdestruct": "0",
      "is_open_source": "1",
      "is_blacklisted": "0",
      "slippage_modifiable": "0",
      "sell_tax": "0.00",
      "buy_tax": "0.00",
      "holder_count": "1234",
      "total_supply": "1000000000",
      "holders": [...],
      "lp_holders": [...]
    }
  }
}
```

---

### 4.2 Agent 2: Liquidity Agent

**File:** `agents/liquidity_agent.py`

**Purpose:** Check if liquidity is locked, for how long, and if it's sufficient.

**Data Sources:**
- GoPlusLabs API → `lp_holders` field from `token_security`
- DexScreener API → liquidity and volume data

**Checks to Perform:**

```python
liquidity_checks = {
    "lp_locked": bool,            # Is LP locked?
    "lp_lock_percentage": float,  # What % is locked?
    "lp_lock_duration_days": int, # How long is it locked?
    "lp_lock_provider": str,      # Which lock service? (Unicrypt, Team.Finance, etc.)
    "total_liquidity_usd": float, # Total liquidity in USD
    "volume_24h_usd": float,      # 24h trading volume
    "liquidity_to_mcap_ratio": float, # Healthy ratio > 0.05
}
```

**Risk Scoring:**

```python
def calculate_liquidity_risk(checks) -> int:
    risk = 0
    if not checks["lp_locked"]: risk += 40
    if checks["lp_lock_percentage"] < 50: risk += 20
    if checks["lp_lock_duration_days"] < 30: risk += 15
    if checks["total_liquidity_usd"] < 10000: risk += 15
    if checks["liquidity_to_mcap_ratio"] < 0.01: risk += 10
    return min(risk, 100)
```

**API Call Example (DexScreener):**

```http
GET https://api.dexscreener.com/latest/dex/tokens/0x...
```

**Response fields to extract:**

```json
{
  "pairs": [{
    "liquidity": { "usd": 50000 },
    "volume": { "h24": 120000 },
    "priceUsd": "0.001",
    "fdv": 1000000
  }]
}
```

---

### 4.3 Agent 3: Holder Agent

**File:** `agents/holder_agent.py`

**Purpose:** Analyze token holder distribution for concentration risk.

**Data Sources:**
- GoPlusLabs API → `holders` field from `token_security`

**Checks to Perform:**

```python
holder_checks = {
    "total_holders": int,
    "top_holder_percentage": float,   # % held by #1 wallet
    "top_10_percentage": float,       # % held by top 10 wallets
    "is_deployer_holding": bool,      # Does deployer still hold?
    "deployer_percentage": float,     # How much does deployer hold?
    "are_top_holders_contracts": bool, # Are top holders contracts?
    "whale_concentration": float,     # Herfindahl index
}
```

**Risk Scoring:**

```python
def calculate_holder_risk(checks) -> int:
    risk = 0
    if checks["top_holder_percentage"] > 40: risk += 35
    elif checks["top_holder_percentage"] > 20: risk += 20
    if checks["top_10_percentage"] > 80: risk += 25
    elif checks["top_10_percentage"] > 60: risk += 15
    if checks["is_deployer_holding"] and checks["deployer_percentage"] > 10:
        risk += 20
    if checks["total_holders"] < 100: risk += 15
    return min(risk, 100)
```

---

### 4.4 Agent 4: Social Agent

**File:** `agents/social_agent.py`

**Purpose:** Check for known scam patterns and social presence.

**Data Sources:**
- GoPlusLabs API → social fields
- CoinGecko API → check if token is listed (legitimacy signal)

**Checks to Perform:**

```python
social_checks = {
    "has_website": bool,
    "has_twitter": bool,
    "has_telegram": bool,
    "is_on_coingecko": bool,      # Listed on CoinGecko = more legit
    "token_age_days": int,         # Very new tokens = higher risk
    "is_fake_token": bool,         # GoPlusLabs fake token detection
    "is_airdrop_scam": bool,       # Known airdrop scam pattern
}
```

**Risk Scoring:**

```python
def calculate_social_risk(checks) -> int:
    risk = 0
    if not checks["has_website"]: risk += 15
    if not checks["has_twitter"]: risk += 10
    if not checks["has_telegram"]: risk += 10
    if not checks["is_on_coingecko"]: risk += 15
    if checks["token_age_days"] < 1: risk += 25
    elif checks["token_age_days"] < 7: risk += 15
    elif checks["token_age_days"] < 30: risk += 5
    if checks["is_fake_token"]: risk += 30
    return min(risk, 100)
```

---

### 4.5 Orchestrator Agent

**File:** `agents/orchestrator.py`

**Purpose:** Run all 4 agents, collect results, calculate final score.

```python
class RugGuardOrchestrator:
    def __init__(self, contract_address: str, chain: str):
        self.address = contract_address
        self.chain = chain
        self.agents = [
            ContractAuditorAgent(),
            LiquidityAgent(),
            HolderAgent(),
            SocialAgent()
        ]
    
    def run_analysis(self) -> RiskReport:
        results = {}
        for agent in self.agents:
            try:
                results[agent.name] = agent.analyze(self.address, self.chain)
            except Exception as e:
                results[agent.name] = AgentResult(error=str(e))
        
        # Weighted final score
        final_score = (
            results["contract"].risk_score * 0.35 +
            results["liquidity"].risk_score * 0.25 +
            results["holder"].risk_score * 0.25 +
            results["social"].risk_score * 0.15
        )
        
        # Determine verdict
        if final_score >= 80: verdict = "🚨 SCAM - DO NOT BUY"
        elif final_score >= 60: verdict = "⚠️ HIGH RISK"
        elif final_score >= 40: verdict = "🟡 CAUTION"
        elif final_score >= 20: verdict = "🟢 LOW RISK"
        else: verdict = "✅ LIKELY SAFE"
        
        return RiskReport(
            final_score=round(final_score),
            verdict=verdict,
            agent_results=results
        )
```

---

### 4.6 AI Explainer Agent

**File:** `agents/ai_explainer.py`

**Purpose:** Use Groq (Llama 3) to generate a plain-language summary.

```python
def generate_explanation(risk_report: RiskReport) -> str:
    prompt = f"""
    You are a crypto security analyst. Explain this token analysis 
    in simple language for a beginner. Be direct and clear.
    
    Token: {risk_report.token_name} ({risk_report.token_symbol})
    Final Risk Score: {risk_report.final_score}/100
    Verdict: {risk_report.verdict}
    
    Contract Risk: {risk_report.agent_results['contract'].risk_score}/100
    Liquidity Risk: {risk_report.agent_results['liquidity'].risk_score}/100
    Holder Risk: {risk_report.agent_results['holder'].risk_score}/100
    Social Risk: {risk_report.agent_results['social'].risk_score}/100
    
    Key findings:
    {risk_report.get_key_findings_text()}
    
    Write a 3-4 sentence explanation in simple English. 
    Do NOT give financial advice. Only explain the risk factors found.
    """
    
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content
```

---

## 5. DATA MODELS

**File:** `models/risk_report.py`

```python
from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class AgentResult:
    agent_name: str
    risk_score: int  # 0-100
    checks: Dict[str, any]
    red_flags: list  # List of string warnings
    error: Optional[str] = None

@dataclass
class RiskReport:
    contract_address: str
    chain: str
    token_name: str
    token_symbol: str
    final_score: int  # 0-100
    verdict: str
    agent_results: Dict[str, AgentResult]
    ai_explanation: str = ""
    timestamp: str = ""
```

---

## 6. UI SPECIFICATION

### 6.1 Main Page Layout (`app.py`)

```text
┌─────────────────────────────────────────────────┐
│  🛡️ RugGuard AI                                │
│  Token Scam & Honeypot Detector                │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ Chain: [Ethereum ▼]                       │ │
│  │ Token Address: [0x________________]  🔍   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │         RISK SCORE: 78/100                 │ │
│  │         🚨 SCAM - DO NOT BUY              │ │
│  │         [Circular Gauge Chart]             │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────┐│
│  │Contract  │ │Liquidity │ │Holders   │ │Soc ││
│  │Auditor   │ │Agent     │ │Agent     │ │Agen││
│  │Score: 85 │ │Score: 70 │ │Score: 90 │ │75  ││
│  │🔴🔴🔴   │ │🔴🔴🟡   │ │🔴🔴🔴   │ │🔴🔴││
│  └──────────┘ └──────────┘ └──────────┘ └────┘│
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ 🤖 AI Analysis:                            │ │
│  │ "This token shows multiple red flags..."   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ 📋 Detailed Findings (Expandable)          │ │
│  │ ✅/❌ Is Honeypot: Yes                    │ │
│  │ ✅/❌ LP Locked: No                        │ │
│  │ ✅/❌ Top Holder > 40%: Yes                │ │
│  │ ...                                        │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ⚠️ Disclaimer: For education only. Not         │
│  financial advice. DYOR.                        │
└─────────────────────────────────────────────────┘
```

### 6.2 UI Components

**Risk Gauge (`risk_gauge.py`):**
- Use Plotly `go.Indicator` with gauge mode
- Color zones: Green (0-30), Yellow (30-50), Orange (50-70), Red (70-100)

**Agent Cards (`agent_cards.py`):**
- Use `st.columns(4)` for 4 agent cards
- Each card shows: Agent name, risk score, top 3 red flags
- Use `st.expander()` for detailed check results

**Loading State:**
- Use `st.spinner("🔍 Analyzing token...")` during API calls
- Show progress: `"Running Contract Auditor... ✅"` etc.

### 6.3 Styling (`styles.py`)

```css
/* Custom CSS for dark theme */
.stApp { background-color: #0e1117; }
.risk-critical { color: #ff4b4b; font-size: 2rem; font-weight: bold; }
.risk-high { color: #ffa500; font-size: 2rem; font-weight: bold; }
.risk-medium { color: #ffff00; font-size: 2rem; font-weight: bold; }
.risk-low { color: #00ff00; font-size: 2rem; font-weight: bold; }
.agent-card {
    background: #1e1e2e;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #333;
}
```

---

## 7. API SERVICE IMPLEMENTATIONS

### 7.1 GoPlusLabs Service (`services/goplus_service.py`)

```python
import requests

def get_token_security(chain_id: int, address: str) -> dict:
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
    params = {"contract_addresses": address}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", {}).get(address.lower(), {})
    except Exception as e:
        return {"error": str(e)}
```

### 7.2 DexScreener Service (`services/dexscreener_service.py`)

```python
def get_token_pairs(address: str) -> dict:
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("pairs", [])
    except Exception as e:
        return []
```

### 7.3 Honeypot.is Service (`services/honeypot_service.py`)

```python
def check_honeypot(address: str, chain: str = "ethereum") -> dict:
    url = "https://api.honeypot.is/v2/IsHoneypot"
    params = {"address": address}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
```

### 7.4 Groq Service (`services/groq_service.py`)

```python
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_summary(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"
```

---

## 8. REQUIREMENTS.TXT

```txt
streamlit==1.38.0
requests==2.32.0
plotly==5.24.0
groq==0.11.0
pydantic==2.9.0
python-dotenv==1.0.1
```

---

## 9. ENVIRONMENT VARIABLES (`.env`)

```bash
GROQ_API_KEY=gsk_your_free_key_here
ETHERSCAN_API_KEY=your_free_etherscan_key
BSCSCAN_API_KEY=your_free_bscscan_key
```

**Get free keys:**
- Groq: https://console.groq.com (free, instant)
- Etherscan: https://etherscan.io/apis (free, 5 calls/sec)
- BscScan: https://bscscan.com/apis (free, 5 calls/sec)

---

## 10. DEPLOYMENT INSTRUCTIONS

### 10.1 Streamlit Cloud (FREE)

1. Push code to GitHub public repo
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New App"
5. Select repo: `ruguard-ai`
6. Select file: `app.py`
7. Add secrets (Environment Variables):

   ```bash
   GROQ_API_KEY="gsk_..."
   ETHERSCAN_API_KEY="..."
   BSCSCAN_API_KEY="..."
   ```

8. Click "Deploy"
9. Your app will be live at: https://ruguard-ai.streamlit.app

### 10.2 `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#ff4b4b"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1e1e2e"
textColor = "#ffffff"

[server]
maxUploadSize = 10
```

---

## 11. TEST TOKENS FOR DEMO

**Safe Tokens (for testing "safe" results):**
- Ethereum USDT: `0xdAC17F958D2ee523a2206206994597C13D831ec7`
- Ethereum USDC: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`

**Known Scam/Honeypot Tokens (for testing "scam" results):**
- Search on https://honeypot.is for recent honeypots
- Check https://tokensniffer.com for flagged tokens
- Use any token from GoPlusLabs scam list

**Demo Script:**
1. First scan USDT → Show "✅ LIKELY SAFE" with low score
2. Then scan a known scam token → Show "🚨 SCAM" with high score
3. Explain the red flags found by each agent
4. Show the AI-generated explanation

---

## 12. ERROR HANDLING

- If GoPlusLabs API fails → Fall back to Honeypot.is + DexScreener
- If DexScreener returns no pairs → Show "No liquidity found" warning
- If Groq API rate limited → Show cached/static explanation
- If address is invalid → Show validation error before API calls
- If chain not supported → Show supported chains list
- All API calls must have 10-second timeout
- Use `try/except` for every external API call

---

## 13. ADDRESS VALIDATION

```python
import re

def validate_address(address: str, chain: str) -> bool:
    # Ethereum-style: 0x followed by 40 hex chars
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))
```

---

## 14. BUILD ORDER (For AI Agent)

Build the project in this exact order:

1. ✅ Create project structure (all folders and `init.py` files)
2. ✅ Create `config.py` with chain configurations
3. ✅ Create `models/risk_report.py` with dataclasses
4. ✅ Create `services/goplus_service.py` (most important API)
5. ✅ Create `services/dexscreener_service.py`
6. ✅ Create `services/honeypot_service.py`
7. ✅ Create `services/groq_service.py`
8. ✅ Create `agents/contract_auditor.py`
9. ✅ Create `agents/liquidity_agent.py`
10. ✅ Create `agents/holder_agent.py`
11. ✅ Create `agents/social_agent.py`
12. ✅ Create `agents/ai_explainer.py`
13. ✅ Create `agents/orchestrator.py`
14. ✅ Create `ui/styles.py`
15. ✅ Create `ui/risk_gauge.py`
16. ✅ Create `ui/agent_cards.py`
17. ✅ Create `ui/dashboard.py`
18. ✅ Create `app.py` (main entry point)
19. ✅ Create `requirements.txt`
20. ✅ Create `.streamlit/config.toml`
21. ✅ Test with USDT address (should show SAFE)
22. ✅ Test with a known scam token (should show SCAM)

---

## 15. DISCLAIMER (Must be in UI)

> ⚠️ RugGuard AI is for educational and informational purposes only. It does NOT constitute financial advice. Always do your own research (DYOR) before interacting with any token. The creators are not responsible for any financial losses.

---

## 🚀 Part 3: Exact Steps to Build in One Shot

### Option A: Using Cursor (Best Control)

