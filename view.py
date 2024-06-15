from flask import Flask, render_template
import os

import matplotlib
matplotlib.use('Agg')
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder='template')

@app.route('/')

def home():
    return render_template('index.html')

def index():
    data = pd.read_csv('AirPassengers.csv')
    data['Month'] = pd.to_datetime(data['Month'])

    data.columns = ['Month','Passengers']
    data['Month'] = pd.to_datetime(data['Month'], format='%Y-%m')
    data = data.set_index('Month')
    data.head(12)
    decomposition = sm.tsa.seasonal_decompose(data.Passengers, model='multiplicative')
    a = decomposition.seasonal
    a.plot()
    try:
        os.remove('foo.png')
    except OSError:
        pass
    plt.savefig('foo.png')
    return "Hello!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port)