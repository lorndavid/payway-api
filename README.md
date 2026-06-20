# ABA KHQR Payment System - Production Ready ✅

Official ABA KHQR payment integration with **two flexible checkout UIs** and real-time payment confirmation.

**Powered by:** Anajak API + ABA PayWay  
**Deployment:** Railway (free tier available)  
**Status:** Production Ready 🚀

---

## 📁 Project Structure

```
payment-test/
├── app.py                          # Flask backend
├── fast_khqr.py                    # CLI tool
├── requirements.txt                # Dependencies
├── Dockerfile                      # Container setup
├── railway.json                    # Railway config
├── Procfile                        # Process file
│
├── templates/
│   ├── index.html                  # Fast KHQR UI
│   └── checkout.html               # ABA Checkout UI (NEW)
│
├── static/
│   └── aba-checkout.min.js         # ABA SDK (NEW)
│
├── README.md                       # This file
├── ABA_INTEGRATION.md              # Full integration guide
└── RAILWAY.md                      # Deployment guide
```

---

## 🚀 Two Payment Experiences

### 1. Fast KHQR Direct (`/`)
**Best for:** Quick QR code scanning  
**URL:** `http://localhost:5000/` or `https://your-app.railway.app/`

- Enter amount
- Generate KHQR code
- Scan with ABA Mobile app
- Real-time payment confirmation
- Download receipt as PDF

### 2. Official ABA Checkout (`/checkout`)
**Best for:** Full payment flow with multiple methods  
**URL:** `http://localhost:5000/checkout` or `https://your-app.railway.app/checkout`

- Enter amount  
- Choose: KHQR or ABA Pay
- Official ABA checkout modal
- Scan or wallet payment
- Auto-redirect on success

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python app.py
```

### 3. Open Browser
```
Fast KHQR:      http://localhost:5000/
ABA Checkout:   http://localhost:5000/checkout
Health Check:   http://localhost:5000/health
```

### 4. Deploy to Railway
```bash
git add .
git commit -m "Ready for Railway deployment"
git push
```

Then:
1. Go to https://railway.app
2. Create new project
3. Connect GitHub repo
4. Railway auto-deploys with Dockerfile
5. Your app goes live! 🎉

---

## 🔧 Configuration

### For ABA Checkout to Work

Edit `templates/checkout.html` around line 279:

```javascript
merchant_id: 'YOUR_MERCHANT_ID',  // ← Replace with your ABA Merchant ID
```

**Get your Merchant ID:**
- ABA PayWay Portal: https://checkout.payway.com.kh
- Contact ABA: support@ababank.com
- Usually looks like: `ABAPAYFB405176Y`

---

## 📊 API Reference

```
POST /generate
├─ Request: { amount: 1000 }
└─ Response: { success, qr_url, qr_string, tran_id, client_id, expire_in_sec }

POST /check
├─ Request: { tran_id, client_id }
└─ Response: { meta: { qr_scanned, payment_approved, finished } }

GET /status-stream
├─ Query: ?tran_id=...&client_id=...
└─ Response: Server-Sent Events (real-time updates)

GET /health
└─ Response: { status: "ok", redis: "ready", upstream: {...} }

GET /download-receipt
├─ Query: ?tran_id=...&merchant=...&amount=...&currency=...
└─ Response: PDF file download

GET /static/<file>
└─ Serves: JavaScript, CSS, images from `static/` folder
```

---

## 🧪 Testing

### Local Testing
```bash
# Terminal 1: Start server
python app.py

# Terminal 2: Test generation
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000}'

# Test health
curl http://localhost:5000/health
```

### Browser Testing
1. Go to `http://localhost:5000/`
2. Enter amount: `1000` KHR
3. Click "Generate KHQR"
4. QR appears (from Anajak API)
5. Can download or display in ABA Mobile

---

## 🛠️ CLI Tool (Optional)

Use the included CLI for automation:

