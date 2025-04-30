#create a memory card application
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, 
    QHBoxLayout, QVBoxLayout, 
    QGroupBox, QRadioButton, QButtonGroup,
    QPushButton, QLabel)
from random import shuffle, randint

# ---------------Class pertanyaan---------------------
class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

#------------List pertanyaan--------------------------
questions_list = [] 
questions_list.append(Question('The state language of Brazil', 'Portuguese', 'English', 'Spanish', 'Brazilian'))
questions_list.append(Question('Which color does not appear on the American flag?', 'Green', 'Red', 'White', 'Blue'))
questions_list.append(Question('A traditional residence of the Yakut people', 'Urasa', 'Yurt', 'Igloo', 'Hut'))

app = QApplication([])
window = QWidget()
window.setWindowTitle("Memory Card")

question = QLabel("Berikut yang tidak termasuk warna")
button_answer = QPushButton("Answer")

answergroup = QGroupBox('Answer Option:')
button1 = QRadioButton('Matcha')
button2 = QRadioButton('Vanilla')
button3 = QRadioButton('Lavender')
button4 = QRadioButton('Cocoa')

#TAMBAHKAN RADIO BUTTON GROUP
radiogroup = QButtonGroup()
radiogroup.addButton(button1)
radiogroup.addButton(button2)
radiogroup.addButton(button3)
radiogroup.addButton(button4)

#layout window
layout1 = QHBoxLayout()
layout2 = QVBoxLayout()
layout3 = QVBoxLayout()
layout2.addWidget(button1)
layout2.addWidget(button2)
layout3.addWidget(button3)
layout3.addWidget(button4)

layout1.addLayout(layout2)
layout1.addLayout(layout3)
answergroup.setLayout(layout1)

#Tambahkan (Answer GroupBox)
answergroupbox = QGroupBox('Test Result')
labelresult = QLabel("Are u correct or not?")
labelcorrect = QLabel("The answer will be here!")

layout_result = QVBoxLayout()
layout_result.addWidget(labelresult, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_result.addWidget(labelcorrect, alignment=Qt.AlignHCenter, stretch=2)
answergroupbox.setLayout(layout_result)

layout_line1 = QHBoxLayout()
layout_line2 = QHBoxLayout()
layout_line3 = QHBoxLayout()

layout_line1.addWidget(question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(answergroup)
layout_line2.addWidget(answergroupbox) #tambahkan layout anser group box
answergroupbox.hide()

layout_line3.addStretch(1)
layout_line3.addWidget(button_answer, stretch=2)
layout_line3.addStretch(1)

#Mengatur main layout
layout_main = QVBoxLayout()
layout_main.addLayout(layout_line1, stretch=2)
layout_main.addLayout(layout_line2, stretch=8)
layout_main.addStretch(1)
layout_main.addLayout(layout_line3, stretch=1)
layout_main.addStretch(1)
layout_main.setSpacing(5)

# -------- Function show question and answer ----------
def show_result():
    answergroup.hide()
    answergroupbox.show()
    button_answer.setText('Next Question')

def show_question():
    answergroup.show()
    answergroupbox.hide()
    button_answer.setText('Answer')
    radiogroup.setExclusive(False)
    button1.setChecked(False)
    button2.setChecked(False)
    button3.setChecked(False)
    button4.setChecked(False)
    radiogroup.setExclusive(True)

answers = [button1, button2, button3, button4]

def ask(q: Question):
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    question.setText(q.question)
    labelcorrect.setText(q.right_answer) 
    show_question()

def show_correct(res):
    ''' show result - put the written text into "result" and show the corresponding panel '''
    labelresult.setText(res)
    show_result()

def check():
    if answers[0].isChecked():
        show_correct('YEAH, Correct!')
        window.score += 1
        print('Statistics\n - Total question:', window.total, '\n -right answer:', window.score)
        print('Rating:', (window.score/window.total*100), '%')
    
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Incorrect!')
            print('Rating:', (window.score/window.total*100))

def next_question():
    window.total += 1
    print('Statistics\n-Total questions: ', window.total, '\n-Right answers: ', window.score)
    cur_question = randint(0, len(questions_list) - 1) 
    q = questions_list[cur_question] # picked a question
    ask(q) # asks

def click_ok():
    if button_answer.text() == 'Answer':
        check()
    else:
        next_question()


#tambahkan (button click)
button_answer.clicked.connect(click_ok)
window.score = 0
window.total = 0
next_question()
#tampilkan aplikasi
window.setLayout(layout_main)
window.resize(400,300)
window.show()
app.exec()