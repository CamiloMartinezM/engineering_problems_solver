# -*- coding: utf-8 -*-
"""
Created on April 18, 2020

@author: Camilo Martínez
"""
from scipy import interpolate
from warnings import warn

class Material:

    def __init__(self, Sy: float, Sut: float, Sc: float, units: str) -> None:
        self.Sy = Sy
        self.Sut = Sut
        self.Sc = Sc
        self.units = units
        self.Se = self.get_Se_prime()
        self.f = FatigueStrengthFactor(self.Sut, self.units).value
        
    def get_Se_prime(self) -> float:
        if self.units == 'kpsi':
            if self.Sut <= 200:
                return 0.5*self.Sut
            else:
                return 100
        else: # MPa
            if self.Sut <= 1400:
                return 0.5*self.Sut
            else:
                return 700

class FatigueStrengthFactor:

    def __init__(self, Sut: float, units: str) -> None:
        self.Sut = Sut
        self.units = units
        self.value = self.get_value()
        
    def get_value(self):
        conversion_factor = 1
        
        if self.units != 'kpsi': # MPa
            conversion_factor = 6.89476
            
        self.x = [70, 80, 90, 100, 110, 120, 130, 140, 150, 160,  170, 184, 190, 200]
        self.x = [i*conversion_factor for i in self.x]
        self.y = [0.9, 0.875,0.8575, 0.844, 0.83, 0.82, 0.816, 0.805, 0.7975, 0.791, 0.787, 0.78, 0.7775, 0.774]
        
        self.interpolating_function = interpolate.interp1d(self.x, self.y, kind=3, fill_value='extrapolate')

        if self.Sut < 70*conversion_factor:
            value = 0.9
        else:
            value = self.interpolating_function(self.Sut).tolist()    
        
        if self.Sut > 200*conversion_factor:
            warn("Sut is greater than 200 kpsi. An aproximate fatigue strength factor will be extrapolated.")
            
        return value