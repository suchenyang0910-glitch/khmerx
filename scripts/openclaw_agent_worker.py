from __future__ import annotations

import os
import time

import httpx


def main():
    api = os.getenv("KHMERX_API", "http://127.0.0.1:3040").rstrip("/")
    key = os.getenv("OPENCLAW_API_KEY", "").strip()
    if not key:
        raise SystemExit("missing OPENCLAW_API_KEY")

    headers = {"X-OpenClaw-Key": key}
    with httpx.Client(timeout=20.0, headers=headers) as client:
        while True:
            r = client.get(f"{api}/openclaw/risk/events/pending", params={"limit": 20})
            r.raise_for_status()
            events = r.json() if r.content else []
            if not events:
                time.sleep(5)
                continue

            for ev in events:
                action = "mark_handled"
                reason = "auto"
                sev = (ev.get("severity") or "").lower()
                if sev == "high":
                    action = "manual_review"
                    reason = "high severity risk event"
                elif ev.get("event_type") == "repayment_overdue":
                    payload = ev.get("payload") or {}
                    if isinstance(payload, dict) and int(payload.get("overdue_days", 0)) >= 7:
                        action = "block_user"
                        reason = "overdue >= 7 days"

                client.post(
                    f"{api}/openclaw/risk/events/{ev['id']}/decide",
                    json={"action": action, "reason": reason},
                ).raise_for_status()


if __name__ == "__main__":
    main()

