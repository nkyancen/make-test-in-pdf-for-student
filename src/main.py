#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog as fd
import gui_wid as gw
import workwithdb as ww
import maketest as mt

main = Tk()
main.title('Создание тестовых заданий')

ww.sw = main.winfo_screenwidth()
ww.sh = main.winfo_screenheight()

main.geometry('+%d+%d' % (ww.screen_weight / 2 - 175, 100))
main.resizable(False, False)

ww.path_to_base = fd.askopenfilename(filetypes=[('DataBase', '.db'), ('all files', '*')])

if not ww.path_to_base:
    exit()

ww.types_of_problems = ww.out_from_database('typeproblem')
for item in ww.types_of_problems:
    ww.type_of_problem[item] = (ww.types_of_problems[item][1])

main_name_of_database = Label(main, text='База подключена\n' + ww.path_to_base, font=ww.other_font)

main_dis = Button(main, text='Дисциплины', width=15, height=2, font=ww.main_font,
                  command=lambda: gw.win_dis(main))
main_section = Button(main, text='Разделы\nи задания', width=15, height=2, font=ww.main_font,
                      command=lambda: gw.win_section(main))
## main_prob = Button(main, text = 'Задания', width=10,height=2, font = ww.main_font)
main_test = Button(main, text='Тесты', width=20, height=2, font=ww.main_font,
                   command=lambda: mt.dis_choise(main))

main_name_of_database.grid(row=1, column=1, columnspan=2, pady=20, padx=(10, 10), sticky='ew')
main_dis.grid(row=2, column=1, pady=20, padx=5, sticky='w')
main_section.grid(row=2, column=2, padx=5, sticky='e')
##main_prob.grid(row = 2, column = 3, padx = 10)
main_test.grid(row=4, column=1, columnspan=2, padx=(10, 10), pady=10, sticky='ew')

main.mainloop()
