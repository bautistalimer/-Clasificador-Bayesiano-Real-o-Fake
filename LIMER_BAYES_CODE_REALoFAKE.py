from collections import defaultdict

noticias = [
    {"texto":"El presidente anunció una nueva reforma educativa  ", "clase":"real"},
    {"texto":"Descubren que la vacuna convierte a las personas en robots", "clase":"fake"},
    {"texto":"La NASA confirma el hallazgo de agua en Marte ", "clase":"real"},
    {"texto":"Científicos afirman que la Tierra es plana", "clase":"fake"},
    {"texto":"El ministerio de salud lanza campaña contra el dengue", "clase":"real"},
    {"texto":"Celebridades usan crema milagrosa para rejuvenecer 30 años", "clase":"fake"},
    {"texto":"Se inaugura el nuevo hospital en la ciudad", "clase":"real"},
    {"texto":"Estudio revela que comer chocolate cura el cáncer", "clase":"fake"},
    {"texto":"Gobierno aprueba ley de protección ambiental", "clase":"real"},
    {"texto":"Investigadores aseguran que los teléfonos espían nuestros sueños", "clase":"fake"}
    ]   

for item in noticias:
    item["palabras"] = item["texto"].lower().split()

conteo_clases = defaultdict(int)
for item in noticias:
    clase= item["clase"]
    conteo_clases[clase] += 1

total_noticias = len(noticias)
P_clase = {}
for clase, conteo in conteo_clases.items():
    P_clase[clase]= conteo / total_noticias

conteo_palabras = defaultdict(lambda: defaultdict(int))
total_palabras_por_clase = defaultdict(int)
vocabulario = set()

for item in noticias:
    clase = item["clase"]
    for palabra in item["palabras"]:
        conteo_palabras[clase][palabra] += 1
        total_palabras_por_clase[clase] +=1
        vocabulario.add(palabra)

def probabilidad_palabra_dada_clase(palabra, clase):
    return (conteo_palabras[clase][palabra] + 1) / (total_palabras_por_clase[clase] + len(vocabulario))

def clasificar_texto(lista_palabras):
    probabilidades = {}
    for clase in P_clase:
        prob = P_clase[clase]
        for palabra in lista_palabras:

            if palabra in vocabulario:
                prob *= probabilidad_palabra_dada_clase(palabra, clase)
        probabilidades[clase] = prob

    maximo = max(probabilidades.values())
    for clase, prob in probabilidades.items():
        if prob == maximo:
            return clase

aciertos = 0
matriz_confusion = {
    "real": {"real": 0, "fake": 0},
    "fake": {"real": 0, "fake": 0}
}

for item in noticias:
    clase_real = item["clase"]
    clase_predicha = clasificar_texto(item["palabras"])
    
    matriz_confusion[clase_real][clase_predicha] += 1
    if clase_real == clase_predicha:
        aciertos += 1

precision_total = (aciertos / total_noticias) * 100

print(f'''RESULTADOS:
    Precisiocion total (accuracy): {precision_total: }

    Matriz de confusión: 
    (filas: real | columnas: predicho)
    real » real: {matriz_confusion['real']['real']} | real » fake: {matriz_confusion['real']['fake']}
    fake » real: {matriz_confusion['fake']['real']} | fake » fake: {matriz_confusion['fake']['fake']}
''')

nuevas_noticias = [ 
"Nuevo estudio demuestra que el café mejora la memoria", 
"Expertos afirman que los gatos pueden hablar con humanos",
"La playstation 5 hace que cuando la juegues te conviertas en zombie",
"el fuego hizo que la casa se prendiera fuego"
] 
print("================================================================================================")
print("clasificacion de nuevas noticias")
for i, texto in enumerate(nuevas_noticias, 1):
    palabras_nuevas = texto.lower().split()
    resultado = clasificar_texto(palabras_nuevas)
    print(f"{i}. {texto} » {resultado}")
