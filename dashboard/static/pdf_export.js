/* ═══════════════════════════════════════════════════════════════
   DATAPULSE — MODULAR PDF EXPORT SYSTEM
   Selective export with html2pdf.js
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
// PDF GENERATION
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

    // Build the export container
    const exportDiv = document.createElement('div');
    exportDiv.style.cssText = 'background: #0a0e17; padding: 30px; color: #f1f5f9; font-family: Inter, sans-serif;';

    // Header
    exportDiv.innerHTML = `
        <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid rgba(168,85,247,0.3); padding-bottom: 20px;">
            <h1 style="font-size: 28px; color: #f1f5f9; margin-bottom: 5px;">
                Data<span style="color: #a855f7;">Pulse</span> Analytics Report
            </h1>
            <p style="color: #94a3b8; font-size: 13px;">
                Generated on ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                &nbsp;|&nbsp; File: ${BACKEND_DATA.fileName}
            </p>
        </div>
    `;

    // AI Summary
    if (selections.summary) {
        const aiText = document.getElementById('ai-text-container');
        if (aiText) {
            exportDiv.innerHTML += `
                <div style="margin-bottom: 25px; padding: 20px; border: 1px solid rgba(168,85,247,0.2); border-radius: 12px; background: rgba(168,85,247,0.05);">
                    <h3 style="color: #a855f7; font-size: 16px; margin-bottom: 12px;">
                        ✦ Executive AI Summary
                    </h3>
                    <div style="color: #94a3b8; font-size: 13px; line-height: 1.8;">
                        ${aiText.innerHTML}
                    </div>
                </div>
            `;
        }
    }

    // KPI Metrics
    if (selections.kpi) {
        const m = BACKEND_DATA.kpiMetrics;
        exportDiv.innerHTML += `
            <div style="margin-bottom: 25px;">
                <h3 style="color: #38bdf8; font-size: 16px; margin-bottom: 12px;">📊 Key Performance Indicators</h3>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                    <div style="padding: 16px; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; text-align: center; background: rgba(0,0,0,0.3);">
                        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Total Sum</div>
                        <div style="font-size: 22px; font-weight: 700; color: #f1f5f9;">${Number(m.total).toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                    </div>
                    <div style="padding: 16px; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; text-align: center; background: rgba(0,0,0,0.3);">
                        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Average</div>
                        <div style="font-size: 22px; font-weight: 700; color: #f1f5f9;">${Number(m.mean).toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                    </div>
                    <div style="padding: 16px; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; text-align: center; background: rgba(0,0,0,0.3);">
                        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Median</div>
                        <div style="font-size: 22px; font-weight: 700; color: #f1f5f9;">${Number(m.median).toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                    </div>
                    <div style="padding: 16px; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; text-align: center; background: rgba(0,0,0,0.3);">
                        <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Std Dev</div>
                        <div style="font-size: 22px; font-weight: 700; color: #f1f5f9;">${Number(m.std).toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                    </div>
                </div>
            </div>
        `;
    }

    // Charts — clone from DOM
    const chartMap = {
        trend: 'trend-chart-container',
        bar: 'bar-chart-container',
        pie: 'pie-chart-container',
    };

    for (const [key, containerId] of Object.entries(chartMap)) {
        if (selections[key]) {
            const original = document.getElementById(containerId);
            if (original && original.style.display !== 'none') {
                const clone = original.cloneNode(true);
                clone.style.marginBottom = '25px';
                clone.style.padding = '20px';
                clone.style.border = '1px solid rgba(255,255,255,0.08)';
                clone.style.borderRadius = '12px';
                clone.style.background = 'rgba(0,0,0,0.3)';
                exportDiv.appendChild(clone);
            }
        }
    }

    // Anomaly section
    if (selections.anomaly) {
        const anomalyContainer = document.getElementById('anomaly-scatter-container');
        const anomalySummary = document.getElementById('anomaly-summary');
        if (anomalySummary) {
            const summClone = anomalySummary.cloneNode(true);
            const wrapper = document.createElement('div');
            wrapper.style.cssText = 'margin-bottom: 25px;';
            wrapper.innerHTML = '<h3 style="color: #ef4444; font-size: 16px; margin-bottom: 12px;">⚠ Anomaly Detection Report</h3>';
            wrapper.appendChild(summClone);
            if (anomalyContainer) {
                const chartClone = anomalyContainer.cloneNode(true);
                chartClone.style.marginTop = '12px';
                wrapper.appendChild(chartClone);
            }
            exportDiv.appendChild(wrapper);
        }
    }

    // Correlation section
    if (selections.correlation) {
        const heatmapContainer = document.getElementById('heatmap-container');
        const corrSummary = document.getElementById('corr-summary-text');
        if (heatmapContainer) {
            const wrapper = document.createElement('div');
            wrapper.style.cssText = 'margin-bottom: 25px;';
            wrapper.innerHTML = '<h3 style="color: #38bdf8; font-size: 16px; margin-bottom: 12px;">🔗 Correlation Analysis</h3>';
            const chartClone = heatmapContainer.cloneNode(true);
            wrapper.appendChild(chartClone);
            if (corrSummary) {
                wrapper.innerHTML += `<div style="margin-top: 12px; padding: 14px; border-left: 3px solid #38bdf8; background: rgba(56,189,248,0.05); border-radius: 8px; font-size: 13px; color: #94a3b8;">${corrSummary.innerHTML}</div>`;
            }
            exportDiv.appendChild(wrapper);
        }
    }

    // Data Table
    if (selections.table) {
        const tableSection = document.getElementById('data-table-section');
        if (tableSection) {
            const clone = tableSection.cloneNode(true);
            clone.style.marginBottom = '25px';
            exportDiv.appendChild(clone);
        }
    }

    // Footer
    exportDiv.innerHTML += `
        <div style="text-align: center; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 20px;">
            <p style="color: #64748b; font-size: 11px;">
                Report generated by DataPulse Analytics Engine &nbsp;|&nbsp; ${new Date().getFullYear()}
            </p>
        </div>
    `;

    // Generate PDF
    closeExportModal();

    const opt = {
        margin: [0.3, 0.3, 0.3, 0.3],
        filename: `DataPulse_Report_${new Date().toISOString().split('T')[0]}.pdf`,
        image: { type: 'jpeg', quality: 0.95 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: false,
            backgroundColor: '#0a0e17',
        },
        jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] },
    };

    // Temporarily append to body for rendering
    exportDiv.style.position = 'fixed';
    exportDiv.style.left = '-9999px';
    exportDiv.style.top = '0';
    exportDiv.style.width = '1100px';
    document.body.appendChild(exportDiv);

    html2pdf().set(opt).from(exportDiv).save().then(() => {
        document.body.removeChild(exportDiv);
    }).catch(() => {
        document.body.removeChild(exportDiv);
    });
}
