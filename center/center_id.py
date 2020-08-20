from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

#Makes a the next unique object ID with
#2 ordered dictionaries
class CentroidTracker():
    def __init__(self, maxDisappeared = 50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDisappeared

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in self.disappeared.keys():
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                usedRows.add(row)
                usedCols.add(col)
                # compute both the row and column index we have NOT yet
                # examined
                unusedRows = set(range(0, D.shape[0])).difference(usedRows)
                unusedCols = set(range(0, D.shape[1])).difference(usedCols)
                if D.shape[0] >= D.shape[1]:
                    # loop over the unused row indexes
                    for row in unusedRows:
                        # grab the object ID for the corresponding row
                        # index and increment the disappeared counter
                        objectID = objectIDs[row]
                        self.disappeared[objectID] += 1

                        # check to see if the number of consecutive
                        # frames the object has been marked "disappeared"
                        # for warrants deregistering the object
                        if self.disappeared[objectID] > self.maxDisappeared:
                            self.deregister(objectID)
                else:
                    for col in unusedCols:
                        self.register(inputCentroids[col])

                    # return the set of trackable objects
                return self.objects