import numpy as np

def romberg(f, a, b, iterMax, tol):
  """
  Funcion que aproxima el valor de una integral definida utilizando el metodo
  de Romberg.

  Entradas:
      f: Funcion a integral.
      a: Limite inferior del intervalo.
      b: Limite superior del intervalo.
      iterMax: maximo de iteraciones.
      tol: tolerancia de error.

  Salida:
      Aproximación del valor de la integral definida.
  """
  Rant, Ract = [0] * iterMax, [0] * iterMax  

  h = b - a  
  Rant[0] =  h / 2 * (f(a) + f(b))  # Primera iteracion por regla del Trapecio

  for i in range(1, iterMax):
    h /= 2.
    sum_trap = 0
    
    # Aproximacion con la regla del Trapecio
    for k in range(1, 2**(i-1) + 1):
      sum_trap += f(a + (2 * k - 1) * h)
    Ract[0] = h * sum_trap + Rant[0] / 2  # R(i,0)

    for j in range(1, i + 1):
      Ract[j] = (4**j * Ract[j - 1] - Rant[j - 1]) / (4**j - 1)  # R(i,j)

    # Extrapolacion
    if i > 1 and abs(Rant[i - 1] - Ract[i]) < tol:
      return Ract[i]

    Rant, Ract = Ract, Rant

  return Rant[iterMax - 1]
