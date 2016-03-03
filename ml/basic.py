import os
import sys
# from pyspark import SparkContext
import numpy as numpy
import csv
import pandas
import sklearn as sk
import sklearn.cluster
import sklearn.ensemble

# def convert_pass_fail(pf):
# 	if pf == "pass":
# 		return 1
# 	else:
# 		return 0

known_test_cases = sys.argv[1]
test_cases = pandas.read_csv(known_test_cases)
# test_cases["pass/fail"].apply(convert_pass_fail)
print test_cases

features = ["longest_1","longest_2","longest_3","longest_4","longest_5"]
model = sklearn.ensemble.RandomForestClassifier(n_estimators=5)
scores = sk.cross_validation.cross_val_score(model, test_cases[features], test_cases["pass/fail"], cv=2)
print("Average Score over 5 folds is:", scores.mean())
model.fit(test_cases[features], test_cases["pass/fail"])

to_predict = sys.argv[2]
tests_to_predict = pandas.read_csv(to_predict)
# tests_to_predict["pass/fail"].apply(convert_pass_fail)
predictions = model.predict(tests_to_predict[features])
print predictions

result = pandas.DataFrame({
	"test_name": tests_to_predict["test_name"],
	"pass": predictions
})

print result
# preds = result.loc[result["pass"] == 1]
# print(preds)