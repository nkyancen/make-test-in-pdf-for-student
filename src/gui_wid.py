#!/usr/bin/env python3

from tkinter import *
import tkinter.messagebox as tkbox
import workwithdb as ww


## Окно работы с дисциплинами
def win_dis(par_name):
    dis_win = Toplevel(par_name)
    dis_win.title("Дисциплины")
    dis_win.resizable(None, None)
    dis_win.focus_force()

    dis_label = Label(dis_win, text='Дисциплины:', font=ww.other_font)

    dis_add_label = Label(dis_win, text='Добавить\nдисциплину:', font=ww.other_font)

    dis_list = Listbox(dis_win, height=8, width=25, selectmode=SINGLE, font=ww.other_font)

    dis_tab = ww.out_from_database('discipline')

    for item in dis_tab:
        dis_list.insert(END, dis_tab[item])

    dis_list.selection_set(END)

    dis_list_scroll = Scrollbar(dis_win, command=dis_list.yview)
    dis_list.config(yscrollcommand=dis_list_scroll.set)

    dis_entry = Entry(dis_win, width=25, font=ww.other_font, justify="center")

    dis_add_but = Button(dis_win, text='Добавить\nдисциплину', font=ww.other_font,
                         command=lambda lb=dis_list, en=dis_entry, dw=dis_win:
                         dis_add(lb, en, dw))

    dis_del_but = Button(dis_win, text='Удалить\nдисциплину', font=ww.other_font,
                         command=lambda lb=dis_list, dw=dis_win:
                         dis_del(lb, dw))

    dis_quit_but = Button(dis_win, text='Закрыть', height=2, font=ww.other_font,
                          command=dis_win.destroy)

    dis_label.grid(row=1, column=1, columnspan=2, pady=(10, 5))
    dis_add_label.grid(row=1, column=3, pady=(10, 5))

    dis_list.grid(row=2, column=1, rowspan=3, padx=(10, 0), pady=(0, 10))
    dis_list_scroll.grid(row=2, column=2, rowspan=3, sticky='ns', padx=(0, 10), pady=(0, 10))

    dis_entry.grid(row=2, column=3, pady=10, padx=10)

    dis_add_but.grid(row=3, column=3, rowspan=2, pady=10, padx=10, sticky='s')
    dis_del_but.grid(row=5, column=1, columnspan=2, pady=(0, 15), padx=10)
    dis_quit_but.grid(row=5, column=3, pady=(0, 15), padx=10)


## Добавление дисциплины
def dis_add(lst, en, rwin):
    new_dis = en.get()

    if new_dis == '':
        tkbox.showwarning('Ошибка', 'Пустая строка', parent=rwin)

    elif ww.find(ww.out_from_database('discipline'), [new_dis]):
        tkbox.showwarning('Ошибка', 'Дисциплина "' + en.get() + '" уже есть', parent=rwin)

    else:
        ww.insert_to_database('discipline', (new_dis,))
        lst.insert(END, new_dis)
        tkbox.showinfo('Успешно', 'Дисциплина "' + en.get() + '" добавлена', parent=rwin)


## Удаление дисциплины
def dis_del(lst, rwin):
    tbl = ww.out_from_database('discipline')

    try:
        od_ind = lst.curselection()
        old_dis = lst.get(od_ind)

        if ww.find_couple(ww.out_from_database('razdel'), ww.kval(tbl, list(old_dis))):
            tkbox.showwarning('Ошибка', 'Дисциплина "' + old_dis[0] + '" содержит разделы',
                              parent=rwin)

        else:
            ww.delete_from_database('discipline', ('dis', ww.kval(tbl, [old_dis[0]])))
            lst.delete(od_ind)
            tkbox.showinfo('Успешно', 'Дисциплина "' + old_dis[0] + '" удалена', parent=rwin)
            lst.selection_set(END)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите дисциплину в списке', parent=rwin)


