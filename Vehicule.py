# -*- coding: utf-8 -*-

from numpy.random import randint
from numpy import cos,sin,pi 
from math import atan2
from fonctions import *
from dprint import dprint
from abc import ABCMeta ,abstractmethod
import dprint as debug

class Vehicule(metaclass=ABCMeta):
    """
    Classe décrivant les comportement par défaut des véhilules. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements de
    déplacement différents.
    """    
    
    nbrVehicule=1# compte le noùnre d'instance de Vehicule afin de définir un id de chaque instance 
    def __init__(self,x,y,circuit,vmax=5,capacite=60,orientation=0):
        """
        Crée un animal aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles l'animal sera créé.
            
        capacité: int
            niveau de santé maximal du reservoir. Vaut 10 par défaut.
        orientation :orientation de la voiture 
        
            
        """
        self._circuit=circuit        
        self.id=0
        
        self.capacite_reservoir= capacite
        self.__reservoir= capacite
        self.coords=x,y 
        
        self.id=self.nbrVehicule
        self.numWayPointDepat= self._circuit.numeroWayPoint(x,y)

                

        self.orientation=orientation

        self.vitessemax=vmax
        
        self.__vitesse=0
      
        self._accelerationmax=self.vitessemax/10
        self.acceleration=0
        self.__masse=randint(200,1000)
        self.rang=1
        self.nombreTourE=0#  nombre de tours effectué par le véhicule
        self.meilleurTemps=0        #
        self.departTour=0
        self.dureeTotale=0               
        Vehicule.nbrVehicule+=1

        self.rayonVision=2
        


        
    
        
