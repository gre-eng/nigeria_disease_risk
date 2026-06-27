# Nigeria Disease Risk Intelligence Platform

An AI-powered web application for disease risk surveillance in Nigeria, focused on cholera and Lassa fever. The platform combines historical outbreak data, machine learning forecasting, and a risk-based resource allocation model into a single interactive dashboard.

## Live Demo

(https://nigeria-disease-risk.onrender.com)

## What This Project Does

- **Cholera Hotspot Mapping** — ranks all 36 Nigerian states and the FCT by a composite risk score based on case burden, case fatality rate, and population-adjusted incidence.
- **Lassa Fever Surveillance** — visualises national weekly case and death trends from NCDC situation reports (2020–2025).
- **AI-Powered Forecasting** — trains and compares three machine learning models (Linear Regression, Polynomial Regression, Random Forest) to forecast Lassa fever cases 12 weeks ahead, automatically selecting the best-performing model by RMSE on a held-out test set.
- **Model Validation** — transparently reports RMSE, MAE, and R² for each model, with a chronological 80/20 train-test split to avoid data leakage in time-series forecasting.
- **Water Access vs Cholera Correlation** — overlays World Bank water access data (indicator `SH.H2O.BASW.ZS`) against cholera case trends to support WASH (Water, Sanitation and Hygiene) investment arguments.
- **AI-Driven Resource Allocation** — proportionally allocates ORS packets, vaccines, and health workers across states based on computed risk scores.
- **LGA-Level Ranking** — surfaces the top 10 highest-risk Local Government Areas for targeted intervention.

## Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn (Linear Regression, Polynomial Regression, Random Forest)
- **Data Processing**: pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript, Chart.js (rendered via Flask/Jinja2 templating)
- **Deployment**: Render (Gunicorn as the production WSGI server)
- **Progressive Web App**: installable on phone, tablet, and desktop via a web app manifest and service worker

## Data Sources

| Dataset | Source | Coverage | Indicator |
|---|---|---|---|
| Lassa Fever Weekly Reports | NCDC Nigeria | 2020–2025 | Suspected, confirmed, deaths |
| Cholera Outbreak Records | HDX / Academic Literature | 1971–2023 | Cases, deaths, CFR by state |
| Water Access | World Bank Open Data | 2000–2025 | `SH.H2O.BASW.ZS` |
| Population Denominators | World Bank / NBS | 1971–2023 | National population estimates |

## Methodology

### Risk Score Formula
Risk Score = (Cases / Max Cases) × 60 + min(CFR, 10) × 2 + min(Cases per 100k, 50) × 0.4

This weights absolute case burden most heavily (60%), while incorporating mortality severity (CFR) and population-adjusted incidence to avoid bias toward densely populated states. States scoring ≥40 are classified High risk, ≥20 Medium, and below 20 Low risk.

### Forecasting Approach

Three models were evaluated — Linear Regression as a baseline, Polynomial Regression to capture seasonal non-linearity, and Random Forest to handle feature interactions without assuming linearity. A chronological (non-shuffled) 80/20 train-test split was used to preserve temporal structure, since random shuffling would constitute data leakage in time-series forecasting. Features used: week index, month (seasonality proxy), and year (trend proxy). The best model is selected automatically by lowest RMSE on the held-out test set.

## Known Data Limitations

- The HDX cholera dataset was retrieved empty (4 bytes); cholera analysis relies entirely on a historical outbreak dataset covering 1971–2023, which has inconsistent LGA-level reporting.
- Lassa fever data has no state-level breakdown — only national weekly aggregates are available from NCDC, so sub-national hotspot mapping for Lassa fever is not currently possible.
- Some source data contained LGA names entered into the State column (e.g. Maiduguri, Jere, Mafa, Ganjuwa); these were corrected programmatically via a validated state-lookup mapping.
- World Bank water access data is national-level only; state-level WASH data would improve spatial modelling.
- The forecasting model uses only temporal features. Incorporating rainfall, temperature, displacement data, and vaccination coverage would likely improve predictive accuracy.

## Future Work

- Integrate LSTM neural networks for sequence-aware outbreak forecasting
- Add a state-level choropleth map using Nigeria GeoJSON for spatial risk visualisation
- Incorporate climate variables (e.g. ERA5 reanalysis data) as model features
- Connect to a live NCDC API for real-time dashboard updates
- Apply SHAP values for model interpretability, relevant to public health policy adoption

## Running Locally

```bash
pip install -r requirements.txt
python generate_html.py
python app.py
```

Then open `http://127.0.0.1:5000` in a browser.

## Author

Built as an independent applied AI project exploring machine learning and data engineering applications for public health surveillance in Nigeria.
