# Audio-tools
#UPDATE:
NEW FILE: audio_tools.py
          this file contains multiple functions for audio processing, mainly 3, these take an array as input (so use wavfile.read() beforehand, this allows for               easier implementation within pipelines):
          compress: applies a compressor to normalize the volume, may be useful on its own as a preprocess but its used mostly for a more stable word separation
           Example: signal_c=compress(signal,-30,1000,0,1.0,500) (how compressors work: https://www.youtube.com/watch?v=pGl8L4fFC14&ab_channel=PiercePorterfield)
          phone: applies a phone "filter" that transforms an audio into what it would sound like if it came from a phone, useful for training phone ASR models
                 Example: signal_phone=telephone(signal,fs)
          get_words: a new approach to separation.py, basically this is less clumsy/chaotic, the results are stable but are usually longer than those
                     that result from the original separation
                     this function creates a subdirectory called "words/" and fills it with segments automatically, return() is obsolete
                     i didnt test the execution time to compare but i believe this version is more optimal
                     this works when multiple speakers are talking (one after the other) at different volumes without risking that sentences get skipped
                     this also (and im practically 100% sure of this) prevents words from being split in half, but it causes segments to be significantly longer
                     than the old version (you can expect files of 30 seconds to one minute on average)
                     you can lower the value "9300" in line 117 to have smaller segments but risk word cutoff
                     there's also a new parameter, mult, at first i meant for the parameter to signify if multiple (not simultanious) speakers exist, and thus
                     to decide if a compression of the signal is necessary or not, in theory i wanted it to be able to replicate the old separation function if
                     mult was different than 1. But with experimentation, it seems that it cant, BUT it also seems to be able to separate the speakers!
                     (for a file from ARP with two talkers, setting mult to 0 results in two long wav files, but each containing the part of one of the
                     speakers)
                     these processes are highly empirical so its hard to garantee results but im quite satisfied with this version, its downfall is that the 
                     output segments are conciderably (and unavoidably) much longer
                     Example: get_words(signal,fs,1.3,1)



Denoise: takes input that contains one word and noise, extracts the word. Example: >denoise("denoise.wav")

Separation: Takes input that contains multiple words/sentences, extracts each and outputs it separately. Example: >separation("separation.wav",0.8)

Removesilence: Takes input that contains phones separated by silence, concatenates them into a word. Example: >removesilence("removesilence.wav")
