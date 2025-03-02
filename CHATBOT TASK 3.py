import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk

# Hugging Face API Endpoint
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer your-huggingface-api-key"}

# Function to get chatbot response
def get_response(user_input):
    payload = {"inputs": user_input}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            else:
                return "Error: Unexpected response format."
        except Exception as e:
            return f"Error: {str(e)}"
    elif response.status_code == 503:
        return "Error: Model is loading, please wait and try again."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to handle sending message
def send_message(event=None):
    user_input = user_entry.get()
    if user_input.strip():
        chat_display.insert(tk.END, "You: " + user_input + "\n", "user")
        chat_display.yview(tk.END)
        response = get_response(user_input)
        chat_display.insert(tk.END, "Bot: " + response + "\n", "bot")
        chat_display.yview(tk.END)
        user_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("500x600")
root.configure(bg="#50C878")  # Emerald background color

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, background="#1E8449", foreground="white")
style.configure("TEntry", font=("Arial", 12))

# Chat Display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=20, bg="#ECF0F1", font=("Arial", 12))
chat_display.pack(pady=10, padx=10)
chat_display.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
chat_display.tag_config("bot", foreground="green", font=("Arial", 12))

# Input Frame
input_frame = tk.Frame(root, bg="#50C878")
input_frame.pack(pady=5)

# User Input Field
user_entry = ttk.Entry(input_frame, width=40, font=("Arial", 12))
user_entry.grid(row=0, column=0, padx=5, pady=5)
user_entry.bind("<Return>", send_message)  # Bind Enter key to send_message

# Send Button with hover effect and light blue color
def on_enter(e):
    send_button.config(bg="#87CEFA", font=("Arial", 14, "bold"))

def on_leave(e):
    send_button.config(bg="#ADD8E6", font=("Arial", 12, "bold"))

send_button = tk.Button(root, text="Send ➤", command=send_message, font=("Arial", 12, "bold"), bg="#ADD8E6", fg="white", padx=10, pady=5)
send_button.pack(pady=30)
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# Run GUI
root.mainloop()
