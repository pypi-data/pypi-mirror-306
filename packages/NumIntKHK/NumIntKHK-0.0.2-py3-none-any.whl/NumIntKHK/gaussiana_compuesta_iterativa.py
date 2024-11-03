from gaussiana_compuesta import gaussiana_compuesta


def gaussiana_compuesta_iterativa(f, a, b, M, tol, iterMax):
    """
    Aproxima el valor numérico de la integral definida de f(x) en el intervalo [a, b]
    utilizando la cuadratura gaussiana compuesta de forma iterativa.

    Este método ajusta el número de subintervalos hasta que la diferencia relativa entre
    dos aproximaciones consecutivas esté dentro de la tolerancia especificada.

    Sintaxis:
        I = gaussiana_compuesta_iterativa(f, a, b, M, tol, iterMax)

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

    tol : float
        Tolerancia para el criterio de parada. Debe ser un número positivo.

    iterMax : int
        Número máximo de iteraciones permitidas.

    Retorna:
    --------
    I : float
        Aproximación numérica de la integral definida de f(x) en el intervalo [a, b].

    Notas:
    ------
    - Este método aplica la cuadratura gaussiana en cada subintervalo, aumentando el número de subintervalos
      hasta que se cumpla el criterio de tolerancia.
    - Si se alcanza iterMax sin cumplir la tolerancia, se devolverá la última aproximación calculada.
    """

    # Verificar que la tolerancia sea positiva
    if tol <= 0:
        raise ValueError("La tolerancia debe ser un número positivo.")

    # Inicializar variables
    N = 1  # Comenzar con un subintervalo
    I_old = gaussiana_compuesta(f, a, b, M, N)  # Aproximación inicial

    for k in range(iterMax):
        # Aumentar el número de subintervalos en 1
        N += 1
        I_new = gaussiana_compuesta(f, a, b, M, N)  # Calcular nueva aproximación

        # Verificar el criterio de parada
        if abs(I_new - I_old) / abs(I_new) < tol:
            return I_new  # Si cumple el criterio de tolerancia, retornar resultado

        # Actualizar I_old para la próxima iteración
        I_old = I_new

    # Si no se cumple el criterio de tolerancia, retornar la última aproximación
    return I_old
