# -*- coding: utf-8 -*-
"""
Module implémentant les différents terrains utilisés lors de la simulation
d'un terrain.
"""
from abc import ABC, abstractmethod
import random as rnd
from dprint import dprint

class Terrain(ABC):
    """
    Créé un case de type Terrain et la rattache à l'écosystème passé en 
    paramètres

    Paramètres
    ----------
    circuit: Circuit
        L'instance de circuit gérant la simulation à laquelle le terrain va
        se rattacher.
        
    coords: tuple
        Abscisse et ordonnée de la case dans la simulation
        
    Notes
    -----
    La classe Terrain étant abstraite ce sont ses classes filles qui doivent
    être instanciées.
    """
    Impact_sante_defaut = -1
    def __init__(self,circuit, coords,numeroWayPoint):
        self._circuit = circuit
        self.__coords = coords
        self.impact_sante = self.Impact_sante_defaut
        self.numeroWayPoint=numeroWayPoint
            
    @property
    def impact_sante(self):
        """
        impact_sante: float
            Chaque terrain modifie, en positif ou négatif, la santé de l'animal
            qui se trouve dessus suivant la règle suivante:
            'sante_animal += impact_sante''            
        """
        return self.__impact_sante
        
    @impact_sante.setter    
    def impact_sante(self, impact_sante):
        self.__impact_sante = impact_sante

    @property
    def coords(self):
        """      
        coords: tuple
            les coordonnées de la case dans la simulation en cours.

        Notes
        -----
        Cet attribut est en lecture seule, les coordonnées d'un terrain
        n'ont pas vocation à être modifiées en cours de simulation. Si
        besoin il faut instancier un nouveau terrain pour remplacer
        l'ancien.
        """
        return self.__coords
        
    @abstractmethod
    def action(self,Vehicule):
        """
        Lorsqu'un véhicule se positionne sur un terrain ce dernier peut avoir
        une influence sur le circuit  en question.
        
        Paramètres
        ----------
        véhicule: Vehicule
            le véhicule qui viste la case courante
            
        Renvoie
        -------
        Rien
        """
        pass
    def getCaractere(self):
        
        
        return 'T'


class Herbe(Terrain):
    """
    Une case ''Nourriture'' permet à chaque véhicule qui la visite de
    retrouver trois points de carburant, 
    """
    Impact_sante_defaut = -1.5
    def __init__(self, circuit, coords,numeroWayPoint):
        super().__init__(circuit, coords,numeroWayPoint)
        self.__stock = rnd.randint(1,10)
        
    def action(self,vehicule):

            vehicule.reservoir += self.impact_sante

    def getCaractere(self):
        
        
        return 'H'


                     
class Mur(Terrain):
    """
    Une case ''Mur '' qui es infranchissable, 
    """

    def __init__(self,circuit, coords,numeroWayPoint):
        super().__init__(circuit,coords,numeroWayPoint)

    def action(self,vehicule):

            vehicule.reservoir += self.impact_sante

       
    def getCaractere(self):
        
        
        return 'M'

                     
                     
class Carburant(Terrain):
    """
    Une case ''Carburant'' permet à chaque véhicule qui la visite de
    retrouver trois points de carburant, 
    """
    Impact_sante_defaut = +50
    def __init__(self,circuit, coords,numeroWayPoint):
        super().__init__(circuit, coords,numeroWayPoint)
        self.__stock =100# rnd.randint(1,10)
        
    
    def getCaractere(self):
        
        
        return 'C'
    def action(self, vehicule):
        if self.__stock:
            self.__stock -= 1
            vehicule.reservoir+= self.impact_sante
        else:
            #self._ecosysteme.cases_besoin_maj.append(self.coords)
            dprint("une case de carburant  vidée par " + str(vehicule))
      
 		

class Goudron(Terrain):
    """
    Une case ''Goudron  qui peut être un élément du chemin'' 
    """
    Impact_sante_defaut = -1.25
    def __init__(self,circuit,coords,numeroWayPoint):
        super().__init__(circuit, coords,numeroWayPoint)
        self.__stock = rnd.randint(1,10)
        
    def action(self,vehicule):

            vehicule.reservoir += self.impact_sante
      
    def getCaractere(self):
        
        
        return 'G'

class Moule(Terrain):
    """
    Une case ''Goudron  qui peut être un élément du chemin'' 
    """
    Impact_sante_defaut = -1
    def __init__(self,circuit,coords,numeroWayPoint):
        super().__init__(circuit, coords,numeroWayPoint)

        
    def action(self,vehicule):

            vehicule.sante += self.impact_sante
      
    def getCaractere(self):
        
        
        return 'O'

                                          