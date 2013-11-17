print 'initializing...'
from SimpleCV import Camera, Color
import Image

if __name__ == '__main__':
    print 'init camera...'
    cam = Camera()

    while 1:
        img = cam.getImage()

        import pdb; pdb.set_trace()
        img = img.resize((320, 240), Image.NEAREST)

        print 'detecting faces...'
        faces = img.findHaarFeatures("haar/haarcascade_frontalface_default.xml")

        #print locations
        for f in faces:
            print "I found a face at " + str(f.coordinates())
            f.draw(Color.GREEN)
        img.show()

    #outline who was drinking last night (or at least has the greenest pallor)
    #faces.sortColorDistance(Color.GREEN)[0].draw(Color.GREEN)

    #import pdb; pdb.set_trace()