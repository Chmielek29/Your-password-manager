from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import random
import pyperclip
import json

# ------------------------ RANDOM PASSWORD GENERATOR ------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate():

    password_list = []

    password_list += [random.choice(letters) for _ in range(random.randint(8, 10))]

    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    password = password_entry.get()
    website = website_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
#Checks if fields are empty
    if len(password) == 0 or len(website) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            password_entry.delete(0, END)
            website_entry.delete(0, END)

#Search for saved password at picked website
def search():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Not existing website", message="There is no data for this website")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website.title(), message=f"Email is: {email}\nPassword is: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky=W)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky=W)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky=W)

#Entries
website_entry = Entry(width=34)
website_entry.grid(row=1, column=1, sticky=W)
website_entry.focus()
email_entry = Entry(width=53)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W)
email_entry.insert(0, "YOUR MAIL")
password_entry = Entry(width=34)
password_entry.grid(row=3, column=1, sticky=W)

#Buttons
generate_password = Button(text="Generate Password", command=generate, width=17)
generate_password.grid(row=3, column=2, sticky=W)
add_button = Button(text="Add", width=52, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky=W)
search_button = Button(text="Search", command=search, width=17)
search_button.grid(row=1, column=2, columnspan=2,sticky=W)

window.mainloop()
