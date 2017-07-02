# -*- coding: utf-8 -*-

import unittest
import Circuit as c
import VehiculeIAA as v
import VehiculeIAB as vb
class TestVehiculeIAA(unittest.TestCase):
    def test_var(self):
        cir=c.Circuit("circuit9.txt",0,2,10)
        

        x,y=cir.coordonneesWayPoint(1)
        ve=v.VehiculeIAA(x,y,cir,5)

        self.assertEqual(ve.x,x)
        self.assertEqual(ve.coords, (x,y))

    def test_type(self):

        cir=c.Circuit("circuit9.txt",2,3)
        x,y=cir.coordonneesWayPoint(1)
        ve=v.VehiculeIAA(x,y,cir,5)
        self.assertIsInstance(ve,v.VehiculeIAA)
class TestVehiculeIAb(unittest.TestCase):
    def test_var(self):
        cir=c.Circuit("circuit9.txt",2,3)
        

        x,y=cir.coordonneesWayPoint(1)
        ve=vb.VehiculeIAB(x,y,cir,5)

        self.assertEqual(ve.x,x)
        self.assertEqual(ve.coords, (x,y))
class TestVehiculeIAc(unittest.TestCase):
    def test_var(self):
        cir=c.Circuit("circuit9.txt",2,3)
        

        x,y=cir.coordonneesWayPoint(1)
        ve=vb.VehiculeIAC(x,y,cir,5)

        self.assertEqual(ve.x,x)
        self.assertEqual(ve.coords, (x,y))
    def test_type(self):

        cir=c.Circuit("circuit9.txt",0,2,10)
        x,y=cir.coordonneesWayPoint(1)
        ve=vb.VehiculeIAB(x,y,cir,5)
        self.assertIsInstance(ve,vb.VehiculeIAB)
class TestCircuit(unittest.TestCase):
    def test_type(self):
         cir=c.Circuit("circuit9.txt",0,2,10)
         self.assertIsInstance(cir, list)

if __name__ == '__main__':
    unittest.main()