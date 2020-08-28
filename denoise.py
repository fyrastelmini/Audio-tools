import scipy
import numpy as np
from scipy.io import wavfile
import statistics as stat

##This function takes as input a .wav file, it returns a .wav file of the same name that overwrites the original input, it can also output a .wav file of the same name that contains the noisy parts of the original file under a directory called "/bruit"
##The input parameter are: >fichier: name of the input file, could also be a subdirectory of the current location of this function (example: fichier = test.wav or fichier = audio/test.wav"
##                         >keepnoise: boolean, if set to True, the function will also output a .wav file of the same name as the input at a subdirectory called "/bruit", you must create this subdirectory or else an error will happen
##                         >coeff: the "tolerence", if sat too low this would cause noise to stay in the output, if sat too high this might cause an empty output, defaut value of 0.8 seems to work file, dont change this unless absolutely necessary
def denoise(fichier,keepnoise=False,coeff=0.8):
    #initializations
    bruit_final=[]
    maax=[]
    audio3=[]
    #5ms of silence is equivalent to an array of zeros of length around 800
    audio4=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    inputch="./"+fichier #input location, defaulted to current folder
    fs, data = wavfile.read(inputch)
    ddtype=data.dtype
    pas=1000
    indices=[]
    segments=[]

    
    #conversion from stereo to mono if input is stereo
    if len(data.shape)==1:
        d = data
    else:
        d=data.sum(axis=1) / 2
    del data #used d instead of data so i clear this variable instead of having to rename every d as data.. 


    #segmentation starts here
    m=stat.mean(abs(d)) 
    for i in range(0,len(d),pas): #this part segments the sound file directly
        tmp=[]
        if i>=len(d):
            return
        else:
            tmp=d[i:i+pas]
            if   stat.mean(abs(tmp))<coeff*(m): #default coeff set to 0.8
                for j in range(i,i+pas):
                    indices.append(True) 
            else:
                for k in range(i,i+pas):
                    indices.append(False) 
    ma=min(len(d),len(indices))
    for i in range(ma,max(len(d),len(indices))):
        indices.pop()
    indices2=[not i for i in indices]
    audio=indices2*d #this an array that contains higher segments (contains word or word + noise)


    
    #conversion of arrays to lists for later computation
    audio2=audio.tolist()
    if keepnoise==True: #storing the noise if you want them as separate output
        bruit=indices*d #this an array that contains lower sounding segments (presumed to be noise)
        bruit2=bruit.tolist()
    segment=[]


    #this part stores each segment of audio inside a list, this is necessary since the audio list can still contain noise and this helps determine which segment contains the word
    j=0
    for i in range(0,len(audio),10):
        if not(j==0):
            if not(stat.mean(abs(audio[j:i]))==0):
                    segment.extend(audio2[j:i])
            else:
                if not(segment==[])or (segments==[]):   
                        segments.append(segment[:])
                        segment.clear()        
        j=i
    for i in segments: #this loop clears empty segments so that they dont interfere in later computation
        if i==[]:
            segments.remove(i)
    if(len(segments)==0): #if segments is empty (which means that the entire file was presumed to be lower sounding noise) the function returns the input, this avoids errors in execution        
        scipy.io.wavfile.write("./"+fichier, fs, d )
        return   


    #this part determines which of the segments contains the word, and stores it
    for i in range(len(segments)): #segments is not empty, this loop searches for the most "energetic" segment which is the most likely to contain the word
        maax.append(sum(abs(np.asarray(segments[i]))))  
    if maax==[]: #this verification is done to avoid critical errors, input is returned as output         
        scipy.io.wavfile.write("./"+fichier, fs, d )
        return

    m1=max(maax)
    for j in range(len(segments)): #this loop identifies the most "energetic" segment and stored it into the output list
        if sum(abs(np.asarray(segments[j])))==m1:
            audio3=segments[j]
            segments.pop(j)
            break;
    if keepnoise==True: #storing the noise if you want them as separate output
        for i in segments:
            for j in i:
                bruit2.append(j)


    #output
    for i in audio3: #output happens here
        audio4.append(i)
    audio3=np.array(audio4)
    audio3 = (audio3).astype(ddtype)

    scipy.io.wavfile.write("./"+fichier, fs, audio3 )
    if keepnoise==True:
        bruit3 = np.array(bruit2)
        bruit3 = (bruit3).astype(ddtype)
        scipy.io.wavfile.write("./bruit/"+fichier, fs, bruit3 )        
    return
