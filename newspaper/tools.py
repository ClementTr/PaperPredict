import pandas as pd
from sklearn.externals import joblib

def load_data(start, path):
    """Load the test set.
        Ideally would have loaded the full data 
        to create train/test sets and returned 
        both df.
    """

    input_file = path + 'x_test.pkl' #
    df = pd.read_pickle(input_file)
    return df

def load_regressor(path, algo='RF'):
    """Load the given pretrained regressor.
        Ideally would have return the regressor 
        freshly trained.    
    """
    reg_file = path
    
    if algo in ['RF', 'AD']:
        reg_file += algo + '.pkl'
        reg = joblib.load(reg_file)
        return reg
    else:
        print('Algorithm unknown.')
    


def predict(path, algo, start, nb_weeks):
    
    path += '/static/newspaper/data/'
    x_test = pd.read_pickle(path + 'x_test.pkl')
    reg = load_regressor(path, algo)
    y_pred = reg.predict(x_test)

    del x_test, reg
    
    y_test = pd.read_pickle(path + 'y_test.pkl')
    y_test['Predictions'] = y_pred

    end_date = pd.to_datetime(start) + pd.Timedelta(int(nb_weeks)*7, unit='d')

    y_test = y_test[:end_date]

    y_test.to_json(path + 'predictions.json', orient='records')
    return True