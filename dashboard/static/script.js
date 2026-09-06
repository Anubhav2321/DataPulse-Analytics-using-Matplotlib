/* ═══════════════════════════════════════════════════════════════
   DATAPULSE — CORE APPLICATION LOGIC
   Navigation, Theme Engine, Settings, Counter Animations
   ═══════════════════════════════════════════════════════════════ */

// ── GLOBALS ──
let currentAIMode = localStorage.getItem('datapulse_ai_mode') || 'local';

// ═══════════════════════════════════════════════════════════════
// 1. VIEW NAVIGATION
// ═══════════════════════════════════════════════════════════════

const VIEW_TITLES = {
    overview: 'System Overview',
    whatif: 'What-If Scenario Simulator',
    anomaly: 'Anomaly Detection',
    correlation: 'Correlation Heatmap',
    askdata: 'Natural Language Query',
    aiinsights: 'AI Insights Engine',
    settings: 'Settings & Configuration',
};

function showView(viewName, clickedLink) {
    // Hide all view panels
    document.querySelectorAll('.view-panel').forEach(p => {
        p.classList.remove('active');
    });

    // Show target view
    const target = document.getElementById('view-' + viewName);
    if (target) {
        target.classList.add('active');
        // Re-trigger animation
        target.style.animation = 'none';
        target.offsetHeight; // force reflow
        target.style.animation = '';
    }

    // Update page title
    const title = VIEW_TITLES[viewName] || 'Dashboard';
    document.getElementById('page-title').innerHTML = `${title} <span class="file-badge"><i class="fa-solid fa-file-csv"></i> ${BACKEND_DATA.fileName}</span>`;

    // Update sidebar active state
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    if (clickedLink) {
        clickedLink.classList.add('active');
    }

    // Lazy-render charts on first visit
    if (viewName === 'anomaly' && !window._anomalyRendered) {
        renderAnomalyView();
        window._anomalyRendered = true;
    }
    if (viewName === 'correlation' && !window._corrRendered) {
        renderCorrelationView();
        window._corrRendered = true;
    }
}

// ═══════════════════════════════════════════════════════════════
// 2. SIDEBAR DROPDOWN
// ═══════════════════════════════════════════════════════════════

function toggleMenu(e) {
    e.preventDefault();
    const menu = document.getElementById('advanced-menu');
    const arrow = document.getElementById('arrow-icon');
    menu.classList.toggle('menu-open');
    arrow.classList.toggle('rotate-arrow');
}


// ═══════════════════════════════════════════════════════════════
// 3. COUNTER ANIMATION
// ═══════════════════════════════════════════════════════════════

function animateCounters() {
    document.querySelectorAll('.counter').forEach(counter => {
        const target = +counter.getAttribute('data-target');
        if (isNaN(target)) return;
        counter.innerText = '0';
        const duration = 800;
        const steps = 30;
        const increment = target / steps;
        let current = 0;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.innerText = target.toLocaleString();
                clearInterval(timer);
            } else {
                counter.innerText = Math.ceil(current).toLocaleString();
            }
        }, duration / steps);
    });
}


// ═══════════════════════════════════════════════════════════════
// 4. KPI METRICS DISPLAY
// ═══════════════════════════════════════════════════════════════

function displayKPIMetrics() {
    const m = BACKEND_DATA.kpiMetrics;
    if (!m) return;

    const sumEl = document.getElementById('kpi-sum-value');
    const avgEl = document.getElementById('kpi-avg-value');
    if (sumEl) sumEl.textContent = Number(m.total).toLocaleString(undefined, {maximumFractionDigits: 2});
    if (avgEl) avgEl.textContent = Number(m.mean).toLocaleString(undefined, {maximumFractionDigits: 2});

    // Apply threshold alerts
    applyThresholdAlerts();
}


// ═══════════════════════════════════════════════════════════════
// 5. THEME ENGINE
// ═══════════════════════════════════════════════════════════════

