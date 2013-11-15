from SimpleCV import Camera

if __name__ == '__main__':
	cam = Camera({"width": 640, "height": 480})
	img = cam.getImage()
	img.save('joepie.jpg')