# Free Hosting on Render.com (Step-by-Step Guide)

This project is already well prepared for **Render** (a popular free Python hosting platform).

**Why Render?**
- Free tier for web services (with limitations)
- Automatic deploys from GitHub
- Uses your existing `Procfile` + `requirements.txt`
- Supports Flask + gunicorn out of the box
- Easy custom domain + HTTPS

---

## 1. Prepare Your Code (Do This First)

1. Make sure your project is a **Git repository** and pushed to **GitHub**:
   ```bash
   # From inside the payment-test folder (or wherever your app.py + templates live)
   git init
   git add .
   git commit -m "Initial commit - Fast KHQR web UI"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Important files already present** (you don't need to create them):
   - `requirements.txt` (includes Flask, requests, reportlab, gunicorn, qrcode, pillow)
   - `Procfile` → `web: gunicorn app:app`
   - `app.py` (now respects `PORT` environment variable)
   - `.gitignore` (we just added one — pycache, *.png samples, venvs, etc. are ignored)

3. (Recommended) Add a health endpoint test:
   - The app already has `GET /health`

---

## 2. Create a Free Render Account

1. Go to https://render.com
2. Click **Sign Up** → choose **GitHub** (easiest)
3. Authorize Render to access your GitHub repositories
4. (Optional but recommended) Create a new GitHub repo just for this project if you haven't already

---

## 3. Create the Web Service on Render (Free Tier)

1. After logging in, click the **New +** button (top right) → **Web Service**
2. In the "Connect a repository" section:
   - Find and select your GitHub repo that contains `app.py`, `templates/`, `Procfile`, etc.
3. Fill in the service settings:

   | Field                  | Recommended Value                              | Notes |
   |------------------------|------------------------------------------------|-------|
   | **Name**               | `anajak-khqr` or `lorn-david-pay`              | This becomes part of your URL |
   | **Region**             | Oregon (US West) or Frankfurt (closest to you) | |
   | **Branch**             | `main`                                         | |
   | **Root Directory**     | (leave empty)                                  | Only change if your app.py is in a subfolder |
   | **Environment**        | `Python 3`                                     | Auto-detected |
   | **Build Command**      | `pip install -r requirements.txt`              | Or leave blank — Render auto-detects |
   | **Start Command**      | (leave blank)                                  | **Uses your Procfile** (`web: gunicorn app:app`) |
   | **Plan**               | **Free**                                       | Important! |

4. Click **Advanced** (optional):
   - You can add a Health Check Path: `/health`
   - No environment variables are required for this app.

5. Click **Create Web Service**

Render will now:
- Clone your repo
- Run `pip install -r requirements.txt`
- Start the service using gunicorn via the Procfile

---

## 4. Wait for the First Deploy

- Watch the **Logs** tab in Render.
- First deploy usually takes 1–3 minutes.
- You will see something like:
  ```
  [INFO] Starting gunicorn ...
  [INFO] Listening at: http://0.0.0.0:10000
  ```
- When you see "Deploy successful", your app is live!

Your public URL will be something like:
**https://anajak-khqr.onrender.com**

---

## 5. Test Your Deployed App

1. Open the URL in your browser.
2. Try the main flow:
   - Enter amount (e.g. 1500)
   - Click **Generate KHQR**
   - You should see the QR screen quickly (the improvements we made help with this)
3. Test the health endpoint directly:
   ```
   https://YOUR-APP.onrender.com/health
   ```
   It should return JSON with `"status": "ok"` and upstream info.

4. (Optional) Use the status stream — generate a QR and have someone scan it with ABA (or test with a real payment if you have the merchant link set up).

---

## 6. Important Free Tier Limitations & Tips

- **Spins down after inactivity**: After ~15 minutes with no traffic, the service sleeps.
  - First visit after sleep = **cold start** (can take 10–30+ seconds).
  - Subsequent requests are fast.
- **No always-on**: For 24/7 uptime you need to upgrade to a paid plan.
- **Wake-up trick**: Some people add a free UptimeRobot ping every 5–10 minutes to keep it warm (search "uptime robot render free").
- **Logs**: Available in the Render dashboard (last 1000 lines on free).
- **Auto deploys**: Every push to `main` will automatically redeploy.
- **Custom domain**: Free on paid plans only (or use a subdomain via Cloudflare etc.).

---

## 7. Updating the Code Later

Just push to GitHub:

```bash
git add .
git commit -m "Improve speed + add better error messages"
git push
```

Render will automatically detect the push and start a new deploy.

---

## 8. Troubleshooting

**"Application error" or 502/503**
- Check the **Logs** tab in Render.
- Common causes: missing dependency in requirements.txt, startup crash.

**Port issues**
- We already fixed `app.py` to read `os.environ.get("PORT")`.
- Gunicorn (from Procfile) also respects the port Render injects.

**Slow first generate after deploy**
- This is normal on free tier (cold Python + external Anajak API call).
- The speed improvements (faster polling 0.8s, tighter timeouts, smoother finally block) help a lot once the dyno is warm.

**Static files / templates not loading**
- Make sure `templates/index.html` is committed and pushed (it should be).

**Anajak API calls failing**
- The upstream `https://api.anajak.site` must be reachable from Render (it is public).
- Same behavior as your local machine.

---

## Bonus: Make It Feel Faster on Free Hosting

We already did several optimizations in this session:

- Reduced internal status poll from 1.5s → **0.8s**
- Tighter request timeouts (generate 20s, checks 8s)
- Faster retry backoff (0.6s)
- Smoother "Generate" finally block — no more button state flicker when switching to QR screen
- PORT support + good Procfile

These changes make both the **Generate** step and the **payment verification** noticeably faster and smoother.

---

## Summary Checklist

- [ ] Code pushed to GitHub with `.gitignore`
- [ ] Render Web Service created (Free plan)
- [ ] First deploy succeeded
- [ ] Tested `/` and `/health`
- [ ] (Optional) Set up UptimeRobot for less cold starts

You're now live on the internet for free!

If you run into any issues during deployment, copy the last 20–30 lines from the Render **Logs** tab and share them.

Good luck with Lorn David payments! 🇰🇭
