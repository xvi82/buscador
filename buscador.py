import re
from datetime import datetime
from nltk.tokenize import word_tokenize
import math
import pdftotext

def abrirpdf(pdf):
    with open(pdf, "rb") as f:
        archivo = pdftotext.PDF(f)
        document = "\n\n".join(archivo)
        return document

def buscador(texto, valor):
    matches = list()
    for index in range(len(texto)):
        if texto[index] == valor:
            matches.append(index)
    if matches:
        return matches
    else:
        raise ValueError("{} no está en {}".format(valor, texto))

def palabras_cercanas(texto, palabra, *lista):
    for index in lista:
        if palabra in texto[(index-2):(index+2)]:
            return index

def fecha_cercana_despido(texto, palabras_cercanas):
    lista = texto[(palabras_cercanas-3):(palabras_cercanas+4)]
    fecha = [word for word in lista if re.match('\d{1,2}(\/|\.|\-)\d{1,2}(\/|\.|\-)\d{1,4}', word)]
    fechaclean = re.sub('\,|\.|\-|\/', '', fecha[0])
    return datetime.strptime(fechaclean, '%d%m%Y').date()

def despido(texto):
    try:
        a = buscador(texto, 'efectos')
    except:
        b = buscador(texto, 'efectividad')
    try:
        c = palabras_cercanas(texto, 'despido', *a)
    except:
        d = palabras_cercanas(texto, 'despido', *b)
    try:
        e = fecha_cercana_despido(texto, c)
        return e
    except:
        f = fecha_cercana_despido(texto, d)
        return f

def salario(texto):
    for item in range(len(texto)):
        if '€' in texto[item] or 'euros' in texto[item]:
            if re.match('(\d+(\,|\.)?\d+?(\,|\.)?\d+?|\d+)', texto[item-1]):
                return float(re.sub(',', '.', texto[item-1]))

def antiguedad(texto):
    try:
        for item in range(len(texto)):
            if texto[item] == "antigüedad":
                if re.match('(\d+(\,|\.)?\d+?(\,|\.)?\d+?|\d+)', texto[item + 1]):
                    antigu = texto[item+1]
                    fechaclean = re.sub('\,|\.|\-|\/', '', antigu)
                    return datetime.strptime(fechaclean, '%d%m%Y').date()
    except:
        fechas = [word for word in texto if re.match('\d{1,2}(\/|\.|\-)\d{1,2}(\/|\.|\-)\d{1,4}', word)]
        fechaclean = re.sub('\,|\.|\-|\/', '', fechas[0])
        return datetime.strptime(fechaclean, '%d%m%Y').date()

def preparar_texto(texto):
    from nltk.corpus import stopwords
    cleaned = re.sub(r'[^A-ZñÑa-zÁ-Úá-úä-ü0-9.€,\/]+', ' ', texto)
    tokenized = word_tokenize(cleaned.lower())
    stopwords = set(stopwords.words('spanish'))
    textprov = [word for word in tokenized if word not in stopwords]
    t = list()
    for i in textprov:
        if re.match('\,', i):
            t.append(i)
        if re.match('\.', i):
            t.append(i)
    textdef = [word for word in textprov if word not in t]
    return textdef

def indemnizacion_despido_completa(texto):
    from datetime import datetime, timedelta
    fechalimite = datetime.strptime('12/02/2012', '%d/%m/%Y').date()
    salar = salario(texto)
    despid = despido(texto)
    antig = antiguedad(texto)
    if antig > fechalimite:
        dif = math.ceil(((despid - antig) / timedelta(days=1))) + 1
        daf = math.ceil(dif / 30.41666667)
        indem = daf * salar * 2.75
        return "Su indemnización sería de {} euros".format(indem)
    else:
        dif1 = math.ceil(((fechalimite - antig) / timedelta(days=1))) + 1
        daf1 = math.ceil((dif1 / 30.41666667))
        indemprev = daf1 * salario * 3.75
        dif2 = math.ceil(((despid - fechalimite) / timedelta(days=1))) + 1
        daf2 = math.ceil(dif2 / 30.41666667)
        indempost = daf2 * salar * 2.75
        indem2 = indemprev + indempost
        return "Su indemnización sería de {} euros".format(indem2)

def indemnizacion_despido_datos(fecha_antiguedad, salari, fecha_despido):
    from datetime import datetime, timedelta
    fechalimite = datetime.strptime('12/02/2012', '%d/%m/%Y').date()
    fechaclean = re.sub('\,|\.|\-|\/', '', fecha_antiguedad)
    antig = datetime.strptime(fechaclean, '%d%m%Y').date()
    despidoclean = re.sub('\,|\.|\-|\/', '', fecha_despido)
    despid = datetime.strptime(despidoclean, '%d%m%Y').date()
    salario = float(re.sub(',', '.', salari))
    if antig > fechalimite:
        dif = math.ceil(((despid - antig) / timedelta(days=1))) + 1
        daf = math.ceil(dif / 30.41666667)
        indem = daf * salario * 2.75
        return "Su indemnización sería de {} euros".format(indem)
    else:
        dif1 = math.ceil(((fechalimite - antig) / timedelta(days=1))) + 1
        daf1 = math.ceil((dif1 / 30.41666667))
        indemprev = daf1 * salario * 3.75
        dif2 = math.ceil(((despid - fechalimite) / timedelta(days=1))) + 1
        daf2 = math.ceil(dif2 / 30.41666667)
        indempost = daf2 * salario * 2.75
        indem2 = indemprev + indempost
        return "Su indemnización sería de {} euros".format(indem2)
