import cv2



indexes=[]
for  i in range(0,10):
	try:
		cap = cv2.VideoCapture(i)

		# Capture frame
		ret, frame = cap.read()
		if ret:
			print(f"frame capture index :{i}")
			indexes.append(i)
			# cv2.imwrite(f'image{i}.jpg', frame)
		cap.release()
	except:
		print(f"---------------- can't success {i}")
		continue
print(indexes)
