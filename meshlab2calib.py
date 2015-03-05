import sys

if len(sys.argv) != 4:
  print "Wrong number of input parameter!"
  print "Usage: " + sys.argv[0] + " <MeshLabSceneFile.mlp> <OutputCalibrationFileName> <OutputImageListFileName>"
  exit()

# Reading input parameters
inName = sys.argv[1]
outCalibName = sys.argv[2]
outImageListName = sys.argv[3]

inFile = open(inName, "r")
outCalibFile = open(outCalibName, "w")
outImageListFile = open(outImageListName, "w")


imageNum = 0
allMatrices = []
allImages = []

# Through the file
while True:
	line = inFile.readline()
	if line == "\n": continue
	if not line: break

	line = line.split()
	if line[0] == "<MLRaster":
		imageNum = imageNum + 1 
		camMatrices = []
		line = inFile.readline().split() # calibration information

		# position is extracted
		translationVector = []
		auxline = line[1].split('"')
		translationVector.append(auxline[1])
		translationVector.append(line[2])
		auxline = line[3].split('"')
		translationVector.append(auxline[0])
		camMatrices.append(translationVector)

		# Distortion
		distortion = []
		auxline = line[4].split('"')
		distortion.append(auxline[1])
		auxline = line[5].split('"')
		distortion.append(auxline[0])
		camMatrices.append(distortion)

		# View Port
		size = []
		auxline = line[6].split('"')
		size.append(auxline[1])
		auxline = line[7].split('"')
		size.append(auxline[0])
		camMatrices.append(size)

		# Pixel size
		pixsize = []
		auxline = line[8].split('"')
		pixsize.append(auxline[1])
		auxline = line[9].split('"')
		pixsize.append(auxline[0])
		camMatrices.append(pixsize)

		# Center pix
		centerpix = []
		auxline = line[10].split('"')
		centerpix.append(auxline[1])
		auxline = line[11].split('"')
		centerpix.append(auxline[0])
		camMatrices.append(centerpix)

		# Focal
		auxline = line[12].split('"')
		focal = auxline[1]
		camMatrices.append(focal)

		# Rotation Matrix
		rotation = []
		auxline = line[13].split('"')
		rotation.append(auxline[1])
		for i in range(14,28):
			rotation.append(line[i])
		auxline = line[28].split('"')
		rotation.append(auxline[0])
		camMatrices.append(rotation)

		line = inFile.readline() # name of the image
		auxline = line.split('"')
		thisImage = auxline[3]
		allImages.append(thisImage)

		allMatrices.append(camMatrices)


# Now output files are written

outCalibFile.write("%d\n" % (imageNum))

for i in range(0,imageNum):
	# current image is written to the image list
	outImageListFile.write(allImages[i] + "\n")

	currentCam = allMatrices[i]
	imWidth = int(currentCam[2][0])
	imHeight = int(currentCam[2][1])
	pixCenterX = int(currentCam[4][0])
	pixcenterY = imHeight - int(currentCam[4][1])

	# current camera parameters
	outCalibFile.write("%s 0 %d 0 %s %d 0 0 1\n" % (currentCam[5], pixCenterX, currentCam[5], pixcenterY ))

	# IN PROGRESS...






