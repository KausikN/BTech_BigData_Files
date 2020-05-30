def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(0.5)

def distmatrix(points):
    distances = []
    for i in range(len(points)):
        distrow = []
        for j in range(len(points)):
            distrow.append(round(dist(points[i], points[j]), 3))
        distances.append(distrow)
    return distances

def printmatrix(matrix):
    for i in range(len(matrix)):
        prtstr = ""
        for j in range(len(matrix[i])):
            prtstr += str(matrix[i][j]) + "\t"
        print(prtstr)

def findminval(matrix):
    minval = -1
    minind = [(0, 1)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if not i == j and not i > j:
                if minval > matrix[i][j] or minval == -1:
                    minval = matrix[i][j]
                    minind = [(i+1, j+1)]
                elif minval == matrix[i][j]:
                    minind.append((i+1, j+1))
    return minind, minval

def reduceMatrx(matrix, indexes, clusters):
    new_matrix = []
    for cluster in clusters:
        

points = [(2, 10), (2, 5), (8, 4), (5, 8), (7, 5), (6, 4), (1, 2), (4, 9), (8, 6), (6, 7)]
matrix = distmatrix(points)
printmatrix(matrix)
print(findminval(matrix))