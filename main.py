import os
import string

from scipy.sparse import dok_matrix
from scipy.sparse.csgraph import dijkstra

from tkinter import *


def new_word(w, p, c):
    return w[:p] + c + w[p + 1:]


# read some instance of the English dictionary
word_list = open('words.txt').readlines()
word_list = map(str.strip, word_list)

# filter 'bad' words
word_list = filter(str.isalpha, word_list)  # no punctuation
word_list = filter(str.islower, word_list)  # no proper nouns or acronyms

# convert to list
word_list = list(word_list)

n = len(word_list)
sparse_graph = dok_matrix((n, n), dtype=bool)

d = dict()
for (ind, word) in enumerate(word_list):
    d[word] = ind

if os.path.isfile('edges.txt'):
    edges = open("edges.txt", 'r').readlines()

    for edge in edges:
        x, y = map(int, edge.strip().split())
        sparse_graph[x, y] = True

else:
    edges = open('edges.txt', 'w')

    for (ind1, word) in enumerate(word_list):
        for (i, old_letter) in enumerate(word):
            for new_letter in string.ascii_lowercase:
                if old_letter != new_letter:
                    ind2 = d.get(new_word(word, i, new_letter), None)

                    if ind2 is not None:
                        sparse_graph[ind1, ind2] = True
                        print(ind1, ind2, file=edges)

    edges.close()

graph = sparse_graph.tocsr()


def compute_solution():
    source = d[str(e1.get())]
    destination = d[str(e2.get())]

    distances, predecessors = dijkstra(graph, indices=source, return_predecessors=True)

    path = []
    node = destination

    while node != source:
        path.append(word_list[node])
        node = predecessors[node]

    path.append(word_list[source])
    print("Distance from {0} to {1} is {2}".format(path[0], path[-1], int(distances[destination])))
    print("List of words: {0}: ".format(path[::-1]))

    e1.delete(0, END)
    e2.delete(0, END)


master = Tk()
master.wm_title("Word Ladder")

Label(master, text="Initial word").grid(row=0)
Label(master, text="Goal word").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Compute', command=compute_solution).grid(row=3, column=1, sticky=W, pady=4)

mainloop()
