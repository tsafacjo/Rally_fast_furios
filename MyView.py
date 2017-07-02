# -*- coding: utf-8 -*-
import sys
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from Circuit  import *
import os 
from PyQt4 import QtGui, QtCore




from PyQt4.QtCore import *

class MyView(QtGui.QGraphicsView):
    
    
    

    def __init__(self,nbtour=5,Controle=0,nbv =4):
        
        nbv =nbv
        nbtour =nbtour

        l=20
        L=20
        
        self.Controle=Controle# pour savoir si le joueur a le contrôle ou si c'est un trounoi entre les intelligences artificielles
        self.cir= Circuit("circuit9.txt",nbv,nbtour)
        
        if self.Controle==1:
            self.joueur=VehiculeControle(self.cir.coordonneesWayPoint(len(self.cir))[0],self.cir.coordonneesWayPoint(len(self.cir))[1],self.cir,3)
            self.joueur.id="joueur1"        
            self.cir.append(self.joueur)
#    
        else :
            
         self.joueur=self.cir[0]    
      
        self.angleCamera=0
                
        
        chemin=os.getcwd()


        #on charge des images pour les voitures les obtacles ..
        self.imvoiture=QImage(chemin+"\\images\\car\\V7.png")
        self.imvoiture3=QImage(chemin+"\\images\\car\\V7.png")            
        self.imvoiture4=QImage(chemin+"\\images\\car\\V12.png") 
        self.imvoiture2=QImage(chemin+"\\images\\car\\V6.png")
        self.imCarbu=QImage(chemin+"\\images\\motifs\\tube1.png")
        self.imWall=QImage(chemin+"\\images\\motifs\\A3.png")#A3.png
        self.imSol=QImage(chemin+"\\images\\motifs\\mur.png")#herbe
        self.imR=QImage(chemin+"\\images\\motifs\\pisteA.png")
        self.imMoule=QImage(chemin+"\\images\\motifs\\Moule.png")        
        
        self.sprites={}
        self.sprites['A']=self.imvoiture2     

        self.sprites['B']=self.imvoiture 
        self.sprites['C']=self.imvoiture4         
    
        self.sprites['P']=self.imvoiture3 

        self.scalex,self.scaley=110,110

        self.scalecarx,self.scalecary=110,110
         

