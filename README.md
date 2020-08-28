# Audio-tools
Denoise: takes input that contains one word and noise, extracts the word. Example: >denoise("denoise.wav")

Separation: Takes input that contains multiple words/sentences, extracts each and outputs it separately. Example: >separation("separation.wav",0.8)

Removesilence: Takes input that contains phones separated by silence, concatenates them into a word. Example: >removesilence("removesilence.wav")
