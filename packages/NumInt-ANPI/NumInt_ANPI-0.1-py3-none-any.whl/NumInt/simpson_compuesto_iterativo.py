import numpy as np
from .simpson_compuesto import simpson_compuesto

def simpson_compuesto_iterativo(f, a, b, tol=1e-5, iterMax=50):
    """
    Aproximación de la integral definida usando la Regla de Simpson Compuesta Iterativa.
    
    :param f: Función a integrar.
    :param a: Límite inferior de integración.
    :param b: Límite superior de integración.
    :param tol: Tolerancia para la precisión de la integral.
    :param iterMax: Número máximo de iteraciones.
    :return: Aproximación de la integral.
    """
    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior.")
    if tol <= 0:
        raise ValueError("La tolerancia debe ser un número positivo.")
    if iterMax <= 0:
        raise ValueError("El número máximo de iteraciones debe ser positivo.")

    # Número inicial de puntos (debe ser par)
    N = 2  # Comenzamos con un número par

    # Primer cálculo de la integral con N puntos
    I_old = simpson_compuesto(f, a, b, N)

    for i in range(iterMax):
        # Incrementamos el número de puntos para mayor precisión (debe ser par)
        N *= 2  # Aumentamos N para que sea siempre par
        
        # Calculamos la integral con el nuevo N
        I_new = simpson_compuesto(f, a, b, N)

        # Revisamos si la diferencia es menor que la tolerancia
        if abs(I_new - I_old) < tol:
            return I_new
        
        # Actualizamos el valor de la integral anterior
        I_old = I_new

    # Si se alcanza iterMax sin convergencia, retornamos el último valor calculado
    print("Advertencia: se alcanzó el número máximo de iteraciones.")
    return I_new
