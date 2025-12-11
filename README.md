# 📔 Simple Journal PRO (Django Edition)

> A powerful, secure, and persistent journaling application built with Django.

![Journal App Preview](https://via.placeholder.com/800x400?text=Journal+App+Preview) 

---

## ✨ Features

### 🔐 Secure & Persistent
- **Google Login**: Secure authentication using your Google account.
- **Database Storage**: All entries remain safe in the database (supports SQLite, PostgreSQL clusters, etc.).
- **IP Tracking**: For security, the IP address of every entry is logged.
- **No Data Loss**: Entries are synced to the server instantly.

### ✍️ Core Experience
- **Rich Text Editor**: Bold, Italic, Headings, Fonts, Colors.
- **Translation Proxy**: Built-in backend proxy for Google Translate allowing you to translate text on the fly.
- **Dashboard**: View your past entries, dates, and writing duration.

### 💾 Export
- **One-Click Backup**: Download all your journals as a **.zip** file containing individual HTML files for each entry.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Google Cloud Project (for logical Login)
- Optional: PostgreSQL Cluster (defaults to local SQLite)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devashishhswami-ux/journal.git
   cd journal
   ```

2. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Variables**
   Rename `.env.example` to `.env` and add your keys:
   ```env
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   DATABASE_URL=postgres://... (Optional)
   ```

4. **Initialize Database**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000`

---

## 🛠️ Deployment (Clusters)

This app is "Cloud Native" ready. 
- **Database**: Connects to any PostgreSQL / MySQL cluster via `DATABASE_URL`.
- **Stateless**: Can be deployed on Render, Railway, or Heroku easily.

---

## 📂 Project Structure

```
journal/
├── journal_core/      # Settings & Config
├── journal/           # Main App Logic
│   ├── models.py      # Database Schema (Entry, User)
│   ├── views.py       # API & Export Logic
│   └── templates/     # Frontend (Modified for Django)
├── static/            # CSS/JS Assets
└── manage.py          # Entry point
```

---

Made with ❤️ by K2
