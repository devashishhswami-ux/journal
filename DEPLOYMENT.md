# Journal Pro - Render Deployment Guide

## Quick Deploy to Render (24/7)

This guide will help you deploy Journal Pro to Render for 24/7 availability with Neon PostgreSQL.

## Prerequisites

✅ GitHub account
✅ Render account (render.com)
✅ Neon database (optional - Render can provision PostgreSQL)

---

##  Step 1: Push to GitHub

```bash
cd /home/coder1/pythonbot/journal-app

# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Render deployment with enhanced admin"

# Push to GitHub (replace with your repo URL)
git remote add origin https://github.com/yourusername/journal-pro.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Render will detect `render.yaml` automatically**
5. **Click "Apply"** - Render will provision:
   - Web service (journal-pro)
   - PostgreSQL database (journal-db)
   - Auto-configure DATABASE_URL

### Option B: Manual Setup

1. **Create PostgreSQL Database**:
   - Dashboard → "New +" → "PostgreSQL"
   - Name: `journal-db`
   - Plan: Free (or paid for guaranteed uptime)
   - Note the connection string

2. **Create Web Service**:
   - Dashboard → "New +" → "Web Service"
   - Connect GitHub repo
   - **Settings**:
     - Name: `journal-pro`
     - Runtime: Python 3
     - Build Command: `chmod +x build.sh && ./build.sh`
     - Start Command: `gunicorn journal_core.wsgi:application`
     - Plan: Free (starts/stops) or Starter ($7/mo for 24/7)

3. **Environment Variables**:
   - `SECRET_KEY` → Generate random string (50+ chars)
   - `DEBUG` → `False`
   - `DATABASE_URL` → Copy from PostgreSQL database
   - `PYTHONUNBUFFERED` → `1`
   - `WEB_CONCURRENCY` → `4`

---

## Step 3: Using Neon Database (Alternative)

If you prefer Neon PostgreSQL:

1. **Get Neon Connection String**:
   - Go to https://neon.tech
   - Create project
   - Copy connection string (looks like: `postgresql://user:pass@host/db?sslmode=require`)

2. **Set in Render**:
   - Go to your web service
   - Environment → Add `DATABASE_URL` with Neon connection string

---

## ⚙️ Step 4: Post-Deployment

Once deployed, run migrations and create superuser:

### Via Render Shell

1. Go to your web service in Render
2. Click "Shell" tab
3. Run:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Create Admin User

```bash
Username: admin
Email: admin@journalpro.com
Password: [choose secure password]
```

---

## 🎯 Step 5: Verify Deployment

### Test These URLs

- **Homepage**: `https://journal-pro.onrender.com/`
- **Login**: `https://journal-pro.onrender.com/accounts/login/`
- **Signup**: `https://journal-pro.onrender.com/accounts/signup/`
- **Admin**: `https://journal-pro.onrender.com/admin/`

### Test Admin Features

1. Login to admin with superuser credentials
2. Verify you can see:
   - **Users list** with entry counts
   - **Journal entries** with IP addresses  
   - Click on a user → see their journals inline
   - Entry details with word count and preview

---

## 🔧 Configuration

### Environment Variables (.env for local)

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True  # False in production
DATABASE_URL=postgresql://...  # For Neon/Render DB
ALLOWED_HOSTS=localhost,journal-pro.onrender.com
```

### Static Files

- Collected automatically during build
- Served by WhiteNoise in production
- No CDN needed for small/medium apps

---

## 🚀 24/7 Uptime

### Free Plan
- Auto-sleeps after 15 min inactivity
- Wakes on first request (slow)
- Good for testing

### Starter Plan ($7/month)
- **24/7 availability**
- No sleep/wake delays
- Recommended for production

To upgrade:
1. Web Service → Settings → Instance Type
2. Change to "Starter" or higher

---

## 🐛 Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError`
- **Fix**: Check `requirements.txt` has all dependencies

**Error**: `Permission denied: build.sh`
- **Fix**: Ensure `chmod +x build.sh` in build command

### Runtime Errors

**Error**: `DisallowedHost`
- **Fix**: Add your Render URL to `ALLOWED_HOSTS` in settings.py

**Error**: `STATIC_ROOT not found`
- **Fix**: Run `python manage.py collectstatic` manually via shell

### Database Issues

**Error**: `database "journal_db" does not exist`
- **Fix**: Ensure DATABASE_URL is set correctly
- **Fix**: Run `python manage.py migrate` via Render shell

---

## 📊 Monitoring

### Logs
- Go to your web service
- Click "Logs" tab
- View real-time application logs

### Database
- PostgreSQL dashboard shows:
  - Connection count
  - Database size
  - Query performance

---

## 🔐 Security Checklist

✅ `DEBUG = False` in production
✅ Strong `SECRET_KEY` (generated)
✅ HTTPS enabled (Render default)
✅ Database password secure
✅ Admin password strong

---

## 🎉 You're Live!

Your Journal Pro app is now:
- ✅ Deployed on Render
- ✅ Using PostgreSQL (Neon or Render)
- ✅ Serving static files
- ✅ Running migrations
- ✅ Ready for users!

Share your URL: `https://journal-pro.onrender.com`

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.1/howto/deployment/
- **Neon Docs**: https://neon.tech/docs

Enjoy your 24/7 journal app! 🚀
