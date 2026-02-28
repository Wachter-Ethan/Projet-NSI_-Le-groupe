import pyxel

# -----------------------------
# Constantes et pages
# -----------------------------
WIDTH = 550
HEIGHT = 275

PAGE_CHARGEMENT = 0
PAGE_MENU = 1
PAGE_CHARACTER_SELECT = 2  # AJOUT
PAGE_MAP_SELECT = 3  # AJOUT: Sélection de map
PAGE_GAME = 4
PAGE_OPTIONS = 5

page = PAGE_CHARGEMENT


COOLDOWN_MAX = 30  # 30 frames = 1 seconde
cooldown_ult = 60

# -----------------------------
# Chargement
# -----------------------------
loading_progress = 0        # de 0 à 100
loading_speed = 0.5         # vitesse de chargement
loading_dots_timer = 0

# -----------------------------
# Menu
# -----------------------------
current_option = 0
options = ["Jouer", "Options", "Quitter"]

# -----------------------------
# Nouveau : Sélection des personnages
# -----------------------------
characters = ["Lancelot", "Herbal Giant"]
# Affichage en jeu : "sprite" = blt(img,u,v,colkey), "rect" = couleur
CHAR_DRAW = [
    ("sprite", 0, 6, 14, 0),   # Robot
    ("sprite", 1, 0, -14, 1),    # Herbal Giant (image 1, position 0,0, size 16x16, transparent color 1)
]
# Sprite d'ultimate pour Herbal Giant
HERBAL_GIANT_ULTIMATE = ("sprite", 1, 192, 88, 1)  # image 1, u=192, v=88, transparent color 1
# Sprite d'ultimate flippé pour le joueur 1
HERBAL_GIANT_ULTIMATE_FLIPPED = ("sprite", 1, 180, 88, 1)  # Coordonnées ajustées pour le flip (u=180, v=88)
# Sprite d'ultimate pour Lancelot
LANCELOT_ULTIMATE = ("sprite", 0, 169, 161, 0)  # image 1, u=169, v=161, transparent color 1
# Sprite d'attaque pour Herbal Giant
HERBAL_GIANT_ATTACK = ("sprite", 1, 168, 0, 1)  # image 1, u=168, v=0, transparent color 1
# Sprite d'attaque pour Lancelot
LANCELOT_ATTACK = ("sprite", 0, 169, 19, 0)  # image 0, u=179, v=19, transparent color 0
# Sprite de marche pour Lancelot
LANCELOT_WALK = ("sprite", 0, 7, 160, 0)  # image 0, u=7, v=160, transparent color 0
# Sprite de recul pour Lancelot
LANCELOT_BACK = ("sprite", 0, 56, 14, 0)  # image 0, u=56, v=14, transparent color 0
# Sprite de déplacement pour Herbal Giant
HERBAL_GIANT_WALK = ("sprite", 1, 0, 177, 1)  # image 1, u=0, v=177, transparent color 1
# Sprite de recul pour Herbal Giant
HERBAL_GIANT_BACK = ("sprite", 1, 152, 176, 1)  # image 1, u=152, v=176, transparent color 1
CHAR_NAMES = ["Lancelot", "Herbal Giant"]  # noms courts pour l'UI
char_index_p1 = 0
char_index_p2 = 0
selection_step = 0  # 0 = Joueur 1 choisit, 1 = Joueur 2 choisit

# -----------------------------
# Sélection de map
# -----------------------------
map_selection = 0  # Index de la map sélectionnée (0 = aléatoire, 1-16 = couleurs)
selected_map_color = 1  # Couleur de fond actuelle pour le jeu
MAP_COLORS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # 16 couleurs Pyxel
map_selection_p1 = 0  # Sélection de map du joueur 1
map_selection_p2 = 0  # Sélection de map du joueur 2
map_selection_step = 0  # 0 = J1 choisit, 1 = J2 choisit, 2 = sélection aléatoire et lancement
p1_validated = False  # Joueur 1 a validé son choix
p2_validated = False  # Joueur 2 a validé son choix



