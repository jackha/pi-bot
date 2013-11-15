from SimpleCV import Camera

if __name__ == '__main__':
	cam = Camera
	img = cam.getImage()
	img.save('joepie.jpg')