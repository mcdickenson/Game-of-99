### The Game of 99
### Created by Matt Dickenson, mcdickenson_at_gmail_dot_com
### Released under a Creative Commons License, Dec 28, 2011

from Tkinter import *
import random

# making text to print on the game board buttons intially
buttonLabels = [ '0', '73', '72', '71', '70', '69', '68','67', '66', '65', ' ', '74', '57', '58', '59', '60', '61', '62', '63', '64', '99', '75', '56', '21', '20', '19', '18', '17', '36', '37', '98', '76', '55', '22',  '13', '14', '15', '16', '35', '38', '97', '77', '54', '23', '12', '1', '4', '5', '34', '39', '96', '78', '53', '24', '11','2','3', '6', '33', '40', '95', '79', '52', '25', '10', '9', '8', '7', '32', '41', '94', '80','51','26','27','28','29','30','31','42','93', '81', '50', '49', '48', '47', '46', '45', '44', '43', '92', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91']
buttonLabelsOld= [ '0', '73', '72', '71', '70', '69', '68','67', '66', '65', ' ', '74', '57', '58', '59', '60', '61', '62', '63', '64', '99', '75', '56', '21', '20', '19', '18', '17', '36', '37', '98', '76', '55', '22',  '13', '14', '15', '16', '35', '38', '97', '77', '54', '23', '12', '1', '4', '5', '34', '39', '96', '78', '53', '24', '11','2','3', '6', '33', '40', '95', '79', '52', '25', '10', '9', '8', '7', '32', '41', '94', '80','51','26','27','28','29','30','31','42','93', '81', '50', '49', '48', '47', '46', '45', '44', '43', '92', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91'] # see line 231 for why this is needed

class MyBoard:
    def __init__(self, myParent):   # this is where I initialize the game
        self.myContainer1 = Frame(myParent)
        self.myContainer1.grid()
        self.start()                # sets all starting variables
        self.makeLayout()           # makes the frame layout
        self.makeBoard()            # makes the game board
        self.makeTurnButtons()      # makes the turn buttons
        self.makePlayerNames()      # prints players' names and their markers (initially blank)
        self.makeText()             # makes the text input/output section
        

    def start(self):                # this is where I set up all the variables to be used throughout 
        self.currentTextOut='Welcome to 99. How many players?'
        self.whatToDo='setPlayers'
        self.playerNames = ['', '', '', '']
        self.playerMarkers = ['','','', '']
        self.currentPlayer = 0 
        self.gameDeck=range(100)         # self.deck with cards 0-99
        random.shuffle(self.gameDeck)    # shuffle the cards
        self.hands = [ [], [], [], [] ]  # a blank one for 0, 1, 2, 3
        self.allowableCardRange = 100    # prevents button from being clickable at first
         
        
    def makeLayout(self): # makes basic layout, with optional title: 
        #self.mainLabel = Label(self.myContainer1, font=('Helvetica',24), text = 'The Game of 99', fg='blue')
        #self.mainLabel.grid(row=0, columnspan=13, sticky=N)
        # make sure that columnspan is the width of the whole frame

        self.blankLabel = Label(self.myContainer1, text='      ') # a blank column
        self.blankLabel.grid(row=1, column=11)

        self.deckDisplay = Listbox(self.myContainer1, font=('Helvetica', 12), fg='red', height=7)
        self.deckDisplay.grid(row = 6, rowspan=3, column=12, columnspan=1, sticky=N)

        self.deckShowButton = Button(self.myContainer1, text='Show Deck', width=9, height=1, command=lambda: self.displayDeck())
        self.deckShowButton.grid(row=6,column=13, sticky=N, padx=10, pady=10)
        
        self.deckHideButton = Button(self.myContainer1, text='Hide Deck', width=9, height=1, command=lambda: self.hideDeck())
        self.deckHideButton.grid(row=7, column=13, sticky=N, padx=10, pady=10)

            
    def makeBoard(self): # this draws the board
        self.buttonDict = {}
        buttonNum = 1

        for rowNum in range(1,11):
            for colNum in range(10):
                thisButton = buttonNum #using "thisButton = (rowNum-1)*10 + (colNum+1)" was slightly slower

                self.buttonDict[thisButton] = Button(self.myContainer1, text=buttonLabels[thisButton], width=2, height=2, command= lambda x=thisButton: self.onClick(x))
                self.buttonDict[thisButton].grid(row=rowNum, column=colNum)
     
                buttonNum += 1


    def makeTurnButtons(self): # this part creates four buttons for a player's choices on their turn
        self.buttonDraw = Button(self.myContainer1, text='Draw', width=4, height=1, command=lambda: self.addCard())
        self.buttonDraw.grid(row=12, column=12, sticky=N)

        self.buttonDiscard = Button(self.myContainer1, text = 'Discard', width=7, height=1, command=lambda: self.removeCard())
        self.buttonDiscard.grid(row=12, column=13, sticky=N)

        self.buttonSkip = Button(self.myContainer1, text='Skip', width=4, height=1, command=lambda: self.nextPlayer())
        self.buttonSkip.grid(row=13, column=12, sticky=N)

        self.buttonPlay = Button(self.myContainer1, text='Play', width=4, height=1, command=lambda: self.playCard())
        self.buttonPlay.grid(row=13, column=13, sticky=N)

                
    def makePlayerNames(self): # this function displays players' names as they are given, and their markers
        self.playerSectionLabel = Label(self.myContainer1, font = ('Helvetica', 18), text = 'Player', fg='black', underline=3)
        self.playerSectionLabel.grid(row=1, column=12, sticky=W)

        self.markerSectionLabel = Label(self.myContainer1, font = ('Helvetica', 18), text = 'Marker', fg='black')
        self.markerSectionLabel.grid(row=1, column=13, sticky=E)

        self.playerNamesDict = {}
        self.pMarksDict = {}
        for pNum in range(1,4):
            self.playerNamesDict[pNum] = Label(self.myContainer1, font=('Helvetica', 16), text=self.playerNames[pNum], fg='black')
            self.playerNamesDict[pNum].grid(row=1+pNum, column=12, sticky=W)

            self.pMarksDict[pNum] = Label(self.myContainer1, font= ('Helvetica', 16), text = self.playerMarkers[pNum], fg='black')
            self.pMarksDict[pNum].grid(row=1+pNum, column=13, sticky=E)

    def makeText(self): # this creates the text entry and output at bottom-left of the frame
        self.currentTextOut = self.currentTextOut + ((' ') * (45-len(self.currentTextOut)))
        
        self.textOutput = Label(self.myContainer1, font = ('Helvetica', 18), fg='blue', text = self.currentTextOut, width=45)
        self.textOutput.grid(row=12, column=0, columnspan=10, sticky=W)

        self.textInput = Entry(self.myContainer1, bg='lightblue', fg='black', font=('Helvetica', 16))
        self.textInput.grid(row=13, column=0, columnspan=6, sticky=W)

        self.textEnter = Button(self.myContainer1, text='Enter', width=5, height=1, padx=10, pady=10, command=lambda: self.enterText(self.whatToDo))
        self.textEnter.grid(row=13, column=7, columnspan=3, sticky=W)      

    
    def nextPlayer(self):

        if self.currentPlayer == self.numPlayersInt:
            self.currentPlayer = 1

        elif self.currentPlayer < self.numPlayersInt:
            self.currentPlayer += 1 

        self.currentTextOut = ("It is " + self.playerNames[self.currentPlayer] + "'s turn.")

        self.deckDisplay.delete(0, END)
        self.makeBoard()
        self.makeText()

        
    def playCard(self):
        if len(self.hands[self.currentPlayer])>0:
            self.currentTextOut=('Which card would you like to play, ' + self.playerNames[self.currentPlayer] + '?')
            self.makeText()
            self.whatToDo = 'getCardName'


    def onClick(self, number): # takes place when a button in the board is clicked
        if (self.currentPlayer>0) & (self.currentPlayer<4) & (buttonLabels[number] in buttonLabelsOld):
            if (int(buttonLabels[number])>=self.allowableCardRange):
                buttonLabels[number] = self.playerMarkers[self.currentPlayer]

                for i in range(0, len(self.hands[self.currentPlayer])): 
                    if self.hands[self.currentPlayer][i-1] == self.allowableCardRange: # which is the card played
                        del self.hands[self.currentPlayer][i-1]
            
                self.allowableCardRange=100
                self.nextPlayer()


    def displayDeck(self): # this displays the current player's self.deck

        self.deckDisplay.delete(0, END) # clears self.deck, to prevent double-printing
        self.tempcard = []

        for i in range(0,len(self.hands[self.currentPlayer])):
            self.tempcard.append(str(self.hands[self.currentPlayer][i]))
            cardText = (self.tempcard[i] + " to 99")
            self.deckDisplay.insert(END, cardText) 


    def hideDeck(self): # this empties the listbox, hiding the player's self.deck
        self.deckDisplay.delete(0, END)  


    def addCard(self): # add a card to the current player's self.deck
        if len(self.hands[self.currentPlayer]) <5:
           
            newCard = self.gameDeck.pop(0)
            self.hands[self.currentPlayer].append(newCard)
            self.nextPlayer()
            #self.makeText()

        else:
            self.currentTextOut = (self.playerNames[self.currentPlayer] + " already has 5 cards. Discard or play.")
            self.makeText()


    def removeCard(self): # this will remove a chosen card from the player's hand
        self.currentTextOut = "Which card would you like to discard?"
        self.whatToDo='deleteCard'
        self.makeText()
        
        
    def enterText(self, thingToDo): # this is the real workhorse function of the game; it gets the state of the world and outputs and inputs text accordingly
    # in practice, the only variables that should get passed to this function are self and self.whatToDo

        self.currentTextIn = self.textInput.get()[0:10]

        if thingToDo == 'setPlayers': # make this only accept a number
            self.numPlayersStr = self.currentTextIn
            
            if self.numPlayersStr == '2' or self.numPlayersStr == '3':
                self.numPlayersInt=int(self.numPlayersStr)
                self.currentTextOut = ("Ok, " + self.numPlayersStr + " players. What is player 1's name?")

                self.whatToDo='getPlayer1Name'
                self.makeText()
            else: 
                self.whatToDo='setPlayers'
                self.makeText()

        elif thingToDo == 'getPlayer1Name': 
            self.playerNames[1] = self.currentTextIn
            self.playerMarkers[1] = 'X' 
            
            self.currentTextOut= ("What is player 2's name?")

            self.whatToDo='getPlayer2Name'
            self.makePlayerNames()
            self.makeText()

        elif thingToDo == 'getPlayer2Name':
            self.playerNames[2] = self.currentTextIn
            self.playerMarkers[2] = 'O'

            if self.numPlayersInt == 2:
                
                self.currentTextOut = ("It is " + self.playerNames[1] + "'s turn.")
                self.currentPlayer=1
                self.whatToDo='p1turn'
                self.makePlayerNames()

            elif self.numPlayersInt == 3:
                self.currentTextOut= ("What is player 3's name?")
                self.whatToDo= 'getPlayer3Name'
                self.makePlayerNames()

            else:
                self.whatToDo='setPlayers'

            self.makeText()

        elif thingToDo == 'getPlayer3Name':
            self.playerNames[3] = self.currentTextIn
            self.playerMarkers[3] = '*'
 
            self.currentTextOut = ("It is " + self.playerNames[1] + "'s turn.")
            self.currentPlayer=1
            self.whatToDo='p1turn'
            self.makePlayerNames()
            self.makeText()
            
        elif thingToDo == 'getCardName': 

            self.attemptedCard = self.currentTextIn
            self.attemptedCardInt = int(self.attemptedCard) # this could be a problem if the string is not a num

            if self.attemptedCardInt in range(0,100): # in buttonLabels2:
                
                if self.attemptedCardInt in self.hands[self.currentPlayer]:

                    self.allowableCardRange=self.attemptedCardInt
                    
                    self.whatToDo = 'playSpot'
                    self.currentTextOut = ("Mark any open spot from " + self.attemptedCard + " to 99."   ) 
                    self.makeText()

                else:
                    self.currentTextOut = "You don't have that card. Enter a card from your hand."
                    self.makeText()
                
            else:
                self.currentTextOut = "That is not allowed. Please enter a card."                      
                self.makeText()
                
        elif thingToDo == 'playSpot':
            self.currentTextOut = ("Mark any open spot from " + self.attemptedCard + " to 99.")
            self.makeText()

        elif thingToDo == 'deleteCard':
            cardToRemove = self.currentTextIn

            cardRemInt = int(cardToRemove)

            if cardRemInt in self.hands[self.currentPlayer]:
                for i in range(0, len(self.hands[self.currentPlayer])): 
                    if self.hands[self.currentPlayer][i-1] == cardRemInt: # which is the card played
                        del self.hands[self.currentPlayer][i-1]

                self.nextPlayer()
                
            else:
                self.currentTextOut = "Please enter a card from your hand."
                self.makeText()

        else:
            self.makeText()


# this part initializes the actual game
root = Tk()
root.geometry('800x610+350+120')    # size and position of the game window
myboard = MyBoard(root)             # place elements in window
root.title('The Game of 99')        # window title
root.mainloop()                     # start the game

