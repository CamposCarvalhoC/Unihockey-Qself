import flask
from flask import render_template, redirect, url_for,request
from pandas.core.frame import DataFrame
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import pandas as pd
import json
import plotly
import plotly.express as px

#define global df
df = pd.DataFrame()
################# Utils ###########################
def read_data_csv(filepath):
	data = pd.read_csv(filepath,sep=";")
	data.index = data["Phone timestamp"]
	data =data.drop(columns=["Phone timestamp","sensor timestamp [ns]"])
	data.index = pd.to_datetime(data.index)
	return data

################# FLASK ###########################
#Init variables
app = flask.Flask(__name__, static_url_path='',
			static_folder='static',
			template_folder='template')
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER']="uploads/"

#set up routes
@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def save_file():
	global df	
	if request.method == 'POST':
		f = request.files['file']
		filename = secure_filename(f.filename)
		print(filename)
		f.save(app.config['UPLOAD_FOLDER'] + filename)
		df = read_data_csv(app.config['UPLOAD_FOLDER'] + filename)
		#content = file.read()
	return content()


# @app.route("/content")
def content():
	global df
	#df = read_data_csv("../../data/Passe_avant.csv")
	fig = px.line(df, x=df.index, y=df.columns,title='Données du match') #,hover_data={"date": "|%B %d, %Y"},
   #fig.update_xaxes( dtick="M1",tickformat="%b\n%Y")
	graphList=[]
	matchGraphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


	dftest = pd.DataFrame({
	  'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
	  'Bananas'],
	  'Amount': [4, 1, 2, 2, 4, 5],
	  'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
	})
	fig2 = px.bar(dftest, x='Fruit', y='Amount', color='City', 
	  barmode='group')
	barGraphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template('content.html', matchGraphJSON=matchGraphJSON,barGraphJSON=barGraphJSON)
	


# @app.route('/testSimpleBar')
# def testSimpleBar():
# 	df = pd.DataFrame({
# 	  'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
# 	  'Bananas'],
# 	  'Amount': [4, 1, 2, 2, 4, 5],
# 	  'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
# 	})
# 	fig = px.bar(df, x='Fruit', y='Amount', color='City', 
# 	  barmode='group')
# 	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
# 	return render_template('notdash.html', graphJSON=graphJSON)


 
#Run app
if __name__ == '__main__':
	app.run(host="localhost", port=5000, debug=True)