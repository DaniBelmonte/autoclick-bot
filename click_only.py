"""Minimal script to attach to an existing Chrome and click the Pay button."""
from __future__ import annotations

import argparse
import time
from datetime import datetime, time as dtime
from typing import Optional
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PAY_BUTTON_XPATH = "//*[@id='root']/div/div[2]/div/div/div/div[2]/div[3]/div/button"


def wait_until(target: Optional[datetime]) -> None:
    if target is None:
        return
    while True:
        now = datetime.now(target.tzinfo)
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            break
        if remaining > 5:
            time.sleep(min(remaining - 1, 1.0))
        elif remaining > 0.5:
            time.sleep(0.1) 
        else:
            time.sleep(0.005)


def parse_run_at(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    tz = ZoneInfo("Europe/Madrid")
    value = value.strip()
    if ":" in value and len(value) <= 8 and "T" not in value:
        today = datetime.now(tz).date()
        return datetime.combine(today, dtime.fromisoformat(value), tzinfo=tz)
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conecta a un Chrome abierto y pulsa el botón de pagar.")
    parser.add_argument(
        "--debugger-address",
        default="127.0.0.1:9222",
        help="host:puerto del Chrome abierto con --remote-debugging-port (default 127.0.0.1:9222)",
    )
    parser.add_argument(
        "--timeout", type=int, default=20, help="Tiempo máximo para localizar el botón (segundos)."
    )
    parser.add_argument(
        "--run-at",
        help="Fecha/hora para pulsar pagar (ISO). Ej: 2025-11-28T00:00:00 o 00:00:00 (Europe/Madrid).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_at = parse_run_at(args.run_at)

    options = webdriver.ChromeOptions()
    options.debugger_address = args.debugger_address
    # Reduce automation flags; keep it minimal to avoid capability errors.
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    wait_until(run_at)
    WebDriverWait(driver, args.timeout).until(
        EC.element_to_be_clickable((By.XPATH, PAY_BUTTON_XPATH))
    ).click()


if __name__ == "__main__":
    main()
