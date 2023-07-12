from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

FONT = ("Arial", 10, "bold")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for i in range(randint(8, 10))]
    password_symbols = [choice(symbols) for i in range(randint(2, 4))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # Copying the password string into the clipboard
    pyperclip.copy(password_entry.get())

# ---------------------------- SEARCH ------------------------------- #


def find_password():
    website_name = website_entry.get()
    if len(website_name) == 0:
        return
    try:
        with open("data.json", "r") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning("Error", "No data file found.")
    else:
        if website_name in file_data:
            email = file_data[website_name]["email"]
            password = file_data[website_name]["password"]
            messagebox.showinfo(website_name, f"Email/Username: {email}\nPassword: {password}")
            pyperclip.copy(password)

        else:
            messagebox.showwarning("Details not found", f"No details for {website_name} exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website_data = website_entry.get()
    email_data = email_user_entry.get()
    password_data = password_entry.get()
    new_data = {website_data: {
        "email": email_data,
        "password": password_data
     }
    }

    if len(website_data) == 0 or len(email_data) == 0 or len(password_data) == 0:
        messagebox.showwarning(title="Blank fields", message="Please fill in all the blank fields!\n")
    else:
        try:
            with open(file="data.json", mode="r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as file:
                json.dump(new_data, file)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open(file="data.json", mode="w") as file:
                # Writing both the old data and the new data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


# Creating the main window
window = Tk()
window.title("Password Manager")
window.config(pady=30, padx=30)

# Creating the logo
logo_image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Creating labels, entries and buttons
website_label = Label(text="Website:", font=FONT)
website_label.grid(row=1, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_user_label = Label(text="Email/Username:", font=FONT)
email_user_label.grid(row=2, column=0)

email_user_entry = Entry(width=35)
email_user_entry.grid(row=2, column=1, columnspan=2)
email_user_entry.insert(0, "defaultEmail@gmail.com")

password_label = Label(text="Password:", font=FONT)
password_label.grid(row=3, column=0)

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)

generate_password_button = Button(text="Generate\n Password", font=FONT, width=12, command=generate_password)
generate_password_button.grid(row=3, column=3, padx=10)

add_button = Button(text="Add", font=FONT, width=25, padx=5, pady=5, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", font=FONT, width=11, padx=5, pady=5, command=find_password)
search_button.grid(row=1, column=3)


window.mainloop()
