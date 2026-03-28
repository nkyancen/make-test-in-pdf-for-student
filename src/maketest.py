#!/usr/bin/env python3

from tkinter import *
import tkinter.messagebox as tkbox
import workwithdb as ww
import random as rnd
import os


def dis_choise(pwin):
    dc_win = Toplevel(pwin)
    dc_win.title('Выбор диcциплины')
    dc_win.resizable(False, False)

    dc_label = Label(dc_win, text='Диcциплины:', font=ww.other_font)

    dc_list = Listbox(dc_win, height=8, width=25, selectmode=SINGLE, font=ww.other_font)

    dc_tab = ww.out_from_database('discipline')

    for item in dc_tab:
        dc_list.insert(END, dc_tab[item])

    dc_list.selection_set(END)

    dc_list_scroll = Scrollbar(dc_win, command=dc_list.yview)
    dc_list.config(yscrollcommand=dc_list_scroll.set)

    rt = (pwin, dc_win, dc_list)

    dc_but = Button(dc_win, text='Выбратьть\nдиcциплину', font=ww.other_font,
                    command=lambda: raz_test_form(rt))

    dc_label.grid(row=1, column=1, columnspan=2, pady=(10, 5))

    dc_list.grid(row=2, column=1, padx=(10, 0), pady=(5, 10))
    dc_list_scroll.grid(row=2, column=2, sticky='ns', padx=(0, 10), pady=(5, 10))

    dc_but.grid(row=3, column=1, columnspan=2, pady=(5, 15), padx=10)


def raz_test_form(par_rt):
    lst = par_rt[2]
    dis_tbl = ww.out_from_database('discipline')

    try:
        dis_ch = [ww.kval(dis_tbl, lst.get(lst.curselection())), lst.get(lst.curselection())[0]]

        par_rt[1].destroy()

        tform = Toplevel(par_rt[0])
        tform.title('Создание тестовых заданий')
        tform.resizable(0, 0)

        tf_raz_label = Label(tform, text='Выберите\nодин или несколько\nразделов', font=ww.other_font)

        tf_raz_list = Listbox(tform, height=10, width=25, selectmode=MULTIPLE, font=ww.other_font)

        raz_tab = ww.out_from_database('razdel', ('raz_dis = ' + str(dis_ch[0])))

        for item in raz_tab:
            tf_raz_list.insert(END, raz_tab[item][0])

        tf_raz_list_scroll = Scrollbar(tform, command=tf_raz_list.yview)
        tf_raz_list.config(yscrollcommand=tf_raz_list_scroll.set)

        tf_var_label = Label(tform, text='Количество вариантов', font=ww.other_font, width=25)

        num_vars = IntVar()

        tf_spbox = Spinbox(tform, from_=1, to=50, textvariable=num_vars,
                           justify='center', width=4, font=ww.other_font)

        tf_frame = Frame(tform)

        tf_num_label = Label(tf_frame,
                             text='Количество заданий\nкаждого типа:',
                             font=ww.other_font, width=25)

        tf_label_ko = Label(tf_frame,
                            text='С кратким ответом:',
                            font=ww.other_font, width=25)

        num_ko = IntVar()

        tf_scale_ko = Scale(tf_frame, variable=num_ko, from_=0, to=20, resolution=1,
                            orient='horizontal', tickinterval=2)

        tf_label_vo = Label(tf_frame,
                            text='С вариантами ответа:',
                            font=ww.other_font, width=25)

        num_vo = IntVar()

        tf_scale_vo = Scale(tf_frame, variable=num_vo, from_=0, to=20, resolution=1,
                            orient='horizontal', tickinterval=2)

        tf_label_sp = Label(tf_frame,
                            text='На сопоставление:',
                            font=ww.other_font, width=25)

        num_sp = IntVar()

        tf_scale_sp = Scale(tf_frame, variable=num_sp, from_=0, to=3, resolution=1,
                            orient='horizontal', tickinterval=1)

        tf_rt = (tform, tf_raz_list, num_vars, num_ko, num_vo, num_sp, dis_ch)

        n = 0

        for item in raz_tab:
            n += len(ww.out_from_database('problem', ('prob_raz = ' + str(item))))

        ##    print(n)
        tf_all = (tform, tf_raz_list, 0, n, n, n, dis_ch)

        tf_raz_but = Button(tform, text='Сформировать\nтест', font=ww.other_font,
                            command=lambda: raz_choice(tf_rt))
        tf_quit_but = Button(tform, text='Закрыть', font=ww.other_font, height=2,
                             command=tform.destroy)
        tf_araz_but = Button(tform, text='Все\nзадания', font=ww.other_font,
                             command=lambda: raz_choice(tf_all))

        tf_raz_label.grid(row=1, column=1, columnspan=2, pady=(10, 5))

        tf_raz_list.grid(row=2, column=1, padx=(10, 0), pady=(5, 5), sticky='ns')
        tf_raz_list_scroll.grid(row=2, column=2, sticky='ns', padx=(0, 10), pady=(5, 5))

        tf_raz_but.grid(row=3, column=3, columnspan=1, padx=10, pady=(5, 10), sticky='')
        tf_quit_but.grid(row=3, column=1, columnspan=2, padx=10, pady=(5, 10), sticky='w')
        tf_araz_but.grid(row=3, column=1, columnspan=2, padx=10, pady=(5, 10), sticky='e')

        tf_var_label.grid(row=1, column=3, padx=10, pady=(10, 0), sticky='n')
        tf_spbox.grid(row=1, column=3, padx=10, pady=(0, 10), sticky='s')

        tf_frame.grid(row=2, column=3, rowspan=1, padx=0, pady=(10, 15), sticky='ns')
        tf_num_label.grid(row=1, column=1, padx=10, sticky='ew')

        tf_label_ko.grid(row=2, column=1, pady=(10, 0), padx=10, sticky='ew')
        tf_scale_ko.grid(row=3, column=1, padx=10, sticky='ew')

        tf_label_vo.grid(row=4, column=1, pady=(10, 0), padx=10, sticky='ew')
        tf_scale_vo.grid(row=5, column=1, padx=10, sticky='ew')

        tf_label_sp.grid(row=6, column=1, pady=(10, 0), padx=10, sticky='ew')
        tf_scale_sp.grid(row=7, column=1, padx=10, sticky='ew')

    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите дисциплину в списке', parent=par_rt[1])


