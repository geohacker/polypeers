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
    neighbors = []

    # Change WARD_NO to whatever identifier that you want to pick.

    neighbors.insert(0, feature1.GetField(attribute))
    for jindex in range(1, feature_count):
        print "Feature ", jindex
        feature2 = layer.GetFeature(jindex)
        geometry2 = feature2.GetGeometryRef()
        if geometry1.Touches(geometry2):
            neighbors.append(feature2.GetField(attribute))
    writer.writerow(neighbors)
