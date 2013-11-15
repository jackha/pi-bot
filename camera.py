print 'initializing...'
from SimpleCV import Camera

if __name__ == '__main__':
	print 'init camera...'
	#cam = Camera({"width": 640, "height": 480})
	cam = Camera({"width": 640, "height": 480})
	img = cam.getImage()

	print 'detecting faces...'
	faces = img.findHaarFeatures("haar/haarcascade_frontalface_alt.xml")

	#print locations
	for f in faces:
		print "I found a face at " + str(f.coordinates())

	#outline who was drinking last night (or at least has the greenest pallor)
	faces.sortColorDistance(Color.GREEN)[0].draw(Color.GREEN)
	img.save("greenest_face_detected.png")
