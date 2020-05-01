# -*- coding: utf-8 -*-
"""
Created on March 23, 2020.

@author: Camilo Martínez
"""
from typing import List, Any, Union
import numpy as np

class FailureTheory:
    """ Parent class for all failure theories. 
    """
    def __init__(self, Sy: float, St: float, Sc: float, label: str) -> None:
        """       
        Args:
            Sy (float): Yield strength of material.
            St (float): Tensile yield strength of material.
            Sc (float): Compressive yield strength of material.
            label (str): Theory label (used in the diagram).
        """
        self.Sy = Sy
        self.St = St
        self.Sc = Sc
        self.label = label
        
class MaximumShearStress(FailureTheory):
    """ Maximum Shear Stress Theory for ductile materials or MSST.
    """
    def no_failure_region_equations(self) -> List[List[Union[str, Any]]]:
        """ Calculates the equations that define the region where failure doesn't occur.
        
        Returns:
            List[List[str, Any]]: List of lists which correspond to an equation. The first position 
            of each list must be a str.
        """
        eqns = list()
        eqns.append(['HorizontalLine', self.Sy, 0, self.Sy])
        eqns.append(['HorizontalLine', -self.Sy, -self.Sy, 0])
        eqns.append(['VerticalLine', self.Sy, 0, self.Sy])
        eqns.append(['VerticalLine', -self.Sy, 0, -self.Sy])
        eqns.append(['Equation', [1, self.Sy], -self.Sy, 0])
        eqns.append(['Equation', [1, -self.Sy], 0, self.Sy])
        return eqns
    
class DistortionEnergy(FailureTheory):
    """ Distortion Energy Theory for ductile materials or DET.
    """
    def no_failure_region_equations(self) -> List[List[Union[str, np.array]]]:
        """ Calculates the equations that define the region where failure doesn't occur.
        
        Returns:
            List[List[str, np.array]]: List of a list whose first element is a str and the second,
            a numpy array.
        """
        b = np.sqrt(6)*self.Sy/3    # Radius on the y-axis
        a = np.sqrt(2)*self.Sy      # Radius on the x-axis
        
        psi = np.pi/4               # Rotation angle
        
        t = np.linspace(0, 2*np.pi, 100)
        ellipse = np.array([a*np.cos(psi)*np.cos(t) - b*np.sin(t)*np.sin(psi), 
                            b*np.cos(psi)*np.sin(t) + a*np.cos(t)*np.sin(psi)])
        
        return [['Ellipse', ellipse]]

class CoulombMohr(FailureTheory):
    """ Coulomb-Mohr Theory for ductile materials or MCT.
    """
    def no_failure_region_equations(self) -> List[List[Union[str, Any]]]:
        """ Calculates the equations that define the region where failure doesn't occur.
    
        Returns:
            List[List[str, Any]]: List of lists which correspond to an equation. The first position 
            of each list must be a str.
        """
        eqns = list()
        eqns.append(['HorizontalLine', self.St, 0, self.St])
        eqns.append(['HorizontalLine', -self.Sc, -self.Sc, 0])
        eqns.append(['VerticalLine', self.St, 0, self.St])
        eqns.append(['VerticalLine', -self.Sc, 0, -self.Sc])
        eqns.append(['Equation', [self.St/self.Sc, self.St], -self.Sc, 0])
        eqns.append(['Equation', [self.Sc/self.St, -self.Sc], 0, self.St])
        return eqns