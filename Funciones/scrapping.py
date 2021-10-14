from bs4 import BeautifulSoup
import requests 
import pandas as pd

'''
La función scrappeoHtml retorna el html de la url que se pase como parámetro
'''

def scrappeoHtml (url):
    page = requests.get(url).text
    return BeautifulSoup(page, "lxml") 

'''
La función generacionUrlInvertirOnline retorna una url en función de lo que se busque Scrappear (url que luego podrá ser usada para generar el html de la web).
'''

def generacionUrlInvertirOnline(activoFinanciero, panel=""):
    respuesta = ""
    urlBase = "https://iol.invertironline.com/mercado/cotizaciones/argentina/"
    if(activoFinanciero == "acciones"):
        if(panel=="general"):
            panel = "/panel-general"
            respuesta = urlBase + activoFinanciero + panel
        elif(panel=="subastas"):
            panel = "/subastas"
            respuesta = urlBase + activoFinanciero + panel
        elif(panel == "lider"):
            panel = "/panel-líderes"
            respuesta = urlBase + activoFinanciero + panel
        else:
            respuesta = "No existe el panel introducido"
    elif(activoFinanciero=="cedears" or activoFinanciero=="bonos"or activoFinanciero=="fondos"):
        respuesta = urlBase + activoFinanciero + "/todos"
    elif(activoFinanciero=="opciones" or activoFinanciero=="letras"or activoFinanciero=="on" or activoFinanciero=="cauciones" or activoFinanciero=="cheques"):
        respuesta = urlBase + activoFinanciero + "/todas"
    elif(activoFinanciero == "monedas"):
        respuesta = urlBase + "/monedas"
    else:
        respuesta = "Verificar el tipo de scrappeo solicitado"
    
    return respuesta

'''
La función generarTablaCotizaciones obtiene la tabla de cotizaciones del html de la web que se pase
'''

def generarTablaCotizaciones(html):
    return html.find('table', {"id" : "cotizaciones"})

'''
La función generarArrayTitulos genera un array con los títulos de las columnas de la tabla
'''

def generarArrayTitulos(html):
    tablaDeCotizaciones = generarTablaCotizaciones(html)
    campos = (tablaDeCotizaciones.findAll("tr"))[0].findAll("td") 
    return [td.text for td in campos]

'''
La función generarArrayDeActivos genera un array con todos los demás datos de la tabla
'''

def generarArrayDeActivos (html):
    tablaDeCotizaciones = generarTablaCotizaciones(html)
    filas = tablaDeCotizaciones.find_all('tr')
    lista = []
    for tr in filas[1:]:
        td = tr.find_all('td')
        row = [tr.text.replace("\n", "").replace("\r", "").replace(" ", "") for tr in td]

        #Reemplazo ',' por '.' y paso el string a float
        for index in range(0, len(row)):
            row[index] = row[index].replace('.', '')
            row[index] = row[index].replace(',', '.')

        lista.append(row)
    
    return lista

'''
La función generarDF crea el DataFrame combinando los datos de la tabla y columna
'''

def generarDF (datos, columnas):
    return pd.DataFrame(datos, columns= columnas)