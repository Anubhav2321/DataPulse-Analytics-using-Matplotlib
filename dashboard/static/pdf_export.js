/* ═══════════════════════════════════════════════════════════════
   DATAPULSE — SERVER-SIDE PDF EXPORT SYSTEM
   Sends data to backend for real Matplotlib chart rendering
   and premium ReportLab PDF generation
   ═══════════════════════════════════════════════════════════════ */

// ═══════════════════════════════════════════════════════════════
// MODAL CONTROLS
// ═══════════════════════════════════════════════════════════════

function openExportModal() {
    document.getElementById('export-modal').classList.add('active');
}

function closeExportModal() {
    document.getElementById('export-modal').classList.remove('active');
}

// Close on backdrop click
document.addEventListener('click', (e) => {
    const modal = document.getElementById('export-modal');
    if (e.target === modal) {
        closeExportModal();
    }
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeExportModal();
    }
});


// ═══════════════════════════════════════════════════════════════
// LOADING OVERLAY
// ═══════════════════════════════════════════════════════════════

function showPDFLoading() {
    const overlay = document.getElementById('pdf-loading-overlay');
    if (overlay) {
        overlay.classList.add('active');
        // Animate progress steps
        _animateProgressSteps();
    }
}

function hidePDFLoading() {
    const overlay = document.getElementById('pdf-loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

function _animateProgressSteps() {
    const steps = document.querySelectorAll('.pdf-progress-step');
    steps.forEach((step, i) => {
        step.classList.remove('active', 'done');
    });

    let currentStep = 0;
    const interval = setInterval(() => {
        if (currentStep > 0 && currentStep <= steps.length) {
            steps[currentStep - 1].classList.remove('active');
            steps[currentStep - 1].classList.add('done');
        }
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 1200);

    // Store interval ID to clear on hide
    window._pdfProgressInterval = interval;
}


// ═══════════════════════════════════════════════════════════════
// PDF GENERATION (Server-Side)
// ═══════════════════════════════════════════════════════════════

function generatePDF() {
    // Read checkbox selections
    const selections = {
        summary: document.getElementById('exp-summary').checked,
        kpi: document.getElementById('exp-kpi').checked,
        trend: document.getElementById('exp-trend').checked,
        bar: document.getElementById('exp-bar').checked,
        pie: document.getElementById('exp-pie').checked,
        anomaly: document.getElementById('exp-anomaly').checked,
        correlation: document.getElementById('exp-correlation').checked,
        table: document.getElementById('exp-table').checked,
    };

    // Check that at least one section is selected
    const hasSelection = Object.values(selections).some(v => v);
    if (!hasSelection) {
        alert('Please select at least one section to include in the report.');
        return;
    }

    // Close modal and show loading overlay
    closeExportModal();
    showPDFLoading();

    // Get the AI insights text from the DOM
    const aiTextEl = document.getElementById('ai-text-container');
    const aiInsights = aiTextEl ? aiTextEl.innerHTML : '';

    // Get the correlation summary text from the DOM
    const corrSummaryEl = document.getElementById('corr-summary-text');
    const corrSummary = corrSummaryEl ? corrSummaryEl.innerHTML : '';

    // Build the payload with all data the backend needs
    const payload = {
        selections: selections,
        file_name: BACKEND_DATA.fileName,
        kpi_metrics: BACKEND_DATA.kpiMetrics,
        bar_data: BACKEND_DATA.barData,
        pie_data: BACKEND_DATA.pieData,
        trend_data: BACKEND_DATA.trendData,
        anomaly_data: BACKEND_DATA.anomalyData,
        anomaly_scatter: BACKEND_DATA.anomalyScatter,
        corr_matrix: BACKEND_DATA.corrMatrix,
        corr_columns: BACKEND_DATA.corrColumns,
        corr_summary: corrSummary,
        ai_insights: aiInsights,
        data_json: BACKEND_DATA.dataJson,
        primary_num: BACKEND_DATA.primaryNum,
        total_rows: document.querySelector('.counter[data-target]')
            ? parseInt(document.querySelector('.counter[data-target]').getAttribute('data-target'))
            : BACKEND_DATA.dataJson.length,
        total_cols: BACKEND_DATA.numericCols.length + BACKEND_DATA.categoricalCols.length,
    };

    // Get CSRF token
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

    // Send to backend
    fetch('/api/export-pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(payload),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'PDF generation failed');
            });
        }
        return response.blob();
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `DataPulse_Report_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        hidePDFLoading();
    })
    .catch(error => {
        hidePDFLoading();
        console.error('PDF export error:', error);
        alert('❌ PDF generation failed: ' + error.message);
    });
}
