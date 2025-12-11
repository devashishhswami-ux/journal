# Simple Journal Web App
A beautiful, distraction-free journal app with rich text, translation, and local persistence.

## 🚀 How to Deploy to GitHub Pages (24/7 Hosting)

> **Note:** Data is saved to your browser's local storage. To prevent data loss, use the **Export Backup** button in the sidebar regularly.

### Step 1: Initialize Git
Open your terminal in the project folder and run:
```bash
git init
git add .
git commit -m "Initial commit of Journal App"
```

### Step 2: Push to GitHub
1. Create a **New Repository** on GitHub (name it `my-journal` or similar).
2. **Copy the commands** GitHub gives you to "push an existing repository". They look like this:
```bash
git remote add origin https://github.com/YOUR_USERNAME/my-journal.git
git branch -M main
git push -u origin main
```
3. Run those commands in your terminal.

### Step 3: Enable GitHub Pages
1. Go to your Repository **Settings** > **Pages** (on the left sidebar).
2. Under **Source**, select `Deploy from a branch`.
3. Select `main` branch and `/ (root)` folder.
4. Click **Save**.

Wait 1-2 minutes, and your site will be live at `https://YOUR_USERNAME.github.io/my-journal/`!

---

## 🌍 Translation Feature Note
*   **Local Mode:** If you run the app locally with `python3 server.py`, you get **instant in-page translation**.
*   **GitHub Pages (Static) Mode:** Since GitHub Pages doesn't run Python backends, the requested translation will automatically **open in Google Translate** in a new tab. This ensures it still works reliably 24/7 without needing a paid server.

## 💾 Saving Your Journals
*   Your journals live in `localStorage`.
*   Click **⬇ Export Backup** in the sidebar to download a `.json` file of all your entries.
*   Keep this file safe!

## 🛠 Features
*   Distraction-free writing.
*   Rich text toolbar (Bold, Italic, Headings, Lists).
*   Google Fonts integration.
*   Auto-save to browser.
*   Dark/Light mode ready (CSS variables).
