import numpy as np

def simpson_compuesto(f, a, b, N):
    """
     Aproximación de la integral definida usando la Regla de Simpson Compuesta.
    
    Parámetros:
    f : function : función f(x) a integrar
    a : float : límite inferior del intervalo
    b : float : límite superior del intervalo
    N : int : número de subintervalos 

    Retorna:
    I : float : aproximación de la integral
    """
    if N % 2 != 0:
        raise ValueError("N debe ser par")
    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior.")

    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    I = f(a) + f(b)  # f(a) y f(b)

    # Sumar los términos de los índices impares y pares
    for i in range(1, N, 2):
        I += 4 * f(x[i])  # términos de índice impar
    for i in range(2, N - 1, 2):
        I += 2 * f(x[i])  # términos de índice par

    I *= h / 3  # multiplicar por h/3
    return I