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
- **AI Reasoning:** Groq API (free tier)
  - API Key: Get free at https://console.groq.com
  - Model: `openai/gpt-oss-20b`
  - Rate limit: ~14,400 requests/day on free tier

### 2.3 Data APIs (ALL FREE, NO KEY NEEDED FOR MOST)

| API | Endpoint | Key Needed? |
|-----|----------|-------------|
| GoPlusLabs | `https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={address}` | ❌ No |
| DexScreener | `https://api.dexscreener.com/latest/dex/tokens/{address}` | ❌ No |
| Honeypot.is | `https://api.honeypot.is/v2/IsHoneypot?address={address}&chainID={chain_id}` | ❌ No |
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
│   ├── __init__.py
│   ├── orchestrator.py   # Main orchestrator agent
│   ├── contract_auditor.py # Agent 1: Contract code analysis
│   ├── liquidity_agent.py # Agent 2: LP lock & liquidity
│   ├── holder_agent.py   # Agent 3: Holder distribution
│   ├── social_agent.py   # Agent 4: Social & scam reports
│   └── ai_explainer.py   # AI agent: Plain-language summary
├── services/
│   ├── __init__.py
│   ├── goplus_service.py    # GoPlusLabs API wrapper
│   ├── dexscreener_service.py # DexScreener API wrapper
│   ├── honeypot_service.py  # Honeypot.is API wrapper
│   ├── etherscan_service.py # Etherscan/BscScan/PolygonScan API wrapper
│   └── groq_service.py      # Groq LLM API wrapper
├── models/
│   ├── __init__.py
│   └── risk_report.py       # Pydantic data models
├── ui/
│   ├── __init__.py
│   ├── dashboard.py         # Main dashboard layout
│   ├── risk_gauge.py        # Circular risk score gauge
│   ├── agent_cards.py       # Individual agent result cards
│   └── styles.py            # Custom CSS
└── utils/
    ├── __init__.py
    ├── validators.py        # Address/URL validation & normalization
    └── formatters.py        # Number/address formatting
```

---

## 3. CHAIN CONFIGURATION

Supported chains (4 chains in production):

```python
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
        "explorer_api": "https://public-api.solscan.io",
        "explorer_url": "https://solscan.io",
        "native_currency": "SOL",
        "api_key_env": "SOLSCAN_API_KEY",
    },
}
```

**Notes:**
- `api_key_env` is the environment variable name for the chain's free explorer API key.
- Solana uses `public-api.solscan.io` (NOT `api.solscan.io`, which is the web UI).
- CoinGecko contract lookup supports Ethereum, BSC, and Polygon only (Solana excluded).

### Solana-specific behavior

- GoPlusLabs does not support Solana. The Contract Auditor returns `risk_score=50` with an error for Solana addresses.
- The Holder Agent also does not support Solana (GoPlusLabs holder data is EVM-only).
- The Liquidity Agent uses DexScreener (chain-agnostic) and works for Solana.
- The Social Agent works for Solana except CoinGecko (returns False).
- Solana explorer URLs are handled by `normalize_address()` via Solscan `/account/` paths.
- Solana transaction signatures (87-88 Base58 chars) are rejected with a specific error message.

## 4. AGENT SPECIFICATIONS

### 4.1 Agent 1: Contract Auditor Agent

**File:** `agents/contract_auditor.py`

**Purpose:** Analyze the token's smart contract code for malicious patterns.

**Data Sources:**
- GoPlusLabs API → `token_security` endpoint (primary)
- Honeypot.is API → fallback when GoPlusLabs fails
- DexScreener API → liquidity and volume data

**Behavior on failure:** If GoPlusLabs and honeypot.is both fail, the agent returns `risk_score=50` with the error stored in `AgentResult.error` and added to `red_flags`. The orchestrator then renormalizes weights across successful agents only.

```python
class ContractAuditorAgent:
    def analyze(self, address: str, chain: str) -> AgentResult:
        try:
            data = goplus_service.get_token_security(chain_id, address)
            if not data:
                data = honeypot_service.check_honeypot(address, chain_id)
            checks = self._map_goplus_fields(data)
            score = self._calculate_risk(checks)
            return AgentResult(risk_score=score, checks=checks, red_flags=...)
        except Exception as e:
            return AgentResult(
                risk_score=50,
                checks={},
                red_flags=[f"Analysis failed: {e}"],
                error=str(e),
            )
