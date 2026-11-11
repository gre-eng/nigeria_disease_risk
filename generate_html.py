html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nigeria Disease Risk Intelligence Platform</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#00b4d8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom"></script>
</head>
<body>

<header>
    <div class="header-inner">
        <div class="header-left">
            <span class="flag">&#127475;&#127468;</span>
            <div>
                <h1>Nigeria Disease Risk Intelligence Platform</h1>
                <p>Cholera &middot; Lassa Fever &middot; AI Forecasting &middot; Resource Allocation &middot; Epidemiological Surveillance</p>
            </div>
        </div>
        <div class="header-right">
            <span class="badge-header">NCDC</span>
            <span class="badge-header">HDX</span>
            <span class="badge-header">World Bank</span>
            <span class="badge-header">ML Powered</span>
        </div>
    </div>
</header>

<nav class="tab-nav">
    <button class="tab-btn active" onclick="showTab('cholera', this)">Cholera Hotspots</button>
    <button class="tab-btn" onclick="showTab('lassa', this)">Lassa Fever</button>
    <button class="tab-btn" onclick="showTab('forecast', this)">AI Forecast</button>
    <button class="tab-btn" onclick="showTab('validation', this)">Model Validation</button>
    <button class="tab-btn" onclick="showTab('water', this)">Water and Disease</button>
    <button class="tab-btn" onclick="showTab('allocation', this)">Resource Allocation</button>
    <button class="tab-btn" onclick="showTab('lga', this)">LGA Ranking</button>
    <button class="tab-btn" onclick="showTab('methodology', this)">Methodology</button>
</nav>

