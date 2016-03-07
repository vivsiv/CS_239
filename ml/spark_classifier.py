import numpy as numpy
import sklearn
import sklearn.ensemble
import sklearn.linear_model
import sklearn.naive_bayes
import pandas
from sklearn import grid_search

# import spark_sklearn
# from spark_sklearn import GridSearchCV
# from pyspark import SparkContext

import os
import sys
import csv
import math

test_csv = sys.argv[1]
pct_train = float(sys.argv[2])
classifier = sys.argv[3]

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

def bayes_classifier(features,train):
	model = sklearn.naive_bayes.BernoulliNB()
	scores = sklearn.cross_validation.cross_val_score(model, train_data[features], train["pass/fail"], cv=2)
	print("Logistic. Average Score over 3 folds:", scores.mean())
	model.fit(train[features],train["pass/fail"])
	return model

def grid_search(features,train,predict):
	models = [
	    (sklearn.linear_model.LogisticRegression(),[{'C':[0.01,.1,.5]}]),
	    (sklearn.ensemble.RandomForestClassifier(),[{'n_estimators':[1,5,10]}]),
	    (sklearn.naive_bayes.BernoulliNB(),[{'alpha':[0,0.5,1.0]}])
	]
	print models
	best_models = []
	best_scores = []
	grid_searches = {}
	for model_info in models:
		model = model_info[0]
		params = model_info[1]
		grid_model = sklearn.grid_search.GridSearchCV(model,params,verbose=5,n_jobs=1,cv=2)
		grid_model.fit(train[features], train["pass/fail"])

    	print("Our best score here:", grid_model.best_score_)
    	print("Our best params here:",grid_model.best_params_)
    	best_scores.append(grid_model.best_score_)
    	best_models.append(grid_model)

    	for params, mean_score, scores in grid_model.grid_scores_:
        	print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))

	print best_scores
	return best_models[numpy.argmax(best_scores)]

def grid_search_spark(sc,features,train,predict):
	models = [
	    (sklearn.linear_model.LogisticRegression(),[{'C':[0.01,.1,.5]}]),
	    (sklearn.naive_bayes.BernoulliNB(),[{'alpha':[0,0.5,1.0]}]),
	    (sklearn.ensemble.RandomForestClassifier(),[{'n_estimators':[1,5,10]}])
	]
	print models
	best_models = []
	best_scores = []
	for model_info in models:
		model = model_info[0]
		params = model_info[1]
		grid_model = spark_sklearn.GridSearchCV(sc,model,params,verbose=5,cv=2)
		grid_model.fit(train[features], train["pass/fail"])

    	print("Our best score here:", grid_model.best_score_)
    	print("Our best params here:",grid_model.best_params_)
    	best_scores.append(grid_model.best_score_)
    	best_models.append(grid_model)

	print best_scores
	return best_models[numpy.argmax(best_scores)]

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

model = None
if classifier == "tree":
	model = forest_classifier(features,train_data)
elif classifier == "linear":
	model = logistic_classifier(features,train_data)
elif classifier == "bayes":
	model = bayes_classifier(features,train_data)
elif classifier == "grid":
	model = grid_search(features,train_data,predict_data)
else:
	import spark_sklearn
	from spark_sklearn import GridSearchCV
	from pyspark import SparkContext 
	sc = SparkContext("local","Metric Classifier")

	model = grid_search_spark(sc,features,train_data,predict_data)

predict(model,predict_data,features)