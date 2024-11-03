def simpson(f, a, b):
    """
    Calcula la aproximación de la integral definida de f(x) en el intervalo [a, b] utilizando la regla de Simpson.

    Esta función estima el área bajo la curva de la función f(x) entre los límites a y b
    utilizando un único par de subintervalos y el valor de la función en el punto medio.

    Sintaxis:
        I = simpson(f, a, b)

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
    I : float
        Aproximación numérica de la integral definida de f(x) en el intervalo [a, b].
        El resultado es un número real que representa el área bajo la curva de f entre los límites a y b.

    Notas:
    ------
    - Este método solo calcula el área bajo la curva utilizando un único par de subintervalos.
      Para una mayor precisión, se recomienda utilizar la función `simpson_compuesto`,
      que divide el intervalo en múltiples subintervalos.
    - La función debe ser continua en el intervalo [a, b] para garantizar la validez del método.
    """

    I = (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))
    return I
