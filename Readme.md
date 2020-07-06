# Installation
To run and install, simply run
```
pip install -r requirements.txt
```

# Questions
In order to get the output of each question, I've provided the following commands.  If the --use-cache flag is set,
it'll use the local json files in /data instead of going to the MBTA api.

## q1
```
python3 main.py q1
OR
python3 main.py q1 --use-cache=True
```
## q2
```
python3 main.py q2
OR
python3 main.py q2 --use-cache=True
```

## route
```
python3 main.py route source=copley destination=arlington
OR
python3 main.py route source=copley destination=arlington --use-cache=True
```
