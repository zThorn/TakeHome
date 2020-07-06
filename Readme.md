# Installation
To run and install, simply run
```
pip install -r requirements.txt
```

# Questions
In order to get the output of each question, I've provided the following commands.  If the cached flag is set,
it'll use the local json files in /data instead of going to the MBTA api.

## q1
```
python3 main.py q1
OR
python3 main.py q1 --cached=True
```
## q2
```
python3 main.py q2
OR
python3 main.py q2 --cached=True
```

## route
```
python3 main.py route source=copley destination=arlington
OR
python3 main.py route source=copley destination=arlington --cached=True
```
