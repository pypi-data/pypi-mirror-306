def ceros_pesos_cuad_gauss(n):
    """
    Calcula los ceros (puntos) y pesos para la cuadratura gaussiana de orden `n`, utilizados en métodos de integración numérica.

    La cuadratura gaussiana es un método para aproximar el valor de una integral definida. Este método selecciona puntos y pesos óptimos
    para maximizar la precisión en el intervalo [-1, 1] y es especialmente eficiente en integrales de funciones polinómicas.

    Sintaxis:
        (x, w) = ceros_pesos_cuad_gauss(n)

    Parámetros:
    -----------
    n : int
        Orden de la cuadratura gaussiana, es decir, el número de puntos. Debe ser un entero en el rango [2, 10].

    Retorna:
    --------
    (x, w) : tuple
        Una tupla que contiene dos listas:
            - x : list of float
                Lista de ceros (puntos) de la cuadratura gaussiana en el intervalo [-1, 1], donde se evalúa la función.
            - w : list of float
                Lista de pesos correspondientes a cada punto, que ponderan las contribuciones de `f(x)` en la integral.

    Notas:
    ------
    - Si `n` está fuera del rango [2, 10], la función devuelve listas vacías y muestra un mensaje de advertencia.
    - Los puntos y pesos están predefinidos para valores de `n` entre 2 y 10, asegurando una máxima precisión para integrales en [-1, 1].
    - Este método es ideal para integrales en el intervalo estándar [-1, 1]. Para otros intervalos, se deben aplicar transformaciones.
    """


    # Validar el rango de n
    if n < 2 or n > 10:
        print("El valor de n debe ser menor o igual a 10 y mayor o igual a 2.")
        return [], []

    # Inicializar los puntos y pesos
    x = []
    w = []

    # Asignar puntos y pesos de acuerdo a n
    if n == 2:
        x = [-0.5773502692, 0.5773502692]
        w = [1.0, 1.0]
    elif n == 3:
        x = [-0.7745966692, 0.0, 0.7745966692]
        w = [0.5555555555, 0.888888888, 0.5555555555]
    elif n == 4:
        x = [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116]
        w = [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]
    elif n == 5:
        x = [-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459]
        w = [0.2369268851, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268851]
    elif n == 6:
        x = [-0.9324695142, -0.6612093865, -0.2386191861, 0.2386191861, 0.6612093865, 0.9324695142]
        w = [0.1713244924, 0.3607615730, 0.4679139346, 0.4679139346, 0.3607615730, 0.1713244924]
    elif n == 7:
        x = [-0.9491079123, -0.7415311856, -0.4058451514, 0.0, 0.4058451514, 0.7415311856, 0.9491079123]
        w = [0.1294849662, 0.2797053915, 0.3818300505, 0.4179591837, 0.3818300505, 0.2797053915, 0.1294849662]
    elif n == 8:
        x = [-0.9602898565, -0.7966664774, -0.5255324099, -0.1834346425, 0.1834346425, 0.5255324099, 0.7966664774,
             0.9602898565]
        w = [0.1012285363, 0.2223810345, 0.3137066459, 0.3626837834, 0.3626837834, 0.3137066459, 0.2223810345,
             0.1012285363]
    elif n == 9:
        x = [-0.9681602395, -0.8360311073, -0.6133714327, -0.3242534234, 0.0, 0.3242534234, 0.6133714327, 0.8360311073,
             0.9681602395]
        w = [0.0812743883, 0.1806481607, 0.2606106964, 0.3123470770, 0.3302393550, 0.3123470770, 0.2606106964,
             0.1806481607, 0.0812743883]
    elif n == 10:
        x = [-0.9739065285, -0.8650633667, -0.6794095683, -0.4333953941, -0.1488743390, 0.1488743390, 0.4333953941,
             0.6794095683, 0.8650633667, 0.9739065285]
        w = [0.0666713443, 0.1494513492, 0.2190863625, 0.2692667193, 0.2955242247, 0.2955242247, 0.2692667193,
             0.2190863625, 0.1494513492, 0.0666713443]

    return x, w
