import scipy
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

##This function takes as input a string with the name of the input file, and a value or the parameter coeff, it outputs multiple .wav files containing each a part of the file, the length isnt of each output isnt determined in advance but depends on the value of coeff, coeff should be adapted to each input
##Input file must be in the same folder as this file, call this function as such: separation("file_name.wav",value_of_coeff)
##Coeff values are for example: 0.1,0.3,0.8 etc.. use values between 0 and 1
##Lower coeff values mean that the code "tolerates" lower sounds more, this makes sure that the separation happens at the end of the word/sentence so that the lower sounding phones (example:"bi","fa") dont get cut off. But this may cause the output segments to be larger in duration
##Higher coeff values make the code "tolerate" less, this makes the duration of the outputs shorter, but at the risk of ignoring lower sounding phones
##Empyrically, the best value for coeff makes the code separate the input into segments of a minimal duration without ignoring parts of the words
##For example: for monotonous sound files with a duration of 20minutes, the value seems to be around 0.2

def separation(fichier,coeff):
    inputch="./"+fichier
    print("(1/5) loading file")
    fs, data = wavfile.read(inputch) #input reading
    ##conversion to 512kbps-mono
    ddtype=data.dtype
    if len(data.shape)==1:
        data = data
    else:
        data=data.sum(axis=1) / 2
##    if data.dtype=='int16':
##        data = data/32767
##        data=data.astype('float32')
    
    print("datatype is: ",ddtype)
    ##computation
    m=stat.mean(abs(data))
    pas=5000
    indices=[]
    segments=[]
    print("(2/5) starting separation")
    for i in range(0,len(data),pas):
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
                    
    
    ma=min(len(data),len(indices))

    for i in range(ma,max(len(data),len(indices))):
        indices.pop()


    audio=data*indices
    del data
    del indices
    j=0

    audio2=(audio).tolist()

    
    





    segment=[]
    print("(3/5) storing segments")
    for i in range(0,len(audio),10): 
        if not(j==0):
            if not(stat.mean(abs(audio[j:i]))==0): 
                    segment.extend(audio2[j:i])
           
            else:
                if not(segment==[])or (segments==[]):
            
                        segments.append(segment[:])
                        segment.clear()
                
        j=i
    for i in segments:
        if (i==[]):
            segments.remove(i)
    indice=0
    
    
    print("(4/5) preparing output")
    for i in segments:
        audio=np.array(i)
        
        if len(audio)<16000:
            continue
        file="mot"+str(indice)+".wav"
        indice=indice+1
        
        audio = (audio).astype(ddtype)
        outputaudio="./"+file
        scipy.io.wavfile.write(outputaudio, fs, audio )
    print("(5/5) Output finished")
