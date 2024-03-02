"""

### INTREGRANTES

    - Oneylis Manuela Mercedes Marte (2021-0357)
    - kaholy Alexandra Dalis Peña (2021-0687)
    - Rosmeiry Garabito Maria (2021-0587)
    - Lisbeth Maria Morales Eusebio (2020-10658)
    - Daniel Alexander Pereyra Beltran (2020-9992)
    - Moises Nuñez Del Rosario (2020-10457)

"""

""" Librerias utilizadas """


""" Clase que representa el Puzzle-n general """




import os
import time
import math
from tkinter import *
from tkinter import ttk
class PuzzleState(object):
    """ docstring para PuzzleState """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n * n != len(config) or n < 2:
            raise Exception("La longitud de la configuracion no es correcta!")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None

        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    """ Expandir el nodo """

    def expand(self):

        # Añadir nodos hijos en orden UDLR (Up-Down-Left-Right)

        if len(self.children) == 0:
            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children


""" texto en cursiva Funcion Indica si se llegó a la meta """


def test_goal(puzzle_state):
    puzzle_completed = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    if puzzle_state.config == puzzle_completed:
        return True


""" Funcion que calcula heuristica posiciones correctas """


def calcular_heurisitica(estado):
    correcto = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    valor_correcto = 0
    piezas_correctas = 0
    piezas_incorrectas = 0
    for valor_pieza, valor_correcto in zip(list(estado.config), correcto):
        if valor_pieza == valor_correcto:
            piezas_correctas += 1
        else:
            piezas_incorrectas += 1
        valor_correcto += 1
    return (piezas_incorrectas - 1) + estado.cost


""" Funcion para calcular la ruta """


def calcular_ruta(state):
    ruta = [state.action]
    ruta_padres = state.parent
    while ruta_padres:
        if ruta_padres.parent:
            ruta.append(ruta_padres.action)
        ruta_padres = ruta_padres.parent
    return ruta[::-1]


""" Lista """


class Estructura_Datos():
    def __init__(self, initial=""):
        self.lista = list()
        self.push(initial)

    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
        dato = self.lista.pop(0)
        return dato

    def top(self):
        dato = self.lista[0]
        return dato

    def empty(self):
        return len(self.lista) == 0


""" Cola """


class Estructura_Cola:
    def __init__(self, initial=""):
        self.lista = list()
        self.push(initial)

    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
        dato = self.lista[-1]
        self.lista.pop()
        return dato

    def top(self):
        dato = self.lista[-1]
        return dato

    def empty(self):
        return len(self.lista) == 0


""" Prioridades de la cola """


class Prioridad_Cola:
    def __init__(self, initial=""):
        self.lista = []
        self.push(initial)

    def push(self, dato):
        self.lista.append(dato)

    def pop(self):
        self.lista = sorted(self.lista, key=lambda x: x[0])
        return self.lista.pop(0)

    def top(self):
        dato = self.lista[0]
        return dato

    def empty(self):
        return len(self.lista) == 0


""" ALGORItMO BFS """


def bfs_search(initial_state):
    frontier = Estructura_Datos(initial_state)
    frontier_dic = {tuple(initial_state.config): "add"}
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            search_depth = len(path_to_goal)
            return path_to_goal, state.cost, nodes_expanded, search_depth, max_search_depth

        nodes_expanded += 1
        for node in state.expand():
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push(node)
                if node.cost > max_search_depth:
                    max_search_depth = node.cost
    return False


""" Resultados """