## Окно работы с разделами
def win_section(par_name):
    raz_win = Toplevel(par_name)
    raz_win.title("Разделы")
    raz_win.resizable(0, 0)
    raz_win.focus_force()

    raz_label = Label(raz_win, text='Разделы:', font=ww.other_font)

    raz_add_label = Label(raz_win, text='Добавить/удалить\nраздел:', font=ww.other_font)

    raz_quit_but = Button(raz_win, text='Закрыть', height=2, font=ww.other_font,
                          command=raz_win.destroy)

    raz_list = Listbox(raz_win, height=10, width=30, selectmode=SINGLE, font=ww.other_font)

    dis_tab = ww.out_from_database('discipline')
    raz_tab = ww.out_from_database('razdel')

    for item in raz_tab:
        raz_list.insert(END, [raz_tab[item][0], '-', dis_tab[raz_tab[item][1]]])

    raz_list.selection_set(END)

    raz_list_scroll = Scrollbar(raz_win, command=raz_list.yview)
    raz_list.config(yscrollcommand=raz_list_scroll.set)

    raz_entry = Entry(raz_win, width=25, font=ww.other_font, justify="center")

    raz_dis_list = Listbox(raz_win, height=5, width=25, selectmode=SINGLE, font=ww.other_font)

    for item in dis_tab:
        raz_dis_list.insert(END, dis_tab[item])

    ##    raz_dis_list.selection_set(END)

    raz_dis_list_scroll = Scrollbar(raz_win, command=raz_dis_list.yview)
    raz_dis_list.config(yscrollcommand=raz_dis_list_scroll.set)

    raz_add_but = Button(raz_win, text='Добавить\nраздел', font=ww.other_font,
                         command=lambda lb=raz_list, en=raz_entry, rdlb=raz_dis_list, dw=raz_win:
                         raz_add(lb, en, rdlb, dw))

    raz_del_but = Button(raz_win, text='Удалить\nраздел', font=ww.other_font,
                         command=lambda lb=raz_list, dw=raz_win: raz_del(lb, dw))

    raz_prob_but = Button(raz_win, text='Задания', width=10, height=2, font=ww.other_font,
                          command=lambda lb=raz_list, dw=raz_win: raz_prob(lb, dw))

    raz_label.grid(row=1, column=1, pady=(10, 5), columnspan=3)
    raz_add_label.grid(row=1, column=3, pady=(10, 5), columnspan=3)

    raz_quit_but.grid(row=5, column=4, columnspan=3, pady=(5, 15), padx=10)

    raz_list.grid(row=2, column=1, rowspan=3, columnspan=2, padx=(10, 0), pady=(0, 10))
    raz_list_scroll.grid(row=2, column=3, rowspan=3, sticky='ns', padx=(0, 10), pady=(0, 10))

    raz_entry.grid(row=2, column=4, columnspan=2, pady=(5, 5), padx=(10, 0))

    raz_add_but.grid(row=4, column=4, pady=(5, 5), padx=(5, 5))
    raz_del_but.grid(row=4, column=5, pady=(5, 5), padx=(10, 5))

    raz_dis_list.grid(row=3, column=4, rowspan=1, columnspan=2, sticky='ns', padx=(10, 0), pady=(0, 5))
    raz_dis_list_scroll.grid(row=3, column=6, rowspan=1, sticky='ns', padx=(0, 10), pady=(0, 5))

    raz_prob_but.grid(row=5, column=1, columnspan=3, pady=(5, 15), padx=(10, 10))


