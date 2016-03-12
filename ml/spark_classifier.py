import numpy as numpy
import sklearn
import sklearn.ensemble
import sklearn.linear_model
import sklearn.naive_bayes
import pandas
from sklearn import grid_search

import os
import sys
import csv
import math

def forest_classifier(features,train,n_trees=1,cv_folds=2):
	model = sklearn.ensemble.RandomForestClassifier(n_estimators=n_trees)
	scores = sklearn.cross_validation.cross_val_score(model, train[features], train["pass/fail"], cv=cv_folds)
	print "Forest. Average Score over {0} folds is: {1}".format(cv_folds,scores.mean())
	model.fit(train[features],train["pass/fail"])
	return {"model":model,"cv_score":scores.mean()}

def logistic_classifier(features,train,cv_folds=2):
	model = sklearn.linear_model.LogisticRegression()
	scores = sklearn.cross_validation.cross_val_score(model, train[features], train["pass/fail"], cv=cv_folds)
	print "Logistic. Average Score over {0} folds: {1}".format(cv_folds, scores.mean())
	model.fit(train[features],train["pass/fail"])
	return {"model":model,"cv_score":scores.mean()}

def bayes_classifier(features,train,cv_folds=2):
	model = sklearn.naive_bayes.BernoulliNB()
	scores = sklearn.cross_validation.cross_val_score(model, train[features], train["pass/fail"], cv=cv_folds)
	print "Logistic. Average Score over {0} folds: {1}".format(cv_folds, scores.mean())
	model.fit(train[features],train["pass/fail"])
	return {"model":model,"cv_score":scores.mean()}

def grid_search(features,train,predict,cv_folds=2):
	models = {
	    "linear":(sklearn.linear_model.LogisticRegression(),[{'C':[0.01,.1,.5]}]),
	    "tree":(sklearn.ensemble.RandomForestClassifier(),[{'n_estimators':[1,5,10]}]),
	    "bayes":(sklearn.naive_bayes.BernoulliNB(),[{'alpha':[0,0.5,1.0]}])
	}

	# best_models = []
	# best_scores = []
	grid_searches = {}
	for model_name,model_info in models.iteritems():
		model = model_info[0]
		params = model_info[1]
		grid_model = sklearn.grid_search.GridSearchCV(model,params,verbose=5,n_jobs=1,cv=cv_folds)
		grid_model.fit(train[features], train["pass/fail"])
		grid_searches[model_name] = grid_model

    	# print("Our best score here:", grid_model.best_score_)
    	# print("Our best params here:",grid_model.best_params_)
    	# best_scores.append(grid_model.best_score_)
    	# best_models.append(grid_model)

	best_model = None
	best_score = 0
	for name,gs in grid_searches.iteritems():
		print "Model: " + name + ", Best Score: " + str(gs.best_score_)
		if gs.best_score_ > best_score:
			best_score = gs.best_score_
			best_model = gs.best_estimator_
	print "Best Model {0}".format(best_model)
	return {"model":best_model,"cv_score":best_score}

	# print best_scores
	# return best_models[numpy.argmax(best_scores)]

def grid_search_spark(sc,features,train,predict,cv_folds=2):
	import spark_sklearn
	models = {
	    "linear":(sklearn.linear_model.LogisticRegression(),[{'C':[0.01,.1,.5]}]),
	    "tree":(sklearn.ensemble.RandomForestClassifier(),[{'n_estimators':[1,2,4,8]}]),
	    "bayes":(sklearn.naive_bayes.BernoulliNB(),[{'alpha':[0,0.5,1.0]}])
	}

	best_models = []
	best_scores = []
	grid_searches = {}
	for model_name,model_info in models.iteritems():
		model = model_info[0]
		params = model_info[1]
		grid_model = spark_sklearn.GridSearchCV(sc,model,params,verbose=5,cv=cv_folds)
		grid_model.fit(train[features], train["pass/fail"])
		grid_searches[model_name] = grid_model

	best_model = None
	best_score = 0
	for name,gs in grid_searches.iteritems():
		print "Model: " + name + ", Best Score: " + str(gs.best_score_)
		if gs.best_score_ > best_score:
			best_score = gs.best_score_
			best_model = gs.best_estimator_
	print "Best Model {0}".format(best_model)
	return {"model":best_model,"cv_score":best_score}

	# print best_scores
	# return best_models[numpy.argmax(best_scores)]

def predict(model_info,predict_data,features):
	model = model_info["model"]
	predictions = model.predict(predict_data[features])
	result = pandas.DataFrame({
		"test_name": predict_data["test_name"],
		"actual": predict_data["pass/fail"],
		"prediction": predictions
	})
	print result

	correct = [i for i, j in zip(predict_data["pass/fail"], predictions) if i == j]
	pct_correct = (float(len(correct))/len(predictions))
	print ("Percent Correct %f" % pct_correct)
	model_info["pct_correct"] = pct_correct

def classify(test_csv,pct_train,classifier,sc=None):
	all_data = pandas.read_csv(test_csv)
	end_train = int(math.floor(pct_train * len(all_data)))
	train_data = all_data[:end_train]
	predict_data = all_data[end_train:]
	headers = list(all_data.columns.values)
	features = headers[1:-1]

	model_info = None
	if classifier == "tree":
		model_info = forest_classifier(features,train_data)
	elif classifier == "linear":
		model_info = logistic_classifier(features,train_data)
	elif classifier == "bayes":
		model_info = bayes_classifier(features,train_data)
	elif classifier == "grid":
		model_info = grid_search(features,train_data,predict_data)
	elif classifier == "spark":
		model_info = grid_search_spark(sc,features,train_data,predict_data)
	else:
		print "ERROR. Classifier <{0}> not supported".format(classifier)

	predict(model_info,predict_data,features)
	test_name = (test_csv.split(".")[0]).split("/")[1]
	return [test_name,model_info["cv_score"],model_info["pct_correct"]]

def main():
	input_dir,pct_train,classifier = None,None,None
	try:
		input_dir = sys.argv[1]
		pct_train = float(sys.argv[2])
		classifier = sys.argv[3]
	except:
		print "ERROR, Usage: python classifier.py <input_dir> <pct_train> <classifier>"
		print "\t<input_dir> Directory containing test case csv's"
		print "\t<pct_train> Percentage of csv to use as training data (0,1)"
		print "\t<classifier> Type of classifier to use: tree, linear, bayes, grid, spark"
		print "\t<To use spark: spark-submit classifier.py <input_dir> <pct_train> spark"
		exit(1)

	sc = None
	if classifier == "spark":
		from pyspark import SparkContext
		sc = SparkContext("local","Metric Classifier")

	with open("classifier_results.csv", "w") as csvOutput:
		writer = csv.writer(csvOutput, delimiter=',', quotechar='"')
		writer.writerow(["feature_name","model_score","percent_correct"])
		for test_file in os.listdir(input_dir):
			if test_file.endswith(".csv"):
				test_csv = "{0}/{1}".format(input_dir,test_file)
				result_row = classify(test_csv,pct_train,classifier,sc)
				print result_row
				writer.writerow(result_row)

if __name__ == "__main__":
    main()