<main>

    <div id="tab-cholera" class="tab-content active">
        <div class="section-header">
            <h2>Cholera Hotspot Allocator - By State</h2>
            <p>Risk scores computed from total cases, case fatality rate, and cases per 100,000 population across all 36 states and FCT</p>
        </div>
        <div class="chart-row">
            <div class="chart-box">
                <h3>Cases and Deaths by Year</h3>
                <canvas id="choleraYearChart"></canvas>
            </div>
            <div class="chart-box">
                <h3>Top 10 States by Case Load</h3>
                <canvas id="choleraStateChart"></canvas>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>State</th>
                    <th>Total Cases</th>
                    <th>Total Deaths</th>
                    <th>Avg CFR (%)</th>
                    <th>Cases per 100k</th>
                    <th>Outbreaks</th>
                    <th>Risk Level</th>
                </tr>
            </thead>
            <tbody>
                {% for i, row in enumerate(cholera_hotspots) %}
                <tr>
                    <td>{{ i + 1 }}</td>
                    <td><strong>{{ row.state }}</strong></td>
                    <td>{{ "{:,.0f}".format(row.total_cases) }}</td>
                    <td>{{ "{:,.0f}".format(row.total_deaths) }}</td>
                    <td>{{ row.avg_cfr }}%</td>
                    <td>{{ row.avg_cases_per_100k }}</td>
                    <td>{{ row.outbreaks }}</td>
                    <td><span class="badge {{ row.risk_level }}">{{ row.risk_level }}</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div id="tab-lassa" class="tab-content">
        <div class="section-header">
            <h2>Lassa Fever - National Epidemiological Trend</h2>
            <p>Weekly surveillance data from NCDC situation reports 2020-2025</p>
        </div>
        <div class="chart-row">
            <div class="chart-box wide">
                <h3>Weekly Confirmed Cases and Deaths</h3>
                <canvas id="lassaTrendChart"></canvas>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Suspected Cases</th>
                    <th>Confirmed Cases</th>
                    <th>Deaths</th>
                    <th>Case Fatality Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {% for row in lassa_summary %}
                <tr>
                    <td><strong>{{ row.epi_year }}</strong></td>
                    <td>{{ "{:,.0f}".format(row.total_suspected) }}</td>
                    <td>{{ "{:,.0f}".format(row.total_confirmed) }}</td>
                    <td>{{ "{:,.0f}".format(row.total_deaths) }}</td>
                    <td>
                        {% if row.cfr > 20 %}
                            <span class="badge High">{{ row.cfr }}%</span>
                        {% elif row.cfr > 10 %}
                            <span class="badge Medium">{{ row.cfr }}%</span>
                        {% else %}
                            <span class="badge Low">{{ row.cfr }}%</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div id="tab-forecast" class="tab-content">
        <div class="section-header">
            <h2>AI-Powered Lassa Fever Outbreak Forecast</h2>
            <p>Best performing model selected automatically from three candidates based on lowest RMSE on held-out test data</p>
        </div>
        <div class="info-cards">
            <div class="info-card">
                <span class="info-label">Best Model Selected</span>
                <span class="info-value">{{ best_model_name }}</span>
            </div>
            <div class="info-card">
                <span class="info-label">Selection Criterion</span>
                <span class="info-value">Lowest RMSE</span>
            </div>
            <div class="info-card">
                <span class="info-label">Train/Test Split</span>
                <span class="info-value">80% / 20%</span>
            </div>
            <div class="info-card">
                <span class="info-label">Forecast Horizon</span>
                <span class="info-value">12 Weeks Ahead</span>
            </div>
        </div>
        <div class="chart-box" style="margin-top:24px">
            <h3>Actual vs Forecasted Confirmed Cases</h3>
            <canvas id="forecastChart"></canvas>
        </div>
        <div class="insight-box">
            <strong>Model Disclaimer:</strong> This forecast is based on historical temporal patterns only.
            Actual outbreak dynamics are influenced by rainfall, population movement, sanitation access,
            and intervention coverage. This tool supports and does not replace expert epidemiological judgment.
        </div>
    </div>

    <div id="tab-validation" class="tab-content">
        <div class="section-header">
            <h2>Model Validation - Comparing Three ML Algorithms</h2>
            <p>80/20 train-test split applied chronologically. Models evaluated on unseen held-out data using RMSE, MAE and R2 metrics.</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>RMSE</th>
                    <th>MAE</th>
                    <th>R2</th>
                    <th>Selected</th>
                </tr>
            </thead>
            <tbody>
                {% for row in model_comparison %}
                <tr class="{{ 'best-row' if row.best else '' }}">
                    <td><strong>{{ row.model }}</strong></td>
                    <td>{{ row.rmse }}</td>
                    <td>{{ row.mae }}</td>
                    <td>{{ row.r2 }}</td>
                    <td>
                        {% if row.best %}
                            <span class="badge Low">Best Model</span>
                        {% else %}
                            <span style="color:#3a5a75">-</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="metric-explainer">
            <div class="metric-card">
                <span class="metric-title">RMSE</span>
                <span class="metric-desc">Root Mean Square Error - penalises large prediction errors. Lower is better.</span>
            </div>
            <div class="metric-card">
                <span class="metric-title">MAE</span>
                <span class="metric-desc">Mean Absolute Error - average prediction error in case counts. Lower is better.</span>
            </div>
            <div class="metric-card">
                <span class="metric-title">R2</span>
                <span class="metric-desc">Coefficient of Determination - how much variance the model explains. Closer to 1.0 is better.</span>
            </div>
        </div>
        <div class="chart-box" style="margin-top:24px">
            <h3>Best Model - Actual vs Predicted on Test Set</h3>
            <canvas id="validationChart"></canvas>
        </div>
    </div>

    <div id="tab-water" class="tab-content">
        <div class="section-header">
            <h2>Water Access vs Cholera Cases - Correlation Analysis</h2>
            <p>World Bank indicator: People using at least basic drinking water services vs annual cholera burden in Nigeria</p>
        </div>
        <div class="chart-box">
            <h3>Water Access (%) vs Cholera Cases Over Time</h3>
            <canvas id="waterChart"></canvas>
        </div>
        <div class="insight-box">
            <strong>Public Health Insight:</strong> This analysis uses World Bank indicator SH.H2O.BASW.ZS
            to examine the relationship between safe water access and cholera burden. Where water access
            stagnates or declines, cholera outbreaks intensify, supporting evidence-based WASH
            (Water, Sanitation and Hygiene) investment as the primary prevention strategy for Nigeria.
        </div>
    </div>

    <div id="tab-allocation" class="tab-content">
        <div class="section-header">
            <h2>AI-Driven Resource Allocation Engine</h2>
            <p>Proportional allocation of national health resources based on composite risk scores. Risk score = 60% case burden + 20% CFR + 20% population-adjusted incidence.</p>
        </div>
        <div class="info-cards">
            <div class="info-card">
                <span class="info-label">Total ORS Packets</span>
                <span class="info-value">500,000</span>
            </div>
            <div class="info-card">
                <span class="info-label">Total Vaccines</span>
                <span class="info-value">200,000</span>
            </div>
            <div class="info-card">
                <span class="info-label">Total Health Workers</span>
                <span class="info-value">5,000</span>
            </div>
            <div class="info-card">
                <span class="info-label">Allocation Method</span>
                <span class="info-value">Risk-Proportional</span>
            </div>
        </div>
        <table style="margin-top:24px">
            <thead>
                <tr>
                    <th>#</th>
                    <th>State</th>
                    <th>Risk Score</th>
                    <th>Risk Level</th>
                    <th>ORS Packets</th>
                    <th>Vaccines</th>
                    <th>Health Workers</th>
                    <th>Total Cases</th>
                    <th>Avg CFR (%)</th>
                </tr>
            </thead>
            <tbody>
                {% for i, row in enumerate(allocations) %}
                <tr>
                    <td>{{ i + 1 }}</td>
                    <td><strong>{{ row.state }}</strong></td>
                    <td>{{ row.risk_score }}</td>
                    <td><span class="badge {{ row.risk_level }}">{{ row.risk_level }}</span></td>
                    <td>{{ "{:,.0f}".format(row.ors_packets) }}</td>
                    <td>{{ "{:,.0f}".format(row.vaccines) }}</td>
                    <td>{{ "{:,.0f}".format(row.health_workers) }}</td>
                    <td>{{ "{:,.0f}".format(row.total_cases) }}</td>
                    <td>{{ row.avg_cfr }}%</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div id="tab-lga" class="tab-content">
        <div class="section-header">
            <h2>Top 10 High-Risk Local Government Areas</h2>
            <p>LGA-level hotspot ranking for targeted intervention and resource allocation</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>State</th>
                    <th>LGA</th>
                    <th>Total Cases</th>
                    <th>Total Deaths</th>
                </tr>
            </thead>
            <tbody>
                {% for i, row in enumerate(top_lga) %}
                <tr>
                    <td>{{ i + 1 }}</td>
                    <td><strong>{{ row.state }}</strong></td>
                    <td>{{ row.lga }}</td>
                    <td>{{ "{:,.0f}".format(row.total_cases) }}</td>
                    <td>{{ "{:,.0f}".format(row.total_deaths) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div id="tab-methodology" class="tab-content">
        <div class="section-header">
            <h2>Methodology, Limitations and Future Work</h2>
            <p>Academic framing of technical decisions, data quality issues, and research directions</p>
        </div>
        <div class="method-section">
            <h3>1. Why AI for Disease Surveillance?</h3>
            <p>Traditional disease surveillance in Nigeria relies on manual aggregation of paper-based
            reports submitted to the Nigeria Centre for Disease Control (NCDC). This introduces
            reporting delays of 2 to 6 weeks, inhibiting timely response. This platform applies
            machine learning to automate risk stratification and outbreak forecasting, enabling
            proactive rather than reactive public health intervention. AI adds value here by
            processing multi-source heterogeneous data including epidemiological records, population
            denominators, and WASH indicators into a unified, interpretable risk signal.</p>
        </div>
        <div class="method-section">
            <h3>2. ML Model Selection Rationale</h3>
            <p>Three models were evaluated: Linear Regression (baseline), Polynomial Regression
            (captures seasonal non-linearity), and Random Forest (handles feature interactions
            without assuming linearity). A chronological 80/20 train-test split was applied
            to preserve temporal structure. Random shuffling would constitute data leakage
            in time-series forecasting. The best model was selected objectively by lowest RMSE
            on the held-out test set. Features used: week index, month as seasonality proxy,
            and year as trend proxy.</p>
        </div>
        <div class="method-section">
            <h3>3. Risk Score Methodology</h3>
            <p>The composite risk score for cholera hotspot classification is computed as:</p>
            <br>
            <code>Risk Score = (Cases / Max Cases) x 60 + min(CFR, 10) x 2 + min(Cases per 100k, 50) x 0.4</code>
            <br><br>
            <p>This weights absolute case burden most heavily at 60%, while incorporating
            mortality severity via CFR and population-adjusted incidence to avoid bias
            toward densely populated states. States scoring 40 and above are High risk,
            20 and above are Medium, and below 20 are Low risk.</p>
        </div>
        <div class="method-section">
            <h3>4. Data Limitations and Acknowledged Gaps</h3>
            <div class="limitation-list">
                <div class="limitation-item">
                    <span class="lim-badge">Gap</span>
                    <span>The HDX cholera CSV was retrieved empty at 4 bytes. Cholera analysis relies entirely on the NGA historical outbreak dataset covering 1971 to 2023 with inconsistent LGA-level reporting.</span>
                </div>
                <div class="limitation-item">
                    <span class="lim-badge">Gap</span>
                    <span>Lassa fever data contains no state-level breakdown, only national weekly aggregates from NCDC situation reports. Sub-national Lassa hotspot mapping is not possible with current data.</span>
                </div>
                <div class="limitation-item">
                    <span class="lim-badge">Gap</span>
                    <span>The NGA dataset contained LGA names entered in the State column such as Maiduguri, Jere, Mafa, and Ganjuwa. These were corrected programmatically by mapping to their parent states using a validated lookup table.</span>
                </div>
                <div class="limitation-item">
                    <span class="lim-badge">Gap</span>
                    <span>World Bank water access data is national-level only. State-level WASH data from NWASCO or JMP would significantly improve spatial risk modelling.</span>
                </div>
                <div class="limitation-item">
                    <span class="lim-badge">Gap</span>
                    <span>The ML forecast uses only temporal features. Incorporating rainfall, temperature, displacement data, and vaccination coverage would substantially improve predictive accuracy.</span>
                </div>
            </div>
        </div>
        <div class="method-section">
            <h3>5. Future Research Directions</h3>
            <div class="future-list">
                <div class="future-item">Integrate LSTM neural networks for sequence-aware outbreak forecasting</div>
                <div class="future-item">Add state-level choropleth map using Nigeria GeoJSON for spatial risk visualisation</div>
                <div class="future-item">Incorporate climate variables from ERA5 reanalysis data as model features</div>
                <div class="future-item">Connect to NCDC live API for real-time surveillance dashboard updates</div>
                <div class="future-item">Expand resource allocation to include cold chain logistics for vaccine distribution</div>
                <div class="future-item">Apply SHAP values for model interpretability critical for public health policy uptake</div>
            </div>
        </div>
        <div class="method-section">
            <h3>6. Data Sources</h3>
            <table>
                <thead>
                    <tr>
                        <th>Dataset</th>
                        <th>Source</th>
                        <th>Coverage</th>
                        <th>Indicator</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Lassa Fever Weekly Reports</td>
                        <td>NCDC Nigeria</td>
                        <td>2020 to 2025</td>
                        <td>Suspected, confirmed, deaths</td>
                    </tr>
                    <tr>
                        <td>Cholera Outbreak Records</td>
                        <td>HDX and Academic Literature</td>
                        <td>1971 to 2023</td>
                        <td>Cases, deaths, CFR by state</td>
                    </tr>
                    <tr>
                        <td>Water Access</td>
                        <td>World Bank Open Data</td>
                        <td>2000 to 2025</td>
                        <td>SH.H2O.BASW.ZS</td>
                    </tr>
                    <tr>
                        <td>Population Denominators</td>
                        <td>World Bank and NBS</td>
                        <td>1971 to 2023</td>
                        <td>National population estimates</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</main>

<footer>
    <p>Nigeria Disease Risk Intelligence Platform - Data Sources: NCDC, HDX, World Bank -
    ML Models: Linear Regression, Polynomial Regression, Random Forest (Scikit-learn) -
    Built for Public Health Surveillance and Applied AI Research</p>
</footer>

<script>
function showTab(name, btn) {
    document.querySelectorAll('.tab-content').forEach(function(t) {
        t.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(function(b) {
        b.classList.remove('active');
    });
    document.getElementById('tab-' + name).classList.add('active');
    btn.classList.add('active');
}

var zoomConfig = {
    pan: { enabled: true, mode: 'x' },
    zoom: { wheel: { enabled: false }, pinch: { enabled: false }, drag: { enabled: false } }
};

window.onload = function() {

    fetch('/api/cholera-by-year')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            new Chart(document.getElementById('choleraYearChart'), {
                type: 'bar',
                data: {
                    labels: data.map(function(d) { return d.year; }),
                    datasets: [
                        { label: 'Cases', data: data.map(function(d) { return d.total_cases; }), backgroundColor: 'rgba(0,180,216,0.7)', borderColor: '#00b4d8', borderWidth: 1 },
                        { label: 'Deaths', data: data.map(function(d) { return d.total_deaths; }), backgroundColor: 'rgba(231,76,60,0.7)', borderColor: '#e74c3c', borderWidth: 1 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#ccc' } }, zoom: zoomConfig },
                    scales: {
                        x: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } },
                        y: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } }
                    }
                }
            });
        });

    var stateLabels = [{% for row in cholera_hotspots[:10] %}"{{ row.state }}",{% endfor %}];
    var stateCases = [{% for row in cholera_hotspots[:10] %}{{ row.total_cases }},{% endfor %}];
    new Chart(document.getElementById('choleraStateChart'), {
        type: 'bar',
        data: {
            labels: stateLabels,
            datasets: [{
                label: 'Total Cases',
                data: stateCases,
                backgroundColor: stateLabels.map(function(_, i) {
                    return i < 3 ? 'rgba(231,76,60,0.8)' : i < 6 ? 'rgba(230,126,34,0.8)' : 'rgba(39,174,96,0.8)';
                }),
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false }, zoom: zoomConfig },
            scales: {
                x: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } },
                y: { ticks: { color: '#ccc' }, grid: { color: '#1e3245' } }
            }
        }
    });

    fetch('/api/lassa-trend')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            new Chart(document.getElementById('lassaTrendChart'), {
                type: 'line',
                data: {
                    labels: data.map(function(d) { return d.week_start_date; }),
                    datasets: [
                        { label: 'Confirmed Cases', data: data.map(function(d) { return d.confirmed_cases; }), borderColor: '#e74c3c', backgroundColor: 'rgba(231,76,60,0.1)', fill: true, tension: 0.3, pointRadius: 0 },
                        { label: 'Deaths', data: data.map(function(d) { return d.deaths; }), borderColor: '#8e44ad', backgroundColor: 'rgba(142,68,173,0.1)', fill: true, tension: 0.3, pointRadius: 0 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#ccc' } }, zoom: zoomConfig },
                    scales: {
                        x: { ticks: { color: '#aaa', maxTicksLimit: 12 }, grid: { color: '#1e3245' } },
                        y: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } }
                    }
                }
            });
        });

    fetch('/api/lassa-forecast')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var actualCount = 0;
            data.forEach(function(d) { if (d.type === 'actual') actualCount++; });
            new Chart(document.getElementById('forecastChart'), {
                type: 'line',
                data: {
                    labels: data.map(function(d) { return d.week_start_date; }),
                    datasets: [
                        {
                            label: 'Actual Cases',
                            data: data.map(function(d) { return d.type === 'actual' ? d.predicted_cases : null; }),
                            borderColor: '#00b4d8',
                            backgroundColor: 'rgba(0,180,216,0.1)',
                            fill: true,
                            tension: 0.3,
                            pointRadius: 2
                        },
                        {
                            label: 'Forecasted Cases',
                            data: data.map(function(d, i) {
                                return (d.type === 'forecast' || i === actualCount - 1) ? d.predicted_cases : null;
                            }),
                            borderColor: '#f39c12',
                            backgroundColor: 'rgba(243,156,18,0.1)',
                            borderDash: [6, 3],
                            fill: true,
                            tension: 0.3,
                            pointRadius: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#ccc' } }, zoom: zoomConfig },
                    scales: {
                        x: { ticks: { color: '#aaa', maxTicksLimit: 16 }, grid: { color: '#1e3245' } },
                        y: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } }
                    }
                }
            });
        });

    var valDates = [{% for row in validation_plot %}"{{ row.date }}",{% endfor %}];
    var valActual = [{% for row in validation_plot %}{{ row.actual }},{% endfor %}];
    var valPred = [{% for row in validation_plot %}{{ row.predicted }},{% endfor %}];
    new Chart(document.getElementById('validationChart'), {
        type: 'line',
        data: {
            labels: valDates,
            datasets: [
                {
                    label: 'Actual Cases',
                    data: valActual,
                    borderColor: '#00b4d8',
                    backgroundColor: 'rgba(0,180,216,0.1)',
                    fill: false,
                    tension: 0.3,
                    pointRadius: 3
                },
                {
                    label: 'Predicted Cases',
                    data: valPred,
                    borderColor: '#f39c12',
                    backgroundColor: 'rgba(243,156,18,0.1)',
                    borderDash: [5, 3],
                    fill: false,
                    tension: 0.3,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#ccc' } }, zoom: zoomConfig },
            scales: {
                x: { ticks: { color: '#aaa', maxTicksLimit: 12 }, grid: { color: '#1e3245' } },
                y: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } }
            }
        }
    });

    fetch('/api/water-correlation')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            new Chart(document.getElementById('waterChart'), {
                type: 'line',
                data: {
                    labels: data.map(function(d) { return d.year; }),
                    datasets: [
                        {
                            label: 'Cholera Cases',
                            data: data.map(function(d) { return d.total_cases; }),
                            borderColor: '#e74c3c',
                            backgroundColor: 'rgba(231,76,60,0.1)',
                            fill: true,
                            tension: 0.3,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Water Access (%)',
                            data: data.map(function(d) { return d.water_access_pct; }),
                            borderColor: '#00b4d8',
                            backgroundColor: 'rgba(0,180,216,0.1)',
                            fill: true,
                            tension: 0.3,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#ccc' } }, zoom: zoomConfig },
                    scales: {
                        x: { ticks: { color: '#aaa' }, grid: { color: '#1e3245' } },
                        y: { ticks: { color: '#e74c3c' }, grid: { color: '#1e3245' }, position: 'left', title: { display: true, text: 'Cases', color: '#e74c3c' } },
                        y1: { ticks: { color: '#00b4d8' }, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Water Access %', color: '#00b4d8' } }
                    }
                }
            });
        });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/service-worker.js');
    }

};
</script>

</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html written successfully")