# hole_measurement

This project is a tool to automatically measure the diameter of holes in parts from images, using image processing with Python and OpenCV.
The interface is simple and was built only to demonstrate the logic.

How it works:

  Select a reference image.
  Input the real diameter (in millimeters) for the reference hole to set the scale.
  Select the image of the part you want to measure.
  The script detects the most central hole and applies the measurement.

The logic was created to solve a real issue at my company: I needed to inspect part assemblies where the parts were very similar, with only a few millimeters of difference.
We had a MES system that told me which product was on the line. With a camera, I took a picture, measured, and returned the size of the hole.

![Uploading Captura de tela 2025-09-19 223337.jpg…]()
