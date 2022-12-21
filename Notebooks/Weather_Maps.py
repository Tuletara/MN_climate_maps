# Import packages
import arcpy
from arcpy.sa import *
import os


Symbology
# https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/uniquevaluerenderer-class.htm

# This applies symbology from another layer that must be stored 

# Apply symbology from layer

arcpy.env.workspace = r"C:\Users\mmMary\Documents\8990\T\LAYERS\symbology\precip"

ppt_monthly = r"C:\Users\mmMary\Documents\8990\T\LAYERS\Layer_Styles\ppt_monthly.shp"
# ann_style = r"C:\Users\mmMary\Documents\8990\Layers\Symbology_Layers\ppt_ann_style.shp"

featureclasses = arcpy.ListFeatureClasses()

for fc in featureclasses:
    if fc.endswith("_ann_bil.shp"):
        arcpy.management.ApplySymbologyFromLayer(fc, "ppt_ann_style", 
                                         "VALUE_FIELD ContourMin ContourMin", "MAINTAIN")
    else:
#         print(fc)
        arcpy.management.ApplySymbologyFromLayer(fc, "ppt_monthly", 
                                         "VALUE_FIELD ContourMin ContourMin", "MAINTAIN")









# Import packages & set workspace
import arcpy
import requests as r
from zipfile import ZipFile

arcpy.env.workspace = r'C:\Users\mmMary\Documents\8990\Map\Weather_Map.aprx'



# Generate list for pulling all monthly & annual variables for normals

date_list = ["%.2d" % i for i in range(13)]
date_list.pop(0)
# Add for the 14 annual normals to the list
date_list.append('14')

print(date_list)

# https://stackoverflow.com/questions/12030074/generate-list-of-numbers-in-specific-format

# Sample url: 'http://services.nacse.org/prism/data/public/4km/<element>/<date>' 

# Set a list of climate variables, base URL
element = ["ppt_", "tmean_", "tmax_", "tmin_"]
base = "http://services.nacse.org/prism/data/public/normals/4km"

for e in element:
    for i in date_list:
        url = os.path.join(base, e + i)
        r.get(base + element + date)   # API call for the data 
        print(url) 
    

# Set path for unzipped files
from zipfile import ZipFile

data_base_path = r"C:\Users\mmMary\Documents\8990\DATA"  # Path for unzipped files
directory = r"C:\Users\mmMary\Downloads"  # Path for downloaded zipped files

def unzip_climate(element):
    output_data_folder = os.path.join(data_base_path, element)

    for filename in os.listdir(directory):
        if filename.startswith("PRISM_" + element):
            with ZipFile(filename, 'r') as zipObj:
                zipObj.extractall(output_data_folder)

unzip_climate("ppt")

# Set path for unzipped files
from zipfile import ZipFile

data_base_path = r"C:\Users\mmMary\Documents\8990\DATA"  # Path for unzipped files
directory = r"C:\Users\mmMary\Downloads"  # Path for downloaded zipped files

def unzip_climate(element):
    output_data_folder = os.path.join(data_base_path, element)

    try:
        for filename in os.listdir(directory):
            if filename.startswith("PRISM_" + element):
                with ZipFile(filename, 'r') as zipObj:
                    zipObj.extractall(output_data_folder)
    
    except Exception as e:
        print("unable to download:",  e)
        

unzip_climate("ppt")

# Copy raw data files into a new folder in the temperary data directiory to store the shorter named files
# This preserves to raw data

# import os

def name_reducer(climate_variable):
     
# SET FILE PATH TO TEMPORARY DATA FOLDER
    dir_path = os.path.join(r"C:\Users\mmMary\Documents\8990\T\DATA", climate_variable)
    os.chdir(dir_path)
    
    for f in os.listdir():

    # Split off file extension from filename
        file_name, file_ext =os.path.splitext(f)

    # Split each name component into seperate parts
        prism, weather_type, yr, normal, resolution, month, extension = file_name.split('_')

    # New name combines just the weather type,month, multiple file extensions where applicable & the last file type
        new_name = '{}_{}_{}{}'.format(weather_type, month, extension, file_ext)

    # Rename all files to short names
        os.rename(f, new_name)

    print(weather_type, "renamed files are done")

name_reducer("ppt")
    
#     https://youtu.be/ve2pmm5JqmI



# This isn't working properly !!!! ERROR 999999
import arcpy

