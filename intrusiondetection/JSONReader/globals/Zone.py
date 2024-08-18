
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Zone:
    def __init__(self, settings):
        self.edges = self.setZoneEdges(settings["edges"])
        self.edgesList = self.setEdgeList(settings["edges"])
        self.edgeNumber = len(self.edges)


    def setZoneEdges(self, edges):
        edges_dict = []
        index = 0
        for i in edges:
            print(i)
            edges_dict.append(i)
            index += 1
        return edges_dict


    def setEdgeList(self, edges):
        edges_dict = []
        index = 0
        for i in edges:
            edges_dict.append((i["x"], i["y"]))
            index += 1
        return edges_dict



    def appendEdge(self, newPoint):
        self.edges.append(newPoint)
        self.edgeNumber +=1
        return self.edges

    def deleteEdge(self, deletedPoint):
        if deletedPoint < self.edgeNumber:
            self.edges.pop(deletedPoint)
            self.edgeNumber -= 1
        elif deletedPoint == self.edgeNumber:
            self.edges.pop()
            self.edgeNumber -= 1
        else:
            return self.edges
        return self.edges

    def deleteAll(self):
        self.edges = []
        self.edgeNumber = 0
        return self.edges

    def updateEgdes(self, newValue):
        self.edges = newValue
        return self.edges


    def setPolygon(self, listPly):
        polygon = []
        for item in listPly:
            polygon.append(Point(item[0], item[1]))
        return polygon

    def is_in_main_zone(self, x, y):
        polygon = self.setPolygon(self.setEdgeList(self.edges))
        point = Point(x, y)
        num_vertices = len(polygon)
        x, y = point.x, point.y
        inside = False

        # Store the first point in the polygon and initialize the second point
        p1 = polygon[0]

        # Loop through each edge in the polygon
        for i in range(1, num_vertices + 1):
            # Get the next point in the polygon
            p2 = polygon[i % num_vertices]

            # Check if the point is above the minimum y coordinate of the edge
            if y > min(p1.y, p2.y):
                # Check if the point is below the maximum y coordinate of the edge
                if y <= max(p1.y, p2.y):
                    # Check if the point is to the left of the maximum x coordinate of the edge
                    if x <= max(p1.x, p2.x):
                        # Calculate the x-intersection of the line connecting the point to the edge
                        x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1.x == p2.x or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside

            # Store the current point as the first point for the next iteration
            p1 = p2

        # Return the value of the inside flag
        return inside
