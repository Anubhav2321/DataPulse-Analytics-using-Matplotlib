/* ═══════════════════════════════════════════════════════════════
   DATAPULSE — APEXCHARTS RENDERING ENGINE
   All chart creation and update logic
   ═══════════════════════════════════════════════════════════════ */

// ── COMMON CHART CONFIG ──
const CHART_THEME = {
    chart: {
        background: 'transparent',
        toolbar: { show: false },
        animations: { enabled: true, easing: 'easeinout', speed: 800 },
        fontFamily: 'Inter, sans-serif',
    },
    theme: { mode: 'dark' },
    grid: { borderColor: 'rgba(56, 189, 248, 0.08)', strokeDashArray: 4 },
    tooltip: {
        theme: 'dark',
        style: { fontSize: '13px', fontFamily: 'Inter' },
        marker: { show: true },
        y: { formatter: (v) => v ? v.toLocaleString(undefined, {maximumFractionDigits: 2}) : '0' }
    },
};

// Store chart instances for cleanup
const chartInstances = {};

function destroyChart(key) {
    if (chartInstances[key]) {
        chartInstances[key].destroy();
        delete chartInstances[key];
    }
}


// ═══════════════════════════════════════════════════════════════
// 1. TREND CHART (Area)
// ═══════════════════════════════════════════════════════════════

function renderTrendChart() {
    const data = BACKEND_DATA.trendData;
    const container = document.getElementById('trend-chart-container');

    if (!data || !data.labels || data.labels.length === 0) {
        container.style.display = 'none';
        return;
    }

    // Find anomaly points for the trend
    const anomalyIndices = [];
    const anomalyInfo = BACKEND_DATA.anomalyData[BACKEND_DATA.primaryNum];
    if (anomalyInfo) {
        anomalyInfo.indices.forEach(idx => {
            if (idx < data.values.length) anomalyIndices.push(idx);
        });
    }

    // Build point annotations for anomalies
    const pointAnnotations = anomalyIndices.map(idx => ({
        x: data.labels[idx],
        y: data.values[idx],
        marker: {
            size: 6,
            fillColor: '#ef4444',
            strokeColor: '#ef4444',
            strokeWidth: 2,
            cssClass: 'anomaly-marker',
        },
        label: {
            text: 'Anomaly',
            style: { background: '#ef4444', color: '#fff', fontSize: '10px', padding: { left: 6, right: 6, top: 2, bottom: 2 } },
            borderRadius: 4,
        }
    }));

    const options = {
        ...CHART_THEME,
        series: [{ name: BACKEND_DATA.primaryNum, data: data.values }],
        chart: { ...CHART_THEME.chart, type: 'area', height: 320 },
        title: {
            text: data.title,
            align: 'left',
            style: { color: '#f1f5f9', fontSize: '15px', fontWeight: '700' }
        },
        colors: ['#a855f7'],
        fill: {
            type: 'gradient',
            gradient: { shadeIntensity: 1, opacityFrom: 0.5, opacityTo: 0.05, stops: [0, 90, 100] }
        },
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 3 },
        xaxis: {
            categories: data.labels,
            labels: { style: { colors: '#64748b', fontSize: '11px' }, rotate: -45, rotateAlways: data.labels.length > 10 }
        },
        yaxis: {
            labels: {
                style: { colors: '#64748b' },
                formatter: (v) => v ? v.toLocaleString(undefined, {maximumFractionDigits: 0}) : '0'
            }
        },
        annotations: { points: pointAnnotations },
    };

    destroyChart('trend');
    chartInstances['trend'] = new ApexCharts(container, options);
    chartInstances['trend'].render();
}


// ═══════════════════════════════════════════════════════════════
// 2. BAR CHART
// ═══════════════════════════════════════════════════════════════

function renderBarChart(targetId, data) {
    const container = document.getElementById(targetId || 'bar-chart-container');
    if (!data || !data.labels || data.labels.length === 0) {
        container.style.display = 'none';
        return;
    }

    const options = {
        ...CHART_THEME,
        series: [{ name: 'Total', data: data.values }],
        chart: { ...CHART_THEME.chart, type: 'bar', height: 300 },
        title: {
            text: data.title,
            align: 'left',
            style: { color: '#f1f5f9', fontSize: '15px', fontWeight: '700' }
        },
        colors: ['#38bdf8', '#a855f7', '#ec4899', '#10b981', '#facc15', '#f97316', '#06b6d4', '#8b5cf6', '#f43f5e', '#14b8a6'],
        plotOptions: {
            bar: { borderRadius: 6, columnWidth: '50%', distributed: true }
        },
        dataLabels: { enabled: false },
        xaxis: {
            categories: data.labels,
            labels: { style: { colors: '#64748b', fontSize: '11px' }, rotate: -45, rotateAlways: data.labels.length > 6 }
        },
        yaxis: {
            labels: {
                style: { colors: '#64748b' },
                formatter: (v) => v ? v.toLocaleString(undefined, {maximumFractionDigits: 0}) : '0'
            }
        },
        legend: { show: false },
    };

    const key = targetId || 'bar';
    destroyChart(key);
    chartInstances[key] = new ApexCharts(container, options);
    chartInstances[key].render();
}


