import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pyrebase

# -------- Firebase Config --------
firebaseConfig = {
    "apiKey": "AIzaSyAB3VS_AOXkvWBJz9OpTVdSUuQDeSoitMY",
    "authDomain": "test-9438d.firebaseapp.com",
    "databaseURL": "https://test-9438d-default-rtdb.firebaseio.com/",
    "projectId": "test-9438d",
    "storageBucket": "test-9438d.firebasestorage.app",
    "messagingSenderId": "294037294245",
    "appId": "1:294037294245:web:cd64d2fbf0342e3f5f514c",
    "measurementId": "G-0LG8NPVQ77"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# -------- UI Setup --------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x600")
app.title("VaultSafe")
app.resizable(True, True)

def show_frame(frame):
    for f in (signin_frame, signup_frame, google_signup_frame):
        f.pack_forget()
    frame.pack(expand=True, fill="both")

def create_password_entry(parent, var, placeholder="Password"):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(pady=(5, 5))

    entry = ctk.CTkEntry(frame, textvariable=var, placeholder_text=placeholder,
                         show="*", width=270, border_color="black", border_width=1)
    entry.grid(row=0, column=0, sticky="w")

    show_pw = {"visible": False}

    def toggle():
        show_pw["visible"] = not show_pw["visible"]
        entry.configure(show="" if show_pw["visible"] else "*")
        btn.configure(image=eye_open_icon if show_pw["visible"] else eye_closed_icon)

    btn = ctk.CTkButton(frame, text="", width=30, height=30, fg_color="transparent",
                        hover_color="#f3f4f6", image=eye_closed_icon,
                        command=toggle, border_width=0)
    btn.grid(row=0, column=1, padx=(5, 0))
    return entry

def create_entry(parent, placeholder):
    entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300,
                         border_color="black", border_width=1)
    entry.pack(pady=5)
    return entry

# -------- Load Icons --------
eye_open_icon = ctk.CTkImage(Image.open(r"C:\Users\mudit\VaultSafe\icons\icons8-eye-24.png"), size=(20, 20))
eye_closed_icon = ctk.CTkImage(Image.open(r"C:\Users\mudit\VaultSafe\icons\icons8-hide-24.png"), size=(20, 20))
google_ctk_img = ctk.CTkImage(Image.open(r"C:\Users\mudit\VaultSafe\icons\google.png"), size=(20, 20))

# -------- Sign In Frame --------
signin_frame = ctk.CTkFrame(app)
signin_container = ctk.CTkFrame(signin_frame, width=360, height=460, corner_radius=10)
signin_container.pack(expand=True)
signin_container.pack_propagate(False)

ctk.CTkLabel(signin_container, text="VaultSafe", font=("Arial", 24, "bold")).pack(pady=(30, 20))

email_entry = ctk.CTkEntry(signin_container, placeholder_text="E-mail", width=300,
                            border_color="black", border_width=1)
email_entry.pack(pady=(10, 10))

password_var = ctk.StringVar()
password_entry = create_password_entry(signin_container, password_var, placeholder="Password")

email_entry.bind("<Return>", lambda e: password_entry.focus())
password_entry.bind("<Return>", lambda e: handle_signin())

def handle_signin():
    email = email_entry.get()
    password = password_var.get()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        messagebox.showinfo("Login Success", f"Welcome, {email}")
    except:
        messagebox.showerror("Login Failed", "Invalid credentials")

link_frame = ctk.CTkFrame(signin_container, fg_color="transparent")
link_frame.pack(fill="x", padx=30)

ctk.CTkLabel(link_frame, text="Don’t have an account? ", font=("Arial", 10)).grid(row=0, column=0, sticky="w")

create_link = ctk.CTkLabel(link_frame, text="Create new account", text_color="#6366F1",
                           font=("Arial", 10, "underline"), cursor="hand2")
create_link.grid(row=0, column=1, sticky="w")
create_link.bind("<Button-1>", lambda e: show_frame(signup_frame))

ctk.CTkLabel(link_frame, text="Forgot Password?", text_color="#6366F1",
             font=("Arial", 10, "underline"), cursor="hand2").grid(row=0, column=2, sticky="e", padx=(30, 0))

ctk.CTkButton(signin_container, text="Sign in", width=120, command=handle_signin).pack(pady=(25, 10))

ctk.CTkLabel(signin_container, text="OR", font=("Arial", 12, "bold")).pack(pady=(10, 10))

