import flask
from flask import render_template, redirect, url_for
import pandas as pd
import json
import plotly
import plotly.express as px

#Init variables
app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='template')
app.config["DEBUG"] = True

#set up routes

@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/<name>")
def user(name):
    return f"Hello-- {name}!"
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route('/testPlotly')
def testPlotly():
   df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
   })
   fig = px.bar(df, x='Fruit', y='Amount', color='City', 
      barmode='group')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('testPlotly.html', graphJSON=graphJSON)
    

#Run app
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)