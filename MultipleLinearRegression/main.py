from sklearn import linear_model
import pandas as pd
import csv
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

fileName = "acs2015_county_data.csv"
fieldnames = []
with open(fileName, encoding='utf-8') as file:
    line = file.readline()
    line = line[0:len(line)-1].split(",")
    for item in line:
        fieldnames.append(item)
    csvreader = csv.DictReader(file, fieldnames)
    csvData = {
        'IncomePerCap': [],
        'Unemployment': []
    }
    targetData = {
        'ChildPoverty': []
    }
    for row in csvreader:
        for i in range(len(fieldnames)):
            if fieldnames[i] == 'Unemployment' or fieldnames[i] == 'IncomePerCap':
                val = float(row[fieldnames[i]])
                csvData[fieldnames[i]].append(val)
            elif fieldnames[i] == 'ChildPoverty':
                if len(row[fieldnames[i]]) > 0:
                    val = float(row[fieldnames[i]])
                else:
                    val = 0
                targetData["ChildPoverty"].append(val)

    df = pd.DataFrame(csvData)

    target = pd.DataFrame(targetData)

    X = df
    y = target

    lm = linear_model.LinearRegression()
    model = lm.fit(X,y)

    IncomePerCapita = 16824 #enter sample income here
    Unemployment = 17.6 #enter sample unemployment rate here
    Coefficients = lm.coef_
    Intercept = lm.intercept_[0]
    Prediction = Intercept + Coefficients[0][0] * IncomePerCapita + Coefficients[0][1] * Unemployment
    print("An area with an average ${} income per capita and\n"
          "an unemployment rate of {} has a\n"
          "predicted child poverty rate of {}".format(IncomePerCapita, Unemployment, Prediction))