```

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
GET https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses={address}
```

**Fallback chain:**
1. GoPlusLabs primary. If it fails or returns no data → fall back to honeypot.is.
2. If both fail → return `risk_score=50` (neutral midpoint) with error flagged in `red_flags`.

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

**Best pair selection:** When DexScreener returns multiple pairs, `get_best_pair()` selects the pair with the highest liquidity USD value.

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

**CoinGecko platform mapping:**
- Ethereum → `ethereum`
- BSC → `binance-smart-chain`
- Polygon → `polygon-pos`
- Solana → not supported (returns False)

**Behavior on failure:** If all data sources fail, returns `risk_score=50` with error in `red_flags`.

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

    def run_analysis(self, use_ai: bool = True) -> RiskReport:
        results = {}
        for agent in self.agents:
            try:
                results[agent.name] = agent.analyze(self.address, self.chain)
            except Exception as e:
                results[agent.name] = AgentResult(
                    risk_score=50,
                    error=str(e),
                    red_flags=[f"Agent error: {e}"],
                )

        # Renormalize weights across successful agents only
        successful = {k: v for k, v in results.items() if not v.has_error()}
        if not successful:
            final_score = 50
        else:
            weights = {"contract": 0.35, "liquidity": 0.25, "holder": 0.25, "social": 0.15}
            total_weight = sum(weights[k] for k in successful)
            final_score = sum(results[k].risk_score * weights[k] for k in successful) / total_weight

        # Determine verdict
        if final_score >= 80: verdict = "🚨 HIGH RISK — Likely Scam"
        elif final_score >= 60: verdict = "⚠️ MEDIUM RISK — Exercise Caution"
        elif final_score >= 40: verdict = "🟡 CAUTION — Some Red Flags"
        elif final_score >= 20: verdict = "🟢 LOW RISK — Looks Safe"
        else: verdict = "✅ VERY LOW RISK — Likely Safe"

        return RiskReport(
            contract_address=self.address,
            chain=self.chain,
            final_score=round(final_score),
            verdict=verdict,
            agent_results=results,
            ai_explanation=self._generate_explanation(results) if use_ai else "",
        )
```

---

### 4.6 AI Explainer Agent

**File:** `agents/ai_explainer.py`

**Purpose:** Use Groq to generate a plain-language summary. Falls back to a static rule-based explanation if Groq is unavailable.

```python
def generate_explanation(risk_report: RiskReport) -> str:
    try:
        return _call_groq(risk_report)
    except Exception:
        return generate_static_explanation(risk_report)

def generate_static_explanation(risk_report: RiskReport) -> str:
    """Rule-based fallback when Groq is unavailable."""
    tier = "low risk"
    if risk_report.final_score >= 80: tier = "high risk / likely scam"
    elif risk_report.final_score >= 60: tier = "medium risk"
    elif risk_report.final_score >= 40: tier = "caution — some red flags"

    findings = risk_report.get_key_findings_text()
    return (
        f"This token shows {tier} (score: {risk_report.final_score}/100). "
        f"{findings} "
        "This is an automated analysis — always do your own research."
    )
```

**Groq call:**

```python
def _call_groq(risk_report: RiskReport) -> str:
    prompt = f"""
    You are a crypto security analyst. Explain this token analysis
    in simple language for a beginner. Be direct and clear.

    Token: {risk_report.token_name} ({risk_report.token_symbol})
    Final Risk Score: {risk_report.final_score}/100
    Verdict: {risk_report.verdict}

    Agent Scores: {report.get_agent_scores_text()}
    Key findings: {report.get_key_findings_text()}

    Write a 3-4 sentence explanation. Do NOT give financial advice.
    """

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )
    return response.choices[0].message.content
```

---

## 5. DATA MODELS

**File:** `models/risk_report.py`

Uses **Pydantic** (not dataclasses) for validation and serialization.

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class AgentResult(BaseModel):
    agent_name: str
    risk_score: int = Field(ge=0, le=100)
    checks: Dict[str, any] = {}
    red_flags: List[str] = []
    error: Optional[str] = None

    def has_error(self) -> bool:
        return self.error is not None

class RiskReport(BaseModel):
    contract_address: str
    chain: str
    token_name: str = "Unknown"
    token_symbol: str = "UNKNOWN"
    final_score: int = Field(ge=0, le=100)
    verdict: str
    agent_results: Dict[str, AgentResult]
    ai_explanation: str = ""
    timestamp: str = ""

    def get_key_findings_text(self) -> str:
        """Summarize the most critical findings across all agents."""
        ...

    def get_agent_scores_text(self) -> str:
        """Return a formatted string of all agent scores."""
        ...
```

