# -*- coding: utf-8 -*-

from Vehicule import *



class VehiculeIAB(Vehicule):
    
    """
    véhicule intélligent B
    """
        
    
    def __init__(self,x,y,circuit,vmax=5,capacite=200,orientation=0):
        
        
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
        return 'B'     
       
    def deplacer(self): 
       
        
        if self.reservoir<20:
         super().mouvCarburant() 
         print(self.vitesse)
         super().deplacer()
               
        else :    
         self.chercherChemin()
 
        
    def chercherChemin(self): 
        """
        chercher le prochain point 
     
        """

        
        liste=self._circuit.vue(self.x,self.y,4)
        
        listeSuppr=[]
        couche_vehicule= self._circuit.Couche_vehicules
   
        for  case in liste :
            #on élimine les cases infranchissbles les cases qui ne sont pas des waypoints 

            if    self._circuit.numeroWayPoint(case[0],case[1])==0 or ( self._circuit.numeroWayPoint(self.x,self.y)!=self._circuit.lastWayPoint and self._circuit.numeroWayPoint(case[0],case[1])<= self._circuit.numeroWayPoint(self.x,self.y)) or( self._circuit.numeroWayPoint(case[0],case[1])>= 5*self._circuit.numeroWayPoint(self.x,self.y) and self._circuit.numeroWayPoint(self.x,self.y)!=0) or self._circuit.plateau[case[1],case[0],couche_vehicule]!=None:#on élimine les points derrière
            
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
                                 
         
                
     
