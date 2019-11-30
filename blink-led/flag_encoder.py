#from flags import *

alpabete = {'A':".-",
'B':"-...",
'C':"-.-.",
'D':"-..",
'E':".",
'F':"..-.",
'G':"--.",
'H':"....",
'I':"..",
'J':".---",
'K':"-.-",
'L':".-..",
'M':"--",
'N':"-.",
'O':"---",
'P':".--.",
'Q':"--.-",
'R':".-.",
'S':"...",
'T':"-",
'U':"..-",
'V':"...-",
'W':".--",
'X':"-..-",
'Y':"-.--",
'Z':"--..",
'0':"-----",
'1':".----",
'2':"..---",
'3':"...--",
'4':"....-",
'5':".....",
'6':"-....",
'7':"--...",
'8':"---..",
'9':"----.",
")":"-.--.-",
"(":"-.--."
}

def str_to_morse(string): 
   morsecode = []
   for char in string.upper():
      morsecode.append(alpabete[char].replace('.', '0').replace('-', '1') )
   return morsecode

def converter(arraystr):
	arrayout1 = []
	arrayout2 = []
	for ss in arraystr:
		if ss[0] == "0":
			arrayout1.append(ss)
			arrayout2.append(-1)
		else:
			arrayout1.append('')
			arrayout2.append(int(ss, 2))
	return arrayout1, arrayout2

flag_3 = "GH19(dec0dem0rs3f1rmw4r3)"

flag = flag_3.upper()
array = str_to_morse(flag)
print("flag len : ", len(flag))
print("flag is : "+ flag)
flagstr, flagint = converter(array)
print("flagstr = ", flagstr)
print("flagint = ", flagint)
