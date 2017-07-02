# -*- coding: utf-8 -*-



from VehiculeIAA import *
from VehiculeIAB import *
from VehiculeIAC import *
from VehiculeControle import *
from Terrain import *
import time
import os 
class Circuit(list) :
    """
    Classe gérant le déroulement du jeu. 
    
    """
        
    Couche_terrain = 0    
    Couche_vehicules=1

    carburant=-1
    mur=-2
    vide=0
    def __init__(self,nomCircuit,nbv,nbt):
        
        self.lastWayPoint=0
        
        self.__plateau=self.chargerCircuit(nomCircuit)
        self.__xmax = len(self.__plateau[0])-1
        self.__ymax = len(self.__plateau)-1
        
        self.nbtours =  nbt

        self.PointClef={}


        nbv = min(nbv,7)# on limite le nombre de voitures pour une course 



        for i in range(nbv):
        
#            if i%2==1:
#    
#               self.append(SmartCarB(self.coordonneesWayPoint(1)[0],self.coordonneesWayPoint(1)[1], self))
#            else:
                choix = np.random.rand()
                

                wayPoint_coordonnees=self.coordonneesWayPoint(i+1)
                print( " i {} {}".format(i+1,wayPoint_coordonnees))
                if choix >0.76:                 
                    car=VehiculeIAA(wayPoint_coordonnees[0],wayPoint_coordonnees[1], self,3)
                elif choix >0.43:                 
                    car=VehiculeIAB(wayPoint_coordonnees[0],wayPoint_coordonnees[1], self,3)

                else:
                    car=VehiculeIAC(wayPoint_coordonnees[0],wayPoint_coordonnees[1], self,3)
#                       
#                    
                self.append(car)
                car.rang=len(self)
                self.plateau[wayPoint_coordonnees[1],wayPoint_coordonnees[0],Circuit.Couche_vehicules]=car

        self.courseFinie=False                          
        self.heurede_depart= 0#time.time()           

    def chargerCircuit(self,nom):
        """charge un circuit 
        
        paramètres : nomdufichier
        renvoie : un tableau contenant le circuit
        
        """
#        try :
            
        f=open(os.getcwd()+"\\circuits\\"+nom)
        dic={" ":0,"M":-1,"C":1,"*":2}
        plateau=[]
        i=0
        j=0
        
        for ligne  in f:
            ligne=ligne.replace("\n","").replace("*","")
            ligneP=[]

            for c in ligne.split("-") :
                donnees=c.split('_')
                nature,numero=donnees[0],int(donnees[1])
                cellule=[]                
#                if nature=='':
#                    cellule.append(Mur(self,(j,i),numero))
                print(nature)     
                if nature=='C':
                    cellule.append(Carburant(self,(j,i),numero))
                    
                elif nature=='G':
                    cellule.append(Goudron(self,(j,i),numero))                                        
                elif nature=='H':
                    cellule.append(Herbe(self,(j,i),numero))                    
                elif nature=='M':
                    cellule.append(Mur(self,(j,i),numero)) 
                elif nature=='O':
                    cellule.append(Moule(self,(j,i),numero))                     
                elif nature=='R':
                    cellule.append(Carburant(self,(j,i),numero))                       

                self.lastWayPoint=max(numero,self.lastWayPoint)
                    
                cellule.append(None) # couche voiture 
                ligneP.append(cellule)
                j+=1
                
            plateau.append(ligneP)  
            i+=1
            j=0
#            print(ligne,end='')
#        print("plateau")    
        print(plateau)    
        return np.array(plateau)
