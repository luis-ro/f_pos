# Multilateracion usando IA

El programa consiste en una simulacion previa a la construccion fisica del proyecto para comprobar la factibilidad del mismo

## Para Iniciar

Para la elaboracion de este programa me base en el uso de IA, concretamente, en una regresion lineal con salida multiple (2 en este caso: X y Y)

### Prerequisitos

Para ejecutar la simulacion es necesario tener [Python](python.org) con los siguientes modulos

* [Numpy](numpy.org)         - Para manejo de datos en matrices y operaciones matematicas
* [PyGame](pygame.org)       - Para visualizar la simulacion
* [Scikit-learn](scikit-learn.org/stable)   - Para entrenar el modelo y hacer las predicciones

## Comandos

Si se desea calcular la posicion solo una onda puede ser dibujada a la vez, a menos que el modo patio de juegos este activado

Teclas:

```
q  ->  Salir del programa

.  ->  generar una onda equidistante a los 3 sensores
0  ->  generar una onda aleatoria
5  ->  generar una onda en la coordenada especificada

t  ->  activar modo aleatorio y si se presiona de nuevo acelera la velocidad de la misma
r  ->  volver velocidad a la original y desactivar modo aleatorio

arriba -> Subir la velocidad de las ondas
abajo  -> Bajar la velocidad de las ondas

Enter  ->  Entrar/Salir del modo patio de juegos 
```

En el modo aleatorio no valen los demas comandos excepto activar el modo patio de juegos y cambiar la velocidad
Si el modo patio de juegos esta activado, es posible dibujar varias ondas a la vez con loc comandos descritos anteriormente, a mas de la rueda del raton, que sirve para dibujar bastantes de golpe

## Version

v1.0.0  -   El calculo de la posicion funciona, pero con sin demasiada fiabilidad

### Notas

En esta version no es posible cambiar de posicion a los sensores ni agregar mas, la IA no esta entrenada para esos casos aun

### Log

**v1.0.0**
```
    Agregada una IA de regresion lineal con r2=0.8197...
    Realizados cambios en todos los archivos para permitir la transferencia de datos
    No existe mucha exactitud con las predicciones
    No es posible cambiar de posicion a los sensores ni variar su cantidad
    Integrado un archivo para crear los puntos para entrenar "get_points.py"
    Adjuntado los puntos usados entrenar la IA en el fichero "test_points.csv", 310k valores - Falta filtrar
    El fichero del modelo ya entrenado es "trained_model.pkl"
```
## Autor

* **[Luis Alvear](https://github.com/luis-ro)**
