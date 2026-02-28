import pyxel

# -----------------------------
# Constantes et pages
# -----------------------------
WIDTH = 600
HEIGHT = 400

PAGE_MENU = 0
PAGE_CHARACTER_SELECT = 1   # AJOUT
PAGE_GAME = 2
PAGE_OPTIONS = 3

page = PAGE_MENU

PERSO_W = 41
PERSO_H = 80

# -----------------------------
# Menu
# -----------------------------
current_option = 0
options = ["Jouer", "Options", "Quitter"]

# -----------------------------
# Nouveau : Sélection des personnages
# -----------------------------
characters = ["Sprite-Robot.pyxres", "Plante"]
# Affichage en jeu : "sprite" = blt(img,u,v,colkey), "rect" = couleur
CHAR_DRAW = [
    ("sprite", 0, 6, 28, 0),   # Robot
    ("rect", 10),               # Plante
]
CHAR_NAMES = ["Robot", "Plante"]  # noms courts pour l'UI
char_index_p1 = 0
char_index_p2 = 0
selection_step = 0  # 0 = Joueur 1 choisit, 1 = Joueur 2 choisit



def draw_centered_big_text(y, text, col):
    """Dessine le texte en double taille, centré horizontalement."""
    w = len(text) * 8
    draw_big_text(WIDTH // 2 - w // 2, y, text, col)


def draw_char_preview(idx, x, y, flip_h=False):
    """Dessine l'aperçu du personnage (comme en jeu). flip_h=True pour J1 (face à droite)."""
    info = CHAR_DRAW[idx]
    if info[0] == "sprite":
        _, img, u, v, colkey = info
        if flip_h:
            pyxel.blt(x + PERSO_W, y, img, u, v, -PERSO_W, PERSO_H, colkey)
        else:
            pyxel.blt(x, y, img, u, v, PERSO_W, PERSO_H, colkey)
    else:
        pyxel.rect(x, y, PERSO_W, PERSO_H, info[1])


# JEU

# ======================
# CONSTANTES D'ÉCHELLE
# ======================
WINDOW_W = 600
WINDOW_H = 400

PERSO_W = 41
PERSO_H = 80

SOL_Y = WINDOW_H - PERSO_H - 10

VITESSE_X = 6
VITESSE_Y = 5

# KNOCKBACK
KNOCKBACK = 70


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

hit_count_1 = 0          # nombre de coups portés
can_ultimate_1 = False  # est-ce que l'ultimate est prête

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

hit_count_2 = 0          # nombre de coups portés
can_ultimate_2 = False  # est-ce que l'ultimate est prête

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

# Ultimate joueur 1
ultimate_1_x = 0
ultimate_1_y = 0
direction_ultimate_1 = 1  # 1 = droite, -1 = gauche
ultimate_speed = 5             # rapide → difficile à esquiver
ultimate_damage = 3
ultimate_width = 50             # gros projectile
ultimate_height = 50
active_ultimate_1 = False

# Ultimate joueur 2
ultimate_2_x = 0
ultimate_2_y = 0
direction_ultimate_2 = -1  # 1 = droite, -1 = gauche
active_ultimate_2 = False

# Collision ulrimte
def rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )


