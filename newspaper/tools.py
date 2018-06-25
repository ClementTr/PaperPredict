import pandas as pd
from sklearn.externals import joblib
import smtplib
import os
import email.message

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
    server = smtplib.SMTP('smtp.gmail.com:587')
    gmail_user = 'filrouge.newspaper@gmail.com'
    gmail_password = 'bestteamever'
    prenom=row['prenom']
    nom=row['nom']
    sent_from = gmail_user
    email_content = """
<html>

<head>
<meta http-equiv="Content-Type" content="text/html charset=utf-8">

   <title>Livraison du 26 Juin 2018</title>
   <style type="text/css">
    a {color: #d80a3e}
  body, #header h1, #header h2, p {margin: 0 padding: 0}
  #main {border: 1px solid #cfcece}
  img {display: block}
  #top-message p, #bottom p {color: #3f4042 font-size: 12px font-family: Arial, Helvetica, sans-serif }
  #header h1 {color: #ffffff !important font-family: "Lucida Grande", sans-serif font-size: 24px margin-bottom: 0!important padding-bottom: 0 }
  #header p {color: #ffffff !important font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif font-size: 12px  }
  h5 {margin: 0 0 0.8em 0}
    h5 {font-size: 18px color: #444444 !important font-family: Arial, Helvetica, sans-serif }
  p {font-size: 12px color: #444444 !important font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif line-height: 1.5}
  .bigger { font-size:28 }
   </style>

   <style>
   /* #logo {
     position: absolute
     left: 50px
     top: 0px
   } */
   </style>
</head>

<body>


<table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
    <tr>
      <td>
        <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="d80a3e">
          <tr>
            <td align="left">  <img id='logo' src="https://gust-production.s3.amazonaws.com/uploads/startup/logo_image/621565/Logo_Transparent_No_Name_Square.png" width="120" height="120"></td>
            <td width="570" align="left"  bgcolor="#d80a3e"><h1>Bonjour, %s %s  </h1></td>
          </tr>
          <tr>
            <td width="570" align="right" bgcolor="#d80a3e"><p>26 Juin 2018</p></td>
          </tr>
        </table>
      </td>
    </tr>

    <tr>
      <td>
        <table id="content-3" cellpadding="0" cellspacing="0" align="center">
          <tr>
            <table id="content-3" cellpadding="0" cellspacing="0" align="center">
              <tr>

            <h3>Previsions de ventes:</h3>
            <p>Pour le 27 Juin 2018, la quantite de journaux a delivrer est de: <span class='bigger'>28</span> .  </p>
            <p>   </p>
            <p>Amicalement,   </p>
            <p>La TEAM: Badr, Yrieix, Baptiste et Clement   </p>

          </tr>

        </table>


            </td>



          </tr>

        </table>
      </td>
    </tr>
    <tr>
      <td>

      </td>
    </tr>

  </table>

</td></tr></table><!-- wrapper -->

</body>
</html>



"""  % (prenom, nom)

    msg = email.message.Message()
    msg['Subject'] = 'Prevision de ventes de journaux pour le 26 Juin 2018'



    password = "bestteamever"
    msg['From'] = "filrouge.newspaper@gmail.com"
    msg['To'] = row['mail']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        # Login Credentials for sending the mail
        s.login(msg['From'], password)

        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        print('Mail envoye a'+prenom+nom)
    except:
        print("Envoie echoue a"+prenom+nom)
