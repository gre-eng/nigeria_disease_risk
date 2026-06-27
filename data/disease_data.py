import pandas as pd
from data.cleaner import clean_nga, clean_lassa, VALID_STATES

def get_cholera_hotspots():
    df = clean_nga('NGA-Table 1.csv')
    hotspots = df.groupby('state').agg(
        total_cases=('cases', 'sum'),
        total_deaths=('deaths', 'sum'),
        avg_cfr=('cfr', 'mean'),
        avg_cases_per_100k=('cases_per_100k', 'mean'),
        outbreaks=('cases', 'count')
    ).reset_index()
    hotspots = hotspots.sort_values('total_cases', ascending=False)
    max_cases = hotspots['total_cases'].max()

    def risk_level(row):
        if max_cases == 0:
            return 'Low'
        score = (row['total_cases'] / max_cases) * 60
        score += min(row['avg_cfr'], 10) * 2
        score += min(row['avg_cases_per_100k'], 50) * 0.4
        if score >= 40:
            return 'High'
        elif score >= 20:
            return 'Medium'
        else:
            return 'Low'

    hotspots['risk_level'] = hotspots.apply(risk_level, axis=1)
    hotspots['avg_cfr'] = hotspots['avg_cfr'].round(2)
    hotspots['avg_cases_per_100k'] = hotspots['avg_cases_per_100k'].round(2)
    return hotspots.to_dict(orient='records')

def get_cholera_by_year():
    df = clean_nga('NGA-Table 1.csv')
    df = df.dropna(subset=['year'])
    by_year = df.groupby('year').agg(
        total_cases=('cases', 'sum'),
        total_deaths=('deaths', 'sum')
    ).reset_index()
    by_year['year'] = by_year['year'].astype(int)
    by_year = by_year.sort_values('year')
    return by_year.to_dict(orient='records')

def get_top10_lga():
    df = clean_nga('NGA-Table 1.csv')
    df = df[df['lga'].notna()]
    top = df.groupby(['state', 'lga']).agg(
        total_cases=('cases', 'sum'),
        total_deaths=('deaths', 'sum')
    ).reset_index()
    top = top[top['total_cases'] > 0]
    top = top.sort_values('total_cases', ascending=False).head(10)
    return top.to_dict(orient='records')

def get_lassa_summary():
    df = clean_lassa('lassa_fever_timeseries_full.csv')
    yearly = df.groupby('epi_year').agg(
        total_suspected=('suspected_cases', 'sum'),
        total_confirmed=('confirmed_cases', 'sum'),
        total_deaths=('deaths', 'sum')
    ).reset_index()
    yearly['cfr'] = (yearly['total_deaths'] / yearly['total_confirmed'].replace(0, 1) * 100).round(1)
    yearly['epi_year'] = yearly['epi_year'].astype(int)
    return yearly.to_dict(orient='records')

def get_lassa_trend():
    df = clean_lassa('lassa_fever_timeseries_full.csv')
    df = df.sort_values('week_start_date')
    trend = df[['week_start_date', 'confirmed_cases', 'suspected_cases', 'deaths']].copy()
    trend['week_start_date'] = trend['week_start_date'].dt.strftime('%Y-%m-%d')
    return trend.to_dict(orient='records')