def raz_choice(prt):
    lst = prt[1]
    raz_tbl = ww.out_from_database('razdel')
    raz_ind = lst.curselection()

    ##    dis_ch = prt[6]
    try:
        nvar = prt[2].get() - 1
    except:
        nvar = prt[2]

    num_type = {}

    temp = []
    for item in ww.type_of_problem.values():
        if item == 'КО':
            try:
                num_type[item] = prt[3].get()
                temp.append(0 == prt[3].get())
            except:
                num_type[item] = prt[3]
                temp.append(0 == prt[3])
        elif item == 'ВО':
            try:
                num_type[item] = prt[4].get()
                temp.append(0 == prt[4].get())
            except:
                num_type[item] = prt[4]
                temp.append(0 == prt[4])
        else:
            try:
                num_type[item] = prt[5].get()
                temp.append(0 == prt[5].get())
            except:
                num_type[item] = prt[5]
                temp.append(0 == prt[5])

    if False not in temp:
        tkbox.showwarning('Ошибка', 'Без заданий не получится', parent=prt[0])

    elif not raz_ind:
        raz_ch = []
        tkbox.showwarning('Ошибка', 'Выберите хотя бы один раздел в списке', parent=prt[0])

    else:
        raz_ch = []
        prob_ch = {}
        tmp_rid = ''

        for item in raz_ind:
            tmp_rid = ww.kval(raz_tbl, [lst.get(item), prt[6][0]])
            raz_ch.append(tmp_rid)

            tmp_dic = {}
            for tp in ww.type_of_problem:
                temp = []
                for elem in ww.out_from_database('problem',
                                                 ('prob_raz = ' + str(tmp_rid) + ' AND prob_type = ' + str(tp))):
                    temp.append((elem))
                tmp_dic[ww.type_of_problem[tp]] = temp
            prob_ch[raz_ch[-1]] = tmp_dic

        ##        print(raz_ch,prob_ch, raz_tbl[raz_ch[0]][0])

        datav = r'\newcommand{\discipline}{' + prt[6][1]

        if len(raz_ind) == 1:
            datav += r' -- \it ' + raz_tbl[raz_ch[0]][0]

        datav += '}\n\n'
        tdata = '\n'
        prob_tbl = ww.out_from_database('problem')
        ans_tbl = ww.out_from_database('answers')

        for nv in range(nvar + 1):
            datav += '\n' + r'%% Вариант №' + str(nv + 1) + '\n\n'

            tempv = []
            for rz in prob_ch:
                for tp in prob_ch[rz]:
                    # n = 0
                    if num_type[tp] > 0:
                        if len(prob_ch[rz][tp]) > num_type[tp]:
                            n = num_type[tp]
                        else:
                            n = len(prob_ch[rz][tp])
                        tempv.extend(rnd.sample(prob_ch[rz][tp], n))

            ##            print('before:', tempv, '\n')
            tempv = rnd.sample(tempv, len(tempv))
            ##            print('after:', tempv, '\n\n')

            var = r'\Var' + ww.trans(nv + 1, 1)
            if nvar != 0:
                tdata += r'\var' + '\n\n'

            tdata += r'\begin{enumerate}' + '\n\n'

            for np, pri in enumerate(tempv):
                pr_temp = prob_tbl[pri]
                prob = var + 'Prob' + ww.trans(np + 1, 1)
                datav += r'\newcommand{' + prob + '}{' + pr_temp[0] + '}\n\n'

                if ww.type_of_problem[pr_temp[2]] == 'КО':
                    datav += '\n'
                    tdata += '\t' + r'\qc{' + prob + r' \vspace{0.4\textheight}' + '}\n\n'

                elif ww.type_of_problem[pr_temp[2]] == 'ВО':
                    temp_ans = []
                    temp = []
                    tdata += '\t' + r'\begin{minipage}[h]{1\linewidth}' + '\n'
                    tdata += '\t\t' + r'\begin{q}{' + prob + '}\n\n'
                    for ta in ans_tbl:
                        if pri in ans_tbl[ta]:
                            na = ta
                            for va in ans_tbl[ta][1:]:
                                if va:
                                    temp.append(va)
                    if nvar == 0:
                        temp_ans = rnd.sample(temp, len(temp))
                    else:
                        temp_ans = rnd.sample(temp, 4)

                    if ans_tbl[na][1] not in temp_ans:
                        temp_ans = temp_ans[:-1]
                        temp_ans.append('правильного ответа нет')
                        temp_ans = rnd.sample(temp_ans, len(temp_ans))

                    for ai, item in enumerate(temp_ans):
                        ans = prob + 'Ans' + ww.trans(ai + 1, 0)
                        if ai + 1 == len(temp_ans):
                            datav += r'\newcommand{' + ans + '}{' + item + '.}\n\n'
                        else:
                            datav += r'\newcommand{' + ans + '}{' + item + ';}\n\n'
                        tdata += '\t\t\t' + r'\item ' + ans + '\n\n'
                    datav += '\n'
                    tdata += '\t\t' + r'\end{q}' + '\n\t' + r'\end{minipage}' + '\n\n'

                else:
                    temp_ans = []
                    temp_sop = []

                    tdata += '\t' + r'\begin{minipage}[h]{1\linewidth}' + '\n'
                    tdata += '\t\t' + r'\begin{q}{' + prob + '}\n\t\t\t' + \
                             r'\begin{minipage}{0.49\linewidth}'
                    for ta in ans_tbl:
                        if pri in ans_tbl[ta]:
                            for va in ans_tbl[ta][1:]:
                                if va:
                                    if va.split(';')[0]:
                                        temp_ans.append(va.split(';')[0])

                                    if va.split(';')[1]:
                                        temp_sop.append(va.split(';')[1])

                    for ai, item in enumerate(rnd.sample(temp_ans, 4)):
                        ans = prob + 'Ans' + ww.trans(ai + 1, 0)
                        if ai + 1 == 4:
                            datav += r'\newcommand{' + ans + '}{' + item + '.}\n\n'
                        else:
                            datav += r'\newcommand{' + ans + '}{' + item + ';}\n\n'
                        tdata += '\n\t\t\t\t' + r'\item ' + ans

                    tdata += '\n\t\t\t' + r'\end{minipage}' + '\n\t\t' + r'\hfill' + \
                             '\n\t\t\t' + r'\begin{minipage}{0.49\linewidth}' + \
                             '\n\t\t\t\t' + r'\begin{qm}'

                    for si, item in enumerate(rnd.sample(temp_sop, len(temp_sop))):
                        sop = prob + 'Sop' + ww.trans(si + 1, 0)
                        if si + 1 == len(temp_sop):
                            datav += r'\newcommand{' + sop + '}{' + item + '.}\n\n'
                        else:
                            datav += r'\newcommand{' + sop + '}{' + item + ';}\n\n'
                        tdata += '\n\t\t\t\t\t' + r'\item ' + sop

                    datav += '\n'
                    tdata += '\n\t\t\t\t' + r'\end{qm}' + \
                             '\n\t\t\t' + r'\end{minipage}' + \
                             '\n\t\t' + r'\end{q}' + '\n\t' + r'\end{minipage}' + '\n\n'

            tdata += r'\end{enumerate}' + '\n\n' + r'\cleardoublepage' + '\n\n\n'

            with open('tex_files/data/datavop.tex', 'w', encoding='utf8') as dvfile:
                print(datav, file=dvfile)

            with open('tex_files/data/testdata.tex', 'w', encoding='utf8') as tdfile:
                print(tdata, file=tdfile)

        ##        print(datav)
        ##        print(tdata)

        os.system('pdflatex -synctex=1 -interaction=nonstopmode tex_files/mktest.tex')

        os.system('xdg-open mktest.pdf')
