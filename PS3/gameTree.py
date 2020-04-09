from graphviz import Digraph

g = Digraph(format="png")
alphabet = 'abcdefghijklmnopqrstuvwxyz'
node_counts = [("sk", "South Korea", 1), ("us", "United States", 2), ("nk", "North Korea", 4)]
scores = {"aaa": (0,0,-10),
          "aap": (-1, -3, 1),
          "apa": (-2, -1, 3),
          "app": (-5, 1, 1),
          "paa": (-2, 1, 0),
          "pap": (-2, -5, 2),
          "ppa": (-5, -2, 5),
          "ppp": (4, 1, 0)
}

for (short, label, count) in node_counts:
    for idx in range(count):
        g.node(f"{short}{idx}", label=label)

for (n, score) in scores.items():
    g.node(n, label=str(score))

g.edge("sk0", "us0", label="aggressive")
g.edge("sk0", "us1", label="passive")

g.edge("us0", "nk0", label="aggressive")
g.edge("us0", "nk1", label="passive")

g.edge("us1", "nk2", label="aggressive")
g.edge("us1", "nk3", label="passive")

g.edge("nk0", "aaa", label="aggressive")
g.edge("nk0", "aap", label="passive")

g.edge("nk1", "apa", label="aggressive")
g.edge("nk1", "app", label="passive")

g.edge("nk2", "paa", label="aggressive")
g.edge("nk2", "pap", label="passive")

g.edge("nk3", "ppa", label="aggressive")
g.edge("nk3", "ppp", label="passive")



g.render("tree")
