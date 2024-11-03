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
    x_val = np.linspace(a,b,n)

    suma = 0
    for i in range(len(x_val)-1):
        sub_a = x_val[i]
        sub_b = x_val[i+1]

        h = sub_b - sub_a

        suma = suma + (h/2)*(f(sub_a) + f(sub_b))

    return suma

"""
#Prueba
def fun(x):
    val = np.log(np.arcsin(x)) / np.log(x) 
    return val 

I = trapecio_compuesto(fun,0.1,0.9,100)
print(I)
"""
