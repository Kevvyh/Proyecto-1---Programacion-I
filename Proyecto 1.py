#Sakin Contreras
#Joaquín Carrillo
#Kevin Inalaf

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Funciones de carga

def buscar_archivos():
    # Buscar y retornar archivos que terminen en .npy en el directorio actual.
    archivos_npy = []
    # Recorrer los archivos.
    for archivo in os.listdir('.'):
        if archivo.endswith('.npy'):
            archivos_npy.append(archivo)
    return archivos_npy

def menu_interactivo_pulento(archivos):
    # Mostrar el menu, validar la entrada del usuario y retornar el archivo seleccionado.
    print("--- Archivos que encontré ---")
    contadorsote = 1
    for archivaco in archivos:
        # Imprimir el menu enumerado y usamos el contador para ir sumando la cantidad de archivos.
        print(f"{contadorsote}. {archivaco}")
        contadorsote =+ 1
    
    while True:
            try:
                # Pedimos una entrada de numero entero al usuario. OCUPAMOS FUNCION TRY-EXCEPT DEIDAD
                seleccion = int(input("Seleccione el número del archivo a cargar: "))
                
                # Validamos si la entrada está en el rango de la lista.
                if 1 <= seleccion <= len(archivos):
                    return archivos[seleccion - 1]
                
                print(f"Error: Ingrese un número entre 1 y {len(archivos)}.")
                
            except ValueError:
                # Si el usuario ingresa letras o simbolos, fallará y pedira nuevamente una selección.
                print("Error: Debe ingresar un número entero. Intente nuevamente.")

def cargar_la_data(nombre_archivo):
    # Cargar un archivo .npy usando la libreria NumPy.
    print(f"Cargando el archivo: {nombre_archivo}...")
    señal = np.load(nombre_archivo)
    return señal.tolist() # Lo convertimos a lista nativa de Python para procesar manualmente.

# Funciones de aplicación de filtros.

def filtro_media_loca(senal, ventana=7):
    # Creamos una lista donde se guarda la señal filtrada.
    resultado = []
    largo = len(senal) # Cantidad total de datos.
    mitad = ventana // 2 
    
    #Recorrer cada posición de la señal original.
    for i in range(largo):
        inicio = i - mitad
        if inicio < 0:
            inicio = 0 #Si nos salimos de la lista forzamos que empiece en el indice 0.
            
        fin = i + mitad + 1 #Donde deberia terminal la ventana.
        if fin > largo:
            fin = largo #El limite de la ventana es el maximo del largo de las muestras.
        
        datos_ventana = [] #Lista para agregar los datos que caen en la ventana.
        for j in range(inicio, fin):
            datos_ventana.append(senal[j]) #Agregamos los datos.
        
        suma_total = 0
        for valor in datos_ventana:
            suma_total = suma_total + valor #Suma de todos los valores de la ventana para sacar el promediovich.
            
        promedio = suma_total / len(datos_ventana) #Dividimos la suma por la cantidad de los datos que realmente entraron en la ventana.
        resultado.append(promedio) #Los agregamos a la lista que tiene la señal filtrada.
        
    return resultado # Retornamos la señal fitrada.

def filtro_mediana_loca(senal, ventana=7):
    #Volvemos a crear una lista que contenera la señal filtrada.
    mediana_filtradita = []
    n = len(senal)
    mitad_ventana = ventana // 2
    
    for i in range(n):
        
        inicio = i - mitad_ventana
        if inicio < 0:
            inicio = 0 #Si nos salimos de la lista forzamos que empiece en el indice 0, otra vez. :c
            
        fin = i + mitad_ventana + 1 #Donde deberia terminal la ventana, y si, otra vez. :v
        if fin > n:
            fin = n #El limite de la ventana es el maximo del largo de las muestras.
        
        #Creamos la ventana que utilizaremos con los limites.
        ventanita = senal[inicio:fin]
        #Ordenamos la ventana porque la mediana funciona solo si están los datos ordenados.
        ventinta_ordenada = sorted(ventanita) 
        
        #Empezamos a cocinar el calculo de la ventana.
        largo_ventana = len(ventanita)
        #Encontramos de inmediato la posición del medio de los datos.
        mitad_indice = largo_ventana // 2
        
        #Si la ventana es par:
        if largo_ventana % 2 == 0:
            #Calcularemos los 2 numeros centrales y los promediaremos.
            mediana = (ventanita[mitad_indice - 1] + ventanita[mitad_indice]) / 2.0
        else:
            #Si no es par, solamente utilizaremos el numero del medio que encontramos con la posición del medio de los datos.
            mediana = ventanita[mitad_indice]
            
        mediana_filtradita.append(mediana) #Agregamos la mediana a a lista filtrada.
        
    return mediana_filtradita

