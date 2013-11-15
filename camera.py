print 'initializing...'
from SimpleCV import Camera, Color

if __name__ == '__main__':
    print 'init camera...'
    #cam = Camera({"width": 640, "height": 480})
    cam = Camera()
    img = cam.getImage()

    print 'detecting faces...'
    faces = img.findHaarFeatures("haar/haarcascade_frontalface_default.xml")

    #print locations
    for f in faces:
    	print "I found a face at " + str(f.coordinates())

    #outline who was drinking last night (or at least has the greenest pallor)
    #faces.sortColorDistance(Color.GREEN)[0].draw(Color.GREEN)
    img.save("greenest_face_detected.png")

    hist = img.histogram(20)
    brightpixels = 0
    darkpixels = 0
    i = 0

    while i < len(hist):
        if (i < 10):
            darkpixels = darkpixels + hist[i]
        else:
            brightpixels = brightpixels + hist[i]
        i = i + 1

    if (brightpixels > darkpixels):
        print "your room is bright"
    else:
        print "your room is dark"

    import pdb; pdb.set_trace()