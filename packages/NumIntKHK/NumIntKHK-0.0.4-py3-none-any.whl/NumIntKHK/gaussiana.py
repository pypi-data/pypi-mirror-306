from .ceros_pesos_cuad_gauss import ceros_pesos_cuad_gauss


def gaussiana(f, a, b, M):
    """
    Aproxima el valor de la integral definida de `f(x)` en el intervalo [a, b] usando cuadratura gaussiana de orden `M`.

    Este método transforma el intervalo de integración [a, b] al intervalo estándar [-1, 1], luego aplica los puntos y pesos
    calculados para `M` en [-1, 1] a través de una fórmula de transformación. El resultado es una aproximación numérica eficiente
    para integrales de funciones suaves o polinómicas en un intervalo finito.

    Sintaxis:
        I = gaussiana(f, a, b, M)

    Parámetros:
    -----------
    f : callable
        Función a integrar. Debe aceptar un argumento numérico y devolver un valor numérico.
        Ejemplo: `f = lambda x: x**2`

    a : float
        Límite inferior de integración. Debe ser un número real.

    b : float
        Límite superior de integración. Debe ser un número real.

    M : int
        Orden de la cuadratura gaussiana, es decir, el número de puntos de evaluación. Debe estar en el rango [2, 10].

    Retorna:
    --------
    I : float
        Aproximación numérica de la integral definida de `f(x)` en el intervalo [a, b].

    Notas:
    ------
    - Este método obtiene los puntos y pesos desde `ceros_pesos_cuad_gauss` y los utiliza para calcular una estimación de la integral.
    - Si `M` está fuera del rango [2, 10], la función generará un error de valor indicando el rango permitido.
    - La precisión de la cuadratura gaussiana aumenta con el orden `M`, pero también incrementa el costo computacional.
    - Ideal para integrales con funciones suaves, especialmente en un intervalo finito, ya que maximiza la precisión usando una cantidad óptima de evaluaciones.
    """

    # Obtener los ceros y pesos para el orden dado
    x, w = ceros_pesos_cuad_gauss(M)

    # Validar que tenemos valores de ceros y pesos
    if not x or not w:
        raise ValueError("El valor de M debe estar entre 2 y 10.")

    # Transformación del intervalo [a, b] a [-1, 1]
    I = 0.0
    for i in range(M):
        # Aplicar la transformación del punto
        xi = ((b - a) / 2) * x[i] + (b + a) / 2
        # Sumar el término ponderado en la integral
        I += w[i] * f(xi)

    # Escalar el resultado por (b - a) / 2
    I *= (b - a) / 2

    return I
