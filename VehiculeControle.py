# -*- coding: utf-8 -*-

from Vehicule import *



class VehiculeControle(Vehicule):
    
    """
    cette classe représente la voiture que le joueur va conduire 
    """
    
    
    
    def __init__(self,x,y,circuit,vmax=1,capacite=100,orientation=0):
        
        
        super().__init__(x,y,circuit,vmax,capacite,orientation)
    
    @property    
    def typeV(self):

        """
        Renvoie le type du véhicule  .
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        c: str
            Le caractère représentant le type du véhicule.
        """
        return 'P'       


    def tournerGauche(self): 

        self.orientation-= (pi/4)

    def tournerDroite(self): 


         self.orientation+= (pi/4)
         
    def accelerer(self): 


         self.vitesse+=1
         
    def deccelerer(self): 


         self.vitesse-=1
         
         
