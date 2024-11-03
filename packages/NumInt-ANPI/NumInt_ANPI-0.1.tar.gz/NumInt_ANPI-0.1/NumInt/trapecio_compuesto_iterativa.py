import numpy as np

def trapecio_compuesto(f,a,b,n):
    """
    Sintaxis: I = trapecio_compuesto(f,a,b,n)

    Parameters
    ----------
    f: funcion de python
    a: real, limite izquierdo del intervalo
    b: real, limite derecho del intervalo
    n: real, numero de divisiones en intervalo 

    Returns
    -------
    I: aproximacion de la integral de f en intervalo [a,b]
    """
    h = (b-a)/n
    x_val = np.arange(a,b+h,h)

    suma = 0
    for i in range(len(x_val)-1):
        sub_a = x_val[i]
        sub_b = x_val[i+1]

        h = sub_b - sub_a

        suma = suma + (h/2)*(f(sub_a) + f(sub_b))

    return suma

def trapecio_compuesto_iterativo(f,a,b,tol,iterMax):
    """
    Sintaxis: I = trapecio_compuesto_iterativo(f,a,b,tol,iterMax)

    Paremeters
    ----------
    f: funcion de python
    a: real, limite izquierdo del intervalo
    b: real, limite derecho del intervalo
    tol: real, tolerancia
    iterMax: entero, numero de iteraciones maximas 

    Returns
    -------
    I: aproximacion de la integral de f en intervalo [a,b]
    """

    sk = trapecio_compuesto(f,a,b,2)
    iter = 0
    for k in range(3,iterMax+1):
        sk_1 = trapecio_compuesto(f,a,b,k)
        error = abs(sk_1 - sk)
        iter += 1
        if error < tol:
            break
        else:
            sk = sk_1
    return sk_1

"""
#Prueba
def fun(x):
    with np.errstate(invalid='ignore', divide='ignore'):
        if x >= 0:
            return np.log(np.arcsin(x)) / np.log(x) if x > 0 else np.nan
        else:
            return np.nan  # Return NaN for invalid x values

I = trapecio_compuesto_iterativo(fun,0.1,0.9,1e-6,2500)
print(I)
"""
    