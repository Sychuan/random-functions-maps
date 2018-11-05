# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 16:28:49 2017

@author: Maksim
"""

import numpy as np
import datetime
# import matplotlib.pyplot as plt

from math import *
import random

from PIL import Image


class X:
    def eval(self, x, y):
        return x

    def __str__(self):
        return "x"


class Y:
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"


class SinPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return np.sin(np.pi * self.arg.eval(x, y))


class CosPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return np.cos(pi * self.arg.eval(x, y))


class Expf:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "exp(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        try:

            return np.exp(pi * self.arg.eval(x, y))
        except:
            return self.arg.eval(x, y)


class RoundF:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "round(" + str(self.arg) + ")"

    def eval(self, x, y):
        try:
            return np.round(self.arg.eval(x, y))
        except:
            return self.arg.eval(x, y)


class Times:
    def __init__(self, prob):
        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def __str__(self):
        return str(self.lhs) + "*" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


class Plus:
    def __init__(self, prob):
        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def __str__(self):
        return str(self.lhs) + "+" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) + self.rhs.eval(x, y)


def buildExpr(prob):
    if random.random() < prob:
        # return random.choice([SinPi, CosPi, Times, Plus, RoundF])(prob)
        return random.choice([SinPi, CosPi, Times, Plus])(prob)
    else:
        return random.choice([X, Y])()


imrange = 400
scale = 5# scale
time = 100 # time parametr
time_scale = 50
im_number = 1
probability = 0.98
mode = '!HSV'

funf = open("funct.txt", "w+")


date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
for i in range(0, im_number):
    expR = buildExpr(probability)
    expG = buildExpr(probability)
    expB = buildExpr(probability)
    funf.write("red = {}\n".format(expR))
    funf.write("green = {}\n".format(expG))
    funf.write("blue = {}\n\n".format(expB))
    print("red = {}\n\ngreen ={}\n\nblue ={}\n\n\n".format(expR, expG, expB))

    for t in range(0, time, 1):
        #scale*=1.2
        x = np.linspace(-imrange // (2*scale), imrange // (2*scale), imrange)
        y = np.linspace(-imrange // (2*scale), imrange // (2*scale), imrange)
        XX, YY = np.meshgrid(x, y)
        res = expR.eval((XX + t) / time_scale, (YY + t) / time_scale)
        R = Image.fromarray((((res * 255)) % 255).astype(np.int8), mode="L")
        res = expG.eval((XX - t) / time_scale, (YY + t) / time_scale)
        G = Image.fromarray((((res * 255)) % 255).astype(np.int8), mode="L")
        res = expB.eval((XX + t) / time_scale, (YY - t) / time_scale)
        B = Image.fromarray((((res * 255)) % 255).astype(np.int8), mode="L")
        if mode == 'HSV':
            finalImage = Image.merge("HSV", (R, G, B))
            finalImage = finalImage.convert("RGB")
        else:
            finalImage = Image.merge("RGB", (R, G, B))

        finalImage.save('img{}_{}_{}.png'.format(i, t, date), "PNG")
funf.close()