## Добавление раздела
def raz_add(lst, en, rdlst, rwin):
    dis_tab = ww.out_from_database('discipline')

    try:
        new_raz = [en.get(), ww.kval(dis_tab, list(rdlst.get(rdlst.curselection())))]

        if new_raz[0] == '':
            tkbox.showwarning('Ошибка', 'Пустая строка', parent=rwin)

        elif ww.find(ww.out_from_database('razdel'), new_raz):
            tkbox.showwarning('Ошибка', 'Раздел "' + new_raz[0] + '" уже есть в дисциплине "' \
                              + dis_tab[new_raz[1]][0] + '"', parent=rwin)

        else:
            ww.insert_to_database('razdel', tuple(new_raz), '?, ?')
            lst.insert(END, [new_raz[0], '-', ww.out_from_database('discipline')[new_raz[1]]])
            tkbox.showinfo('Успешно', 'Раздел "' + new_raz[0] + '" добавлен в дисциплину "' \
                           + dis_tab[new_raz[1]][0] + '"', parent=rwin)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выберите дисциплину в списке', parent=rwin)


## Удаление раздела
def raz_del(lst, rwin):
    tbl = ww.out_from_database('razdel')
    dis_tab = ww.out_from_database('discipline')
    # or_ind = lst.curselection()

    try:
        or_ind = lst.curselection()
        old_raz = lst.get(or_ind)

        if ww.find_couple(ww.out_from_database('problem'),
                          ww.kval(tbl, [old_raz[0], ww.kval(dis_tab, list(old_raz[2]))])):
            tkbox.showwarning('Ошибка', 'Раздел "' + old_raz[0] + '" содержит задачи',
                              parent=rwin)
        else:
            ww.delete_from_database('razdel', ('raz',
                                               ww.kval(tbl, [old_raz[0],
                                                             ww.kval(ww.out_from_database('discipline'), list(old_raz[2]))])))
            lst.delete(or_ind)
            tkbox.showinfo('Успешно', 'Раздел "' + old_raz[0] + '" удален из дисциплины "' + old_raz[2][0] + '"',
                           parent=rwin)
            lst.selection_set(END)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите раздел в списке', parent=rwin)


## Добавляем, изменяем или удаляем задания для выбранного раздела
def raz_prob(lst, pwin):
    try:
        raz = [lst.get(lst.curselection())[0],
               ww.kval(ww.out_from_database('discipline'), list(lst.get(lst.curselection())[2]))]
        raz_id = ww.kval(ww.out_from_database('razdel'), raz)

        prob = Toplevel(pwin)
        prob.title('Задания')
        prob.geometry('+%d+%d' % (50, 120))
        prob.resizable(0, 0)

        problem = ww.out_from_database('problem', ('prob_raz = ' + str(raz_id)))

        prob_label = Label(prob, text='Задания раздела "' + raz[0] + '" дисциплины "' + ww.out_from_database(
            'discipline')[raz[1]][
            0] + '"', font=ww.other_font)

        prob_list_width = ww.sw // 11
        prob_list = Listbox(prob, height=20, width=prob_list_width,
                            selectmode=SINGLE, font=ww.other_font)

        for item in problem:
            prob_list.insert(END, [ww.types_of_problems[problem[item][2]][1], '-', problem[item][0]])

        prob_list.selection_set(END)

        prob_list_scroll = Scrollbar(prob, command=prob_list.yview)
        prob_list.config(yscrollcommand=prob_list_scroll.set)

        prob_list_xscroll = Scrollbar(prob, command=prob_list.xview, orient="horizontal")
        prob_list.config(xscrollcommand=prob_list_xscroll.set)

        prob_quit_but = Button(prob, text='Закрыть', height=1, font=ww.other_font,
                               command=prob.destroy)

        prob_add_but = Button(prob, text='Добавить задание', font=ww.other_font,
                              command=lambda razid=raz_id, dw=prob, lb=prob_list:
                              raz_add_prob(razid, dw, lb))
        prob_del_but = Button(prob, text='Удалить задания', font=ww.other_font,
                              command=lambda lb=prob_list, razid=raz_id, dw=prob:
                              raz_del_prob(lb, razid, dw))
        prob_upd_but = Button(prob, text='Изменить задание', font=ww.other_font,
                              command=lambda:
                              raz_upd_prob(prob_list, raz_id, prob))

        prob_label.grid(row=1, column=1, columnspan=3, sticky='we', pady=(10, 5))

        prob_list.grid(row=2, column=1, columnspan=2, pady=(5, 0), padx=(10, 0))
        prob_list_scroll.grid(row=2, column=3, sticky='ns', padx=(0, 10), pady=(5, 0))
        prob_list_xscroll.grid(row=3, column=1, columnspan=2, sticky='ew', padx=(10, 0), pady=(0, 10))

        prob_quit_but.grid(row=4, column=2, columnspan=2, pady=(5, 15), padx=50, sticky='e')

        prob_add_but.grid(row=4, column=1, columnspan=3, sticky='w',
                          pady=(5, 15), padx=(240, 10))
        prob_del_but.grid(row=4, column=1, columnspan=3, sticky='e',
                          pady=(5, 15), padx=(10, 400))
        prob_upd_but.grid(row=4, column=1, columnspan=3,
                          pady=(5, 15))  ##, padx = (10,200))


    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите раздел в списке', parent=pwin)


