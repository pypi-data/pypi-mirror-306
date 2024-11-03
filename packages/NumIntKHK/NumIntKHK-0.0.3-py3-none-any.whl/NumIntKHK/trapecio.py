def trapecio(f, a, b):
    """
    Calcula el área bajo la curva utilizando la regla del trapecio.

    Esta función estima el área bajo la curva de la función f(x) entre los límites a y b
    utilizando un único trapecio, que se forma por los puntos (a, f(a)) y (b, f(b)).

    Sintaxis:
        area = trapecio(f, a, b)

    Parámetros:
    ----------
    f : callable
        Función a integrar. Debe ser una función que tome un solo argumento (x) y devuelva un valor numérico.
        Ejemplo: f = lambda x: x**2

    a : float
        Límite inferior de integración. Debe ser un número real que represente el inicio del intervalo.

    b : float
        Límite superior de integración. Debe ser un número real que represente el final del intervalo.

    Retorna:
    --------
    (f(a) + f(b)) * (b - a) / 2 : float
        Aproximación del área bajo la curva entre los puntos a y b. El resultado es un número real
        que representa el área del trapecio formado entre la función f y el eje x.

    Notas:
    ------
    - Este método solo calcula el área bajo la curva utilizando un único trapecio.
      Para una mayor precisión, se recomienda utilizar la función `trapecio_compuesto`,
      que divide el intervalo en múltiples subintervalos.
    - La función debe ser continua en el intervalo [a, b] para garantizar la validez del método.
    """

    return (f(a) + f(b)) * (b - a) / 2
