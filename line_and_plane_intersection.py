# -*- coding: utf-8 -*-
"""
Thomas Stainer

Python 3 program to compute the intersecting points between a plane and 3 lines
The main function is IntersectingPoints(p1, p2, p3, c) which asks for 3 points p1, p2, p3
defining 3 lines between them, c, is the hieght of the plane located perpendicular to the z axis
at (0,0,c). The function returns a list of intersecting points, note that if the line or lines are parallel
to the plane (no intersection) then these point are omitted. 

In the case when all 3 points are in the plane and form a line, the 2 end points are returned. 
If all 3 points are in the plane but do not all form 1 line, then no points are returned.

In the case when 1 or 2 points are in the plane but the third is not then obviously the points in
the plane will be returned (if only 1 point in the plane then an additional point could also be returned)

"""

import math
import numpy as np
import numpy.linalg as la

# The point class, defines the operations needed for a point (x,y,z)
class Point:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    
  def __str__(self):
    return "({}, {}, {})".format(self.x, self.y, self.z)

  def __neg__(self):
    return Point(-self.x, -self.y, -self.z)

  def __add__(self, point):
    return Point(self.x+point.x, self.y+point.y, self.z+point.z)

  def __sub__(self, point):
    return self + -point

  def __mul__(self, scalar):
    return Point(scalar*self.x, scalar*self.y, scalar*self.z)

  def Mag(self):
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)
  
  def Dot(self, point):
    return self.x*point.x + self.y*point.y + self.z*point.z
  
  def Vectorise(self):
    return [self.x, self.y, self.z]

  __rmul__ = __mul__
  
# The line - require 2 points to define a line
class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        
    # Computes a point on the line, given the parameter a
    def __call__(self, a):
        return self.p1 + (a*(self.p2 - self.p1))
    
    # Checks if another point lies in the line
    def IsPointValid(self, point):
        diff21 = self.p2 - self.p1
        diff31 = point - self.p1
        
        factor1 = 1.0/diff21.Mag()
        factor2 = 1.0/diff31.Mag()
        
        unit1 = diff21*factor1
        unit2 = diff31*factor2
    
        # dot them
        dot = abs(unit1.Dot(unit2))
        if math.isclose(dot, 1):
            return True
        else:
            return False
    
# The plane - require 3 points to define a plane
class Plane:
    def __init__(self, point1, point2, point3):
        self.p1 = point1
        self.p2 = point2
        self.p3 = point3
        
    # Computes a point on the plane, given the parameters b and c
    def __call__(self, b, c):
        return self.p1 + (b*(self.p2 - self.p1)) + (c*(self.p3 - self.p1))
    
    def NormUnitVector(self):
        a = (self.p2 - self.p1).Vectorise()
        b = (self.p3 - self.p1).Vectorise()
        norm = np.cross(a,b)
        norm_point = Point(norm[0], norm[1], norm[2])
        factor = 1.0/norm_point.Mag()
        return factor*norm_point
    
    # Checks if another point lies in the plane
    def IsPointValid(self, point):
        # can use any point in the plane
        dot = (point - self.p1).Dot(self.NormUnitVector())
        if math.isclose(dot, 0.0):
            return True
        else:
            return False

# Returns the matrix for the line-plane intersection
def Matrix(line, plane):
    line_diff = line.p1 - line.p2
    plane_diff21 = plane.p2 - plane.p1
    plane_diff31 = plane.p3 - plane.p1
    
    return np.matrix([[line_diff.x, plane_diff21.x, plane_diff31.x ],
                     [line_diff.y, plane_diff21.y, plane_diff31.y ],
                     [line_diff.z, plane_diff21.z, plane_diff31.z]])
    
# Returns the vector for the line-plane intersection
def Vector(line, plane):
    vec = line.p1 - plane.p1
    return np.matrix([[vec.x],
                      [vec.y],
                      [vec.z]])

# Square matricies only
# Checks if it has an inverse - by checking whether the determinant is 0
# returns true if it is invertable, false otherwise
def HasInverse(mat):
    if la.det(mat) == 0:
        return False
    else:
        return True
    
# Find the end points given a list of points
# i.e. the pair of points which gives the largest diff, \pi - pj\
def EndPoints(points):
    largest_diff = 0.0
    i1 = 0
    i2 = 0
    for i in range(0,len(points)):
        for j in range(0,len(points)):
            diff = (points[i] - points[j]).Mag()
            if diff > largest_diff:
                largest_diff = diff
                i1 = i
                i2 = j
                
    return [points[i1],points[i2]]
                
# Given 2 points for the line: l1 and l2, and given the 3 points in the plane: p1, p2, p3,
# we compute the intersecting point.
# If the points are parallel to plane or are in the plane there is no inverse, so we return....
def IntersectionPoint(line, plane):
    
    # compute matrix and vector
    mat = Matrix(line,plane)
    vec = Vector(line, plane)
    
    # check if the inverse exists - if not then it either does not intersect or 
    # is in the plane
    if HasInverse(mat) == False: 
        return None
    
    # Compute the inverse
    inv = la.inv(mat)
    
    # compute the parameters for line and plane
    params = inv*vec
    
    # a is the parameter for the line
    a = (float)(params[0])
    
    return line(a)

"""
Main function
"""
# For plane at (0,0,c)
def IntersectingPoints(p1,p2,p3,c):
    
    # 3 points in plane, we know it is perpendicular to the z axis,
    # so we pick any 3 points with z=c
    plane = Plane(Point(0,0,c),Point(1,2,c),Point(3,4,c))
    
    # first check if the three points form one line in the plane
    l12 = Line(p1,p2)
    l13 = Line(p1,p3)
    l23 = Line(p2,p3)
    
    # if they do form one single line, in the plane, then return the end points
    if l12.IsPointValid(p3) and plane.IsPointValid(p3):
        return EndPoints([p1,p2,p3])
    
    points = [
     IntersectionPoint(l12, plane),
     IntersectionPoint(l13, plane),
     IntersectionPoint(l23, plane)
     ]
    
    # only return points that intersect removing duplicates
    return list(set([p for p in points if p != None]))

# main for testing only
def main():
    p1 = Point(0,0,0);
    p2 = Point(0,0,3);
    p3 = Point(1,1,1);
    c = 2

    points = IntersectingPoints(p1,p2,p3,c)
    
    for p in points:
        print("intersecting point = ", p)

if __name__ == "__main__":
    main()