import tkinter as tk
from tkinter import messagebox
import random
import requests

# TMDB API call setup
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer "
}

def get_movie_titles():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movie_titles = [movie['title'] for movie in data['results']]
        return movie_titles
    else:
        print("Failed to fetch movies:", response.status_code)
        return []

# Initial setup
movies = get_movie_titles()
word = random.choice(movies).lower()

guesses = 6
guessed_letters = []

# Tkinter setup
root = tk.Tk()
root.title("Hangman")

canvas = tk.Canvas(root, width=300, height=300)
canvas.grid(column=0, row=0)
canvas.create_line(20, 280, 120, 280)
canvas.create_line(70, 280, 70, 20)
canvas.create_line(70, 20, 170, 20)
canvas.create_line(170, 20, 170, 50)

# Display masked word (only letters hidden, space and & shown)
masked_word = " ".join(["_" if letter.isalpha() else letter for letter in word])
word_label = tk.Label(root, text=masked_word)
word_label.grid(column=0, row=1)

guesses_label = tk.Label(root, text="Guesses remaining: {}".format(guesses))
guesses_label.grid(column=0, row=2)

guessed_label = tk.Label(root, text="Guessed letters: ")
guessed_label.grid(column=0, row=3)

guess_entry = tk.Entry(root)
guess_entry.grid(column=0, row=4)

def check_guess():
    global guesses
    global guessed_letters
    global word_label

    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)

    if len(guess) != 1 or (not guess.isalpha() and guess not in [" ", "&"]):
        return

    if guess in guessed_letters:
        return

    guessed_letters.append(guess)
    guessed_label.config(text="Guessed letters: {}".format(" ".join(guessed_letters)))

    if guess in word:
        current_display = list(word_label["text"])
        for i in range(len(word)):
            if word[i] == guess:
                current_display[2 * i] = guess
        word_label.config(text="".join(current_display))

        if "_" not in current_display:
            messagebox.showinfo("Hangman", "You win!")
            exit_button.grid(column=0, row=6)
            guess_entry.config(state=tk.DISABLED)
            return
    else:
        guesses -= 1
        guesses_label.config(text="Guesses remaining: {}".format(guesses))

        if guesses == 5:
            canvas.create_oval(140, 50, 200, 110)
        elif guesses == 4:
            canvas.create_line(170, 110, 170, 170)
        elif guesses == 3:
            canvas.create_line(170, 130, 140, 140)
        elif guesses == 2:
            canvas.create_line(170, 130, 200, 140)
        elif guesses == 1:
            canvas.create_line(170, 170, 140, 190)
        elif guesses == 0:
            canvas.create_line(170, 170, 200, 190)
            messagebox.showinfo("Hangman", "You lose! The word was '{}'".format(word))
            exit_button.grid(column=0, row=6)
            guess_entry.config(state=tk.DISABLED)

def retry_game():
    global word, guesses, guessed_letters

    word = random.choice(movies).lower()
    guesses = 6
    guessed_letters = []

    word_label.config(text=" ".join(["_" if letter.isalpha() else letter for letter in word]))
    guesses_label.config(text="Guesses remaining: {}".format(guesses))
    guessed_label.config(text="Guessed letters: ")
    guess_entry.config(state=tk.NORMAL)
    canvas.delete("all")

    canvas.create_line(20, 280, 120, 280)
    canvas.create_line(70, 280, 70, 20)
    canvas.create_line(70, 20, 170, 20)
    canvas.create_line(170, 20, 170, 50)

    exit_button.grid_forget()

def exit_game():
    root.destroy()

exit_button = tk.Button(root, text="Exit", command=exit_game)

root.bind("<Return>", lambda event: check_guess())

root.mainloop()
