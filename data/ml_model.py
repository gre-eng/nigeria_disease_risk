import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from data.cleaner import clean_lassa, clean_nga


def prepare_lassa_data():
    df = clean_lassa('lassa_fever_timeseries_full.csv')
    df = df.sort_values('week_start_date').reset_index(drop=True)
    df['week_index'] = range(len(df))
    df['month'] = df['week_start_date'].dt.month
    df['year'] = df['week_start_date'].dt.year
    X = df[['week_index', 'month', 'year']].values
    y = df['confirmed_cases'].values
    return X, y, df


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, 0, None)
    rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 2)
    mae = round(mean_absolute_error(y_test, y_pred), 2)
    r2 = round(r2_score(y_test, y_pred), 4)
    return rmse, mae, r2, y_pred


def train_and_compare_models():
    X, y, df = prepare_lassa_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # Model 1 — Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_rmse, lr_mae, lr_r2, lr_pred = evaluate_model(lr, X_test, y_test)

    # Model 2 — Polynomial Regression degree 3
    poly = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
    poly.fit(X_train, y_train)
    poly_rmse, poly_mae, poly_r2, poly_pred = evaluate_model(poly, X_test, y_test)

    # Model 3 — Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_rmse, rf_mae, rf_r2, rf_pred = evaluate_model(rf, X_test, y_test)

    # Pick best model by RMSE
    models = {
        'Linear Regression': (lr_rmse, lr),
        'Polynomial Regression': (poly_rmse, poly),
        'Random Forest': (rf_rmse, rf)
    }
    best_name = min(models, key=lambda k: models[k][0])
    best_model = models[best_name][1]

    comparison = [
        {
            'model': 'Linear Regression',
            'rmse': lr_rmse,
            'mae': lr_mae,
            'r2': lr_r2,
            'best': best_name == 'Linear Regression'
        },
        {
            'model': 'Polynomial Regression (degree 3)',
            'rmse': poly_rmse,
            'mae': poly_mae,
            'r2': poly_r2,
            'best': best_name == 'Polynomial Regression'
        },
        {
            'model': 'Random Forest (100 estimators)',
            'rmse': rf_rmse,
            'mae': rf_mae,
            'r2': rf_r2,
            'best': best_name == 'Random Forest'
        }
    ]

    # Test set actual vs predicted for best model
    test_dates = df.iloc[len(X_train):]['week_start_date'].dt.strftime('%Y-%m-%d').tolist()
    best_pred = list(np.clip(best_model.predict(X_test), 0, None).round(0).astype(int))
    validation_plot = [
        {'date': d, 'actual': int(a), 'predicted': int(p)}
        for d, a, p in zip(test_dates, y_test, best_pred)
    ]

    return comparison, validation_plot, best_name, best_model, X, y, df


def train_lassa_forecast():
    comparison, validation_plot, best_name, best_model, X, y, df = train_and_compare_models()

    last_index = X[-1][0]
    last_date = df['week_start_date'].max()
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(weeks=1), periods=12, freq='W'
    )
    future_X = np.array([
        [last_index + i, d.month, d.year]
        for i, d in enumerate(future_dates, 1)
    ])
    predictions = np.clip(best_model.predict(future_X), 0, None).round(0).astype(int)

    actual = df.tail(20)[['week_start_date', 'confirmed_cases']].copy()
    actual['week_start_date'] = actual['week_start_date'].dt.strftime('%Y-%m-%d')
    actual['type'] = 'actual'
    actual = actual.rename(columns={'confirmed_cases': 'predicted_cases'})
    actual_list = actual.to_dict(orient='records')

    forecast_list = [
        {
            'week_start_date': d.strftime('%Y-%m-%d'),
            'predicted_cases': int(p),
            'type': 'forecast'
        }
        for d, p in zip(future_dates, predictions)
    ]

    return actual_list + forecast_list


def get_model_comparison():
    comparison, validation_plot, best_name, _, _, _, _ = train_and_compare_models()
    return comparison, validation_plot, best_name


def get_water_correlation():
    with open('datasets/worldbank_water.json') as f:
        raw = json.load(f)

    records = raw[1]
    water_data = {}
    for r in records:
        if r['value'] is not None:
            year = int(r['date'])
            water_data[year] = round(float(r['value']), 2)

    df = clean_nga('NGA-Table 1.csv')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    yearly = df.groupby('year').agg(total_cases=('cases', 'sum')).reset_index()

    merged = []
    for _, row in yearly.iterrows():
        year = int(row['year'])
        if year in water_data:
            merged.append({
                'year': year,
                'total_cases': int(row['total_cases']),
                'water_access_pct': water_data[year]
            })

    return sorted(merged, key=lambda x: x['year'])


def get_risk_allocation():
    df = clean_nga('NGA-Table 1.csv')
    hotspots = df.groupby('state').agg(
        total_cases=('cases', 'sum'),
        total_deaths=('deaths', 'sum'),
        avg_cfr=('cfr', 'mean'),
        avg_cases_per_100k=('cases_per_100k', 'mean')
    ).reset_index()

    max_cases = hotspots['total_cases'].max()

    def compute_risk_score(row):
        if max_cases == 0:
            return 0
        score = (row['total_cases'] / max_cases) * 60
        score += min(row['avg_cfr'], 10) * 2
        score += min(row['avg_cases_per_100k'], 50) * 0.4
        return round(score, 1)

    hotspots['risk_score'] = hotspots.apply(compute_risk_score, axis=1)
    total_score = hotspots['risk_score'].sum()

    TOTAL_ORS = 500000
    TOTAL_VACCINES = 200000
    TOTAL_WORKERS = 5000

    allocations = []
    for _, row in hotspots.sort_values('risk_score', ascending=False).iterrows():
        share = row['risk_score'] / total_score if total_score > 0 else 0
        if row['risk_score'] >= 40:
            risk_level = 'High'
        elif row['risk_score'] >= 20:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        allocations.append({
            'state': row['state'],
            'risk_score': row['risk_score'],
            'risk_level': risk_level,
            'ors_packets': int(share * TOTAL_ORS),
            'vaccines': int(share * TOTAL_VACCINES),
            'health_workers': int(share * TOTAL_WORKERS),
            'total_cases': int(row['total_cases']),
            'avg_cfr': round(row['avg_cfr'], 2)
        })

    return allocations