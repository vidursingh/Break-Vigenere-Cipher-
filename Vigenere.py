"""
CSP HW1. Vidur Singh. All rights reserved. 
"""



#this function does a frequency analysis on a text file, given the file address.
#returns frequencies as percentage. 
def frequency_analysis(filename):
    file = open(filename, "r")
    frequency_dict = {}
    line = file.readline()

    while line:
        for i in line:
            char = i.lower()

            #ignore non alphabet characters 
            if (ord(char)<97 or ord(char)>122) and ord(char)!= 32:
                continue

            if char in frequency_dict:
                frequency_dict[char] = frequency_dict[char] + 1

            elif char not in frequency_dict:
                frequency_dict[char] = 1
        line = file.readline()
    frequencylist = []
    for i in range(0,26):
        frequencylist += [frequency_dict[chr(97+i)]]
    total = sum(frequencylist)

    for i in range(0, 26):
        frequencylist[i] = (frequencylist[i]*100)/total

    return(frequencylist)

#similar frequency calculator, given a string.
def frequency_on_string(line):
    frequency_dict = {}

    for i in line:
        char = i.lower()

        if (ord(char)<97 or ord(char)>122) and ord(char)!= 32:
            continue

        if char in frequency_dict:
            frequency_dict[char] = frequency_dict[char] + 1

        elif char not in frequency_dict:
            frequency_dict[char] = 1

    frequencylist = []

    for i in range(0,26):
        try:
            frequencylist += [frequency_dict[chr(97+i)]]
        except:
            frequencylist += [0]
    total = sum(frequencylist)

    for i in range(0, 26):
        frequencylist[i] = (frequencylist[i]*100)/total

    return(frequencylist)

#returns the inpt string shifted by "shift" value. 
def shift(inpt, shift):
    output = ""  #output string for particular string 
    for char in inpt:  #for each character in input string:
        #append chr(ord(char)-97 (so that a has value of 0) + i(current shift) %26
        #(26 letters) + 97 (to get back to actual ascii values))
        output = output + chr(97+(ord(char)-97+shift)%26)  
    return(shift, output)

#finds "distance" of expected frequency (calculated using the book "pride and prejudice", and actual frequency (of a possible plain text)
def geterror(expectedfrequency, actualfrequency):
    analysisforletters = "abcdefghijklmnopqrstuvwxyz"   #put into this string, the letters which you want to consider while finding the distance. 
    analysisforindices = [ord(letter)-97 for letter in analysisforletters]
    error = 0
    for i in analysisforindices:
        error = error + abs(expectedfrequency[i]-actualfrequency[i])  #can use absolute or root of (squared error). Results vary. 
    
    return error

pandpfrequency = frequency_analysis("pride and prejudice.txt")

#open and read the input file. 
filename = "inputfile.txt"
file = open(filename, "r")
cyphertext = ""
line = file.readline().rstrip()
while line:

    cyphertext = cyphertext + line
    line = file.readline().rstrip()



# [[a,f,g,a,f,f], [p,a,f,a,s,f]]

overallminerror = 10000000000000   #arbitrarily large number so that the minimum error will update.
overall_i = 0   #value for the overall value of i (len of key word) with best results. 
overall_shifts =[]   #value of shifts for each letter of the keywor with best results.

#for all possible lengths of key word (1-6):
for i in range(1,7):
    l = []  #will store the divided up cypher text
    
    for index in range(0, i):
        l = l +[""]  #string of form ["","",""....i times ]

    index = 0  #reset variable
    
    for index in range(0, len(cyphertext)):
        l[index%i] = l[index%i] + str(cyphertext[index])  #divide cypher text into groups of i.
        
    index = 0  #reset variable again.
    
    currentminerror = 0  #value for minimum error for a particular length of keyword.

    shifts = []  #will store the shifts of the keyword (basically, [0,2,2] means keyword is "acc"

    #len(l) = currently assumed keyword length. (iterate through the letters of the keyword) 
    for index in range(0, len(l)):
        
        minimumerror = 100000  #arbitrarily high value.
        minimumerrorshift = 0   #some value
        minimumerrorshiftedstring = ""  #some value. 

        for j in range(0, 26):  #for all possible shifts:
            shiftnumber, shiftedstring = shift(l[index], j)  #shift the current substring by j.
            frequency_list = frequency_on_string(shiftedstring)  #do frequency analysis on it. 
            error = geterror(pandpfrequency, frequency_list)   #get sum of squared error on these values. 

            #if this error is less than the minimum error so far for the current substring, update values of minimum error and shifts etc. 
            if error < minimumerror:
                minimumerror= error
                minimumerrorshift = shiftnumber
                minimumerrorshiftedstring = shiftedstring

        #after completing one substring, append the value of the shift that led to the least error to the list "shifts"
        shifts = shifts + [26 - minimumerrorshift]  #by the end of the outer for loop, this list will store the shifts with least error for each substring
        
    overall_shifts += [shifts]




#putting the cyphertext back:
index =0
l=[]
minerror = 100000000
finaloutput = ""
alloutputs = []


#print ("POSSIBLE SOLUTIONS FOR EACH KEY LENGTH ARE:")
#alloutputs contains the "plain texts" for the keyword with the best results for each possible length (between 1 and 6)
for index in range(0,len(overall_shifts)):
    currentoutput = ""
    currenterror = 0
    shifts = overall_shifts[index]
    
    for letter in range(0, len(cyphertext)):
        currentoutput += chr(((ord(cyphertext[letter])-97 - shifts[letter%len(shifts)])%26)+97)
    currenterror = geterror(pandpfrequency, frequency_on_string(currentoutput))
    alloutputs += [currentoutput]

#find the element in alloutputs whose frequency most closely matches that of english(Pride and Prejudice)
for element in alloutputs:
    frequency = frequency_on_string(element)
    error = geterror(pandpfrequency, frequency)
    #print all the "best" plain texts for each possible length of the keyword. Doing this because sometimes
    #the plain text with the least distance from english, may not be the actual plaintext.
    print("POSSIBLE DECRYPTION:")
    print(element)
    print()
    print()

    if error < minerror:
        minerror = error
        finaloutput = element

#this is likely to be the right answer, however, may be wrong. 
print("MOST LIKELY ANSWER, BASED ON FREQUENCY ANALYSIS IS (this answer may be wrong):")
print(finaloutput)
