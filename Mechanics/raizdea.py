# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:58 2020

@author: Camilo Martínez
"""
import math

def calcular_raiz_de_a(modo: str, Sut: float) -> float:
    if modo == 'f' or modo == 'a':
        return 0.246 - 3.08*math.pow(10, -3)*Sut + 1.51*math.pow(10, -5)*math.pow(Sut, 2) - 2.67*math.pow(10, -8)*math.pow(Sut, 3)
    else:
        return 0.190 - 2.51*math.pow(10, -3)*Sut + 1.35*math.pow(10, -5)*math.pow(Sut, 2) - 2.67*math.pow(10, -8)*math.pow(Sut, 3)

def main():
    Sut = float(input("Introduzca Sut en kpsi: "))
    modo = input("Flexión, axial o torsión (f, a, t): ")
    ra = calcular_raiz_de_a(modo, Sut)
    print("Raíz de a: " + str(ra))
    r = float(input("r = "))
    q = 1/(1 + ra/math.sqrt(r))
    print("q = " + str(q))
    Kt = float(input("Kt = "))
    Kf = 1 + q*(Kt - 1)
    print("Kf = " + str(Kf))

main()