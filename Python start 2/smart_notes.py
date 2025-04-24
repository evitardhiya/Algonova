#start to create smart notes app
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QListWidget, QLineEdit, QTextEdit, QInputDialog,
    QHBoxLayout, QVBoxLayout, QFormLayout )
import json

app = QApplication([])

#---------------Notes JSON-------------------------------------------
# notes = {
#     "Welcome!" : {
#         "text" : "This is the best note taking app in the world!",
#         "tags" : ["good", "instructions"]
#     }
# }
# with open("notes_data.json", "w") as file:
#     json.dump(notes, file, ensure_ascii=False)

#--------------Application Interface---------------------------------
noteswindow = QWidget()
noteswindow.setWindowTitle('Smart Notes')
noteswindow.resize(900,600)

#app window widget
listnotes = QListWidget()
Listnoteslabel = QLabel('List of Notes')
buttonnote_create = QPushButton('Create Note')
buttonnote_del = QPushButton('Delete Note')
buttonnote_save = QPushButton('Save Note')
fieldtag = QLineEdit('')
fieldtag.setPlaceholderText('Enter tag ...')
fieldtext= QTextEdit()
button_add = QPushButton("Add to Note")
button_del = QPushButton('Untag From Note')
button_search = QPushButton('Search Notes by Tag')
listtags = QListWidget()
listtagslabel = QLabel()

#Layout widget
layoutnotes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(fieldtext)

col2 = QVBoxLayout()
col2.addWidget(Listnoteslabel)
col2.addWidget(listnotes)

row1 = QHBoxLayout()
row1.addWidget(buttonnote_create)
row1.addWidget(buttonnote_del)

row2 = QHBoxLayout()
row2.addWidget(buttonnote_save)

col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(listtagslabel)
col2.addWidget(listtags)
col2.addWidget(fieldtag)

row3 = QHBoxLayout()
row3.addWidget(button_add)
row3.addWidget(button_del)

row4 = QHBoxLayout()
row4.addWidget(button_search)

col2.addLayout(row3)
col2.addLayout(row4)

layoutnotes.addLayout(col1, stretch = 2)
layoutnotes.addLayout(col2, stretch = 1)
noteswindow.setLayout(layoutnotes)

#---------------Application function-------------------------------------------
#menambahkan notes
def add_note():
    note_name, ok = QInputDialog.getText(noteswindow, 'Add Note', 'Note nama: ')
    if ok and note_name != '':
        notes[note_name] = {'text': '', 'tags': []}
        listnotes.addItem(note_name)
        listtags.addItems(notes[note_name]['tags'])
        print(notes)

#menampilkan notes
def show_note():
    key = listnotes.selectedItems()[0].text()
    print(key)
    fieldtext.setText(notes[key]["text"])
    listtags.clear()
    listtags.addItems(notes[key]["tags"])

#menyimpan notes
def save_notes():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        notes[key]['text'] = fieldtext.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Note to save is not selected!')

#menghapus notes
def del_notes():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        del notes[key]
        listnotes.clear()
        listtags.clear()
        fieldtext.clear()
        listnotes.addItems(notes)
        with open('notes_data.json', 'w') as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Note to delete is not selected!')

#menambahkan tags
def add_tag():
    if listnotes.selectedItems():
        key = listnotes.selectedItems()[0].text()
        tag = fieldtag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            listtags.addItem(tag)
            fieldtag.clear()
        with open('notes_data.json', 'w') as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Note to add a tag is not selected!')

#menambahkan tags
def del_tag():
    if listtags.selectedItems():
        key = listnotes.selectedItems()[0].text()
        tag = listtags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        listtags.clear()
        listtags.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w') as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Tgas to delete is not selected!')

#mencari tags
def search_tag():
    print(button_search.text())
    tag = fieldtag.text()
    if button_search.text() == 'Search notes by tag' and tag :
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filtered[note] = notes[note]
        button_search.setText('Reset search')
        listnotes.clear()
        listtags.clear()
        listnotes.addItems(notes_filtered)
        print(button_search.text())
    elif button_search.text() == 'Reset search':
        fieldtag.clear()
        listnotes.clear()
        listtags.clear()
        listnotes.addItems(notes)
        button_search.setText('Search note by tag')
        print(button_search.text())
    else:
        pass


#---------------Run  Application-------------------------------------------
#event handling
buttonnote_create.clicked.connect(add_note)
listnotes.itemClicked.connect(show_note)
buttonnote_save.clicked.connect(save_notes)
buttonnote_del.clicked.connect(del_notes)
button_add.clicked.connect(add_tag)
button_del.clicked.connect(del_tag)
button_search.clicked.connect(search_tag)

#show main app
noteswindow.show()

#open json
with open("notes_data.json", "r") as file:
    notes = json.load(file)
listnotes.addItems(notes)

app.exec_()
