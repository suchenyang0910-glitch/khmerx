"""
汇率爬虫 — 爬取 ABA Bank 或 ACLEDA 的 USD/KHR 汇率

目标网站：
- ABA Bank: https://www.ababank.com/ (exchange rates)
- ACLEDA: https://www.acledabank.com.kh/ (foreign exchange)

用法：
    python -m app.services.rate_fetcher
    或
    from app.services.rate_fetcher import fetch_aba_rate, fetch_acleda_rate
"""
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 尝试导入 requests 和 BeautifulSoup
try:
    import requests
except ImportError:
    requests = None  # type: ignore

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore


def fetch_aba_rate() -> Optional[dict]:
    """
    从 ABA Bank 官网爬取 USD/KHR 汇率
    返回: {"buy": float, "sell": float, "source": "ABA"} 或 None
    """
    if not requests or not BeautifulSoup:
        logger.warning("requests/beautifulsoup4 not installed, cannot fetch ABA rate")
        return None

    try:
        url = "https://www.ababank.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # ABA 官网的汇率通常在表格中，查找包含 "USD" 的行
        buy_rate = None
        sell_rate = None

        # 尝试多种 selector 模式
        # 模式1: 查找表格
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                cell_texts = [c.get_text(strip=True) for c in cells]
                combined = " ".join(cell_texts)
                if "USD" in combined.upper():
                    # 尝试提取数字
                    numbers = re.findall(r"[\d,]+\.?\d*", combined)
                    if len(numbers) >= 2:
                        try:
                            buy_rate = float(numbers[0].replace(",", ""))
                            sell_rate = float(numbers[1].replace(",", ""))
                        except ValueError:
                            pass
                    break
            if buy_rate and sell_rate:
                break

        # 模式2: 查找带有 exchange/rate 字样的 div
        if not buy_rate or not sell_rate:
            rate_elements = soup.find_all(
                lambda tag: tag.name in ("div", "span", "td", "p")
                and "USD" in tag.get_text(strip=True).upper()
                and any(c.isdigit() for c in tag.get_text(strip=True))
            )
            for el in rate_elements:
                numbers = re.findall(r"[\d,]+\.?\d*", el.get_text(strip=True))
                if len(numbers) >= 2:
                    try:
                        buy_rate = float(numbers[0].replace(",", ""))
                        sell_rate = float(numbers[1].replace(",", ""))
                        break
                    except ValueError:
                        pass

        if buy_rate and sell_rate:
            logger.info(f"ABA rate: buy={buy_rate}, sell={sell_rate}")
            return {"buy": buy_rate, "sell": sell_rate, "source": "ABA"}

        logger.warning("Could not parse ABA rate from page")
        return None

    except Exception as e:
        logger.error(f"Failed to fetch ABA rate: {e}")
        return None


def fetch_acleda_rate() -> Optional[dict]:
    """
    从 ACLEDA Bank 官网爬取 USD/KHR 汇率
    返回: {"buy": float, "sell": float, "source": "ACLEDA"} 或 None
    """
    if not requests or not BeautifulSoup:
        logger.warning("requests/beautifulsoup4 not installed, cannot fetch ACLEDA rate")
        return None

    try:
        url = "https://www.acledabank.com.kh/kh/eng/foreignexchange"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        buy_rate = None
        sell_rate = None

        # ACLEDA 的汇率通常在表格中
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                cell_texts = [c.get_text(strip=True) for c in cells]
                combined = " ".join(cell_texts)
                if "USD" in combined.upper():
                    numbers = re.findall(r"[\d,]+\.?\d*", combined)
                    if len(numbers) >= 2:
                        try:
                            buy_rate = float(numbers[0].replace(",", ""))
                            sell_rate = float(numbers[1].replace(",", ""))
                        except ValueError:
                            pass
                    break
            if buy_rate and sell_rate:
                break

        if buy_rate and sell_rate:
            logger.info(f"ACLEDA rate: buy={buy_rate}, sell={sell_rate}")
            return {"buy": buy_rate, "sell": sell_rate, "source": "ACLEDA"}

        logger.warning("Could not parse ACLEDA rate from page")
        return None

    except Exception as e:
        logger.error(f"Failed to fetch ACLEDA rate: {e}")
        return None


def fetch_rate() -> Optional[dict]:
    """
    智能获取汇率：先尝试 ABA，失败则尝试 ACLEDA
    返回: {"buy": float, "sell": float, "source": str} 或 None
    """
    result = fetch_aba_rate()
    if result:
        return result
    result = fetch_acleda_rate()
    if result:
        return result
    logger.warning("All rate fetchers failed")
    return None


# ── CLI ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    result = fetch_rate()
    if result:
        print(f"💰 {result['source']} USD/KHR: Buy={result['buy']}, Sell={result['sell']}")
    else:
        print("❌ Failed to fetch rate from all sources")
