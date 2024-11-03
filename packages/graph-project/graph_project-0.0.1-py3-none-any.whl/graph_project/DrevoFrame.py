from random import randint
import networkx as nx
# import openpyxl module
import openpyxl
import matplotlib.pyplot as plt
from networkx import DiGraph


class Drevo:
    def init(self):
        pass

    """дый класс является всей библиотекой, в ней предаставлен весь код и все функции,
     которые используются в даннной библиотеке

     краткое описание функций:

     cvet_uzlov - вспомогательная функция, нужна для понимания какому ребру какая связь пренадлежит
     otdelno_uzl - вспомогательная функция, выдает массив связей элементов (ребра)
     conus - выводит массив строк, которые образуют конус
     konecha - сравнивает цвет ребер общего построения с цветом ребер конуса
     grupp_cveta_konus - основная функция, которая строит конус, так же сохраняет его изображение
     postroenie - создает массив ребер и их цветов
     uroven - выводит уровень фрейма, в виде строки
     p_sme - вспомогательная функция, создает сет вершин
     tabl_smegmm - вспомогательная функция, выводит таблицу смежности
     postroenie_grafa- основнаяя функция, строит граф и сохраняет его изображение
     agent - вспомогательная функция, строит отдельную ветку дерева и сохраняет её изображение
     agent_frame - основная функция, строит отдельную ветку дерева и сохраняет её изображение
     layer - вспомогательная функция, выводит уровень фрейма, сохраняет его изображение
     layer_frame - основная функция, выводит уровень фрейма, сохраняет его изображение
     postroenie_Exel - вспомомгательная функция, переводит таблицу смежности в Exel таблицу и сохраняет её
     postroenie_grafa_frame - основная функция, которая строит граф, сохраняет его таблицу смежности, сохраняет изображение графа
     conus_frame - основная функция, которая строит конус, сохраняет таблицу смежности, а так же сохроняем изображение
     ctenie - вспомогательная функция, которая нужна для удаления первых трех символов в каждой строке, для граматной работы программы
    """

    def cvet_uzlov(self, mas):  # получает на вход масив выдает два списка один с узлами второй с их цветом
        isxodn_uzl = []
        cvet_uzlov = []
        for i in range(len(mas)):
            x = mas[i]
            x = x.split()
            for j in range(len(x) - 1):
                isxodn_uzl.append(x[j] + ' ' + x[j + 1])
                cvet_uzlov.append(i + 1)
        return isxodn_uzl, cvet_uzlov

    """Данная функция выполняет задачу разделения масивов на элементы связи,
    а так же запоминает цвет связи данных узлов, на вход подается масив всех связей типа: ['a b c f g h'] """

    def otdelno_uzl(self, mas):  # нужно, что бы вывести какой с каким элементом связан
        con_mass = []
        for i in range(len(mas)):
            x = mas[i].split()

            for j in range(len(x) - 1):
                con_mass.append(x[j] + ' ' + x[j + 1])
        return list(set(con_mass))

    """Данная функция просто разделяет масивы на связи имеет точно такой же принцип работы как и функция выше, но не запоминает связи 
        принимает масив строк типа:[''a b c f g]"""

    def conus(self, mas, iskom):  # конус для вывод
        massiv_conusov = []
        flag = False
        for j in mas:
            if j.count(iskom) != 0:
                massiv_conusov.append(j[j.index(iskom):])
        return massiv_conusov

    """
    Даная функция нужна для нахождения всего конуса в дереве, она выводит ветки связей в дереве из которых состоит конус(['a b c', 'a j k'])
    на вход по значение mas должнен подаваться весь масив строк типа:['a b c d']
    в переменную iskom должен подаваться символ, относительно которого будет строится конус, если элемента iskom нет во входном массиве, то будет выведен пустой список
    """

    def konecha(self, mas_isxod_uzl, cvet_uzlov, conus_mas):  # сравнивает значения с исходным цветом узлов с конусом
        conus_cvet = []
        for i in conus_mas:
            conus_cvet.append(cvet_uzlov[mas_isxod_uzl.index(i)])
        return conus_cvet

    '''
    Данная функция нужна, что бы программа при построение конусов в дереве, понимала, какие узлы должны быть соеденены одним цветом, а какие разными
    на вход подается:
    mas_isxod_uzl- это все имеющиеся связи (ребра) в данном дереве формата(['a b','b c'])
    cvet_uzlov- это массив содержащий числовые обозначения [1, 2], каждое число это цвет ребра, и каждое число относится к определенному ребру, которое стоит в масиве на таком же месте как и число
    conus_mas- это  масиив в котором храняться связи (его ребра) конуса по типу: ['a b', 'c d']
    на выходе подается массив чисел которые обозначают цвет ребер между узлами из conus_mas связи :[1,2]
    '''

    def grupp_cveta_konus(self, mas, isxod):  # для построения конуса

        '''

        :param mas: массив строк формата ['a b c v']
        :param isxod: название вершины относительно которой строить сам конус
        :return: конус в виде дерева
        '''

        s = []
        v, n = self.cvet_uzlov(mas)  # запрашивает связи в дереве и цвета ребер
        s.append(
            self.konecha(v, n, self.otdelno_uzl(self.conus(mas, isxod))))  # добавляет в массив s цвета ребер в конусе

        s.append(self.otdelno_uzl(self.conus(mas, isxod)))  # добавляет в массив s  ребера в конусе

        '''
        Если узлом конуса является крайний элемент дерева не имеющий потомков или элемент которого нет в самом дереве, то функция выведит просто один узел, который
        подавался пользователем в функцию.
        Так же функция выведет текст 'конус образован одним элементом, или не имеет отношения к дереву'
        '''
        if s[1] == []:
            # создания пустого дерева
            G = nx.Graph()
            nx.draw_planar(G, with_labels=True)

            # Добавление узла который вводит пользователь
            G.add_node(isxod)
            nx.draw_planar(G, with_labels=True)

            # пока дерева
            plt.show()
            return "конус образован одним элементом, или не имеет отношения к дереву"

        """"создает массив цветов
        которые используются в построение"""
        # создание пустого массива цветов
        mas_cvetov = []
        # запускаем цикл, который генерирует цвета в виде 16тиричного кода, цветов генерируется в 10 раз больше, для того, что бы гарантированно у каждого каждого ребра мог быть свой цвет
        for i in range(len(s[1]) * 10):
            mas_cvetov.append('#%06X' % randint(0, 0xFFFFFF))  # Генерация 16тиричных кодов и их запись в масив цветов
        mas_cvetov = list(set(mas_cvetov))  # удаление всех повторящихся элементов

        mas_sviz = s[1]
        mas_uzl_cvet = s[0]
        mass = self.p_sme(mas_sviz)  # создаем сет элементов всего конуса
        # Создаем граф
        G = nx.Graph()

        nx.draw_planar(G, with_labels=True)

        # Добавляем узлы
        G.add_nodes_from(mass)

        # Добавляем ребра с разными цветами
        for i in range(len(mas_sviz) - 1, -1, -1):
            s = mas_sviz[i].split()
            G.add_edge(s[0], s[1], color=mas_cvetov[mas_uzl_cvet[i]])

        '''создаем словарь который содержит верщины и их цвет, первая верншина(корень) всегда красная, так мы обозначаем корень дерева, все остальные голубые'''
        node_colors = {isxod: 'red'}  # создание словаря где корень имеет красный цвет
        n = mass.pop(mass.index(isxod))  # удаляем корень из сета всех вершин конуса
        for i in mass:  # цикл которые заполнит оставшийся словарь где ключем будет вершина, а его аргументом цвет, в данном случем голубой
            node_colors[i] = ('lightblue')

        # Получаем список цветов для ребер
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]

        # Позиции узлов для отображения
        # Рисуем дерево по шаблону planar с разными цветами вершин и ребер
        nx.draw_planar(G, with_labels=True, node_color=[node_colors[n] for n in G.nodes()], edge_color=edge_colors)
        plt.savefig('image_conus.jpg')  # сохраняем получившееся дерево в формате .jpg
        plt.show()  # показываем дерево

        '''
        Функция на вход получает массив строк типа:['a b c d'], а так же элемент isxod который нужен что бы панять от какого элемента строить конус
        на выход функция ничего не возвращает, только делает изображение получившегося конуса
        примечание, для узлов значение обязательно должно храниться в словаре
        '''

    def postroenie(self, mas):  # функция для общего построения

        '''

        :param mas: массив строк формата ['a b c v']
        :return: массив цветов ребер и самих ребер
        '''

        s = []  # создаем перемнную для хранения цветов ребр и самих ребр
        v, n = self.cvet_uzlov(mas)  # создаем связи(ребра) всего дерева и цвета ребер
        s.append(self.konecha(v, n, self.otdelno_uzl(self.conus(mas, mas[0][0]))))
        s.append(self.otdelno_uzl(self.conus(mas, mas[0][0])))
        return s

    '''
    Данная функция получает на вход массив строк формата:['a b c d']
    и создает массив цветов ребер и самих ребер 
    '''

    def uroven(self, mas, c):

        '''

        :param mas: массив строк формата ['a b c v']
        :param c: уровень который нужно вывести
        :return: строка формата 'с: a b ... g' например: '3: a v f'
        '''

        uzels = []  # создаем пустой маасив для того, что бы хранить в нем нужный уровень каждой ветки, если такой уровень есть
        for i in range(len(mas)):
            x = mas[
                i].split()  # перевод ветки в массив и если в ветке есть нужный уровень, то он добавляется в переменную uzels
            if len(x) >= c:
                uzels.append(x[c - 1])
        uzels = list(set(uzels))  # убираем все повторяющиеся элемнты
        stroka_vod = str(c) + ':'
        for i in uzels:
            stroka_vod += ' ' + str(i)
        return stroka_vod  # организовываем вывод формата "2: a b"

    '''Функция нужна для вывода уровней дерева
    На вход подается массив строк формата ['a b c v'], с - это уровень, который нужно вывести
    На выходе представлена строка формата 'с: a b ... g' например: '3: a v f' '''

    def codirovka(self, Stroca, Set_elementov):
        conecn = []
        Stroca = (Stroca).split()
        for i in range(len(Stroca)):
            conecn.append(Set_elementov.index(Stroca[i]) + 1)
        return conecn

    def p_sme(self, mas):  # массив всех вершин без повторений

        '''
        :param mas: масиив строк типа:['a b c', 'f g h']
        :return: отсортированный масив всех вершин без повторений формата ['a','b','c']
        '''

        nabor_elementov = ''  # строка, которая впосредствии будет представленна в виде отсортированого набора элементов
        for i in range(len(mas)):
            nabor_elementov += mas[i] + ' '  # добавляем все имеищиеся вершины в строку
        nabor_elementov = nabor_elementov[:-1]  # удаляем последний элемент который будет ' '
        nabor_elementov = list(
            set(nabor_elementov.split()))  # превращаем строку в масив и убираем при помощи setа все повторения и снова превращаем set в массив
        return sorted(nabor_elementov)  # сортируем набор вершин для удобства в будущем

    def tabl_smegmm(self, mas):  # вход масив входных данных выводит таблицу смежности
        '''

        :param mas: масиив строк типа:['a b c', 'f g h']
        :return: таблица смежности массива
        '''

        set_elementov = self.p_sme(mas)  # создаем сет всех вершин
        conechn_mas = []
        for i in range(len(mas)):
            conechn_mas.append(self.codirovka(mas[i], set_elementov))
        '''
        создаем пустую таблицу смежности она заполнена нулями и имеет одну дополнительную строку и сталбец для того,
        что бы заполнить их вершина
        '''

        tablica_smeg = (len(set_elementov) + 1) * ['0']
        for i in range(len(set_elementov) + 1):
            tablica_smeg[i] = (len(set_elementov) + 1) * ['0']

        '''
        заполняем таблицу смежности, если находим один элемент, то симетрично запалняем и второй
        '''

        for i in range(len(conechn_mas)):
            for j in range(len(conechn_mas[i]) - 1):
                tablica_smeg[conechn_mas[i][j]][conechn_mas[i][j + 1]] = '1'
                tablica_smeg[conechn_mas[i][j + 1]][conechn_mas[i][j]] = '1'

        '''
        заполняем вершины в таблице смежности
        '''

        tablica_smeg[0][0] = ' '  # убираем верхний левый элемент
        for i in range(len(set_elementov)):
            tablica_smeg[0][i + 1] = set_elementov[i]  # заполяем вершины по строке
            tablica_smeg[i + 1][0] = set_elementov[i]  # завполныем вершины в столбике

        '''
        конечный вариант выглядит примрно так:

          a b c d f
        a 0 1 0 0 1
        b 1 0 0 0 0
        c 0 0 0 0 0
        f 1 0 0 0 0

        '''
        return tablica_smeg  # выводим таблицу смежности

    def postroenie_grafa(self, mass):
        '''

        :param mass: масиив строк типа:['a b c', 'f g h']
        :return: n-арное дерево построенное по шаблону planar библиотеки NetworkX
        '''

        mas = self.p_sme(mass)  # сет всех элементов
        """"создает массив цветов
        которые используются в построение"""
        mas_cvetov = []  # массив в котором будут лежать все цвета
        for i in range(
                len(mas) * 10):  # Запускаем цикл по генерации цветов, запустил что бы цветов было в 10 раз больше чемсамих вершин, это нужно, что бы исключить, что цвета повторяются
            mas_cvetov.append('#%06X' % randint(0, 0xFFFFFF))  # генерация цветов в 16ти ричной кодировке
        mas_cvetov = list(set(mas_cvetov))  # удаляем все повторяющиеся цвета

        mas_sviz, mas_uzl_cvet = self.cvet_uzlov(mass)

        # Создаем граф
        G = nx.Graph()

        nx.draw_planar(G, with_labels=True)

        # Добавляем узлы
        G.add_nodes_from(mas)

        # Добавляем ребра с разными цветами
        for i in range(len(mas_sviz) - 1, -1, -1):
            s = mas_sviz[i].split()
            G.add_edge(s[0], s[1], color=mas_cvetov[mas_uzl_cvet[i]])

        '''создаем словарь который содержит верщины и их цвет, первая верншина всегда красная, так мы обозначаем корень дерева, все остальные голубые'''
        node_colors = {mass[0][0]: 'red'}
        n = mas.pop(mas.index(mass[0][0]))
        for i in mas:
            node_colors[i] = ('lightblue')

        # Получаем список цветов для ребер
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]

        # Позиции узлов для отображения

        nx.draw_planar(G, with_labels=True, node_color=[node_colors[n] for n in G.nodes()], edge_color=edge_colors)
        plt.savefig('image.jpg')  # сохраняем изображение n-арного дерева
        plt.show()  # рисуем граф

    '''Функция агент фрейм'''

    def agent(self, mas, n):
        '''

        :param mas: масиив строк типа:['a b c', 'f g h']
        :param n: номер ветки
        :return: на выводе мы получим ветку которую запросил пользователь, а так же изображение самой ветки
        '''
        if n > len(mas) or n < 0:  # проверка на наличие данной ветки в дереве, если таковой нет, то выводится 0
            return (0)

        stroka_massiv = mas[n - 1]  # сама ветка

        '''
        построение ветки дерева по шаблону planar библиотеки NetworkX
        '''
        massiv = stroka_massiv.split()  # разделяем ветку на вершины

        G = nx.Graph()  # создаем пустой граф
        G.add_nodes_from(massiv)  # Добавляем в граф все вершины

        # Добавляю связи между элементами
        for i in range(len(massiv) - 1):
            G.add_edge(massiv[i], massiv[i + 1])

        nx.draw_planar(G, with_labels=True)  # строим дерево пошаблону Planar
        plt.savefig('image_agent.jpg')  # сохраняем изображение ветки дерева
        plt.show()  # рисуем ветку дерева по шаблону Planar библиотеки NetworkX

        return stroka_massiv

    def agent_frame(self, mass, n):
        '''
        :param mass: масиив строк типа:['1: a b c', '2: f g h']
        :param n: номер ветки
        :return: на выводе мы получим ветку которую запросил пользователь, а так же изображение самой ветки
        '''
        return (self.agent(ctenie(mass), n))

    """                 Конец"""

    '''Функция лайер, короче она нужна что бы вывести уровень узлов'''

    def layer(self, mas, n):
        '''
        :param mas: масиив строк типа:['a b c', 'f g h']
        :param n: уровень который требуется
        :return: на выводе получаем изображение узлов, а так же сами узлы
        '''

        stroka = []  # массив в котором будут находится все уровни без повторений
        '''
        добавляляем элементы в массив
        '''
        for i in mas:
            lous = i.split()  # разделяем каждую строку, на массив
            if len(lous) >= n and n > 0:
                stroka.append(lous[n - 1])  # добавляем элемент в массив, если такой есть
        stroka = list(set(stroka))  # удаляем все повторяющиеся элементы
        otvet = ''  # конечная строка, которая будет содержать в себе весь уровень фрейма
        for i in stroka:
            otvet += i + ' '

        mass = self.p_sme(mas)  # сет всех элементов

        """"создает массив цветов
        которые используются в построение"""
        mas_cvetov = []  # массив в котором будут лежать все цвета
        for i in range(
                len(mass) * 10):  # Запускаем цикл по генерации цветов, запустил что бы цветов было в 10 раз больше чемсамих вершин, это нужно, что бы исключить, что цвета повторяются
            mas_cvetov.append('#%06X' % randint(0, 0xFFFFFF))  # генерация цветов в 16ти ричной кодировке
        mas_cvetov = list(set(mas_cvetov))  # удаляем все повторяющиеся цвета

        mas_sviz, mas_uzl_cvet = self.cvet_uzlov(mas)

        # Создаем граф
        G = nx.Graph()

        nx.draw_planar(G, with_labels=True)

        # Добавляем узлы
        G.add_nodes_from(mass)

        # Добавляем ребра с разными цветами
        for i in range(len(mas_sviz) - 1, -1, -1):
            s = mas_sviz[i].split()
            G.add_edge(s[0], s[1], color=mas_cvetov[mas_uzl_cvet[i]])

        '''создаем словарь который содержит верщины и их цвет, первая верншина всегда красная, так мы обозначаем корень дерева, все остальные голубые'''
        '''Дополнительная проверки, если уровень в фрейме равен 1'''
        if n != 1:
            node_colors = {mas[0][0]: 'red'}  # первый элемент а так же вершина была красной
            for i in stroka:
                node_colors[i] = ('green')  # все вершины уровня будут зелеными
                n = mass.pop(mass.index(i))  # удаляем вершины уровня из массива

            n = mass.pop(mass.index(mass[0][0]))  # удаление вершины
            for i in mass:
                node_colors[i] = ('lightblue')  # все оставшиеся вершины будут голубыми
        else:
            node_colors = {mas[0][0]: 'green'}  # корень красив в зеленый
            n = mass.pop(mass.index(mass[0][0]))  # удаляем корень
            for i in mass:
                node_colors[i] = ('lightblue')  # все оставшиеся вершины будут голубыми
        # Получаем список цветов для ребер
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]

        # Позиции узлов для отображения

        nx.draw_planar(G, with_labels=True, node_color=[node_colors[n] for n in G.nodes()], edge_color=edge_colors)
        plt.savefig('layer.jpg')  # сохраняем изображение n-арного дерева
        plt.show()  # рисуем граф

        return (otvet)

    '''конечная функция'''

    def layer_frame(self, mas, n):
        '''
        :param mas: масиив строк типа:['1: a b c', '2: f g h']
        :param n: номер уровня
        :return: изображение уровня и вывод его в виде строки
        '''

        return self.layer(ctenie(mas), n)

    def postroenie_Exel(self, mas):  # Функция для построения таблицы Exel
        '''
        :param mas: масиив строк типа:['a b c', 'f g h']
        :return: эксель файл, содержащий таблицу смежности
        '''

        massiv = self.tabl_smegmm(mas)  # сохраняем таблицу смежности
        wb = openpyxl.Workbook()  # создаем таблицу

        sheet = wb.active
        '''
        заполняем таблицу смежности
        '''
        for i in range(len(massiv)):
            # заполняем посимвольно таблицу
            for j in range(len(massiv[i])):
                c = sheet.cell(row=i + 1, column=j + 1)
                c.value = massiv[i][j]

        wb.save("sampling.xlsx")  # сохраняем таблицу Exel

    def postroenie_grafa_frame(self, mass):
        '''
        :param mass: масиив строк типа:['1: a b c', '2: f g h']
        :return: n-арное дерево построенное по шаблону planar библиотеки NetworkX
        '''
        mas = ctenie(mass)  # убираем первые 3 символа во входных данных
        self.postroenie_grafa(mas)

        self.postroenie_Exel(mas)

    '''конечная функция которая выводит конусы и строит таблицу смежности если конус >1'''

    def conus_frame(self, mass, isxod):
        '''
        :param mass: масиив строк типа:['1: a b c', '2: f g h']
        :param isxod: название вершины относительно которой строить сам конус
        :return: построение конуса и вывод его веток
        '''
        mas = ctenie(mass)  # убираем первые 3 символа во входных данных
        self.postroenie_Exel(self.conus(mas, isxod))
        n = self.grupp_cveta_konus(mas, isxod)
        return self.p_sme(self.conus(mas, isxod))


def ctenie(mas):  # функция для чтения входных данных
    '''
    :param mas: масиив строк типа:['1: a b c', '2: f g h']
    :return: масиив строк типа:['a b c', 'f g h']
    '''
    konecnkl_massiv = []  # конечный массив
    for i in mas:
        stroka = i[i.index(' ') + 1:]  # удаляем первые 3 элемента строки
        konechnai_stroka = ''
        for i in stroka:
            # удаление запятых, если таковые имеются
            if i != ',':
                konechnai_stroka += i
        konecnkl_massiv.append(konechnai_stroka)  # дабавляем строку без первых 3 элементов

        '''
        может обрабатывать как последовательности строк содержащие запятые между вершинами
        например:
        ['1: a, b, c, d', '2: a, b, c, e', '3: a, b, c, f']
        так и просто массив входных данных:
        ['1: a b c d', '2: a b c e', '3: a b c f']
        '''

    return (konecnkl_massiv)


mass = ['1: a b c d', '2: a b c e', '3: a b c f к']
derevo = Drevo()
mas = ctenie(mass)
print(derevo.conus_frame(mass, 'c'))