def resul(query_list, type, total_results):
    ventana = Tk()
    ventana.title('Resultado de la forma ' + type)
    ventana.geometry('400x300')
    ventana['bg'] = '#fb0'

    tv = ttk.Treeview(ventana, height=5, columns=("col1", "col2"))

    tv.column("#0", width=80)
    tv.column("col1", width=80, anchor=CENTER)
    tv.column("col2", width=80, anchor=CENTER)

    tv.heading("#0", text=" ", anchor=CENTER)
    tv.heading("col1", text="Inicio", anchor=CENTER)
    tv.heading("col2", text="  ", anchor=CENTER)

    tv.insert("", END, text=query_list[0],
              values=(query_list[1], query_list[2]))
    tv.insert("", END, text=query_list[3],
              values=(query_list[4], query_list[5]))
    tv.insert("", END, text=query_list[6],
              values=(query_list[7], query_list[8]))

    tv1 = ttk.Treeview(ventana, height=5, columns=("col1", "col2"))

    tv1.column("#0", width=80)
    tv1.column("col1", width=80, anchor=CENTER)
    tv1.column("col2", width=80, anchor=CENTER)

    tv1.heading("#0", text=" ", anchor=CENTER)
    tv1.heading("col1", text="Final", anchor=CENTER)
    tv1.heading("col2", text="  ", anchor=CENTER)

    tv1.insert("", END, text="1", values=("2", "3"))
    tv1.insert("", END, text="4", values=("5", "6"))
    tv1.insert("", END, text="7", values=("8", "0"))

    writeOutput(total_results)
    tv.pack()
    tv1.pack()
    ventana.mainloop()


""" Datos de salida del algoritmo """


def writeOutput(resultado):
    path_to_goal, cost_of_path, nodes_expande, search_depth, max_search_depth = resultado[0]
    running_time = resultado[1]
    file = open("output.txt", "w")
    file.write(f"""
    path_to_goal: {path_to_goal}
    cost_of_path: {cost_of_path}
    nodes_expanded: {nodes_expande}
    search_depth: {search_depth}               
    max_search_depth: {max_search_depth}
    running_time: {running_time}
    """)
    file.close()
    path = 'output.txt'
    os.system('start ' + path)


""" ALGORITMO  DFS """


def dfs_search(initial_state):
    frontier = Estructura_Cola(initial_state)
    frontier_dic = {tuple(initial_state.config): "add"}
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            search_depth = len(path_to_goal)
            return path_to_goal, state.cost, nodes_expanded, search_depth, max_search_depth

        nodes_expanded += 1
        for node in state.expand()[::-1]:
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push(node)
                if node.cost > max_search_depth:
                    max_search_depth = node.cost
    return False


""" ALGORITMO AST """


def a_star_search(initial_state):
    """ A * search """

    frontier = Prioridad_Cola(
        (calcular_heurisitica(initial_state), initial_state))
    frontier_dic = {tuple(initial_state.config): "add"}
    explored = set()
    max_search_depth = 0
    nodes_expanded = 0

    while not frontier.empty():
        state_heuristic, state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            path_to_goal = calcular_ruta(state)
            search_depth = len(path_to_goal)
            return path_to_goal, state.cost, nodes_expanded, search_depth, max_search_depth

        nodes_expanded += 1
        for node in state.expand():
            if tuple(node.config) not in frontier_dic and node.config not in explored:
                frontier_dic[tuple(node.config)] = "add"
                frontier.push((calcular_heurisitica(node), node))
                if node.cost > max_search_depth:
                    max_search_depth = node.cost
    return False


""" MAIN """


# Función Main que leerá las entradas y llamará el algoritmo correspondiente

def main():
    resultado = []
    type = "tipo"
    clear()
    print("Bienvenido a la solución del problema del 8-puzzle\n")
    print("Seleccione el algoritmo que desea utilizar:")
    print("1. BFS")
    print("2. DFS")
    print("3. AST")
    print("4. Salir")
    opcion = int(input("\nIngrese una opción: "))

    if opcion == 4:
        print("Gracias por utilizar el programa")
        return

    query_list = input("Ingrese el puzzle: ")
    if len(query_list) != 17:
        main()

    star_time = time.time()
    query_list = query_list.split(",")
    query = tuple(map(int, query_list))
    size = int(math.sqrt(len(query)))
    hard_state = PuzzleState(query, size)

    if opcion == 1:
        resultado = bfs_search(hard_state)
        type = "BFS"
    elif opcion == 2:
        resultado = dfs_search(hard_state)
        type = "DFS"
    elif opcion == 3:
        resultado = a_star_search(hard_state)
        type = "AST"
    if resultado:
        total_time = time.time() - star_time
        total_results = (resultado, total_time)
        resul(query_list, type, total_results)

    else:
        clear()
        print("No se pudo encontrar una solucción al puzzle")
        return


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
