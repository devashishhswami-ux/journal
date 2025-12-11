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
        aiGrammarBtn: document.getElementById('aiGrammarBtn'),
        langSelector: document.getElementById('langSelector')
    };

    // If we are on login screen, some elements might be missing
    if (!elements.journalArea) return;

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    let state = {
        startTime: null,
        timerInterval: null,
        isTimerRunning: false,
        currentEntryId: null
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

        const targetLang = elements.langSelector.value;

        // Visual Feedback
        const btnIcon = elements.startTranslationBtn.firstElementChild;
        const originalIcon = btnIcon.name;
        btnIcon.name = 'hourglass-outline';
        elements.startTranslationBtn.classList.add('loading-pulse');

        try {
            // Updated to Django API
            const response = await fetch(`/api/translate?text=${encodeURIComponent(selectedText)}&target=${targetLang}`);

            if (response.ok) {
                const data = await response.json();
                if (data && data.translatedText) {
                    elements.journalArea.focus();
                    document.execCommand('insertText', false, data.translatedText);
                    showToast("✅ Translated successfully!", 2000);
                    return;
                }
            }
            throw new Error("Proxy failed");

        } catch (err) {
            console.log("Proxy unreachable", err);
            showToast("⚠️ Translation failed", 3000);
        } finally {
            btnIcon.name = originalIcon;
            elements.startTranslationBtn.classList.remove('loading-pulse');
        }
    });

    // AI Grammar Check
    if (elements.aiGrammarBtn) {
        elements.aiGrammarBtn.addEventListener('click', async () => {
            let textToCheck = "";
            const selection = window.getSelection();
            const selectedText = selection.toString();

            const isSelection = !!selectedText.trim();
            textToCheck = isSelection ? selectedText : elements.journalArea.innerText;

            if (!textToCheck.trim()) {
                showToast("⚠️ Nothing to check!", 2000);
                return;
            }

            const btnIcon = elements.aiGrammarBtn.firstElementChild;
            const originalIcon = btnIcon.name;
            btnIcon.name = 'sync-outline';
            elements.aiGrammarBtn.classList.add('loading-pulse');

            try {
                const res = await fetch('/api/ai/grammar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ text: textToCheck })
                });

                if (res.ok) {
                    const data = await res.json();
                    if (data.corrected) {
                        elements.journalArea.focus();
                        if (isSelection) {
                            document.execCommand('insertText', false, data.corrected);
                        } else {
                            if (confirm("AI Suggestion:\n\n" + data.corrected + "\n\nApply changes?")) {
                                elements.journalArea.innerText = data.corrected;
                            }
                        }
                        showToast("✨ Grammar Check Complete!", 3000);
                    } else {
                        showToast("✅ No issues found.", 2000);
                    }
                } else {
                    throw new Error("AI Error");
                }
            } catch (e) {
                console.error(e);
                showToast("❌ AI Busy or Error", 3000);
            } finally {
                btnIcon.name = originalIcon;
                elements.aiGrammarBtn.classList.remove('loading-pulse');
            }
        });
    }


    function showToast(msg, duration) {
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

    async function saveEntry() {
        if (!elements.journalArea.innerText.trim()) {
            alert("Empty journal? Write something!");
            return;
        }

        clearInterval(state.timerInterval);
        state.isTimerRunning = false;

        const now = new Date();
        const diff = state.startTime ? (now - state.startTime) : 0;
        const secs = Math.floor(diff / 1000);
        const mins = Math.floor(secs / 60);
        const hrs = Math.floor(mins / 60);

        let durationStr = "";
        if (hrs > 0) durationStr += `${hrs}h `;
        if (mins > 0) durationStr += `${mins % 60}m `;
        durationStr += `${secs % 60}s`;
        if (!durationStr) durationStr = "0s";

        const newEntry = {
            id: state.currentEntryId,
            title: elements.titleInput.value || 'Untitled',
            content: elements.journalArea.innerHTML,
            durationStr: durationStr
        };

        try {
            const res = await fetch('/api/entries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(newEntry)
            });

            if (res.ok) {
                const data = await res.json();
                state.currentEntryId = data.id; // Update ID to prevent duplicates
                showPopup(durationStr);
                loadEntries();
            } else {
                throw new Error('Save failed');
            }
        } catch (e) {
            showToast("❌ Error saving.", 3000);
            console.error(e);
        }
    }

    async function loadEntries() {
        elements.entriesList.innerHTML = '<p class="empty-state">Loading...</p>';
        try {
            const res = await fetch('/api/entries');
            if (res.ok) {
                const entries = await res.json();
                renderEntries(entries);
            }
        } catch (e) {
            elements.entriesList.innerHTML = '<p class="empty-state">Error loading entries.</p>';
        }
    }

    function renderEntries(entries) {
        elements.entriesList.innerHTML = '';

        if (entries.length === 0) {
            elements.entriesList.innerHTML = '<p class="empty-state">No entries yet.</p>';
            return;
        }

        entries.forEach(entry => {
            const card = document.createElement('div');
            card.className = 'entry-card';
            // View logic moved to server/zip, but for now we technically don't have a view page
            // We could make it reopen in editor?
            // For now, let's just preview.
            // Better behavior: Click to load into editor? Or keep view.html?
            // User asked for "Repoens his journal he doesnt loose any data".
            // Let's make clicking it READ-ONLY, or LOAD it back.
            // Let's do simple alert for now or nothing as we removed view.html
            // Wait, we should probably implement a View mode.
            card.onclick = () => {
                // Populate editor
                state.currentEntryId = entry.id;
                elements.titleInput.value = entry.title;
                elements.journalArea.innerHTML = entry.content;
                startWritingMode();
            };

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
        resetEditor();
    });

    elements.newEntryBtn.addEventListener('click', resetEditor);

    function resetEditor() {
        elements.titleScreen.classList.remove('hidden');
        elements.mainContent.classList.remove('active-mode');
        elements.titleInput.value = '';
        elements.journalArea.innerHTML = '';
        elements.timerDisplay.innerText = "00:00:00";
        elements.popupOverlay.classList.add('hidden');

        state.startTime = null;
        state.currentEntryId = null;
        clearInterval(state.timerInterval);
        state.isTimerRunning = false;
        elements.titleInput.focus();
    }

});
