#Python 2.7
#pip 19.2.3

Device used: Galaxy J7 SM-J737VPP

#Introduction:
This script will extract GPS data from a collection of geo-referenced images.
Specifically in this case, .jpg files. The output is a csv file with the date,
index, xy coordinates, file name, and format. This information can be uploaded
to mapping software or pulled back in for manipulation in Python. I took the 
liberty of quickly walking around wonderful Fargo, ND to snap some pictures for 
showing how it works. These are included in the Image file folder as examples.

#Installation:
Running the Extract.py file should result in all imports being completed. They
will be pulled from the Modules.py file. Keep in mind this was written using
pip 19.2.3, so if an import fails it will then use a sys.subprocess call. Depending
on your version of pip, the syntax may not work. If this be the case you will have
to upgrade your pip, or install the imports using a different method.

#USE:
Place the images you wish to extract data from in the Images folder. After 
you have placed all the images you wish to process, simply run the Extract.py
file from your command prompt. The result will be an initial data check. You 
will be informed how many images with correct GPS data, then it will prompt 
if you wish to continue. If you agree then the files will be processed. This is 
simply in place to let you know how many failures are to be expected. The final
outputs will be a CompleteData.csv and/or an ErrorData.csv.

Sample Data:
This small collection of images (of poor quality) provide you with an ouput. You can 
see how the data is supposed to be extracted. Results could vary by device.

Expectations:
Expect many errors within these images. Your cellphone may lose a GPS singal and simply
use a previously determined location if the time interval is short between pictures.
These errors will be noted by the error csv file. If the image still contained
coordinates despite the GPS signal error, it will still be placed in the complete data
csv. Coordinates will just be equal to the previously confirmed GPS location.  
If no data is available for the image, it will only be found in the error csv file.