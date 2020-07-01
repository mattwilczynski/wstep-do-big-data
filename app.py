# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:57:18 2020

@author: mattw
"""

from flask import Flask, render_template, Response
from matplotlib import pyplot as plt
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

import requests

# Klasa SiteUtils będzie zawierała dodatkowe mechanizmy wykorzystywane
# w naszej aplikacji

class SiteUtils():
#zapytanie API o aktywne przypadki w Polsce
    def requests_active_covid_cases(self):
        zakazenia = requests.get("https://api.covid19api.com/country/poland")
        #zakazenia = requests.get("https://api.exchangeratesapi.io/history?start_at=2018-01-01&end_at=2018-09-01&base=USD")
        return zakazenia

#tworzenie dataframe z danych z api
    def prepare_data(self):
        zakazenia = self.requests_active_covid_cases()
        df = pd.read_json(zakazenia.content)
        return df

#tworzenie wykresu
    def create_figure(self):
        df = self.prepare_data()
        plot = df['Active'].plot()
        fig = plot.get_figure()
        return fig
        
        # print(df['Active'])
                  

app = Flask(__name__)
utils = SiteUtils()   

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plot_png():
    fig = utils.create_figure()
    output=io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    app.run()