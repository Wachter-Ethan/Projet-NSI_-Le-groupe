import pyxel

# -----------------------------
# Constantes et pages
# -----------------------------
WIDTH = 600
HEIGHT = 400

PAGE_MENU = 0
PAGE_GAME = 1
PAGE_OPTIONS = 2

page = PAGE_MENU

# -----------------------------
# Menu
# -----------------------------
current_option = 0
options = ["Jouer", "Options", "Quitter"]



# Parti code jeu :

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

# KNOCKBACK
KNOCKBACK = 50

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



# -----------------------------
# Update
# -----------------------------
def update():
    global current_option, page

    # ---- Menu ----
    if page == PAGE_MENU:
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_L):
            current_option = (current_option + 1) % len(options)
        elif pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_O):
            current_option = (current_option - 1) % len(options)

        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_E):
            if options[current_option] == "Jouer":
                page = PAGE_GAME
            elif options[current_option] == "Options":
                page = PAGE_OPTIONS
            elif options[current_option] == "Quitter":
                pyxel.quit()

    # ---- Jeu ----
    elif page == PAGE_GAME:
        global position_joueur1_x, position_joueur1_y, is_jumping
        global position_joueur2_x, position_joueur2_y, is_jumping2
        global attaque_active, attaque_timer, attaque2_active, attaque2_timer
        global pv_joueur1, pv_joueur2, attaque1_a_touche, attaque2_a_touche
        global KNOCKBACK, VITESSE_Y, VITESSE_X, SOL_Y, PERSO_H, PERSO_W

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
                
                # Knockback vers la droite
                position_joueur2_x += KNOCKBACK
                if position_joueur2_x + PERSO_W > WINDOW_W:
                    position_joueur2_x = WINDOW_W - PERSO_W
                
                attaque1_a_touche = True
        else:
            attaque1_a_touche = False

        if attaque2_active:
            if not attaque2_a_touche and collision_largeur(
                position_joueur2_x - attaque2_portee, position_joueur2_y + 20,
                attaque2_portee, 50,
                position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
                pv_joueur1 -= 1
                
                # Knockback vers la gauche
                position_joueur1_x -= KNOCKBACK
                if position_joueur1_x < 0:
                    position_joueur1_x = 0
                
                attaque2_a_touche = True
        else:
            attaque2_a_touche = False
        
    # ---- Options ----
    elif page == PAGE_OPTIONS:
        if pyxel.btnp(pyxel.KEY_TAB):
            page = PAGE_MENU

# -----------------------------
# Draw
# -----------------------------
def draw():
    pyxel.cls(11)

    if page == PAGE_MENU:
        pyxel.text(WIDTH//2 - 70, 50, "PLANT FIGHTER", pyxel.COLOR_BLACK)
        for i, option in enumerate(options):
            color = pyxel.COLOR_GREEN if i == current_option else pyxel.COLOR_BLACK
            pyxel.text(WIDTH//2 - 40, 150 + i*50, option, color)  # texte plus grand et espacé

    elif page == PAGE_GAME:
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

    elif page == PAGE_OPTIONS:
        pyxel.cls(7)
        pyxel.text(50, 50, "=== OPTIONS ===", pyxel.COLOR_BLACK)
        pyxel.text(50, 100, "Contrôles J1:", pyxel.COLOR_BLACK)
        pyxel.text(70, 130, "Q/D: déplacer", pyxel.COLOR_BLACK)
        pyxel.text(70, 160, "Z: sauter", pyxel.COLOR_BLACK)
        pyxel.text(70, 190, "E: attaquer", pyxel.COLOR_BLACK)
        pyxel.text(200, 100, "Contrôles J2:", pyxel.COLOR_BLACK)
        pyxel.text(220, 130, "K/M: déplacer", pyxel.COLOR_BLACK)
        pyxel.text(220, 160, "O: sauter", pyxel.COLOR_BLACK)
        pyxel.text(220, 190, "P: attaquer", pyxel.COLOR_BLACK)
        pyxel.text(50, 250, "TAB: retour au menu", pyxel.COLOR_RED)

# -----------------------------
# Lancement
# -----------------------------
pyxel.init(WIDTH, HEIGHT, fps=60)
pyxel.run(update, draw)