function setTheme(swatch) {
    const color = swatch.dataset.color;
    const glow = swatch.dataset.glow;

    document.documentElement.style.setProperty('--neon-accent', color);
    document.documentElement.style.setProperty('--neon-accent-glow', glow);
    document.documentElement.style.setProperty('--border-accent', color.replace(')', ',0.25)').replace('rgb', 'rgba').replace('#', ''));

    // Compute border-accent from hex
    const r = parseInt(color.slice(1,3), 16);
    const g = parseInt(color.slice(3,5), 16);
    const b = parseInt(color.slice(5,7), 16);
    document.documentElement.style.setProperty('--border-accent', `rgba(${r},${g},${b},0.25)`);

    // Update active swatch
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
    swatch.classList.add('active');

    // Persist
    localStorage.setItem('datapulse_theme', JSON.stringify({ accent: color, glow: glow }));
}

function resetTheme() {
    localStorage.removeItem('datapulse_theme');
    document.documentElement.style.setProperty('--neon-accent', '#a855f7');
    document.documentElement.style.setProperty('--neon-accent-glow', 'rgba(168,85,247,0.6)');
    document.documentElement.style.setProperty('--border-accent', 'rgba(168,85,247,0.25)');

    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
    const defaultSwatch = document.querySelector('.color-swatch[data-color="#a855f7"]');
    if (defaultSwatch) defaultSwatch.classList.add('active');
}

function loadSavedTheme() {
    const saved = localStorage.getItem('datapulse_theme');
    if (saved) {
        try {
            const theme = JSON.parse(saved);
            document.documentElement.style.setProperty('--neon-accent', theme.accent);
            document.documentElement.style.setProperty('--neon-accent-glow', theme.glow);

            const r = parseInt(theme.accent.slice(1,3), 16);
            const g = parseInt(theme.accent.slice(3,5), 16);
            const b = parseInt(theme.accent.slice(5,7), 16);
            document.documentElement.style.setProperty('--border-accent', `rgba(${r},${g},${b},0.25)`);

            // Highlight correct swatch
            document.querySelectorAll('.color-swatch').forEach(s => {
                s.classList.remove('active');
                if (s.dataset.color === theme.accent) s.classList.add('active');
            });
        } catch (e) {}
    }
}


// ═══════════════════════════════════════════════════════════════
// 6. AI MODE TOGGLE
// ═══════════════════════════════════════════════════════════════

function toggleAIMode() {
    const toggle = document.getElementById('ai-mode-toggle');
    currentAIMode = toggle.checked ? 'cloud' : 'local';
    localStorage.setItem('datapulse_ai_mode', currentAIMode);
    updateAIModeUI();
}

function updateAIModeUI() {
    const badge = document.getElementById('ai-mode-badge');
    const label = document.getElementById('ai-mode-label');
    const toggleLabel = document.getElementById('ai-toggle-label');
    const toggle = document.getElementById('ai-mode-toggle');

    if (currentAIMode === 'cloud') {
        badge.className = 'ai-mode-indicator mode-cloud';
        label.textContent = 'Cloud AI';
        if (toggleLabel) toggleLabel.innerHTML = '<i class="fa-solid fa-cloud"></i> <strong>Cloud AI Mode</strong> — Groq-powered insights';
        if (toggle) toggle.checked = true;
    } else {
        badge.className = 'ai-mode-indicator mode-local';
        label.textContent = 'Local Math';
        if (toggleLabel) toggleLabel.innerHTML = '<i class="fa-solid fa-microchip"></i> <strong>Local Math Mode</strong> — Data stays private';
        if (toggle) toggle.checked = false;
    }
}


// ═══════════════════════════════════════════════════════════════
// 7. KPI THRESHOLD ALERTS
// ═══════════════════════════════════════════════════════════════

function saveThresholds() {
    const min = document.getElementById('threshold-min').value;
    const max = document.getElementById('threshold-max').value;
    localStorage.setItem('datapulse_thresholds', JSON.stringify({ min: min, max: max }));
    applyThresholdAlerts();
}

function loadThresholds() {
    const saved = localStorage.getItem('datapulse_thresholds');
    if (saved) {
        try {
            const t = JSON.parse(saved);
            if (t.min) document.getElementById('threshold-min').value = t.min;
            if (t.max) document.getElementById('threshold-max').value = t.max;
        } catch(e) {}
    }
}

