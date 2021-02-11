# PX4-Python-SITL

This Documentation will guide you to program a drone runnning PX4 firmaware using the Python mavsdk module, with the added option of 3d smulation using Gazebo11

Before following this Steps install <a href="https://github.com/F-LAB-Systems/SITL_2021">PX4-Autipilot installation<a> for <a href="https://www.youtube.com/watch?v=AAv2zVYgxIY&feature=youtu.be">Video tutorial</a> 
  
https://user-images.githubusercontent.com/78522341/106847388-cc341f80-66d4-11eb-9966-00c068135fcc.png
 
## STEP 1 INSTALL PYCHARM

You can download the .tar file from the official website <a href="https://www.jetbrains.com/pycharm/download/#section=linux">Pycharm</a>

Follow the following steps to extract and run Pycharm

```

cd ~/Downloads

tar -xzf pycharm-community-2020.3.3.tar.gz //NOTE: Folder name will change according to the current version

```
```

cd pycharm-community-2020.3.3 //NOTE: Folder name will change according to the current version

cd bin

chmod u+x pycharm.sh

sh pycharm.sh

```
Installation window will open, complete it and move to the next step

## OR

If you have Pycharm already installed

```
cd pycharm-community-2020.3.3 //NOTE: Folder name will change according to the current version

cd bin

./pycharm.sh
```

## STEP 2: Create a new Project

We will do a simple take off and land using python !
Start by cloning this repository in your project folder using pycharm terminal

```
git clone https://github.com/F-LAB-Systems/PX4-Python-SITL-2021.git
```

## STEP 3: Open PX4-Autopilot & Gazebo

In new Terminal open PX4-Autopilot & Gazebo
```
cd~

cd PX4-Autopilot

make px4_sitl gazebo //QuadCopter
```

## STEP 4: Open QGroundControl

In new terminal open QGroundControl
```
cd~

cd Documents //If AppImage is in documents

./QGroundControl.AppImage
```
