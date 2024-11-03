from .trapecio import trapecio


def trapecio_compuesto(f, a, b, N):
    """
    Aproxima el valor numérico de la integral definida de f(x) en el intervalo [a, b] utilizando la regla del trapecio compuesta.

    Esta función divide el intervalo [a, b] en N subintervalos y calcula la suma de las áreas de los trapecios formados en cada subintervalo.
    La precisión del resultado depende del número de subintervalos (N) utilizados.

    Sintaxis:
        I = trapecio_compuesto(f, a, b, N)

    Parámetros:
    ----------
    f : callable
        Función a integrar. Debe ser una función que tome un solo argumento (x) y devuelva un valor numérico.


    a : float
        Límite inferior de integración. Debe ser un número real que represente el inicio del intervalo.

    b : float
        Límite superior de integración. Debe ser un número real que represente el final del intervalo.

    N : int
        Número de subintervalos en los que se divide el intervalo [a, b]. Debe ser un entero positivo.

    Retorna:
    --------
    I : float
        Aproximación numérica de la integral definida de f(x) en el intervalo [a, b]. El resultado es un número real que representa el área bajo la curva de f en el intervalo especificado.

    Notas:
    ------
    - Se recomienda usar un número mayor de subintervalos (N) para obtener una mejor aproximación de la integral.
    - La función debe ser continua en el intervalo [a, b] para garantizar la validez del método.
    """

    I = 0.0
    h = (b - a) / N

    # Calcular el valor de la integral en cada subintervalo
    for k in range(N):
        x_k = a + k * h
        x_k1 = a + (k + 1) * h
        I += trapecio(f, x_k, x_k1)

    return I