## Добавляем задания в выбранный раздел
def raz_add_prob(rid, parent_window, lst):
    apr = Toplevel(parent_window)
    apr.title('Добавление задания')
    apr.resizable(None, None)

    pra_quit_but = Button(apr, text='Закрыть', height=2, font=ww.other_font,
                          command=apr.destroy)

    pra_add_label = Label(apr, text='Введите условие задания', font=ww.other_font)

    pra_frame = Frame(apr)

    pra_type_label = Label(pra_frame, text='Выберите тип\nзадания', font=ww.other_font)

    pra_text = Text(apr, height=15, width=ww.sw // 15, font=ww.other_font, wrap=WORD)
    pra_text_scroll = Scrollbar(apr, command=pra_text.yview)
    pra_text.config(yscrollcommand=pra_text_scroll.set)

    pra_type_list = Listbox(pra_frame, height=5, width=35,
                            selectmode=SINGLE, font=ww.other_font)

    for item in ww.types_of_problems:
        pra_type_list.insert(END, [ww.types_of_problems[item][0], '(', ww.types_of_problems[item][1], ')'])

    pra_type_list.selection_set(END)

    pra_type_list_scroll = Scrollbar(pra_frame, command=pra_type_list.yview)
    pra_type_list.config(yscrollcommand=pra_type_list_scroll.set)

    new_prob = (lst, rid, pra_text, pra_type_list, apr)

    pra_add_but = Button(apr, text='Добавить', height=2, width=15, font=ww.other_font,
                         command=lambda: add_prob(new_prob))

    pra_add_label.grid(row=1, column=1, columnspan=2, pady=(10, 10))

    pra_type_label.grid(row=1, column=1, columnspan=2)

    pra_quit_but.grid(row=2, column=3, pady=(10, 15), padx=10, sticky='s')
    pra_add_but.grid(row=2, column=3, pady=(10, 90), padx=10, sticky='s')

    pra_text.grid(row=2, column=1, columnspan=1, pady=(5, 15), padx=(10, 0))
    pra_text_scroll.grid(row=2, column=2, sticky='ns', padx=(0, 10), pady=(5, 15))

    pra_frame.grid(row=1, rowspan=2, column=3, pady=(10, 10), padx=(10, 10), sticky='n')

    pra_type_list.grid(row=2, column=1, columnspan=1)
    pra_type_list_scroll.grid(row=2, column=2, sticky='ns')


## Команда добавления задания в раздел
def add_prob(np):
    lst_tp = np[3]

    try:
        tp = lst_tp.get(lst_tp.curselection())[::2]
        new_prob = (np[2].get(1.0, END)[0:-1], np[1], ww.kval(ww.types_of_problems, list(tp)))

        rwin = np[4]
        praz = ww.out_from_database('razdel')[np[1]][0]
        ##        print(new_prob)
        ##        print(ww.find(ww.dbout('problem'), list(new_prob)))

        if new_prob[0] == '':
            tkbox.showwarning('Ошибка', 'Введите текст задания', parent=rwin)

        elif ww.find(ww.out_from_database('problem'), list(new_prob)):
            tkbox.showwarning('Ошибка', 'Такое задание уже есть в разделе "' + praz + '"', parent=rwin)

        else:
            np[0].insert(END, [tp[1], '-', new_prob[0]])
            ww.insert_to_database('problem', new_prob, '?,?,?')

            ans_type = ['КО']

            if tp[1] not in ans_type:
                ans = Toplevel(rwin)
                ans.title('Варианты ответов для задания')
                ans.resizable(0, 0)

                ans_label = Label(ans, text=
                'Введите варианты ответов\n(обязательны к заполнению первые 4 варианта)\n' +
                'Ответы для заданий на сопоставление разделять ";"',
                                  font=ww.other_font + ' bold')

                ans_var1_label = Label(ans, text='Вариант ответа №1 (верный)',
                                       font=ww.other_font + ' bold')
                ans_var2_label = Label(ans, text='Вариант ответа №2',
                                       font=ww.other_font + ' bold')
                ans_var3_label = Label(ans, text='Вариант ответа №3',
                                       font=ww.other_font + ' bold')
                ans_var4_label = Label(ans, text='Вариант ответа №4',
                                       font=ww.other_font + ' bold')
                ans_var5_label = Label(ans, text='Вариант ответа №5',
                                       font=ww.other_font)
                ans_var6_label = Label(ans, text='Вариант ответа №6',
                                       font=ww.other_font)

                ans_var1_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)
                ans_var2_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)
                ans_var3_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)
                ans_var4_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)
                ans_var5_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)
                ans_var6_entry = Entry(ans, width=35, font=ww.other_font, justify=CENTER)

                pp = (ans, praz, list(new_prob), ans_var1_entry, ans_var2_entry,
                      ans_var3_entry, ans_var4_entry,
                      ans_var5_entry, ans_var6_entry, rwin)

                ans_add_but = Button(ans, text='Добавить\nварианты ответов', font=ww.other_font,
                                     command=lambda: add_answer(pp))

                ans_label.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky='ew')

                ans_var1_label.grid(row=3, column=1, pady=10, padx=10, sticky='ew')
                ans_var2_label.grid(row=4, column=1, pady=10, padx=10, sticky='ew')
                ans_var3_label.grid(row=5, column=1, pady=10, padx=10, sticky='ew')
                ans_var4_label.grid(row=6, column=1, pady=10, padx=10, sticky='ew')
                ans_var5_label.grid(row=7, column=1, pady=10, padx=10, sticky='ew')
                ans_var6_label.grid(row=8, column=1, pady=10, padx=10, sticky='ew')

                ans_var1_entry.grid(row=3, column=2, pady=10, padx=10)
                ans_var2_entry.grid(row=4, column=2, pady=10, padx=10)
                ans_var3_entry.grid(row=5, column=2, pady=10, padx=10)
                ans_var4_entry.grid(row=6, column=2, pady=10, padx=10)
                ans_var5_entry.grid(row=7, column=2, pady=10, padx=10)
                ans_var6_entry.grid(row=8, column=2, pady=10, padx=10)

                ans_add_but.grid(row=9, column=1, columnspan=2, pady=10, padx=10)

            else:
                tkbox.showinfo('Успешно', 'Задание добавлено в раздел "' + praz + '"', parent=rwin)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выберите тип задания в списке', parent=rwin)


