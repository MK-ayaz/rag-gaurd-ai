"""Agent 4: Social Agent — checks social presence, token age, and known scam patterns."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

from models.risk_report import AgentResult
from services.goplus_service import get_token_security
from config import API_TIMEOUT, CHAINS


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip() == "1"
    return bool(value)


def _check_coingecko(address: str) -> bool:
    """Check if a token is listed on CoinGecko by searching its API."""
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{address.lower()}",
            timeout=API_TIMEOUT,
        )
        return resp.status_code == 200
    except Exception:
        return False


def calculate_social_risk(checks: Dict[str, Any]) -> int:
    risk = 0
    if not checks["has_website"]:
        risk += 15
    if not checks["has_twitter"]:
        risk += 10
    if not checks["has_telegram"]:
        risk += 10
    if not checks["is_on_coingecko"]:
        risk += 15
    if checks["token_age_days"] < 1:
        risk += 25
    elif checks["token_age_days"] < 7:
        risk += 15
    elif checks["token_age_days"] < 30:
        risk += 5
    if checks["is_fake_token"]:
        risk += 30
    return min(risk, 100)


class SocialAgent:
    name = "social"
    display_name = "Social Agent"
    description = "Checks social presence, token age, and known scam patterns"

    def analyze(self, address: str, chain: str) -> AgentResult:
        chain_cfg = CHAINS.get(chain, {})
        chain_id = chain_cfg.get("chain_id", 1)

        gp_data = get_token_security(chain_id, address)

        _website_raw = gp_data.get("website")
        _twitter_raw = gp_data.get("twitter")
        _telegram_raw = gp_data.get("telegram")
        has_website = isinstance(_website_raw, str) and _website_raw.strip() not in ("", "0")
        has_twitter = isinstance(_twitter_raw, str) and _twitter_raw.strip() not in ("", "0")
        has_telegram = isinstance(_telegram_raw, str) and _telegram_raw.strip() not in ("", "0")
        is_fake_token = _to_bool(gp_data.get("is_fake_token"))
        is_airdrop_scam = _to_bool(gp_data.get("is_airdrop_scam"))

        # Token age from GoPlusLabs personal_holder_count timestamp or token creation
        token_age_days = 0
        created_at = gp_data.get("token_creation_time") or gp_data.get("created_at")
        if created_at:
            try:
                ts = int(float(created_at))
                token_age_days = (datetime.now(timezone.utc).timestamp() - ts) / 86400
            except (ValueError, TypeError):
                pass

        # CoinGecko listing check
        is_on_coingecko = _check_coingecko(address) if chain == "ethereum" else False

        checks: Dict[str, Any] = {
            "has_website": has_website,
            "has_twitter": has_twitter,
            "has_telegram": has_telegram,
            "is_on_coingecko": is_on_coingecko,
            "token_age_days": max(0, int(token_age_days)),
            "is_fake_token": is_fake_token,
            "is_airdrop_scam": is_airdrop_scam,
            "website_url": _website_raw if isinstance(_website_raw, str) else "",
            "twitter_url": _twitter_raw if isinstance(_twitter_raw, str) else "",
            "telegram_url": _telegram_raw if isinstance(_telegram_raw, str) else "",
        }

        risk_score = calculate_social_risk(checks)

        red_flags: List[str] = []
        if is_fake_token:
            red_flags.append("Fake token detected — impersonating a legitimate project")
        if is_airdrop_scam:
            red_flags.append("Associated with airdrop scam pattern")
        if not has_website:
            red_flags.append("No website")
        if not has_twitter:
            red_flags.append("No Twitter/X presence")
        if not has_telegram:
            red_flags.append("No Telegram community")
        if not is_on_coingecko:
            red_flags.append("Not listed on CoinGecko")
        if token_age_days < 1:
            red_flags.append("Token is less than 1 day old")
        elif token_age_days < 7:
            red_flags.append(f"Token is only {token_age_days} days old")

        return AgentResult(
            agent_name=self.name,
            risk_score=risk_score,
            checks=checks,
            red_flags=red_flags,
        )
