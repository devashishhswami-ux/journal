document.addEventListener('DOMContentLoaded', () => {

    const elements = {
        titleInput: document.getElementById('titleInput'),
        journalArea: document.getElementById('journalArea'),
        saveBtn: document.getElementById('saveBtn'),
        entriesList: document.getElementById('entriesList'),
        timerDisplay: document.getElementById('timerDisplay'),
        mainContent: document.querySelector('.main-content'),
        titleScreen: document.getElementById('titleScreen'),
        formattingToolbar: document.getElementById('formattingToolbar'),
        headingSelector: document.getElementById('headingSelector'),
        fontSelector: document.getElementById('fontSelector'),
        spellCheckToggle: document.getElementById('spellCheckToggle'),
        popupOverlay: document.getElementById('popupOverlay'),
        finalTimeSpan: document.getElementById('finalTime'),
        closePopupBtn: document.getElementById('closePopupBtn'),
        newEntryBtn: document.getElementById('newEntryBtn'),
        foreColorBtn: document.getElementById('foreColorBtn'),
        dateTimeDisplay: document.getElementById('dateTimeDisplay'),
        startTranslationBtn: document.getElementById('startTranslationBtn'),
        langSelector: document.getElementById('langSelector')
    };

    let state = {
        startTime: null,
        timerInterval: null,
        isTimerRunning: false
    };

    // --- Initialization ---
    updateDateTime();
    setInterval(updateDateTime, 60000); // Every minute
    loadEntries();

    function updateDateTime() {
        if (elements.dateTimeDisplay) {
            elements.dateTimeDisplay.innerText = new Date().toLocaleString('en-US', {
                weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit'
            });
        }
    }

    // --- Interaction Logic ---

    // 1. Enter Title -> Start Writing
    elements.titleInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && elements.titleInput.value.trim() !== '') {
            startWritingMode();
        }
    });

    function startWritingMode() {
        elements.titleScreen.classList.add('hidden');
        elements.mainContent.classList.add('active-mode');
        elements.journalArea.focus();
    }

    // 2. Toolbar & Formatting
    elements.formattingToolbar.addEventListener('click', (e) => {
        // Handle normal buttons
        const btn = e.target.closest('button');
        if (btn && btn.dataset.cmd) {
            document.execCommand(btn.dataset.cmd, false, null);
            elements.journalArea.focus();
        }
    });

    elements.headingSelector.addEventListener('change', () => {
        if (elements.headingSelector.value) {
            document.execCommand('formatBlock', false, elements.headingSelector.value);
            elements.journalArea.focus();
        }
    });

    elements.fontSelector.addEventListener('change', () => {
        if (elements.fontSelector.value) {
            document.execCommand('fontName', false, elements.fontSelector.value);
            elements.journalArea.focus();
        }
    });

    // Color Picker
    elements.foreColorBtn.addEventListener('input', (e) => {
        document.execCommand('foreColor', false, e.target.value);
        elements.journalArea.focus();
    });

    // Translator
    elements.startTranslationBtn.addEventListener('click', async () => {
        const selection = window.getSelection();
        const selectedText = selection.toString();

        if (!selectedText.trim()) {
            showToast("⚠️ Select text to translate first", 2000);
            return;
        }

        // Save selection range
        let range = null;
        if (selection.rangeCount > 0) {
            range = selection.getRangeAt(0);
        }

        const targetLang = elements.langSelector.value;

        // Visual Feedback
        const btnIcon = elements.startTranslationBtn.firstElementChild;
        const originalIcon = btnIcon.name;
        btnIcon.name = 'hourglass-outline';
        elements.startTranslationBtn.classList.add('loading-pulse');

        try {
            // 1. Try Local Proxy (Works if server.py is running)
            const response = await fetch(`/api/translate?text=${encodeURIComponent(selectedText)}&target=${targetLang}`);

            if (response.ok) {
                const data = await response.json();
                if (data && data.translatedText) {
                    // Restore selection
                    elements.journalArea.focus();
                    selection.removeAllRanges();
                    if (range) selection.addRange(range);
                    document.execCommand('insertText', false, data.translatedText);
                    showToast("✅ Translated successfully!", 2000);
                    return; // Success!
                }
            }
            throw new Error("Proxy failed"); // Trigger fallback

        } catch (err) {
            console.log("Proxy unreachable, trying fallback...", err);

            // 2. Fallback: Open Google Translate (For GitHub Pages / Static Hosting)
            const url = `https://translate.google.com/?sl=auto&tl=${targetLang}&text=${encodeURIComponent(selectedText)}&op=translate`;
            window.open(url, '_blank');
            showToast("↗️ Opened in Google Translate (Static Mode)", 3000);

        } finally {
            btnIcon.name = originalIcon;
            elements.startTranslationBtn.classList.remove('loading-pulse');
        }
    });

    // Export Logic
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            const entries = localStorage.getItem('simple_journal_entries');
            if (!entries || entries === '[]') {
                alert("Nothing to export yet!");
                return;
            }
            const blob = new Blob([entries], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `journal_backup_${new Date().toISOString().slice(0, 10)}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast("💾 Backup downloaded!", 2000);
        });
    }

    function showToast(msg, duration) {
        // Create or reuse toast element
        let toast = document.getElementById('toastNotification');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toastNotification';
            toast.style.cssText = `
                position: fixed; bottom: 20px; right: 20px;
                background: #333; color: white; padding: 10px 20px;
                border-radius: 5px; z-index: 1000; font-size: 0.9em;
                opacity: 0; transition: opacity 0.3s; pointer-events: none;
            `;
            document.body.appendChild(toast);
        }
        toast.innerText = msg;
        toast.style.opacity = '1';
        setTimeout(() => {
            toast.style.opacity = '0';
        }, duration);
    }

    // Spell Check
    elements.spellCheckToggle.addEventListener('change', (e) => {
        elements.journalArea.setAttribute('spellcheck', e.target.checked);
    });

    // 3. Timer
    elements.journalArea.addEventListener('input', () => {
        if (!state.isTimerRunning) {
            state.startTime = new Date();
            state.isTimerRunning = true;
            state.timerInterval = setInterval(updateTimer, 1000);
        }
    });

    function updateTimer() {
        if (!state.startTime) return;
        const diff = new Date() - state.startTime; // ms
        const date = new Date(diff);
        const h = String(date.getUTCHours()).padStart(2, '0');
        const m = String(date.getUTCMinutes()).padStart(2, '0');
        const s = String(date.getUTCSeconds()).padStart(2, '0');
        elements.timerDisplay.innerText = `${h}:${m}:${s}`;
    }

    // 4. Save & Load
    elements.saveBtn.addEventListener('click', saveEntry);

    function saveEntry() {
        if (!elements.journalArea.innerText.trim()) {
            alert("Empty journal? Write something!");
            return;
        }

        clearInterval(state.timerInterval);
        state.isTimerRunning = false;

        const now = new Date();
        const diff = state.startTime ? (now - state.startTime) : 0;

        // Calculate duration string
        // Simple approximation
        const secs = Math.floor(diff / 1000);
        const mins = Math.floor(secs / 60);
        const hrs = Math.floor(mins / 60);

        let durationStr = "";
        if (hrs > 0) durationStr += `${hrs}h `;
        if (mins > 0) durationStr += `${mins % 60}m `;
        durationStr += `${secs % 60}s`;
        if (!durationStr) durationStr = "0s";

        const newEntry = {
            id: Date.now(),
            title: elements.titleInput.value || 'Untitled',
            content: elements.journalArea.innerHTML,
            date: now,
            durationStr: durationStr
        };

        const entries = JSON.parse(localStorage.getItem('simple_journal_entries') || '[]');
        entries.unshift(newEntry);
        localStorage.setItem('simple_journal_entries', JSON.stringify(entries));

        showPopup(durationStr);
        loadEntries();
    }

    function loadEntries() {
        const entries = JSON.parse(localStorage.getItem('simple_journal_entries') || '[]');
        elements.entriesList.innerHTML = '';

        if (entries.length === 0) {
            elements.entriesList.innerHTML = '<p class="empty-state">No entries yet.</p>';
            return;
        }

        entries.forEach(entry => {
            const card = document.createElement('div');
            card.className = 'entry-card';
            card.onclick = () => window.open(`view.html?id=${entry.id}`, '_blank');

            // Plain text preview
            const tmp = document.createElement('div');
            tmp.innerHTML = entry.content;
            const preview = (tmp.textContent || tmp.innerText || "").substring(0, 80);

            card.innerHTML = `
                <div class="entry-header">
                    <span>${new Date(entry.date).toLocaleDateString()}</span>
                    <span>${entry.durationStr}</span>
                </div>
                <span class="entry-title">${entry.title}</span>
                <div class="entry-snippet">${preview}...</div>
            `;
            elements.entriesList.appendChild(card);
        });
    }

    // 5. Popup & Reset
    function showPopup(time) {
        elements.finalTimeSpan.innerText = time;
        elements.popupOverlay.classList.remove('hidden');
    }

    elements.closePopupBtn.addEventListener('click', () => {
        elements.popupOverlay.classList.add('hidden');
        resetEditor(); // Optional: reset for new entry immediately?
    });

    elements.newEntryBtn.addEventListener('click', resetEditor);

    function resetEditor() {
        // Reset to title screen
        elements.titleScreen.classList.remove('hidden');
        elements.mainContent.classList.remove('active-mode');
        elements.titleInput.value = '';
        elements.journalArea.innerHTML = '';
        elements.timerDisplay.innerText = "00:00:00";
        elements.popupOverlay.classList.add('hidden');

        state.startTime = null;
        clearInterval(state.timerInterval);
        state.isTimerRunning = false;

        elements.titleInput.focus();
    }

});
