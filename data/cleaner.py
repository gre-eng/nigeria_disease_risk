import pandas as pd

# The only 36 valid Nigerian states + FCT
VALID_STATES = [
    'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa',
    'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo',
    'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano',
    'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger',
    'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto',
    'Taraba', 'Yobe', 'Zamfara', 'Federal Capital Territory'
]

# Map dirty values to correct state names
STATE_CORRECTIONS = {
    'akwa': 'Akwa Ibom',
    'akwa ': 'Akwa Ibom',
    'oyo ': 'Oyo',
    'osum': 'Osun',
    'borno ': 'Borno',
    'adamawa ': 'Adamawa',
    'kwara ': 'Kwara',
    'cross river ': 'Cross River',
    'yobe ': 'Yobe',
    'kebi': 'Kebbi',
    'jugawa': 'Jigawa',
    'federal capital territory ': 'Federal Capital Territory',
    # These are LGAs mistakenly in the State column — map to their real state
    'maiduguri': 'Borno',
    'jere': 'Borno',
    'mafa': 'Borno',
    'guzamala': 'Borno',
    'monguno': 'Borno',
    'dikwa': 'Borno',
    'muna': 'Borno',
    'tofa lga': 'Kano',
    'ganjuwa': 'Bauchi',
    'akwa ibom': 'Akwa Ibom',
}

def fix_state(value):
    if pd.isna(value):
        return None
    cleaned = str(value).strip().lower()
    # Check corrections map first
    if cleaned in STATE_CORRECTIONS:
        return STATE_CORRECTIONS[cleaned]
    # Check if it already matches a valid state (case-insensitive)
    for state in VALID_STATES:
        if cleaned == state.lower():
            return state
    # No match — discard
    return None

def clean_nga(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        'State': 'state',
        'Local Government Area': 'lga',
        'Cases': 'cases',
        'Deaths': 'deaths',
        'Confirmed': 'confirmed',
        'CFR (%)': 'cfr',
        'Population': 'population',
        'Cases/100,000': 'cases_per_100k',
        'Deaths/100,000': 'deaths_per_100k',
        'Year': 'year'
    })
    df['state'] = df['state'].apply(fix_state)
    # Drop rows where state could not be identified
    df = df[df['state'].notna()]
    df['cases'] = pd.to_numeric(df['cases'], errors='coerce').fillna(0)
    df['deaths'] = pd.to_numeric(df['deaths'], errors='coerce').fillna(0)
    df['cfr'] = pd.to_numeric(df['cfr'], errors='coerce').fillna(0)
    df['population'] = pd.to_numeric(df['population'], errors='coerce').fillna(0)
    df['cases_per_100k'] = pd.to_numeric(df['cases_per_100k'], errors='coerce').fillna(0)
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    return df

def clean_lassa(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['confirmed_cases'])
    df['epi_year'] = pd.to_numeric(df['epi_year'], errors='coerce')
    df['confirmed_cases'] = pd.to_numeric(df['confirmed_cases'], errors='coerce').fillna(0)
    df['suspected_cases'] = pd.to_numeric(df['suspected_cases'], errors='coerce').fillna(0)
    df['deaths'] = pd.to_numeric(df['deaths'], errors='coerce').fillna(0)
    df['week_start_date'] = pd.to_datetime(df['week_start_date'], errors='coerce')
    return df