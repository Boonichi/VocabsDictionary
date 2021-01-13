from tkinter import *
import os

def PrintText(self):
        with open(filename + '/Definitions/' + VocabsListBox.selection_get() + '.txt', 'r') as File:
        LibraryText.insert(END,File.read())
    LibraryText.pack(side = RIGHT, fill = BOTH, expand = True)
Root = Tk()                                                                                                                                                                                                         
Root.geometry('500x400')
Root.title('Test')
filename = os.getcwd()
ScrollVocabsListBox = Scrollbar(Root, orient = VERTICAL) 
VocabsListBox = Listbox(Root,height = 25, width = 15,selectmode = SINGLE, yscrollcommand=ScrollVocabsListBox.set,font = 3)
List = os.listdir(filename+'/Definitions')
for i in range(len(List)):
    if os.path.splitext(List[i])[1] == '.txt':
        VocabsListBox.insert(i,os.path.splitext(List[i])[0])
VocabsListBox.pack(side = LEFT,fill = BOTH)
LibraryText = Text(Root, height = 25,width = 40)
LibraryText.pack(side = RIGHT, fill = BOTH, expand = True)
VocabsListBox.bind('<Double-Button>',PrintText)
mainloop()