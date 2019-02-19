from flask import Flask, render_template, url_for, request, jsonify
from experiment import Experiment
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():
	data = request.get_json()
	exp = Experiment(
		pA=data['pA'],
		pB=data['pB'],
		cA=data['cA'],
		cB=data['cB']
	)
	return jsonify(exp.serialize())

@app.route('/showResults', methods=["GET","POST"])
def showResults():
    if request.method == 'POST':
        pA = float(request.form['pA'])
        cA = float(request.form['cA'])
        pB = float(request.form['pB'])
        cB = float(request.form['cB'])
        url = "http://127.0.0.1:5000/result"
        data = requests.post(url, json={"pA": pA,"pB":pB, "cA":cA, "cB":cB}).json()
    return render_template('showResults.html', data=data)

app.debug = True
app.run(port=5000)

