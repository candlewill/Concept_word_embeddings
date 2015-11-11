import numpy as np
import math
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn import neighbors
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from load_data import load_embeddings
from load_data import load_vader
from load_data import load_pickle
from save_data import dump_picle
from log_manager import log_state, log_performance


def build_docvecs(model, ratings):
    nb_text = len(ratings)  # 4200
    size = len(model.docvecs['L_SENT_0'])  # 50
    vecs = [model.docvecs['L_SENT_%s' % id].reshape((1, size)) for id in range(nb_text)]
    dump_picle((np.concatenate(vecs), ratings), './data/acc/twitter_docvecs.p')


def run_build_docvecs():
    model = load_embeddings('twitter')
    print(model.docvecs[0])
    print(model.docvecs['L_SENT_4'])
    _, ratings = load_vader('./resource/tweets.txt')

    # Do not account the 1240 and 3516 -th item
    r = ratings[:1240] + ratings[1241:3516] + ratings[3517:]

    build_docvecs(model, r)


def evaluate(true, pred, msg):
    true, pred = np.array(true), np.array(pred)
    MAE = mean_absolute_error(np.array(true), np.array(pred))
    MSE_sqrt = math.sqrt(mean_squared_error(np.array(true), np.array(pred)))
    MSE = mean_squared_error(np.array(true), np.array(pred))
    R2 = r2_score(np.array(true), np.array(pred))
    Pearson_r = pearsonr(np.array(true), np.array(pred))
    Spearman_r = spearmanr(np.array(true), np.array(pred))
    log_state(msg)
    log_performance(MSE, MAE, Pearson_r, R2, Spearman_r, MSE_sqrt)
    return None


def linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='ordinary_least_squares'):
    if cost_fun == 'ordinary_least_squares':
        regr = linear_model.LinearRegression()
    elif cost_fun == 'Ridge_Regression':
        regr = linear_model.Ridge(alpha=1)
    elif cost_fun == 'Bayesian_Regression':
        regr = linear_model.BayesianRidge()
    elif cost_fun == 'SVR':
        regr = SVR(C=1.0, epsilon=0.2, kernel='linear')
    elif cost_fun == 'KNN_Reg':
        regr = neighbors.KNeighborsRegressor(5, weights='distance')
    else:
        raise Exception('The type of cost function is not specified.')

    # Train the model using the training sets
    regr.fit(X_train, Y_train)
    predict = regr.predict(X_test)
    # record the experiment performance, Explained variance score: 1 is perfect prediction
    np.seterr(invalid='ignore')
    print(list(predict)[:100])
    print(Y_test[:100])
    evaluate(list(predict), np.array(Y_test),
             'linear regression ' + 'Explained variance score: %.2f' % regr.score(X_test, Y_test))


def cv(data, target):
    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(data, target, test_size=0.2, random_state=10)
    linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='ordinary_least_squares')
    linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='Ridge_Regression')
    linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='Bayesian_Regression')
    linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='SVR')
    linear_regression_multivariant(X_train, X_test, Y_train, Y_test, cost_fun='KNN_Reg')


if __name__ == "__main__":
    run_build_docvecs()  # only at the first time, you should run this
    X, Y = load_pickle('./data/acc/twitter_docvecs.p')
    Y = np.array(Y) + np.ones(len(Y), dtype=float) * 5
    cv(X, Y)
