import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import filedialog
# from Student_database import submit, Show
from sqlite3 import * 
from tkinter import ttk


class Student:
    
    def __init__(self, window):    
        self.window = window
        self.window.title("PALLPUBB")
        self.window.geometry("1920x1050")
        self.window.minsize(1920, 1050)
        self.window.configure(bg="#324370")
        
        def clear_text(event):
            search_bar.delete(0, tk.END)

        def open_image():
            filepath = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")))
            photo_entry.delete(0, tk.END)
            photo_entry.insert(tk.END, filepath)

        def open_text_file():
            filepath = filedialog.askopenfilename(initialdir="/", title="Select Text File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            article_entry.delete(0, tk.END)
            article_entry.insert(tk.END, filepath)

        def back():
            self.window.destroy()
        
        def clear():
            for entry in entry_list:
                entry.delete(0, tk.END)
        
        # def search():
        #     name = search_bar.get()


        # Create the title bar and set the bg color of the title bar
        title_bar = tk.Frame(self.window, bg="#769ADD", height=200)
        title_bar.pack(fill=tk.X)

        # Create the title label in the title bar of PULLPUBB
        title_font = font.Font(family="Helvetica bold", size=60, weight="bold")
        title_label = tk.Label(title_bar, text="STUDENT", fg="white", bg="#769ADD", font=title_font)
        title_label.pack(pady=10)

        # Create back button to go back to the main PULLPUBB dashboard
        button_font = font.Font(family="Helvetica bold", size=12, weight="bold")
        back_button = tk.Button(self.window, text="BACK", bg="#255ABC", fg="white", width=10, font=button_font, command=back)
        back_button.place(x=20, y=140) 


        # Create a frame for the input fields and labels
        input_frame = tk.Frame(self.window, bg="#324370")
        # input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True, side=tk.LEFT)
        input_frame.place(x=150, y=200)

        # Create input fields and labels on the left side
        labels = [
            "Student Name:", "Address:", "Contact:", "Student School Name:", "Photo (Student):",
            "Article:"
        ]
        entry_list = []

        for i, label_text in enumerate(labels):
            label = tk.Label(input_frame, text=label_text, bg="#324370", fg="white", font=("Helvetica bold", 20, "bold"))
            label.grid(row=i, column=0, sticky="w", pady=5, padx=5)

            if label_text == "Photo (Student):":
                photo_entry = tk.Button(input_frame, bg="white", font=("Helvetica", 16), width=10, command=lambda event: open_image())
                photo_entry.grid(row=i, column=1, pady=5, padx=5, sticky="we")
                # entry_list.append(photo_entry)

            elif label_text == "Article:":
                article_entry = tk.Button(input_frame, bg="white", font=("Helvetica", 16), width=10, command= lambda event : open_text_file())
                article_entry.grid(row=i, column=1, pady=5, padx=5, sticky="we")
                # entry_list.append(article_entry)
            else:
                entry = tk.Entry(input_frame, bg="white", font=("Helvetica", 20), width=10)
                entry.grid(row=i, column=1, pady=5, padx=5, sticky="we")
                entry_list.append(entry)

        # Create the sidebar
        # Create the sidebar on the right side
        sidebar = tk.Frame(self.window, bg="#698ED4", width=300, height=800)
        sidebar.pack(fill=tk.Y, side=tk.RIGHT)
        
        # Create a submit button
        submit_button = tk.Button(input_frame, text="SUBMIT", fg="white", bg="#698ED4", font=("Helvetica bold", 20, "bold"), command=lambda: submit(entry_list[:]))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)
        submit_button.configure(activebackground="#769ADD", activeforeground="white")

        # search button
        search_text = tk.StringVar()
        search_text.set("Search Text")
        search_bar = tk.Entry(sidebar, bg="white", font=("Helvetica bold", 20, "bold"), width=20, textvariable=search_text)
        search_bar.grid(row=0, column=0, padx=10, pady=(50, 30))
        search_bar.bind("<Button-1>", clear_text)
        
        search_button = tk.Button(sidebar, bg="white", text="SEARCH", font=("Helvetica bold", 20, "bold"), command=lambda: data(search_bar.get()))
        search_button.grid(row=0, column=1, padx=10, pady=(50, 30))

        # create a delete button
        delete_button = tk.Button(sidebar, bg="white", text="DELETE", font=("Helvetica bold", 20, "bold"), width=20)
        delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=30)

        # create a delete button
        edit_button = tk.Button(sidebar, bg="white", text="EDIT", font=("Helvetica bold", 20, "bold"), width=20)
        edit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=30)

        # create a delete button
        clear_button = tk.Button(sidebar, bg="white", text="CLEAR ALL", font=("Helvetica bold", 20, "bold"), width=20, command=clear)
        clear_button.grid(row=3, column=0, columnspan=2, padx=10, pady=30)

        # Create back button to go back to the main PULLPUBB dashboard
        button_font = font.Font(family="Helvetica bold", size=12, weight="bold")

        back_button = tk.Button(self.window, text="BACK", bg="#255ABC", fg="white", width=10, font=button_font, command=back)
        back_button.place(x=20, y=140) 
        back_button.configure(activebackground="#255ABC", activeforeground="white")
        data()


