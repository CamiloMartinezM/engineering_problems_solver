# -*- coding: utf-8 -*-
"""
Created on April 8, 2020.

@author: Camilo Martínez
"""
from typing import List
import numpy as np
import math

class BucklingCalculator:
    """ Calculates various buckling parameters and finally determines whether buckling
        will occur.

        Refer to Chapter 4-11 - 4-15 of Shigley's Mechanical Engineering Design (pags. 175-183).
    """

    def __init__(self, inf_bdry_condition: str, sup_bdry_condition: str, l: float, cross_section: List[List], E: float, Sy: float, req_conservativeness: int = 3, axis: str = 'x') -> None:
        """       
        Args:
            inf_bdry_condition (str): Fixed or Pinned.
            sup_bdry_condition (str): Fixed, Pinned or Free.
            l (float): Length of column.
            cross_section (List[List[str, float]]): Cross-section parameters and dimensions.
                                                    The first element must be a str, that denotes the type of cross-
                                                    sectional area (circular, square, I-shaped, T-shaped). The second 
                                                    element must be a list, which contains the necessary dimensions
                                                    to fully define the cross-sectional area.
            E (float): Young's modulus of material.
            Sy (float): Yield strength of column material.
            req_conservativeness (int, optional): 1 for theoretical-, 2 for conservative- and 3 for recommended value. 
                                                  Defaults for 3.
            axis (str, optional): 'x' for x axis, 'y' for y axis.
        """
        # Material properties
        self.E = E*math.pow(10, 9)
        self.Sy = Sy*math.pow(10, 6)

        # Boundary conditions
        self.inf_bdry_condition = inf_bdry_condition.strip().lower()
        self.sup_bdry_condition = sup_bdry_condition.strip().lower()

        # Geometry
        self.l = l
        self.cross_section_type = cross_section[0]
        self.cross_section_dimensions = cross_section[1]
        self.C = self.calculate_C(req_conservativeness)
        self.A = self.calculate_area()
        self.I = self.calculate_inertia(axis)
        self.k = self.calculate_k()
        self.lk = self.calculate_slenderness()
        self.lk1 = self.calculate_minimum_slenderness()

        # Critical stresses
        self.johnson_critical_stress = self.calculate_johnson_critical_stress()
        self.euler_critical_stress = self.calculate_euler_critical_stress()

    def calculate_C(self, req_conservativeness: int) -> float:
        """ Calculates the constant C depending on the boundary conditions.

                        Theoretical     Conservative    Recommended
        Fixed-Free:         1/4             1/4             1/4
        Pinned-Pinned:       1               1               1
        Fixed-Pinned:        2               1              1.2
        Fixed-Fixed:         4               1              1.2
        
        Args:
            req_conservativeness (int): 1 for theoretical-, 2 for conservative- and 3 for recommended value.
        
        Returns:
            float: Constant C value.
        """
        if self.inf_bdry_condition == "fixed" and self.sup_bdry_condition == "free":
            return 1/4
        elif self.inf_bdry_condition == "pinned" and self.sup_bdry_condition == "pinned":
            return 1
        elif self.inf_bdry_condition == "fixed" and self.sup_bdry_condition == "pinned":
            if req_conservativeness == 1:
                return 2
            elif req_conservativeness == 2:
                return 1
            else:
                return 1.2
        elif self.inf_bdry_condition == "fixed" and self.sup_bdry_condition == "fixed":
            if req_conservativeness == 1:
                return 4
            elif req_conservativeness == 2:
                return 1
            else:
                return 1.2
        else: # Never happens
            return 1

    def calculate_euler_critical_stress(self) -> float:
        """ Calculates the critical stress for buckling according to Euler's theory.
        
        sigma_cr = P_cr/A = C*pi^2*E/(l/k)^2 (Euler's Theory)

        Returns:
            float: sigma_cr.
        """
        return self.C*(np.pi**2)*self.E/(self.lk**2)

    def calculate_johnson_critical_stress(self) -> float:
        """ Calculates the critical stress for buckling according to Johnson's theory.
        
        sigma_cr = P_cr/A = Sy - 1/CE * (Sy*l/(2*pi*k))^2

        Returns:
            float: sigma_cr.
        """
        return self.Sy - 1/(self.C*self.E)*(self.Sy*self.l/(2*np.pi*self.k))**2

    def euler_theory_is_valid(self) -> bool:
        """        
        Returns:
            bool: True if Euler's theory use is valid. l/k > (l/k)_1
        """
        return self.lk > self.lk1

    def calculate_k(self) -> float:
        """ Calculates the radius of gyration.

        k = (I/A)^(1/2)

        Returns:
            float: Radius of gyration, k.
        """
        return np.sqrt(self.I/self.A)

    def calculate_slenderness(self) -> float:
        """ Calculates the slenderness of the column.

        Returns:
            float: Slenderness of column. l/k
        """
        return float(self.l/self.k)

    def calculate_minimum_slenderness(self) -> float:
        """ Calculates the minimum slenderness for which Euler's buckling theory holds true.
        
        (l/k_1) = (2*pi^2*CE/Sy)^(1/2)

        Returns:
            float: Minimum slenderness.
        """
        lk1 = np.sqrt(2*(np.pi**2)*self.C*self.E/self.Sy)
        return float(lk1)

    def calculate_area(self) -> float:
        """ Calculates the cross-sectional area.
        
        Returns:
            float: Cross-sectional area.
        """
        if self.cross_section_type == "circular":
            return float(np.pi/4*self.cross_section_dimensions[0]**2)
        elif self.cross_section_type == "square":
            return float(self.cross_section_dimensions[0]*self.cross_section_dimensions[1])
        else:
            return 0

    def calculate_inertia(self, axis: str) -> float:
        """ Calculates the second moment of area or moment of inertia around the specified axis.
        
        Args:
            axis (str): 'x' or 'y'.
        
        Returns:
            float: Moment of inertia.
        """
        if axis == 'x':
            return self.calculate_inertia_xx()
        else: # axis = 'y'
            return self.calculate_inertia_yy()

    def calculate_inertia_xx(self) -> float:
        """ Calculates the second moment of area or moment of inertia of the cross-sectional area around the x axis.
        
        If the cross-section type is circular, then cross_section_dimensions must be [d], where d is diameter.
        If it's square, then cross_section_dimensions must be [b, h], where b is width and h is height.

        Returns:
            float: Moment of inertia.
        """
        if self.cross_section_type == "circular":
            return float(np.pi/64*math.pow(self.cross_section_dimensions[0], 4))
        elif self.cross_section_type == "square":
            return float(self.cross_section_dimensions[0]*math.pow(self.cross_section_dimensions[1], 3)/12)
        else:
            return 0

    def calculate_inertia_yy(self) -> float:
        """ Calculates the second moment of area or moment of inertia of the cross-sectional area around the y axis.
        
        If the cross-section type is circular, then cross_section_dimensions must be [d], where d is diameter.
        If it's square, then cross_section_dimensions must be [b, h], where b is width and h is height.

        Returns:
            float: Moment of Inertia.
        """
        if self.cross_section_type == "circular":
            return float(np.pi/64*math.pow(self.cross_section_dimensions[0], 4))
        elif self.cross_section_type == "square":
            return float(math.pow(self.cross_section_dimensions[0], 3)*self.cross_section_dimensions[1]/12)
        else:
            return 0

    def get_recommended_theory(self) -> str:
        """        
        Returns:
            str: 'Euler's theory' if Euler's theory is valid. Otherwise, returns 'Johnson's theory'.
        """
        if self.euler_theory_is_valid():
            return "Euler's theory"
        else:
            return "Johnson's theory"

    @staticmethod
    def get_relative_error(cls, exp: float, theo: float) -> str:
        """ Gets the relative error in percent.
        
        e [%] = (exp - theo)/theo * 100%

        Args:
            exp (float): Obtained or experimental value.
            theo (float): Theoretical value.
        
        Returns:
            str: Relative error with 2 decimals and a percent sign.
        """
        return "{0:.2%}".format(np.abs(np.abs(exp - theo)/theo)*100)

    def get_results(self) -> str:
        """
        Returns:
            str: String which contains a report with all the results.
        """
        s = "\nGeometrical properties:\n"
        s += "\tA = " + str(self.A) + ' m^2\n'
        s += "\tIx = " + str(self.calculate_inertia_xx()*math.pow(1000, 4)) + ' mm^4\n'
        s += "\tIy = " + str(self.calculate_inertia_yy()*math.pow(1000, 4)) + ' mm^4\n'
        s += "\tk = " + str(self.k) + ' m\n'
        s += "\tl/k = " + str(self.lk) + '\n'
        s += "\t(l/k)_1 = " + str(self.lk1) + '\n'
        s += "\tC = " + str(self.C) + '\n'
        s += "\nMaterial properties:\n"
        s += "\tE = " + str(self.E/math.pow(10, 9)) + ' GPa\n'
        s += "\tSy = " + str(self.Sy/math.pow(10, 6)) + ' MPa\n'
        s += "\nEuler's theory:\n"
        s += "\tCritical stress = " + str(self.euler_critical_stress/math.pow(10, 6)) + ' MPa\n'
        s += "\tCritical load = " + str(self.euler_critical_stress*self.A/1000) + ' kN\n'

        if not self.euler_theory_is_valid():
            s += "\nJohnson's theory:\n"
            s += "\tCritical stress = " + str(self.johnson_critical_stress/math.pow(10, 6)) + ' MPa\n'
            s += "\tCritical load = " + str(self.johnson_critical_stress*self.A/1000) + ' kN\n'
            s += "\nRecommended theory to use in this case: " + self.get_recommended_theory() + '\n'
            s += "\nRelative error of Johnson's theory with respect to Euler's theory: " + \
                BucklingCalculator.get_relative_error(self, self.johnson_critical_stress, self.euler_critical_stress) + '\n'
            s += "Relative error of Euler's theory with respect to Johnson's theory: " + \
                BucklingCalculator.get_relative_error(self, self.euler_critical_stress, self.johnson_critical_stress)
        
        return s

def main():
    cross_section_type = int(input("Type of cross-sectional area (circular: 1, square: 2, I-shaped: 3, T-shaped: 4): "))
    if cross_section_type == 1:
        d = float(input("Diameter [m] = "))
        l = float(input("Length of column [m] = "))
        inf_cond = input("Inferior boundary condition (Fixed: f, Pinned: p): ")
        sup_cond = input("Superior boundary condition (Fixed: f, Pinned: p, Free: f): ")
        E = float(input("Young's modulus, E [GPa] = "))
        Sy = float(input("Yield strength, Sy [MPa] = "))

        BC = BucklingCalculator(inf_cond, sup_cond, l, ['circular', [d]], E, Sy)
        print(BC.get_results())