# Fast KHQR Generator (Anajak API)

Ultra-fast KHQR (Cambodia) QR code generation and real-time payment status monitoring powered by the Anajak Pay API.

## Features
- **Fast path**: Uses the official `download_qr` pre-rendered PNG from ABA — zero local QR encoding, minimal latency and CPU.
- Web demo (Flask) with live polling for `qr_scanned` / `payment_approved`.
- Powerful CLI `fast_khqr.py` for scripts, terminals, or automation (only needs `requests`).

## Quick Start

```bash
cd payment-test
pip install -r requirements.txt
```

### Web UI (demo)
```bash
python app.py
# open http://127.0.0.1:5000
```

Enter amount (KHR) → Generate → shows official KHQR image instantly + polls status.

### Fast CLI (recommended for speed / scripting)
```bash
# Generate + save official PNG (fastest)
python fast_khqr.py 1500

# Custom output name
python fast_khqr.py 500 -o invoice_123.png

# Only the raw qr_string (pipeable)
python fast_khqr.py 250 --raw

# Generate and watch until customer pays
python fast_khqr.py 1000 --watch

# Check status of a previous transaction
python fast_khqr.py --status 1780561... client-xxx-yyy

# Upstream health
python fast_khqr.py --health
```

## API Routes (this wrapper)
- `POST /generate` → `{ qr_url?, qr?, qr_string, tran_id, client_id, merchant, amount, currency, ... }`
- `POST /check` → Anajak check-status (look at `meta.payment_approved`)
- `GET /health` → this service + upstream

## Notes
- The Anajak `POST /api/create-qr` requires a valid ABA PayWay merchant `url` + `amount`.
- `client_id` + `tran_id` are required together for `/check-status`.
- Upstream can occasionally return 5xx during ABA link navigation (the CLI and backend have light retries).
- When `download_qr` is present we use it directly (fast + canonical image). Local `qrcode`+`pillow` only as rare fallback.

## Raw Anajak Endpoints Used
- `GET https://api.anajak.site/health`
- `POST https://api.anajak.site/api/create-qr`
- `POST https://api.anajak.site/api/check-status`

Built for fast merchant checkout flows.

## Easy Double-Click .bat Files (Windows)

For the simplest experience on Windows (no typing commands):

| File                  | What it does                              | How to use                     |
|-----------------------|-------------------------------------------|--------------------------------|
| `run.bat`             | Menu with all options                     | Double-click → choose 1, 2 or 3 |
| `start-web.bat`       | Starts the web interface + opens browser  | Double-click                   |
| `generate-khqr.bat`   | Prompts for amount and generates QR       | Double-click → type amount     |

**Recommended**: Just double-click `run.bat` — it gives you a simple menu.

> Note: These .bat files assume `python` is available in your PATH and you have already run `pip install -r requirements.txt` at least once.

## New Features in Web UI (Clean Modern Bank UX)

- **No more custom receipt UI**: We removed the built HTML receipt box completely.
- **Real PDF Receipt like ABA**: "Download Receipt (PDF)" button generates and downloads a clean professional PDF receipt (styled exactly like official ABA Bank receipts - blue header, transaction summary, highlighted total, thank you footer).
- **Clean ABA-like Success Message**: On approval, the UI loads a modern, clean bank-style success screen with green check icon, "Payment Successful", simple transaction details list, and ABA blue "Thank you for your payment!" message.
- **ABA-style Background + UX**: Light blue success background, deep #003087 accents, professional clean layout like a real bank account / payment confirmation page.
- **Cancel Payment** and **Back to Main Page** still available for smooth flow.

### Performance Improvements (Faster + Smoother UX)

- **Generate flow**: Immediate loading spinner + status text ("Contacting Anajak API..."). Button and input are disabled instantly. Uses the pre-generated `qr_url` from Anajak/ABA (fastest possible QR image — no local generation delay).
- **Payment status checking**: Replaced client-side polling with **Server-Sent Events (SSE)**. 
  - Server internally checks Anajak every **0.8 seconds** (faster detection of scan/approval).
  - Only pushes updates to the browser when something actually changes (scanned / approved).
  - Feels instant and lag-free on the client. Much better than fixed interval polling.
- Generate flow now has a **smoother finally block** — no button/input state flicker when transitioning to the QR screen.
- Smooth CSS transitions, fade-in animations, and button press feedback throughout.
- Overall: More responsive "bank-like" feel with less perceived waiting.
- **Download Receipt (PNG)**: Click **⬇ Download Receipt (PNG)** for a high-quality image of the receipt.
- **Print / Save as PDF**: Opens a printer-friendly version (use "Save as PDF" in the dialog).
- Receipt includes: Merchant, Amount, Tran ID, Paid time, Method, Status + small QR reference image.
