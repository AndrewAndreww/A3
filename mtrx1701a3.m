clc;
clear;


oc_map = csvread('testres600t60.txt')
oc_map = binaryOccupancyMap(oc_map, 20);
oc_map.GridLocationInWorld=[-20,-20];
show(oc_map)