import scipy
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

##This function takes as input a string with the name of the input file, and a value or the parameter coeff, it outputs multiple .wav files containing each a part of the file, the length isnt of each output isnt determined in advance but depends on the value of coeff, coeff should be adapted to each input
##Input file must be in the same folder as this file, call this function as such: separation("file_name.wav",value_of_coeff)
##Coeff values are for example: 0.1,0.8,1.5 etc.. use values between 0 and 2
##Lower coeff values mean that the code "tolerates" lower sounds more, this makes sure that the separation happens at the end of the word/sentence so that the lower sounding phones (example:"bi","fa") dont get cut off. But this may cause the output segments to be larger in duration
##Higher coeff values make the code "tolerate" less, this makes the duration of the outputs shorter, but at the risk of ignoring lower sounding phones
##Empyrically, the best value for coeff makes the code separate the input into segments of a minimal duration without ignoring parts of the words
##For example: for monotonous sound files with a duration of 20minutes, the value seems to be around 0.2, for a clear voice file of 15 seconds, the value seems to be around 1.5

def separation(fichier,coeff):
    inputch="./"+fichier
    print("(1/5) loading file")
    fs, data = wavfile.read(inputch) #input reading
    ##conversion to mono
    ddtype=data.dtype
    if len(data.shape)==1:
        data = data
    else:
        data=data.sum(axis=1) / 2
    ##computation
    #initializations
    m=stat.mean(abs(data))
    pas=5000
    indices=[]
    segments=[]
    print("(2/5) starting separation")
    for i in range(0,len(data),pas): #this part segments the sound file directly 
        tmp=[]
        if i>=len(data):
            break
        else:
            tmp=data[i:i+pas]
            if   stat.mean(abs(tmp))<coeff*(m):
                for j in range(i,i+pas):
                    indices.append(False)
            else:
                for k in range(i,i+pas):
                    indices.append(True)
    #this avoids a critical error
    ma=min(len(data),len(indices))
    for i in range(ma,max(len(data),len(indices))):
        indices.pop()
    #segmenting audio directly (inserting zeros where silence is perceived)
    audio=data*indices
    #deleting the variables that are no longer used, this helps when dealing with larger sound files, to avoir memory errors
    del data
    del indices
    audio2=(audio).tolist() #convertion to list for later computation
    #initializations
    segment=[]
    print("(3/5) storing segments")
    j=0
    #this loop stores each segment into a list of segments
    for i in range(0,len(audio),10): 
        if not(j==0):
            if not(stat.mean(abs(audio[j:i]))==0): 
                    segment.extend(audio2[j:i])
           
            else:
                if not(segment==[])or (segments==[]):
            
                        segments.append(segment[:])
                        segment.clear()
                
        j=i
    #this solves a critical error
    for i in segments:
        if (i==[]):
            segments.remove(i)
    #Output
    print("(4/5) preparing output")
    indice=0
    for i in segments:
        audio=np.array(i)
        
        if len(audio)<16000: #this checks if the segment is long enough to contain at least one word, if not it ignores it (some segments may contain impultions, this solves it)
            continue
        file="mot"+str(indice)+".wav" #output name
        indice=indice+1
        
        audio = (audio).astype(ddtype)
        outputaudio="./"+file
        scipy.io.wavfile.write(outputaudio, fs, audio ) #output
    print("(5/5) Output finished")
