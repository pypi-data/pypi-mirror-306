from .simpson import simpson

def simpson_compuesto(f, a, b, N):
    """
    Aproxima el valor numérico de la integral definida de f(x) en el intervalo [a, b] utilizando la regla de Simpson compuesta.

    Esta función divide el intervalo [a, b] en N subintervalos (debe ser par) y calcula la suma de las áreas
    bajo la curva utilizando la regla de Simpson en cada subintervalo. La precisión del resultado depende del
    número de subintervalos (N) utilizados.

    Sintaxis:
        I = simpson_compuesto(f, a, b, N)

    Parámetros:
    ----------
    f : callable
        Función a integrar. Debe ser una función que tome un solo argumento (x) y devuelva un valor numérico.
        Ejemplo: f = lambda x: x**2

    a : float
        Límite inferior de integración. Debe ser un número real que represente el inicio del intervalo.

    b : float
        Límite superior de integración. Debe ser un número real que represente el final del intervalo.

    N : int
        Número de subintervalos en los que se divide el intervalo [a, b]. Debe ser un entero par para garantizar
        que se utilice la regla de Simpson de manera adecuada.

    Retorna:
    --------
    I : float
        Aproximación numérica de la integral definida de f(x) en el intervalo [a, b].
        El resultado es un número real que representa el área bajo la curva de f entre los límites a y b.

    Notas:
    ------
    - Este método utiliza la regla de Simpson en cada subintervalo, lo que mejora la precisión en comparación
      con el uso de la regla del trapecio.
    - Es esencial que el número de subintervalos (N) sea par para que la regla de Simpson se aplique correctamente.
    - La función debe ser continua en el intervalo [a, b] para garantizar la validez del método.
    """

    I = 0.0
    h = (b - a) / N

    # Calcular el valor de la integral en cada subintervalo
    for k in range(N):
        x_k = a + k * h
        x_k1 = a + (k + 1) * h
        I += simpson(f, x_k, x_k1)

    return I