function applyThresholdAlerts() {
    const saved = localStorage.getItem('datapulse_thresholds');
    if (!saved) return;

    try {
        const t = JSON.parse(saved);
        const m = BACKEND_DATA.kpiMetrics;
        if (!m) return;

        const sumCard = document.getElementById('kpi-sum');
        const avgCard = document.getElementById('kpi-avg');

        // Clear previous alerts
        [sumCard, avgCard].forEach(card => {
            if (card) {
                card.classList.remove('alert-high', 'alert-low');
                const oldBadge = card.querySelector('.alert-badge');
                if (oldBadge) oldBadge.remove();
            }
        });

        // Check sum against thresholds
        if (t.max && m.total > parseFloat(t.max)) {
            sumCard.classList.add('alert-high');
            sumCard.insertAdjacentHTML('beforeend', '<span class="alert-badge high">Above Limit</span>');
        } else if (t.min && m.total < parseFloat(t.min)) {
            sumCard.classList.add('alert-low');
            sumCard.insertAdjacentHTML('beforeend', '<span class="alert-badge low">Below Limit</span>');
        }

        // Check avg against thresholds
        if (t.max && m.mean > parseFloat(t.max)) {
            avgCard.classList.add('alert-high');
            avgCard.insertAdjacentHTML('beforeend', '<span class="alert-badge high">Above Limit</span>');
        } else if (t.min && m.mean < parseFloat(t.min)) {
            avgCard.classList.add('alert-low');
            avgCard.insertAdjacentHTML('beforeend', '<span class="alert-badge low">Below Limit</span>');
        }
    } catch(e) {}
}


// ═══════════════════════════════════════════════════════════════
// 8. WHAT-IF SIMULATOR
// ═══════════════════════════════════════════════════════════════

function initWhatIfControls() {
    const colSelect = document.getElementById('whatif-column');
    if (!colSelect) return;

    BACKEND_DATA.numericCols.forEach(col => {
        const opt = document.createElement('option');
        opt.value = col;
        opt.textContent = col;
        colSelect.appendChild(opt);
    });

    // Sync slider with input
    const slider = document.getElementById('whatif-slider');
    const input = document.getElementById('whatif-value-input');
    const label = document.getElementById('whatif-slider-label');
    const opSelect = document.getElementById('whatif-operation');

    slider.addEventListener('input', () => {
        input.value = slider.value;
        updateSliderLabel();
    });

    input.addEventListener('input', () => {
        slider.value = Math.min(Math.max(input.value, 0), 100);
        updateSliderLabel();
    });

    opSelect.addEventListener('change', updateSliderLabel);

    function updateSliderLabel() {
        const op = opSelect.value;
        const val = input.value;
        if (op.includes('pct')) {
            label.textContent = val + '%';
        } else if (op === 'multiply') {
            label.textContent = val + 'x';
        } else {
            label.textContent = val;
        }
    }
}

function runWhatIf() {
    const column = document.getElementById('whatif-column').value;
    const operation = document.getElementById('whatif-operation').value;
    const value = document.getElementById('whatif-value-input').value;
    const btn = document.getElementById('whatif-run-btn');

    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Simulating...';
    btn.disabled = true;

    // Determine secondary cat
    const secondaryCat = BACKEND_DATA.categoricalCols.length > 1 
        ? BACKEND_DATA.categoricalCols[1] 
        : BACKEND_DATA.primaryCat;

    fetch('/api/whatif/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            data_json: BACKEND_DATA.dataJson,
            column: column,
            operation: operation,
            value: value,
            primary_cat: BACKEND_DATA.primaryCat,
            secondary_cat: secondaryCat,
            date_col: BACKEND_DATA.dateCat,
            ai_mode: currentAIMode,
        })
    })
    .then(res => res.json())
    .then(data => {
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Simulate';
        btn.disabled = false;

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Show comparison
        const compSection = document.getElementById('whatif-comparison');
        compSection.style.display = 'block';

        const origEl = document.getElementById('whatif-original');
        const projEl = document.getElementById('whatif-projected');
        origEl.textContent = Number(data.original_metrics.total).toLocaleString(undefined, {maximumFractionDigits: 2});
        projEl.textContent = Number(data.new_metrics.total).toLocaleString(undefined, {maximumFractionDigits: 2});

        // Color the projected value
        if (data.new_metrics.total > data.original_metrics.total) {
            projEl.classList.remove('change-negative');
            projEl.classList.add('change-positive');
        } else if (data.new_metrics.total < data.original_metrics.total) {
            projEl.classList.remove('change-positive');
            projEl.classList.add('change-negative');
        }

        // AI Forecast
        const forecastSection = document.getElementById('whatif-forecast');
        if (data.ai_forecast && data.ai_forecast.trim()) {
            forecastSection.style.display = 'block';
            document.getElementById('whatif-forecast-text').textContent = data.ai_forecast;
        } else {
            forecastSection.style.display = 'none';
        }

        // Render What-If charts
        renderWhatIfCharts(data.bar_data, data.pie_data);
    })
    .catch(err => {
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Simulate';
        btn.disabled = false;
        console.error('What-If error:', err);
    });
}


