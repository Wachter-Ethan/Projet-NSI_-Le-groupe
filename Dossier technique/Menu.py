import pyxel

# -----------------------------
# Constantes et pages
# -----------------------------
WIDTH = 700
HEIGHT = 500

PAGE_MENU = 0
PAGE_CHARACTER_SELECT = 1   # AJOUT
PAGE_GAME = 2
PAGE_OPTIONS = 3

page = PAGE_MENU

# -----------------------------
# Menu
# -----------------------------
current_option = 0
options = ["Jouer", "Options", "Quitter"]

# -----------------------------
# Nouveau : Sélection des personnages
# -----------------------------
characters = ["Robot", "Plante"]
char_index_p1 = 0
char_index_p2 = 0
selection_step = 0  # 0 = Joueur 1 choisit, 1 = Joueur 2 choisit


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
    pyxel.cls(11)

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

        if selection_step == 0:
            pyxel.text(260, 120, "Joueur 1 choisit :", 0)
            pyxel.text(300, 200, characters[char_index_p1], 10)
            pyxel.text(200, 350, "<- Q / D ->   Valider : E", 0)

        else:
            pyxel.text(260, 120, "Joueur 2 choisit :", 0)
            pyxel.text(300, 200, characters[char_index_p2], 8)
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
pyxel.run(update, draw)


