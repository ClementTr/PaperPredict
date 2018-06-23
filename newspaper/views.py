from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaulttags import register
from django.template import loader
from django.urls import reverse
import pandas as pd
import numpy as np
import pickle
import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adleads.settings")
from .tools import predict, send_email, construct_maildf


def home(request):
    if (request.method == "POST"):
        return redirect("france/")
    if (request.method == "POST"):
        return redirect("presentation/")
    return render(request, 'newspaper/home.html')

def presentation(request):
    return render(request, 'newspaper/presentation.html')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def france(request):
    if (request.method == "POST"):
        departement_choose = request.POST.get('getDept')
        code_departement_choose = departement_choose[:2]
        name_departement_choose = departement_choose[5:]
        return redirect(str(code_departement_choose) + "/")

    ''' Dictionnaire des régions '''
    path_dict_reg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/dict_regions.pickle')
    with open(path_dict_reg, 'rb') as handle: dict_regions = pickle.load(handle)

    ''' Dictionnaire des départements '''
    path_dict_dept = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/dict_departement.pickle')
    with open(path_dict_dept, 'rb') as handle: dict_departement = pickle.load(handle)

    ''' Contexte '''
    context = {'dict_regions': dict_regions, 'dict_departement': dict_departement}

    return render(request, 'newspaper/france.html', context)


def departement(request, code_dept):
    if (request.method == "POST"):
        ville_choose = request.POST.get('getVille')
        print(ville_choose)
        return redirect(str(ville_choose) + "/")

    ''' List des départements ordonnée '''
    path_dict_dept = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/dict_departement.pickle')
    with open(path_dict_dept, 'rb') as handle: dict_departement = pickle.load(handle)
    nom_departement = dict_departement[code_dept]
    path_df_dept_ville = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/df_dept_ville.csv')
    df_dept_ville = pd.read_csv(path_df_dept_ville)
    list_ville_spec_dept = df_dept_ville[df_dept_ville["code_dept"] == int(code_dept)]["Ville"].ravel()
    list_ville_spec_dept.sort()

    ''' Json de la somme des ventes pour un département donné par jour '''
    path_reg_days = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/df_reg_days.csv')
    df_reg_days = pd.read_csv(path_reg_days, dtype=object)
    df_reg_days = df_reg_days[["code_dept", "Sales", "Delivered", "Day"]].groupby(["code_dept", "Day"]).sum().reset_index()
    df_specreg_days = df_reg_days[(df_reg_days["code_dept"] == code_dept)
                                & (df_reg_days["Day"] != "Dimanche")][["Day", "Sales"]]
    df_specreg_days["Sales"] = pd.to_numeric(df_specreg_days["Sales"], downcast='signed')
    df_specreg_days["Hex"]  = ["#B8381F", "#EAD352", "#3D4477",
                            "#539D99", "#FDEF97", "#375F35"][:len(df_specreg_days)]
    list_js = df_specreg_days.astype(object).to_dict(orient='records')
    list_js = json.dumps(list_js);

    ''' Stats descriptives par département '''
    dict_name = ['dict_dept_Delivered_max.pickle', 'dict_dept_Delivered_mean.pickle',
                 'dict_dept_Delivered_min.pickle', 'dict_dept_Sales_max.pickle',
                 'dict_dept_Sales_mean.pickle', 'dict_dept_Sales_min.pickle']
    dict_del_sales = {}
    for dn in dict_name:
        path_dict_dept = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/newspaper/data/", dn)
        with open(path_dict_dept, 'rb') as handle: dict_del_sales[dn[10:-7]] = pickle.load(handle)

    ''' Sales / Deliveries d3'''
    path_df_dept_sales_deliveries = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/newspaper/data/df_dept_sales_deliveries.csv")
    df_dept_sales_deliveries = pd.read_csv(path_df_dept_sales_deliveries, dtype=object)
    json_dept_sales_deliveries = df_dept_sales_deliveries[df_dept_sales_deliveries["code_dept"] == code_dept][["Sales", "Date", "Delivered"]].to_json(orient='records')
    json_dept_sales_deliveries = json.dumps(json_dept_sales_deliveries)

    ''' SPEEDOMETER RUPTURES '''
    path_df_dept_ruptures = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/newspaper/data/df_ruptures_dept.csv")
    df_dept_ruptures = pd.read_csv(path_df_dept_ruptures, dtype=object)
    mean_ruptures_val = df_dept_ruptures[df_dept_ruptures["code_dept"] == "D"+code_dept]["Ruptures_mean"].values[0]
    mean_ruptures_val = round(float(mean_ruptures_val), 2)

    ''' PIECHART SEGMENTS '''
    path_df_dept_segments = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/newspaper/data/df_dept_segments.csv")
    df_dept_segments = pd.read_csv(path_df_dept_segments, dtype=object)
    seg_serie = df_dept_segments[df_dept_segments["code_dept"] == "D" + code_dept]["Segment"].value_counts() / np.sum(df_dept_segments[df_dept_segments["code_dept"] == "D" + code_dept]["Segment"].value_counts())
    print(seg_serie)
    df_dept_spec_segments = pd.DataFrame({"Segment": seg_serie.index.tolist(), "Value": seg_serie.values.tolist()})
    json_dept_spec_segments = json.dumps(df_dept_spec_segments.to_json(orient="records"))

    ''' Contexte '''
    context = {'code_dept': code_dept, 'nom_departement': nom_departement,
               'list_ville_spec_dept': list_ville_spec_dept, 'list_js': list_js,
               'dict_sales_min': dict_del_sales['Sales_min'],
               'dict_sales_max': dict_del_sales['Sales_max'],
               'dict_sales_mean': dict_del_sales['Sales_mean'],
               'dict_deliveries_min': dict_del_sales['Delivered_min'],
               'dict_deliveries_max': dict_del_sales['Delivered_max'],
               'dict_deliveries_mean': dict_del_sales['Delivered_mean'],
               'json_dept_sales_deliveries': json_dept_sales_deliveries,
               'mean_ruptures_val': mean_ruptures_val, 'json_dept_spec_segments': json_dept_spec_segments}

    return render(request, 'newspaper/departement.html', context)


