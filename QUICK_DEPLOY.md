# Deploy to Railway - 3 Minutes ⚡

This app is **already configured** for Railway deployment!

## Prerequisites
- ✅ GitHub account  
- ✅ Railway account (free at https://railway.app)
- ✅ Your code pushed to GitHub

---

## 🚀 Deployment Steps

### Step 1: Commit & Push to GitHub (2 minutes)

```bash
# From your project folder
cd d:\Anajak API Payment\payment-test

# Add all files
git add .

# Commit
git commit -m "ABA KHQR ready for Railway deployment"

# Push to GitHub
git push origin main
```

### Step 2: Create Railway Project (1 minute)

1. Go to: https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Choose your repository
5. Click **"Deploy"**

✅ **Done!** Railway auto-deploys.

---

## 🎉 Your App is Live!

Railway will show you the URL:
```
https://your-project-name.railway.app
```

### Access Your Payment UIs

**Fast KHQR:**
```
https://your-project-name.railway.app/
```

**ABA Checkout:**
```
https://your-project-name.railway.app/checkout
```

---

## ⚙️ Configuration (Optional)

### Before Deployment

Edit `templates/checkout.html` and update merchant ID:

```javascript
// Around line 279
merchant_id: 'YOUR_MERCHANT_ID_HERE',  // ← Add your ABA Merchant ID
```

Then push to GitHub → Railway auto-redeploys!

---

## 📊 How It Works

1. You push code to GitHub
2. Railway detects changes
3. Railway reads your `Dockerfile`
4. Builds Docker image with:
   - Python 3.11
   - All packages from `requirements.txt`
   - Your Flask app
5. Deploys container
6. App goes live with HTTPS

---

## 🔍 Monitor Your App

### View Logs
1. Go to Railway Dashboard
2. Select your project
3. Click **"Logs"** tab
4. See real-time activity

### Troubleshoot
```
Look for lines like:
- "Listening on 0.0.0.0:8000"
- "INFO: Application startup complete"
- Any error messages
```

---

## 🛠️ Common Tasks

### Update Code
```bash
# Make changes locally
# Edit any file

# Commit & push
git add .
git commit -m "Update description"
git push

# Railway auto-redeploys! (30 seconds)
```

### View Logs Live
```
Railway Dashboard → Your Project → Logs
Watch real-time requests and errors
```

### Check Health
```
https://your-project-name.railway.app/health

Expected response:
{
  "status": "ok",
  "redis": "ready",
  "upstream": { ... }
}
```

---

## 🔒 Security

✅ **HTTPS** automatically enabled  
✅ **SSL Certificate** auto-generated  
✅ **Domain** auto-configured  
✅ **Environment variables** protected  
✅ **No exposed credentials** in logs  

---

## 💰 Pricing

**Railway Free Tier includes:**
- ✅ $5 monthly credit (usually enough for this app)
- ✅ Free SSL certificate
- ✅ Custom domain support
- ✅ Real-time logs
- ✅ Automatic deployments

**Estimated monthly cost:** $0-2 (under free credit)

---

## 📝 Dockerfile Explained

Your `Dockerfile` tells Railway how to run your app:

```dockerfile
FROM python:3.11-slim
# Use Python 3.11 lightweight image

WORKDIR /app
# Set working directory

# Install system deps for ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copy & install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-8000}", "--workers", "4", "app:app"]
```

---

## 🚨 If Deployment Fails

### Check These Things

1. **GitHub connection** - Railway can access your repo
2. **Dockerfile syntax** - No errors in Dockerfile
3. **requirements.txt** - All packages installable
4. **app.py syntax** - Valid Python code
5. **Railway logs** - Look for error messages

### Debugging Steps

```bash
# 1. Check local build first
docker build -t my-app .

# 2. Run locally
docker run -p 8000:8000 my-app

# 3. Check Railway logs for errors
# Dashboard → Your Project → Logs tab
```

---

## 🎯 Next Steps

- [ ] Push code to GitHub
- [ ] Create Railway project
- [ ] Verify deployment succeeds
- [ ] Test both UIs work
- [ ] Share URL with customers
- [ ] Monitor logs for errors
- [ ] Set up merchant account (for real payments)

---

## 📞 Quick Help

**Railway won't deploy?**
- Check Railway logs tab
- Verify GitHub connection
- Ensure Dockerfile is correct
- Rebuild project in dashboard

**App crashes after deploy?**
- Check Railway logs (Logs tab)
- Verify PORT env var works
- Check all imports in app.py
- Test locally first: `python app.py`

**Static files not loading?**
- Verify `static/` folder exists in GitHub
- Check file paths in HTML
- Restart deployment in Railway

---

## 🏁 Success!

Your payment system is now:
- ✅ Deployed to Railway
- ✅ Live with HTTPS
- ✅ Accessible worldwide
- ✅ Auto-updating on git push
- ✅ Monitored & logged
- ✅ Production ready

Share your URLs with customers! 🚀

---

**Need more help?**  
- Railway Docs: https://docs.railway.app
- Your Project Logs: Railway Dashboard → Logs tab
- GitHub Commit History: See deployment history

**You're all set!** 🎉
