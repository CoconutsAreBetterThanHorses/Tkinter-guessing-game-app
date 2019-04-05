import tkinter as tk
import random

#model
window = tk.Tk()
window.title('Guess the capital')
fulldict = {'Argentina':'buenosaires', 'Austria':'vienna', 'Belgium':'brussels', 'Brazil':'brasilia', 'Canada':'ottawa', 
'Chile':'santiago', 'China':'beijing', 'Denmark':'copenhagen', 'Egypt':'cairo', 'Estonia':'tallinn', 
'Ghana':'accra', 'Hungary':'budapest', 'Indonesia':'jakarta', 'Iraq':'baghdad', 'Japan':'tokio', 
'Kenya':'nairobi', 'Mexico': 'mexicocity', 'New Zealand':'wellington', 'Philippines':'manila','Romania':'bucharest', 
'Saudi Arabia':'riyadh', 'South Africa':'capetown', 'Turkmenistan':'ashgabat', 'United Kingdom':'london', 'Vietnam':'hanoi'}
dictwordvar = tk.StringVar()
guesswordvar = tk.StringVar()
resultvar = tk.StringVar()

#transforming to readable format
dictword = dictwordvar.get()
dictword = random.choice(list(fulldict.keys()))
dictwordvar.set(dictword)
failures=[]
failuremax = 5 #the attempt amount
answer = False

#controller
def counter(): #the attempt counter
	failures.append(1)
	if sum(failures) >= failuremax:
		window.destroy()

def click1(): #checking the answer
	guessword = guesswordvar.get()
	guessword = guessword.replace(' ', '').lower()  #eliminating the value errors
	result = resultvar.get()
	if fulldict[dictword] == guessword:
		global answer
		answer = True
		result = ('That\'s right!')
	else:
		counter()
		result = ('You didn\'t guess! The attempt #' + str(sum(failures)+1))
	resultvar.set(result)

def click2(): #setting new country
	global dictword
	global answer
	dictword = random.choice(list(fulldict.keys()))
	dictwordvar.set(dictword)
	if answer == False:
		counter()
		result = ('You didn\'t guess the previous capital! The attempt #' + str(sum(failures)+1))
		resultvar.set(result)
	else:
		answer = False #returning to initial position

def click3(): #exit the program
	window.destroy()

#view
frame = tk.Frame(window)
frame.pack()
countrylabel = tk.Label(frame, width=40, textvariable=dictwordvar)
countrylabel.pack()
capitalentry = tk.Entry(frame, width=30, textvariable=guesswordvar)
capitalentry.pack()
resultlabel = tk.Label(frame, textvariable=resultvar)
resultlabel.pack()
tk.Button(frame, text='Check', width=20, font='arial 10', command=click1).pack()
tk.Button(frame, text='New country', width=17, font='arial 10', command=click2).pack()
tk.Button(frame, text='Quit', width=14, font='arial 10', command=click3).pack()
window.mainloop()