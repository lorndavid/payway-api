#!/usr/bin/env python3
"""
fast_khqr.py - Ultra fast KHQR generator using Anajak API
Usage:
  python fast_khqr.py 500                  # generate + save PNG (uses official download)
  python fast_khqr.py 1200 --out myqr.png  # custom filename
  python fast_khqr.py 100 --raw            # just print the qr_string (no image)
  python fast_khqr.py --status <tran_id> <client_id>   # check status once
  python fast_khqr.py 50 --watch           # generate + poll until paid or timeout

Fast path: directly downloads the pre-rendered KHQR PNG from ABA (no local QR encoding).
Only dependency: requests (already in requirements).
"""

import argparse
import json
import sys
import time
from pathlib import Path

import requests

ANAJAK_CREATE = "https://api.anajak.site/api/create-qr"
ANAJAK_CHECK = "https://api.anajak.site/api/check-status"
ANAJAK_HEALTH = "https://api.anajak.site/health"

# Your merchant ABA PayWay link (update if needed)
DEFAULT_ABA_URL = "https://link.payway.com.kh/ABAPAYFB405176Y"


def create_qr(amount: float, url: str, timeout: int = 45, retries: int = 3):
    """Call Anajak to create fast KHQR. Returns full response dict.
    Retries a couple times because upstream can be occasionally slow (playwright nav to ABA).
    """
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                ANAJAK_CREATE,
                json={"url": url, "amount": amount},
                timeout=timeout,
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code == 200:
                return resp.json()
            last_err = RuntimeError(f"Create QR failed [{resp.status_code}]: {resp.text[:300]}")
        except Exception as e:
            last_err = e
        if attempt < retries:
            time.sleep(2 * (attempt + 1))
    raise last_err or RuntimeError("create_qr failed")


def download_qr_image(download_url: str, dest_path: Path, timeout: int = 20) -> Path:
    """Download the official ABA KHQR PNG directly (fastest)."""
    r = requests.get(download_url, timeout=timeout)
    r.raise_for_status()
    dest_path.write_bytes(r.content)
    return dest_path


def check_status(tran_id: str, client_id: str, timeout: int = 15):
    """Check payment status (meta has qr_scanned, payment_approved, finished)."""
    resp = requests.post(
        ANAJAK_CHECK,
        json={"tran_id": tran_id, "client_id": client_id},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def print_result(data: dict, image_path: Path | None = None):
    print("\n=== KHQR GENERATED (Anajak fast) ===")
    print(f"tran_id     : {data.get('status', {}).get('tran_id')}")
    print(f"client_id   : {data.get('client_id')}")
    print(f"amount      : {data.get('transaction_summary', {}).get('order_details', {}).get('amount')}")
    print(f"merchant    : {data.get('transaction_summary', {}).get('merchant', {}).get('company')}")
    print(f"expire_sec  : {data.get('expire_in_sec')}")
    qr_str = data.get("qr_string", "")
    if qr_str:
        print(f"qr_string   : {qr_str[:70]}...")
    if image_path:
        print(f"image       : {image_path.resolve()}")
    if data.get("download_qr"):
        print(f"download_url: {data['download_qr'][:80]}...")
    print("====================================\n")


def cmd_generate(args):
    print(f"[fast] Creating KHQR for amount={args.amount} ...")
    data = create_qr(args.amount, args.url)

    tran_id = data.get("status", {}).get("tran_id")
    client_id = data.get("client_id")

    image_path = None
    if not args.raw:
        if data.get("download_qr"):
            # FAST: use official image, no qrcode/pillow
            out_name = args.out or f"khqr_{tran_id}.png"
            image_path = Path(out_name)
            print("[fast] Downloading official KHQR image from ABA...")
            download_qr_image(data["download_qr"], image_path)
            print(f"[fast] Saved {image_path}")
        else:
            # Rare fallback - would need qrcode lib here, but for --fast we skip heavy
            print("[warn] No download_qr in response. Only qr_string available.")
            if args.out:
                print("[info] To render PNG you need qrcode + pillow + the qr_string.")

    print_result(data, image_path)

    if args.watch:
        print("[fast] Starting payment watch (polling every 2s)...")
        cmd_watch(tran_id, client_id, max_seconds=180)


def cmd_check(tran_id: str, client_id: str):
    data = check_status(tran_id, client_id)
    meta = data.get("meta", {})
    print(json.dumps(data, indent=2))
    print("\n--- meta ---")
    print(f"qr_scanned      : {meta.get('qr_scanned')}")
    print(f"payment_approved: {meta.get('payment_approved')}")
    print(f"finished        : {meta.get('finished')}")


def cmd_watch(tran_id: str, client_id: str, max_seconds: int = 180):
    start = time.time()
    last = ""
    while time.time() - start < max_seconds:
        try:
            data = check_status(tran_id, client_id)
            meta = data.get("meta", {})
            status_line = (
                f"scanned={meta.get('qr_scanned')} "
                f"approved={meta.get('payment_approved')} "
                f"finished={meta.get('finished')}"
            )
            if status_line != last:
                print(f"[{int(time.time()-start)}s] {status_line}")
                last = status_line

            if meta.get("payment_approved") or meta.get("finished"):
                print("\n✅ PAYMENT APPROVED / FINISHED!")
                print(json.dumps(meta, indent=2))
                return 0
        except Exception as e:
            print("check error:", e)
        time.sleep(2)
    print("\n[timeout] Payment not completed within time limit.")
    return 1


def cmd_health():
    r = requests.get(ANAJAK_HEALTH, timeout=5)
    print("Anajak upstream:", r.text)


def main():
    parser = argparse.ArgumentParser(description="Fast KHQR generator via Anajak API")
    parser.add_argument("amount", nargs="?", type=float, help="Amount in KHR (e.g. 1000)")
    parser.add_argument("--out", "-o", help="Output PNG filename (default: khqr_<tran_id>.png)")
    parser.add_argument("--raw", action="store_true", help="Only output the raw qr_string (for scripts)")
    parser.add_argument("--watch", "-w", action="store_true", help="After generate: poll until paid")
    parser.add_argument("--status", nargs=2, metavar=("TRAN_ID", "CLIENT_ID"),
                        help="Check status for existing tran_id + client_id")
    parser.add_argument("--health", action="store_true", help="Check Anajak service health")
    parser.add_argument("--url", default=DEFAULT_ABA_URL, help="Override ABA PayWay merchant URL")

    args = parser.parse_args()

    if args.health:
        cmd_health()
        return

    if args.status:
        tran_id, client_id = args.status
        cmd_check(tran_id, client_id)
        return

    if args.amount is None:
        parser.print_help()
        print("\nExample: python fast_khqr.py 500 --watch")
        sys.exit(1)

    try:
        cmd_generate(args)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
