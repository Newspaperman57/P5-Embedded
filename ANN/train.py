from process_data import process_data
from pred_set import Pred_set
from train_helpers import equal_size_train, merge_trains
import numpy as np


def train(input_list):
    tests = list()
    label_dict = {}
    for args in input_list:
        (path, label_list) = args
        label = ''.join(str(nr) for nr in label_list)
        (train, test) = process_data(path)
        test_pred_set = Pred_set(test, label_list)
        if label not in label_dict:
            label_dict[label] = Pred_set(train, label_list)
        else:
            label_dict[label].data = np.concatenate([label_dict[label].data, train])
        tests.append(test_pred_set)
    trains = equal_size_train(label_dict)
    (merged_trains, merged_labels) = merge_trains(trains)
    return (merged_trains, merged_labels, tests)