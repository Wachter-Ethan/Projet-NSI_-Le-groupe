import pyxel

# -----------------------------
# Constantes et pages
# -----------------------------
WIDTH = 700
HEIGHT = 500

PAGE_MENU = 0
PAGE_GAME = 1
PAGE_OPTIONS = 2

page = PAGE_MENU

# -----------------------------
# Menu
# -----------------------------
current_option = 0
options = ["Jouer", "Options", "Quitter"]

# -----------------------------
# Joueur 1
# -----------------------------
position_joueur1_x = 60
position_joueur1_y = 350
LARGEUR_PERSO = 64
jump = 150
is_jumping = False
attaque_active = False
attaque_timer = 0
attaque_duree = 10
attaque_portee = 50

# -----------------------------
# Joueur 2
# -----------------------------
position_joueur2_x = 500
position_joueur2_y = 350
jump2 = 150
is_jumping2 = False
attaque2_active = False
attaque2_timer = 0
attaque2_duree = 10
attaque2_portee = 50

# -----------------------------
# Points de vie et touches
# -----------------------------
pv_joueur1 = 15
pv_joueur2 = 15
attaque1_a_touche = False
attaque2_a_touche = False

# -----------------------------
# Fonctions collision
# -----------------------------
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
    global position_joueur1_x, position_joueur1_y, is_jumping, attaque_active, attaque_timer
    global position_joueur2_x, position_joueur2_y, is_jumping2, attaque2_active, attaque2_timer
    global pv_joueur1, pv_joueur2, attaque1_a_touche, attaque2_a_touche

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
        # Joueur 1
        if pyxel.btn(pyxel.KEY_D):
            next_x = position_joueur1_x + 6
            if next_x + LARGEUR_PERSO <= position_joueur2_x:
                position_joueur1_x = next_x
        if pyxel.btn(pyxel.KEY_Q):
            next_x = position_joueur1_x - 6
            if next_x >= 0:
                position_joueur1_x = next_x
        if pyxel.btnp(pyxel.KEY_Z) and not is_jumping:
            is_jumping = True
            position_joueur1_y = 350 - jump
        if is_jumping:
            next_y = position_joueur1_y + 5
            if collision_hauteur(position_joueur1_x, next_y, LARGEUR_PERSO, 96,
                                 position_joueur2_x, position_joueur2_y, LARGEUR_PERSO, 96):
                position_joueur1_y = position_joueur2_y - 96
                is_jumping = False
            elif next_y < 350:
                position_joueur1_y = next_y
            else:
                position_joueur1_y = 350
                is_jumping = False
        if pyxel.btnp(pyxel.KEY_E) and not attaque_active:
            attaque_active = True
            attaque_timer = attaque_duree
        if attaque_active:
            attaque_timer -= 1
            if attaque_timer <= 0:
                attaque_active = False

        # Joueur 2
        if pyxel.btn(pyxel.KEY_K):
            next_x = position_joueur2_x - 6
            if next_x >= position_joueur1_x + LARGEUR_PERSO:
                position_joueur2_x = next_x
        if pyxel.btn(pyxel.KEY_M):
            next_x = position_joueur2_x + 6
            if next_x + LARGEUR_PERSO <= WIDTH:
                position_joueur2_x = next_x
        if pyxel.btnp(pyxel.KEY_O) and not is_jumping2:
            is_jumping2 = True
            position_joueur2_y = 350 - jump2
        if is_jumping2:
            next_y = position_joueur2_y + 5
            if collision_hauteur(position_joueur2_x, next_y, LARGEUR_PERSO, 96,
                                 position_joueur1_x, position_joueur1_y, LARGEUR_PERSO, 96):
                position_joueur2_y = position_joueur1_y - 96
                is_jumping2 = False
            elif next_y < 350:
                position_joueur2_y = next_y
            else:
                position_joueur2_y = 350
                is_jumping2 = False
        if pyxel.btnp(pyxel.KEY_P) and not attaque2_active:
            attaque2_active = True
            attaque2_timer = attaque2_duree
        if attaque2_active:
            attaque2_timer -= 1
            if attaque2_timer <= 0:
                attaque2_active = False

        # Gestion PV et touches
        if attaque_active:
            attaque_x = position_joueur1_x + LARGEUR_PERSO
            attaque_y = position_joueur1_y + 20
            if not attaque1_a_touche and collision_largeur(
                attaque_x, attaque_y, attaque_portee, 50,
                position_joueur2_x, position_joueur2_y, LARGEUR_PERSO, 96):
                pv_joueur2 -= 1
                attaque1_a_touche = True
        else:
            attaque1_a_touche = False

        if attaque2_active:
            attaque2_x = position_joueur2_x - attaque2_portee
            attaque2_y = position_joueur2_y + 20
            if not attaque2_a_touche and collision_largeur(
                attaque2_x, attaque2_y, attaque2_portee, 50,
                position_joueur1_x, position_joueur1_y, LARGEUR_PERSO, 96):
                pv_joueur1 -= 1
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
        if pv_joueur1 > 0 and pv_joueur2 > 0:
            pyxel.cls(1)
            # Joueur 1
            pyxel.rect(position_joueur1_x, position_joueur1_y, LARGEUR_PERSO, 96, 10)
            if attaque_active:
                pyxel.rect(position_joueur1_x + LARGEUR_PERSO, position_joueur1_y + 20, attaque_portee, 50, 8)
            # Joueur 2
            pyxel.rect(position_joueur2_x, position_joueur2_y, LARGEUR_PERSO, 96, 11)
            if attaque2_active:
                pyxel.rect(position_joueur2_x - attaque2_portee, position_joueur2_y + 20, attaque2_portee, 50, 3)
            # PV
            pyxel.rect(20, 20, pv_joueur1 * 10, 10, 8)
            pyxel.text(20, 10, f"J1 PV: {pv_joueur1}", 7)
            pyxel.rect(WIDTH-20-pv_joueur2*10, 20, pv_joueur2 * 10, 10, 3)
            pyxel.text(WIDTH-120, 10, f"J2 PV: {pv_joueur2}", 7)
        else:
            pyxel.cls(0)
            pyxel.text(300, 200, "GAME OVER", 7)
            if pv_joueur1 <= 0:
                pyxel.text(300, 250, "J2 a gagné", 7)
            else:
                pyxel.text(300, 250, "J1 a gagné", 7)

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
