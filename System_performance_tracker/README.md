# System_performance_tracker
# HeatSink(the Application Name)
System performance tracker using PyQt5 for the UI and python source code. SQL Database is used and is compatible with Linux and Microsoft OS.

**!!!DO NOT CHANGE ANY FILE NAME OR MESS WITH ANY ASSETS!!!**

It is a Python based application to track the system functionalities in Real-Time.
I have used PyQt5 widgets and Qtdesigner produced .ui files for the User Interface. 
![image](https://user-images.githubusercontent.com/89335295/210090582-3357db62-4f5f-4c04-973d-bbf1d5ec0795.png)
I have used SQL to store login details.
## Dependancies
Many python libraries must be installed.
You can use pip or if your using an Anaconda Enivronment u can use "conda install" statements.
I prefer you use this command line 
```bash
python -m pip install "name of library"
```
**THE LIST OF LIBRARIES:**
```python
speedtest-cli
GPUtil
shutil
pyside2
psutil
datetime
platform
```
In SQL youll have to run the following commands to set-up the database.

**its quite simple:**
```bash
create database se;
use se;
create table users(uname varchar(20),pass varchar(20));
```

**Keep all the provided files in the same folder .**

## Running 
Recommended to use VS Code . Execute the file LOGIN_PAGE.py.
This pops up the login page. Keep all the assest file in the same folder.

![image](https://user-images.githubusercontent.com/89335295/210212347-55bd53c8-9335-490e-987f-5cefa4ff8a3c.png)


***connect to database by clicking connect.***

You can setup a new user id and password. Click login to login and the page redirects to main page .

**IF YOU DONT WANT TO USE THE LOGIN PAGE YOU ACN DIRECTLY RUN THE MAIN_APP.py **


## Functionalities 

**I have used threads to bring upon parellel processing. 2 Threads are being used in this app to give you proper looped realtime system usage.**

![image](https://user-images.githubusercontent.com/89335295/210212409-7dc61a06-ed2c-4af4-8a63-68328c68e4fb.png)

```bash
1. Dashboard
2. CPU
3. RAM
4. Storage
5. Network
6. GPU
7. System info
8. Activity
9. Sensors
10. Battery
```
## CPU
**Visually depicts the cpu usage in real time with all the core info.**
![image](https://user-images.githubusercontent.com/89335295/210216350-9d447e41-4e6e-4f3a-a8b7-733523a4bea5.png)

## RAM
**Real-time ram usage in the form of a spiral progress bar**
![image](https://user-images.githubusercontent.com/89335295/210216369-9d704e4d-0932-47e3-ad47-dfb1d582de79.png)

## Storage
**The amount of ROM used and available(presize data).**
![image](https://user-images.githubusercontent.com/89335295/210216388-ab9e4772-3a01-4f3d-a4ac-e1505f6300f4.png)

## Network
**shows at what speed is the system consuming or uploadind information into the net.**
![image](https://user-images.githubusercontent.com/89335295/210216409-5d06d30e-17f5-40d5-a20f-f4d936e15a90.png)

## GPU
**real time System  GPU usage (Run any grafic intensive game to check ).**
![image](https://user-images.githubusercontent.com/89335295/210216428-c23d50a9-711f-417e-a1e9-00f99f9c1ff5.png)

## System info
**Standarfd out of the box system specifications**
![image](https://user-images.githubusercontent.com/89335295/210218244-727a908e-c383-4f4e-b4c0-8ea91129159e.png)

## Activity
**Functions and processes running on the system. Can search any process by its name**
![image](https://user-images.githubusercontent.com/89335295/210218277-6f388f3d-1a5a-4d5c-be64-fc305c3f7f8b.png)


## Sensors
**Only available on ubuntu systems**
![image](https://user-images.githubusercontent.com/89335295/210218298-e955d602-513c-4b21-ac48-73e9b5a504f8.png)

## Battery
**battery real time specifications**
![image](https://user-images.githubusercontent.com/89335295/210219388-150bb8ec-159c-46fa-b348-ccb8f138eb47.png)

# THANK YOU
