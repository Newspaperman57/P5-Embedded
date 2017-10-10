from sklearn.neural_network import MLPClassifier


class Classifier:
    def __init__(self):
        self.clf = MLPClassifier(solver='lbfgs', verbose=True, tol=1e-10, hidden_layer_sizes=(100), max_iter=1000000, random_state = 0, activation = "logistic")

    def learn(self, train, labels):
        print len(train[0])
        self.clf.fit(train, labels)
        return self.clf