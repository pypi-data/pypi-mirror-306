# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:54:10 2024

@author: OKEEFFR1
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:20:47 2024

@author: OKEEFFR1
"""
#dependencies------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import zipfile,fnmatch,os
import glob
import shutil
import dicom2nifti # to convert DICOM files to the NIftI format
import pydicom
import time 

#UnZipper---------------------------------------------------------------------------------------------------------------------------------
def UnZipper (Path):
    pattern = '*.zip'
    for root, dirs, files in os.walk(Path):
        for filename in fnmatch.filter(files, pattern):
            print(os.path.join(root, filename))
            zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
        for file in files:
            if file.endswith(".zip"):
                os.remove(os.path.join(root, file))
    print("Done")

#Parser-----------------------------------------------------------------------------------------------------------------------------------

def Parser(Path, Exclusion_df, ID_variable_name):
    eid = Exclusion_df[ID_variable_name].values.tolist()
    eid = str(eid)
    os.chdir(Path)
    try:
        for dirname in os.listdir(Path):
            if dirname[:7] not in eid:
                shutil.rmtree(dirname)
    except NotADirectoryError:
        print("Done")

#Attainer---------------------------------------------------------------------------------------------------------------------------------

def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_") # replace everything with an underscore
    return string.lower()  

def Acquirer(Path, Series_Number, Series_Description):
    start_time = time.time()
    count = 1
    Path_dcm = Path + "\\**\\*.dcm"
    for i in os.listdir(Path):
        print('reading file list...')
        unsortedList = []
        for root, dirs, files in os.walk(Path):
            for file in files: 
                if ".dcm" in file:# exclude non-dicoms, good for messy folders
                    unsortedList.append(os.path.join(root, file))
    
        print('%s files found.' % len(unsortedList))
    
    for dicom_loc in unsortedList:
        # read the file
        loc_dicom = os.path.dirname(dicom_loc)
        ds = pydicom.read_file(dicom_loc, force=True)
        # get patient, study, and series information
        patientID = os.path.basename(Path)
        studyDate = clean_text(ds.get("StudyDate", "NA"))
        studyDescription = clean_text(ds.get("StudyDescription", "NA"))
        seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
        seriesNumber = ds.get("SeriesNumber", "NA")
          
            # generate new, standardized file name
        modality = ds.get("Modality","NA")
        seriesInstanceUID = ds.get("SeriesInstanceUID","NA")
        instanceNumber = str(ds.get("InstanceNumber","0"))
        fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"
               
            # uncompress files (using the gdcm package)
        try:
            ds.decompress()
        except:
            print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (patientID, studyDate, studyDescription, seriesDescription ))
                
        if seriesNumber in Series_Number:
            if seriesDescription in Series_Description:
                if not os.path.exists(os.path.join(loc_dicom)):
                    os.makedirs(os.path.join(loc_dicom))
                   
                if not os.path.exists(os.path.join(loc_dicom, studyDate)):
                    os.makedirs(os.path.join(loc_dicom, studyDate))
                       
                if not os.path.exists(os.path.join(loc_dicom, studyDate, studyDescription)):
                    os.makedirs(os.path.join(loc_dicom, studyDate, studyDescription))
                       
                if not os.path.exists(os.path.join(loc_dicom, studyDate, studyDescription, seriesDescription)):
                    os.makedirs(os.path.join(loc_dicom, studyDate, studyDescription, seriesDescription))
                    print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription ))
                    print('%s files out of %s total files extracted.' % (count, len(unsortedList)))
                       
                ds.save_as(os.path.join(loc_dicom, studyDate, studyDescription, seriesDescription, fileName))
                count = count +1
    
    for root, dirs, files in os.walk(Path):
        for file in files:
            if file.startswith("1.3."):
                os.remove(os.path.join(root, file))
                
    print("Done")
    print("--- %s seconds per patient ---" % ((time.time()-start_time)/len(os.listdir(Path))))   


#Namer which isnt used---------------------------------------------------------------------------------------------------------------------
def namer (Path, extension, exclusion_path):
    df = pd.read_excel(exclusion_path, sheet_name = "Sheet2")
    os.chdir(Path)

    eid = df['f.eid'].values.tolist()
    eid = str(eid)
    for dirname in os.listdir(Path):
        os.rename(dirname, dirname.replace(extension,"" ))
        
    for dirname in os.listdir(Path):
        if dirname not in eid:
            shutil.rmtree(dirname)
            

#Converter--------------------------------------------------------------------------------------------------------------------------------
def Converter (Path):
    count = 0
    os.chdir(Path)
    for dirname in os.listdir(Path):
        dicom2nifti.convert_directory(dirname, dirname)
        count = count +1
        print("%s has been converted to NIfTI format (%s/%s)" % (dirname, count, len(os.listdir(Path))) )
    print("Done")


#Example----------------------------------------------------------------------------------------------------------------------------------