def super_funcion_estadistica(senal):
    el_maximo = senal[0] #Asumimos que el primer dato es el maximo.
    el_minimo = senal[0] #Lo mismo acá.
    suma_datos = 0 # Acumuladordeidad para ir sumando todos los valores.
    
    for valor in senal: #Recorremos la lista.
        #Buscamos el valor maximo.
        if valor > el_maximo:
            el_maximo = valor #Y se guarda, paaaa.
        #Buscamos el valor minimo.
        if valor < el_minimo:
            el_minimo = valor #Y se guarda, paaaa.
        suma_datos += valor  #Sumamos, paaaa.
        
    #Calculo de promedio normal
    largo = len(senal)
    el_promedio = suma_datos / largo #Calculamos el promedio.
    
    #Acumulador para la desviación estandar.
    suma_restas_cuadrado = 0

    for valor in senal:
        resta = valor - el_promedio # Calculamos la distancia entre el valor y el promedio
        cuadrado = resta ** 2 # Todo numero dentro de la varianza esta elevado al cuadrado.
        suma_restas_cuadrado = suma_restas_cuadrado + cuadrado #Agregamos los cuadrados al acumulador.
        
    #La varianza es la desviacion estandar sin raiz, la usaremos para sacarla luego.    
    varianza = suma_restas_cuadrado / largo #Es basicamente el promedio.
    desviacion = varianza ** 0.5 #Al parecer la forma nativa de sacar la raiz cuadrada es elevar a 0.5.
    
    return el_maximo, el_minimo, el_promedio, desviacion #Retornamos todos los calculos completamente exitosos. :v

# Visualización de la interfaz gráfica. -----

