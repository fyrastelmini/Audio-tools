import scipy
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat


#This function takes as input a string containing the name of the input file, it outputs a file called "mot0.wav", names and directories can be changed.
#Call it this way: >removesilence("sounds.wav")



def removesilence(nom):
    inputch="./"+nom #.wav file path, name given as an input       
    fs, data = wavfile.read(inputch)

#channels/encoding conversion: converts 256kbps/512kbps(stereo or mono) input into 512kbps-mono,
    if len(data.shape)==1:
        data = data
    else:
        data=data.sum(axis=1) / 2
    if data.dtype=='int16':
        data = data/32767
        data=data.astype('float32')

#where the magic happens

    m=stat.mean(abs(data))

    pas=5000
    indices=[]
    segments=[]
#this loop identifies the "louder" chunks or the audio input and keeps them, makes the "quiet" chunks silent
    for i in range(0,len(data),pas):
        tmp=[]
        if i>=len(data):
            break
        else:
            tmp=data[i:i+pas]
            if   stat.mean(abs(tmp))<0.5*(m):
                for j in range(i,i+pas):
                    indices.append(False)
                    

            else:
                for k in range(i,i+pas):
                    indices.append(True)
                    

    ma=min(len(data),len(indices))
    for i in range(ma,max(len(data),len(indices))):  #this solves an error caused by array sizes not being equal
        indices.pop()


    audio=data*indices  #audio array contains now the "lowder" chunks, with the "quiet" set at 0

    j=0

    audio2=data.tolist() #transform array to list for later computation, the datatype of the original array is lost at this point, this is why this function converts all input to the same format: to conserve the datatype

#deleting variables for memory management (important when the input is a long audio file)
    del data
    del indices
  
    segment=[]
#this loop identifies individual chunks of the audio list and saves each one inside the list called "segments"
    for i in range(0,len(audio),10):
        if not(j==0):
            if not(stat.mean(abs(audio[j:i]))==0):
                    segment.extend(audio2[j:i])
           
            else:
                if not(segment==[])or (segments==[]):
            
                        segments.append(segment[:])
                        segment.clear()
                
        j=i
    for i in segments: #solves a bug where segments contains empty lists
        if (i==[]):
            segments.remove(i)
    indice=0



#output

    audiol=[]
    for i in segments:
        for j in range(len(i)):
            audiol.append(i[j])  #takes each point of each segment and appends it to a list, at this point the audio list contains all segments back to back without the silence inbetween them
    audio=np.array(audiol) #list into array for exporting

    file="mot"+str(indice)+".wav"  #name of the output file

    audio = (audio).astype('float32') #setting the corresponding dataype for 512kbps
    outputaudio="./"+file  #adresse output
    scipy.io.wavfile.write(outputaudio, fs, audio )



