import requests;

# Función que accede a api de meteogaliza e devolve unha información meteorolóxica básica
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

# Función que devolve unha imaxe a traves da api da nasa.
def get_apod():
  url = 'https://api.nasa.gov/planetary/apod.jpg';
  response = requests.get(url, params={'api_key':'hMcVEIZB3yVAw5r5hrNTB6iCiUDAfIn8tdyRhot6'});
  img_url = response.json()['hdurl'];
  response = requests.get(img_url);
  with('./input/apod') as archivo:
     archivo.write(response.content);
