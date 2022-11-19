import pandas as pd
from flask import Flask , request,jsonify,render_template,redirect,url_for
import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "wYjS7xFVjurVWF0LtAT5_FJwgyKYVud4scNeJxF6RyQ1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], "values": [[316,104,3,3,3.5,8,1]]}]}
response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e6e20418-0467-4649-8bd4-cda0dd5e580a/predictions?version=2022-11-18', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions =response_scoring.json()
pred = predictions['predictions'][0]['values'][0][0]
if(pred == 0):
    print("You're unselected")
else:
    print("You're selected")