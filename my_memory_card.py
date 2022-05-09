from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel)
from random import shuffle, randint

#Данные о вопросе удобно «обернуть» в класс Question
class Question():
    ''' содержит вопрос, правильный ответ и три неправильных'''
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3, wrong4, wrong5):
        # все строки надо задать при создании объекта, они запоминаются в свойства
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3
        self.wrong4 = wrong4
        self.wrong5 = wrong5

# что делаем? 
questions_list = [] 
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский', 'Русккий', 'Немецкий'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий', 'Черный', 'Коричневй'))
questions_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата', 'Землянка', 'Квартира'))
 
app = QApplication([]) #приложение
 
btn_OK = QPushButton('Ответить') # кнопка ответа
lb_Question = QLabel() # текст вопроса
 
RadioGroupBox = QGroupBox("Варианты ответов") # группа на экране для переключателей с ответами
 
rbtn_1 = QRadioButton() #вариант1
rbtn_2 = QRadioButton() #вариант2
rbtn_3 = QRadioButton() #вариант3
rbtn_4 = QRadioButton() #вариант4
rbtn_5 = QRadioButton()
rbtn_6 = QRadioButton()
answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4, rbtn_5, rbtn_6]

# создаем группировку переключателей, чтобы управлять их поведением и добавляем в нее переключатели
RadioGroup = QButtonGroup() 
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)
RadioGroup.addButton(rbtn_5)
RadioGroup.addButton(rbtn_6)
 
layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout() 
layout_ans4 = QVBoxLayout()


layout_ans2.addWidget(rbtn_1) # два ответа в первый столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # два ответа во второй столбец
layout_ans3.addWidget(rbtn_4)
layout_ans4.addWidget(rbtn_5)
layout_ans4.addWidget(rbtn_6)



# размещаем вертикальные столбцы в одной строке
layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) 
layout_ans1.addLayout(layout_ans4) 


# размещаем layout_ans1 (строку со столбцами) на группе RadioGroupBox
RadioGroupBox.setLayout(layout_ans1)
 
# теперь создаем группу и виджеты для ответа 
AnsGroupBox = QGroupBox("Результат теста") # группа на экране для ответа
lb_Result = QLabel() # виджет надписи "правильно" или "неправильно"
lb_Correct = QLabel() # виджет текста правильного ответа
 
layout_res = QVBoxLayout() # направляющая для lb_Result и lb_Correct
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res) # панель с lb_Result и lb_Correct

#направляющие: 
layout_line1 = QHBoxLayout() # для вопроса
layout_line2 = QHBoxLayout() # для варианта ответов или результата теста
layout_line3 = QHBoxLayout() # для кнопки "Ответить"

# привязываем соответсвующие виджеты к направляющим:
layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)   
layout_line2.addWidget(AnsGroupBox)  
AnsGroupBox.hide() # скроем панель с ответом, сначала должна быть видна панель вопросов
 
layout_line3.addStretch(1) # растяжение направляющей с привязкой к левой границе
layout_line3.addWidget(btn_OK, stretch=2) # добавляем коэф. растяжения соттветствующего виджета
layout_line3.addStretch(1) # растяжение направляющей с привязкой к правой границе
 
#вертикальная направляющая и привязки к ней
layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # пробелы между содержимым

#главное окно    
window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memo Card')
# текущий вопрос из списка сделаем свойством объекта "окно", так мы сможем спокойно менять его из функции:
window.cur_question = -1    # по-хорошему такие переменные должны быть свойствами, 
                            # только надо писать класс, экземпляры которого получат такие свойства, 
                            # но python позволяет создать свойство у отдельно взятого экземпляра
window.total = 0
def show_result():
    ''' показать панель ответов '''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')
 
def show_question():
    ''' показать панель вопросов '''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    # сбросить выбранную радио-кнопку
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    rbtn_5.setChecked(False)
    rbtn_6.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана
 
 
def ask(q: Question):
    ''' функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом'''
    shuffle(answers) # перемешали список из кнопок, теперь на первом месте списка какая-то непредсказуемая кнопка
    answers[0].setText(q.right_answer) # первый элемент списка заполним правильным ответом, остальные - неверными
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    answers[4].setText(q.wrong4)
    answers[5].setText(q.wrong5)
    lb_Question.setText(q.question) # вопрос
    lb_Correct.setText(q.right_answer) # ответ 
    show_question() # показываем панель вопросов 
 
def show_correct(res):
    ''' показать результат - установим переданный текст в надпись "результат" и покажем нужную панель '''
    lb_Result.setText(res)
    show_result()
 
def check_answer():
    #проверяем, на каком ответе стоит флажок
    ''' если выбран какой-то вариант ответа, то надо проверить и показать панель ответов'''
    if answers[0].isChecked():
        # правильный ответ!
     
        show_correct('Правильно!')  
        window.score +=1
        print('Статистика \n Всего вопроса:', window.total, '\n-Правильных ответов:',window.core)
        print('Рейтинг:',(window.score/window.total*100),'%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked() or answers[4].isChecked() or answers[5].isChecked():
            # неправильный ответ!
            show_correct('Неверно!')
 
def next_question():
    window.total += 1
    print('Статистика\n Всего вопроса:', window.total, '\n-Правильных ответов:',window.score)
    cur_question = randint(0, len(questions_list) - 1)
    q = questions_list[cur_question]
    ask(q)
 
def click_OK():
    ''' определяет, надо ли показывать другой вопрос либо проверить ответ на этот '''
    if btn_OK.text() == 'Ответить':
        check_answer() # проверка ответа
    else:
        next_question() # следующий вопрос
 

 
btn_OK.clicked.connect(click_OK) # по нажатии на кнопку выбираем, что конкретно происходит
 
# все настроено, осталось задать вопрос и показать окно:
next_question()
window.resize(600, 500)
window.show()
app.exec()