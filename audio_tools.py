from scipy.io import wavfile
import struct
import numpy as np
import time
import os
from scipy.signal import butter,lfilter





chunk_size = 512*2

def get_db(signal):
	num_chunk  = len(signal) // chunk_size
	sn = []
	for chunk in range(0, num_chunk):
		sn.append(np.mean(signal[chunk*chunk_size:(chunk+1)*chunk_size]**2))
	for i in range(len(sn)):
		if sn[i]==0:
			sn[i]=0.00001
	
	logsn = 10*np.log10(sn)
	return(logsn)

def active_nr(signal,coeff): #nullifies silences
	num_chunk  = len(signal) // chunk_size
	indice=[]
	decibels=get_db(signal)
	#print(decibels)
	moy=np.mean(decibels)
	for chunk in range(0, num_chunk):
		if (decibels[chunk]<(moy)*coeff):
			for i in range(chunk_size):
				indice.append(0)
		else:
			for i in range(chunk_size):
				indice.append(1)
	indice=np.array(indice, dtype=np.int16)
	signal=signal[0:num_chunk*chunk_size]
	signal=signal*indice
	return(signal)
def active_nri(signal,coeff): #a version of active_nr that returns a binairy array used for word separation
	num_chunk  = len(signal) // chunk_size
	indice=[]
	decibels=get_db(signal)
	#print(decibels)
	moy=np.mean(decibels)
	for chunk in range(0, num_chunk):
		if (decibels[chunk]<(moy)*coeff): #the bigger coeff is the more it leaves
			for i in range(chunk_size):
				indice.append(0)
		else:
			for i in range(chunk_size):
				indice.append(1)
	#indice=np.array(indice, dtype=np.int16)
	return(indice)
def compress(signal,threshold,ratio,makeup,attack,release): #compressor, used within get_words
	#attack and release time constant
	a=np.exp(-np.log10(9)/(44100*attack*1.0E-3))
	re=np.exp(-np.log10(9)/(44100*release*1.0E-3))

	data=signal.copy()
	data[np.where(data==0)]=0.00001 #prevents log(0)
	#convert to dB
	data_dB=20*np.log10(abs(data))
	dataC=[]
	n=len(data_dB)
	for i in range(n):
		#compression
		dataC.append(threshold+(data_dB[i]-threshold)/(ratio))
	gain=np.zeros(n)
	sgain=np.zeros(n)
	#calculate gain
	gain=np.subtract(dataC,data_dB)

	sgain=gain.copy()
	#smoothen gain
	for i in range (1,n):
		if sgain[i-1]>=sgain[i]:
			sgain[i]=(a*sgain[i-1]+(1-a)*sgain[i])#*0.5
		if sgain[i-1]<sgain[i]:
			sgain[i]=(re*sgain[i-1]+(1-re)*sgain[i])#*0.5
	#Array for the smooth compressed data with makeup gain applied
	dataCs=np.zeros(n)
	dataCs=data_dB+sgain+makeup
	#Convert our dB data back to bits
	dataCs_bit=10.0**((dataCs)/20.0)
	#sign the bits appropriately:
	for i in range (n):
		if data[i]<0.0:
			dataCs_bit[i]=-1.0*dataCs_bit[i]
	return dataCs_bit


def normalize(signal): #this doesnt work when you use compression for a reason i couldnt understand

	data=signal.copy()
	data[np.where(data==0)]=0.00001
	#convert to dB
	print(np.where(data==0))
	data_dB=20*np.log10(abs(data))
	diff=0-max(data_dB)
	
	data_dB_norm=data_dB+diff
	
	data_norm=10.0**((data_dB_norm)/20.0)
	data_norm[np.where(data==0.00001)]=0
	n=len(data_dB)
	for i in range (n):
		if data[i]<0.0:
			data_norm[i]=-1.0*data_norm[i]

	return(data_norm)

def sub(ind,liste,listetmp): #this checks if a word is cut, technically you can lower the value "9300" but it could cause words to be segmented, the 9300 is a safe thershold but could cause longer segments
	if ind-listetmp[-1]> 9300:
		return(True)
		
	else: return (False)
		
