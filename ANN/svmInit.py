from sklearn import svm
from clf import Classifier
from svmInit import svm
from process_data import process_data
from accuracy import calculate_accuracy
from save_model import save_model



# class weight??
def svm(C=1.0, kernel = "rbf", degree = 3, gamma = "auto", coef0 = 0.0, probability = False, shrinking = True, tol = 1e-3, cache_size = 200, class_weight = "??", verbose = False, max_iter = -1, decision_function_shape = "ovr", random_state = None)
	#her kan man fx bare bruge try catch på om input er korrekt