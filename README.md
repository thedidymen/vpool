# Setting up your environment

Setup up an environment:  

```python3 -m venv ./env```

and activate it:  

```source ./env/bin/activate``` for linux/mac

# Get the source code

Clone the repository:  

```git clone https://github.com/thedidymen/vpool```

# Install the dependencies

The project requires several libraries to function. Change into the directory (default: vpool). 
Please install the requirements:  

```pip install -r requirements.txt```

# Change to milestone-branch

Further development will happen on the main-branch, so please checkout the milestone-branch: 

```git checkout oplevering```

# Starting the application

Players names can be altered at the end of the vpool.py file. 
Easy mode is currently enabled and can be disabled at the end file.

The application can be started by:  

```python vpool.py```

# Playing the game

Choose a game to play from the menu.

The 'cue' give the direction and power of the shot. The angle can be adjusted clockwise: 'D' - 0.1, 'd' - 1, 'e' - 10, 'E' - 90 degrees;
or counterclockwise: 'A' - 0.1, 'a' - 1, 'q' - 10, 'Q' - 90 degrees. The power of the shot can be adjusted by: 'w' for increase or 's' for 
decrease, 'W' and 'S' will do a 10 fold jump. To take a shot press 'space bar'. The cueball can be stopped by pressing 'z' or 'x' for all 
balls. Right click on the mouse + moving will move the camera. The arrows wil move the camera around. Movement is relative to the in game 
coordinate system, not to the viewpoint of the observer.