def get_words(signal,fs,coeff,mult): #mult corresponds to multiple (but not simultaniuous) speakers, if its at 1, compression will be applying to normalize the volume through the wav file
	chunk_size_2=chunk_size*2
	num_chunk  = len(signal) // chunk_size_2
	if mult==1:
		signal_nr=active_nr(signal,coeff) #nullifying silences
	#wavfile.write("nr.wav",fs,signal_nr)
		signal_c=compress(signal_nr,-30,1000,0,1.0,500)
	#wavfile.write("comp.wav",fs,signal_c)
	else:	
		signal_nr=active_nr(signal,coeff)
		signal_c=signal_nr
	words_ind=active_nri(signal_c,coeff)

	l_ind=[] #this is a list of lists, each internal list contains a word
	tmp=[]
	for i in range(len(words_ind)): #gathering segments while making sure words dont get separated
		if i==(len(words_ind)-1):
				if not tmp ==[]:
					l_ind.append(tmp)
		elif words_ind[i]==1:
			if i==0:
				tmp.append(i)
				continue
			elif words_ind[i-1]==1:
				tmp.append(i)
				continue
			elif sub(i,l_ind,tmp) :
				l_ind.append(tmp)
				tmp=[]
				continue
			
				
			else:
				tmp.append(i)
				continue
		
		
		else:
			continue
	indi=0
	print(len(l_ind))
	if not os.path.exists("./words"):
		os.mkdir("./words")
	for i in l_ind: #exporting loop
		if len(i)<2*chunk_size_2: #skips segments that are too short which are assumed to be just noise
			print("skip")
			continue
		else:
			print("looping")
			minn=min(i)
			maxx=max(i)
			out=np.array(signal[minn:maxx]).astype(np.float32) #list needs to be transformed into an array of float32/int16 to be exported
			wavfile.write("words/out"+str(indi)+".wav",fs,out)
			indi=indi+1
	
	return words_ind

def telephone(filename,fs):
    out=bandpass(filename,fs,300,3400,3)
    return(out)

def bandpass(signal,sr,f1,f2,Q=1): #bandpass filter, input is signal (array), sr: sampling rate, f1/f2: cutoff frequencies, Q: filter ratio
    data=signal
    b, a = butter(Q,Wn=(f1/sr,f2/sr),btype='bandpass')
    data_filtered=lfilter(b,a,data,axis=0)
    return data_filtered



start=time.time()

#INPUT
fs,signal= wavfile.read("out0.wav")
get_words(signal,fs,1.3,1)
#use compress/phone/get_words functions here
# export using wavfile.write("name_output.wav",fs,signal)



#######################################################################################################################
########################################### tests here, feel free to ignore ###########################################
#######################################################################################################################
#signal_int16=np.int16(signal)
#1024 #* 2
#num_chunk  = len(signal) // chunk_size


#for chunk in range(0, num_chunk):
	
#	sn.append(np.mean(signal[chunk*chunk_size:(chunk+1)*chunk_size]**2))
#logsn = 10*np.log10(sn)

#signal=active_nr(signal,1.2)
#db2=get_db(signal)
#print(signal)
#print(db2)
#print(max(db2))
#print(np.mean(db2))

#print(signal.dtype)
#signal=np.int16(signal)
#######signal_nr=active_nr(signal,1.9)
#######signal_c=compress(signal_nr,-30,1000,0,1.0,500)
#signal_final=np.array(signal_c).astype(signal.dtype)
#print(signal_final)
#signal_nr=active_nr(signal_final,1.2)
#signal_norm=normalize(signal_final)

#words=get_words(signal_c)
#get_words(signal_c)
#print('Done!')
#end=time.time()
#elapsed=int(1000*(end-start))
#print('...............................')
#print('Completed in '+str(elapsed)+' milliseconds.')
#signal_phone=telephone(signal,fs)
#wavfile.write("phone.wav",fs,signal_phone)
#print('Done!')
#end=time.time()
#elapsed=int(1000*(end-start))
#print('...............................')
#print('Completed in '+str(elapsed)+' milliseconds.')
#print(shape(words),type(words))
#words=np.array(words).astype(np.float32)
#print(words.shape,words.dtype)
#print(words)
#wavfile.write("out.wav",fs,signal_nr)
#wavfile.write("compressed.wav",fs,signal_final)
#wavfile.write("normalized.wav",fs,signal_norm)
#wavfile.write("words.wav",fs,words)
