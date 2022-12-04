from tkinter import *
import pandas as pd
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    en_word = current_card["English"]
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(title_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=en_word, fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    es_word = current_card["Español"]
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(title_text, text="Español", fill="white")
    canvas.itemconfig(word_text, text=es_word, fill="white")


def is_known():
    to_learn.remove(current_card)
    next_card()


def save_data():
    pd.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    window.destroy()


window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, flip_card)

# Images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")


# Canvas
canvas = Canvas(width=800, height=526)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
card_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Button
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.protocol("WM_DELETE_WINDOW", save_data)

window.mainloop()
