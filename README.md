# Privatsiya, blur faces with Python basicly

This program blurs faces with Ultralytics and OpenCV2 library.

## Installation of Libraries
```
pip install opencv-python
pip install opencv-contrib-python
pip install ultralytics

pip install argparse
pip install filetype
```

## Usage Example
```
python main.py -i test.img -s 1 -n blurredtest.png
```
##Known Issues
Faces are sometimes not detected for short periods of time (which can be fixed with a better trained AI model.)
Video processing is slow (which can be fixed with multiprocessing.)

## Results
![test](https://github.com/maxwell400/Privatsiya/assets/151213362/1f29e405-ea5e-4e62-a85f-34febc2cdf19)
