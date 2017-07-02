# -*- coding: utf-8 -*-
"""
Created on Wed May 17 21:10:47 2017

@author: jeffy_000
"""

from Vehicule import *
import time


class VehiculeIAD(Vehicule):
    

    def __init__(self,x,y,circuit,vmax=5,capacite=100,orientation=0):
        
        
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
        return 'D'     
           
       
    def deplacer(self): 
       
        
        if self.reservoir<10:
         super().mouvCarburant() 
         print(self.vitesse)
         super().deplacer()
               
        else :  
         print("prévision")   
         self.prevision() #chercherChemin()
         
    def prevision(self):

        lste=self._circuit.vue(self.x,self.y,10)
        lc=[]
        z = 0
#        print("liste ",lste)

        couche_terrain = self._circuit.Couche_terrain
        for i,case in enumerate(lste):
            if   self._circuit.plateau[case[1],case[0],couche_terrain].getCaractere()=='C' and self._circuit.numeroWayPoint(case[0],case[1])>= self._circuit.numeroWayPoint(self.x,self.y):
                z+=1
                lc.append(case)
            
            
        if z >=2  :
            
#            x,y = self.coords
            a=distance(self.coords,lc[1])
 
              
            if self.reservoir >= a*1.25 :
              self.chercherChemin()  
                
             
                                    
            else:
#                 print("carbure",self.reservoir," ",a*1.25," ",lc )
                # time.sleep(100)
                 l=lc[0]
                 pasx=0
                 pasy=0
                 if self.x<l[0] : 
                     pasx=1
                 elif self.x>l[0] :
                     pasx=-1
                 if self.y<l[1] : 
                     pasy=1
                 elif self.y>l[1] :
                     pasy=-1
                 debug.dprint(" id {} {}:({},{})  Waypoint {}  Point:({},{}) WayPoint {} vitesse :{} reservoir:{}".format(self.id,self.typeV,self.x,self.y,self._circuit.numeroWayPoint(self.x,self.y),l[0],l[1],self._circuit.numeroWayPoint(l[0],l[1]),self.vitesse,self.reservoir))
                 self.orientation=atan2(pasy,pasx)
    
                 self.vitesse=1
    
                 debug.dprint(self)                
                 
                 super().deplacer()

        else :
            
            self.chercherChemin()
        
        
 
        
 
        
    def chercherChemin(self): 
        """
        chercher le prochain point 
     
        """

        
        liste=self._circuit.vue(self.x,self.y,self.rayonVision)
        
        listeSuppr=[]
        couche_vehicule= self._circuit.Couche_vehicules
   
        for  case in liste :
            #on élimine les cases infranchissbles les cases qui ne sont pas sur le chemin à suivre  

            if    self._circuit.numeroWayPoint(case[0],case[1])==0 or ( self._circuit.numeroWayPoint(self.x,self.y)!=self._circuit.lastWayPoint and self._circuit.numeroWayPoint(case[0],case[1])<= self._circuit.numeroWayPoint(self.x,self.y)) or( self._circuit.numeroWayPoint(case[0],case[1])>= 5*self._circuit.numeroWayPoint(self.x,self.y) and self._circuit.numeroWayPoint(self.x,self.y)!=0) or ( self._circuit.numeroWayPoint(self.x,self.y)==self._circuit.lastWayPoint and self._circuit.numeroWayPoint(case[0],case[1])== self._circuit.numeroWayPoint(self.x,self.y)) or self._circuit.plateau[case[1],case[0],couche_vehicule]!=None:#on élimine les points derrière
            
                listeSuppr.append(case)

                
        for  case in listeSuppr:
           
                liste.remove(case)
         
        if len(liste)>=1:
             l=liste[0]

             for nour in liste :
               
                if distance((self.x,self.y),(l[0],l[1])) > distance((self.x,self.y),(nour[0],nour[1])):
                    l=nour
             pasx=0
             pasy=0
             if self.x<l[0] : 
                 pasx=1
             elif self.x>l[0] :
                 pasx=-1
             if self.y<l[1] : 
                 pasy=1
             elif self.y>l[1] :
                 pasy=-1
             debug.dprint(" id {} {}:({},{})  Waypoint {}  Point:({},{}) WayPoint {} vitesse :{} reservoir:{}".format(self.id,self.typeV,self.x,self.y,self._circuit.numeroWayPoint(self.x,self.y),l[0],l[1],self._circuit.numeroWayPoint(l[0],l[1]),self.vitesse,self.reservoir))
             self.orientation=atan2(pasy,pasx)

             self.vitesse=1

             debug.dprint(self)                
             
             super().deplacer()
           

             self.rayonVision=4
        else :#  on augemente le rayon de vision au cas ou toutes les cases sont occupées ou non franchissables
                self.rayonVision*=3
                         
                    