// ═══════════════════════════════════════════════════════════════
// 3. DONUT CHART
// ═══════════════════════════════════════════════════════════════

function renderDonutChart(targetId, data) {
    const container = document.getElementById(targetId || 'pie-chart-container');
    if (!data || !data.labels || data.labels.length === 0) {
        container.style.display = 'none';
        return;
    }

    const options = {
        ...CHART_THEME,
        series: data.values,
        labels: data.labels,
        chart: { ...CHART_THEME.chart, type: 'donut', height: 310 },
        title: {
            text: data.title,
            align: 'left',
            style: { color: '#f1f5f9', fontSize: '15px', fontWeight: '700' }
        },
        colors: ['#a855f7', '#38bdf8', '#ec4899', '#facc15', '#10b981'],
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        name: { color: '#94a3b8', fontSize: '13px' },
                        value: {
                            color: '#f1f5f9', fontSize: '22px', fontWeight: '700',
                            formatter: (v) => Number(v).toLocaleString(undefined, {maximumFractionDigits: 0})
                        },
                        total: {
                            show: true,
                            color: '#94a3b8',
                            fontSize: '12px',
                            label: 'Total',
                            formatter: (w) => {
                                const t = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                                return t.toLocaleString(undefined, {maximumFractionDigits: 0});
                            }
                        }
                    }
                }
            }
        },
        stroke: { show: true, colors: ['#0f172a'], width: 2 },
        legend: { position: 'bottom', labels: { colors: '#94a3b8' }, fontSize: '12px' },
    };

    const key = targetId || 'donut';
    destroyChart(key);
    chartInstances[key] = new ApexCharts(container, options);
    chartInstances[key].render();
}


// ═══════════════════════════════════════════════════════════════
// 4. ANOMALY SCATTER CHART
// ═══════════════════════════════════════════════════════════════

function renderAnomalyView() {
    const scatter = BACKEND_DATA.anomalyScatter;
    const anomalyData = BACKEND_DATA.anomalyData;
    const container = document.getElementById('anomaly-scatter-container');
    const summaryDiv = document.getElementById('anomaly-summary');

    // Summary cards
    const primaryAnom = anomalyData[BACKEND_DATA.primaryNum];
    const totalAnomalies = primaryAnom ? primaryAnom.count : 0;
    const totalPoints = (scatter.normal_x.length + scatter.anomaly_x.length);
    const anomalyPct = totalPoints > 0 ? ((totalAnomalies / totalPoints) * 100).toFixed(1) : 0;

    summaryDiv.innerHTML = `
        <div class="anomaly-stat">
            <div class="num red">${totalAnomalies}</div>
            <div class="desc">Anomalies Found</div>
        </div>
        <div class="anomaly-stat">
            <div class="num blue">${totalPoints}</div>
            <div class="desc">Total Data Points</div>
        </div>
        <div class="anomaly-stat">
            <div class="num ${totalAnomalies > 0 ? 'red' : 'green'}">${anomalyPct}%</div>
            <div class="desc">Anomaly Rate</div>
        </div>
        <div class="anomaly-stat">
            <div class="num blue">${primaryAnom ? primaryAnom.mean.toLocaleString(undefined, {maximumFractionDigits: 2}) : '—'}</div>
            <div class="desc">Mean (${BACKEND_DATA.primaryNum})</div>
        </div>
    `;

    // Build scatter series
    const normalSeries = scatter.normal_x.map((x, i) => ([x, scatter.normal_y[i]]));
    const anomalySeries = scatter.anomaly_x.map((x, i) => ([x, scatter.anomaly_y[i]]));

    const options = {
        ...CHART_THEME,
        series: [
            { name: 'Normal', data: normalSeries },
            { name: 'Anomaly (Z > 2)', data: anomalySeries },
        ],
        chart: { ...CHART_THEME.chart, type: 'scatter', height: 350 },
        title: {
            text: `${BACKEND_DATA.primaryNum} — Anomaly Detection (Z-Score > 2.0)`,
            align: 'left',
            style: { color: '#f1f5f9', fontSize: '15px', fontWeight: '700' }
        },
        colors: ['#38bdf8', '#ef4444'],
        markers: {
            size: [5, 8],
            strokeWidth: [0, 2],
            strokeColors: ['transparent', '#ef4444'],
            hover: { sizeOffset: 3 }
        },
        xaxis: {
            title: { text: 'Data Point Index', style: { color: '#64748b' } },
            labels: { style: { colors: '#64748b' } },
        },
        yaxis: {
            title: { text: BACKEND_DATA.primaryNum, style: { color: '#64748b' } },
            labels: {
                style: { colors: '#64748b' },
                formatter: (v) => v ? v.toLocaleString(undefined, {maximumFractionDigits: 0}) : '0'
            },
        },
        legend: {
            position: 'top',
            labels: { colors: '#94a3b8' },
            fontSize: '12px',
            markers: { size: 6 },
        },
    };

    destroyChart('anomaly');
    chartInstances['anomaly'] = new ApexCharts(container, options);
    chartInstances['anomaly'].render();
}