def iniciar_interfaz(senal_original):
    #La mejor base de datos, para saber que calcular.
    diccionarsito = {
        "senal_actual": senal_original,
        "nombre_actual": "Señal Original"
    }

    # Creamos la ventana donde se ejecutara el grafico.
    fig, ax = plt.subplots(figsize=(10, 6))
    #Espacio para los botones debajo del grafico.
    plt.subplots_adjust(bottom=0.25)
    
    # Graficamos la señal original.
    linea, = ax.plot(diccionarsito["senal_actual"], label="Amplitud", color='blue')
    
    ax.set_title("Señal Original") #Aplicamos el titulo.
    ax.set_xlabel("Muestras (Tiempo)") #Eje X
    ax.set_ylabel("Amplitud") #Eje Y
    ax.grid()

    #Funciones de actualización
    
    def actualizar_interfaz(nueva_senal, nuevo_nombre, color):
        #Actualización del diccionaristo :v
        diccionarsito["senal_actual"] = nueva_senal
        diccionarsito["nombre_actual"] = nuevo_nombre
        
        #No borramos la grafica anterior,
        #simplemente le insertamos los nuevos datos de las filtradas.
        linea.set_ydata(nueva_senal)
        linea.set_color(color)
        ax.set_title(nuevo_nombre)
        
        #Vuelve a graficar la señal.
        fig.canvas.draw_idle()

    #Funcion de los botones.

    def mostrar_original(evento):
        #Muestra la señal original no filtrada. :v
        actualizar_interfaz(senal_original, "Señal Original", 'blue')

    def mostrar_media(evento):
        print("Calculando Media Móvil...")
        senal_filtrada = filtro_media_loca(senal_original, ventana=7)
        #Llama a la funcion de la señal filtrada de la media.
        actualizar_interfaz(senal_filtrada, "Señal Filtrada: Media Móvil", 'green')
        #La actualiza, paaa.

    def mostrar_mediana(evento):
        print("Calculando Mediana Móvil...")
        senal_filtrada = filtro_mediana_loca(senal_original, ventana=7)
        #Llama a la funcion de la señal filtrada de la mediana.
        actualizar_interfaz(senal_filtrada, "Señal Filtrada: Mediana Móvil", 'red')
        #La actualiza, paaa.

    def mostrar_estadisticas(evento):
        #Toma en cuenta las estadisticas que se muestran en pantalla.
        maximo, minimo, prom, desv = super_funcion_estadistica(diccionarsito["senal_actual"])
        
        print(f"Estadísticas de {diccionarsito['nombre_actual']}") #Se muestra el nombre de la señal que se esta graficando.
        print(f"Valor Máximo: {maximo:.3f}") #Limitamos los decimales del maximo
        print(f"Valor Mínimo: {minimo:.3f}") #Limitamos los decimales del minimo
        print(f"Promedio: {prom:.3f}") #Limitamos los decimales del promedio
        print(f"Desviación Estándar: {desv:.3f}") #Limitamos los decimales de la desviacion estandar.
        print("---------------------------------------------")
        
        #Creamos la variable que tendra el nombre de todas las estadisticas con sus respectivos datos.
        texto_stats = f"{diccionarsito['nombre_actual']} | Max: {maximo:.2f} | Min: {minimo:.2f} | Prom: {prom:.2f} | Desviación Estandar: {desv:.2f}"
        ax.set_title(texto_stats, fontsize=10) #Lo colocamos arriba como titulo en la grafica.
        #Pedimos que lo dibuje.
        fig.canvas.draw_idle()

    # Creamos los botones con sus respectivos tamaños.
    ax_btn_orig = plt.axes([0.1, 0.05, 0.15, 0.075]) #Original
    ax_btn_media = plt.axes([0.3, 0.05, 0.15, 0.075]) #Media
    ax_btn_mediana = plt.axes([0.5, 0.05, 0.18, 0.075]) #Mediana
    ax_btn_stats = plt.axes([0.75, 0.05, 0.15, 0.075]) #Estadisticas
    
    #Le asignamos el nombre a cada boton.
    btn_orig = Button(ax_btn_orig, 'Original')
    btn_media = Button(ax_btn_media, 'Media Móvil')
    btn_mediana = Button(ax_btn_mediana, 'Mediana Móvil')
    btn_stats = Button(ax_btn_stats, 'Estadísticas')
    
    #Iniciamos los eventos al ser clickeados.
    btn_orig.on_clicked(mostrar_original)
    btn_media.on_clicked(mostrar_media)
    btn_mediana.on_clicked(mostrar_mediana)
    btn_stats.on_clicked(mostrar_estadisticas)

    #Guardamos los botones en una lista para retornalos.
    botones_activos = [btn_orig, btn_media, btn_mediana, btn_stats]
    
    #Retornamos los botones y las figuras.
    return fig, botones_activos

#Iniciar y mostrar el programa

def el_programa_certero():
    print("Analisis de señales con botones funcionales.")
    
    # Guardamos en una variable la funcion de buscar archivos.
    archivos = buscar_archivos()
    
    if not archivos:
        print("No se encontraron archivos .npy en el directorio actual.") #Si no hay archivos, lo imprimimos para avisar.
        return
        
    # Seleccion del archivo
    # Guardamos en una variable la funcion del menu.
    archivo_seleccionado = menu_interactivo_pulento(archivos)
    
    # Cargar los archivos
    # Guardamos la funcion en una variable para cargar los archivos de la carpeta data.
    senal = cargar_la_data(archivo_seleccionado)
    
    # Procedemos con el inicio de la interfaz.
# Iniciamos la interfaz grafica.
    print("Iniciando interfaz gráfica...")
    # Guardamos los botones en una variable para que no dejen de funcionar.
    figura, mis_botones = iniciar_interfaz(senal) 
    plt.show() #Mostramos el programa

el_programa_certero() #Iniciamos la funcion del programa finalmente :,,,v