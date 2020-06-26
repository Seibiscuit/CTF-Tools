# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:31:13 2020

@author: Biscuit
"""

from pydub import AudioSegment #pip install filetype
import binascii

def getInfo(default_vars):
    """
    Runs through the different variables that come in challenges.
    """
    
    print("Paste values into prompt or enter q to reset or quit\n\
          If value not given then enter 0.\n\nValues in parenthesis\n\
          will be passed if user presses enter to go to the next line\n")

    for key, value in default_vars.items():
        ip = input(f"What is the value of {key}? ({value})\n")
        if ip == "q": break
        elif ip != "": 
            default_vars[key] = ip
    
    return default_vars

    
def decode(default_vars):
    '''
    Takes input file and measures the volume every frames skipped from the starting point.
    It converts it based on the threshold and whether high or low are 1 or 0.
    
    The file should sound like the volume is going up and down.
    
    Starting position can be different than 0. Some files start with 10 ms dead zone.
    Some files could not have its secret message start until later in the song.
    
    Frames to skip will probably be different. To identify what should be put into
    this field, open the file in audacity and zoom all the way in. Identify where
    an isolated digit would be, like a 010 or 101. Look at the time stamp and see
    how long that digit is held for, in my case the file was 150 ms long.
    
    Threshold is just at what point a 1 will be a 1 and 0 will be a 0. In my case,
    the lows were between 0 and -2 and the highs were between -16 and -18. So to be 
    safe I could go from -3 to -15 and I would have still decoded my message.
    
    Reversing threshold is just reversing the 1s and 0s position. In my case 1 was
    the softer volume and 0 was the louder volume. If 0 was the softer volume and 1
    was the louder volume than I would set reversing threshold to "true".
    
    '''
    
    #Unpack
    filename = default_vars["filename"]       
    starting_position = int(default_vars["starting position"])
    frames_to_skip = int(default_vars["frames to skip"])
    threshold = int(default_vars["threshold"])
    reversing_threshold = default_vars["reversing threshold"]
    
    song = AudioSegment.from_wav(filename) #imports song file
    chopped = [ frame.dBFS for frame in song[starting_position::frames_to_skip] ] #holds raw valumes
    transcribed = [] #holds the 1s and 0s based on raw volumes
    
    if reversing_threshold == "false":
        transcribed = ["1" if volume > threshold else "0" for volume in chopped]
#    EQUATES TO ===
#    for volume in chopped:  #pulls volume
#        if volume > -3:     #compares volume with threshold
#            transcribed.append("1") #sets to 1 if above threshold
#        else: transcribed.append("0") #sets to 0 if below threshold
    else:
        transcribed = ["1" if volume < threshold else "0" for volume in chopped]
#    the sign is reversed

            
    transcribed = ''.join(transcribed) #removes spaces
    while (len(transcribed)%8 != 0): transcribed = transcribed[:-1] #sees if transcribed is divisible by 8, if not trims trailing numbers
    
    bytes_transcribed = int(transcribed,2) #converts string to bytes object
    ascii_transcribed = binascii.unhexlify("%x" % bytes_transcribed) #converts binary to ascii
    ascii_transcribed = str(ascii_transcribed)[2:-1] #converts bytes to string object and trims leading b" and trailing "
    
    return ascii_transcribed #returns message as string
        
        
def output(message):
    print(f"If the message does not make sense, try reversing the threshold \n\
          changing the amount of frames skipped, changing the starting\n\
          or slightly adjusting the threshold \n\n {message}")

def main():
    default_vars = {                                \
            "filename":"constantTone.wav",          \
            "starting position":"0",                \
            "frames to skip":"150",                 \
            "threshold":"-3",                       \
            "reversing threshold":"false"}
    
    while True:
        default_vars = getInfo(default_vars)
        message = decode(default_vars)
        output(message)
        userInput = input("Type quit to exit or press Enter to continue\n")
        if userInput == "quit":
            break

if __name__ == '__main__':
    main()
