

from scipy.special import roots_legendre
import numpy as np

def gaussiana_compuesta(f, a, b, M, N):
    """
    parámetros:
    f  -- función a integrar
    a, b -- límites del intervalo de integración [a, b]
    M  -- orden de la cuadratura de polinomio de Legendre (máximo 10)
    N  -- número de subintervalos en los que se divide [a, b]
    
    Retorna:
    I  -- aproximación de la integral
    """
    xi, wi = roots_legendre(M)
    h = (b - a) / N
    I = 0.0
    
    for i in range(N):
        x0 = a + i * h
        x1 = x0 + h
        x_= 0.5 * (x1 - x0) * xi + 0.5 * (x1 + x0)
        I += 0.5 * (x1 - x0) * np.sum(wi * f(x_))
    
    return I

def gaussiana_compuesta_iterativa(f, a, b, M, tol, iterMax):
    """
    parámetros:
    f  -- función a integrar
    a, b -- límites del intervalo de integración [a, b]
    M  -- orden de la cuadratura de polinomio de Legendre (máximo 10)
    tol -- tolerancia para la convergencia
    iterMax -- número máximo de iteraciones
    
    Retorna:
    I -- aproximación numérica de la integral
    """
    N = 1
    I_prev = gaussiana_compuesta(f, a, b, M, N)
    
    for iteration in range(iterMax):
        N *= 2
        I = gaussiana_compuesta(f, a, b, M, N)
        
        if abs(I - I_prev) < tol:
            return I
        
        I_prev = I
    
    print("no se alcanzó convergencia")
    return I


