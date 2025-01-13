import tkinter as tk
import tkinter.messagebox
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    label.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
    window.after_cancel(timer) # This stops the timer
    global reps
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    checkmark_label.config(text="", fg=GREEN, bg=YELLOW,  font=(FONT_NAME, 25))

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # If it's the 1st, 3rd, 5th, 7th rep.. so time to work
    if reps % 2 != 0:
        time = work_sec
        label.config(text="Work", fg = RED, font=(FONT_NAME, 50, "bold"))

    # If it's the 8th rep, then it's time for a long break
    elif reps % 8 == 0:
        time = long_break_sec
        label.config(text="Long Break", fg = GREEN, font=(FONT_NAME, 50, "bold"))
        show_long_break_message()

    # If its the 2nd, 4th, 6th rep, then it's time for a short break
    elif reps % 2 == 0:
        time = short_break_sec
        label.config(text="Short Break", fg = PINK, font=(FONT_NAME, 50, "bold"))
        show_short_break_message()

    count_down(time)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    # This section deals with formatting the time to be displayed in the format MM:SS

    count = int(count) 

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = "0" + str(count_sec)

    if count_min < 10:
        count_min = "0" + str(count_min)

    canvas.itemconfig(timer_text, text = f"{count_min}:{count_sec}")

    # This initialises a countdown timer to count down every second
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count -1) 

    # If the count reaches 0, then start the timer again, and add a checkmark for each work session done
    if count == 0:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"	
        checkmark_label.config(text = marks)

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Banadora")
window.config(padx=100, pady=50, bg=YELLOW)

label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
label.grid(column=1, row=0)

checkmark_label = tk.Label(text="", fg=GREEN, bg=YELLOW,  font=(FONT_NAME, 25))
checkmark_label.grid(column=1, row=3)

# Setting up the buttons

start_button = tk.Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Setting the image
tomato_img = tk.PhotoImage(file="tomato.png")

canvas = tk.Canvas(width=300, height=300, bg=YELLOW, highlightthickness=0) # setting canvas to have same bg color and remove border
canvas.create_image(50, 50, image=tomato_img, anchor="nw")
timer_text = canvas.create_text(155, 175, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Setting pop-up message

def show_short_break_message():
    tkinter.messagebox.showinfo("Break Time", "Time for a break!")

def show_long_break_message():
    tkinter.messagebox.showinfo("Long Break", "You have 20 minutes of break!")


window.mainloop()