#        except Exception as e :
#            print(str(e) )               
        


       
    @property
    def dims(self):
        """
        Renvoies les dimensions du plateau de jeu
        """
        return (self.__xmax, self.__ymax)        
        
        
        
            
    def case(self,x,y):
        """
        méthode qui retourne la nature de la case  x,y 
        
        Paramètres
        ----------
        x colonne ,y ligne 
        
        Renvoie
        -------
        1 si contient de la nourriture          
        """
        return self.__plateau[y,x,Circuit.Couche_terrain]  

    def estSurLeCircuit(self,x,y):
        
        return y<len(self.plateau) and x<len(self.plateau[y])
        
        

    def estCarbur(self,x,y):
        """
        méthode qui retourne True si la nature de la case  x,y est carburant 
        
        Paramètres
        ----------
        x colonne ,y ligne 
        
        Renvoie
        -------
        True  si contient du carburant False sinon        
        """
        return self.estSurLeCircuit(x,y) and self.__plateau[y,x,Circuit.Couche_terrain]==self.carburant     
    def estMur(self,x,y):
        """
        méthode qui retourne True si la nature de la case  x,y est carburant 
        
        Paramètres
        ----------
        x colonne ,y ligne 
        
        Renvoie
        -------
        boolean          
        """
        return  self.estSurLeCircuit(x,y) and self.__plateau[y,x,Circuit.Couche_terrain]==self.mur   
    def estSol(self,x,y):
        """
        méthode qui retourne True si la nature de la case  x,y est sol 
        
        Paramètres
        ----------
        x colonne ,y ligne 
        
        Renvoie
        -------
        
        """
        return   self.estSurLeCircuit(x,y) and self.__plateau[y,x,Circuit.Couche_terrain]==self.vide        
        
    def estWayPoint(self,x,y):
        """
        méthode qui retourne True si la nature de la case  x,y est carburant 
        
        Paramètres
        ----------
        x colonne ,y ligne 
        
        Renvoie
        -------
        1 si contient de la nourriture          
        """
        return    self.estSurLeCircuit(x,y) and not self.estCarbur(x,y) and not  self.estMur(x,y) and not self.estSol(x,y) 
           
    def vue(self,x,y,r):
        """
        méthode qui retourne une liste de case trouve à une distance r du point de coordonnes (x,y)
        
        Paramètres
        ----------
        x colonne ,y ligne , r distance 
        
        Renvoie
        -------
        une liste         
        """     
        
        #listeR=self.plateau[x-r,x+r,y-r:y+r,Circuit.Couche_terrain]   
        liste=[]
        debutx=max(0,x-r)
        finx=min(x+r,self.__xmax)        
        debuty=max(y-r,0)
        finy=min(y+r,self.__ymax)    

        for j in range(debuty,finy):
            for i in range(debutx,finx):
                       if  ((i-x)**2+(j-y)**2)**0.5<=r   :
                           liste.append([i,j])
        debug.dprint("liste ")                   
        debug.dprint(liste)                       
        return liste
    def vueVehicules(self,x,y,r):
        """
        méthode qui retourne une liste de vehicules trouve à une distance r du point de coordonnes (x,y)
        
        Paramètres
        ----------
        x colonne ,y ligne , r distance 
        
        Renvoie
        -------
        une liste         
        """        
        liste=[]
        for v in self :
   
               if  ((v.x-x)**2+(v.y-y)**2)**0.5<=r   :
                   liste.append(v)
                           
        return liste 



                          
    @property                      
    def  plateau(self):
        """
        méthode qui retourne le plateau de jeu
        Paramètres
        ----------
        aucun
        
        Renvoie
        -------
        rien          
        """      
        return self.__plateau
        
        
    def lancerCourse(self):  
        
        
        self.heurede_depart=time.time()
        for v in self :
            
            v.departTour=self.heurede_depart
            
            
            
        
    def simuler (self):
        """
        Contrôle l'évolution du jeu, affiche le résultat de chaque tour dans
        un terminal.
        
        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        Rien  
        """
        
        for t in range(self.nbtours):
            debug.dprint("### Tour %i ###"%(t))
            self.unTour()
            debug.dprint(self)
            time.sleep(0.02)
    def coordonneesWayPoint(self,numero,typeT='G'):
        
        """
        retourne les coordonnées d'un  wayPoints connaissant son numéro par défaut un recherche le type goudron
        
        Paramètres: num: int numéro du wayPoint
        
        Renvoie :x,ycoordonnées
        """
        print(" numero i {} ".format(numero))
        for j in range(len(self.__plateau)):
            for i in range(len(self.__plateau[j])):
                debug.dprint(self.plateau[j,i,Circuit.Couche_terrain].numeroWayPoint)
                debug.dprint(self.plateau[j,i,Circuit.Couche_terrain].numeroWayPoint==numero)
                if self.plateau[j,i,Circuit.Couche_terrain].numeroWayPoint==numero and self.plateau[j,i,Circuit.Couche_terrain].getCaractere()==typeT:

                      return i,j  
            
                      
                      
                      
    def numeroWayPoint(self,i,j):
        
        """
        retourne les coordonnées d'un  wayPoints connaissant son numéro
        
        Paramètres: num: int numéro du wayPoint
        
        Renvoie :x,ycoordonnées
        """
            
        
        return self.__plateau[j,i,Circuit.Couche_terrain].numeroWayPoint  

        
        
        
    def __str__(self):
        """
        Conversion en chaîne avec deux caractères par case.
        """
        pos = {}
        for v in self:
            pos[v.coords]=v.typeV

        s = ""
   
        for j in range(len(self.__plateau)):
            for i in range(len(self.__plateau[j])):
                
                
                if self.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='C':
                    if (i, j) in pos:
                        s +="X"  # lorsqu'une voiture se recharge en carburant                
                    else:
                         s += "C" 
                elif (i, j) in pos:
                    s += pos[(i,j)]
                   
                     
                elif self.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='M':
                  
                     s += "M"
                elif self.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='G':
                  
                     s += "."                     

                else:
                    s += "*"
            s += "\n"
        return s
        



    def unTour(self):
        """
        Effectue toutes les actions liées à un tour de jeu.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        Rien
        """
        
        # rnd.shuffle(self)    Utile si gestion des collisions
        for v in self:  # fonctionne car Ecosysteme descend de list

