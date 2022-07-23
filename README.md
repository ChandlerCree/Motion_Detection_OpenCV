# Motion_Detection_OpenCV

# Requirements

`pip install pandas`
`pip install opencv-python`
`pip install bokeh`

# Runtime

1. In order to run the motion detector please run `motion_detector.py`
   - To run with the output generating a bokeh plot run `timeframe_plotting.py`
2. Wait for first 200 iterations in order for camera to focus.
   - You will notice that the image appears to refresh
3. As you enter the frame and exit the frame
   - `Red box` is a small image making up less than `250x250` pixels
   - `Green box` is a larger image making up more than `250x250` pixels
4. Press 'q' to exit the the program at any time
5. You will notice the console display a list of datetime values
   - `output/times` will be where these values are stored in a csv using pandas
6. If you ran `timeframe_plotting.py` then a web browser will be opened displaying
   the timeframe graph of all occurances when the camera picked up motion
   - `output/graphs` will be where this .html file is stored

# TODO

1. Implement this to produce sound as a object enters the screen
2. Recognize whether or not the object on the screen is a face using the file
   `haarcascade_frontalface_default.xml` located at `resources/`
   - This will be accomplished using `cv2.CascadeClassifier`
3. Implement a way for the program to understand when an object has come to a stop
   and is now no longer in motion
4. TBD (open to suggestions)
