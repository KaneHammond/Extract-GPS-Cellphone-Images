import Modules
from Modules import *

#####################_List all Files_#########################
# Write a list of all image files in the image folder. This  #
# will create a basis for determining file location and      #
# allow for extracting information from image files.         #
##############################################################

# Add Image path to the system to search for image files
sys.path.append("Images")

# Identify the path you've recentaly appended
mypath = 'Images'

# Write a function to create a list of files within the given path
# using listdir to identify the directory and isfile to select only 
# files. Join combines each element into a list format.
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

################_ Check Tag Information_######################
# This section will prompt if you want to view your image    #
# tag information. If it matches, the data can be extracted  #
# using this method. If not, modifications are required.     #
##############################################################


GeoTags = []

Format = ['GPS GPSLatitude', 'GPS GPSLongitude', 'GPS GPSTimeStamp',
	'GPS GPSDate', 'GPS GPSLongitudeRef', 'GPS GPSLatitudeRef']

ImageFailZero = []

ImageFailUnk = []

Passed = 0

Failed = 0

for aItem in onlyfiles:
	try:
		Pic = (mypath + '/' + aItem)

		# Use exifread to extract tag information
		tags = exifread.process_file(open(Pic), 'rb')

		# Define which tags are requested. In this case, we
		# desire all tags which contain the GPS tag.
		geo = {t:tags[t] for t in tags.keys() if t.startswith('GPS')}
		count = 0
		for aItem in geo:
			if aItem==Format[0]:
				count = count+1
			if aItem==Format[1]:
				count = count+1
			if aItem==Format[2]:
				count = count+1
			if aItem==Format[3]:
				count = count+1

		if count==4:
			GeoTags.append('Y')
			Passed = Passed+1
		if count<4:
			GeoTags.append('N')
			ImageFailZero.append(aItem)
			Failed = Failed+1
	except:
		# This will pass images where GPS data is incomplete. Other 
		# files with 0 gps data will be processed above as 'N'.
		GeoTags.append('N')
		ImageFailUnk.append(aItem)
		Failed = Failed+1

# Write a list of failed images with information pertaining to failure.

# Entire list
FailList = []

# Temporary list for insertion into full list
Temp = []

# Loop through ImageFailZero to insert missing data determination
for aItem in ImageFailZero:
	Temp.append(aItem)
	Temp.append('Missing Data')
	FailList.append(Temp)
	Temp=[]
# Loop through ImageFailUnk to insert unkown determination
for aItem in ImageFailUnk:
	Temp.append(aItem)
	Temp.append('Unkown')
	FailList.append(Temp)
	Temp=[]	

# Write the list into a pandas dataframe for ease of visualizing
IFdt = pd.DataFrame(FailList, columns=['Image', 'Issue'])

# Query to continue based upon available data. If zero images passed, the system 
# will exit. If more than zero pass, it will inform you of how many images
# contain the correct amount of data for extraction and prompt to continue.

if Passed==0:
	print ('\nAll images failed to process.')
	sys.exit()

if Passed>0:
	print ('\nTotal image files found: %i' % (len(onlyfiles)))
	print ('Images containing correct GPS format: %i\nImages missing data: %i\n' % (Passed, Failed))
	query = raw_input('Would you like to continue? Y/N:')
	query = query.upper()
	# Check the input given to query. With the .upper() command, the query is not
	# case sensitive. If anything other than Y or N is entered, the system
	# will inform the user of incorrect entry and exit.
	if query == 'Y':
		print ('\nProcessing Images...\n')
	if query == 'N':
		print ('\nExiting Module...')
		sys.exit()
	if query != 'Y' and query != 'N':
		print ('Incorrect entry, exiting module...')
		sys.exit()

###################_Extract File Data_########################
# Open images and extract imagery data. Uses file list       #
# provided by previous section. exifread will provide all    #
# available data for a given image. This section will only   #
# focus on extracting the time, date, lat and long.          #
##############################################################

# Write a conversion def for converting degrees, minutes, and
# seconds to decimal degrees.
def dms_to_dd(d, m, s):
	d = float(d)
	dd = d + float(m)/60 + float(s)/3600
	return dd

# Identify file type
Format = '.jpg'

# Write a loop to extract all data for image in folder.
# i will be the index this iteration is based upon. Each
# image will filter through this loop and all data will be 
# appended to a master data list (AllData).


