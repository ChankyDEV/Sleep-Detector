import csv
import matplotlib.pyplot as plt
from scipy import ndimage

def read_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter =' ')
        x = []
        y= []
        conf= []
        for row in reader:
            splited = row[0].split(';')
            x.append(float(splited[0]))
            y.append(float(splited[1]))
            conf.append(float(splited[2]))
        return x,y,conf


