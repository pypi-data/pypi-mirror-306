def romberg(f, a, b, n):
    """
    Implementa el método de integración de Romberg para aproximar una integral definida.
    
    Parámetros:
    -----------
    f : función
        La función a integrar. Debe ser una función continua en el intervalo [a,b].
    a : float
        Límite inferior del intervalo de integración.
    b : float
        Límite superior del intervalo de integración.
    n : int
        Número de filas en la tabla de Romberg (n > 0).
        
    Retorna:
    --------
    R : list of list
        Tabla de Romberg con las aproximaciones sucesivas.
        R[i][j] contiene la aproximación de orden O(h^(2j))
    """
    
    # Inicializar la tabla de Romberg
    R = [[0] * (n) for _ in range(n)]
    h = b - a
    
    # Calcular R[0][0] usando la regla trapezoidal con un solo intervalo
    R[0][0] = h/2 * (f(a) + f(b))
    
    # Llenar la primera columna de R usando la regla trapezoidal compuesta
    for i in range(1, n):
        h = h/2
        # Calcular los nuevos puntos para esta iteración
        suma = 0
        for k in range(1, 2**(i), 2):
            suma += f(a + k*h)
            
        # Usar la fórmula recursiva para R[i][0]
        R[i][0] = R[i-1][0]/2 + h*suma
        
        # Calcular las extrapolaciones usando la fórmula de Richardson
        for j in range(1, i+1):
            R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1])/(4**j - 1)
    
    return R

def print_romberg_table(R):
    """
    Imprime la tabla de Romberg de forma legible.
    
    Parámetros:
    -----------
    R : list of list
        Tabla de Romberg generada por la función romberg()
    """
    n = len(R)
    for i in range(n):
        for j in range(i+1):
            print(f"{R[i][j]:.10f}", end="\t")
        print()

# Ejemplo de uso
if __name__ == "__main__":
    import math
    
    # Ejemplo 1: Integrar sin(x) de 0 a pi
    def test_sin():
        print("Ejemplo 1: Integrar sin(x) de 0 a pi")
        result = romberg(math.sin, 0, math.pi, 6)
        print_romberg_table(result)
        print(f"Mejor aproximacion: {result[-1][-1]}")
        print(f"Valor exacto: 2.0")
        print()

    # Ejemplo 2: Integrar x^2 de 0 a 1
    def test_square():
        print("Ejemplo 2: Integrar x^2 de 0 a 1")
        result = romberg(lambda x: x**2, 0, 1, 4)
        print_romberg_table(result)
        print(f"Mejor aproximacion: {result[-1][-1]}")
        print(f"Valor exacto: {1/3}")
        print()

    # Ejecutar ejemplos
    test_sin()
    test_square()