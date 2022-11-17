import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape

import inputScript  
import requests

app = Flask(__name__)

API_KEY = "JilW5zLzltmxGM00oOUA9alK1O5X-915tssbaLcLn2tE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



@app.route('/')
def predict():
    return render_template("final2.html")


@app.route('/predict',methods=["POST"])
def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)
    
    payload_scoring = {"input_data": [{"field": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f17","f18","f19","f20","f21","f22","f23","f24","f25","f26","f27","f28","f29"]], "values": check_predic}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e9cb62f7-175a-47e1-ab52-d5f3021adbfe/predictions?version=2022-11-15', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    
    prediction=(response_scoring.json())
    

   
    predic=prediction['predictions'][0]['values'][0][0]

    
    if(predic==-1):
        pred = "You are safe!! This is a Legimate Website :)"
    elif(predic==1):
        pred = "You are in a phishing site. Dont Trust :("
    else:
        pred = "You are in a suspecious site. Be Cautious ;("

    return render_template("final2.html", pred_text = '{}'.format(pred), url = url)


"""@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)
    predic = model.y_predict([np.array(list(data.values()))])
    result = predic[0]
    return jsonify(result)"""

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
