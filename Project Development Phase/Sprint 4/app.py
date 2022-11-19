import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "wYjS7xFVjurVWF0LtAT5_FJwgyKYVud4scNeJxF6RyQ1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,
                                                                                 "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(_name_, template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'post'])
def predict():
    GRE_Score = int(request.form['GRE Score'])
    TOEFL_Score = int(request.form['TOEFL Score'])
    University_Rating = int(request.form['University Rating'])
    SOP = float(request.form['SOP'])
    LOR = float(request.form['LOR'])
    CGPA = float(request.form['CGPA'])
    Research = int(request.form['Research'])
    final_features = [[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]]

    payload_scoring = {'input_data': [
        {'fields': [["GRE Score", "TOEFL Score", "University Rating", "SOP", "LOR ", "CGPA", "Research"]],
         'values': final_features}]}
    print("hello")
    response_scoring = requests.post(
        'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e6e20418-0467-4649-8bd4-cda0dd5e580a/predictions?version=2022-11-18',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("scoring response")
    pred = response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    percent=output*100

    if output > 0.5:
        return redirect(url_for('chance', percent=output * 100))
    else:
        return redirect(url_for('no_chance', percent=output * 100))


@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])


@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("nochance.html", content=[percent])

if _name_ == "_main_":
    app.run(debug=True)