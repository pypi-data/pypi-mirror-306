from gaussiana import gaussiana

def gaussiana_compuesta(f, a, b, M, N):
    """
    Aproxima el valor numérico de la integral definida de f(x) en el intervalo [a, b] utilizando
    la cuadratura gaussiana compuesta, basada en la función de cuadratura gaussiana de orden M.

    Esta función divide el intervalo [a, b] en N subintervalos y calcula la suma de las áreas bajo
    la curva utilizando la cuadratura gaussiana en cada subintervalo. La precisión del resultado
    depende del orden de la cuadratura (M) y del número de subintervalos (N).

    Sintaxis:
        I = gaussiana_compuesta(f, a, b, M, N)

    Parámetros:
    ----------
    f : callable
        Función a integrar. Debe ser una función que tome un solo argumento (x) y devuelva un valor numérico.
        Ejemplo: f = lambda x: x**2

    a : float
        Límite inferior de integración. Debe ser un número real que representa el inicio del intervalo.

    b : float
        Límite superior de integración. Debe ser un número real que representa el final del intervalo.

    M : int
        Orden de la cuadratura gaussiana. Debe estar en el rango [2, 10].

    N : int
        Número de subintervalos en los que se divide el intervalo [a, b].

    Retorna:
    --------
    I : float
        Aproximación numérica de la integral definida de f(x) en el intervalo [a, b].

    Notas:
    ------
    - Este método aplica la cuadratura gaussiana en cada subintervalo, utilizando la función `gaussiana`.
    - El orden de cuadratura (M) debe estar en el rango [2, 10]. Si M está fuera de este rango,
      la función devolverá un error.
    """

    # Tamaño del subintervalo
    I = 0.0
    h = (b - a) / N


    # Calcular la integral en cada subintervalo
    for k in range(N):
        # Limites del subintervalo
        x_k = a + k * h
        x_k1 = x_k + h

        # Aplicar la cuadratura gaussiana en el subintervalo [x_k, x_k1]
        I += gaussiana(f, x_k, x_k1, M)

    return I