#            if v.nombreTourE>=self.nbtours:
#             break ; 
#             
            v.detectCollision()
            if v.nombreTourE<=self.nbtours:# s'il a fini de courir
            
    
                v.dureeTotale=time.time()-self.heurede_depart                  
                v.deplacer()  
                cord=self.coordonneesWayPoint(v.numWayPointDepat)
      
                if distance(cord,v.coords)<=v.vitesse*3 and time.time()-v.departTour>4 and v.vitesse >0 :
                   v.nombreTourE+=1
                   if round(v.meilleurTemps)!=0:#voir le meilleur temps
                        v.meilleurTemps=min(v.meilleurTemps,time.time()-v.departTour)
                        v.departTour=time.time()
                   else :# au départ le compte de tour s'incrémente donc on ne considére pas le temps fait  
    
                        v.meilleurTemps=time.time()-self.heurede_depart 
                        v.departTour=time.time()          
                         
                debug.dprint(" id {}  rang {} nombre de tours effectués {}  meilleur temps {} ".format(v.id,v.rang,v.nombreTourE,v.meilleurTemps))    
    
    
            self.Tri_Selection()
         

    def Tri_Selection(self):
            l=self
            """ permet de faire un classement temporaire voiture ayant effectué le plus grand nombre de tours
                Tri Selection - O(n^2) """
            for i in range(len(l)-1):
                mini=i
                for j in range(i+1,len(l)):
                   # if l[j]<l[mini]: mini=j
                    if l[j].cmp(l[mini])==1: mini=j
                l[mini],l[i]=l[i],l[mini]
                l[i].rang=i+1    
            l[-1].rang=len(self)
    def Tri_finale(self):
            l=self
            """
            cette fonction permet de faire le classement final dépandant du meilleur temps
            et du temps mis pour faire tous les tours
                Tri Selection - O(n^2) """
            for i in range(len(l)-1):
                mini=i
                for j in range(i+1,len(l)):

                    if l[j].meilleurTemps+l[j].dureeTotale<l[mini].meilleurTemps+l[mini].dureeTotale : mini=j
                l[mini],l[i]=l[i],l[mini]
                l[i].rang=mini+1    
           
                
                
if __name__ == "__main__":
    nbv =1
    nbtour =2
    cir= Circuit("circuit9.txt",nbv,nbtour)           
    print(cir)
    cir.simuler()        
              
        
        
        
    
    