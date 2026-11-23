import itertools
import numpy as np

# --- Stratégie classique : on teste les 16 stratégies possibles ---
def meilleur_classique():
    meilleur = 0
    for a0, a1, b0, b1 in itertools.product([0, 1], repeat=4):
        A = {0: a0, 1: a1}
        B = {0: b0, 1: b1}
        gains = sum((A[x] ^ B[y]) == (x & y) for x in (0, 1) for y in (0, 1))
        meilleur = max(meilleur, gains / 4)
    return meilleur

# --- Stratégie quantique ---
phi = np.array([1, 0, 0, 1]) / np.sqrt(2)  # paire de Bell

def base(t):
    # deux résultats possibles (0 et 1) pour une mesure d'angle t
    return [np.array([np.cos(t), np.sin(t)]),
            np.array([-np.sin(t), np.cos(t)])]

def mesure(x, y):
    ta = [0, np.pi / 4][x]            # angle d'Alice
    tb = [np.pi / 8, -np.pi / 8][y]   # angle de Bob
    probas = []
    for a in range(2):
        for b in range(2):
            v = np.kron(base(ta)[a], base(tb)[b])
            probas.append(abs(v @ phi) ** 2)
    r = np.random.choice(4, p=probas)
    return r // 2, r % 2              # (a, b)

def jeu_quantique(n=10000):
    victoires = 0
    for _ in range(n):
        x, y = np.random.randint(2), np.random.randint(2)
        a, b = mesure(x, y)
        victoires += (a ^ b) == (x & y)
    return victoires / n

print(f"Meilleur classique : {meilleur_classique():.1%}")
print(f"Quantique (10000 parties) : {jeu_quantique():.1%}")

# --- Mode "boîte magique" : chaque élève joue pour de vrai ---
# (décommente pour l'utiliser)
# while True:
#     x = np.random.randint(2); y = np.random.randint(2)
#     a, b = mesure(x, y)
#     print(f"Alice reçoit x={x} -> a={a} | Bob reçoit y={y} -> b={b}")
#     input("Entrée pour le tour suivant...")
