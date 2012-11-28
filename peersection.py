# Identify peers per the distance of intersection as the threshold.

import ogr
import sys
import csv

# Select the driver. Shapefile it is.
driver = ogr.GetDriverByName('ESRI Shapefile')

# Open the file using the driver.
data = driver.Open(sys.argv[1])
if(sys.argv[2]):
    attribute = sys.argv[2]
else:
    print "No attribute selected, using 'id'.."
    attribute = 'id'

# Open a file to dump the neighbor relations.
neighbors = open("neighbors.csv", "a")
writer = csv.writer(neighbors, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

# Select the first layer.
layer = data.GetLayer(0)
feature_count = layer.GetFeatureCount()

print "Features in the layer: ", feature_count

for index in range(feature_count):
    print "Feature ", index
    feature1 = layer.GetFeature(index)
    geometry1 = feature1.GetGeometryRef()
    boundary1 = geometry1.GetBoundary()
    neighbors = []
    peers = []
    # Change WARD_NO to whatever identifier that you want to pick.

    peers.insert(0, feature1.GetFieldAsInteger(attribute))
    for jindex in range(1, feature_count):
        # print "Feature jindex", jindex
        feature2 = layer.GetFeature(jindex)
        if feature1.GetFieldAsInteger(attribute) != feature2.GetFieldAsInteger(attribute):
            geometry2 = feature2.GetGeometryRef()
            if geometry1.Touches(geometry2):
                neighbors.append(feature2)
    if len(neighbors) > 5:
        print "More than 5 neighbors found, checking coverage..."
        sorted = False
        while not sorted:
            sorted = True
            for i in range(len(neighbors)-1):
                neighbor1_boundary = neighbors[i].GetGeometryRef().GetBoundary()
                neighbor2_boundary = neighbors[i + 1].GetGeometryRef().GetBoundary()
                if boundary1.Intersection(neighbor1_boundary).Length() < boundary1.Intersection(neighbor2_boundary).Length():
                    sorted = False
                    neighbors[i], neighbors[i + 1] = neighbors[i + 1], neighbors[i]
        for neighbor in neighbors[:5]:
            peers.append(neighbor.GetFieldAsInteger(attribute))
    else:
        for neighbor in neighbors:
            peers.append(neighbor.GetFieldAsInteger(attribute))
    writer.writerow(peers)










