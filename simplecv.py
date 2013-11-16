print 'initializing...'
from SimpleCV import Camera, Color, Image

if __name__ == '__main__':
    #print 'init camera...'
    #cam = Camera({"width": 640, "height": 480})
    #cam = Camera()
    images = []
    images.append(Image('parking-car.png'))#cam.getImage()
    images.append(Image('parking-no-car.png'))
    images.append(Image('girl.jpg'))

    for img in images:
        print 'busy with %r...' % img
        print 'detecting faces...'
        faces = img.findHaarFeatures("haar/haarcascade_frontalface_default.xml")

        #print locations
        for f in faces:
        	print "I found a face at " + str(f.coordinates())

        #outline who was drinking last night (or at least has the greenest pallor)
        if faces:
            faces.sortColorDistance(Color.GREEN)[0].draw(Color.GREEN)
            img.save("greenest_face_detected.png")

        hist = img.histogram(20)