climate_variable = "ppt"
# Set the current workspace
arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Desktop\8990\test\DATA", climate_variable)
spatial_reference_object = arcpy.SpatialReference(26915)

rasters = arcpy.ListRasters()
for raster in rasters:
    print(raster)
    arcpy.management.ProjectRaster(raster, arcpy.env.workspace, spatial_reference_object)
    print(raster + " is now in UTM15 N")
    
# https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/listrasters.htm    
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/project-raster.htm

# Project raw .bil U.S. files into MN CRS ESPG 26915

# This works when running ind layer

# Create project command using spatial reference object

in_raster = r"C:\Users\mmMary\Documents\8990\DATA\Precipitation\PRISM_ppt_30yr_normal_4kmM3_annual_bil.bil"
out_raster = r"C:\Users\mmMary\Documents\8990\T\Project_Rasters\ppt\PRISM_ppt_30yr_normal_4kmM3_annual_bil.bil"
# wkt = 'PROJCS["NAD_1983_UTM_Zone_15N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-93.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
spatial_reference_object = arcpy.SpatialReference(26915)
arcpy.management.ProjectRaster(in_raster, out_raster, spatial_reference_object)

# Sources:
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/project-raster.htm
# https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/spatialreference.htm
#     https://epsg.io/26915

# This works when I project one file at a time but doesn't when looping thru folder (see below)

import os
# Set base path for raw rasters
directory = os.fsencode(r"C:\Users\mmMary\Documents\8990\DATA\Precipitation")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".bil"):
        
# Get file names for all .bil files
#         print(filename)
                            
        base_path = r"C:\Users\mmMary\Documents\8990\T\Project_Rasters\ppt"
        out_raster = os.path.join(base_path, filename)
       
 # Projection system for MN
        spatial_reference_object = arcpy.SpatialReference(26915)
        
# Project all US scale rasters
        arcpy.management.ProjectRaster(filename, out_raster, spatial_reference_object)
        print(output_file)

# Another attempt to automate the projection. This, sadly, also raises an error (shown at the bottom)
# Try using arcpy.ListRasters

import os
import arcpy
# Set base path for raw rasters
climate_variable = "tmax"

# arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Documents\8990\T\DATA", climate_variable)
in_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\DATA", climate_variable)   
out_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\MN_Extent", climate_variable)
arcpy.env.workspace = in_raster

raster_list = arcpy.ListRasters()
for raster in raster_list:
#     print(raster)
    try:  
        # Projection system for MN
        spatial_reference_object = arcpy.SpatialReference(26915)
        
        # Project all US scale rasters
        arcpy.management.ProjectRaster(raster, out_raster, spatial_reference_object)
        print(raster + "in now in UTM 15N")
    except Exception as e:
        print(e)
        
        
"""Something unexpected caused the tool to fail. Contact Esri Technical Support (http://esriurl.com/support) to Report a Bug, and refer to the error help for potential solutions or workarounds.
Failed to execute (ProjectRaster)."""        

Step 2. Convert metric to standard units - milimeters to inches









input = 

arcpy.management.Clip("JAN_PRISM_ppt_30yr_normal_4kmM3_annual_bil.bil", "-97.2698643033953 43.4353843588883 -89.3971195198901 49.4045362223117", r"C:\Users\mmMary\Documents\8990\Layers\MN_Precip\Jan", "State", "-9999", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

# Clip projected U.S. raster to MN Rectangle Extent

import arcpy, os

def extent_clip(climate_variable):
    arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\UTM", climate_variable)  
    clip_shp = r"C:\Users\mmMary\Documents\8990\Layers\MN_Boundary\State.shp"

    raster_list = arcpy.ListRasters()
    for raster in raster_list:
        out_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\MN_Extent", climate_variable, raster) 
        arcpy.management.Clip(raster, "170463.204 4796993.2567 780967.2014 5491739.865", out_raster, clip_shp, "-9999", "NONE", "MAINTAIN_EXTENT")
        print(raster + " is clipped to MN rectangle")
        
extent_clip("tmin")


# Sources
# https://stackoverflow.com/questions/30043403/create-for-loop-to-process-multiple-rasters-in-a-file-using-arcpy-clip-managemen
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/clip.htm

#import libraries
import arcpy
from arcpy.sa import *
import os

climate_variable = "precip"
in_raster_path = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\MN_Extent", climate_variable)   
arcpy.env.workspace = in_raster_path


rasters = arcpy.ListRasters()
for raster in rasters:
# Directory for converted rasters    
    new_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable, raster)  
