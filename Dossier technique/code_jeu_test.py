import pyxel

# ======================
# CONSTANTES D'ÉCHELLE
# ======================
WINDOW_W = 600
WINDOW_H = 400

PERSO_W = 33
PERSO_H = 76

SOL_Y = WINDOW_H - PERSO_H

VITESSE_X = 6
VITESSE_Y = 5

# ======================
# JOUEUR 1
# ======================
position_joueur1_x = 60
position_joueur1_y = SOL_Y

jump = 150
is_jumping = False

attaque_active = False
attaque_timer = 0
attaque_duree = 10
attaque_portee = 40

pv_joueur1 = 15
attaque1_a_touche = False

# ======================
# JOUEUR 2
# ======================
position_joueur2_x = 500
position_joueur2_y = SOL_Y

jump2 = 150
is_jumping2 = False

attaque2_active = False
attaque2_timer = 0
attaque2_duree = 10
attaque2_portee = 40

pv_joueur2 = 15
attaque2_a_touche = False


# ======================
# COLLISIONS
# ======================
def collision_largeur(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )

def collision_hauteur(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 + w1 > x2 and
        x1 < x2 + w2 and
        y1 + h1 <= y2 + 10 and
        y1 + h1 >= y2
    )

def est_sur(x1, y1, w1, h1, x2, y2, w2):
    return (
        x1 + w1 > x2 and
        x1 < x2 + w2 and
        y1 + h1 == y2
    )


# ======================
# UPDATE
# ======================
def update():
    global position_joueur1_x, position_joueur1_y, is_jumping
    global position_joueur2_x, position_joueur2_y, is_jumping2
    global attaque_active, attaque_timer, attaque2_active, attaque2_timer
    global pv_joueur1, pv_joueur2, attaque1_a_touche, attaque2_a_touche

    # --- Joueur 1 déplacements ---
    if pyxel.btn(pyxel.KEY_D):
        nx = position_joueur1_x + VITESSE_X
        if nx + PERSO_W <= position_joueur2_x:
            position_joueur1_x = nx

    if pyxel.btn(pyxel.KEY_Q):
        position_joueur1_x = max(0, position_joueur1_x - VITESSE_X)

    if pyxel.btnp(pyxel.KEY_Z) and not is_jumping:
        is_jumping = True
        position_joueur1_y = SOL_Y - jump

    if is_jumping:
        ny = position_joueur1_y + VITESSE_Y
        if collision_hauteur(position_joueur1_x, ny, PERSO_W, PERSO_H,
                             position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
            position_joueur1_y = position_joueur2_y - PERSO_H
            is_jumping = False
        elif ny < SOL_Y:
            position_joueur1_y = ny
        else:
            position_joueur1_y = SOL_Y
            is_jumping = False

    # --- Attaque J1 ---
    if pyxel.btnp(pyxel.KEY_E) and not attaque_active:
        attaque_active = True
        attaque_timer = attaque_duree

    if attaque_active:
        attaque_timer -= 1
        if attaque_timer <= 0:
            attaque_active = False

    # --- Joueur 2 déplacements ---
    if pyxel.btn(pyxel.KEY_K):
        nx = position_joueur2_x - VITESSE_X
        if nx >= position_joueur1_x + PERSO_W:
            position_joueur2_x = nx

    if pyxel.btn(pyxel.KEY_M):
        nx = position_joueur2_x + VITESSE_X
        if nx + PERSO_W <= WINDOW_W:
            position_joueur2_x = nx

    if pyxel.btnp(pyxel.KEY_O) and not is_jumping2:
        is_jumping2 = True
        position_joueur2_y = SOL_Y - jump2

    if is_jumping2:
        ny = position_joueur2_y + VITESSE_Y
        if collision_hauteur(position_joueur2_x, ny, PERSO_W, PERSO_H,
                             position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
            position_joueur2_y = position_joueur1_y - PERSO_H
            is_jumping2 = False
        elif ny < SOL_Y:
            position_joueur2_y = ny
        else:
            position_joueur2_y = SOL_Y
            is_jumping2 = False

    # --- Attaque J2 ---
    if pyxel.btnp(pyxel.KEY_P) and not attaque2_active:
        attaque2_active = True
        attaque2_timer = attaque2_duree

    if attaque2_active:
        attaque2_timer -= 1
        if attaque2_timer <= 0:
            attaque2_active = False

    # --- Dégâts ---
    if attaque_active:
        if not attaque1_a_touche and collision_largeur(
            position_joueur1_x + PERSO_W, position_joueur1_y + 20,
            attaque_portee, 50,
            position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
            pv_joueur2 -= 1
            attaque1_a_touche = True
    else:
        attaque1_a_touche = False

    if attaque2_active:
        if not attaque2_a_touche and collision_largeur(
            position_joueur2_x - attaque2_portee, position_joueur2_y + 20,
            attaque2_portee, 50,
            position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
            pv_joueur1 -= 1
            attaque2_a_touche = True
    else:
        attaque2_a_touche = False


# ======================
# DRAW
# ======================
def draw():
    pyxel.cls(1)

    if pv_joueur1 > 0 and pv_joueur2 > 0:
    # Joueurs
        pyxel.rect(position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H, 10)
        pyxel.rect(position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H, 11)

        # Attaques collées aux persos
        if attaque_active:
            attaque_x = position_joueur1_x + PERSO_W  # bord droit du joueur 1
            attaque_y = position_joueur1_y + 20
            pyxel.rect(attaque_x, attaque_y, attaque_portee, 50, 8)

        if attaque2_active:
            attaque2_x = position_joueur2_x - attaque2_portee  # bord gauche du joueur 2
            attaque2_y = position_joueur2_y + 20
            pyxel.rect(attaque2_x, attaque2_y, attaque2_portee, 50, 3)
            
        # Barre PV
        pyxel.rect(20, 20, pv_joueur1 * 10, 10, 8)
        pyxel.rect(600 - 20 - pv_joueur2 * 10, 20, pv_joueur2 * 10, 10, 3)
        # PV
        pyxel.text(20, 10, f"J1 PV: {pv_joueur1}", 7)
        pyxel.text(WINDOW_W - 60, 10, f"J2 PV: {pv_joueur2}", 7)

    elif pv_joueur2 <= 0:
        pyxel.cls(0)
        pyxel.text(300, 200, 'GAME OVER', 7)
        pyxel.text(300, 250, 'J1 à ganger', 7)
    elif pv_joueur1 <= 0:
        pyxel.cls(0)
        pyxel.text(300, 200, 'GAME OVER', 7)
        pyxel.text(300, 250, 'J2 à ganger', 7)


# ======================
# LANCEMENT
# ======================
pyxel.init(WINDOW_W, WINDOW_H)
pyxel.run(update, draw)
