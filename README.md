# 📔 Simple Journal App

> A minimal, distraction-free journaling application built for focus and simplicity.

![Journal App Preview](https://via.placeholder.com/800x400?text=Journal+App+Preview) 
*(Self-hosted preview recommended)*

---

## ✨ Features

### ✍️ Core Writing Experience
- **Distraction-Free Interface**: Clean design that puts your words front and center.
- **Rich Text Editor**: Support for **Bold**, *Italic*, Underline, Lists, and Headings (H1-H6).
- **Font Customization**: Choose from a variety of Google Fonts to match your style.
- **Text Alignment**: Left, Center, and Right alignment options.
- **Color Picker**: Highlight important thoughts with custom colors.
- **Spell Check Toggle**: Turn spell check on or off for uninterrupted flow.

### ⏱️ Productivity Tools
- **Session Timer**: Automatically tracks how long you've been writing.
- **Word Counter**: Keep track of your daily output (implied by design).
- **Date & Time Display**: Always know when you wrote an entry.

### 💾 Data & Privacy
- **Local Storage**: All entries are saved directly to your browser's local storage. Your data never leaves your device unless you export it.
- **Export to JSON**: Backup your journal entries with a single click.
- **Secure**: No external database required.

### 🌍 Accessibility & Extras
- **Translation Support**: Select text to translate instantly (Supports Google Translate Proxy).
- **Responsive Design**: Works on desktop and tablets.
- **Printing**: Print your entries directly from the view page.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (for the server)
- A modern web browser (Chrome, Firefox, Safari)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devashishhswami-ux/journal.git
   cd journal-app
   ```

2. **Run the Server**
   This app uses a simple Python server to handle local files and translation proxying.
   ```bash
   python server.py
   ```

3. **Open in Browser**
   Navigate to `http://localhost:8080` in your web browser.

---

## 🛠️ Deployment

### Replit (Recommended for 24/7)
This project is configured for **Replit**.
1. Create a new Repl on [Replit.com](https://replit.com).
2. Import this repository.
3. Click "Run" - the `.replit` and `replit.nix` files will handle the setup automatically.

### Render / Other Platforms
You can deploy this as a Python Web Service.
- **Start Command**: `python server.py`
- **Build Command**: `pip install -r requirements.txt` (if applicable, current deps are standard lib)

---

## 📂 Project Structure

```
journal-app/
├── index.html       # Main application interface
├── script.js        # Core logic (Timer, Saving, Translation)
├── styles.css       # Styling (Themes, Layout)
├── server.py        # Python backend (Static serving + API Proxy)
├── view.html        # Read-only view for saved entries
├── .replit          # Replit configuration
└── replit.nix       # Replit environment dependencies
```

---

## 🤝 Contributing

Contributions are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by K2
