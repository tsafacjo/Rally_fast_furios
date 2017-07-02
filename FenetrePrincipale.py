# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:38:26 2017

@author: toumiab
"""


import sys
from  Fenetre import *

from PyQt4 import QtGui, QtCore

from MyView import *

# l'approche par héritage simple de la classe QMainWindow (même type de notre fenêtre 
# créée avec QT Designer. Nous configurons après l'interface utilisateur 
# dans le constructeur (la méthode init()) de notre classe


class MonAppli(QtGui.QWidget,Ui_Fenetre):
   def  __init__(self,parent=None):
       

       
     QtGui.QWidget.__init__(self,parent)

     self.setupUi(self)
     #variables de d'instance
     self.joeur=0

     
#     self.choixcircuit()
     
     #connexion
    
     self.btnJouer.clicked.connect(self.jouer)
     self.btnJoueurs.clicked.connect(self.choix1joueur)
     self.btnPrecedent.clicked.connect(self.precedent)
     self.btnSuivant.clicked.connect(self.choixvoiture)     
     self.btnSuivantCircuit.clicked.connect(self.choixcircuit)
     self.btnPrecedentCircuit.clicked.connect(self.precedent)
     self.btonChoixOrdianateurs.clicked.connect(self.choixOrdinateur )
     self.btnMenu.clicked.connect(self.retourneMenu)
     self.son=QtGui.QSound("sons/generique.wav")
     self.son.play()

     
  
     
   def retourneMenu(self):     
       
       self.stackedWidget.setCurrentIndex(0)
     
   def jouer(self):
       
       self.stackedWidget.setCurrentIndex(1)

   def choix1joueur(self):
       
       self.joeur=1
       self.stackedWidget.setCurrentIndex(2)
       
   def choixOrdinateur(self):
       
       self.joeur=2# Intelligence artificielle
       self.stackedWidget.setCurrentIndex(3) 
       
   def choixvoiture(self):
       
 
       self.stackedWidget.setCurrentIndex(3)
       
   def precedent(self):
       
 
       self.stackedWidget.setCurrentIndex( self.stackedWidget.currentIndex()-1)
       
   def choixcircuit(self):
       
       # penser faire varier le circuit 
       self.view=MyView(5,self.joeur,6)    
     #self.view.setParent(self)   
       self.view.setGeometry(150,40,1200,950)
       self.stackedWidget.setCurrentIndex(0)
       self.stackedWidget.setCurrentIndex(4) 
       QtCore.QObject.connect(self.view.timer1, QtCore.SIGNAL("timeout()"),self.finCourse)
   
       
       self.view.lancerCourse()
       #self.view.move(self.x(),self.y())
       self.hide()
       self.view.show()

       

              
   def finCourse(self):
       
     if self.view.cir.courseFinie:
          

       l=[]
       for i,v in enumerate(self.view.cir) :
           l.append(" Rang {}  , Pilote:{}  duree {}s  meilleur Temps :{}s ".format(i+1,str(v.id)+v.typeV,round(v.dureeTotale,3),round(v.meilleurTemps,3)))
           
           
       model 	= QStringListModel()                   
       model.setStringList(l)
       
       self.listClassement.setModel(model)
       self.stackedWidget.setCurrentIndex(6)
       self.view.hide()       
       self.show()


       
   def option(self):
       pass
       
              
       

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    #Form = QtGui.QWidget()
    #ui = Ui_Form()
    #ui.setupUi(Form)
    Form=MonAppli()
    Form.show()
    sys.exit(app.exec_())