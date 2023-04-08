#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate():
    try:
        N = int(N_entry.get())
        t_end = float(t_end_entry.get())*86400
        L = float(L_entry.get())
        lamda = float(lamda_entry.get())
        ro = float(ro_entry.get())
        c = float(c_entry.get())
        T0 = float(T0_entry.get())
        Tl = float(Tl_entry.get())
        Tr = float(Tr_entry.get())
        
        T = (N+1)*[0]
        alfa =(N+1)*[0]
        beta =(N+1)*[0]
        
        #{определяем расчетный шаг сетки по пространственной координате} 
        h = L/(N-1)
        #{определяем расчетный шаг сетки по времени}
        tau = t_end/100 
        #{определяем поле температуры в начальный момент времени}
        for i in range(1,N+1):
            T[i] = T0
        #{проводим интегрирование нестационарного уравнения теплопроводности}
        time = 0
        while time < t_end: #{используем цикл с предусловием}
            time = time+tau
            #{определяем начальные прогоночные коэффициенты на основе левого граничного условия}
            alfa[1] = 0.0
            beta[1] = Tl
            #{цикл с параметром для определения прогоночных коэффициентов}
            for i in range(2,N):
                #{ai, bi, ci, fi – коэффициенты канонического представления СЛАУ с трехдиагональной матрицей}
                ai = lamda/(h**2)
                bi = 2.0*lamda/(h**2)+ro*c/tau
                ci = lamda/(h**2)
                fi = -ro*c*T[i]/tau
                #{alfa[i], beta[i] – прогоночные коэффициенты}
                alfa[i] = ai/(bi-ci*alfa[i-1])
                beta[i] = (ci*beta[i-1]-fi)/(bi-ci*alfa[i-1])
            #{определяем значение температуры на правой границе}
            T[N] = Tr
            #{используя соотношение (7) определяем неизвестное поле температуры}
            for i in range(N-1, 0, -1):
                T[i] = alfa[i]*T[i+1]+beta[i]
        x=N*[0]
        temp=N*[0]
        time=N*[0]
        days=int(t_end/86400)
        for i in range(0,N):
            x[i]=x[i-1]+h
            temp[i]=T[i+1]
        dayt=""
        if days==1:
            dayt=" день"

        if days in {2,3,4}:
            dayt=" дня"
        else:
            dayt=" дней"

        # Создаем новое окно для графика
        plot_window = tk.Toplevel(root)
        plot_window.title("Изменение температуры")

        # Создаем график matplotlib
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(x, temp)
        ax.set_xlabel("Глубина")
        ax.set_ylabel("Температура")
        ax.set_title("Изменение температуры за "+str(days)+dayt)

        # Вставляем рисунок matplotlib в окно tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения")


# Создание главного окна
root = tk.Tk()
root.title("График изменения температуры")

# Создание полей для ввода параметров
N_label = tk.Label(root, text="Количество пространственных узлов, N:")
N_label.grid(column=0, row=0)
N_entry = tk.Entry(root)
N_entry.grid(column=1, row=0)

t_end_label = tk.Label(root, text="Срок в днях, t_end:")
t_end_label.grid(column=0, row=1)
t_end_entry = tk.Entry(root)
t_end_entry.grid(column=1, row=1)

L_label = tk.Label(root, text="Толщина пласта, L:")
L_label.grid(column=0, row=2)
L_entry = tk.Entry(root)
L_entry.grid(column=1, row=2)

lamda_label = tk.Label(root, text="Коэффициент теплопроводности, lamda:")
lamda_label.grid(column=0, row=3)
lamda_entry = tk.Entry(root)
lamda_entry.grid(column=1, row=3)

ro_label = tk.Label(root, text="Плотность грунта, ro:")
ro_label.grid(column=0, row=4)
ro_entry = tk.Entry(root)
ro_entry.grid(column=1, row=4)

c_label = tk.Label(root, text="Теплоемкость , c:")
c_label.grid(column=0, row=5)
c_entry = tk.Entry(root)
c_entry.grid(column=1, row=5)

T0_label = tk.Label(root, text="Начальная температура , T0:")
T0_label.grid(column=0, row=6)
T0_entry = tk.Entry(root)
T0_entry.grid(column=1, row=6)

Tl_label = tk.Label(root, text="Температура сверху, Tl:")
Tl_label.grid(column=0, row=7)
Tl_entry = tk.Entry(root)
Tl_entry.grid(column=1, row=7)

Tr_label = tk.Label(root, text="Температура снизу, Tr:")
Tr_label.grid(column=0, row=8)
Tr_entry = tk.Entry(root)
Tr_entry.grid(column=1, row=8)

# Создание кнопки для вычислений и постройки графика
calc_button = tk.Button(root, text="Построить график", command=calculate)
calc_button.grid(column=0, row=9, columnspan=2)
root.mainloop()


# In[ ]:





# In[ ]:




