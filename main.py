from tkinter import *
import pandas as pd
import random

current_card = {} # making an empty dict so that both functions can use the same dict
to_learn = {}
try:
    de_df = pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    orignal_data = pd.read_csv("de_words.csv")
    to_learn = orignal_data.to_dict(orient="records") #orient record makes this dict into a list 
else:
    to_learn = de_df.to_dict(orient="records") # the records orientations gives the required orientation where each word has its translations

#Constants
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel",40,"bold","italic")
WORD_FONT = ("Ariel",55,"bold","italic")

#Functions
def next_card():
    global current_card,flip_timer #making both the variables global so that both the function can access these.
    window.after_cancel(flip_timer) #for every time we go to a new card we will invalidate this timer
    current_card = random.choice(to_learn)
    de_card = current_card["German"]
    canvas.itemconfig(card_title,text=f"Deutsch",fill="black")
    canvas.itemconfig(de_word,text=f"{de_card}",fill="black")
    canvas.itemconfig(card_bg,image=card_front_img)
    flip_timer = window.after(4000,func=flip_card)

def flip_card():
    canvas.itemconfig(card_bg,image=card_back_img)
    canvas.itemconfig(card_title,text="English",fill = "white")
    canvas.itemconfig(de_word,text = current_card["English"],fill = "white")
    
def known_card():
    to_learn.remove(current_card) # it removes the current_card from the dict 
    known_words = pd.DataFrame(to_learn)
    known_words.to_csv("words_to_learn.csv",index=False)
    next_card()
    
    
#UI
window = Tk()
window.title("FlashCards")
window.minsize()
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer = window.after(4000,func=flip_card) #windows after will call the function after 2s 

canvas = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
card_front_img = PhotoImage(file="images\card_front.png")
card_back_img = PhotoImage(file="images\card_back.png")
card_bg = canvas.create_image(400,263,image = card_front_img)
card_title = canvas.create_text(400,150,text=f"title",font=TITLE_FONT)
de_word = canvas.create_text(400,263,text="word",font=WORD_FONT)
canvas.grid(column=0,row=0,columnspan=2)

cross_img = PhotoImage(file="images\wrong.png")
cross_button = Button(image=cross_img,highlightthickness=0,command=next_card)
cross_button.grid(row=1,column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img,highlightthickness=0,command=known_card)
right_button.grid(row=1,column=1)

next_card()

#Reading_data



window.mainloop()

