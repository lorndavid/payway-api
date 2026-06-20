# ABA KHQR Payment Integration Guide

Your payment system now has **two options** for processing ABA KHQR payments:

## 1. **Fast KHQR UI** (Current)
- **URL:** `/` (index.html)
- **Type:** Custom real-time QR display with Server-Sent Events
- **Best for:** Direct KHQR QR code scanning
- **Features:**
  - Live status updates (QR scanned, payment approved)
  - Countdown timer
  - Real-time payment confirmation
  - PDF receipt generation

## 2. **Official ABA Checkout** (New)
- **URL:** `/checkout` (checkout.html)
- **Type:** Official ABA Payway integration
- **Best for:** Complete payment flow with multiple payment methods
- **Features:**
  - KHQR payment option
  - ABA Pay wallet option
  - Official ABA branding
  - Mobile app integration support

---

## Configuration Required

### For ABA Checkout to Work Fully

Update your merchant details in [checkout.html](templates/checkout.html):

```javascript
const checkoutData = {
  form_url: 'https://checkout.payway.com.kh',
  merchant_id: 'YOUR_MERCHANT_ID',  // ← Replace this
  tran_id: data.tran_id,
  client_id: data.client_id,
  amount: amount.toString(),
  currency: 'KHR',
  // ... rest of config
};
```

### Environment Variables (Optional)

Set in your deployment:
```bash
ABA_MERCHANT_ID=your_merchant_id_here
```

Then update checkout.html line 279:
```javascript
merchant_id: process.env.ABA_MERCHANT_ID || 'MERCHANT_ID',
```

---

## API Endpoints Used

### Both UIs use these backend routes:

**POST `/generate`**
- Generates KHQR string via Anajak API
- Returns: QR image URL, transaction ID, expiration time
- Used by: Both `/` and `/checkout`

**POST `/check`**
- Checks payment status
- Returns: Payment approval meta-data

**GET `/status-stream`**
- Server-Sent Events endpoint
- Real-time payment status updates
- Used by: `/` (main UI)

**GET `/health`**
- Service health check
- Verifies upstream Anajak connectivity

**GET `/download-receipt`**
- Generates PDF receipt
- Used by: Success screen

---

## How to Use

### Option 1: Fast KHQR Direct (Recommended for QR-only)
```
1. Navigate to: https://your-app.railway.app/
2. Enter amount
3. Click "Generate KHQR"
4. Customer scans QR with ABA Mobile
5. Real-time confirmation
6. Download receipt
```

### Option 2: Official ABA Checkout
```
1. Navigate to: https://your-app.railway.app/checkout
2. Enter amount
3. Choose payment method (KHQR or ABA Pay)
4. Click "Generate Payment"
5. ABA checkout modal opens
6. Complete payment in ABA's official flow
7. Auto-redirect to success or error page
```

---

## Payment Flow

```
[Customer] → [Your App] → [Anajak API] → [ABA PayWay]
                ↓
         [Generate KHQR]
         [tran_id, client_id]
                ↓
         [Display QR / Checkout]
                ↓
         [ABA Mobile / Payway]
                ↓
         [Payment Approved]
                ↓
         [Success Screen]
```

---

## Testing

### Test Amounts
- Any valid Khmer Riel amount works
- Recommended for testing: 1000, 5000, 10000 KHR

### Test Locally
```bash
# Terminal 1: Start the server
python app.py

# Terminal 2: Open browser
http://localhost:5000/
http://localhost:5000/checkout
```

### Check Anajak Health
```bash
curl https://api.anajak.site/health
# Expected: {"status": "ok", "redis": "ready"}
```

---

## Customization

### Branding
- Edit merchant name in templates
- Update logo/flag emoji (🇰🇭 Cambodia flag)
- Change colors in CSS :root variables

### Success/Error Callbacks
In [checkout.html](templates/checkout.html) line 277-285:
```javascript
onSuccess: function(result) {
  // Custom success logic here
  console.log('Payment successful:', result);
  alert('Payment completed!');
  window.location.href = '/success?tran_id=' + data.tran_id;
},
onError: function(error) {
  // Custom error logic here
  console.log('Payment error:', error);
  alert('Payment failed: ' + error.message);
}
```

---

## Troubleshooting

### "QR unavailable" Error
**Cause:** Anajak API not returning download_qr URL
**Solution:**
1. Check `/health` endpoint
2. Verify ABA link is correct in app.py
3. Ensure internet connection

### Payment not confirming
**Cause:** Status stream not receiving updates
**Solution:**
1. Check browser console for errors
2. Verify SSE connection in DevTools Network tab
3. Test `/check` endpoint directly with tran_id

### ABA Checkout modal not opening
**Cause:** aba-checkout.min.js not loaded
**Solution:**
1. Verify `/static/aba-checkout.min.js` exists
2. Check browser console for JavaScript errors
3. Ensure merchant_id is set correctly

### Receipt PDF not downloading
**Cause:** Download-receipt endpoint error
**Solution:**
1. Check ReportLab is installed: `pip list | grep reportlab`
2. Verify all required parameters in URL
3. Check app logs for errors

---

## Production Deployment

### Railway Deployment Steps
```bash
git add .
git commit -m "Add ABA KHQR checkout integration"
git push

# Then in Railway Dashboard:
# 1. Create new project
# 2. Connect GitHub repo
# 3. Deploy automatically
```

### Security Checklist
- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for merchant ID
- [ ] Enable HTTPS (Railway does this automatically)
- [ ] Add CORS headers if needed for third-party sites
- [ ] Implement webhook validation for production
- [ ] Store transaction logs securely

---

## Support

**Anajak API Docs:** https://anajak.site/aba/
**ABA PayWay Docs:** https://checkout.payway.com.kh
**Railway Docs:** https://docs.railway.app

---

## Next Steps

1. **Update merchant_id** in checkout.html
2. **Test both UIs** locally
3. **Deploy to Railway**
4. **Monitor logs** in Railway dashboard
5. **Set up webhook** for production payment verification (optional)

Good luck! 🚀