// ═══════════════════════════════════════════════════════════════
// 9. ASK DATA (Natural Language Query)
// ═══════════════════════════════════════════════════════════════

function setQuery(text) {
    document.getElementById('ask-data-input').value = text;
    askData();
}

function askData() {
    const input = document.getElementById('ask-data-input');
    const query = input.value.trim();
    if (!query) return;

    const resultDiv = document.getElementById('ask-data-result');
    resultDiv.innerHTML = '<div class="query-result-card"><p style="color: var(--text-dim);"><i class="fa-solid fa-spinner fa-spin"></i> Analyzing...</p></div>';

    fetch('/api/query/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: query,
            data_json: BACKEND_DATA.dataJson,
            ai_mode: currentAIMode,
            primary_num: BACKEND_DATA.primaryNum,
            numeric_cols: BACKEND_DATA.numericCols,
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<div class="query-result-card">
                <p class="result-text" style="color: var(--neon-red);"><i class="fa-solid fa-circle-exclamation"></i> ${data.error}</p>
            </div>`;
            return;
        }

        let html = '<div class="query-result-card">';
        html += `<div class="result-label">${data.label || 'Result'}</div>`;
        html += `<div class="result-value">${data.value || data.text || '—'}</div>`;
        if (data.ai_explanation) {
            html += `<p class="result-text" style="margin-top: 12px; border-top: 1px solid var(--border-subtle); padding-top: 12px;">
                <i class="fa-solid fa-wand-magic-sparkles" style="color: var(--neon-accent);"></i> ${data.ai_explanation}
            </p>`;
        }
        html += '</div>';
        resultDiv.innerHTML = html;
    })
    .catch(err => {
        resultDiv.innerHTML = `<div class="query-result-card">
            <p class="result-text" style="color: var(--neon-red);"><i class="fa-solid fa-circle-exclamation"></i> Network error. Please try again.</p>
        </div>`;
        console.error('Ask Data error:', err);
    });
}


// ═══════════════════════════════════════════════════════════════
// 10. CORRELATION AI SUMMARY
// ═══════════════════════════════════════════════════════════════

function fetchAICorrelationSummary() {
    const btn = document.getElementById('corr-ai-btn');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Fetching...';
    btn.disabled = true;

    fetch('/api/correlation-summary/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            corr_matrix: BACKEND_DATA.corrMatrix,
            columns: BACKEND_DATA.corrColumns,
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('corr-summary-text').innerHTML = data.summary || 'No summary available.';
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Updated';
        btn.disabled = false;
        setTimeout(() => {
            btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Get AI Summary';
        }, 2000);
    })
    .catch(err => {
        btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Get AI Summary';
        btn.disabled = false;
        console.error('Correlation summary error:', err);
    });
}


// ═══════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Load settings
    loadSavedTheme();
    updateAIModeUI();
    loadThresholds();

    // Display metrics
    displayKPIMetrics();
    animateCounters();

    // Initialize What-If controls
    initWhatIfControls();
});
