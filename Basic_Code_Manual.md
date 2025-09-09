# Basic Codes
### Start Robot
```
pybricksdev run ble Code Name.py
```
### Set DrvieBase:
```
drivebase = DriveBase(Left_motor, Right_motor, Wheel Diameter, axle_track)
```
### Drive by a given distance
```
drivebase.straight(distance(mm), stop_option)
```
### Point Turn
```
drivebase.turn(angle, stop_option)