---

## 6. UI SPECIFICATION

### 6.1 Component Architecture (`ui/dashboard.py`)

The dashboard is composed of these functions, called from `app.py`:

| Function | Purpose |
|----------|---------|
| `render_header()` | Branded hero: logo, gradient title, tagline, accent divider |
| `render_input_section(chain_options, default_chain)` | Search card with 3-column layout: chain select, address input, analyze button |
| `render_risk_score(report)` | Plotly gauge chart + verdict + token meta (name, chain, address) |
| `render_agent_cards_section(report)` | 4-column agent card grid (contract, liquidity, holder, social) |
| `_render_score_card(title, subtitle, result, color, icon)` | Individual agent card with score, progress bar, red flags, expandable details |
| `_render_error_card(title, subtitle, error, color)` | Agent card for failed analysis (N/A score, error message) |
| `_render_empty_card(title)` | Placeholder card when agent data is unavailable |
| `_render_agent_details(checks)` | Check-row layout inside expander: icon, label, color-coded value |
| `render_ai_explanation(report)` | AI analysis box with indigo gradient background |
| `render_detailed_findings(report)` | Expandable per-agent findings with red flags and all checks |
| `render_disclaimer()` | Educational disclaimer (rendered in sidebar AND at bottom of report) |
| `render_full_report(report)` | Orchestrates: risk score → agent cards → AI explanation → detailed findings → disclaimer |

**Agent card colors:**
- Contract Auditor: `#6366f1` (indigo)
- Liquidity Agent: `#06b6d4` (cyan)
- Holder Agent: `#10b981` (emerald)
- Social Agent: `#f59e0b` (amber)

### 6.2 Risk Gauge (`risk_gauge.py`)

- Plotly `go.Indicator` with `mode="gauge+number"`
- Number font: 60pt, bold, colored by score tier
- Gauge bar thickness: 0.22, no border
- Threshold line at the current score value
- Color zones: Red (≥80), Orange (≥60), Yellow (≥40), Green (<40)

### 6.3 Styling (`styles.py`)

Full branded design system:

- **Background:** Deep navy `#06080d`
- **Brand gradient:** Indigo `#6366f1` → Violet `#8b5cf6`
- **Typography:** Inter font family (Google Fonts)
- **Cards:** Glass-morphism with `backdrop-filter: blur(24px)`, rgba backgrounds, subtle white borders
- **Hero:** Brand logo (gradient square), gradient title text, tagline, shimmer accent divider
- **Search card:** 3-column layout (chain | address | button), labeled fields, gradient analyze button
- **Agent grid:** CSS Grid, 4 columns default, 2 columns at `max-width: 900px` (responsive)
- **Agent cards:** Colored top border (`::before` pseudo-element, 3px), icon badge, score with progress bar, hover lift effect
- **AI box:** Indigo gradient background with left accent border
- **Section dividers:** Gradient fade lines
- **Streamlit overrides:** Custom button, input, selectbox, expander, spinner styles
- **Hidden elements:** Footer, MainMenu
- **Custom scrollbar:** 6px width, dark track, slate thumb

---

## 7. API SERVICE IMPLEMENTATIONS

### 7.1 GoPlusLabs Service (`services/goplus_service.py`)

```python
import requests
from config import API_TIMEOUT

def get_token_security(chain_id: int, address: str) -> dict:
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
    params = {"contract_addresses": address}
    try:
        resp = requests.get(url, params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data.get("result", {}).get(address.lower(), {})
    except Exception as e:
        return {"error": str(e)}
```

### 7.2 DexScreener Service (`services/dexscreener_service.py`)

```python
from config import API_TIMEOUT

def get_token_pairs(address: str) -> list:
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    try:
        resp = requests.get(url, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data.get("pairs", [])
    except Exception as e:
        return []

def get_best_pair(pairs: list) -> dict:
    """Select the pair with the highest liquidity USD value."""
    if not pairs:
        return {}
    return max(pairs, key=lambda p: p.get("liquidity", {}).get("usd", 0))
```