ctk.CTkButton(
    signin_container,
    text="  Sign in With Google",
    width=250,
    fg_color="white",
    hover_color="#f3f4f6",
    text_color="black",
    border_color="black",
    border_width=2,
    image=google_ctk_img,
    anchor="w",
    command=lambda: show_frame(google_signup_frame)
).pack(pady=10)

# -------- Sign Up Frame --------
signup_frame = ctk.CTkFrame(app)
signup_card = ctk.CTkFrame(signup_frame, width=400, height=600, corner_radius=10,
                           fg_color="white", border_color="black", border_width=1)
signup_card.pack(expand=True)
signup_card.pack_propagate(False)

ctk.CTkLabel(signup_card, text="VaultSafe - Sign Up", font=("Arial", 24, "bold")).pack(pady=(25, 10))

name_entry = create_entry(signup_card, "Your Name")
username_entry = create_entry(signup_card, "Username")
email_signup_entry = create_entry(signup_card, "E-mail")
mobile_entry = create_entry(signup_card, "Mobile no.")
password_signup_var = ctk.StringVar()
password_signup_entry = create_password_entry(signup_card, password_signup_var, placeholder="Password")
confirm_signup_var = ctk.StringVar()
confirm_password_entry = create_password_entry(signup_card, confirm_signup_var, placeholder="Confirm Password")

name_entry.bind("<Return>", lambda e: username_entry.focus())
username_entry.bind("<Return>", lambda e: email_signup_entry.focus())
email_signup_entry.bind("<Return>", lambda e: mobile_entry.focus())
mobile_entry.bind("<Return>", lambda e: password_signup_entry.focus())
password_signup_entry.bind("<Return>", lambda e: confirm_password_entry.focus())
confirm_password_entry.bind("<Return>", lambda e: handle_signup())

def handle_signup():
    email = email_signup_entry.get()
    password = password_signup_var.get()
    confirm = confirm_signup_var.get()
    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return
    try:
        auth.create_user_with_email_and_password(email, password)
        messagebox.showinfo("Success", "Account created! Please sign in.")
        show_frame(signin_frame)
    except:
        messagebox.showerror("Signup Failed", "Invalid or existing email.")

ctk.CTkButton(signup_card, text="Sign up", width=100, fg_color="#e5e7eb",
              hover_color="#d1d5db", text_color="black",
              font=("Arial", 12, "bold"), border_color="black", border_width=1,
              command=handle_signup).pack(pady=(15, 10))

ctk.CTkLabel(signup_card, text="OR", font=("Arial", 12, "bold"), text_color="black").pack(pady=(5, 5))

ctk.CTkButton(signup_card,
    text="  Sign up with Google",
    width=280,
    height=40,
    corner_radius=20,
    fg_color="white",
    hover_color="#f3f4f6",
    text_color="black",
    border_color="black",
    border_width=1,
    image=google_ctk_img,
    anchor="w",
    command=lambda: show_frame(google_signup_frame)
).pack(pady=(5, 10))

# -------- Google Sign Up Frame --------
google_signup_frame = ctk.CTkFrame(app)
google_card = ctk.CTkFrame(google_signup_frame, width=360, height=480, corner_radius=10,
                    fg_color="#f5f8fa", border_color="black", border_width=1)
google_card.pack(expand=True)
google_card.pack_propagate(False)

ctk.CTkLabel(google_card, text="VaultSafe - Google Sign Up", font=("Arial", 20, "bold")).pack(pady=(30, 10))

google_username = create_entry(google_card, "Username")
google_pw_var = ctk.StringVar()
google_password = create_password_entry(google_card, google_pw_var, placeholder="Password")
google_conf_var = ctk.StringVar()
google_confirm = create_password_entry(google_card, google_conf_var, placeholder="Confirm Password")

google_username.bind("<Return>", lambda e: google_password.focus())
google_password.bind("<Return>", lambda e: google_confirm.focus())
google_confirm.bind("<Return>", lambda e: show_frame(signin_frame))

ctk.CTkButton(google_card, text="Finish Sign up", width=100, fg_color="#e5e7eb",
              hover_color="#d1d5db", text_color="black",
              font=("Arial", 12, "bold"), border_color="black", border_width=1,
              command=lambda: show_frame(signin_frame)).pack(pady=(10, 10))

# Start at Sign In
show_frame(signin_frame)
app.mainloop()