# database  
def submit(entries):
    conn = connect('database.db')
    con_cursor = conn.cursor()
    query_table = 'CREATE TABLE IF NOT EXISTS STUDENT (S_ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, ADDRESS TEXT NOT NULL, CONTACT INTEGER NOT NULL, STUDENT_SCHOOL_NAME TEXT NOT NULL)'
    con_cursor.execute(query_table)
    query_entries = 'INSERT INTO STUDENT (NAME, ADDRESS, CONTACT, STUDENT_SCHOOL_NAME) VALUES(?, ?, ?, ?)'
    values = [entry.get() for entry in entries]
    con_cursor.execute(query_entries, values)
    conn.commit()
    con_cursor.close()
    conn.close()
    data()

def data(search=""):
    # create a tableview 
    table = ttk.Treeview(window, columns=("SR_NO", "NAME", "ADDRESS", "CONTACT", "STUDENT_SCHOOL_NAME"), show="headings")

    # create headings 
    table.heading("SR_NO", text="SR_NO")
    table.heading("NAME", text="NAME")
    table.heading("ADDRESS", text="ADDRESS")
    table.heading("CONTACT", text="CONTACT")
    table.heading("STUDENT_SCHOOL_NAME", text="STUDENT_SCHOOL_NAME")

    table.place(y=780, x=300)

    # create dataentries 
    conn = connect('database.db')
    con_cursor = conn.cursor()
    query_table = 'CREATE TABLE IF NOT EXISTS STUDENT (S_ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, ADDRESS TEXT NOT NULL, CONTACT INTEGER NOT NULL, STUDENT_SCHOOL_NAME TEXT NOT NULL)'
    con_cursor.execute(query_table)
    query_show = 'SELECT * FROM STUDENT'
    if search==""or search==None:
        result = con_cursor.execute(query_show)
    else:
        query_s = query_show + ' WHERE NAME=?'
        result = con_cursor.execute(query_s, (search))
    i=0
    for entry in result:
        table.insert(parent='', index=i, values=entry)
        i+=1


if __name__ == "__main__":
    window = tk.Tk()
    app = Student(window)
    window.mainloop()
    




        # def data():
        #     # create a tableview 
        #     table = ttk.Treeview(window, columns= ("SR_NO", "NAME", "ADDRESS", "CONTACT", "STUDENT_SCHOOL_NAME"), show="headings")

        #     # create headings 
        #     table.heading("SR_NO", text="SR_NO")
        #     table.heading("NAME", text="NAME")
        #     table.heading("ADDRESS", text="ADDRESS")
        #     table.heading("CONTACT", text="CONTACT")
        #     table.heading("STUDENT_SCHOOL_NAME", text="STUDENT_SCHOOL_NAME")

        #     table.place(y=780, x=300)

        #     # create dataentries 
        #     conn = connect('database.db')
        #     con_cursor = conn.cursor()
        #     query_show = 'SELECT * FROM STUDENT'
        #     result = con_cursor.execute(query_show)
        #     for entry in result:
        #         table.insert(parent='', index=0, values=entry)

        # def search():
        #     # Get the name from the search bar
        #     name = search_bar.get()

        #     # Connect to the database
        #     conn = connect('database.db')
        #     con_cursor = conn.cursor()

        #     # Query the database for the student with the given name
        #     con_cursor.execute("SELECT * FROM STUDENT WHERE NAME=?", (name))

        #     # Fetch the results
        #     results = con_cursor.fetchall()

        #     # Close the cursor and the connection
        #     con_cursor.close()
        #     conn.close()

        #     # If no results were found, show an error message
        #     if not results:
        #         messagebox.showerror("Error", "No such contact found")
        #     else:
        #         # Otherwise, populate the entry fields with the results
        #         for i, entry in enumerate(self.entry_list):
        #             entry.delete(0, tk.END)
        #             entry.insert(tk.END, results[0][i])

