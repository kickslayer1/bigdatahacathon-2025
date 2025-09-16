from flask import Flask, send_file, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def home():
    # HTML template with embedded chart
    html = '''
    <html>
    <head><title>Exports Dashboard</title></head>
    <body>
        <h1>Exports Data Visualization</h1>
        <img src="/chart.png" alt="Exports Chart" style="max-width:100%;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.12);">
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/chart.png')
def chart():
    # Load and plot data
    df = pd.read_csv('datasetx.csv')
    pivot = df.pivot_table(index='time', columns='item', values='amount', aggfunc='sum', fill_value=0)
    ax = pivot.plot(kind='bar', figsize=(10,6), colormap='tab20')
    plt.title('Exports Over Time by Item')
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.tight_layout()

    # Save to in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


# Endpoint to serve options for form
@app.route('/options')
def get_options():
    df = pd.read_csv('datasetx.csv')
    items = sorted(df['item'].unique())
    times = sorted(df['time'].unique())
    amounts = sorted(df['amount'].unique())
    return {'items': items, 'times': times, 'amounts': amounts}

# Dummy prediction endpoint (replace with model logic as needed)
from flask import request, jsonify
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Example: Dummy prediction using amount
    price = float(data.get('amount', 0)) * 1.1  # Replace with your model
    return jsonify({'price': price})

if __name__ == '__main__':
    app.run(debug=True)