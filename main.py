import argparse
import os 
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import pandas as pd 
from utils.prep_data import PrepareData
import matplotlib.pyplot as plt


def LinearReg(X_train, X_test, y_train, y_test, model_dir):
    lr = LinearRegression()
    lr.fit(X_train,y_train)
    y_pred_lr = lr.predict(X_test)
    R2_Score_lr = round(r2_score(y_pred_lr,y_test) * 100, 2)
    # save the model to disk
    filename = os.path.join(model_dir, 'LR_model.sav')
    pickle.dump(lr, open(filename, 'wb'))
    print("R2 Score : ",R2_Score_lr,"%")
    
def RandomForestReg(X_train, X_test, y_train, y_test, model_dir):
    rfr = RandomForestRegressor()
    rfr.fit(X_train,y_train)
    y_pred_rfr = rfr.predict(X_test)
    R2_Score_rfr = round(r2_score(y_pred_rfr,y_test) * 100, 2)
    filename = os.path.join(model_dir, 'RF_model.sav')
    pickle.dump(rfr, open(filename, 'wb'))
    print("R2 Score : ",R2_Score_rfr,"%")

def DecisionTreeReg(X_train, X_test, y_train, y_test, model_dir):
    dtr = DecisionTreeRegressor()
    dtr.fit(X_train,y_train)
    y_pred_dtr = dtr.predict(X_test)
    R2_Score_dtr = round(r2_score(y_pred_dtr,y_test) * 100, 2)
    filename = os.path.join(model_dir, 'DT_model.sav')
    pickle.dump(dtr, open(filename, 'wb'))
    print("R2 Score : ",R2_Score_dtr,"%")

def predict(X_test, y_test, filename, res_dir):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    prediction = loaded_model.predict(X_test)
    cross_checking = pd.DataFrame({'Actual' : y_test , 'Predicted' : prediction})
    # Create a line plot
    # Set the figure size
    plt.figure(figsize=(12,6))
    plt.plot(cross_checking['Actual'], color='red', linestyle='--', label ='Actual')
    plt.plot(cross_checking['Predicted'], color='blue', linestyle=':', label ='Predicted')
    plt.legend()
    plt.xlabel('Time point')
    # Set the y axis label of the current axis.
    plt.ylabel('AC power (W)')
    # Set a title of the current axes.
    plt.title('Real-time AC power prediction vs actual')
    # cross_checking.plot(x='Actual', y='Predicted')
    plt.savefig('result/AC_power_prediction.png')
    print(cross_checking.head())
    # Write the result to a JSON file
    cross_checking.head().to_json(os.path.join(res_dir, 'predictions.json'))
   

def main():
    # define input args
    parser = argparse.ArgumentParser(
        description='solar power generation.')
    parser.add_argument(
        "--mode", help="train or predict",
        type=str, required=False, default='train')
    parser.add_argument(
        "--model", help="LinearRegression, RandomForestRegressor, DecisionTreeRegressor",
        type=str, required=False, default='LinearRegression')
    parser.add_argument(
        "--generation-data-loc", help="generation data directory",
        type=str, required=False, default='data/Plant_2_Generation_Data.csv')
    parser.add_argument(
        "--weather-data-loc", help="weather data directory",
        type=str, required=False, default='data/Plant_2_Weather_Sensor_Data.csv')
    parser.add_argument(
        "--model-save-dir", help="the directory to save model",
        type=str, required=False, default='model')
    parser.add_argument(
        "--result-save-dir", help="the directory to save prediction result",
        type=str, required=False, default='result')
    args = parser.parse_args()
    assert args.mode in ['train', 'predict']
    #data preparetion
    generation_data_loc = args.generation_data_loc
    weather_data_loc = args.weather_data_loc
    data = PrepareData(generation_data_loc, weather_data_loc)
    df_solar = data.merge_process()
    X,y = data.get_input(df_solar)
    model_dir = args.model_save_dir
    # data split
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.2,random_state=21)
    if args.mode == "train":
        if args.model == "LinearRegression":
            LinearReg(X_train,X_test,y_train,y_test,model_dir)
        if args.model == "RandomForestRegressor":
            RandomForestReg(X_train,X_test,y_train,y_test,model_dir)
        if args.model == "DecisionTreeRegressor":
            DecisionTreeReg(X_train,X_test,y_train,y_test,model_dir)

    if args.mode == "predict":
        if args.model == "LinearRegression":
            filename = os.path.join(model_dir, 'LR_model.sav')
        if args.model == "RandomForestRegressor":
            filename = os.path.join(model_dir, 'RF_model.sav')
        if args.model == "DecisionTreeRegressor":
            filename = os.path.join(model_dir, 'DT_model.sav')
        predict(X,y, filename, args.result_save_dir)
if __name__ == '__main__':
    main()