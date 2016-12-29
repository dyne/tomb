# gtomb
A GUI for Tomb (https://www.dyne.org/software/tomb/)

`gtomb` is a wrapper for another wrapper called [Tomb](https://github.com/dyne/Tomb)  
It is imagined to make usage of Tomb even easier for end-users.

## Usage
![gtomb UI](https://github.com/parazyd/gtomb/raw/master/screenshot.png "gtomb UI")  
The UI consists of all commands included in Tomb. You can choose a command you wish to run via the
list and the script will run it for you. Easy-peasy.

### Random notes
* If you type in your sudo password once correctly, in the next 5 (or whatever your sudoers timeout is) minutes, you can type in the wrong password as well.
* The function for catching cancellation sometimes fails because of bad ps syntax. (Possibly fixed, needs more testing)

## Dependencies
* [tomb](https://github.com/dyne/Tomb) (also get tomb's dependencies)
* zenity

## TODO
* Complete error checking
* and more stuff 

## What you need to do
* Be patient or help with coding :)
* Request features