```bash
# Generate + save QR image
python fast_khqr.py 1500

# Raw QR string (for scripts)
python fast_khqr.py 250 --raw

# Watch until paid
python fast_khqr.py 1000 --watch

# Check previous transaction
python fast_khqr.py --status TID-123456 client-id-xyz

# Verify API health
python fast_khqr.py --health
```

---

## 📱 Mobile Support

Both UIs are fully responsive:

### iOS
- Open in Safari
- Test KHQR with ABA Mobile app
- Scan QR code

### Android  
- Open in Chrome
- Test with ABA Mobile app
- Full payment flow works

---

## 🔒 Security Features

- ✅ HTTPS enabled (Railway auto)
- ✅ 256-bit SSL encryption
- ✅ No sensitive data in logs
- ✅ Secure Server-Sent Events
- ✅ CORS configured for ABA
- ✅ Input validation on all endpoints

---

## 🚀 Production Deployment

### Step 1: Update Configuration
```javascript
// In templates/checkout.html line ~279
merchant_id: 'YOUR_PRODUCTION_MERCHANT_ID',
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Production ready"
git push origin main
```

### Step 3: Deploy to Railway
1. Go to https://railway.app
2. Sign up (free tier available)
3. Create new project
4. Select GitHub repository
5. Railway auto-detects Docker setup
6. Deploy happens automatically
7. Your app goes live at: `https://your-project-name.railway.app`

### Step 4: Monitor
- Dashboard: View logs in real-time
- Alerts: Set up optional notifications
- Metrics: Monitor CPU, memory, requests

---

## 📝 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend, all API endpoints |
| `templates/index.html` | Fast KHQR UI |
| `templates/checkout.html` | ABA Checkout UI |
| `static/aba-checkout.min.js` | ABA Payway SDK |
| `requirements.txt` | Python packages |
| `Dockerfile` | Container image |
| `railway.json` | Railway config |
| `ABA_INTEGRATION.md` | Full integration docs |
| `RAILWAY.md` | Deployment guide |

---

## 🐛 Troubleshooting

### "Failed to generate QR"
- Check: `curl http://localhost:5000/health`
- Verify internet connection
- Check Anajak API status

### Payment not confirming
- Check browser console (F12 → Console)
- Look at Network tab for SSE connection
- Verify tran_id and client_id are valid

### Static files not loading
- Ensure `static/` folder exists
- Check file paths match in HTML
- Restart Flask server

### ABA Checkout modal not showing
- Verify `aba-checkout.min.js` loaded (check Network tab)
- Check merchant_id is set in checkout.html
- Look for JavaScript errors in console

---

## 📚 Documentation

- **[ABA_INTEGRATION.md](ABA_INTEGRATION.md)** - Complete integration guide
- **[RAILWAY.md](RAILWAY.md)** - Railway deployment steps
- **[Anajak API](https://anajak.site/aba/)** - API reference
- **[ABA PayWay](https://checkout.payway.com.kh)** - Official docs

---

## 💡 Features Included

✅ Real-time QR code generation  
✅ Server-Sent Events for instant updates  
✅ PDF receipt generation  
✅ Official ABA checkout integration  
✅ Multiple payment methods (KHQR + ABA Pay)  
✅ Mobile responsive UI  
✅ Health check endpoint  
✅ Full error handling  
✅ Railway deployment ready  
✅ Docker containerized  
✅ Production secure  

---

## 🎯 Next Steps

1. **Local Testing**
   ```bash
   python app.py
   # Visit: http://localhost:5000/
   ```

2. **Configure Merchant ID**
   - Edit `templates/checkout.html`
   - Add your ABA Merchant ID

3. **Deploy to Railway**
   ```bash
   git push  # Railway auto-deploys
   ```

4. **Go Live**
   - Your app: `https://your-project.railway.app`
   - Share the URL with customers

---

## 📞 Support

**Anajak Issues:** https://anajak.site  
**ABA PayWay:** Contact ABA Bank  
**Railway Help:** https://docs.railway.app  

---

## 📄 License

This integration is free to use. Follow ABA Bank and Anajak terms of service.

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
