"""
    File name: flooding_classes.py
    Description: For CEGE0096: Flooding Emergency Planning - classes used in main.py script
    Author: Falcon Team
    Date created: 10/12/2022
    Date last modified: 23/12/2022
    Python Version: 3.8
    Virtual env: geospatial
"""

class Geometry:  # reference: Week 4 solution for the Exercise 7
    def __init__(self, id):
        self.__id = id

    def get_name(self):
        return self.__id


class Point(Geometry):  # reference: Week 4 solution for the Exercise 7
    # Takes easting and northing coordinates x and y and an id for the object point
    def __init__(self, pt_id, x_coord, y_coord):
        super().__init__(pt_id)
        self.__x_coord = x_coord
        self.__y_coord = y_coord

    def get_x(self):
        return self.__x_coord

    def get_y(self):
        return self.__y_coord

    def build_pair(self):
        pairs = []
        for x in range(len(self.get_x())):
            pairs.append((self.get_name()[x], self.get_x()[x], self.get_y()[x]))
        return pairs


class Link(Geometry):
    # Take id ofr the link and two Point object
    def __init__(self, link_id, pt1, pt2):
        super().__init__(link_id)
        self.__pt1 = pt1
        self.__pt2 = pt2

    def get_pt1(self):
        return self.__pt1

    def get_pt2(self):
        return self.__pt2

    def get_listx(self):
        return [self.get_pt1().get_x(), self.get_pt2().get_x()]

    def get_listy(self):
        return [self.get_pt1().get_y(), self.get_pt2().get_y()]

    def distance(self):
        # distance between the 2 points
        distance = self.get_pt1.distance(self.get_pt2(), align=False)
        return distance

