import pyxel

position_joueur1_x = 60
position_joueur1_y = 350
LARGEUR_PERSO = 64

jump = 150
is_jumping = False

attaque_active = False
attaque_timer = 0
attaque_duree = 10
attaque_portee = 50


position_joueur2_x = 500
position_joueur2_y = 350

jump2 = 150
is_jumping2 = False

attaque2_active = False
attaque2_timer = 0
attaque2_duree = 10
attaque2_portee = 50

pv_joueur1 = 15
pv_joueur2 = 15

attaque1_a_touche = False
attaque2_a_touche = False

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


def update():
    global position_joueur1_x, position_joueur1_y, is_jumping, jump, attaque_active, attaque_timer, attaque_duree, attaque_portee
    global position_joueur2_x, position_joueur2_y
    global is_jumping2, jump2
    global attaque2_active, attaque2_timer
    
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
        
    if position_joueur1_y < 350:
        if not est_sur(position_joueur1_x, position_joueur1_y, 64, 96,
                       position_joueur2_x, position_joueur2_y, 64):
            is_jumping = True
            
    if is_jumping:
        next_y = position_joueur1_y + 5
        if collision_hauteur(position_joueur1_x, next_y, 64, 96,
                          position_joueur2_x, position_joueur2_y, 64, 96):
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
    
    
    if pyxel.btn(pyxel.KEY_K):
        next_x = position_joueur2_x - 6
        if next_x >= position_joueur1_x + LARGEUR_PERSO:
            position_joueur2_x = next_x

    if pyxel.btn(pyxel.KEY_M):
        next_x = position_joueur2_x + 6
        if next_x + LARGEUR_PERSO <= 700:
            position_joueur2_x = next_x
            
    if pyxel.btnp(pyxel.KEY_O) and not is_jumping2:
        is_jumping2 = True
        position_joueur2_y = 350 - jump2
        
    if position_joueur2_y < 350:
        if not est_sur(position_joueur2_x, position_joueur2_y, 64, 96, position_joueur1_x, position_joueur1_y, 64):
            is_jumping2 = True
            
    if is_jumping2:
        next_y = position_joueur2_y + 5
        if collision_hauteur(position_joueur2_x, next_y, 64, 96, position_joueur1_x, position_joueur1_y, 64, 96):
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
    
    
    global pv_joueur2, attaque1_a_touche
    if attaque_active:
        attaque_x = position_joueur1_x + LARGEUR_PERSO
        attaque_y = position_joueur1_y + 20
        if not attaque1_a_touche and collision_largeur(
            attaque_x, attaque_y, attaque_portee, 50,
            position_joueur2_x, position_joueur2_y, 64, 96
        ):
            pv_joueur2 -= 1
            attaque1_a_touche = True
    if not attaque_active:
        attaque1_a_touche = False
        
    global pv_joueur1, attaque2_a_touche

    if attaque2_active:
        attaque2_x = position_joueur2_x - attaque2_portee
        attaque2_y = position_joueur2_y + 20
        if not attaque2_a_touche and collision_largeur(
            attaque2_x, attaque2_y, attaque2_portee, 50,
            position_joueur1_x, position_joueur1_y, 64, 96
        ):
            pv_joueur1 -= 1
            attaque2_a_touche = True

    if not attaque2_active:  
        attaque2_a_touche = False        


def draw():
    
    if pv_joueur1 > 0 and pv_joueur2 > 0:
        pyxel.cls(1)
        pyxel.rect(position_joueur1_x, position_joueur1_y, LARGEUR_PERSO, 96, 10)
        if attaque_active:
            attaque_x = position_joueur1_x + 64
            attaque_y = position_joueur1_y + 20
            pyxel.rect(attaque_x, attaque_y, attaque_portee, 50, 8)
        
        pyxel.rect(position_joueur2_x, position_joueur2_y, LARGEUR_PERSO, 96, 11)
        if attaque2_active:
            attaque2_x = position_joueur2_x - attaque2_portee
            attaque2_y = position_joueur2_y + 20
            pyxel.rect(attaque2_x, attaque2_y, attaque2_portee, 50, 3)
        
        
        pyxel.rect(20, 20, pv_joueur1 * 10, 10, 8)
        pyxel.text(20, 10, f"J1 PV: {pv_joueur1}", 7)

        pyxel.rect(700 - 20 - pv_joueur2 * 10, 20, pv_joueur2 * 10, 10, 3)
        pyxel.text(700 - 120, 10, f"J2 PV: {pv_joueur2}", 7)
    elif pv_joueur2 <= 0:
        pyxel.cls(0)
        pyxel.text(300, 200, 'GAME OVER', 7)
        pyxel.text(300, 250, 'J1 à ganger', 7)
    elif pv_joueur1 <= 0:
        pyxel.cls(0)
        pyxel.text(300, 200, 'GAME OVER', 7)
        pyxel.text(300, 250, 'J2 à ganger', 7)

    

pyxel.init(700, 500)
pyxel.run(update, draw)