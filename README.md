# Playing the game

Choose a game to play from the menu.

The 'cue' give the direction and power of the shot. The angle can be adjusted clockwise: 'D' - 0.1, 'd' - 1, 'e' - 10, 'E' - 90 degrees;
or counterclockwise: 'A' - 0.1, 'a' - 1, 'q' - 10, 'Q' - 90 degrees. The power of the shot can be adjusted by: 'w' for increase or 's' for 
decrease, 'W' and 'S' will do a 10 fold jump. To take a shot press 'space bar'. The cueball can be stopped by pressing 'z' or 'x' for all 
balls. Right click on the mouse + moving will move the camera. The arrows wil move the camera around. Movement is relative to the in game 
coordinate system, not to the viewpoint of the observer.

# Mac/linux instructions

## Setting up your environment

Setup up an environment:  

```python3 -m venv ./env```

and activate it:  

```source ./env/bin/activate``` for linux/mac

## Get the source code

Clone the repository:  

```git clone https://github.com/thedidymen/vpool```

## Install the dependencies

The project requires several libraries to function. Change into the directory (default: vpool). 
Please install the requirements:  

```pip install -r requirements.txt```

## Change to milestone-branch

Further development will happen on the main-branch, so please checkout the oplevering-branch: 

```git checkout oplevering```

## Starting the application

Players names can be altered at the end of the vpool.py file. 
Easy mode is currently enabled and can be disabled at the end file.

The application can be started by:  

```python vpool.py```

# Windows instructions

Ik ga uit van de situatie zoals die is bij begin van het
practicum. Vscode geinstalleerd en een werkende terminal
en python 3.10.

installeer git voor windows:
https://git-scm.com/download/win

Default instelling zou moeten werken, doe een reboot (want windows)
Nu zou git moeten werken in de de terminal van VsCode.

Creeer in de prompt een directory en verander in de directory. Hier
een voorbeeld voor tmp, check of deze niet al bestaat!

```mkdir tmp```
```cd tmp```

Windows doet moeilijk met environments, hiervoor moet een
policy gezet worden

```Set-ExecutionPolicy -Scope CurrentUser```

geef dan ```Unrestricted``` op.

creeer een environment:
```python3 -m venv env```

activeer environment:
```./env/Scripts/activate```

Clone de repository:
```git clone https://github.com/thedidymen/vpool.git```

Verander van directory:
```cd vpool```

verander van branch:
```git checkout oplevering```

Check de branch met:
```git status```
De eerste regel geeft aan op welke branch je zit.

installeer de requirements:
```pip install -r requirements.txt```

Start het programma:
```python vpool.py```

check allow access.

Verwijderen van het programma:

vanuit de directory vpool
```cd ../..```

Let op! dit verwijdert heel tmp inclusief eventuele andere bestanden check of alleen vpool hierin staat!
```rm -r -force <path to tmp>```

Voor mij was dat:
```rm -r -force C:\Users\rcvan\tmp```
