import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
import json
import html
import argparse  # Importa argparse para manejar los argumentos
import sys
import requests

#Función que hace un GET a la url con el JSON (ejemplo: https://www.hipervarejo.com.br/api/catalog_system/pub/products/search/sensor-freio-abs-fiat-siena-2012-a-2015-dianteiro-passageiro/p?compSpecs=true)
def get_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Retorna el JSON de la respuesta
    else:
        print(f"Error al obtener los datos: {response.status_code}")
        return None

# Devuelvo el json de las marcas y modelos en un .txt ó lo que sea
def save_to_txt(data, filename="output.txt"):
    # Abre el archivo en modo escritura
    with open(filename, 'a', encoding='utf-8') as f:
        # Convierte el diccionario a formato JSON y lo guarda en el archivo
        json.dump(data, f, ensure_ascii=False, indent=4)

def recursive_child_node_html(element):
    #print("El elemento es: ", element)
    # Caso base: Si el elemento es un nodo de texto (hoja), devuelve su etiqueta padre
    if isinstance(element, NavigableString):  
        return element.parent  # Devuelve el nombre del tag que contiene este texto
    
    # Si tiene hijos, recorremos los hijos recursivamente
    for child in element.children:
        result = recursive_child_node_html(child)  
        if result:  
            return result  # Devuelve el primer nodo hoja encontrado

    return None  # Si no hay hijos, retorna None

def extract_brands_and_models(html_string):
    brands_and_models = {}
    soup = BeautifulSoup(html_string, 'html.parser')

    paragraphs = soup.find_all('p')  

    marca_nueva = None
    for paragraph in paragraphs:  # Itera sobre cada <p> encontrado
        if(paragraph.children):
            nodo_hoja = recursive_child_node_html(paragraph)
            #print("El nodo es: ", nodo_hoja)
            if(nodo_hoja.name == "strong"):
                nodo_padre = paragraph  # El <p> entero es el nodo padre
                marca = nodo_padre.find("strong").text.strip()  # Extrae la marca del <strong>
                #print("La marca es: ", marca)
                
                # Elimina la marca del texto del nodo padre para obtener solo el modelo
                texto_completo = nodo_padre.text.strip()
                modelo = texto_completo.replace(marca, '').strip()  # Elimina la marca del texto
                #print("El modelo es: ", modelo)
                
                # Almacena en el diccionario
                if marca in brands_and_models:
                    brands_and_models[marca].append(modelo)
                else:
                    brands_and_models[marca] = [modelo]
            
            if(nodo_hoja.name == "span"):
                #print("El nodo hoja es: ", nodo_hoja.text)
                marca_nueva = nodo_hoja.text.strip()  # Guarda el nombre de la marca
                if marca_nueva not in brands_and_models:
                    brands_and_models[marca_nueva] = []  # Inicializa el array de modelos para esta marca
                #print(f"Marca encontrada: {marca_nueva}")

            if(nodo_hoja.name == "font"):
                brands_and_models[marca_nueva].append(nodo_hoja.text.strip())  # Agrega el modelo al array de la marca
                #print(f"Modelo agregado a {marca_nueva}: {nodo_hoja.text.strip()}")


    return brands_and_models



# # https://www.hipervarejo.com.br/api/catalog_system/pub/products/search/sensor-freio-abs-fiat-siena-2012-a-2015-dianteiro-passageiro/p?compSpecs=true
# json3_value ="""
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003EFIAT\u003C/span\u003E\u003C/font\u003E\u003C/font\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003ESIENA EL 1.4 MPI FIRE FLEX 8V 4P 2012 até 2016\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003ESIENA EL CELEB. 1.4 MPI FIRE FLEX 8V 4P 2012 até 2016\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003ESIENA TETRAFUEL 1.4 MPI FIRE FLEX 8V 4P 2012\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003ESIENA EL 1.6 MPI 16V 2013 até 2015\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003EPEUGEOT\u003C/span\u003E\u003C/font\u003E\u003C/font\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E308 1.6 THP 16V 2010 até 2014\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# \u003Cp style='line-height: 1; text-align: left;'\u003E\u003Cspan style='font-family: Verdana, Geneva, sans-serif;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E\u003Cfont style='vertical-align: inherit;'\u003E208 1.6 VTI 16V 2012 até 2015\u003C/font\u003E\u003C/font\u003E\u003C/span\u003E\u003C/p\u003E
# """

# html_text_1 = html.unescape(json3_value)
# #print(extract_brands_and_models(html_text_1))
# brands_and_models = extract_brands_and_models(html_text_1)
# save_to_txt(brands_and_models, "brands_and_models_json_1.txt")

# print("----------------------------------------------------")

# # # https://www.hipervarejo.com.br/api/catalog_system/pub/products/search/jogo-anel-segmento-std-boxer-ducato-jumper-2-3-16v-mahle-dc8770/p?compSpecs=true
# escaped_text = "\u003Cp\u003E\u003Cstrong\u003ECitroen\u003C/strong\u003E\u003Cbr /\u003EJumper 2.3 16V 2010 a 2011\u003C/p\u003E \u003Cp\u003E\u003Cbr /\u003E\u003Cstrong\u003ECitroen\u003C/strong\u003E\u003Cbr /\u003EJumper 2.3 16V 2015 a 2019\u003C/p\u003E \u003Cp\u003E\u003Cbr /\u003E\u003Cstrong\u003EFiat\u003C/strong\u003E\u003Cbr /\u003EDucato 2.3 16V 2009 a 2015\u003C/p\u003E \u003Cp\u003E\u003Cbr /\u003E\u003Cstrong\u003EPeugeot\u003C/strong\u003E\u003Cbr /\u003EBoxer 2.3 16V 2010 a 2011\u003C/p\u003E"

# html_text = html.unescape(escaped_text)
# print(extract_brands_and_models(html_text))
# save_to_txt(brands_and_models, "brands_and_models_json_2.txt")



def main():
    
    print(sys.argv)

    # Verifica que se haya pasado al menos una URL
    if len(sys.argv) < 2:
        print("Por favor, proporciona al menos una URL como argumento.")
        sys.exit(1)
    
    # Recorre las URLs pasadas como argumentos (exceptuando el primer argumento que es el nombre del script)
    for i in range(1, len(sys.argv)):
        url = sys.argv[i]
        print(f"Obteniendo datos desde la URL: {url}")
        
        data = get_json_from_url(url)  # Suponiendo que esta función está definida

        complete_specifications = None
        for entry in data:
            # Recorre los datos JSON y extrae la clave 'completeSpecifications'
            complete_specifications = entry.get('completeSpecifications')
        
        if complete_specifications:
            objeto_aplicacao = next((item for item in complete_specifications if item['FieldId'] == '291'), None)
            if objeto_aplicacao:
                values_objeto_aplicacao = objeto_aplicacao.get("Values")
                if values_objeto_aplicacao:
                    first_item = values_objeto_aplicacao[0]
                    html_compatibilidades = first_item.get('Value')
                    brands_and_models = extract_brands_and_models(html_compatibilidades)
                    save_to_txt(brands_and_models, f"brands_and_models_{i}.txt")  # Guardar con un nombre único

#Función main
if __name__ == "__main__":
    main()