# à chque voiture on associe une image dépendant de son type  
        self.voitures=dict()
        
        self.periodeMiseAjour=200
        
        self.scene = QGraphicsScene()
        self.listFoos=[]



        
        super(MyView, self).__init__()

        self.initUI()
        #self.scroll(500,500)
        # on cache le scroll pour des fins esthétiques 
        self.setVerticalScrollBarPolicy(1);
        self.setHorizontalScrollBarPolicy(1);
        self.dessiner()

        self.setScene(self.scene)
        self.timer1=QtCore.QTimer()
        QtCore.QObject.connect(self.timer1, QtCore.SIGNAL("timeout()"),self.unTour)
        self.timer1.setInterval(self.periodeMiseAjour)  
        
       

    def initUI(self):
       
        self.setViewport(QGLWidget())
    

        self.setGeometry(500,200,1000,800)
        self.setWindowTitle('Course ')


    def keyPressEvent(self, e):
        print(e.key())
        if self.Controle !=1 :# si c'est une course entre les intelligence artificielle on n'a pas besoin de détecter les évènements
            return 


        if e.key() ==QtCore.Qt.Key_Left:

                    self.joueur.tournerGauche()
        if e.key() ==QtCore.Qt.Key_Right:

                   self.joueur.tournerDroite()                
        if e.key() == QtCore.Qt.Key_Up:

                     self.joueur.accelerer()                    
        if e.key() == QtCore.Qt.Key_Down:

                     self.joueur.deccelerer()                               
            
                    
        
        if e.key() == QtCore.Qt.Key_Escape:
            
                
            
            
            self.close()




    def dessiner(self):
    

     for  j in range(len(self.cir.plateau)):
    
        for  i in range(len(self.cir.plateau[j])):
            if self.cir.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='C':
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imSol.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                  
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imCarbu.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)
            elif self.cir.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='M':
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imSol.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                  
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imWall.scaled( self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                
            elif self.cir.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='O':
                
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imSol.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                 
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imMoule.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                  
                 
            elif self.cir.plateau[j,i,Circuit.Couche_terrain].getCaractere()=='H':
                
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imSol.scaled(self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)    
            else:
                
                self.listFoos.append(self.scene.addPixmap(QPixmap.fromImage(self.imR.scaled( self.scalex,self.scaley ))))

                self.listFoos[-1].setPos(self.scalex*i,self.scaley*j)                  
     for v in self.cir :


            self.voitures[v.id]=(self.scene.addPixmap(QPixmap.fromImage(self.sprites[v.typeV].scaled( self.scalecarx,self.scalecary ))))
           
            self.voitures[v.id].setTransformOriginPoint (QPoint(self.scalecarx/2,self.scalecarx/2 )); 
            self.voitures[v.id].setPos(v.x*self.scalex,v.y*self.scaley)
            self.voitures[v.id].setRotation(90+v.orientation*(180/3.14))
      

     self.centerOn(self.voitures[self.joueur.id])
                
     self.textRang=QGraphicsTextItem(" rang {} tour {}/{}".format(self.joueur.rang,self.joueur.nombreTourE,self.joueur._circuit.nbtours))               
     font=QtGui.QFont('White Rabbit')
     font.setPointSize(18)
     font.setBold(True)
     self.textRang.setFont(font)
     self.textRang.setDefaultTextColor(QColor('lightgray'))

     self.MarqueurCamera=QGraphicsRectItem(10,10,10,10)     
     self.MarqueurCamera.setBrush( QBrush( Qt.yellow)) 
     self.scene.addItem(self.textRang)
     self.scene.addItem(self.MarqueurCamera)
     
   #◘ self.scale(1,1)
     
           
    def unTour(self):
        
        

            
     for v in self.cir :
            coord=v.coords
            self.voitures[v.id].setRotation(90+v.orientation*(180/3.14))
            self.voitures[v.id].setPos(coord[0]*self.scalex,coord[1]*self.scaley)

     self.centerOn(self.voitures[self.joueur.id])
     #self.rotate((10/3.14)*(self.joueur.orientation-self.angleCamera))    

     self.cir.unTour() 
     self.angleCamera=self.joueur.orientation

     self.textRang.setHtml(" Rang {}/{} tours {}/{} v={} R={} L".format(self.joueur.rang,len(self.cir),self.joueur.nombreTourE,self.joueur._circuit.nbtours,self.joueur.vitesse,self.joueur.reservoir))               
     self.textRang.setPos(self.mapToScene (QPoint(0,0)))
#     self.indicateurDeVitesse.setPos(self.voitures[self.joueur.id].x()-10,self.voitures[self.joueur.id].y()-10)
#     self.setBaseSize((self.joueur.reservoir*50)/self.joueur.capacite_reservoir,10)
     self.MarqueurCamera.setPos(self.voitures[self.joueur.id].x(),self.voitures[self.joueur.id].y())
     print("un tour de plus")
     
     if(self.joueur.reservoir==0)  :
         self.timer1.stop()  
         self.cir.courseFinie=True  
         self.cir.Tri_finale()

         msgBox=QMessageBox()
         msgBox.setText("vous avez perdu faute de carburant")
         msgBox.exec_()
         

     
     if self.cir[len(self.cir)-1].nombreTourE>self.cir.nbtours:#  si la course est terminée 
     
     
         self.timer1.stop()  
         self.cir.courseFinie=True  
         self.cir.Tri_finale()

               
    
    def lancerCourse(self):
         self.cir.heurede_depart=time.time()        
         self.timer1.start()     
         

if __name__=="__main__":

    app = QtGui.QApplication(sys.argv)
    fen=QtGui.QWidget()

    fenetre= MyView(5,1,6)
    #fenetre.setParent(fen)
    fenetre.show()

    fenetre.lancerCourse()
    
    sys.exit(app.exec_())

