import pandas as pd
from sklearn.externals import joblib
import smtplib
import os

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



mailing_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/mailinglist.txt')

def construct_maildf():

    f= open(mailing_path, "r")
    mails = f.read()

    mails = mails.split(',')

    df_mails = pd.DataFrame()



    df_mails['mail']= mails
    df_mails['prenom']=''
    df_mails['nom']= ''



    for i in range(0,len(df_mails)):
        if '<' in df_mails['mail'][i]:
            df_mails['prenom'].iloc[i]= df_mails['mail'][i].split('<')[0].strip().split(' ')[0]
            df_mails['nom'].iloc[i]= df_mails['mail'][i].split('<')[0].strip().split(' ')[1]
            df_mails['mail'].iloc[i]= df_mails['mail'][i].split('<')[1].split('>')[0]

        else:
            df_mails['prenom'].iloc[i]= df_mails['mail'][i].split('@')[0].split('.')[0]
            try:
                df_mails['nom'].iloc[i]= df_mails['mail'][i].split('@')[0].split('.')[1]
            except:
                pass


    df_mails['nom'] = df_mails['nom'].str.upper()
    df_mails['prenom'] = df_mails['prenom'].str.lower()
    df_mails['mail']= df_mails['mail'].str.replace('\n','')

    df_mails['prenom'] = df_mails['prenom'].apply(lambda x: x.title())

    #correction
    df_mails.loc[6,'prenom']= 'Antoine'
    df_mails.loc[53,'prenom']= 'Clement'
    df_mails.loc[8,['prenom','nom']]= ['Chris','Belinguier']
    df_mails.loc[22,'nom']= 'DE TRUCHIS'
    df_mails.loc[43,['prenom','nom']]= ['Marie','RANCHET']
    df_mails.loc[35,['prenom','nom']]= ['Arianne','MANINTCHAP']

    #ajout d'adresse mails

    df_mails.loc[59,:]= ['stephan.clemencon@telecom-paristech.fr','Stephan', 'CLEMENÇON' ]
    df_mails.loc[60,:]= ['marc.hispa@bearingpoint.com','Marc', 'HISPA' ]
    df_mails.loc[61,:]= ['olivier.fercoq@telecom-paristech.fr','Olivier', 'FERCOQ' ]
    df_mails.loc[62,:]= ['badr.ghazlane@telecom-paristech.fr','Badr', 'GHAZLANE' ]

    return df_mails





def send_email(row):
    gmail_user = 'filrouge.newspaper@gmail.com'
    gmail_password = 'bestteamever'
    prenom=row['prenom']
    nom=row['nom']
    sent_from = gmail_user
    to = row['mail']
    subject = 'Livraison journaux 25 Juin 2018'
    body = '''Bonjour %s %s, \n
    Nous tenons a vous informer qu'au vu de nos previsions, %s journaux seront livres en Ile-de-France \n\n Bonne journee ! '''  % (prenom,nom, '8')

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
