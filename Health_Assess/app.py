# Importing essential libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from PIL import Image
import tensorflow as tf


app = Flask(__name__)
app.secret_key = 'O.\x89\xcc\xa0>\x96\xf7\x871\xa2\xe6\x9a\xe4\x14\x91\x0e\xe5)\xd9'

# Load the Random Forest CLassifier model
filename = 'Models/diabetes-model.pkl'

classifier = pickle.load(open(filename, 'rb'))

usernamearr = [];
passwordarr = [];

@app.route('/Login', methods=['GET', 'POST'])
def login():
      # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        for i in usernamearr:
            for j in passwordarr:
                if i == username and j == password:
                    print("username",username,password)
                    return redirect(url_for('home'))
                else:
                    msg = "Kindly check login credentials"
                
        if username == 'kewal' and password == '123456':
            msg = "Login sucessful"
            return redirect(url_for('home'))
        else:
            msg = "Kindly check login credentials"
    return render_template('user_login.html')

@app.route('/RegUser', methods=['GET', 'POST'])	
def user_register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        pname = request.form['pname']
        page = request.form['page']
        pcontact = request.form['p_contact']
        usernamearr.append(username)
        passwordarr.append(password)
        print(usernamearr)
        print(passwordarr)
        print('You have successfully registered!Clik on login button to proceed')
        msg = "You have successfully registered!Clik on login button to proceed"
        return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('user_register.html')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    if request.method == 'POST':
        try:
            preg = int(request.form['pregnancies'])
            glucose = int(request.form['glucose'])
            bp = int(request.form['bloodpressure'])
            st = int(request.form['skinthickness'])
            insulin = int(request.form['insulin'])
            bmi = float(request.form['bmi'])
            dpf = float(request.form['dpf'])
            age = int(request.form['age'])

            data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
            my_prediction = classifier.predict(data)

            return render_template('d_result.html', prediction=my_prediction)
        except ValueError:
            flash(
                'Invalid input. Please fill in the form with appropriate values', 'info')
            return redirect(url_for('diabetes'))



def ValuePredictor(to_predict_list, size):
    loaded_model = joblib.load('models/heart_model')
    to_predict = np.array(to_predict_list).reshape(1, size)
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/heart')
def heart():
    return render_template('heart.html')


@app.route('/predict_heart', methods=['POST'])
def predict_heart():

    if request.method == 'POST':
        try:
            to_predict_list = request.form.to_dict()
            to_predict_list = list(to_predict_list.values())
            to_predict_list = list(map(float, to_predict_list))
            result = ValuePredictor(to_predict_list, 11)

            if(int(result) == 1):
                prediction = 1
            else:
                prediction = 0

            return render_template('h_result.html', prediction=prediction)
        except ValueError:
            flash(
                'Invalid input. Please fill in the form with appropriate values', 'info')
            return redirect(url_for('heart'))


# this function use to predict the output for Fetal Health from given data





def strokeValuePredictor(s_predict_list):
    '''function to predict the output by data we get
    from the route'''

    model = joblib.load('Models/stroke_model.pkl')
    data = np.array(s_predict_list).reshape(1, -1)
    result = model.predict(data)
    return result[0]


@app.route('/stroke')
def stroke():
    return render_template('stroke.html')


@app.route('/predict_stroke', methods=['POST'])
# this route for predicting chances of stroke
def predict_stroke():

    if request.method == 'POST':
        s_predict_list = request.form.to_dict()
        s_predict_list = list(s_predict_list.values())
        # list to keep the values of the dictionary items of request.form field
        s_predict_list = list(map(float, s_predict_list))
        result = strokeValuePredictor(s_predict_list)

        if(int(result) == 1):
            prediction = 1
        else:
            prediction = 0
        return render_template('st_result.html', prediction=prediction)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
