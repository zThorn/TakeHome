# Installation
To run and install, simply run
```
pip install -r requirements.txt
```

# Questions
In order to get the output of each question, I've provided the following commands.  If the --use-cache flag is set,
it'll use the local json files in /data instead of going to the MBTA api.

## Q1
```
python3 main.py q1
OR
python3 main.py q1 --use-cache=True
```
<img src="/img/render1594018947894.gif?raw=true"/>

## Q2
```
python3 main.py q2
OR
python3 main.py q2 --use-cache=True
```

## Route
```
python3 main.py route --origin='Malden Center' --destination=arlington
OR
python3 main.py route --origin='Malden Center' destination=arlington --use-cache=True
```