# -----------------------------
# Update
# -----------------------------
def update():
    global current_option, page
    global char_index_p1, char_index_p2, selection_step
    global pv_joueur1, pv_joueur2, position_joueur1_x, position_joueur2_x

    # ---- Menu ----
    if page == PAGE_MENU:
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_L):
            current_option = (current_option + 1) % len(options)
        elif pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_O):
            current_option = (current_option - 1) % len(options)

        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_E):
            if options[current_option] == "Jouer":
                pv_joueur1 = 15
                pv_joueur2 = 15
                position_joueur1_x = 60
                position_joueur2_x = 500
                page = PAGE_CHARACTER_SELECT
                selection_step = 0
            elif options[current_option] == "Options":
                page = PAGE_OPTIONS
            elif options[current_option] == "Quitter":
                pyxel.quit()

    # ---- Sélection des personnages ----
    elif page == PAGE_CHARACTER_SELECT:
        # Joueur 1 choisit
        if selection_step == 0:
            if pyxel.btnp(pyxel.KEY_Q):
                char_index_p1 = (char_index_p1 - 1) % len(characters)
            if pyxel.btnp(pyxel.KEY_D):
                char_index_p1 = (char_index_p1 + 1) % len(characters)
            if pyxel.btnp(pyxel.KEY_E):
                selection_step = 1  # Passe à J2

        # Joueur 2 choisit
        elif selection_step == 1:
            if pyxel.btnp(pyxel.KEY_K):
                char_index_p2 = (char_index_p2 - 1) % len(characters)
            if pyxel.btnp(pyxel.KEY_M):
                char_index_p2 = (char_index_p2 + 1) % len(characters)
            if pyxel.btnp(pyxel.KEY_P):
                page = PAGE_GAME  # Lance le jeu


    # ---- Jeu ----
    elif page == PAGE_GAME:
        global position_joueur1_y, is_jumping
        global position_joueur2_y, is_jumping2
        global attaque_active, attaque_timer, attaque2_active, attaque2_timer
        global attaque1_a_touche, attaque2_a_touche
        global KNOCKBACK, VITESSE_Y, VITESSE_X, SOL_Y, PERSO_H, PERSO_W
        global ultimate_1_x, ultimate_1_y, ultimate_speed, ultimate_damage, ultimate_width, ultimate_height, active_ultimate_1
        global ultimate_2_x, ultimate_2_y, active_ultimate_2
        global hit_count_1, hit_count_2, can_ultimate_1, can_ultimate_2

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
            if ny < SOL_Y:
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
            if ny < SOL_Y:
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
            if not attaque1_a_touche and collision_largeur(position_joueur1_x + PERSO_W, position_joueur1_y + 20, attaque_portee, 50, position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
                pv_joueur2 -= 1
                hit_count_1 += 1
                
                # Knockback vers la droite
                position_joueur2_x += KNOCKBACK
                if position_joueur2_x + PERSO_W > WINDOW_W:
                    position_joueur2_x = WINDOW_W - PERSO_W
                
                position_joueur1_x -= KNOCKBACK
                if position_joueur1_x < 0:
                    position_joueur1_x = 0
                    
                attaque1_a_touche = True
        else:
            attaque1_a_touche = False

        if attaque2_active:
            if not attaque2_a_touche and collision_largeur(position_joueur2_x - attaque2_portee, position_joueur2_y + 20, attaque2_portee, 50, position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
                pv_joueur1 -= 1
                
                hit_count_2 += 1
                
                # Knockback vers la gauche
                position_joueur1_x -= KNOCKBACK
                if position_joueur1_x < 0:
                    position_joueur1_x = 0
                
                position_joueur2_x += KNOCKBACK
                if position_joueur2_x + PERSO_W > WINDOW_W:
                    position_joueur2_x = WINDOW_W - PERSO_W
                
                attaque2_a_touche = True
        else:
            attaque2_a_touche = False
            
        if hit_count_1 >= 5:
            can_ultimate_1 = True
        if hit_count_2 >= 5:
            can_ultimate_2 = True
        
        # Utilisation ultimate
        if pyxel.btnp(pyxel.KEY_A) and can_ultimate_1:
            active_ultimate_1 = True
            ultimate_1_x = position_joueur1_x
            ultimate_1_y = position_joueur1_y
            hit_count_1 = 0
            can_ultimate_1 = False
        if pyxel.btnp(pyxel.KEY_I) and can_ultimate_2:
            active_ultimate_2 = True
            ultimate_2_x = position_joueur2_x
            ultimate_2_y = position_joueur2_y
            hit_count_2 = 0
            can_ultimate_2 = False
        
        if active_ultimate_1:
            ultimate_1_x += ultimate_speed * direction_ultimate_1
            if ultimate_1_x < - ultimate_width or ultimate_1_x > pyxel.width:
                active_ultimate_1 = False
            if rect_collision(ultimate_1_x, ultimate_1_y, ultimate_width, ultimate_height, position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
                pv_joueur2 -= ultimate_damage
                active_ultimate_1 = False
        
        if active_ultimate_2:
            ultimate_2_x += ultimate_speed * direction_ultimate_2
            if ultimate_2_x < - ultimate_width or ultimate_2_x > pyxel.width:
                active_ultimate_2 = False
            if rect_collision(ultimate_2_x, ultimate_2_y, ultimate_width, ultimate_height, position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
                pv_joueur1 -= ultimate_damage
                active_ultimate_2 = False
            
        # ---- Options ----
    elif page == PAGE_OPTIONS:
        if pyxel.btnp(pyxel.KEY_TAB):
            page = PAGE_MENU


    # ---- Options ----
    elif page == PAGE_OPTIONS:
        if pyxel.btnp(pyxel.KEY_TAB):
            page = PAGE_MENU

# -----------------------------
# Draw
# -----------------------------
def draw():
    global page
    pyxel.cls(11)

    def draw_centered_text(y, text, color):
        # Police Pyxel: 4px par caractère
        x = WIDTH // 2 - (len(text) * 4) // 2
        pyxel.text(x, y, text, color)

    # ---- MENU ----
    if page == PAGE_MENU:
        pyxel.text(WIDTH//2 - 70, 50, "PLANT FIGHTER", pyxel.COLOR_BLACK)
        for i, option in enumerate(options):
            color = pyxel.COLOR_GREEN if i == current_option else pyxel.COLOR_BLACK
            pyxel.text(WIDTH//2 - 40, 150 + i*50, option, color)

    # ---- SELECTION DE PERSONNAGES ----
    elif page == PAGE_CHARACTER_SELECT:
        pyxel.cls(6)
        pyxel.text(200, 40, "SELECTION DES PERSONNAGES", 0)

        prev_x = WIDTH // 2 - PERSO_W // 2
        prev_y = 160

        if selection_step == 0:
            pyxel.text(260, 120, "Joueur 1 choisit :", 0)
            draw_char_preview(char_index_p1, prev_x, prev_y)
            draw_centered_text(260, CHAR_NAMES[char_index_p1], 10)
            pyxel.text(200, 350, "<- Q / D ->   Valider : E", 0)
        else:
            pyxel.text(260, 120, "Joueur 2 choisit :", 0)
            draw_char_preview(char_index_p2, prev_x, prev_y)
            draw_centered_text(260, CHAR_NAMES[char_index_p2], 8)
            pyxel.text(200, 350, "<- K / M ->   Valider : P", 0)

    # ---- JEU ----
    elif page == PAGE_GAME:
        pyxel.cls(1)

        if pv_joueur1 > 0 and pv_joueur2 > 0:
        # Joueurs
            # Joueurs : affichage selon le personnage choisi en sélection
            # J1 à gauche → tourné vers la droite (flip si Robot)
            draw_char_preview(char_index_p1, position_joueur1_x - PERSO_W, position_joueur1_y, flip_h=True)
            draw_char_preview(char_index_p2, position_joueur2_x, position_joueur2_y)

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

            if active_ultimate_1:
                pyxel.circ(ultimate_1_x + ultimate_width // 2, ultimate_1_y + ultimate_height // 2, ultimate_width // 2, 9)

            if can_ultimate_1:
                pyxel.text(20, 50, "ULTIMATE 1 READY", 10)
                
            if active_ultimate_2:
                pyxel.circ(ultimate_2_x + ultimate_width // 2, ultimate_2_y + ultimate_height // 2, ultimate_width // 2, 9)

            if can_ultimate_2:
                pyxel.text(WINDOW_W - 90, 50, "ULTIMATE 2 READY", 10)

        elif pv_joueur2 <= 0:
            pyxel.cls(0)
            go_y2 = HEIGHT // 2 - 30
            go_y1, go_y3 = go_y2 - 60, go_y2 + 60
            draw_centered_text(go_y1, 'GAME OVER', 7)
            draw_centered_text(go_y2, 'J1 a gagné', 7)
            draw_centered_text(go_y3, 'TAB: retour au menu', 7)
            if pyxel.btnp(pyxel.KEY_TAB):
                page = PAGE_MENU
        elif pv_joueur1 <= 0:
            pyxel.cls(0)
            go_y2 = HEIGHT // 2 - 30
            go_y1, go_y3 = go_y2 - 60, go_y2 + 60
            draw_centered_text(go_y1, 'GAME OVER', 7)
            draw_centered_text(go_y2, 'J2 a gagné', 7)
            draw_centered_text(go_y3, 'TAB: retour au menu', 7)
            if pyxel.btnp(pyxel.KEY_TAB):
                page = PAGE_MENU
    
    # ---- OPTIONS ----
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
# Lien avec les autres fichiers
pyxel.load("Sprite-Lancelot.pyxres")
pyxel.run(update, draw)





