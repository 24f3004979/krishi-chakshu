# Krishi Chakshu - Deployment Guide

Complete guide to deploy your plant disease detection app to the cloud.

---

## Deployment Platform Comparison

| Platform | Cost | Difficulty | Best For | Model Size Limit | Notes |
|----------|------|-----------|----------|------------------|-------|
| **Railway** | $5-20/mo | ⭐⭐ Easy | Production | 10GB | Best free tier option, generous limits |
| **Render** | Free/Paid | ⭐⭐ Easy | Hobby/Prod | 500MB (free) | Good free tier, simple deployment |
| **PythonAnywhere** | Free/Paid | ⭐ Very Easy | Beginner | 100MB (free) | Easiest for beginners |
| **Heroku** | Paid only | ⭐⭐ Easy | Production | Depends | No longer has free tier |
| **DigitalOcean** | $5-12/mo | ⭐⭐⭐ Medium | Production | 55GB | Most affordable, full control |
| **AWS/Google Cloud** | Pay-as-you-go | ⭐⭐⭐⭐ Hard | Large scale | Unlimited | Powerful, complex setup |
| **ngrok + Local** | Free | ⭐ Very Easy | Testing | Local | Good for quick demos |

---

## RECOMMENDED: Railway.app (Best All-Around)

**Why Railway is best for this project:**
- ✅ Free tier with generous limits
- ✅ Automatic deployment from GitHub
- ✅ Supports large model files (up to 10GB)
- ✅ Good for ML models with TensorFlow
- ✅ Simple CLI deployment

### Step 1: Prepare Your App for Deployment

Create a `Procfile` in your project root:

```
web: python app.py
```

Create a `runtime.txt` (optional but recommended):

```
python-3.10.13
```

### Step 2: Sign Up & Install Railway CLI

1. Go to https://railway.app
2. Sign up with GitHub
3. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
   Or on macOS:
   ```bash
   brew install railway
   ```

### Step 3: Deploy Your App

```bash
cd /home/madhavrimal/workspace/Projects/Krishi_chakshu

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

Railway will:
- Build your app
- Install dependencies from `requirements.txt`
- Start your Flask server
- Give you a live URL

### Step 4: Configure Environment

In Railway dashboard:
1. Click on your project
2. Go to "Variables"
3. Add if needed:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=0
   ```

### Step 5: Access Your App

Your app will be live at: `https://your-app-name.railway.app`

**Cost**: Free tier covers ~5GB/month. For more, upgrade to $5/month.

---

## EASIEST: PythonAnywhere (Beginner-Friendly)

**Best for**: First-time deployment, learning

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Create free account
3. Verify email

### Step 2: Upload Files

1. Open "Files" tab
2. Upload your files or use GitHub:
   ```bash
   # In PythonAnywhere terminal
   git clone https://github.com/YOUR_USERNAME/Krishi_chakshu.git
   ```

### Step 3: Create Web App

1. Click "Web" tab → "Add a new web app"
2. Choose "Python 3.10" + "Flask"
3. PythonAnywhere will create `/var/www/username_pythonanywhere_com_wsgi.py`

### Step 4: Configure WSGI File

Edit the WSGI file to point to your app:

```python
import sys
path = '/home/username/Krishi_chakshu'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 5: Install Dependencies

In PythonAnywhere terminal:

```bash
pip install -r /home/username/Krishi_chakshu/requirements.txt
```

### Step 6: Reload

1. Go to Web tab
2. Click "Reload" button
3. Your app is live at: `https://username.pythonanywhere.com`

**Cost**: Free tier allows 100MB storage. Good for testing.

---

## FREE + EASY: Render.com

**Best for**: Free hosting with reasonable limits

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Connect GitHub

1. Authorize Render to access your GitHub
2. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Select your GitHub repo
3. Configure:
   - **Name**: krishi-chakshu
   - **Runtime**: Python 3.10
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python app.py`

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Your app is live at: `https://krishi-chakshu.onrender.com`

**Cost**: Free tier pauses after 15 minutes of inactivity. $7/month to keep it running.

---

## AFFORDABLE PRODUCTION: DigitalOcean (App Platform)

**Best for**: Long-term, reliable hosting with full control

### Step 1: Create DigitalOcean Account

1. Go to https://www.digitalocean.com
2. Sign up (get $200 free credit)

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Deploy to DigitalOcean"
git push origin main
```

### Step 3: Create App on DigitalOcean

1. Login to DigitalOcean
2. Click "Apps" → "Create App"
3. Connect GitHub repo
4. Configure:
   - **Python version**: 3.10
   - **Run command**: `python app.py`
5. Click "Create App"

### Step 4: Domain & Deployment

1. Add your custom domain (optional)
2. DigitalOcean deploys automatically
3. Your app is live in ~5 minutes

**Cost**: $5-12/month depending on resources.

---

## QUICK TESTING: ngrok (Local Tunnel)

**Best for**: Quick demos, testing before deployment

### Step 1: Install ngrok

```bash
# On Linux/macOS
brew install ngrok

