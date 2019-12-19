from tkinter import *
def Search(event):
    print(Search_Content.get()) 
Root = Tk()
global Search_Content
Search_Content = StringVar()
Search_Engine = Entry(Root, width = 15, textvariable = Search_Content)
Search_Engine.pack()
Search_Engine.bind('<ENTER>',Search)
mainloop()