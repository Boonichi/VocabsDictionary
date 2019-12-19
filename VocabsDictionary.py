from tkinter import *
from tkinter import filedialog
from bs4 import BeautifulSoup as BS
import os
import re
import requests
from lxml import html
### Master
Root = Tk()
Root.geometry("500x400")
Root.title("VocabsDictionary")
CambridgeLink = 'https://dictionary.cambridge.org'
OxFordLink = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
filename = os.getcwd()
###
### All Frame Location:
Top_Frame = Frame(Root)
Top_Frame.pack(side = TOP)
Mid_Frame = Frame(Root)
Mid_Frame.pack(side = TOP)
Bottom_Frame= Frame(Root)
Bottom_Frame.pack(side = BOTTOM)
###
def PrintText(self):
    LibraryText.delete('1.0', END)
    with open(filename + '/Definitions/' + VocabsListBox.selection_get() + '.txt', 'r') as File:
        LibraryText.insert(END,File.read())
    LibraryText.pack(side = RIGHT, fill = BOTH, expand = True)
def Search(*args):
    Pattern = Search_Content.get()
    List = os.listdir(filename+'/Definitions')
    VocabsListBox.delete(0,END)
    for i in range(len(List)):
        if os.path.splitext(List[i])[1] == '.txt' and re.match(Pattern,os.path.splitext(List[i])[0]):
            VocabsListBox.insert(i,os.path.splitext(List[i])[0])
    VocabsListBox.pack(side = LEFT,fill = BOTH)
def LibraryWindow():
    global LibraryWin
    global LibraryText
    global VocabsListBox
    try:
        if LibraryWin.state() == "normal": LibraryWin.focus()
    except:
        LibraryWin = Toplevel()
        LibraryWin.title('Library')
        LibraryWin.geometry("500x400")
        global Search_Content
        Search_Content = StringVar()
        Search_Engine = Entry(LibraryWin,width = 15, textvariable = Search_Content)
        Search_Engine.pack(side = TOP)
        ScrollVocabsListBox = Scrollbar(LibraryWin, orient = VERTICAL) 
        VocabsListBox = Listbox(LibraryWin,height = 25, width = 15,selectmode = SINGLE, yscrollcommand=ScrollVocabsListBox.set,font = 3)
        List = os.listdir(filename+'/Definitions')
        for i in range(len(List)):
            if os.path.splitext(List[i])[1] == '.txt':
                VocabsListBox.insert(i,os.path.splitext(List[i])[0])
        VocabsListBox.pack(side = LEFT,fill = BOTH)
        LibraryText = Text(LibraryWin, height = 25,width = 40)
        LibraryText.pack(side = RIGHT, fill = BOTH, expand = True)
        LibraryWin.bind('<Key>',Search)
        VocabsListBox.bind('<Double-Button>',PrintText)
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(' +', ' ',re.sub(clean, ' ', text))
def FormatPassage(Vocab,Index,Definitions,Examples):
    print(Definitions,Examples)
    File = open(filename +'/Definitions/' + Vocab+'.txt','a')
    Definitions = str(Index) + '. ' + Definitions[1:].capitalize() + ':'
    File.writelines(Definitions+'\n')
    Result = ' ' + Examples[1]
    for index in range(2,len(Examples)):
        if Examples[index] == '.' or Examples[index] == '?' or Examples[index] == ':':
            Result+= Examples[index]
            File.writelines('    ' +'.'+ Result+'\n')
            Result = ''
        else:
            Result+= Examples[index]
    File.close()
def WriteFile(Pattern,text):
    File = open(Pattern,'wb')
    File.write(text)
    File.close()
def LinkAudio(Pattern):
    result = ''
    Turn = False
    for index in Pattern[0]:
        if index == '/': Turn = True
        if Turn == True:
            result += index
            if index == '3': 
                return result
def Change_Folder():
    global filename
    filename = filedialog.askdirectory()
def DownloadAudio(Vocab):
    Page = requests.get(CambridgeLink + '/dictionary/english/' + Vocab)
    soup = BS(Page.content, 'lxml')
    htmlContent = soup.prettify("utf-8")
    UKPattern = r'.source src=..media.english.uk.pron.*type=.audio'
    USPattern = r'.source src=..media.english.us.pron.*type=.audio'
    UKSearchContent = re.findall(UKPattern,htmlContent.decode('utf_8'))
    USSearchContent = re.findall(USPattern,htmlContent.decode('utf_8'))
    if not os.path.exists(filename+'/VocabsAudio'):
        os.mkdir(filename+'/VocabsAudio')
    UKAudio = requests.get(CambridgeLink + LinkAudio(UKSearchContent))
    WriteFile(filename+'/VocabsAudio'+'/'+Vocab +'_UK' + '.mp3',UKAudio.content)
    USAudio = requests.get(CambridgeLink + LinkAudio(USSearchContent))
    WriteFile(filename+ '/VocabsAudio' +'/'+ Vocab + '_US' + '.mp3',UKAudio.content)
def DefinitionVocab(Vocab):
    Page = requests.get(OxFordLink + Vocab)
    soup = BS(Page.content, 'lxml')
    if not os.path.exists(filename+'/Definitions'):
        os.mkdir(filename+'/Definitions')
    File = open(filename +'/Definitions/' + Vocab+'.txt','w')
    File.close()
    SoupContent = soup.find( attrs = {'class':'sn-gs'})
    print(SoupContent)
    SoupContent = SoupContent.findAll( attrs = {'class':'sn-g'})
    print(SoupContent)
    for Index in range(len(SoupContent)):
        VocabsDefinition = SoupContent[Index].find('span', attrs= {'class':'def'})
        VocabsExamples = SoupContent[Index].find('span', attrs={'class':'x-gs'})
        FormatPassage(Vocab,Index,remove_html_tags(str(VocabsDefinition)),remove_html_tags(str(VocabsExamples)))
def Vocabs_Handle():
    inputValue=VocabsInput.get("1.0",END)
    for Vocab in inputValue.splitlines():
        DownloadAudio(Vocab)
        DefinitionVocab(Vocab)
### Text Box
Label(Top_Frame, text ="Type Your Vocabs:", bg = "White").grid(sticky = W,row = 0, column = 0, padx = 50)
LibraryButton = Button(Top_Frame, text="Library", fg="Black", bg="White", command = LibraryWindow).grid(sticky = E,row = 0, column = 1,padx = 50)
VocabsInput =Text(Mid_Frame, width = 50, height = 20)
VocabsInput.pack(fill = BOTH, expand = TRUE)
###
### Button Settings:
QuitButton = Button(Bottom_Frame, text = "QUIT", fg = "Black", bg = "White", command = quit).grid(row = 0, column = 0,sticky = W)
Change_FolderButton = Button(Bottom_Frame, text = "Change Folder", fg = "Black", bg = "White", command = Change_Folder).grid(row = 0,column = 1, sticky = E)
AddButton=Button(Bottom_Frame, fg = "Black", bg = "White" ,text="ADD", command=Vocabs_Handle).grid(row = 0, column = 2,sticky = E)
###
### END
mainloop()