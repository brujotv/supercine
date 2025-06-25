import xml.etree.ElementTree as ET
import requests

# Leer configuración de búsqueda
config = ET.parse('busqueda.xml')
root = config.getroot()
fuente = root.find('fuente').text.strip() if root.find('fuente') is not None else ''
criterios = root.find('criterios')

# Recoger todos los criterios con valor
criterios_busqueda = []
if criterios is not None:
    for criterio in criterios.findall('criterio'):
        campo = criterio.attrib.get('campo', '').strip()
        valor = (criterio.text or '').strip()
        if campo and valor:
            criterios_busqueda.append((campo, valor))

if not fuente or not criterios_busqueda:
    print('No se ha definido una fuente o criterios de búsqueda válidos en busqueda.xml')
    exit(1)

print('Buscando por los siguientes criterios:')
for campo, valor in criterios_busqueda:
    print(f'  - {campo}: "{valor}"')
print(f'En: {fuente}\n')

# Descargar el XML remoto
data = requests.get(fuente).content

# Parsear el XML de películas
peliculas_root = ET.fromstring(data)
resultados = []
for item in peliculas_root.findall('item'):
    cumple = True
    for campo, valor in criterios_busqueda:
        campo_valor = (item.findtext(campo) or '').strip()
        if valor.lower() not in campo_valor.lower():
            cumple = False
            break
    if cumple:
        titulo = (item.findtext('title') or '').strip()
        genero = (item.findtext('genre') or '').strip()
        anio = (item.findtext('year') or '').strip()
        resultados.append(f'{titulo} | {genero} | {anio}')

if resultados:
    print('Resultados encontrados:')
    for r in resultados:
        print(r)
else:
    print('No se encontraron resultados para esos criterios.') 