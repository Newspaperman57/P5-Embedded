import numpy as np
from sklearn import svm
from train import train

result = train([("grundberg2.csv", [0, 1]), ("morten2.csv", [1, 0])])

tester = process_data("mortenvsgrunberg_rematch.csv")[0]

tester2 = process_data("grunbergvsmorten_rematch.csv")[0]

tester3 = process_data("mortenvsgrunberg.csv")[0]

tester4 = process_data("grunbergvsmorten.csv")[0]

clf = svm.SVC()
clf.fit(result[0], result[1]);



#http://scikit-learn.org/stable/modules/svm.html

# should be 1 for morten
pred1 = clf.predict_proba(tester)

guess = calculate_accuracy(pred1)
print "expected [1 0]"
print guess

pred2 = clf.predict_proba(tester2)
guess2 = calculate_accuracy(pred2)
print "expected [0 1]"
print guess2

pred3 = clf.predict_proba(tester3)
guess3 = calculate_accuracy(pred3)
print "expected [1 0]"
print guess3

pred4 = clf.predict_proba(tester4)
print "expected [0 1]"
guess4 = calculate_accuracy(pred4)
print guess4

print "Do you want to save this model?"
user_input = raw_input("(yes / no)")
if "yes" in user_input:
    save_model(clf, raw_input("enter path: "))