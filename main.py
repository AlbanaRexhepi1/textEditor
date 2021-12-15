from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk


window = tk.Tk()
window.title("Simple Text Editor")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open")
btn_save = tk.Button(fr_buttons, text="Save As...")
btn_fonts = tk.Button(fr_buttons, text="Fonts..")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
btn_fonts.grid(row=2, column=0, sticky="ew", padx=5)


#Open file function
def open_file():
    """Open a file for editing."""
    my_text.delete("1.0", END)
    
    text_file = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    
    if text_file:
        global open_status_name 
        open_status_name = text_file
    
    #Update status bar
    name = text_file
    status_bar.config(text=name)
    name = name.replace("C:/Users/alban","")
    root.title(f'{name}')

    #open the file
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()

#Save As File
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}')
        name = name.replace("C:/Users/alban","")
        root.title(f'{name}')

        #save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

#Save File
def save_file():
    global open_status_name
    if open_status_name:
        #save the file
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

        status_bar.config(text=f'Saved: {open_status_name}')
    else:
        save_as_file()

#Cut Text
def cut_text(e):
    global selected
    #check to see if keyboard shortcut used
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        #Grab selected text from textbox
        selected = my_text.selection_get()
        #Delete selected text
        my_text.delete("sel.first", "sel.last")
        #Clear the clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)

#Copy Text
def copy_text(e):
    global selected
    #check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        #Grab selected text from textbox
        selected = my_text.selection_get()
        #Clear the clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)

#Paste Text
def paste_text(e):
    global selected
    #check to see if keyboard shortcut used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)
#Bold Text
def bold_it():
    #Crate our font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    my_text.tag_configure("bold", font=bold_font)

    current_tags = my_text.tag_names("sel.first")
    #If statement to see if tag has been set
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


def italics_it():
    #Crate our font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")
    my_text.tag_configure("italic", font=italics_font)

    current_tags = my_text.tag_names("sel.first")
    #If statement to see if tag has been set
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

#Change selected Text Color
def text_color():
    #Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        #Crate our font
        color_font = font.Font(my_text, my_text.cget("font"))

        my_text.tag_configure("colored", font=color_font, foreground=my_color)

        current_tags = my_text.tag_names("sel.first")
        #If statement to see if tag has been set
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last")

#Change bg color
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

#Change all text color
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

#Font size function
def font_size_chooser(e):
    our_font.config(
        size=font_size_listbox.get(font_size_listbox.curselection()))

#Font Style function
def font_style_chooser(e):
    style = font_style_listbox.get(font_style_listbox.curselection()).lower()

    if style == "bold":
        our_font.config(weight=style)
    if style == "regular":
        our_font.config(weight="normal", slant="roman", underline=0, overstrike=0)
    if style == "italic":
        our_font.config(slant=style)
    if style == "bold/italic":
        our_font.config(weight="bold", slant="italic")
    if style == "underline":
        our_font.config(underline=1)
    if style == "strike":
        our_font.config(overstrike=1)

#Choosing the font 
def font_chooser(e):
    our_font.config(
        family=my_listbox.get(my_listbox.curselection()))


our_font = font.Font(family="Helvetica", size = "16")

#Create a toolbar Frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

#Crate main frame
my_frame = Frame(root, width=510, height=275)
my_frame.pack(pady=10)

my_frame.grid_propagate(False)
my_frame.columnconfigure(0, weight = 10)

#Scrollbar 
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#Horizontal Scrollbar
hor_scroll = Scrollbar(my_frame, orient = 'horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

#Create Text Box
my_text = Text(my_frame, width=510, height=275, font=our_font, selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, xscrollcommand=hor_scroll.set, wrap="none")
# my_text.grid(row=0, column=0)
# my_text.grid_rowconfigure(0,weight=1)
# my_text.grid_columnconfigure(0,weight=1)
my_text.pack()

text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

#Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")

#Add Color Menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Selected Text", command=text_color)
color_menu.add_command(label="All Text", command=all_text_color)
color_menu.add_command(label="Background", command=bg_color)

#Bottom Frame
bottom_frame = Frame(root)
bottom_frame.pack()

#Add labels
font_label = Label(bottom_frame, text="Choose Font", font=("Helvetica", 14))
font_label.grid(row=0, column=0, padx=10, sticky=W)

size_label= Label(bottom_frame, text="Font Size", font=("Helvetica", 14))
size_label.grid(row=0, column=1, sticky=W)

style_label = Label(bottom_frame, text="Font Style", font=("Helvetica", 14))
style_label.grid(row=0, column=2, padx=10, sticky=W)

#font families
my_listbox = Listbox(bottom_frame, selectmode=SINGLE, width=40)
my_listbox.grid(row=10, column=0, pady= 10)

font_size_listbox= Listbox(bottom_frame, selectmode=SINGLE, width=20)
font_size_listbox.grid(row=1, column= 1)

font_style_listbox = Listbox(bottom_frame, selectmode=SINGLE, width=20)
font_style_listbox.grid(row=1, column=2, padx= 10)

#Add font families to Listbox
for f in font.families():
    my_listbox.insert('end', f)

#Add Sizes to Size Listbox
font_sizes = [8, 10, 12, 14, 16, 18, 20, 36, 48]
for size in font_sizes:
    font_size_listbox.insert('end', size)

#Add Styles to Style Listbox
font_styles = ["Regular", "Bold", "Italic", "Bold/Italic", "Underline", "Strike"]
for style in font_styles:
    font_style_listbox.insert('end', style)


status_bar = Label(root, text="Ready         ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

#Edit Binding
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

#create buttons

#Bold button
bold_button = Button(toolbar_frame, text= "Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)
#Italics button
italics_button = Button(toolbar_frame, text= "Italics", command=italics_it)
italics_button.grid(row=0, column=1, padx=5)
#Undo/Redo buttons
undo_button = Button(toolbar_frame, text= "Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)
redo_button = Button(toolbar_frame, text= "Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

#Text color
color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5)

my_listbox.bind('<ButtonRelease-1>', font_chooser)
font_size_listbox.bind('<ButtonRelease-1>', font_size_chooser)
font_style_listbox.bind('<ButtonRelease-1>', font_style_chooser)
root.mainloop()

# TODO: Flexible font style 