#!/bin/bash
# Script to add Google OAuth credentials to .env file

ENV_FILE="/home/coder1/pythonbot/journal-app/.env"

# Google OAuth Credentials - GET THESE FROM GOOGLE CLOUD CONSOLE
# Instructions:
# 1. Go to https://console.cloud.google.com/
# 2. Navigate to APIs & Services > Credentials
# 3. Copy your OAuth 2.0 Client ID and Client Secret
# 4. Replace the placeholders below with your actual values

GOOGLE_CLIENT_ID="YOUR-CLIENT-ID.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="YOUR-CLIENT-SECRET"

echo "🔧 Adding Google OAuth credentials to .env file..."

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Check if credentials already exist
if grep -q "GOOGLE_CLIENT_ID=" "$ENV_FILE"; then
    echo "⚠️  Google credentials already exist in .env file. Updating..."
    # Update existing values
    sed -i "s|^GOOGLE_CLIENT_ID=.*|GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID|" "$ENV_FILE"
    sed -i "s|^GOOGLE_CLIENT_SECRET=.*|GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET|" "$ENV_FILE"
else
    echo "✅ Adding new Google credentials to .env file..."
    # Add credentials to end of file
    cat >> "$ENV_FILE" << EOL

# ============================================
# Google OAuth Configuration
# ============================================
GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET
EOL
fi

echo "✅ Google OAuth credentials added successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure redirect URIs in Google Cloud Console:"
echo "   - Local: http://localhost:8000/accounts/google/login/callback/"
echo "   - Production: https://your-app.onrender.com/accounts/google/login/callback/"
echo ""
echo "2. Start the development server:"
echo "   cd /home/coder1/pythonbot/journal-app"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "3. Test Google Sign-In at: http://localhost:8000/accounts/login/"