## Добавляем ответы к вопросам с вариантами
def add_answer(par_pr):
    ##    print(par_pr[2])
    new_ans = (ww.kval(ww.out_from_database('problem'), par_pr[2]), par_pr[3].get(), par_pr[4].get(), par_pr[5].get(),
               par_pr[6].get(), par_pr[7].get(), par_pr[8].get())
    ##    print(new_ans)
    ww.insert_to_database('answers', new_ans, '?,?,?,?,?,?,?')
    par_pr[0].destroy()
    tkbox.showinfo('Успешно', 'Задание и варианты ответов добавлены в раздел "' + par_pr[1] + '"',
                   parent=par_pr[9])


## Удаляем задание из выбранного раздела
def raz_del_prob(lst, rid, pwin):
    tbl_prob = ww.out_from_database('problem')
    tbl_ans = ww.out_from_database('answers')

    try:
        op_ind = lst.curselection()

        for item in ww.types_of_problems:
            if lst.get(op_ind)[0] in ww.types_of_problems[item]:
                old_prob = (lst.get(op_ind)[2], rid, item)

        pid = ww.kval(tbl_prob, list(old_prob))

        if ww.find_couple(ww.out_from_database('answers'), pid):
            for item in tbl_ans:
                if pid in tbl_ans[item]:
                    old_ans = tbl_ans[item]

            ww.delete_from_database('answers', ('ans', ww.kval(tbl_ans, old_ans)))

        ww.delete_from_database('problem', ('prob', pid))
        lst.delete(op_ind)

        tkbox.showinfo('Успешно', 'Задание удалено', parent=pwin)
        lst.selection_set(END)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите задание в списке', parent=pwin)