### 7.3 Honeypot.is Service (`services/honeypot_service.py`)

```python
from config import API_TIMEOUT

def check_honeypot(address: str, chain_id: int = 1) -> dict:
    url = "https://api.honeypot.is/v2/IsHoneypot"
    params = {"address": address, "chainID": chain_id}
    try:
        resp = requests.get(url, params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
```

### 7.4 Etherscan Service (`services/etherscan_service.py`)

Unified wrapper for Etherscan, BscScan, and PolygonScan APIs.

```python
from config import CHAINS, API_TIMEOUT

def get_source_code(address: str, chain: str) -> dict:
    """Fetch contract source code from the chain's explorer API."""
    cfg = CHAINS[chain]
    api_key = os.getenv(cfg["api_key_env"], "")
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key,
    }
    try:
        resp = requests.get(cfg["explorer_api"], params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
```

### 7.5 Groq Service (`services/groq_service.py`)

```python
from groq import Groq
from config import API_TIMEOUT

_client: Groq | None = None

def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))
    return _client

def generate_summary(prompt: str) -> str:
    try:
        response = _get_client().chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"
```

---

## 8. REQUIREMENTS.TXT

```txt
streamlit
requests>=2.32.3
plotly==5.24.0
groq>=1.2.0
pydantic>=2.11.0
python-dotenv==1.0.1
```

**Notes:**
- `streamlit` is unpinned to allow Streamlit Cloud to resolve the latest compatible version.
- `requests>=2.32.3` is required because 2.32.0 was yanked due to CVE-2024-35195.
- `pydantic>=2.11.0` is required because PyO3 0.22.x in earlier pydantic builds does not support Python 3.14.

---

## 9. ENVIRONMENT VARIABLES (`.env`)

```bash
GROQ_API_KEY=gsk_your_free_key_here
ETHERSCAN_API_KEY=your_free_etherscan_key
BSCSCAN_API_KEY=your_free_bscscan_key
POLYGONSCAN_API_KEY=your_free_polygonscan_key
SOLSCAN_API_KEY=your_free_solscan_key
```

**Get free keys:**
- Groq: https://console.groq.com (free, instant)
- Etherscan: https://etherscan.io/apis (free, 5 calls/sec)
- BscScan: https://bscscan.com/apis (free, 5 calls/sec)
- PolygonScan: https://polygonscan.com/apis (free, 5 calls/sec)
- Solscan: https://solscan.io/ (free tier available)

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
   POLYGONSCAN_API_KEY="..."
   SOLSCAN_API_KEY="..."
   ```

8. Click "Deploy"
9. Your app will be live at a deployment-specific `*.streamlit.app` URL

### 10.2 `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#06080d"
secondaryBackgroundColor = "#0f172a"
textColor = "#f1f5f9"
font = "Inter, sans-serif"