def ville(request, code_dept, nom_ville):
    ''' Dictionnaire des départements '''
    path_dict_dept = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/dict_departement.pickle')
    with open(path_dict_dept, 'rb') as handle: dict_departement = pickle.load(handle)

    ''' DataFrame Kisoques et Villes '''
    path_df_kioques_villes = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/newspaper/data/df_kioques_villes.csv')
    df_kioques_villes = pd.read_csv(path_df_kioques_villes, dtype=object)
    df_kioques_villes_spec = df_kioques_villes[df_kioques_villes['Ville'] == nom_ville]
    list_df_values = []
    for i in range(len(df_kioques_villes_spec)):
        list_df_values.append(df_kioques_villes_spec.iloc[i].tolist())

    ''' Context '''
    nom_departement = dict_departement[code_dept]
    context = {'code_dept': code_dept, 'nom_ville': nom_ville, 'nom_departement': nom_departement,
               'list_df_values': list_df_values}
    return render(request, 'newspaper/ville.html', context)


def predictor(request):
    context = {}
    return render(request,  'newspaper/predictor.html', context)


def compute(request):
    if request.method == 'GET':
        algo = request.GET.get('algorithm')
        nb_weeks = request.GET.get('nb_weeks')
        start = request.GET.get('start')

        path = os.path.dirname(os.path.realpath(__file__))
        if predict(path, algo, start, nb_weeks):
            print('\n\n JSON File Saved \n\n')

    return redirect('/predictor/results'+'/')


def results(request):
    if (request.method == "POST"):

        df_mails = construct_maildf()
        test= df_mails.loc[[32,3,53,62],:]
        gmail_user = 'filrouge.newspaper@gmail.com'
        gmail_password = 'bestteamever'

        for _, row in test.iterrows(): #remplacer test par df_mails pour l'envoyer à tout le monde
            send_email(row)



        return redirect('/predictor/results')



    context = {}

    return render(request,  'newspaper/results.html', context)
