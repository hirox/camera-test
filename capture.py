desc = 'Show or save camera image'

import argparse
import cv2

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-d', '--device', type=int, help='device number', default=0)
parser.add_argument('-s', '--save', action='store_true')
args = parser.parse_args()

capture = cv2.VideoCapture(args.device)

if args.save:
	ret, frame = capture.read()
	if ret:
		cv2.imwrite('out.png', frame)
	else:
		print("Failed to capture")
else:
	while(True):
		ret, frame = capture.read()

		if ret:
			# resize the window
			windowsize = (800, 600)
			frame = cv2.resize(frame, windowsize)

			cv2.imshow('title',frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

capture.release()
cv2.destroyAllWindows()
