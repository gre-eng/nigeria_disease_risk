from flask import Flask, render_template, jsonify
from data.disease_data import (
    get_cholera_hotspots,
    get_cholera_by_year,
    get_top10_lga,
    get_lassa_summary,
    get_lassa_trend
)
from data.ml_model import (
    train_lassa_forecast,
    get_water_correlation,
    get_risk_allocation,
    get_model_comparison
)

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)


@app.route('/')
def index():
    cholera_hotspots = get_cholera_hotspots()
    top_lga = get_top10_lga()
    lassa_summary = get_lassa_summary()
    allocations = get_risk_allocation()
    comparison, validation_plot, best_name = get_model_comparison()
    return render_template('index.html',
        cholera_hotspots=cholera_hotspots,
        top_lga=top_lga,
        lassa_summary=lassa_summary,
        allocations=allocations,
        model_comparison=comparison,
        best_model_name=best_name,
        validation_plot=validation_plot
    )


@app.route('/api/lassa-trend')
def lassa_trend():
    return jsonify(get_lassa_trend())


@app.route('/api/cholera-by-year')
def cholera_by_year():
    return jsonify(get_cholera_by_year())


@app.route('/api/lassa-forecast')
def lassa_forecast():
    return jsonify(train_lassa_forecast())


@app.route('/api/water-correlation')
def water_correlation():
    return jsonify(get_water_correlation())


if __name__ == '__main__':
    app.run(debug=True)