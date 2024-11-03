from .simpson_compuesto import simpson_compuesto


def simpson_compuesto_iterativo(f, a, b, tol, iterMax):
    """
    Aproxima el valor numérico de la integral definida de f(x) en el intervalo [a, b]
    utilizando la regla de Simpson compuesta de forma iterativa.

    Este método ajusta el número de subintervalos hasta que la diferencia relativa entre
    dos aproximaciones consecutivas esté dentro de la tolerancia especificada.

    Sintaxis:
        I = simpson_compuesto_iterativo(f, a, b, tol, iterMax)

    Parámetros:
    ----------
    f : callable
        Función a integrar. Debe ser una función que tome un solo argumento (x) y devuelva un valor numérico.
        Ejemplo: f = lambda x: x**2

    a : float
        Límite inferior de integración. Debe ser un número real que representa el inicio del intervalo.

    b : float
        Límite superior de integración. Debe ser un número real que representa el final del intervalo.

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
    - Este método aplica la regla de Simpson en cada subintervalo, aumentando el número de subintervalos
      hasta que se cumpla el criterio de tolerancia.
    - Si se alcanza iterMax sin cumplir la tolerancia, se devolverá la última aproximación calculada.
    """

    # Inicializar variables
    N = 2  # Comenzar con 2 subintervalos (debe ser par)
    I_old = simpson_compuesto(f, a, b, N)  # Aproximación inicial

    for k in range(iterMax):
        # Aumentar el número de subintervalos en 2 para mantenerlo par
        N += 2
        I_new = simpson_compuesto(f, a, b, N)  # Calcular nueva aproximación

        # Verificar el criterio de parada
        if abs(I_new - I_old) / abs(I_new) < tol:
            return I_new  # Si cumple el criterio de tolerancia, retornar resultado

        # Actualizar I_old para la próxima iteración
        I_old = I_new

    # Si no se cumple el criterio de tolerancia, retornar la última aproximación
    return I_old