soundproject
============

One morning, my fellow PhD student and were at coffee when we got a
fun idea for a project: why don't we try to make our computers talk to
each other in Morse Code? In the end, this proved much more difficult
than anticipated, but we did manage to transmit signals from my
computer to his as long as we held the microphone within a few inches
of the speaker. You can find the complete program [here](https://github.com/TheNursery/TheNurseryLibrary/tree/master/soundproject).

Included here is just the transmission side of the project. You can
type text into the command prompt, and the text is converted to
audible Morse Code, which is either written to a .wav file or played
out loud by the computer, depending on input parameters. 

# Instructions

To run the Morse Code transmission:

```sh
python continuous_input.py
```

To write the Morse Code transmission to a .wav file:

```sh
python continuous_input.py -w 1
```

To learn about more options:

```sh
python continuous_input.py -h
```

It is also possible to run the morse.py script directly on a string
input. For example, the following will play a Morse Code transmission
of "Hello World":

```sh
python morse.py "Hello World"
```

To write this to a file, test.wav, instead, use the following command:

```sh
python morse.py "Hello World" -f test.wav -w 1
```

To find out about more options:

```sh
python morse.py -h
```

# Packages

The code in this project uses the following special Python packages:

```sh
argparse, wave, struct, alsaaudio
```

The code was written and tested using Python 2.7.6.