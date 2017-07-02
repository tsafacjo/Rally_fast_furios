# -*- coding: utf-8 -*-

dprint_debug = True 

def dprint(*args, **kwargs):
    """
    Fonction rendant plus simple la gestion de l'affichage en mode debug.
    Si la variable globale ''dprint_debug'' est à ''False'' aucun affichage
    ne sera produit, si elle est à ''True'' alors ''dprint_debug'' se 
    comportera comme ''print''
    """
    
    if dprint_debug:
        print(*args, **kwargs)