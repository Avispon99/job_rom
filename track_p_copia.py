import cv2 
import numpy as np 
import time
from center.center_id import CentroidTracker


cut=False
ct = CentroidTracker()
while 1:

	cap = cv2.VideoCapture(r'C:\Users\Usuario\Downloads\camina2.mp4') #change please

	ret, frame1 = cap.read()
	ret, frame2 = cap.read()
	rects = []

	while cap.isOpened():
		#try:
			diff = cv2.absdiff(frame1, frame2)
			gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray, (5,5),0)
			_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
			dilated = cv2.dilate(thresh, None, iterations=3)
			contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cv2.line(frame1,(0,350),(1300,350),(0,255,0),1)
			
			"""	
			for contour in contours:
				(x, y, w, h) = cv2.boundingRect(contour)# OK
				
				if cv2.contourArea(contour) < 700:
					continue
				cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 255, 0), 2)
				#cv2.putText(frame1, "Status: ()".format('M'), (10,20), cv2.FONT_HERSHEY_SIMPLEX,
				#	1,(0, 0, 255), 3)
			"""	
			for c in contours:
				(x, y, w, h) = cv2.boundingRect(c)
				if cv2.contourArea(c) < 700:
					continue
				rectangle = [x, y, (x + w), (y + h)] 
				rects.append(rectangle)
				cv2.rectangle(frame1, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]),(0, 255, 0), 2)       
			#print('rects: ',type(rects))
			#Detectar centroIDs
			objects = ct.update(rects)
			if objects is not None:
				for (objectID, centroid) in objects.items():
					#text = "ID:{}".format(objectID)
					#cv2.putText(frame1, text, (centroid[0] - 10, centroid[1] - 10),
                     #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
					cv2.circle(frame1, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
			
			cv2.imshow("feed", frame1)
			frame1 = frame2
			ret, frame2= cap.read()

			if cv2.waitKey(40) == 32 or cv2.waitKey(40) == 27:
				cut=True
				print('....88')
				break

				
		#except Exception as e:
		#	print(e)
		#	cv2.destroyAllWindows()
		#	cap.release()
		#	#time.sleep(3)
		
	if cut==True:
		print('---99')
		break

	
print('---0')
cv2.destroyAllWindows()
cap.release()
