import numpy as numpy
import sklearn
import sklearn.ensemble
import sklearn.linear_model
import pandas
from sklearn import grid_search

import spark_sklearn
from spark_sklearn import GridSearchCV
from pyspark import SparkContext

import os
import sys
import csv
import math

sc = SparkContext("local","Metric Classifier")

test_csv = sys.argv[1]
pct_train = float(sys.argv[2])

all_data = pandas.read_csv(test_csv)
end_train = int(math.floor(pct_train * len(all_data)))
train_data = all_data[:end_train]
predict_data = all_data[end_train:]
headers = list(all_data.columns.values)
features = headers[1:-1]
print "Features: features"

def forest_classifier(features,train):
	model = sklearn.ensemble.RandomForestClassifier(n_estimators=5)
	scores = sklearn.cross_validation.cross_val_score(model, train[features], train["pass/fail"], cv=2)
	print("Forest. Average Score over 3 folds is:", scores.mean())
	model.fit(train[features],train["pass/fail"])
	return model

def logistic_classifier(features,train):
	model = sklearn.linear_model.LogisticRegression()
	scores = sklearn.cross_validation.cross_val_score(model, train_data[features], train["pass/fail"], cv=2)
	print("Logistic. Average Score over 3 folds:", scores.mean())
	model.fit(train[features],train["pass/fail"])
	return model

def grid_search(sc,features,train,predict):
	models = [
	    (sklearn.linear_model.LogisticRegression(),[{'C':[0.01,.1,.5]}]),
	    (sklearn.ensemble.RandomForestClassifier(),[{'n_estimators':[1,5,10]}])
	]
	best_models = []
	best_scores = []
	for model_info in models:
		model = model_info[0]
		params = model_info[1]
		grid_model = spark_sklearn.GridSearchCV(sc,model,params)
		grid_model.fit(train[features], train["pass/fail"])

    	print("Our best score here:", grid_model.best_score_)
    	print("Our best params here:",grid_model.best_params_)
    	best_scores.append(grid_model.best_score_)
    	best_models.append(grid_model)

	return best_models[numpy.argmax(best_scores)]
	# predictions = final_model.predict(predict[features])
	# print predictions

def predict(model,predict_data,features):
	predictions = model.predict(predict_data[features])
	result = pandas.DataFrame({
		"test_name": predict_data["test_name"],
		"actual": predict_data["pass/fail"],
		"prediction": predictions
	})
	print result

	correct = [i for i, j in zip(predict_data["pass/fail"], predictions) if i == j]
	print ("Percent Correct %f" % (float(len(correct))/len(predictions)))

#best_model = forest_classifier(features,train_data)
#best_model = logistic_classifier(features,train_data)
best_model = grid_search(sc,features,train_data,predict_data)
predict(best_model,predict_data,features)