## Изменяем задание в выбранном разделе
def raz_upd_prob(lst, rid, pwin):
    tbl_prob = ww.out_from_database('problem')
    tbl_ans = ww.out_from_database('answers')

    try:
        op_ind = lst.curselection()

        for item in ww.types_of_problems:
            if lst.get(op_ind)[0] in ww.types_of_problems[item]:
                old_prob = (lst.get(op_ind)[2], rid, item)

        pid = ww.kval(tbl_prob, list(old_prob))

        ##        print(op_ind)
        ##        print(pid, old_prob, '\n')

        old_ans = []

        if ww.find_couple(ww.out_from_database('answers'), pid):
            for item in tbl_ans:
                if pid in tbl_ans[item]:
                    old_ans = tbl_ans[item]
                    aid = ww.kval(tbl_ans, list(old_ans))
        ##            print(aid, old_ans[1:], '\n')

        upr = Toplevel(pwin)
        upr.title('Изменение задания')
        upr.resizable(0, 0)

        pru_quit_but = Button(upr, text='Закрыть', height=2, font=ww.other_font,
                              command=upr.destroy)

        pru_upd_label = Label(upr, text='Условие задания', font=ww.other_font)

        pru_text = Text(upr, height=16, width=ww.sw // 20, font=ww.other_font,
                        wrap=WORD)
        pru_text_scroll = Scrollbar(upr, command=pru_text.yview)
        pru_text.config(yscrollcommand=pru_text_scroll.set)

        pru_text.insert(1.0, old_prob[0])

        pupd = (upr, pru_text, op_ind, lst, pid)

        pru_upd_but = Button(upr, text='Изменить задание', height=2, width=15,
                             font=ww.other_font,
                             command=lambda: upd_prob(pupd))

        ans = Frame(upr)

        ans_label = Label(ans,
                          text='Варианты ответов\n' +
                               '(обязательны к заполнению первые 4 варианта)\n' +
                               'Ответы для заданий на сопоставление разделять ";"',
                          font=ww.other_font)

        ans_var1_label = Label(ans, text='Вариант ответа №1 (верный)',
                               font=ww.other_font + ' bold')
        ans_var2_label = Label(ans, text='Вариант ответа №2',
                               font=ww.other_font + ' bold')
        ans_var3_label = Label(ans, text='Вариант ответа №3',
                               font=ww.other_font + ' bold')
        ans_var4_label = Label(ans, text='Вариант ответа №4',
                               font=ww.other_font + ' bold')
        ans_var5_label = Label(ans, text='Вариант ответа №5',
                               font=ww.other_font)
        ans_var6_label = Label(ans, text='Вариант ответа №6',
                               font=ww.other_font)

        ans_var1_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)
        ans_var2_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)
        ans_var3_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)
        ans_var4_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)
        ans_var5_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)
        ans_var6_entry = Entry(ans, width=25, font=ww.other_font, justify=CENTER)

        pru_upd_label.grid(row=1, column=1, columnspan=2, pady=(10, 10))

        pru_quit_but.grid(row=3, column=1, columnspan=2, pady=(10, 15), padx=20, sticky='w')
        pru_upd_but.grid(row=3, column=1, columnspan=2, pady=(10, 15), padx=20, sticky='e')

        pru_text.grid(row=2, column=1, columnspan=1, pady=(5, 10), padx=(10, 0))
        pru_text_scroll.grid(row=2, column=2, sticky='ns', padx=(0, 10), pady=(5, 10))

        if old_ans:
            ans_var1_entry.insert(1, old_ans[1])
            ans_var2_entry.insert(1, old_ans[2])
            ans_var3_entry.insert(1, old_ans[3])
            ans_var4_entry.insert(1, old_ans[4])
            ans_var5_entry.insert(1, old_ans[5])
            ans_var6_entry.insert(1, old_ans[6])

            aupd = (upr, aid, ans_var1_entry, ans_var2_entry,
                    ans_var3_entry, ans_var4_entry,
                    ans_var5_entry, ans_var6_entry)

            ans_upd_but = Button(ans, text='Изменить\nварианты ответов', height=2, width=15,
                                 font=ww.other_font,
                                 command=lambda: upd_ans(aupd))

            ans.grid(row=1, rowspan=3, column=3, sticky='ewns', padx=(0, 20))
            ans_upd_but.grid(row=9, column=1, columnspan=2,
                             pady=(19, 10), padx=10, sticky='s')

        ans_label.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky='ew')

        ans_var1_label.grid(row=2, column=1, pady=(0, 10), padx=10, sticky='ew')
        ans_var2_label.grid(row=3, column=1, pady=10, padx=10, sticky='ew')
        ans_var3_label.grid(row=4, column=1, pady=10, padx=10, sticky='ew')
        ans_var4_label.grid(row=5, column=1, pady=10, padx=10, sticky='ew')
        ans_var5_label.grid(row=6, column=1, pady=10, padx=10, sticky='ew')
        ans_var6_label.grid(row=7, column=1, pady=10, padx=10, sticky='ew')

        ans_var1_entry.grid(row=2, column=2, pady=10, padx=10)
        ans_var2_entry.grid(row=3, column=2, pady=10, padx=10)
        ans_var3_entry.grid(row=4, column=2, pady=10, padx=10)
        ans_var4_entry.grid(row=5, column=2, pady=10, padx=10)
        ans_var5_entry.grid(row=6, column=2, pady=10, padx=10)
        ans_var6_entry.grid(row=7, column=2, pady=10, padx=10)

    except TclError:
        tkbox.showwarning('Ошибка', 'Выделите задание в списке', parent=pwin)


## Изменяем задание
def upd_prob(up):
    tbl_prob = ww.out_from_database('problem')

    new_prob = up[1].get(1.0, END)[:-1]
    lst = up[3]

    if not ww.find_couple(tbl_prob, new_prob):
        ww.database_update('problem', ('prob_name', str(new_prob), 'prob', str(up[4])))
        lst.delete(up[2])
        lst.insert(up[2], [ww.type_of_problem[tbl_prob[up[4]][2]], '-', new_prob])

        tkbox.showinfo('Успешно', 'Задание изменено', parent=up[0])


## Изменяем варианты ответов
def upd_ans(ua):
    tbl_ans = ww.out_from_database('answers')

    ai = ua[1]

    temp = False

    n = 1

    for item in ua[2:8]:
        if item.get() not in tbl_ans[ai]:
            temp = True
            ww.database_update('answers', ('ans_' + ww.trans(n, 0), item.get(), 'ans', str(ai)))
        n += 1

    if temp:
        tkbox.showinfo('Успешно', 'Варианты ответов изменены', parent=ua[0])
