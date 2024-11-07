<picture>
 <source media="(prefers-color-scheme: dark)" srcset="Documents/Assets/Dark_mode.jpg">
 <source media="(prefers-color-scheme: light)" srcset="Documents/Assets/Light_mode.jpg">
 <img alt="UKB-UnPAC" src="Documents/Assets/Light_mode.jpg">
</picture>



# Welcome to UKB-UnPAC!
UKB-UnPAC is a Python package dedicated to the extraction of curated image data from the UK-Biobank. Developed by researchers in Trinity College Dublin’s Discipline of Radiation Therapy, as part of a project funded by the **World Cancer Research Fund** (WCRF). The funded project aimed to extract radiomics information from the Dixon weighted MRIs found in the UK-Biobank after being granted access. Considering the vastness of the data available an automated pipline was needed to streamline the acquisition of useful data from the UK-Biobank. This gave rise to UKB-UnPAC!

# What is UKB-UnPAC?
UKB-UnPAC offers an all-in-one system, designed to reduce the workload from extracting image data from the UK-Biobank, but can be adapted for any large scale radiological dataset. UKB-UnPAC has 4 main scripts which are its name sake, that allows researchers to:
* UnZip downloaded DICOM files.
* Parse those DICOM files based on researcher set variables.
* Acquire only anatomically relevant images from the UK-Biobank imaging datasets.
* Convert these images into a more research friendly format.

![Schematic diagram of the UKN-UnPAC process, highlighting inputs, outputs, and the 4 key processes](/Documents/Assets/Pipeline_diagram.png)

More detail on each of the processes are detailed below. Usage instructions can be found in (LINK)

## UnZipper
When initally downloaded, the MRI images from the UK-Biobank (UKB) come in the form of compressed, zip files (.zip). This file type is not easily read into many applications and is not accesable for research purposes. To overcome this, the UnZipper script was created. This function iteratively unzips each of the files into a readable, unzipped format, ready for use in research activities. This function retains the name of the zip file and matches the unzipped and zipped directories based on name. After all directories have been unzipped, the function then deletes the original zipped directories, to reduce data storage. 

## Parser
The parser function allows researchers to filter which data to parse based on a user set variable. Resaerchers will need to have created a CSV file with the list of patient IDs to be included in the study, and assign the patient ID variable name when calling the function. **This function works by comparing the list of unzipped image files names to the CSV file list, therefore directory names and patient ID in the CSV must match!** Any directory not found on your CSV list will be deleted. 

## Acquirer
The acquirer function, as is illustrated above, reads the metadata of the MRI and splits the full body MRI into its component parts based on the name of the series and the series number. This can be changed to allow for scans of different anatomical areas to be retained. The acquirer function reads the metadata, organizes the files in a neater pathway, based on the work of (REFERENCE). The acquirer function then discards the unspecified images, to reduce data storage requirments. The final product is a file pathway containing a 3D image of only the region of interest, in a specified weight from a specified series. 

## Converter
The objective of this project was to use segmented images to train U-Net based neural network. In order to achieve this both the images and the segments must be stored in the same format. To overcome this, the converter script creates a copy of all images in a directory as a NIfTI file. This function retains both the DICOM file and the newly generated NIfTI file. 

![Flow chart of the information contained in a UK-Biobank download with the image data relevant to this study highlighted](/Documents/Assets/ukb_flowchart.png)

The above diagram shows the extent of the imaging data available on the UKB vs the data needed (highlighted nodes). UnPAC allows the researcher to dictate how much of this data they store.

# Application
We believe that this package and the included function will be extremley benefical to the research community. The most evident application is the analysis of the UKB, however with small alterations to the code, and an undertsnading of the image formats, these functions could be applied to any large scale 3D radiological databases. These fucntions automate what is a repetitive task in this type of research and can also do it in a fraction of the time, saving time and resources. The entire pipeline from start to finish takes approx. 11.1 seconds per pateint. This could not be achieved at this speed manually. 

For more information visit the usage document on how to apply it to your own research. 
