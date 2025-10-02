<h1> hole measurement </h1>

This project is a tool to automatically measure the diameter of holes in parts from images, using image processing with Python and OpenCV.
The interface is simple and was built only to demonstrate the logic.

<h2> How it works:</h2>

1 - install the requirements.txt

2 - run python medidor_furo.py

3 - Select a reference image.

4 - Input the real diameter (in millimeters) for the reference hole to set the scale.

5 - Select the image of the part you want to measure.

6 - The script detects the most central hole and applies the measurement.

<h2> Why? </h2>

The logic was created to solve a real issue at my company: I needed to inspect part assemblies where the parts were very similar, with only a few millimeters of difference.
We had a MES system that told me which product was on the line. With a camera, I took a picture, measured, and returned the size of the hole.
All that write in C#, using OpenCVSharp to manipulate the image and using API integration with the other system, beside the object detection to check the part position, but this is another topic.

![restritor (2)](https://github.com/user-attachments/assets/dfe7697f-4046-4e7f-a840-6da9eeed8a6d)
