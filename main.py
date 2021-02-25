from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn import metrics
app = Flask(__name__)
# model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
model = load('OrthogonalMatchingPursuit_model.joblib')
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
#         Year = int(request.form['Year'])
#         Present_Price=float(request.form['Present_Price'])
#         Kms_Driven=int(request.form['Kms_Driven'])
#         Kms_Driven2=np.log(Kms_Driven)
#         Owner=int(request.form['Owner'])
#         Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
#         if(Fuel_Type_Petrol=='Petrol'):
#                 Fuel_Type_Petrol=1
#                 Fuel_Type_Diesel=0
#         else:
#             Fuel_Type_Petrol=0
#             Fuel_Type_Diesel=1
#         Year=2020-Year
#         Seller_Type_Individual=request.form['Seller_Type_Individual']
#         if(Seller_Type_Individual=='Individual'):
#             Seller_Type_Individual=1
#         else:
#             Seller_Type_Individual=0	
#         Transmission_Mannual=request.form['Transmission_Mannual']
#         if(Transmission_Mannual=='Mannual'):
#             Transmission_Mannual=1
#         else:
#             Transmission_Mannual=0
#         prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        val_dict = {
    'Year':int(request.form['Year']),
    'Present_Price':float(request.form['Present_Price']),
    'Kms_Driven':int(request.form['Kms_Driven']),
    'Fuel_Type':request.form['Fuel_Type_Petrol'],
    'Seller_Type':request.form['Seller_Type_Individual'],
    'Transmission':request.form['Transmission_Mannual'],
    'Owner':int(request.form['Owner']),
}
    
        testdf = pd.DataFrame([val_dict])
        for col in ['Fuel_Type','Seller_Type','Transmission',]:
            dummies = pd.get_dummies(testdf[col], prefix=col)
            testdf = pd.concat([testdf, dummies], axis=1)    
        testdf['age'] = 2020 - testdf.Year

        dropcols = ['Year']+['Fuel_Type','Seller_Type','Transmission',]
        testdf.drop(dropcols, axis=1, inplace=True)

        columns = ['Present_Price', 'Kms_Driven', 'Owner', 'Fuel_Type_CNG',
               'Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Seller_Type_Dealer',
               'Seller_Type_Individual', 'Transmission_Automatic',
               'Transmission_Manual', 'age']
        testdf = testdf.align(pd.DataFrame([], columns=columns), fill_value =0)[0]
        tpoint = testdf[columns].values        
        prediction = model.predict(tpoint2)
        
        
        
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

