import wave
import struct
import math
import argparse
import alsaaudio
import sys

class Morse:

    MORSE_DICT = {
        'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

    def __init__(self, dot_length, frequency, framerate, amplitude):
        self.dot_length = dot_length
        self.dash_length = 3*self.dot_length
        self.lspace_len = self.dash_length
        self.wspace_len = 2*self.dash_length

        self.freq = frequency
        self.framerate = framerate

        if amplitude > 1.0: amplitude = 1.0
        if amplitude < 0.0: amplitude = 0.0
        amplitude = amplitude * 32767
        self.amp = amplitude


    def dot(self):
        return self.tone(self.dot_length) + self.space(self.dot_length)

    def dash(self):
        return self.tone(self.dash_length) + self.space(self.dot_length)

    def lspace(self):
        return self.space(self.lspace_len)

    def wspace(self):
        return self.space(self.wspace_len)

    def tone(self, length):

        period = int(self.framerate / self.freq)
        
        # clip to an integer number of periods for better sound quality
        length = length - length%period

        pac_vals = []

        for i in range(length):
            val = int(float(self.amp) * 
                      math.sin(2.0*math.pi*float(self.freq)*
                               (float(i%period)/float(self.framerate))))
            # To write a wav file, we pack the integer values as C struct
            # short signed integers
            pv = struct.pack('h', val)
            pac_vals.append(pv)

        pac_valstr = ''.join(pac_vals)
        return pac_valstr

    def space(self, length):

        pac_vals = []

        for i in range(length):
            pv = struct.pack('h', 0)
            pac_vals.append(pv)

        pac_valstr = ''.join(pac_vals)
        return pac_valstr

    def getMorse(self, output_string, debug=False):

        values = []
    
        output_string = output_string.upper()

        for char in output_string:
            if char.isspace():
                packed_value = self.wspace()
                values.append(packed_value)
                if (debug): print char
            elif char.isalnum():
                morse_str = self.MORSE_DICT[char];
                for dd in morse_str:
                    if dd == '-':
                        packed_value = self.dash()
                    elif dd == '.':
                        packed_value = self.dot()
                    else:
                        print 'character not understood:', dd
                        break
                    values.append(packed_value)
                packed_value = self.lspace()
                values.append(packed_value)
                if (debug): print char, morse_str
            else:
                raise ValueError(char)

        value_str = ''.join(values)

        return value_str


def writeMorse(output_string, debug=False, filename='morse_output.wav',
               frequency=450.0, dot_length=1000):

    channels = 1
    sample_size = 2
    frame_rate = 44100
    number_of_frames = 0  # number of frames corrected by writeframes() later
    compression_type = 'NONE'
    compression_name = 'not compressed'

    amp = 0.5

    my_morse = Morse(dot_length, frequency, frame_rate, amp)

    try:
        value_str = my_morse.getMorse(output_string, debug=debug)

        noise_output = wave.open(filename, 'w')
        noise_output.setparams((channels, sample_size, frame_rate, 
                                number_of_frames, compression_type, 
                                compression_name))
        noise_output.writeframes(value_str)
    except ValueError:
        raise ValueError

    noise_output.close()

    return filename

def playMorse(output_string, debug=False, frequency=450.0, dot_length=1000):

    channels = 1
    sample_size = 2                      # bytes per sample
    frame_size = channels * sample_size  # bytes per frame
    frame_rate = 44100                   # frames per second

    period_size = frame_rate

    pcm = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
    pcm.setchannels(channels)
# PCM format for ALSA audio (PCM_FORMAT_S16): 
#   Signed 16 bit samples for each channel
#   matches sample_size of 2 bytes in writeMorse() and choice of short signed 
#   int struct packing in tone() and space()
    if (sys.byteorder == 'little'):
        pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE) # Little endian byte order
    else:
        pcm.setformat(alsaaudio.PCM_FORMAT_S16_BE) # Big endian byte order
    pcm.setrate(frame_rate)
    pcm.setperiodsize(period_size)

    amp = 0.5
    my_morse = Morse(dot_length, frequency, frame_rate, amp)

    try:
        valstr = my_morse.getMorse(output_string, debug=debug)
        pcm.write(valstr)
    except ValueError:
        raise ValueError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', 
                        help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-w', '--wavfile', 
                        help="Output as wav file", default=0, type=int)
    parser.add_argument('-f', '--filename', 
                        help="Filename to write wav file", 
                        default='morse_output.wav', type=str)
    parser.add_argument('-l', '--dot_length', 
                        help="Length of one dot", default=1000, type=int)
    parser.add_argument('-F', '--frequency', 
                        help="Carrier frequency", default=450.0, type=float)
    parser.add_argument('output_string', help="String to convert to morse")
    args = parser.parse_args()

    if (args.wavfile):
        try:
            fn = writeMorse(args.output_string, 
                            debug=args.debug, 
                            filename=args.filename,
                            frequency=args.frequency,
                            dot_length=args.dot_length)
            print 'Wrote file to ', fn
        except ValueError:
            print 'Invalid character: Use only alphanumeric characters.'
    else:
        try:
            playMorse(args.output_string,
                      debug=args.debug,
                      frequency=args.frequency,
                      dot_length=args.dot_length)
        except ValueError:
            print 'Invalid character: Use only alphanumeric characters.'


if __name__ == "__main__":
    main()
