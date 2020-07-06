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

I've opted to shift the filtering off to the API for this question.  Typically, I evaluate whether or not to use
        API specific features based on their likelihood of deprecation, as well as the difficulty of migrating away
        from said features.  Generally, if I believe there's moderate or greater risk that the feature could go away,
        and the feature or filter isn't too hard to implement myself, I would do so.  In this case, I thought
        the filter would be pretty trivial to implement locally if need be, but was also
        pretty unlikely to be removed from the MBTA's API (It seems pretty core).  So due to that, I opted to use
        the MBTA's compute power, instead of my own!
        
## Q2
```
python3 main.py q2
OR
python3 main.py q2 --use-cache=True
```

<img src="/img/render1594020009111.gif?raw=true"/>

## Route
```
python3 main.py route --origin='Malden Center' --destination=arlington
OR
python3 main.py route --origin='Malden Center' --destination=arlington --use-cache=True
```
<img src="/img/render1594019573079.gif?raw=true"/>