def setup_music():
    # ============================================================
    #  MUSIQUE 1 pour le menu(sons 16,17,18)

    pyxel.sound(16).set(
        notes="A3 R A3 R A3 G3 A3 R F3 R F3 R F3 E3 F3 R E3 R E3 R E3 D3 E3 R D3 E3 D3 C3 D3 R R R A3 R A3 R A3 G3 A3 R C4 R C4 R B3 R A3 R G3 R G3 F3 E3 D3 E3 R A3 R R R R R R R",
        tones="S",
        volumes="7 0 7 0 7 6 7 0 7 0 7 0 7 6 7 0 7 0 7 0 7 6 7 0 6 6 6 5 6 0 0 0 7 0 7 0 7 6 7 0 7 0 7 0 7 0 7 0 7 0 6 6 6 5 6 0 7 0 0 0 0 0 0 0",
        effects="N N N N N N S N N N N N N N S N N N N N N N S N N N N N S N N N N N N N N N S N N N N N N N N N N N N N N N S N F N N N N N N N",
        speed=14
    )

    pyxel.sound(17).set(
        notes="A2 R E3 R A2 R E3 R F2 R C3 R F2 R C3 R E2 R B2 R E2 R B2 R D2 E2 F2 R E2 R R R A2 R E3 R A2 R E3 R F2 R C3 R F2 R C3 R E2 R B2 R G2 R A2 R A2 R R R R R R R",
        tones="P",
        volumes="5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 5 5 0 5 0 0 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 0 0 0 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N F N N N N N N N",
        speed=14
    )

    pyxel.sound(18).set(
        notes="A1 R R A1 R A1 R R F1 R R F1 R F1 R R E1 R R E1 R E1 R R D1 R E1 R F1 R R R A1 R R A1 R A1 R R F1 R R F1 R F1 R R E1 R R E1 R G1 R R A1 R R R R R R R",
        tones="T",
        volumes="7 0 0 6 0 7 0 0 7 0 0 6 0 7 0 0 7 0 0 6 0 7 0 0 7 0 7 0 7 0 0 0 7 0 0 6 0 7 0 0 7 0 0 6 0 7 0 0 7 0 0 6 0 7 0 0 7 0 0 0 0 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N F N N N N N N N",
        speed=14
    )

    pyxel.music(1).set([16], [17], [18], [])

    # ============================================================
    #  MUSIQUE 2 jeu (sons 0-14)

    # debut
    pyxel.sound(0).set(
        notes="R R R R R R R R E2 R R R G2 R R R A2 R G2 R E2 R R R B2 R B2 R B2 A2 G2 R E2 R R R G2 R A2 R B2 R A2 G2 E2 R R R D3 R C3 R B2 R A2 R G2 A2 B2 R E3 R R R",
        tones="T",
        volumes="0 0 0 0 0 0 0 0 4 0 0 0 5 0 0 0 6 0 5 0 5 0 0 0 7 0 7 0 7 6 5 0 5 0 0 0 6 0 6 0 7 0 6 6 5 0 0 0 7 0 7 0 7 0 6 0 6 6 7 0 7 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N S N N N N N N N N N S N N N N N N N N N N N N N S N N N N N N N N N N N N N F N N N N N",
        speed=15
    )
    pyxel.sound(1).set(
        notes="R R R R R R R R E1 R E1 R E1 R E1 R E1 R E1 R E1 R R R G1 R G1 R A1 R B1 R E1 R E1 R E1 R E1 R G1 R A1 R G1 E1 R R A1 R A1 R A1 G1 A1 R B1 R B1 R E2 R R R",
        tones="P",
        volumes="0 0 0 0 0 0 0 0 4 0 4 0 4 0 4 0 5 0 5 0 5 0 0 0 5 0 5 0 6 0 6 0 5 0 5 0 5 0 5 0 5 0 6 0 5 5 0 0 6 0 6 0 6 5 6 0 7 0 7 0 7 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )
    pyxel.sound(2).set(
        notes="R R R R R R R R E1 R R R E1 R R R E1 R R E1 R R E1 R G1 R R G1 R R B1 R E1 R R R E1 R R R E1 R R E1 G1 R R R A1 R R A1 R R A1 R B1 R R B1 R R E2 R",
        tones="T",
        volumes="0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 6 0 0 6 0 0 6 0 6 0 0 6 0 0 7 0 6 0 0 0 6 0 0 0 7 0 0 7 7 0 0 0 7 0 0 7 0 0 7 0 7 0 0 7 0 0 7 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )

    # apres le debut  
    pyxel.sound(4).set(
        notes="E3 R E3 R G3 R E3 R D3 R C3 R B2 R R R E3 R E3 R G3 R A3 R B3 R R R B3 R R R E3 R E3 R G3 R E3 R D3 R C3 B2 A2 R R R C3 R D3 R E3 R G3 R E3 D3 C3 R B2 R R R",
        tones="T",
        volumes="7 0 7 0 7 0 7 0 7 0 7 0 7 0 0 0 7 0 7 0 7 0 7 0 7 0 0 0 7 0 0 0 7 0 7 0 7 0 7 0 7 7 7 0 0 0 7 0 7 0 7 0 7 7 7 0 7 0 0 0",
        effects="N N N N N N S N N N N N F N N N N N N N N N S N F N N N N N N N N N N N N N S N N N N N F N N N N N N N N N N N N N F N F N N N",
        speed=15
    )
    pyxel.sound(5).set(
        notes="E2 G2 E2 G2 E2 G2 E2 G2 D2 F2 D2 F2 D2 F2 D2 F2 E2 G2 E2 G2 E2 G2 A2 G2 B2 R B2 R B2 R B2 R E2 G2 E2 G2 E2 G2 E2 G2 D2 F2 D2 F2 C2 E2 C2 E2 C2 E2 D2 F2 E2 G2 E2 G2 E2 D2 C2 B1 B1 R R R",
        tones="P",
        volumes="5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 6 4 6 0 6 0 6 0 6 0 5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 5 4 6 4 6 4 6 4 6 5 5 5 5 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N F N N N",
        speed=15
    )
    pyxel.sound(6).set(
        notes="E1 R E1 R E1 E1 R R D1 R D1 R D1 D1 R R E1 R E1 R E1 E1 A1 R B1 R R B1 R R B1 R E1 R E1 R E1 E1 R R D1 R D1 R C1 C1 R R C1 R D1 R E1 R G1 R E1 D1 C1 R B0 R R R",
        tones="T",
        volumes="7 0 7 0 7 7 0 0 7 0 7 0 7 7 0 0 7 0 7 0 7 7 7 0 7 0 0 7 0 0 7 0 7 0 7 0 7 7 0 0 7 0 7 0 7 7 0 0 7 0 7 0 7 0 7 0 7 7 7 0 7 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )

    # apres apres le debut
    pyxel.sound(8).set(
        notes="B2 R A2 R G2 R A2 R B2 R R R B2 R R R C3 R B2 R A2 R G2 R A2 R R R A2 G2 R R F2 R G2 R A2 R B2 R C3 R B2 A2 G2 R R R D3 R E3 R D3 C3 B2 R A2 B2 C3 R B2 R R R",
        tones="T",
        volumes="7 0 7 0 7 0 7 0 7 0 0 0 7 0 0 0 7 0 7 0 7 0 7 0 7 0 0 0 6 6 0 0 7 0 7 0 7 0 7 0 7 0 7 7 7 0 0 0 7 0 7 0 7 7 7 0 7 7 7 0 7 0 0 0",
        effects="N N N N N N N N F N N N N N N N N N N N N N N N F N N N N N N N N N N N N N N N N N N N F N N N N N N N N N S N N N F N F N N N",
        speed=15
    )
    pyxel.sound(9).set(
        notes="B1 R R B1 R R B1 R B1 R R R A1 R R R C2 R R C2 R R C2 R A1 R R R A1 R R R F1 R G1 R A1 R B1 R C2 B1 A1 G1 R R R R D2 R D2 R D2 C2 B1 R B1 A1 G1 R B1 R R R",
        tones="P",
        volumes="6 0 0 6 0 0 6 0 6 0 0 0 6 0 0 0 6 0 0 6 0 0 6 0 6 0 0 0 6 0 0 0 6 0 6 0 6 0 7 0 7 6 6 5 0 0 0 0 7 0 7 0 7 6 6 0 6 5 5 0 6 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )
    pyxel.sound(10).set(
        notes="B0 R R B0 R B0 R R B0 R R R A0 R R R C1 R R C1 R C1 R R A0 R R R A0 R A0 R F0 R G0 R A0 R B0 R C1 R B0 R A0 R R R D1 R D1 R D1 R C1 R B0 R A0 R B0 R R R",
        tones="T",
        volumes="7 0 0 7 0 7 0 0 7 0 0 0 7 0 0 0 7 0 0 7 0 7 0 0 7 0 0 0 7 0 7 0 7 0 7 0 7 0 7 0 7 0 7 0 7 0 0 0 7 0 7 0 7 0 7 0 7 0 7 0 7 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )

    # finito
    pyxel.sound(12).set(
        notes="E3 G3 E3 G3 B3 G3 E3 R D3 F3 D3 F3 A3 F3 D3 R E3 G3 E3 G3 B3 A3 G3 R A3 R B3 R E3 R R R E3 G3 E3 G3 B3 G3 E3 R D3 F3 D3 C3 B2 A2 G2 R A2 B2 C3 D3 E3 F3 G3 A3 B3 R E3 R E3 R R R",
        tones="T",
        volumes="7 6 7 6 7 6 7 0 7 6 7 6 7 6 7 0 7 6 7 6 7 6 7 0 7 0 7 0 7 0 0 0 7 6 7 6 7 6 7 0 7 6 7 7 7 6 6 0 6 6 7 7 7 7 7 7 7 0 7 0 7 0 0 0",
        effects="N N N N N N F N N N N N N N F N N N N N N N F N F N S N F N N N N N N N N N F N N N N N N N N N N N N N N N N N F N S N F N N N",
        speed=15
    )
    pyxel.sound(13).set(
        notes="E2 G2 B2 E2 G2 B2 E2 G2 D2 F2 A2 D2 F2 A2 D2 F2 E2 G2 B2 E2 G2 B2 A2 G2 B2 G2 E2 G2 B2 E3 R R E2 G2 B2 E2 G2 B2 E2 G2 D2 F2 A2 D2 C2 E2 G2 B2 C2 E2 G2 B2 D2 F2 A2 C3 B2 G2 E2 G2 B2 E3 R R",
        tones="P",
        volumes="6 5 5 6 5 5 6 5 6 5 5 6 5 5 6 5 6 5 5 6 5 5 6 5 7 5 5 5 7 7 0 0 6 5 5 6 5 5 6 5 6 5 5 6 6 5 5 5 6 5 5 5 6 5 5 5 7 5 5 5 7 7 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )
    pyxel.sound(14).set(
        notes="E1 E2 R E1 E2 R E1 R D1 D2 R D1 D2 R D1 R E1 E2 R E1 E2 R A1 R B1 R B1 B2 E2 R R R E1 E2 R E1 E2 R E1 R D1 D2 R C1 C2 R C1 R C1 D1 E1 F1 G1 A1 B1 C2 B1 R E1 R E2 R R R",
        tones="T",
        volumes="7 6 0 7 6 0 7 0 7 6 0 7 6 0 7 0 7 6 0 7 6 0 7 0 7 0 7 6 7 0 0 0 7 6 0 7 6 0 7 0 7 6 0 7 6 0 7 0 7 7 7 7 7 7 7 7 7 0 7 0 7 0 0 0",
        effects="N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N N",
        speed=15
    )

    pyxel.music(0).set(
        [0, 4, 8, 12],
        [1, 5, 9, 13],
        [2, 6, 10, 14],
        [],
    )


def draw_centered_big_text(y, text, col):
    """Dessine le texte en double taille, centré horizontalement."""
    w = len(text) * 16  # Double taille (8 * 2)
    x = WIDTH // 2 - w // 2
    # Dessiner chaque caractère deux fois pour l'effet "big"
    for i, char in enumerate(text):
        pyxel.text(x + i * 16, y, char, col)
        pyxel.text(x + i * 16 + 1, y, char, col)  # Léger décalage pour l'effet gras


def draw_char_preview(idx, x, y, flip_h=False, is_ultimating=False, is_attacking=False, is_walking=False, is_backing=False, is_hit=False):
    """Dessine l'aperçu du personnage (comme en jeu). flip_h=True pour J1 (face à droite)."""
    # Si le personnage est en train d'utiliser son ultimate
    if is_ultimating:
        if CHAR_NAMES[idx] == "Herbal Giant":
            # Choisir le sprite selon si c'est le joueur 1 (flippé) ou joueur 2 (normal)
            if flip_h:
                info = HERBAL_GIANT_ULTIMATE_FLIPPED  # Joueur 1 : sprite flippé
                should_flip = True  # Forcer le flip visuel
            else:
                info = HERBAL_GIANT_ULTIMATE  # Joueur 2 : sprite normal
                should_flip = False  # Pas de flip
            
            # Utiliser les dimensions visuelles pour l'ultimate
            visual_w = VISUAL_W
            visual_h = VISUAL_H - 3
            # Centrer le sprite plus grand sur la hitbox
            offset_x = (PERSO_W - visual_w) // 2
            offset_y = (PERSO_H - visual_h) // 2
        elif CHAR_NAMES[idx] == "Lancelot":
            info = LANCELOT_ULTIMATE
            should_flip = flip_h
            # Utiliser les dimensions standard pour l'ultimate de Lancelot
            visual_w = PERSO_W
            visual_h = PERSO_H
            offset_x = 0
            offset_y = 0
    # Si le personnage est en train d'attaquer
    elif is_attacking:
        if CHAR_NAMES[idx] == "Herbal Giant":
            info = HERBAL_GIANT_ATTACK
            should_flip = flip_h
            # Dimensions plus grandes pour l'attaque (bras allongé)
            visual_w = PERSO_W + attaque_portee  # Hitbox fusionnée
            visual_h = PERSO_H - 5
            # Positionner le sprite pour qu'il couvre la zone d'attaque
            if flip_h:
                offset_x = -attaque_portee  # Joueur 1 : attaque vers la gauche
            else:
                offset_x = 0 - attaque_portee  # Joueur 2 : attaque vers la droite (pas de décalage)
            offset_y = 14  # Ajuster pour aligner avec la position d'attaque
        elif CHAR_NAMES[idx] == "Lancelot":
            info = LANCELOT_ATTACK
            should_flip = flip_h
            # Dimensions plus grandes pour l'attaque (bras allongé comme Herbal Giant)
            visual_w = PERSO_W + attaque_portee  # Hitbox fusionnée
            visual_h = PERSO_H - 5
            # Positionner le sprite pour qu'il couvre la zone d'attaque
            if flip_h:
                offset_x = -attaque_portee
                offset_y = 4  # Joueur 1 : attaque vers la gauche
            else:
                offset_x = -50  # Joueur 2 : attaque vers la droite avec 10px de décalage vers la gauche
                offset_y = 4  # Ajuster pour aligner avec la position d'attaque (14 - 10 = 4)
    # Si le personnage est en train de marcher
    elif is_walking:
        if CHAR_NAMES[idx] == "Herbal Giant":
            info = HERBAL_GIANT_WALK
            should_flip = flip_h
            # Utiliser les dimensions standard pour le déplacement
            visual_w = PERSO_W + 20
            visual_h = PERSO_H
            offset_x = 0 if not flip_h else -20  # Joueur 2: 0, Joueur 1: 0
            offset_y = 15
        elif CHAR_NAMES[idx] == "Lancelot":
            info = LANCELOT_WALK
            should_flip = flip_h
            # Utiliser les dimensions standard pour la marche de Lancelot
            visual_w = PERSO_W + 20
            visual_h = PERSO_H
            offset_x = 0 if not flip_h else -40  # Joueur 2: 0, Joueur 1: 0
            offset_y = 2
    # Si le personnage est en train de reculer
    elif is_backing:
        if CHAR_NAMES[idx] == "Herbal Giant":
            info = HERBAL_GIANT_BACK
            should_flip = flip_h
            # Utiliser les dimensions standard pour le recul
            visual_w = PERSO_W + 20
            visual_h = PERSO_H
            offset_x = 0 if not flip_h else -35  # Joueur 2: 0, Joueur 1: 0
            offset_y = 15
        elif CHAR_NAMES[idx] == "Lancelot":
            info = LANCELOT_BACK
            should_flip = flip_h
            # Utiliser les dimensions standard pour le recul de Lancelot
            visual_w = PERSO_W + 20
            visual_h = PERSO_H
            offset_x = 0 if not flip_h else -35  # Joueur 2: 0, Joueur 1: 0
            offset_y = 0  
    else:
        info = CHAR_DRAW[idx]
        should_flip = flip_h  # Flip normal pour les sprites standards
        # Utiliser les dimensions standard pour les sprites normaux
        visual_w = PERSO_W
        visual_h = PERSO_H
        offset_x = 0
        offset_y = 0
    
    if info[0] == "sprite":
        _, img, u, v, colkey = info
        draw_x = x + offset_x
        draw_y = y + offset_y
        
        # Affichage normal du sprite (plus de flash blanc)
        if should_flip:
            # Appliquer le flip visuel
            pyxel.blt(draw_x + visual_w, draw_y, img, u, v, -visual_w, visual_h, colkey)
        else:
            # Pas de flip
            pyxel.blt(draw_x, draw_y, img, u, v, visual_w, visual_h, colkey)
    else:
        # Rectangle normal pour les hitbox
        pyxel.rect(x + offset_x, y + offset_y, visual_w, visual_h, info[1])


# JEU

# ======================
# CONSTANTES D'ÉCHELLE
# ======================
WINDOW_W = 550
WINDOW_H = 275

PERSO_W = 46
PERSO_H = 100

# Dimensions visuelles des sprites (peuvent être différentes de la hitbox)
VISUAL_W = 80  # Largeur visuelle pour Herbal Giant ultimate
VISUAL_H = 90  # Hauteur visuelle pour Herbal Giant ultimate

SOL_Y = WINDOW_H - PERSO_H - 10

VITESSE_X = 4
VITESSE_Y = 5

# KNOCKBACK
KNOCKBACK = 70


# ======================
# JOUEUR 1
# ======================
position_joueur1_x = 10
position_joueur1_y = SOL_Y

# Joueur 1 - Saut amélioré avec double saut
jump_velocity = -12  # Vitesse initiale du saut (négative = vers le haut)
jump_velocity_double = -8  # Vitesse initiale du double saut (moins haut)
jump_hold_multiplier = 0.95  # Réduction de la vitesse quand on maintient la touche
min_jump_velocity = -4  # Vitesse minimale pour un petit saut
gravity = 0.6  # Force de gravité
vertical_velocity = 0  # Vitesse verticale actuelle
is_jumping = False
jump_button_held = False  # Si la touche de saut est maintenue
jump_count = 0  # Nombre de sauts effectués (0 = au sol, 1 = premier saut, 2 = double saut)
max_jumps = 2  # Nombre maximum de sauts autorisés

attaque_active = False
attaque_timer = 0
attaque_duree = 10
attaque_portee = 40

pv_joueur1 = 15
attaque1_a_touche = False

hit_count_1 = 0          # nombre de coups portés
can_ultimate_1 = False  # est-ce que l'ultimate est prête

cooldown_ult_1 = 0
charging_ult_1 = False

cooldown_1 = 0

# ======================
# JOUEUR 2
# ======================
position_joueur2_x = 500
position_joueur2_y = SOL_Y

# Joueur 2 - Saut amélioré avec double saut
jump_velocity2 = -12  # Vitesse initiale du saut (négative = vers le haut)
jump_velocity_double2 = -8  # Vitesse initiale du double saut (moins haut)
vertical_velocity2 = 0  # Vitesse verticale actuelle
is_jumping2 = False
jump_button_held2 = False  # Si la touche de saut est maintenue
jump_count2 = 0  # Nombre de sauts effectués (0 = au sol, 1 = premier saut, 2 = double saut)
max_jumps2 = 2  # Nombre maximum de sauts autorisés

attaque2_active = False
attaque2_timer = 0
attaque2_duree = 10
attaque2_portee = 40

pv_joueur2 = 15  
attaque2_a_touche = False

hit_count_2 = 0          # nombre de coups portés
can_ultimate_2 = False  # est-ce que l'ultimate est prête

cooldown_ult_2 = 0
charging_ult_2 = False

cooldown_2 = 0

# Variables pour suivre l'état de marche
j1_was_walking = False
j2_was_walking = False

# Variables pour les effets de gouttes de sang quand on prend un coup
# Système de particules pour les gouttes de sang
blood_particles = []  # Liste des particules de sang

# Système de particules pour les éclaboussures de sang décoratives (écran de victoire)
victory_blood_splashes = []  # Liste des éclaboussures décoratives

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
ultimate_speed = 6             # rapide → difficile à esquiver
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
# Système de particules de sang
# -----------------------------
def create_blood_particles(x, y, count, character_index=None):
    """Crée des particules de sang à la position spécifiée"""
    global blood_particles
    import random
    
    # Déterminer la couleur en fonction du personnage
    if character_index is not None:
        if CHAR_NAMES[character_index] == "Lancelot":
            blood_color = 10  # Jaune pour Lancelot
        elif CHAR_NAMES[character_index] == "Herbal Giant":
            blood_color = 3   # Vert pour Herbal Giant
        else:
            blood_color = 10  # Jaune par défaut pour les autres
    else:
        blood_color = 10  # Jaune par défaut si aucun personnage spécifié
    
    for _ in range(count):
        # Direction aléatoire pour les gouttes de sang
        angle = random.uniform(0, 2 * 3.14159)  # Angle en radians
        speed = random.uniform(1, 3)  # Vitesse aléatoire
        
        particle = {
            'x': x,
            'y': y,
            'vx': speed * (random.uniform(-1, 1)),  # Vitesse horizontale
            'vy': random.uniform(-4, -1),  # Vitesse verticale (vers le haut)
            'life': 30,  # Durée de vie en frames
            'size': random.randint(1, 3),  # Taille de la goutte
            'color': blood_color  # Couleur spécifique au personnage
        }
        blood_particles.append(particle)

def update_blood_particles():
    """Met à jour toutes les particules de sang"""
    global blood_particles
    
    # Mettre à jour chaque particule
    particles_to_remove = []
    for i, particle in enumerate(blood_particles):
        # Appliquer la gravité
        particle['vy'] += 0.3  # Gravité
        
        # Mettre à jour la position
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        
        # Réduire la durée de vie
        particle['life'] -= 1
        
        # Marquer pour suppression si la vie est terminée ou si le sang touche le sol
        if particle['life'] <= 0 or particle['y'] >= SOL_Y + PERSO_H:
            particles_to_remove.append(i)
    
    # Supprimer les particules mortes (en ordre inverse pour éviter les problèmes d'index)
    for i in reversed(particles_to_remove):
        blood_particles.pop(i)

def draw_blood_particles():
    """Dessine toutes les particules de sang"""
    for particle in blood_particles:
        # Utiliser la couleur spécifique de la particule
        base_color = particle['color']
        alpha = particle['life'] / 30  # Transparence basée sur la vie restante
        
        # Ajuster la couleur en fonction de l'alpha
        if alpha > 0.5:
            color = base_color  # Couleur normale
        else:
            # Couleur plus foncée selon le type
            if base_color == 10:  # Jaune
                color = 9  # Jaune orangé foncé
            elif base_color == 3:  # Vert
                color = 2  # Vert foncé
            else:  # Autre (jaune par défaut)
                color = 9  # Jaune orangé foncé
            
        # Dessiner la goutte de sang
        pyxel.rect(particle['x'], particle['y'], particle['size'], particle['size'], color)

# -----------------------------
# Système d'éclaboussures décoratives (écran de victoire)
# -----------------------------
def create_victory_blood_splashes(center_x, center_y):
    """Crée des éclaboussures de sang décoratives autour du personnage gagnant"""
    global victory_blood_splashes
    import random
    
    # Vider les anciennes éclaboussures
    victory_blood_splashes = []
    
    # Créer 15-25 éclaboussures autour du personnage
    splash_count = random.randint(15, 25)
    
    for _ in range(splash_count):
        # Position aléatoire autour du centre (rayon de 30-80 pixels)
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.uniform(30, 80)
        
        splash_x = center_x + distance * (random.uniform(-1, 1))
        splash_y = center_y + distance * (random.uniform(-1, 1))
        
        # Taille aléatoire (petites éclaboussures)
        size = random.randint(1, 4)
        
        # Couleur jaune (comme demandé)
        color = 10  # Jaune vif dans Pyxel
        
        # Durée de vie décorative (longue pour l'écran de victoire)
        life = random.randint(100, 200)
        
        splash = {
            'x': splash_x,
            'y': splash_y,
            'size': size,
            'color': color,
            'life': life,
            'max_life': life,
            'vy': 0,  # Vitesse verticale initiale
            'gravity': 0.05  # Gravité réduite pour tomber moins vite
        }
        victory_blood_splashes.append(splash)

def draw_victory_blood_splashes():
    """Dessine les éclaboussures décoratives de sang"""
    for splash in victory_blood_splashes:
        # Calculer l'alpha en fonction de la vie restante
        alpha = splash['life'] / splash['max_life']
        
        # Changer la couleur en fonction de l'alpha (toujours jaune)
        if alpha > 0.7:
            color = 10  # Jaune vif
        elif alpha > 0.3:
            color = 11  # Jaune plus clair
        else:
            color = 9  # Jaune orangé foncé pour la fin
        
        # Appliquer la gravité réduite
        splash['vy'] += splash['gravity']
        splash['y'] += splash['vy']
        
        # Dessiner l'éclaboussure
        pyxel.rect(splash['x'], splash['y'], splash['size'], splash['size'], color)
        
        # Mettre à jour la durée de vie
        splash['life'] -= 1
    
    # Supprimer les éclaboussures mortes
    victory_blood_splashes[:] = [s for s in victory_blood_splashes if s['life'] > 0]

# -----------------------------
# Update
# -----------------------------
def update():
    global current_option, page
    global char_index_p1, char_index_p2, selection_step
    global pv_joueur1, pv_joueur2, position_joueur1_x, position_joueur2_x
    global hit_count_1, hit_count_2, can_ultimate_1, can_ultimate_2
    global cooldown_1, cooldown_2, COOLDOWN_MAX
    global loading_progress, loading_dots_timer
    global cooldown_ult, map_selection, selected_map_color
    global map_selection_p1, map_selection_p2, map_selection_step, p1_validated, p2_validated
    global blood_particles, victory_blood_splashes
    global jump_velocity, jump_velocity_double, gravity, vertical_velocity, is_jumping, jump_button_held
    global jump_velocity2, jump_velocity_double2, vertical_velocity2, is_jumping2, jump_button_held2
    global jump_count, max_jumps, jump_count2, max_jumps2

    # ---- Chargement ----
    if page == PAGE_CHARGEMENT:
        loading_progress += loading_speed
        loading_dots_timer += 1

        # Quand le chargement est fini → menu
        if loading_progress >= 100:
            loading_progress = 100
            page = PAGE_MENU

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
                hit_count_1 = 0
                hit_count_2 = 0
                can_ultimate_1 = False
                can_ultimate_2 = False
                position_joueur1_x = 10
                position_joueur2_x = 500
                blood_particles = []  # Réinitialiser les particules de sang
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
                page = PAGE_MAP_SELECT  # Redirige vers la sélection de map

    # ---- Sélection de map ----
    elif page == PAGE_MAP_SELECT:
        # Les deux joueurs naviguent simultanément
        # Joueur 1 (ZQSD) - seulement s'il n'a pas validé
        if not p1_validated:
            if pyxel.btnp(pyxel.KEY_Q):
                map_selection_p1 = (map_selection_p1 - 1) % 17
            elif pyxel.btnp(pyxel.KEY_D):
                map_selection_p1 = (map_selection_p1 + 1) % 17
            elif pyxel.btnp(pyxel.KEY_Z):
                if map_selection_p1 >= 6:
                    map_selection_p1 -= 6
                else:
                    map_selection_p1 = 12
            elif pyxel.btnp(pyxel.KEY_S):
                if map_selection_p1 <= 10:
                    map_selection_p1 += 6
                else:
                    map_selection_p1 = 0
            elif pyxel.btnp(pyxel.KEY_E):
                p1_validated = True
        
        # Joueur 2 (OKLMP) - seulement s'il n'a pas validé
        if not p2_validated:
            if pyxel.btnp(pyxel.KEY_K):
                map_selection_p2 = (map_selection_p2 - 1) % 17
            elif pyxel.btnp(pyxel.KEY_M):
                map_selection_p2 = (map_selection_p2 + 1) % 17
            elif pyxel.btnp(pyxel.KEY_O):
                if map_selection_p2 >= 6:
                    map_selection_p2 -= 6
                else:
                    map_selection_p2 = 12
            elif pyxel.btnp(pyxel.KEY_L):
                if map_selection_p2 <= 10:
                    map_selection_p2 += 6
                else:
                    map_selection_p2 = 0
            elif pyxel.btnp(pyxel.KEY_P):
                p2_validated = True
        
        # Lancer le jeu quand les deux ont validé
        if p1_validated and p2_validated:
            # Sélection aléatoire entre les deux choix
            import random
            chosen_map = random.choice([map_selection_p1, map_selection_p2])
            
            # Déterminer la couleur de map finale
            if chosen_map == 0:
                # Map aléatoire
                selected_map_color = random.choice(MAP_COLORS)
            else:
                # Map spécifique (1-16 -> couleurs 0-15)
                selected_map_color = MAP_COLORS[chosen_map - 1]
            
            # Réinitialiser les variables de jeu et lancer
            pv_joueur1 = 15
            pv_joueur2 = 15
            hit_count_1 = 0
            hit_count_2 = 0
            can_ultimate_1 = False
            can_ultimate_2 = False
            position_joueur1_x = 10
            position_joueur2_x = 500
            blood_particles = []  # Réinitialiser les particules de sang
            page = PAGE_GAME
            
            # Réinitialiser pour la prochaine partie
            p1_validated = False
            p2_validated = False
            
            # Lancer la musique de jeu seulement au début du combat
            pyxel.stop()
            pyxel.playm(0, loop=True)  # musique de jeu


    # ---- Jeu ----
    elif page == PAGE_GAME:
        global position_joueur1_y, is_jumping
        global position_joueur2_y, is_jumping2
        global jump_velocity, jump_velocity_double, gravity, vertical_velocity, jump_button_held
        global jump_velocity2, jump_velocity_double2, vertical_velocity2, jump_button_held2
        global jump_count, max_jumps, jump_count2, max_jumps2
        global attaque_active, attaque_timer, attaque2_active, attaque2_timer
        global attaque1_a_touche, attaque2_a_touche
        global KNOCKBACK, VITESSE_Y, VITESSE_X, SOL_Y, PERSO_H, PERSO_W
        global ultimate_1_x, ultimate_1_y, ultimate_speed, ultimate_damage, ultimate_width, ultimate_heigh, active_ultimate_1
        global ultimate_2_x, ultimate_2_y, active_ultimate_2
        global cooldown_ult_1, cooldown_ult_2, charging_ult_1, charging_ult_2
        global j1_was_walking, j2_was_walking
        
        # décrémentation du cooldown
        if cooldown_1 > 0:
            cooldown_1 -= 1
        if cooldown_2 > 0:
            cooldown_2 -= 1
        
        # --- Joueur 1 déplacements ---
        # Détecter si le joueur 1 était en marche au frame précédent
        was_j1_walking = j1_was_walking
        j1_was_walking = (CHAR_NAMES[char_index_p1] == "Herbal Giant" and pyxel.btn(pyxel.KEY_D))
        
        # Si le joueur 1 était en marche et ne l'est plus, ajuster sa position
        if was_j1_walking and not j1_was_walking:
            # Positionner le sprite normal au pixel le plus à droite de la position de marche précédente
            position_joueur1_x = position_joueur1_x + 20  # Ajouter la largeur supplémentaire de la marche
            # S'assurer qu'il ne dépasse pas les limites
            if position_joueur1_x + PERSO_W > position_joueur2_x:
                position_joueur1_x = position_joueur2_x - PERSO_W - 1
            if position_joueur1_x < 0:
                position_joueur1_x = 0
        
        if pyxel.btn(pyxel.KEY_D) and not charging_ult_1:
            nx = position_joueur1_x + VITESSE_X
            
            # Calculer la largeur visuelle du joueur 1 selon son état
            if CHAR_NAMES[char_index_p1] == "Herbal Giant" and pyxel.btn(pyxel.KEY_D):
                j1_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant marche
            else:
                j1_visual_w = PERSO_W  # Largeur standard
            
            # Calculer la largeur visuelle du joueur 2 selon son état
            if CHAR_NAMES[char_index_p2] == "Herbal Giant" and pyxel.btn(pyxel.KEY_M):
                j2_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant marche
            else:
                j2_visual_w = PERSO_W  # Largeur standard
            
            if nx + j1_visual_w <= position_joueur2_x:
                position_joueur1_x = nx

        if pyxel.btn(pyxel.KEY_Q) and not charging_ult_1:
            nx = position_joueur1_x - VITESSE_X
            
            # Pour le recul, on vérifie seulement la limite gauche de l'écran
            if nx >= 0:
                position_joueur1_x = nx

        # Saut J1 - Double saut (appuyer 2 fois sur Z, sans maintien)
        if pyxel.btnp(pyxel.KEY_Z) and jump_count < max_jumps and not charging_ult_1 and not jump_button_held:
            # Premier saut : doit être au sol
            if jump_count == 0 and position_joueur1_y >= SOL_Y:
                is_jumping = True
                vertical_velocity = jump_velocity
                jump_button_held = True
                jump_count = 1
            # Double saut : peut être fait en l'air, mais moins haut
            elif jump_count == 1:
                vertical_velocity = jump_velocity_double  # Reset avec vitesse réduite pour le double saut
                jump_button_held = True
                jump_count = 2
        
        # Détecter si la touche de saut est relâchée
        if not pyxel.btn(pyxel.KEY_Z):
            jump_button_held = False

        if is_jumping:
            # Appliquer la physique du saut (sans contrôle de hauteur par maintien)
            vertical_velocity += gravity  # Appliquer la gravité
            
            position_joueur1_y += vertical_velocity  # Mettre à jour la position
            
            # Vérifier si on a atterri
            if position_joueur1_y >= SOL_Y:
                position_joueur1_y = SOL_Y
                is_jumping = False
                vertical_velocity = 0
                jump_button_held = False
                jump_count = 0  # Reset le compteur de sauts quand on atterrit

        # --- Attaque J1 ---
        if pyxel.btnp(pyxel.KEY_E) and not attaque_active and cooldown_1 == 0 and not charging_ult_1:
            attaque_active = True
            attaque_timer = attaque_duree
            cooldown_1 = COOLDOWN_MAX

        if attaque_active:
            attaque_timer -= 1
            if attaque_timer <= 0:
                attaque_active = False

        # --- Joueur 2 déplacements ---
        # Détecter si le joueur 2 était en marche au frame précédent
        was_j2_walking = j2_was_walking
        j2_was_walking = (CHAR_NAMES[char_index_p2] == "Herbal Giant" and pyxel.btn(pyxel.KEY_M))
        
        # Si le joueur 2 était en marche et ne l'est plus, ajuster sa position
        if was_j2_walking and not j2_was_walking:
            # Positionner le sprite normal au pixel le plus à droite de la position de marche précédente
            position_joueur2_x = position_joueur2_x - 20  # Retirer la largeur supplémentaire de la marche
            # S'assurer qu'il ne dépasse pas les limites
            if position_joueur2_x < position_joueur1_x + PERSO_W:
                position_joueur2_x = position_joueur1_x + PERSO_W + 1
            if position_joueur2_x + PERSO_W > WINDOW_W:
                position_joueur2_x = WINDOW_W - PERSO_W
        
        if pyxel.btn(pyxel.KEY_K) and not charging_ult_2:
            nx = position_joueur2_x - VITESSE_X
            
            # Calculer la largeur visuelle du joueur 1 selon son état
            if CHAR_NAMES[char_index_p1] == "Herbal Giant" and pyxel.btn(pyxel.KEY_D):
                j1_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant marche
            else:
                j1_visual_w = PERSO_W  # Largeur standard
            
            # Calculer la largeur visuelle du joueur 2 selon son état
            if CHAR_NAMES[char_index_p2] == "Herbal Giant" and pyxel.btn(pyxel.KEY_K):
                j2_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant recule
            else:
                j2_visual_w = PERSO_W  # Largeur standard
            
            if nx >= position_joueur1_x + j1_visual_w:
                position_joueur2_x = nx

        if pyxel.btn(pyxel.KEY_M) and not charging_ult_2:
            nx = position_joueur2_x + VITESSE_X
            
            # Calculer la largeur visuelle du joueur 1 selon son état
            if CHAR_NAMES[char_index_p1] == "Herbal Giant" and pyxel.btn(pyxel.KEY_D):
                j1_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant marche
            else:
                j1_visual_w = PERSO_W  # Largeur standard
            
            # Calculer la largeur visuelle du joueur 2 selon son état
            if CHAR_NAMES[char_index_p2] == "Herbal Giant" and pyxel.btn(pyxel.KEY_M):
                j2_visual_w = PERSO_W + 20  # Largeur visuelle quand Herbal Giant marche
            else:
                j2_visual_w = PERSO_W  # Largeur standard
            
            if nx + j2_visual_w <= WINDOW_W and nx >= position_joueur1_x + j1_visual_w:
                position_joueur2_x = nx

        # Saut J2 - Double saut (appuyer 2 fois sur O, sans maintien)
        if pyxel.btnp(pyxel.KEY_O) and jump_count2 < max_jumps2 and not charging_ult_2 and not jump_button_held2:
            # Premier saut : doit être au sol
            if jump_count2 == 0 and position_joueur2_y >= SOL_Y:
                is_jumping2 = True
                vertical_velocity2 = jump_velocity2
                jump_button_held2 = True
                jump_count2 = 1
            # Double saut : peut être fait en l'air, mais moins haut
            elif jump_count2 == 1:
                vertical_velocity2 = jump_velocity_double2  # Reset avec vitesse réduite pour le double saut
                jump_button_held2 = True
                jump_count2 = 2
        
        # Détecter si la touche de saut est relâchée
        if not pyxel.btn(pyxel.KEY_O):
            jump_button_held2 = False

        if is_jumping2:
            # Appliquer la physique du saut (sans contrôle de hauteur par maintien)
            vertical_velocity2 += gravity  # Appliquer la gravité
            
            position_joueur2_y += vertical_velocity2  # Mettre à jour la position
            
            # Vérifier si on a atterri
            if position_joueur2_y >= SOL_Y:
                position_joueur2_y = SOL_Y
                is_jumping2 = False
                vertical_velocity2 = 0
                jump_button_held2 = False
                jump_count2 = 0  # Reset le compteur de sauts quand on atterrit

        # --- Attaque J2 ---
        if pyxel.btnp(pyxel.KEY_P) and not attaque2_active and cooldown_2 == 0 and not charging_ult_2:
            attaque2_active = True
            attaque2_timer = attaque2_duree
            cooldown_2 = COOLDOWN_MAX

        if attaque2_active:
            attaque2_timer -= 1
            if attaque2_timer <= 0:
                attaque2_active = False

        # --- Dégâts ---
        if attaque_active:
            if not attaque1_a_touche and collision_largeur(position_joueur1_x + PERSO_W, position_joueur1_y + 20, attaque_portee, 50, position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
                pv_joueur2 -= 1
                hit_count_1 += 1
                # Créer des gouttes de sang pour J2
                create_blood_particles(position_joueur2_x + PERSO_W//2, position_joueur2_y + PERSO_H//2, 5, char_index_p2)
                
                # Knockback vers la droite
                position_joueur2_x += KNOCKBACK
                if position_joueur2_x + PERSO_W > WINDOW_W:
                    position_joueur2_x = WINDOW_W - PERSO_W
                
                position_joueur1_x -= KNOCKBACK
                if position_joueur1_x < 0:
                    position_joueur1_x = 0
                
                # Empêcher le chevauchement après knockback
                if position_joueur1_x + PERSO_W > position_joueur2_x:
                    # Si les personnages se chevauchent, les séparer
                    center = (position_joueur1_x + position_joueur2_x + PERSO_W) // 2
                    position_joueur1_x = center - PERSO_W - 1
                    position_joueur2_x = center + 1
                    
                attaque1_a_touche = True
        else:
            attaque1_a_touche = False

        if attaque2_active:
            if not attaque2_a_touche and collision_largeur(position_joueur2_x - attaque2_portee, position_joueur2_y + 20, attaque2_portee, 50, position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
                pv_joueur1 -= 1
                
                hit_count_2 += 1
                # Créer des gouttes de sang pour J1
                create_blood_particles(position_joueur1_x + PERSO_W//2, position_joueur1_y + PERSO_H//2, 5, char_index_p1)
                
                # Knockback vers la gauche
                position_joueur1_x -= KNOCKBACK
                if position_joueur1_x < 0:
                    position_joueur1_x = 0
                
                position_joueur2_x += KNOCKBACK
                if position_joueur2_x + PERSO_W > WINDOW_W:
                    position_joueur2_x = WINDOW_W - PERSO_W
                
                # Empêcher le chevauchement après knockback
                if position_joueur1_x + PERSO_W > position_joueur2_x:
                    # Si les personnages se chevauchent, les séparer
                    center = (position_joueur1_x + position_joueur2_x + PERSO_W) // 2
                    position_joueur1_x = center - PERSO_W - 1
                    position_joueur2_x = center + 1
                
                attaque2_a_touche = True
        else:
            attaque2_a_touche = False
            
        if hit_count_1 >= 5:
            can_ultimate_1 = True
        if hit_count_2 >= 5:
            can_ultimate_2 = True
        
        # Mettre à jour les particules de sang
        update_blood_particles()
            
        # Utilisation ultimate
        if pyxel.btnp(pyxel.KEY_A) and can_ultimate_1 and not charging_ult_1 and not active_ultimate_1:
            charging_ult_1 = True
            cooldown_ult_1 = cooldown_ult  # durée de charge (ex: 60 frames)
        
        if charging_ult_1:
            cooldown_ult_1 -= 1
        
            if cooldown_ult_1 <= 0:
                charging_ult_1 = False
                active_ultimate_1 = True
                ultimate_1_x = position_joueur1_x
                # Position Y en fonction du personnage
                if CHAR_NAMES[char_index_p1] == "Lancelot":
                    ultimate_1_y = position_joueur1_y + 20  # Plus haut pour Lancelot
                elif CHAR_NAMES[char_index_p1] == "Herbal Giant":
                    ultimate_1_y = position_joueur1_y + 40  # Plus bas pour Herbal Giant
                else:
                    ultimate_1_y = position_joueur1_y + 40  # Position par défaut
                hit_count_1 = 0
                can_ultimate_1 = False
        if pyxel.btnp(pyxel.KEY_I) and can_ultimate_2 and not charging_ult_2 and not active_ultimate_2:
            charging_ult_2 = True
            cooldown_ult_2 = cooldown_ult  # durée de charge (ex: 60 frames)
        
        if charging_ult_2:
            cooldown_ult_2 -= 1
        
            if cooldown_ult_2 <= 0:
                charging_ult_2 = False
                active_ultimate_2 = True
                ultimate_2_x = position_joueur2_x
                # Position Y en fonction du personnage
                if CHAR_NAMES[char_index_p2] == "Lancelot":
                    ultimate_2_y = position_joueur2_y + 20  # Plus haut pour Lancelot
                elif CHAR_NAMES[char_index_p2] == "Herbal Giant":
                    ultimate_2_y = position_joueur2_y + 40  # Plus bas pour Herbal Giant
                else:
                    ultimate_2_y = position_joueur2_y + 40  # Position par défaut
                hit_count_2 = 0
                can_ultimate_2 = False
        
        if active_ultimate_1:
            ultimate_1_x += ultimate_speed * direction_ultimate_1
            if ultimate_1_x < - ultimate_width or ultimate_1_x > pyxel.width:
                active_ultimate_1 = False
            if rect_collision(ultimate_1_x, ultimate_1_y, ultimate_width, ultimate_height, position_joueur2_x, position_joueur2_y, PERSO_W, PERSO_H):
                pv_joueur2 -= ultimate_damage
                # Créer plus de gouttes de sang pour l'ultimate
                create_blood_particles(position_joueur2_x + PERSO_W//2, position_joueur2_y + PERSO_H//2, 10, char_index_p2)
                active_ultimate_1 = False
        
        if active_ultimate_2:
            ultimate_2_x += ultimate_speed * direction_ultimate_2
            if ultimate_2_x < - ultimate_width or ultimate_2_x > pyxel.width:
                active_ultimate_2 = False
            if rect_collision(ultimate_2_x, ultimate_2_y, ultimate_width, ultimate_height, position_joueur1_x, position_joueur1_y, PERSO_W, PERSO_H):
                pv_joueur1 -= ultimate_damage
                # Créer plus de gouttes de sang pour l'ultimate
                create_blood_particles(position_joueur1_x + PERSO_W//2, position_joueur1_y + PERSO_H//2, 10, char_index_p1)
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
        
    # ----Chargement ----
    if page == PAGE_CHARGEMENT:
        pyxel.cls(5)  # Fond bleu foncé pour l'écran de chargement
        
        # Animation de fond avec des étoiles/particules
        for i in range(20):
            star_x = (pyxel.frame_count * 2 + i * 30) % (WIDTH + 20) - 10
            star_y = 20 + (i * 13) % (HEIGHT - 40)
            star_size = 1 + (i % 3)
            pyxel.rect(star_x, star_y, star_size, star_size, 7)
        
        # Titre du jeu avec effet 3D
        title_y = 40
        draw_centered_big_text(title_y - 2, "PLANT FIGHTER", 0)  # Ombre noire
        draw_centered_big_text(title_y, "PLANT FIGHTER", 10)  # Texte jaune vif
        
        # Affichage des personnages principaux
        # Lancelot à gauche
        lancelot_x = WIDTH // 4 - PERSO_W // 2
        lancelot_y = 80  # 20 pixels plus haut (était 100)
        draw_char_preview(0, lancelot_x, lancelot_y)  # Lancelot (index 0)
        
        # Herbal Giant à droite  
        herbal_x = 3 * WIDTH // 4 - PERSO_W // 2
        herbal_y = 80  # 20 pixels plus haut (était 100)
        draw_char_preview(1, herbal_x, herbal_y)  # Herbal Giant (index 1)
        
        # Affichage des sprites d'ultimate
        # Ultimate de Lancelot
        pyxel.blt(lancelot_x + 5, lancelot_y + 93, 0, 130, 180, 30, 30, 0)
        pyxel.text(lancelot_x + 5, lancelot_y + 120, "ULTIMATE", 10)
        
        # Ultimate de Herbal Giant
        pyxel.blt(herbal_x + 5, herbal_y + 93, 1, 8, 114, 40, 30, 1)
        pyxel.text(herbal_x + 5, herbal_y + 120, "ULTIMATE", 10)
        
        # Barre de chargement stylisée
        bar_x = WIDTH // 2 - 120
        bar_y = HEIGHT - 60
        bar_w = 240
        bar_h = 20
        
        # Cadre de la barre avec double bordure
        pyxel.rectb(bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4, 0)
        pyxel.rectb(bar_x, bar_y, bar_w, bar_h, 7)
        
        # Barre de progression avec couleur jaune unique
        fill_w = int(bar_w * (loading_progress / 100))
        if fill_w > 0:
            pyxel.rect(bar_x, bar_y, fill_w, bar_h, 10)  # Jaune vif (couleur 10)
        
        # Texte de chargement avec animation
        dots = (loading_dots_timer // 15) % 4
        loading_text = "CHARGEMENT" + "." * dots
        pyxel.text(WIDTH // 2 - 40, bar_y - 15, loading_text, 7)
        
        # Pourcentage de chargement
        pyxel.text(WIDTH // 2 - 15, bar_y + bar_h + 5, f"{int(loading_progress)}%", 7)
        
        # Petits sprites décoratifs
        for i in range(8):
            decor_x = 50 + (i * 60)
            decor_y = HEIGHT - 25
            # Sprite alterné pour l'effet décoratif
            if i % 2 == 0:
                pyxel.blt(decor_x, decor_y, 0, 6, 14, 16, 16, 0)  # Sprite de Lancelot
            else:
                pyxel.blt(decor_x, decor_y, 1, 0, 0, 16, 16, 1)  # Sprite de Herbal Giant

    # ---- MENU ----
    if page == PAGE_MENU:
        # Titre plus haut et centré
        draw_centered_text(30, "PLANT FIGHTER", pyxel.COLOR_BLACK)
        for i, option in enumerate(options):
            color = pyxel.COLOR_GREEN if i == current_option else pyxel.COLOR_BLACK
            draw_centered_text(120 + i*40, option, color)

    # ---- SELECTION DE PERSONNAGES ----
    elif page == PAGE_CHARACTER_SELECT:
        pyxel.cls(6)
        # Titre centré
        draw_centered_text(40, "SELECTION DES PERSONNAGES", 0)

        prev_x = WIDTH // 2 - PERSO_W // 2
        prev_y = 130

        if selection_step == 0:
            # Texte centré pour Joueur 1 - position plus haute
            draw_centered_text(90, "Joueur 1 choisit :", 0)
            draw_char_preview(char_index_p1, prev_x, prev_y)
            draw_centered_text(230, CHAR_NAMES[char_index_p1], 10)
            draw_centered_text(320, "<- Q / D ->   Valider : E", 0)
        else:
            # Texte centré pour Joueur 2 - position plus haute
            draw_centered_text(90, "Joueur 2 choisit :", 0)
            draw_char_preview(char_index_p2, prev_x, prev_y)
            draw_centered_text(230, CHAR_NAMES[char_index_p2], 10)
            draw_centered_text(320, "<- K / M ->   Valider : P", 0)

    # ---- SELECTION DE MAP ----
    elif page == PAGE_MAP_SELECT:
        pyxel.cls(6)
        
        # Titre
        pyxel.text(WIDTH//2 - 60, 30, "SELECTION DES MAPS", 0)
        
        # Instructions pour les deux joueurs
        pyxel.text(50, 50, "J1: ZQSD naviguer  E: valider", 0)
        pyxel.text(300, 50, "J2: OKLMP naviguer  P: valider", 0)
        
        # État de validation
        if p1_validated:
            pyxel.text(50, 65, "J1: PRET", 10)
        else:
            pyxel.text(50, 65, "J1: choisit...", 7)
            
        if p2_validated:
            pyxel.text(300, 65, "J2: PRET", 10)
        else:
            pyxel.text(300, 65, "J2: choisit...", 7)
        
        # Grille de 4x6 avec 17 cases (16 couleurs + 1 aléatoire)
        start_x = 40
        start_y = 90  # Augmenté de 20 (était 70)
        rect_size = 35
        spacing = 12
        
        for i in range(17):
            # Calculer la position dans la grille
            row = i // 6
            col = i % 6
            
            x = start_x + col * (rect_size + spacing)
            y = start_y + row * (rect_size + spacing)
            
            # Dessiner les rectangles de sélection pour les deux joueurs
            if i == map_selection_p1 and not p1_validated:
                # Sélection du J1 - bordure bleue
                pyxel.rectb(x - 2, y - 2, rect_size + 4, rect_size + 4, 12)
                pyxel.rectb(x - 1, y - 1, rect_size + 2, rect_size + 2, 12)
            
            if i == map_selection_p2 and not p2_validated:
                # Sélection du J2 - bordure rouge
                pyxel.rectb(x - 2, y - 2, rect_size + 4, rect_size + 4, 8)
                pyxel.rectb(x - 1, y - 1, rect_size + 2, rect_size + 2, 8)
            
            # Si les deux joueurs ont validé la même case
            if i == map_selection_p1 and i == map_selection_p2 and p1_validated and p2_validated:
                # Double sélection - bordure verte
                pyxel.rectb(x - 3, y - 3, rect_size + 6, rect_size + 6, 11)
                pyxel.rectb(x - 2, y - 2, rect_size + 4, rect_size + 4, 11)
            
            # Ajouter un carré noir autour de la map numéro 6
            if i == 7:  # Map numéro 6 (index 7 car 0 = aléatoire)
                pyxel.rectb(x - 3, y - 3, rect_size + 6, rect_size + 6, 0)
            
            if i == 0:
                # Case aléatoire avec "?"
                pyxel.rect(x, y, rect_size, rect_size, 2)
                pyxel.text(x + rect_size//2 - 4, y + rect_size//2 - 4, "?", 7)
            else:
                # Case de couleur spécifique
                color = MAP_COLORS[i - 1]
                pyxel.rect(x, y, rect_size, rect_size, color)
                # Afficher le numéro de la couleur
                pyxel.text(x + 2, y + 2, str(i - 1), 7 if color > 8 else 0)
        
        # Message quand les deux sont prêts
        if p1_validated and p2_validated:
            pyxel.text(WIDTH//2 - 60, HEIGHT - 30, "LES DEUX SONT PRETS - LANCEMENT...", 10)

    # ---- JEU ----
    elif page == PAGE_GAME:
        pyxel.cls(selected_map_color)

        if pv_joueur1 > 0 and pv_joueur2 > 0:

            draw_char_preview(char_index_p1, position_joueur1_x - PERSO_W, position_joueur1_y, flip_h=True, is_ultimating=charging_ult_1, is_attacking=attaque_active, is_walking=pyxel.btn(pyxel.KEY_D), is_backing=pyxel.btn(pyxel.KEY_Q))
            draw_char_preview(char_index_p2, position_joueur2_x, position_joueur2_y, is_ultimating=charging_ult_2, is_attacking=attaque2_active, is_walking=pyxel.btn(pyxel.KEY_K), is_backing=pyxel.btn(pyxel.KEY_M))

            # Dessiner les particules de sang
            draw_blood_particles()

            # Barre PV
            # Couleurs personnalisées selon la map
            pv1_color = 8  # Couleur par défaut J1
            pv2_color = 3  # Couleur par défaut J2
            text_color = 7  # Couleur de texte par défaut
            ult_ready_color = 10  # Couleur ult prêt par défaut
            
            if selected_map_color == 8:  # Map couleur 8
                pv1_color = 13  # Rose pour J1
            elif selected_map_color == 3:  # Map couleur 3
                pv2_color = 12  # Bleu pour J2
            
            if selected_map_color == 7:  # Map blanche
                text_color = 0  # Texte noir
            
            if selected_map_color == 11:  # Map jaune (couleur 11 dans Pyxel)
                ult_ready_color = 3  # Vert pour ult prêt
            elif selected_map_color == 10:  # Alternative pour jaune (couleur 10)
                ult_ready_color = 3  # Vert pour ult prêt
            
            pyxel.rect(20, 20, pv_joueur1 * 10, 10, pv1_color)
            pyxel.rect(WIDTH - 20 - pv_joueur2 * 10, 20, pv_joueur2 * 10, 10, pv2_color)
            # PV
            pyxel.text(20, 10, f"J1 PV: {pv_joueur1}", text_color)
            pyxel.text(WINDOW_W - 60, 10, f"J2 PV: {pv_joueur2}", text_color)

            if active_ultimate_1:
                # Projectile différent selon le personnage du joueur 1
                if CHAR_NAMES[char_index_p1] == "Lancelot":
                    # Projectile de Lancelot: image 0, u=130, v=180
                    pyxel.blt(ultimate_1_x, ultimate_1_y, 0, 130, 180, 40, 43, 0)
                else:
                    # Projectile de Herbal Giant: image 1, u=0, v=112 (inchangé)
                    pyxel.blt(ultimate_1_x, ultimate_1_y, 1, 0, 112, 40, 43, 1)

            if can_ultimate_1:
                pyxel.text(20, 50, "ULTIMATE 1 READY", ult_ready_color)
                
            if active_ultimate_2:
                # Projectile différent selon le personnage du joueur 2
                if CHAR_NAMES[char_index_p2] == "Lancelot":
                    # Projectile de Lancelot: image 0, u=130, v=180
                    pyxel.blt(ultimate_2_x, ultimate_2_y, 0, 130, 180, 40, 43, 0)
                else:
                    # Projectile de Herbal Giant: image 1, u=0, v=112 (inchangé)
                    pyxel.blt(ultimate_2_x, ultimate_2_y, 1, 0, 112, 40, 43, 1)

            if can_ultimate_2:
                pyxel.text(WINDOW_W - 90, 50, "ULTIMATE 2 READY", ult_ready_color)

        elif pv_joueur2 <= 0:
            pyxel.cls(1)
            # Écran de victoire J1
            # Afficher le personnage gagnant (J1) au centre
            winner_x = WIDTH // 2 - PERSO_W // 2
            winner_y = HEIGHT // 2 - 20
            draw_char_preview(char_index_p1, winner_x, winner_y)
            
            # Créer des éclaboussures de sang décoratives autour du gagnant
            create_victory_blood_splashes(winner_x + PERSO_W // 2, winner_y + PERSO_H // 2)
            draw_victory_blood_splashes()
            
            # Afficher le trophée à 10 pixels à droite du sprite gagnant
            pyxel.blt(winner_x + PERSO_W + 10, winner_y, 2, 6, 3, 20, 20, 7)
            
            # Afficher "1" sous le personnage gagnant (J1)
            pyxel.text(WIDTH // 2 - 4, winner_y + PERSO_H + 15, "1er", 10)  # Jaune pour le gagnant
            
            # Afficher le personnage perdant (J2) à droite avec "2" sous lui
            loser_x = WIDTH - 150
            loser_y = HEIGHT // 2 - 20
            draw_char_preview(char_index_p2, loser_x, loser_y)
            pyxel.text(loser_x + PERSO_W // 2 - 4, loser_y + PERSO_H + 15, "2e", 7)  # Blanc pour le perdant
            
            # Grand texte VICTOIRE au centre
            draw_centered_big_text(HEIGHT // 2 - 80, "VICTOIRE", 10)
            
            # Instructions
            draw_centered_text(HEIGHT - 30, 'TAB: retour au menu', 7)
            if pyxel.btnp(pyxel.KEY_TAB):
                page = PAGE_MENU
                pyxel.stop()
                pyxel.playm(1, loop=True)  # musique menu
        elif pv_joueur1 <= 0:
            pyxel.cls(1)
            # Écran de victoire J2
            # Afficher le personnage gagnant (J2) au centre
            winner_x = WIDTH // 2 - PERSO_W // 2
            winner_y = HEIGHT // 2 - 20
            draw_char_preview(char_index_p2, winner_x, winner_y)
            
            # Créer des éclaboussures de sang décoratives autour du gagnant
            create_victory_blood_splashes(winner_x + PERSO_W // 2, winner_y + PERSO_H // 2)
            draw_victory_blood_splashes()
            
            # Afficher le trophée à 10 pixels à droite du sprite gagnant
            pyxel.blt(winner_x + PERSO_W + 10, winner_y, 2, 6, 3, 20, 20, 7)
            
            # Afficher "2" sous le personnage gagnant (J2)
            pyxel.text(WIDTH // 2 - 4, winner_y + PERSO_H + 15, "1er", 10)  # Jaune pour le gagnant
            
            # Afficher le personnage perdant (J1) à gauche avec "1" sous lui
            loser_x = 50
            loser_y = HEIGHT // 2 - 20
            draw_char_preview(char_index_p1, loser_x, loser_y, flip_h=True)
            pyxel.text(loser_x + PERSO_W // 2 - 4, loser_y + PERSO_H + 15, "2e", 7)  # Blanc pour le perdant
            
            # Grand texte VICTOIRE au centre
            draw_centered_big_text(HEIGHT // 2 - 80, "VICTOIRE", 10)
            
            # Instructions
            draw_centered_text(HEIGHT - 30, 'TAB: retour au menu', 7)
            if pyxel.btnp(pyxel.KEY_TAB):
                page = PAGE_MENU
                pyxel.stop()
                pyxel.playm(1, loop=True)  # musique menu
    
    # ---- OPTIONS ----
    elif page == PAGE_OPTIONS:
        pyxel.cls(7)
        pyxel.text(50, 50, "=== OPTIONS ===", pyxel.COLOR_BLACK)
        pyxel.text(50, 100, "Contrôles J1:", pyxel.COLOR_BLACK)
        pyxel.text(70, 130, "Q/D: déplacer", pyxel.COLOR_BLACK)
        pyxel.text(70, 160, "Z: sauter", pyxel.COLOR_BLACK)
        pyxel.text(70, 190, "E: attaquer", pyxel.COLOR_BLACK)
        pyxel.text(70, 220, "A: ultimate", pyxel.COLOR_BLACK)
        pyxel.text(200, 100, "Contrôles J2:", pyxel.COLOR_BLACK)
        pyxel.text(220, 130, "K/M: déplacer", pyxel.COLOR_BLACK)
        pyxel.text(220, 160, "O: sauter", pyxel.COLOR_BLACK)
        pyxel.text(220, 190, "P: attaquer", pyxel.COLOR_BLACK)
        pyxel.text(220, 220, "I: ultimate", pyxel.COLOR_BLACK)
        pyxel.text(50, 250, "TAB: retour au menu", pyxel.COLOR_RED)

# -----------------------------
# Lancement
# -----------------------------
pyxel.init(WIDTH, HEIGHT, fps=60)
# Lien avec les autres fichiers
pyxel.load("Sprite.pyxres")

# Configuration de la musique
setup_music()
pyxel.playm(1, loop=True)  # musique menu au démarrage

pyxel.run(update, draw)


