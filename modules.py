import requests;
import random;
import pandas as pd;
from bs4 import BeautifulSoup;

# Función que accede a api de meteogaliza e devolve unha información meteorolóxica básica
def get_weather():
    url = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action';
    response = requests.get(url, params={'idConc':'27049'})
    tMin = response.json()['predConcello']['listaPredDiaConcello'][0]['tMin'];
    tMax = response.json()['predConcello']['listaPredDiaConcello'][0]['tMax'];
    choiva = response.json()['predConcello']['listaPredDiaConcello'][0]['pchoiva'];
    maña = choiva['manha'];
    tarde = choiva['tarde'];
    noite = choiva['noite'];
    return f'Temperaturas:\nMínima: {tMin}\tMáxima: {tMax}\nProbabilidades de choiva:\nMañán: {maña}%\tTarde: {tarde}%\tNoite: {noite}%';

# Función que devolve unha imaxe a traves da api da nasa.
def get_apod():
  url = 'https://api.nasa.gov/planetary/apod';
  response = requests.get(url, params={'api_key':'hMcVEIZB3yVAw5r5hrNTB6iCiUDAfIn8tdyRhot6'});
  img_url = response.json()['url'];
  res = requests.get(img_url);
  with open('apod.jpg', 'wb') as img:
    img.write(res.content);
  return res, response.json()['explanation'], response.json()['title']

def get_joke():
  url = 'https://v2.jokeapi.dev/joke/Any?type=single';
  response = requests.get(url);
  return response.json()['joke'];

def convert(path):
  filename = path.split('.')[0];
  if 'csv' in path:
    df = pd.read_csv(path);
    filename += '.json';
    df.to_json(filename);
  elif 'json' in path:
    df = pd.read_json(path, orient='records');
    filename += '.csv';
    df.to_csv(filename, index=False);
  return filename;

def get_info(path):
  df = pd.read_csv(path);
  res = '';
  for i in range(len(df.columns)):
    res += f'{df.columns[i]}: {df.dtypes[i]}\t';
  res += f'\n\n{df.describe()}';
  return res;

def get_news(limit):
  url = 'https://www.elprogreso.es';
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  sp = soup.findAll('a', href=lambda value: value and '/articulo/' in value)
  dicc = {};
  lista_titulos = [];
  for i in sp:
    title, href = i.get('title'), i.get('href');
    if 'https://' not in href: href = url+href;
    dicc[title] = href;
    if title not in lista_titulos: lista_titulos += [title];

  res = '';
  for i in range(limit):
    n = random.randint(0, len(lista_titulos)-1);
    clave = lista_titulos[n];
    res += f'Título: {clave}\n{dicc[clave]}\n';

  return res;

  def get_movies(limit):
  url = 'https://yelmocines.es';
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  soup = soup.find('section', {'class':'cartelera uPanel'}).find('ul',{'class':"listCartelera tituloPelicula cf"})
  sp = soup.findAll('li')

  dicc = {};
  lista_titulos = [];

  for i in sp:
    title, href = i.find('h1'), i.find('href');
    if 'https://' not in href: href = url+href;
    dicc[title] = href;
    if title not in lista_titulos: lista_titulos += [title];

  res = '';
  for i in range(limit):
    n = random.randint(0, len(lista_titulos)-1);
    clave = lista_titulos[n];
    res += f'Título: {clave}\n{dicc[clave]}\n';

  return res;