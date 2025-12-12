# Email Setup Guide for Password Reset

This guide explains how to configure email for password reset functionality in your Journal Pro app.

## Development vs Production

### Development (Local)
- **Default**: Emails print to console (terminal)
- **No configuration needed** - works out of the box
- Check your terminal/console to see password reset emails

### Production (Render/Live)
- **Required**: Gmail SMTP or another email service
- Sends real emails to users
- Requires environment variables to be set

---

## Gmail SMTP Setup (Recommended for Production)

### Step 1: Enable 2-Step Verification
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Find "2-Step Verification" and enable it
3. Follow the setup wizard

### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. You might need to re-authenticate
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Name it: "Journal App" or "Journal Pro"
6. Click **Generate**
7. **Copy the 16-character password** (shown with spaces like: `xxxx xxxx xxxx xxxx`)
8. Remove spaces when pasting: `xxxxxxxxxxxxxxxx`

### Step 3: Configure Environment Variables

#### For Local Development (.env file):
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop  # 16-char app password (no spaces)
DEFAULT_FROM_EMAIL=Journal Pro <youremail@gmail.com>
```

#### For Render (Environment Variables):
Add these in your Render dashboard under "Environment":
- `EMAIL_BACKEND` = `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST_USER` = `youremail@gmail.com`
- `EMAIL_HOST_PASSWORD` = `your-16-char-app-password`
- `DEFAULT_FROM_EMAIL` = `Journal Pro <youremail@gmail.com>`

---

## Testing Password Reset

### Local Testing:
1. Start your development server
2. Go to login page
3. Click "Forgot Password?"
4. Enter your email
5. Check your **terminal/console** for the reset link
6. Copy the link and paste in browser

### Production Testing:
1. Deploy to Render with email variables set
2. Go to your live site
3. Click "Forgot Password?"
4. Enter your email
5. Check your **inbox** for the reset email
6. Click the link in the email

---

## Troubleshooting

### Email Not Sending in Production?
1. **Check Environment Variables**: Verify all email settings in Render dashboard
2. **Verify App Password**: Make sure it's the 16-char app password, not regular password
3. **Check Logs**: Look at Render logs for email errors
4. **Gmail Less Secure Apps**: Not needed if using App Password

### Email Goes to Spam?
- This is normal for Gmail SMTP initially
- Mark as "Not Spam" to train Gmail
- Consider using a dedicated email service like SendGrid or Mailgun for production

### "Authentication Failed" Error?
- Double-check the app password (no spaces)
- Ensure 2-Step Verification is enabled
- Try generating a new app password

### Still Not Working?
- Check Django logs for specific error messages
- Verify EMAIL_USE_TLS is set to True
- Ensure EMAIL_PORT is 587 (not 465 or 25)

---

## Alternative Email Services

If you prefer not to use Gmail, here are alternatives:

### SendGrid (Free tier: 100 emails/day)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### Mailgun
```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=postmaster@your-domain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-smtp-password
```

---

## Security Notes

⚠️ **NEVER commit your .env file to Git!**
- It's already in .gitignore
- Only share App Passwords through secure channels
- Regenerate App Password immediately if compromised
- Use different app passwords for different applications

✅ **Best Practices:**
- Use App-Specific Passwords (not your main password)
- Keep EMAIL_HOST_PASSWORD in environment variables only
- Don't hardcode credentials in code
- Rotate passwords periodically
