# Google OAuth Setup Guide for Journal App

This guide will walk you through everything you need to add Google Sign-In to your journal application.

## 📋 What You Provided

- ✅ **Google Client Secret**: `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`

## ❗ What You Still Need

### 1. Google Client ID

You need to provide your **Google OAuth Client ID**. It looks like this:
```
123456789-abc123xyz456.apps.googleusercontent.com
```

**Where to find it:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID (the same one where you got the Client Secret)
5. Copy the **Client ID** value

---

## 🔧 Complete Setup Steps

### Step 1: Configure Google Cloud Console

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select or Create a Project**
3. **Enable Google+ API**:
   - Go to **APIs & Services** → **Library**
   - Search for "Google+ API"
   - Click **Enable**

4. **Configure OAuth Consent Screen**:
   - Go to **APIs & Services** → **OAuth consent screen**
   - Choose **External** user type (unless you have a Google Workspace)
   - Fill in required fields:
     - App name: `Journal Pro` (or your preferred name)
     - User support email: Your email
     - Developer contact email: Your email
   - Add scopes: `email`, `profile`, `openid` (should be default)
   - Add test users if in development mode
   - Save and continue

5. **Configure Redirect URIs** (CRITICAL):
   - Go to **APIs & Services** → **Credentials**
   - Click on your OAuth 2.0 Client ID
   - Under **Authorized redirect URIs**, add:
   
   **For Local Development:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   
   **For Production (Render):**
   ```
   https://your-app-name.onrender.com/accounts/google/login/callback/
   ```
   *(Replace `your-app-name` with your actual Render app URL)*
   
   - Click **Save**

---

### Step 2: Update Environment Variables

Add these to your `.env` file:

```bash
# ============================================
# Google OAuth Configuration
# ============================================
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```

**For Production (Render):**
- Add the same variables in your Render dashboard under **Environment Variables**
- Or update your `render.yaml` to include them

---

### Step 3: Files That Will Be Modified

The following files will be automatically updated:

1. **`journal_core/settings.py`**
   - Add Google provider to installed apps
   - Configure social account settings
   - Add Google OAuth credentials from environment

2. **`.env.example`**
   - Add Google OAuth variables as template

3. **`journal/templates/account/login.html`**
   - Add "Sign in with Google" button
   - Add Google branding

4. **`journal/templates/account/signup.html`**
   - Add "Sign up with Google" button
   - Quick registration option

---

### Step 4: Run Migrations

After configuration, run:

```bash
cd /home/coder1/pythonbot/journal-app
python manage.py migrate
```

This creates necessary database tables for social authentication.

---

### Step 5: Configure Site Domain (Django Sites Framework)

Django Allauth uses Django's Sites framework. You need to set the correct domain:

**For Local Development:**
```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.sites.models import Site
site = Site.objects.get_current()
site.domain = 'localhost:8000'
site.name = 'Journal Pro (Local)'
site.save()
exit()
```

**For Production (via Django Admin):**
1. Go to `https://your-app.onrender.com/admin/`
2. Navigate to **Sites**
3. Click on the site (usually "example.com" by default)
4. Change:
   - Domain name: `your-app-name.onrender.com`
   - Display name: `Journal Pro`
5. Save

---

## 🎨 What Users Will See

### Login Page
- Traditional email/password form (existing)
- **OR** divider
- "Sign in with Google" button with Google branding
- Clicking Google button → redirects to Google OAuth → returns to app

### Signup Page  
- "Quick Sign Up with Google" button (prominent)
- **OR** divider
- Traditional email/password registration (existing)

### After Google Sign-In
- New users: Account created automatically with Google email
- Existing users: If email matches, accounts are linked
- All users: Redirected to journal homepage (`/`)

---

## 🧪 Testing Checklist

After implementation, test these scenarios:

- [ ] Click "Sign in with Google" on login page
- [ ] Complete Google OAuth flow
- [ ] Verify redirect back to journal homepage
- [ ] Check user profile in Django admin shows Google link
- [ ] Sign out and sign in again with Google (should work instantly)
- [ ] Try with different Google account (creates new user)
- [ ] Try with same Google account twice (doesn't duplicate)
- [ ] Test on mobile device
- [ ] Test the signup page Google button

---

## 🚨 Common Issues & Solutions

### Issue: "Redirect URI mismatch"
**Solution**: Make sure EXACT redirect URIs are added in Google Cloud Console:
- `http://localhost:8000/accounts/google/login/callback/` (local)
- `https://your-app.onrender.com/accounts/google/login/callback/` (production)

### Issue: "Error 400: redirect_uri_mismatch"
**Solution**: Check your Site domain in Django admin matches your actual domain.

### Issue: "The app is in test mode"
**Solution**: In Google Cloud Console, publish your app (OAuth consent screen → Publish App) OR add test users who can access during development.

### Issue: User gets redirected to wrong domain
**Solution**: Update Site domain in Django admin to match your actual domain (don't include `http://` or `https://`).

### Issue: "Social account not found"
**Solution**: Make sure migrations have been run: `python manage.py migrate`

---

## 📱 Mobile Considerations

The Google Sign-In button will be fully responsive and work on mobile devices. The OAuth flow will:
1. Open Google's mobile-optimized sign-in page
2. Support Google account quick-pick if signed in
3. Redirect cleanly back to your app

---

## 🔒 Security Notes

- ✅ Client Secret is kept in `.env` (gitignored - never committed)
- ✅ HTTPS enforced in production (Render handles this)
- ✅ OAuth tokens stored securely in database
- ✅ User emails verified by Google (trusted source)
- ✅ No passwords to manage for Google sign-in users

---

## 📝 Summary

**You need to provide:**
1. ✅ Google Client Secret (you provided this)
2. ❌ **Google Client ID** (please provide this)

**What needs to be configured in Google Cloud:**
1. OAuth consent screen
2. Redirect URIs for your domains
3. Enable Google+ API (or Google Identity)

**What will be automated:**
1. Code changes to Django settings
2. Template updates for login/signup pages
3. Database migrations

Once you provide the Client ID, I can proceed with the implementation! 🚀
