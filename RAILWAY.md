# Deployment Guide for Railway

Your app is now configured for Railway hosting! Here's how to deploy:

## Prerequisites
- GitHub account
- Railway account (free tier available at https://railway.app)
- Your code pushed to GitHub

## Deployment Steps

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Ready for Railway deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Create Railway Account
- Go to https://railway.app
- Sign up with GitHub (easiest)
- Authorize Railway to access your repositories

### 3. Deploy on Railway
1. Click **New Project**
2. Select **Deploy from GitHub repo**
3. Choose your repository
4. Railway will automatically:
   - Read the `Procfile` and `Dockerfile`
   - Install dependencies from `requirements.txt`
   - Deploy your Flask app

### 4. Configure Environment (if needed)
Railway automatically sets the `PORT` environment variable. No additional config needed!

### 5. Access Your App
Railway will provide a public URL. Your app will be live at:
- `https://your-project.railway.app`

## How It Works
- **Dockerfile**: Ensures Python 3.11 with all system dependencies for reportlab
- **Procfile**: Tells Railway how to start your app (gunicorn)
- **requirements.txt**: All Python dependencies
- **app.py**: Already configured to use the PORT environment variable

## Features
✅ Health check endpoint: `/health`
✅ Automatic scaling (if needed on paid tier)
✅ HTTPS out of the box
✅ Custom domain support
✅ GitHub integration (auto-deploy on push)

## Troubleshooting

### App won't start
- Check Railway logs: Dashboard → Your App → Logs
- Verify `PORT` environment variable is being used

### Build fails
- Check Docker image size
- Verify all dependencies in `requirements.txt` are installable

### Health check failing
- Ensure `/health` endpoint is working
- Check API connectivity to `https://api.anajak.site/health`

For more info: https://docs.railway.app