# Create a raster object
    rasterObject = Raster(raster)
# Convert from mm to inches
    outraster = rasterObject / 25.4
# Check the min & max values to assess quality    
    min_inch = outraster.minimum
    max_inch = outraster.maximum
#Save to new folder
    outraster.save(new_raster)    
    print("Converted to inches: ", raster, "min & max inches: ", min_inch, max_inch)

# A function to convert temperature from Celsius to Fahrenheit 

def celsius_to_fahren(climate_variable):
    in_raster_path = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\MN_Extent", climate_variable)   
    arcpy.env.workspace = in_raster_path
   

    rasters = arcpy.ListRasters()
    for raster in rasters:
            
        # Directory for converted rasters    
        new_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable, raster)  
        # Create a raster object
        rasterObject = Raster(raster)
        # Convert from Cesius to Fahrenheit
        outraster = (rasterObject * 1.8) + 32
        # Check the min & max values to assess quality    
        min_temp = outraster.minimum
        max_temp = outraster.maximum
        #Save to new folder
        outraster.save(new_raster)    
        print("Converted to Degrees Fahrenheit: ", raster, "min & max Degrees: ", min_temp, max_temp)



# Call the function for each temperature variables
celsius_to_fahren("tmin")

def temp_contour(climate_variable):
    arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable)  
    # List to hold names of rasters that were successfully converted
    contour_list = []
    
    raster_list = arcpy.ListRasters()
    for raster in raster_list:
        input_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable, raster) 
        output_contour = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Contour", climate_variable, raster + ".shp")
        
        
        arcpy.sa.Contour(
        input_raster, output_contour, 
        2, 0, 1, "CONTOUR_POLYGON", None)
        
        contour_list.append(raster)
        
    ann_raster = arcpy.ListRasters("*ann_bil*")
    for raster in ann_raster:

        arcpy.sa.Contour(
        input_raster, output_contour, 
        1, 0, 1, "CONTOUR_POLYGON", None)
    
        contour_list.append(raster)
      
 # Show list of all converted files to make sure all were successful
    print(contour_list, " is now contoured")

# Call the function for each temperature variable    
temp_contour("tmax")    

import arcpy, os
from arcpy.sa import *

def precip_contour(climate_variable):
    arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable)  
    # List to hold names of rasters that were successfully converted
    contour_list = []
    
# Convert all of the monthly rasters using the 0.25 increment    
    raster_list = arcpy.ListRasters()
    for raster in raster_list:
        input_raster = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Standard_Units", climate_variable, raster) 
        output_contour = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Contour", climate_variable, raster + ".shp")
        
        arcpy.sa.Contour(
        input_raster, output_contour, 
        0.25, 0, 1, "CONTOUR_POLYGON", None)
        
        contour_list.append(raster)

# Handle the annual raster with 2 inch increment
    ann_raster = arcpy.ListRasters("*ann_bil*")
    for raster in ann_raster:
        
        arcpy.sa.Contour(
        input_raster, output_contour, 
        2, 15, 1, "CONTOUR_POLYGON", None)
        
        contour_list.append(raster)

# Print out confirmation list to ensure all files were successfully converted
    print(output_contour + " is now contoured")

# Call the function for precipitation
precip_contour("precip")    
       

# Clip projected U.S. raster to MN Rectangle Extent

def MN_clip(climate_variable):
    arcpy.env.workspace = os.path.join(r"C:\Users\mmMary\Documents\8990\T\LAYERS\Contour", climate_variable)  
    clip_feature = r"C:\Users\mmMary\Documents\8990\Layers\MN_Boundary\State.shp"

    feature_classes = arcpy.ListFeatureClasses()
    for fc in feature_classes:
        in_feature = os.path.join(arcpy.env.workspace, fc)
        out_feature = os.path.join(r"C:\Users\mmMary\Documents\8990\Layers\MN_Vector_Varibles", climate_variable, fc) 
        
        arcpy.analysis.Clip(in_feature, clip_feature, out_feature, None)
        print(fc + " is clipped to MN boundary")
        
                
MN_clip("precip")

 feature_classes = arcpy.ListFeatureClasses()
    for fc in feature_classes:






