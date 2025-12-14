# 🚨 URGENT FIX FOR EMAIL ERROR

## Problem Found!

Your Gmail App Password has **SPACES** in it:
```
EMAIL_HOST_PASSWORD="vzwt jyko xqme koej"  ❌ WRONG
```

Gmail app passwords are 16 characters with **NO SPACES**!

---

## ✅ IMMEDIATE FIX

### Go to Render Dashboard → Environment Variables

**Change this:**
```
EMAIL_HOST_PASSWORD = vzwt jyko xqme koej
```

**To this (remove ALL spaces):**
```
EMAIL_HOST_PASSWORD = vzwtjykoxqmekoej
```

That's it! Just remove the spaces.

---

## Quick Steps:

1. Go to: https://dashboard.render.com
2. Click your journal-pro service
3. Go to **Environment** tab
4. Find `EMAIL_HOST_PASSWORD`
5. Click **Edit**
6. Remove ALL spaces: `vzwtjykoxqmekoej`
7. Click **Save**
8. Wait 2-3 minutes for auto-deploy

---

## Alternative: Use Console Backend (For Testing)

If you want password reset to work RIGHT NOW without fixing email:

**Delete these from Render Environment:**
- `EMAIL_BACKEND`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_HOST_USER` 

Then it will use console backend (reset links in logs).

---

## After Fix:

Password reset will send REAL emails to users! ✉️
