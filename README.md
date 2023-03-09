# robot
Code to operate a Raspberry Pi powered robot.

**Components**   
- Devastator Tank Robot Platform with 2x DC motors
- Raspberry Pi 3A+
- Cytron 3A 4V-16V 2 Channel DC Motor Driver  
- RPI camera (unknown brand)
- PiHut mini pan and tilt platform with micro servos
- PNY Curve 5200 powerbank to power the RPI
- 6x AA batteries holder to power motor driver
- Lots of patch cables

**RPI GPIO Pin connections**  
|Physical Pin No.|GPIO Pin|Connection|
| --- | --- | --- |
|2|5v power|x servo power|
|4|5v power|y servo power|
|6|ground|motor driver ground|
|9|ground|	x servo  ground|
|11|GPIO 17|x servo input|
|13|GPIO 27|y servo input|
|14|ground|y servo ground|
|19|GPIO 10|M2B motor driver input| 
|21|GPIO 9|M2A motor driver input|  
|24|GPIO 8|M1A motor driver input| 
|26|GPIO  7|M1B motor driver input|  

**Current functionality**   

**web_bot** Remote control and video feed from the robot via a web app using flask. This version has been refactored to a Python class based script, with the robot class stored in a separate module. The web app runs on port 5000, which will need to be opened on your router to allow access outside of your network.  

**Work in Progress RC_bot** Operate as a remote control device using a wireless game contoller. Video footage from camera returned to RPI desktop. Refactor in progress.

**Work in Progress ball_bot** Object seeking robot based on OpenCV and YOLO. 


**Compatibility**  
This was built on an RPI 3 A Plus running the Buster edition of Raspberry Pi OS. It is  not functional on Bullseye, due to an overhaul of the camera implementation. 

The pigpio library is used to control servos, and the pigpiod daemon must be installed and launched before running any of the code. 

The an_robot module in tools>robot_class  should be installed to use the web bot by running "python setup.py install" from the robot class folder. If you would rather not install it, copy the robot_class.py file to the root folder, and change 'import an_robot' in the script to 'import robot_class'. 

![robot1](/photos/robot1.jpg)
![robot2](/photos/robot2.jpg)