i = 0

AllData = []

ProgBarLimit = len(onlyfiles)

# print len(onlyfiles)
# print onlyfiles
# sys.exit()
fail = []

for i in tqdm.tqdm(range(ProgBarLimit)):
# for aItem in onlyfiles:
	try: 
		try:
			# Set image path specific to image file in folder
			Pic = (mypath + '/' + onlyfiles[i])

			# Use exifread to extract tag information
			tags = exifread.process_file(open(Pic), 'rb')

			# Define which tags are requested. In this case, we
			# desire all tags which contain the GPS tag.
			geo = {t:tags[t] for t in tags.keys() if t.startswith('GPS')}
		except:
			fail.append(Pic)

		# Place this into a try and except loop. If failes, then data was
		# not able to be collected for that location.
		try:
			# Convert data to string to allow for extraction and modification
			# data is being converted from instance to string
			La = str(geo['GPS GPSLatitude'])
			Lo = str(geo['GPS GPSLongitude'])
			Time = str(geo['GPS GPSTimeStamp'])
			Date = str(geo['GPS GPSDate'])
			EW = str(geo['GPS GPSLongitudeRef'])
			NS = str(geo['GPS GPSLatitudeRef'])

			# Extract degrees, minutes, and seconds using def for Latitude.
			# Must first define which elements in string are needed. Remove 
			# sections of string and replace them to result in the format:
			# d-m-s. Once completed, it will be converted to a list which is
			# split by the dash (-). This will be the same for Longitude.
			Fix = La.replace(', ', '-')
			Fix = Fix.replace('[', '')
			Fix = Fix.replace(']', '')
			Fix = Fix.split('-')
			# print type(Fix)
			d = Fix[0]
			m = Fix[1]
			s = Fix[2]
			Latitude = dms_to_dd(d, m, s)

			# Ensure coordinates are correctly positive or negative using the Ref tag
			if NS=='S':
				#Check conversion has not taken place.
				if Latitude>0:
					Latitude = Latitude*-1

			# Extract degrees, minutes, and seconds using def for Longitude.
			# Must first define which elements in string are needed.
			Fix = Lo.replace(', ', '-')
			Fix = Fix.replace('[', '')
			Fix = Fix.replace(']', '')
			Fix = Fix.split('-')
			d = Fix[0]
			m = Fix[1]
			s = Fix[2]
			Longitude = dms_to_dd(d, m, s)

			# Ensure coordinates are correctly positive or negative using the Ref tag
			if EW=='W':
				#Check conversion has not taken place.
				if Longitude>0:
					Longitude = Longitude*-1
			# Coordinates have been converted and adjusted to correct positive and negative
			# by this section.
		except:
			Longitude = 'Null'
			Latitude = 'Null'

		# Extract Date Information by converting string to datetime format
		ConvDate = datetime.strptime(Date, '%Y:%m:%d')

		# Identify image name
		Name = onlyfiles[i].replace(Format, '')
	except:
		print ('Image failed to process')
		Latitude = 'Null'
		Longitude = 'Null'
		ConvDate = 'Null'
		Name = onlyfiles[i].replace(Format, '')
	# Index images, add 1 to prevent starting the index at 0 for the .csv
	Index = i+1

	ImageData = [Index, Latitude, Longitude, ConvDate, Name, Format]
	AllData.append(ImageData)

	# Iterate the loop by adding 1 to i
	i = i+1


###################_Write Output Files_#######################
# Take list created from previous step and place it into a   #
# Pandas dataframe. This will then be used to write it to a  #
# .csv file for future use and reference.                    #
##############################################################


# Complete data file (includes images without data)

# Define the header of the pandas dataframe to match the 
# data type for each image
Header = ['Index', 'Y', 'X', 'Date', 'Name', 'Format']

# Write pandas dataframe, print message to inform user it is being
# created. Useful for large datasets which take longer.
print ('\nCreating DataFrame...')
df = pd.DataFrame(AllData, columns=Header)

# Output the data to a .csv
print ('\nWriting Complete Data to CSV...')
df.to_csv(path_or_buf='CompleteData.csv')

# Write error file
print ('\nWriting Error Data to CSV...')
IFdt.to_csv(path_or_buf='ErrorData.csv')


