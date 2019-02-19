from flask import Flask, render_template, url_for, request, jsonify
from experiment import Experiment
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/showResults', methods=["GET","POST"])
def showResults():
    if request.method == 'POST':
        pA = float(request.form['pA'])
        cA = float(request.form['cA'])
        pB = float(request.form['pB'])
        cB = float(request.form['cB'])
        exp = Experiment(
			pA=pA,
			pB=pB,
			cA=cA,
			cB=cB
		)
        data = exp.serialize()
    return render_template('showResults.html', data=data)

if __name__ == '__main__':
    app.run()