# On Windows
choco install ngrok
```

Or download from: https://ngrok.com/download

### Step 2: Run Your App Locally

```bash
cd /home/madhavrimal/workspace/Projects/Krishi_chakshu
python app.py
```

### Step 3: Create Public URL

In another terminal:

```bash
ngrok http 5000
```

You'll get:
```
Forwarding                    https://xxxx-xx-xxxx-xxxx-xx.ngrok.io -> http://localhost:5000
```

**Cost**: Free tier allows 2-3 hours per session.

---

## DOCKER CONTAINERIZATION (For Any Platform)

**Recommended for production** — makes deployment consistent across platforms.

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Step 2: Create .dockerignore

```
.git
.gitignore
.venv
__pycache__
uploads/*
*.pyc
.DS_Store
```

### Step 3: Build Image

```bash
docker build -t krishi-chakshu .
```

### Step 4: Test Locally

```bash
docker run -p 5000:5000 krishi-chakshu
```

### Step 5: Push to Docker Hub (Optional)

```bash
# Create account at hub.docker.com
docker tag krishi-chakshu YOUR_USERNAME/krishi-chakshu
docker push YOUR_USERNAME/krishi-chakshu
```

---

## STEP-BY-STEP: Deploy to Railway (Recommended)

### Prerequisites

```bash
# 1. Install Node.js and npm (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# 2. Install Railway CLI
npm install -g @railway/cli
```

### Full Deployment Process

```bash
# 1. Navigate to project
cd /home/madhavrimal/workspace/Projects/Krishi_chakshu

# 2. Create Procfile
cat > Procfile <<'EOF'
web: python app.py
EOF

# 3. Create runtime.txt
cat > runtime.txt <<'EOF'
python-3.10.13
EOF

# 4. Push to GitHub (if using git)
git add Procfile runtime.txt
git commit -m "Add deployment config"
git push origin main

# 5. Login to Railway
railway login

# 6. Create new Railway project
railway init

# 7. Deploy
railway up

# 8. Set production variables (optional)
railway variables set FLASK_ENV=production
railway variables set FLASK_DEBUG=0
```

After `railway up`, you'll get a live URL instantly! 🎉

---

## Environment Variables for Production

Create a `.env` file locally (don't commit):

```
FLASK_ENV=production
FLASK_DEBUG=0
MAX_UPLOAD_SIZE=16777216
MODEL_PATH=best_plant_illness_model.keras
```

For Railway/Render/others:
1. Go to dashboard
2. Add Variables section
3. Paste same variables

---

## Monitoring & Logs

### Railway
```bash
railway logs
```

### Render
```bash
# In Render dashboard → Logs tab
```

### DigitalOcean
```bash
# In App dashboard → Runtime logs
```

---

## Optimize for Deployment

### 1. Reduce Model Size (Optional)

If your model is too large for free tier:

```python
# Quantize model (in Python)
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

### 2. Use Gunicorn for Production

Instead of Flask dev server:

```bash
pip install gunicorn
```

Update `Procfile`:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 3. Add Production Config to app.py

```python
import os

if os.environ.get('FLASK_ENV') == 'production':
    app.config['JSON_SORT_KEYS'] = False
    # Add more production settings
```

---

## Troubleshooting Deployment

### Build Fails: "ModuleNotFoundError"

**Solution**: Ensure all imports in `requirements.txt`

```bash
pip freeze > requirements.txt
```

### Memory Error During Build

**Solution**: Use lightweight alternatives
- Replace `tensorflow[and-cuda]` with `tensorflow`
- Add to `Procfile`: `web: python app.py --workers=1`

### Model File Not Found

**Solution**: Ensure `best_plant_illness_model.keras` is:
1. In git (if using GitHub deployment)
2. Or uploaded directly to platform

### Port Already In Use

**Solution**: Use dynamic port

```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## Deployment Checklist

- [ ] Create `Procfile` with `web: python app.py`
- [ ] Create `runtime.txt` with Python version
- [ ] Update `requirements.txt` with all dependencies
- [ ] Test app locally: `python app.py`
- [ ] Push to GitHub
- [ ] Choose platform (Railway recommended)
- [ ] Deploy via platform CLI or dashboard
- [ ] Test live app
- [ ] Add custom domain (optional)
- [ ] Set up monitoring/alerts (optional)

---

## Recommended Path Based on Use Case

### 🌱 Learning & Testing
→ **ngrok** (free, instant) or **PythonAnywhere** (easiest)

### 🚀 First Production Deployment
→ **Railway.app** (free tier, generous limits, scalable)

### 💰 Cost-Conscious Production
→ **DigitalOcean** ($5/mo, full control)

### 📱 Large Scale
→ **AWS/Google Cloud** (pay-as-you-go, unlimited)

---

## Cost Summary (Monthly)

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Railway | $5 credit | $5-20/mo |
| Render | Limited | $7-12/mo |
| PythonAnywhere | 100MB | $5-35/mo |
| DigitalOcean | None | $5-12/mo |
| AWS | 12 months free | $10-100+/mo |

---

## Next Steps

1. **Choose a platform** from the comparison table
2. **Follow the step-by-step guide** for your chosen platform
3. **Test the live app** by uploading a plant image
4. **Share the live URL** with farmers!
5. **Monitor logs** and user feedback
6. **Iterate** based on real usage

Good luck with your deployment! 🌱🚀
