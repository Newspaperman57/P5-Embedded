from sklearn.externals import joblib


def save_model(model, filepath):
    if ".pkl" not in filepath:
        joblib.dump(model, "{}.pkl".format(filepath))
    else:
        joblib.dump(model, filepath)


def load_mode(filepath):
    return joblib.load(filepath)