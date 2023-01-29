# Setting up your environment

Setup up an environment:  

```python3 -m venv ./env```

and activate it:  

```source ./env/bin/activate``` for linux/mac

# Get the source code

Clone the repository:  

```git clone https://github.com/thedidymen/vpool```

# Install the dependencies

The project requires several libraries to function. Please install them:  

```pip install -r requirements.txt```

# Change to milestone-branch

Further development will happen on the main-branch, so please checkout the milestone-branch
```git checkout milestone```

# Starting the application

The application can be started by:  

```python vpool.py```

# Playing the game

The "cue" give the direction and power of the shot. The angle can be adjusted clockwise: 'd' by one degree, 'e' by 10 degrees; or counterclockwise: 'a' by one degree, 'q' by 10 degrees. The power of the shot can be adjusted by: 'w' for increase or 's' for decrease. To take a shot press 'space bar'. The cue-ball can be stopped by pressing 'z' or 'x' for all balls.