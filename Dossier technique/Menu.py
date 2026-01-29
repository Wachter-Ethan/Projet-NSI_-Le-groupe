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


def draw_big_text(x, y, text, col):
    """Dessine le texte en double taille (2x)."""
    for i, c in enumerate(text):
        cx = x + i * 8
        for dy in [0, 7]:
            for oy in [0, 1]:
                for ox in [0, 1]:
                    pyxel.text(cx + ox, y + dy + oy, c, col)


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


# -----------------------------
# Update
# -----------------------------
def update():
    global current_option, page
    global char_index_p1, char_index_p2, selection_step

    # ---- Menu ----
    if page == PAGE_MENU:
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_L):
            current_option = (current_option + 1) % len(options)
        elif pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_O):
            current_option = (current_option - 1) % len(options)

        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_E):
            if options[current_option] == "Jouer":
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
        pass

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
        pass
    
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
pyxel.load("Sprite-Robot.pyxres")
pyxel.run(update, draw)