[server]
maxUploadSize = 10
```

---

## 11. TEST TOKENS FOR DEMO

**Safe Tokens (for testing "safe" results):**
- Ethereum USDT: `0xdAC17F958D2ee523a2206206994597C13D831ec7`
- Ethereum USDC: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- BSC USDT: `0x55d398326f99059ff775485246999027b3197955`

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

### Address normalization (`utils/validators.py`)

`normalize_address(raw)` extracts a bare contract address from:
- EVM explorer URLs: `/address/` and `/token/` paths (Etherscan, BscScan, PolygonScan)
- Solana explorer URLs: `/account/` paths (Solscan)
- Transaction URLs: `/tx/` paths (EVM and Solana — rejected before analysis)
- Markdown-wrapped input (e.g., `[text](0x...)` pasted from a link)
- Plain addresses (bare strings)

### Validation error messages

The app in `app.py` shows specific errors based on the input type:
- **Invalid format:** "That does not look like a token contract address."
- **Transaction hash (EVM):** "That looks like a transaction hash, not a token contract address. Transaction hashes are 64 characters; contract addresses are 40."
- **Solana transaction signature:** "That looks like a Solana transaction signature, not a token contract address. Transaction signatures are 87-88 characters; contract addresses are 43-44."
- **Unsupported chain:** "Unsupported chain. Supported chains: ethereum, bsc, polygon, solana"

### GoPlusLabs fallback chain

1. GoPlusLabs primary.
2. If GoPlusLabs fails or returns empty → honeypot.is fallback.
3. If both fail → `risk_score=50` with error flagged.

### AI explanation fallback

1. Groq is attempted first.
2. If Groq fails (no key, rate limit, network error) → `generate_static_explanation()` produces a rule-based summary from the score tier and key findings.

### Agent failure behavior

The orchestrator catches individual agent exceptions and assigns `risk_score=50` with the error stored in `AgentResult.error` and added to `red_flags`. Weights are renormalized across successful agents only. If all agents fail, the final score defaults to 50.

### Timeouts

All external API calls use `API_TIMEOUT` (defined in config, default 15s).

---

## 13. ADDRESS VALIDATION AND NORMALIZATION

**File:** `utils/validators.py`

### Validation patterns

| Pattern | Regex | Description |
|---------|-------|-------------|
| EVM address | `^0x[a-fA-F0-9]{40}$` | 0x prefix + exactly 40 hex chars |
| EVM tx hash | `^0x[a-fA-F0-9]{64}$` | 0x prefix + exactly 64 hex chars |
| Solana address | `^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{43,44}$` | Base58, 43-44 chars |
| Solana tx signature | `^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{87,88}$` | Base58, 87-88 chars |

### Normalization pipeline (`normalize_address`)

1. Strip whitespace and markdown links from raw input.
2. If input matches an explorer URL, extract the address from `/address/`, `/token/`, `/account/`, or `/tx/` path segments.
3. If the extracted value is a tx hash (EVM 64-char or Solana 87-88-char), return it as-is (it will be rejected downstream).
4. If the input is a bare address, validate it against EVM and Solana patterns.

### Downstream guards in `app.py`

After normalization, the app runs these checks before analysis:
1. `is_tx_hash(normalized)` → Show "transaction hash" error.
2. `is_solana_tx(normalized)` → Show "Solana transaction signature" error.
3. `validate_address(normalized)` → Show "invalid format" error.
4. `validate_chain(chain_key)` → Show "unsupported chain" error.

---

## 14. BUILD ORDER (Reference)

Build the project in this order:

1. Create project structure (all folders and `__init__.py` files)
2. Create `config.py` with chain configurations
3. Create `models/risk_report.py` with Pydantic models
4. Create `utils/validators.py` and `utils/formatters.py`
5. Create `services/goplus_service.py` (most important API)
6. Create `services/dexscreener_service.py`
7. Create `services/honeypot_service.py`
8. Create `services/etherscan_service.py`
9. Create `services/groq_service.py`
10. Create `agents/contract_auditor.py`
11. Create `agents/liquidity_agent.py`
12. Create `agents/holder_agent.py`
13. Create `agents/social_agent.py`
14. Create `agents/ai_explainer.py`
15. Create `agents/orchestrator.py`
16. Create `ui/styles.py`
17. Create `ui/risk_gauge.py`
18. Create `ui/agent_cards.py`
19. Create `ui/dashboard.py`
20. Create `app.py` (main entry point)
21. Create `requirements.txt`
22. Create `.streamlit/config.toml`
23. Test with USDT address (should show LOW RISK)
24. Test with a known scam token (should show HIGH RISK)

---

## 15. DISCLAIMER (Must be in UI)

> ⚠️ RugGuard AI is for educational and informational purposes only. It does NOT constitute financial advice. Always do your own research (DYOR) before interacting with any token. The creators are not responsible for any financial losses.

The disclaimer is rendered in **two places**: the sidebar (via `render_disclaimer()` in `app.py`) and at the bottom of the full report (via `render_disclaimer()` in `ui/dashboard.py`).

---

## 16. AGENT ERROR BEHAVIOR

When an individual agent fails (API timeout, network error, unexpected response):

- `AgentResult.risk_score` is set to **50** (neutral midpoint).
- `AgentResult.error` stores the exception message.
- The error message is added to `AgentResult.red_flags`.
- The orchestrator **renormalizes weights** across successful agents only. If an agent fails, its weight is redistributed proportionally among the remaining agents.
- If **all agents fail**, the final score defaults to **50**.

This ensures the user always receives a complete report, even when some data sources are unavailable.

---