#    @abstractmethod      
    def deplacer(self):
       """
        Mouvement du véhicule 
        de la position courante. Utilise l'accesseur coords.
       """ 
       self.vitesse=self.acceleration+self.vitesse
       self.coords=int (self.coords[0]+round(self.vitesse*cos(self.orientation))),int (self.coords[1]+round(self.vitesse*sin(self.orientation)))


       
    def mouvAlea(self):
        """
       déplacer aléatoirement le véhicule
        """
        self.coords = (self.x+randint(-1,2),
        self.y+randint(-1,2))
       


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
            Le caractère représentant l'animal.
        """
        return 'V'       
       
    def __str__(self):
        
        """
        Affiche l'état courant du véhicule.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        s: str
            La chaîne de caractères qui sera affichée via ''print''
        """
        return " position ({}, {})  orientation : {}  vitesse:{} reservoir:".format(self.coords[0],self.coords[1],self.orientation*(180/3.14),self.__vitesse,self.__reservoir)
       
    @property    
    def  masse(self):
        """
        masse
        """
        return  self.__masse      
    @property    
    def  acceleration(self):
        """
        tuple contenant l'accélération  suivant x et y 
        """
        return  self.__acceleration
       
    @acceleration.setter

    def acceleration(self,nvaccelartion):
        """
        mis à jour de l'accélération en évitant 
        """
        debug.dprint(" nv acc  {} ".format(nvaccelartion))    
        a = nvaccelartion
        a = min(a,self._accelerationmax)
        a = max(a,0)

        self.__acceleration=a
    @property
    def vitesse(self):
        """
        vitesse: tuple float,float
            
           
        """
        return self.__vitesse     

    @vitesse.setter
    def vitesse(self, nvvitesse):
        """
        Met à jour le niveau de la vitesse  du véhicule. Garantit que la valeur arrive 
        dans l'intervalle [0, self.vitessemax]. Met à 0 les valeurs négatives, ne
        fait rien pour les valeurs trop grandes.
        """
        v = nvvitesse
        v = min(v,self.vitessemax)
        v = max(v,-self.vitessemax)

        self.__vitesse =v

    
    
    @property     
    def x(self):
        """
        x: nombre entier
            Abscisse de l'animal
        """        
        
        return self.__coords[0]

    @property     
    def y(self):
        """
        y: nombre entier
            Abscisse de l'animal
        """            
        return self.__coords[1]

        

        
    @property
    def coords(self):
        """
        coords: tuple
            Les coordonnées du véhicule sur le circuit 
        """
        return self.__coords


    @coords.setter
    def coords(self,nvcoords):
        """
        Met à jour les coordonnées du véhicule.
        Garantit qu'ils arrivent dans la zone définie par
        le circuit self._eco.
    
        Paramètres
        ----------
        nouv_coords : tuple représentant les coordonnées auquelles 
                      le véhicule  essaie de se rendre.
         
        
       """
        if self.__reservoir==0:
           return 
        x, y = nvcoords
        x = min(x,self._circuit.dims[0])
        x = max(x, 0)
        y = min(y, self._circuit.dims[1])
        y = max(y, 0)

        plateau = self._circuit.plateau
        couche_vehicules=self._circuit.Couche_vehicules
        couche_terrain=self._circuit.Couche_terrain

        # premier cas la voiture vient d' etre créee ert ne contient pas encore  le champ self.__coords
        
        if   self.id==0  :
            
            self.__coords =(x,y)
    
        
        elif   self.coords == (x,y):
           pass
#            # on applique une nouvelle fois l'action éventuelle liée à la case
#            plateau[x, y, couche_terrain].action(self)
#            return

            # si la destination est libre on y va
        elif plateau[y ,x,couche_terrain].getCaractere()=='M':

                # zone interdite
             debug.dprint("zone interdite")  
        
             
        elif plateau[y ,x,couche_vehicules] is None:
             plateau[y,x, couche_vehicules] = self
                # on  vide l'ancienne case
             plateau[self.coords[1], self.coords[0],couche_vehicules] = None

             self.__coords =(x,y)
             
                # on applique les éventuelles actions que la case peut avoir sur
                # l'animal
             #plateau[x, y, couche_terrain].action(self)
             self._circuit.plateau[y,x,couche_terrain].action(self)
                       
        else: 
                # pas de bol, la case a été prise entre le tour de décision
                # et le tour de mouvement
                # on applique à nouveau l'action de la case courante            
##                plateau[self.coords[0], self.coords[1],                             couche_terrain].action(self) 
                debug.dprint("La case (%i,%i) est occupée"%(x, y))

        
    @property
    def reservoir(self):
        """
        reservoir: float
            Le niveau de santé de l'animal. Si ce niveau arrive à 0 l'animal
            est marqué comme mort et sera retiré du plateau de jeu
        """
        return self.__reservoir
    
    @reservoir.setter
    def reservoir(self, value):
        """
        Met à jour le niveau de le reservoir du véhicule. Garantit que la valeur arrive 
        dans l'intervalle [0, self.capacite_reservoir]. Met à 0 les valeurs négatives, ne
        fait rien pour les valeurs trop grandes.
        """
        if value <=self.capacite_reservoir:
            self.__reservoir = value
        if value <= 0:  # <= car à  certaines vitesses le véhicule consomme  plus de 1 en carburant
             self.__reservoir = 0   # ce qui gèrera les décès plus tard
    
    def mouvCarburant(self):
        """
        dirigé le véhicule vers la  station de carburant la plus proche
        
        
        
        """
        debug.dprint(" id {} je cherche le car".format(self.id))
        liste=self._circuit.vue(self.x,self.y,10)

        listeSuppr=[]

        couche_terrain = self._circuit.Couche_terrain
        couche_vehicule= self._circuit.Couche_vehicules
        for  case in liste:
            if self._circuit.plateau[case[1],case[0],couche_vehicule]!=None or self._circuit.plateau[case[1],case[0],couche_terrain].getCaractere()!='C':
                listeSuppr.append(case)
                
        for  case in listeSuppr:
           
                liste.remove(case)
         
        if len(liste)>=1:
             l=liste[0]
             for nour in liste :
               
                if   distance((l[0],l[1]),(self.x,self.y))> distance((nour[0],nour[1]),(self.x,self.y)):
                    l=nour
             pasx=0
             pasy=0
             debug.dprint(" Pos :({},{}) car proche :({},{})".format(self.x,self.y,l[0],l[1]))
             if self.x<l[0] : 
                 pasx=1
             elif self.x>l[0] :
                 pasx=-1
             if self.y<l[1] : 
                 pasy=1
             elif self.y>l[1] :
                 pasy=-1
             self.orientation= atan2(pasy,pasx)
             self.vitesse=1
         


   
                 
    def detectCollision(self):
        """
        
        méthode qui detecte les collision ralenti la voiture qui est derrière 
        
        """
        other=self._circuit.vueVehicules(self.x,self.y,1)
        if len(other)>0  and other[0].id!=self.id:
            
            
            debug.dprint("collision!")
            other=other[0]


        
            if self._circuit.numeroWayPoint(self.x,self.y) >self._circuit.numeroWayPoint(other.x,other.y):
            
                self.vitesse=self.vitesse+other.vitesse

                self.orientation=self.orientation-pi/4
               # other.vitesse=-other.vitesse
               # other.acceleration=other.acceleration/5#=other.vitesse/4 
                other.orientation=other.orientation+pi/4

                self.deplacer()
                other.deplacer()
                

                
            else :
                
                other.vitesse=other.vitesse+self.vitesse
                other.orientation=other.orientation-pi/4
                #self.vitesse=-self.vitesse
                #self.acceleration=self.acceleration/5#self.vitesse/4 
                self.orientation=self.orientation+pi/4
#                self.acceleration=self.acceleration=0
                self.acceleration=0
                other.deplacer()
                self.deplacer()
                
                

        
        
    def cmp(self,other):
        
      if ( self.nombreTourE>other.nombreTourE or (self.nombreTourE==other.nombreTourE and self._circuit.numeroWayPoint(self.x,self.y)>self._circuit.numeroWayPoint(other.x,other.y))):
          
          return +1
                
      if ( self.nombreTourE<other.nombreTourE or (self.nombreTourE==other.nombreTourE and self.nombreTourE==other.nombreTourE and self._circuit.numeroWayPoint(self.x,self.y)<self._circuit.numeroWayPoint(other.x,other.y))) : 
            return -1
      return 0
    
                         
                    
                

        

    
    
    
    
    
                     






       
       
       
       
       
        
        