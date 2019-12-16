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
Bottom_Frame= Frame(Root)
Bottom_Frame.pack(side = BOTTOM)
###
def TextOccur(VocabsListBox):
    Clicked_item = VocabsListBox.curselection()
    print(Clicked_item)
def LibraryWindow():
    global LibraryWin
    try:
        if LibraryWin.state() == "normal": LibraryWin.focus()
    except:
        LibraryWin = Toplevel()
        LibraryWin.title('Library')
        LibraryWin.geometry("500x400")
        ###VocabsListBox = Listbox(Left_Frame,height = 400, width = 200,selectmode = SINGLE)
        '''for i in range(len(os.listdir(filename+'/Definitions'))):
            if os.path.splitext(os.listdir(filename+'/Definitions')[i])[1] == '.mp3':
                VocabsListBox.insert(i,os.path.splitext(os.listdir(filename+'Definitions')[i])[0])'''
        ###VocabsListBox.pack()
        ###VocabsListBox.bind('<Double-Button>',TextOccur(VocabsListBox))
        VocabsInput =Text(LibraryWin, width = 2, height = 2 ).pack()
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(' +', ' ',re.sub(clean, ' ', text))
def FormatPassage(Vocab,Index,Definitions,Examples):
    File = open(filename +'/Definitions/' + Vocab+'.txt','a')
    Definitions = str(Index) + '. ' + Definitions[1:].capitalize() + ':'
    File.writelines(Definitions+'\n')
    String = Examples[1]
    for index in range(2,len(Examples)):
        if Examples[index].isupper() == True:
            Result = String
            File.writelines('    ' + Result+'\n')
            String = Examples[index]
        else:
            String+= Examples[index]
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
    VocabsDefinition = soup.findAll('span', attrs= {'class':'def'})
    VocabsExamples = soup.findAll('span', attrs={'x-gs'})
    File = open(filename +'/Definitions/' + Vocab+'.txt','w')
    File.close()
    for Index in range(len(VocabsDefinition)):
        FormatPassage(Vocab,Index,remove_html_tags(str(VocabsDefinition[Index])),remove_html_tags(str(VocabsExamples[Index])))
def Vocabs_Handle():
    inputValue=VocabsInput.get("1.0",END)
    for Vocab in inputValue.splitlines():
        DownloadAudio(Vocab)
        DefinitionVocab(Vocab)
### Text Box
Label(Top_Frame, text ="Type Your Vocabs:", bg = "White").pack()
LibraryButton = Button(Top_Frame, text="Library", fg="Black", bg="White", command = LibraryWindow)
LibraryButton.pack()
VocabsInput =Text(Top_Frame, width = 50, height = 20)
VocabsInput.pack()
###
### Button Settings:
QuitButton = Button(Bottom_Frame, text = "QUIT", fg = "Black", bg = "White", command = quit).grid(row = 0, column = 0,sticky = W)
Change_FolderButton = Button(Bottom_Frame, text = "Change Folder", fg = "Black", bg = "White", command = Change_Folder).grid(row = 0,column = 1, sticky = E)
AddButton=Button(Bottom_Frame, fg = "Black", bg = "White" ,text="ADD", command=Vocabs_Handle).grid(row = 0, column = 2,sticky = E)
###
### END
mainloop()