// ═══════════════════════════════════════════════════════════════
// 5. CORRELATION HEATMAP
// ═══════════════════════════════════════════════════════════════

function renderCorrelationView() {
    const matrix = BACKEND_DATA.corrMatrix;
    const columns = BACKEND_DATA.corrColumns;
    const container = document.getElementById('heatmap-container');

    if (!matrix || !columns || columns.length < 2) {
        container.innerHTML = '<p style="color: var(--text-dim); text-align: center; padding: 40px;">Need at least 2 numeric columns for correlation analysis.</p>';
        return;
    }

    // Build heatmap series (ApexCharts expects [{name, data: [{x, y}]}])
    const series = columns.map((rowName, i) => ({
        name: rowName,
        data: columns.map((colName, j) => ({
            x: colName,
            y: matrix[i][j]
        }))
    }));

    const options = {
        ...CHART_THEME,
        series: series,
        chart: { ...CHART_THEME.chart, type: 'heatmap', height: Math.max(300, columns.length * 50) },
        title: {
            text: 'Pearson Correlation Matrix',
            align: 'left',
            style: { color: '#f1f5f9', fontSize: '15px', fontWeight: '700' }
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                radius: 4,
                colorScale: {
                    ranges: [
                        { from: -1, to: -0.5, name: 'Strong Negative', color: '#ef4444' },
                        { from: -0.5, to: -0.2, name: 'Weak Negative', color: '#f97316' },
                        { from: -0.2, to: 0.2, name: 'Neutral', color: '#64748b' },
                        { from: 0.2, to: 0.5, name: 'Weak Positive', color: '#38bdf8' },
                        { from: 0.5, to: 1, name: 'Strong Positive', color: '#a855f7' },
                    ]
                }
            }
        },
        dataLabels: {
            enabled: true,
            style: { colors: ['#f1f5f9'], fontSize: '12px', fontWeight: '600' },
            formatter: (val) => val.toFixed(2),
        },
        xaxis: {
            labels: { style: { colors: '#94a3b8', fontSize: '11px' } },
        },
        yaxis: {
            labels: { style: { colors: '#94a3b8', fontSize: '11px' } },
        },
        legend: {
            position: 'bottom',
            labels: { colors: '#94a3b8' },
            fontSize: '11px',
        },
    };

    destroyChart('heatmap');
    chartInstances['heatmap'] = new ApexCharts(container, options);
    chartInstances['heatmap'].render();
}


// ═══════════════════════════════════════════════════════════════
// 6. WHAT-IF CHARTS (Updated after simulation)
// ═══════════════════════════════════════════════════════════════

function renderWhatIfCharts(barData, pieData) {
    const chartsSection = document.getElementById('whatif-charts');
    chartsSection.style.display = 'grid';

    const barContainer = document.getElementById('whatif-bar-container');
    const pieContainer = document.getElementById('whatif-pie-container');

    // Reset visibility
    barContainer.style.display = '';
    pieContainer.style.display = '';

    if (barData && barData.labels && barData.labels.length > 0) {
        renderBarChart('whatif-bar-container', barData);
    } else {
        barContainer.style.display = 'none';
    }

    if (pieData && pieData.labels && pieData.labels.length > 0) {
        renderDonutChart('whatif-pie-container', pieData);
    } else {
        pieContainer.style.display = 'none';
    }
}


// ═══════════════════════════════════════════════════════════════
// INITIALIZATION — Render overview charts on load
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Render overview charts
    renderTrendChart();
    renderBarChart('bar-chart-container', BACKEND_DATA.barData);
    renderDonutChart('pie-chart-container', BACKEND_DATA.pieData);
});
