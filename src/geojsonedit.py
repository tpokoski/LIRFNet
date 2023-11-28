import json

def add_property(geojson, property_name):
    for feature in geojson['features']:
        if feature['properties']['TrtmPlotID'] in trt_1:            
            feature['properties'][property_name] = 1
        elif feature['properties']['TrtmPlotID'] in trt_2:            
            feature['properties'][property_name] = 2
        elif feature['properties']['TrtmPlotID'] in trt_3:            
            feature['properties'][property_name] = 3
        elif feature['properties']['TrtmPlotID'] in trt_4:            
            feature['properties'][property_name] = 4
        elif feature['properties']['TrtmPlotID'] in trt_5:            
            feature['properties'][property_name] = 5
        elif feature['properties']['TrtmPlotID'] in trt_6:            
            feature['properties'][property_name] = 6
        elif feature['properties']['TrtmPlotID'] in trt_7:            
            feature['properties'][property_name] = 7
        elif feature['properties']['TrtmPlotID'] in trt_8:            
            feature['properties'][property_name] = 8
        elif feature['properties']['TrtmPlotID'] in trt_9:            
            feature['properties'][property_name] = 9
        elif feature['properties']['TrtmPlotID'] in trt_10:            
            feature['properties'][property_name] = 10
        elif feature['properties']['TrtmPlotID'] in trt_11:            
            feature['properties'][property_name] = 11
        elif feature['properties']['TrtmPlotID'] in trt_12:            
            feature['properties'][property_name] = 12
            
            
with open('LIRF.json') as filepath:
    geojson = json.load(filepath)
    
trt_1 = ['B11', 'B23', 'A33', 'A42', 'C12', 'C22', 'D31', 'D43']
trt_2 = ['A15', 'A22', 'B32', 'B46', 'D12', 'D22', 'C34', 'C41']
trt_3 = ['A14', 'A24', 'B31', 'B45', 'D13', 'D21', 'C36', 'C45']
trt_4 = ['B15', 'B22', 'A31', 'A46', 'C14', 'C23', 'D34', 'D46']
trt_5 = ['B14', 'B25', 'A34', 'A44', 'C11', 'C24', 'D33', 'D44']
trt_6 = ['A16', 'A26', 'B34', 'B41', 'D16', 'D25', 'C35', 'C42']
trt_7 = ['A11', 'A25', 'B33', 'B44', 'C13', 'C21', 'D36', 'D45']
trt_8 = ['B12', 'B26', 'A32', 'A41', 'D14', 'D26', 'C32', 'C43']
trt_9 = ['B13', 'B21', 'A35', 'A43', 'D15', 'D23', 'C31', 'C44']
trt_10 = ['A12', 'A23', 'B35', 'B42', 'C16', 'C25', 'D35', 'D42']
trt_11 = ['B16', 'B24', 'A36', 'A45', 'C15', 'C26', 'D32', 'D41']
trt_12 = ['A13', 'A21', 'B36', 'B43', 'C13', 'C21', 'D36', 'D45']
   
property_name = "Trt_code"

add_property(geojson, property_name)    
    
    
    
with open('modified_LIRF.json', 'w') as outfile:
    json.dump(geojson, outfile, indent=4)
print('complete')