import requests;

def get_weather():
    url = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action';
    response = requests.get(url, params={'idConc':'27049'})
    tMin = response.json()['predConcello']['listaPredDiaConcello'][0]['tMin'];
    tMax = response.json()['predConcello']['listaPredDiaConcello'][0]['tMax'];
    choiva = response.json()['predConcello']['listaPredDiaConcello'][0]['pchoiva'];
    maña = choiva['manha'];
    tarde = choiva['tarde'];
    noite = choiva['noite']
    return f'Temperaturas:\nMínima: {tMin}\tMáxima: {tMax}\nProbabilidades de choiva:\nMañán: {maña}%\tTarde: {tarde}%\tNoite: {noite}%';