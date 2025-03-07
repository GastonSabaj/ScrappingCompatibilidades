from fastapi import FastAPI
from ScrappingCompatibilidadesPython import get_json_from_url, extract_brands_and_models

app = FastAPI()

# Ejemplo: GET /Compatibilidades/?urlString=https://example.com/data
@app.get("/Compatibilidades/")
def getCompatibilidades(urlString: str):
    print(urlString)
    data = get_json_from_url(urlString)  # Suponiendo que esta función está definida

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
                return brands_and_models  # Devolver en la API

                #print(brands_and_models)

