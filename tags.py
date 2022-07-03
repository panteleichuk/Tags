from tkinter import*
#ипорт функции для перемшивания списка цифр и цветов
from random import shuffle
# модуль время - для задержки окна
import time

#модуль для работы с ОС, что бы найти абсолютный путь к картинке для иконки приложения. 
import os
def path(name):
    return os.path.join( os.path.abspath(__file__+"/.."), name )

#создаем свой класс на базе Tk. Что бы установить свои настройки кона: заголовок, иконку, цвет фона
class My_window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Tags")
        self.iconbitmap(path("tag.ico"))
        self.resizable(False, False)
        self.config(bg = "yellow")
      
    #функция для отцентрирования окна по монитору
    def window_center(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w//2 # середина экрана
        h = h//2 
        w = w - 250 # смещение от середины
        h = h - 400
        self.geometry('500x650+{}+{}'.format(w, h))
# создаме свое окно      
window = My_window()
#создаем лейбл для оповещания о победе
lbl_win = Label(text="WIN!!!", font=("Comic Sans MS",24, "bold"), bg = "red")
#создаем и заполняем список  чисел для пятнашек от 1 до 15 включительно, число 16- будет пустая пятнашка
map_game = list(range(1, 17))
#список для цветов пятнашек- каждая клеточка своего цвета, последний цвет - для пустой клеточки
color = ["#b22222","#ff6347","#f0e68c","#66cdaa","#008000","#7b68ee","#000080","#9932cc","#ff69b4","#ee82ee","#5f9ea0","#f4a460","#daa520","#f08080","#FFC0CB","#2f4f4f"]
#список для кнопок-пятнашек
btn_list = list()
#список для фреймов- где будем размещать по 4 кнокпи-пятнашки
frame_list = list()

#функция обработчик нажатия на кнопку-пятнашку
def click_btn(n):
    #проверяем не нажата ли пустая кнопка
    if map_game[n]!=16:
        #находим индекс пустой пятнашик 
        m = map_game.index(16)
        # проверяем сосед ли пустая кнопка той что мы нажали
        # 1  2  3  4
        # 5  6  7  8
        # 9  10 11 12
        # 13 14 15 16 
        # разница между индексом нажатой кнопки и пустой должен быть равен=1(проверяем справа или слева) abs(n//4 - m//4)-проверяем в одной ли они строке
        # либо 4(для проверки клетки вверху или внизу)

        if (abs(n-m)==1+abs(n//4 - m//4)) or abs(n-m)==4:
            #меняем местами значение в списке цифр
            map_game[n], map_game[m] = map_game[m], map_game[n]
             #меняем местами значение в списке цветов
            color[n], color[m] = color[m], color[n]
             #меняем цвет, текст кнопок
            btn_list[n].config(text = "",bg = color[n])
            btn_list[m].config(text = map_game[m], bg = color[m])
            
            #проверка на выигрыш
            #  если отсортированые список-цифр равен самому себе не отсортированому 
            if sorted(map_game) == map_game:
            #тогда прячем кнопки и фреймы
                for btn in btn_list:
                    btn.pack_forget()
                for fr in frame_list:
                    fr.pack_forget()
                # и наоброт показываме надпись о выигрыше
                lbl_win.pack(expand=YES, fill=None)

#функция для создания, отриосвки кнопок-пятнашек
def draw_tag():
    #удаляем пока последнюю цифру 16 пустая пятнашка всегда должна быть в конце списка, то же касается и цвета
    map_game.remove(16)
    color.remove("#2f4f4f")
    # перемешиваем список цветов и цифр
    #shuffle(map_game)
    shuffle(color)
    #снова добавляем последнюю цифру и цвет дя пустой пятнашки
    map_game.append(16)
    color.append("#2f4f4f")
    # создаем фреймы и на них кнопки
    for i in range(4):
        #сначало создаем фрейм
        frame_list.append(Frame())
        # располагаем его на окне
        frame_list[i].pack(expand=YES, fill=BOTH)
        for j in range(4):
            # создаем кнопку , цвет и цифру для кнопки берем из список color и map_game
            btn_list.append(Button(frame_list[i],bg = color[i*4+j], font=('mono', 24, 'bold'), text = map_game[i*4+j], command=lambda n=i*4+j: click_btn(n), width=5, height=3 ))
           # размещаме кнопку на фрейме(по 4 на фрейм)
            btn_list[i*4+j].pack(side=LEFT,expand=YES,fill=BOTH)
            # если это последняя кнопка(16) пустая меняем текст на пустое значение
            if map_game[i*4+j]==16:
                btn_list[i*4+j].config(text="")
        
#функция обработчки нажатия на кнопку рестарт
def restart():
    
    # "прячем" лейбл о победе
    lbl_win.pack_forget()
    #удаляем фреймы
    for i in range(4):
        frame_list[i].destroy()
    #очищаем списки кнопок и фреймов
    frame_list.clear()
    btn_list.clear()
     # вызываем функцию отрисовки кнопок-пятнашек
    draw_tag()
#функция обработчик кнопки выхода из игры
def exitt():
    for btn in btn_list:
        btn.pack_forget()
    for fr in frame_list:
        fr.pack_forget()
    lbl_win.config( text = "GOOD BUY")
    lbl_win.pack(expand=YES, fill=None)
    #задержим окно что бі попрощаться
    window.update()
    window.after(1000, window.quit())

  
#функция отрисовки кнопок меню - рестарт и выход
def draw_menu():
    # создаме фрейм для кнопок
    fram_menu = Frame()
    fram_menu.pack(expand=NO, fill=BOTH)
    #создаем кнопку рестарт размещаем ее слева на фрейме
    btn_restart = Button(fram_menu,bg = "#FFFFE0", font=('mono', 14, 'bold'), text = "Restart game", command=restart, width=10, height=2 )
    btn_restart.pack(side=LEFT)
    #создаем кнопку выход размещаем ее справа
    btn_exit = Button(fram_menu,bg = "#FFFFE0", font=('mono', 14, 'bold'), text = "EXIT", command=exitt, width=10, height=2 )
    btn_exit.pack(side=RIGHT)

#вызываем функции отрисовки меню и кнопок-пятнашек
draw_menu()    
draw_tag()
#отцентруем окно
window.window_center()
window.mainloop()

