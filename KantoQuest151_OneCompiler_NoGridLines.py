# KANTO QUEST 151 — 1920 x 1080 DESKTOP EDITION
# One Python file. Requires pygame only: python -m pip install pygame
# OneCompiler edition: crisp 960x540 grid map with no seam lines; instant movement.

from pathlib import Path
import pygame

SCREEN_W, SCREEN_H = 960, 540
BROWSER_W, BROWSER_H = 960, 540
MAP_X, MAP_Y, TILE = 30, 145, 27
MAP_W, MAP_H = 20 * TILE, 12 * TILE
PANEL_X = 602
canvas = None
window = None
clock = None
fonts = {}
ink_color = (0, 0, 0)
fullscreen = False

NAVY = (16, 28, 39)
DARK = (24, 42, 51)
MID = (35, 65, 72)
TEAL = (42, 132, 126)
MINT = (100, 212, 176)
GOLD = (255, 190, 94)
PAPER = (244, 248, 243)
INK_DARK = (28, 47, 56)
MUTED = (113, 142, 146)
CARD = (35, 58, 67)
CARD_2 = (44, 77, 83)
RED = (231, 104, 104)

class GameExit(Exception):
    """Raised when the window is closed."""


def initialize_display():
    """Open OneCompiler display with a native, legible compact interface."""
    global window, canvas, clock
    pygame.init()
    pygame.font.init()
    # OneCompiler streams this window into the webpage; do not request
    # an actual 1920x1080 desktop display from the hosted environment.
    window = pygame.display.set_mode((BROWSER_W, BROWSER_H))
    canvas = pygame.Surface((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Kanto Quest 151 | Clean Tile Map')
    pygame.key.set_repeat(250, 125)
    clock = pygame.time.Clock()
    print('Kanto Quest: display ready. Click the game screen to focus, then use the arrow keys and Enter.', flush=True)


def present():
    """Display the compact interface with aspect-ratio-preserving scaling."""
    if window is None:
        return
    w, h = window.get_size()
    if w <= 0 or h <= 0:
        return
    scale = min(w / SCREEN_W, h / SCREEN_H)
    dw = max(1, round(SCREEN_W * scale))
    dh = max(1, round(SCREEN_H * scale))
    window.fill(NAVY)
    if (dw, dh) == (SCREEN_W, SCREEN_H):
        window.blit(canvas, ((w - dw) // 2, (h - dh) // 2))
    else:
        # Half-scale preview, without asking the server to stream a full HD frame.
        window.blit(pygame.transform.scale(canvas, (dw, dh)),
                    ((w - dw) // 2, (h - dh) // 2))
    pygame.display.flip()
    clock.tick(30)

def set_color(red, green, blue):
    global ink_color
    ink_color = (int(red), int(green), int(blue))


def fill_rect(x, y, w, h):
    pygame.draw.rect(canvas, ink_color, (int(x), int(y), int(w), int(h)))


def draw_rect(x, y, w, h):
    pygame.draw.rect(canvas, ink_color, (int(x), int(y), int(w), int(h)), 2)


def draw_text(x, y, text):
    ui_text(str(text), x, y - 34, 29, ink_color)


def fill_circle(x, y, radius):
    pygame.draw.circle(canvas, ink_color, (int(x), int(y)), int(radius))


def draw_circle(x, y, radius):
    pygame.draw.circle(canvas, ink_color, (int(x), int(y)), int(radius), 2)


def clear():
    canvas.fill(NAVY)


def wait_key():
    """Return the original game's keycode from a browser Pygame event."""
    present()
    keyboard = {
        pygame.K_UP: 25, pygame.K_w: 25,
        pygame.K_DOWN: 34, pygame.K_s: 34,
        pygame.K_LEFT: 24, pygame.K_a: 24,
        pygame.K_RIGHT: 26, pygame.K_d: 26,
        pygame.K_RETURN: 105, pygame.K_KP_ENTER: 105, pygame.K_SPACE: 105,
        pygame.K_ESCAPE: 45, pygame.K_BACKSPACE: 45,
        pygame.K_1: 92, pygame.K_KP1: 92,
        pygame.K_2: 93, pygame.K_KP2: 93,
        pygame.K_3: 94, pygame.K_KP3: 94,
        pygame.K_4: 82, pygame.K_KP4: 82,
        pygame.K_5: 83, pygame.K_KP5: 83,
        pygame.K_6: 84, pygame.K_KP6: 84,
        pygame.K_7: 72, pygame.K_8: 73, pygame.K_9: 74,
        pygame.K_0: 102,
    }
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            raise GameExit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                # The website owns browser fullscreen; don't ask SDL to switch mode.
                continue
            if event.key in keyboard:
                return keyboard[event.key]

def ui_font(size, bold=False):
    key = (size, bold)
    if key not in fonts:
        fonts[key] = pygame.font.SysFont('inter,arial,dejavusans', size, bold=bold)
    return fonts[key]


def ui_text(text, x, y, size=32, color=PAPER, bold=False, max_width=None, align='left'):
    """Draw text with measured horizontal clipping, not character-count trimming."""
    f = ui_font(size, bold)
    s = str(text)
    if max_width:
        if f.size(s)[0] > max_width:
            while s and f.size(s + '…')[0] > max_width:
                s = s[:-1]
            s += '…'
    art = f.render(s, True, color)
    if align == 'center':
        x -= art.get_width() // 2
    elif align == 'right':
        x -= art.get_width()
    canvas.blit(art, (int(x), int(y)))
    return art.get_width()


def ui_box(x, y, w, h, color=CARD, radius=24, border=None):
    rect = pygame.Rect(int(x), int(y), int(w), int(h))
    pygame.draw.rect(canvas, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(canvas, border, rect, 2, border_radius=radius)


def ui_rule(x, y, w, color=(63, 91, 96), h=2):
    pygame.draw.rect(canvas, color, (int(x), int(y), int(w), int(h)))


def ui_pill(text, x, y, color=TEAL, text_color=PAPER, width=None):
    f = ui_font(23, True)
    width = width or f.size(str(text))[0] + 34
    ui_box(x, y, width, 42, color, 21)
    ui_text(text, x + width // 2, y + 7, 22, text_color, True, align='center')


def ui_frame(title, subtitle='', section='ADVENTURE'):
    canvas.fill(NAVY)
    pygame.draw.rect(canvas, (19, 35, 44), (0, 0, SCREEN_W, 124))
    ui_box(56, 38, 48, 48, TEAL, 13)
    ui_text('K', 80, 43, 28, PAPER, True, align='center')
    ui_text('KANTO  /  QUEST', 124, 47, 28, PAPER, True)
    ui_pill(section, 1580, 41, CARD_2, MINT, 280)
    ui_text(title, 76, 139, 54, PAPER, True, 1390)
    if subtitle:
        ui_text(subtitle, 80, 211, 25, MUTED, max_width=1400)


def ui_footer(help_text='ARROWS / WASD  Navigate      ENTER  Select      ESC  Back'):
    ui_rule(72, 1010, SCREEN_W - 144, (43, 73, 80))
    ui_text(help_text, 82, 1028, 26, (173, 194, 191), max_width=1750)


def ui_health_bar(x, y, w, h, current, maximum):
    amount = max(0, min(1.0, current / max(1, maximum)))
    color = (83, 199, 142) if amount > 0.6 else GOLD if amount > 0.3 else RED
    ui_box(x, y, w, h, (62, 81, 85), h // 2)
    if amount:
        ui_box(x, y, max(h, int(w * amount)), h, color, h // 2)


def ui_glow(x, y, r, c):
    """Layered circles for simple stylized portrait backgrounds."""
    for factor, mix in ((1.0, 0.22), (.77, .32), (.52, .47)):
        cc = tuple(round(NAVY[i] * (1-mix) + c[i] * mix) for i in range(3))
        pygame.draw.circle(canvas, cc, (int(x), int(y)), int(r * factor))


def draw_landmark(kind, x, y):
    """Readable buildings and pickups inside the 64-pixel world grid."""
    x, y = int(x), int(y)
    ratio = TILE / 64.0
    pygame.draw.rect(canvas, (215, 203, 160), (x, y, TILE, TILE))
    def r(dx,dy,w,h,c):
        pygame.draw.rect(canvas, c, (x+round(dx*ratio), y+round(dy*ratio), max(1,round(w*ratio)), max(1,round(h*ratio))))
    if kind in ('H','S','G'):
        roof = {'H':(205,73,89),'S':(220,151,66),'G':(106,104,191)}[kind]
        r(5,25,54,36,(236,226,207))
        r(0,16,64,16,roof)
        r(6,9,52,8,roof)
        r(24,38,16,23,(42,71,84))
        r(8,37,10,11,(109,195,213));r(46,37,10,11,(109,195,213))
        if kind == 'H':
            r(29,2,6,22,PAPER);r(21,10,22,6,PAPER)
        elif kind == 'S':
            r(23,6,18,9,(75,167,93))
        else:
            r(25,4,14,12,GOLD)
    elif kind == 'T':
        r(21,10,24,13,(187,74,85));r(23,23,19,17,(238,185,144))
        r(15,40,34,19,(61,103,182));r(20,56,9,8,(33,45,56));r(36,56,9,8,(33,45,56))
    elif kind == 'I':
        r(10,28,44,31,(114,77,49));r(10,22,44,11,(212,158,74));r(29,31,8,23,GOLD)
    elif kind == 'C':
        pygame.draw.circle(canvas, (155,111,194), (x+TILE//2,y+TILE//2), round(23*ratio))
        pygame.draw.circle(canvas, GOLD, (x+TILE//2,y+TILE//2), round(13*ratio))
        pygame.draw.circle(canvas, PAPER, (x+TILE//2,y+TILE//2), round(6*ratio))


# GAME LOGIC (ported from the original TI-84 Evo version)

import json
from pathlib import Path
SAVE_FILE = Path('kanto_save.json')
from random import randint
KEY_UP = 25
KEY_DOWN = 34
KEY_LEFT = 24
KEY_RIGHT = 26
KEY_CONFIRM = 105
KEY_CANCEL = 45
KEY_ONE = 92
KEY_TWO = 93
KEY_THREE = 94
KEY_FOUR = 82
KEY_FIVE = 83
KEY_SIX = 84
KEY_SEVEN = 72
KEY_EIGHT = 73
KEY_NINE = 74
KEY_ZERO = 102
SPECIES_NAME_PACKS = ('Bulbasaur|Ivysaur|Venusaur|Charmander|Charmeleon|Charizard|Squirtle|Wartortle|Blastoise|Caterpie|Metapod|Butterfree|Weedle|Kakuna|Beedrill|Pidgey|Pidgeotto|Pidgeot|Rattata|Raticate|Spearow|Fearow|Ekans|Arbok|Pikachu|Raichu|Sandshrew|Sandslash|Nidoran F|Nidorina|Nidoqueen|Nidoran M|Nidorino|Nidoking|Clefairy|Clefable|Vulpix|Ninetales', 'Jigglypuff|Wigglytuff|Zubat|Golbat|Oddish|Gloom|Vileplume|Paras|Parasect|Venonat|Venomoth|Diglett|Dugtrio|Meowth|Persian|Psyduck|Golduck|Mankey|Primeape|Growlithe|Arcanine|Poliwag|Poliwhirl|Poliwrath|Abra|Kadabra|Alakazam|Machop|Machoke|Machamp|Bellsprout|Weepinbell|Victreebel|Tentacool|Tentacruel|Geodude|Graveler|Golem', "Ponyta|Rapidash|Slowpoke|Slowbro|Magnemite|Magneton|Farfetch'd|Doduo|Dodrio|Seel|Dewgong|Grimer|Muk|Shellder|Cloyster|Gastly|Haunter|Gengar|Onix|Drowzee|Hypno|Krabby|Kingler|Voltorb|Electrode|Exeggcute|Exeggutor|Cubone|Marowak|Hitmonlee|Hitmonchan|Lickitung|Koffing|Weezing|Rhyhorn|Rhydon|Chansey|Tangela", 'Kangaskhan|Horsea|Seadra|Goldeen|Seaking|Staryu|Starmie|Mr. Mime|Scyther|Jynx|Electabuzz|Magmar|Pinsir|Tauros|Magikarp|Gyarados|Lapras|Ditto|Eevee|Vaporeon|Jolteon|Flareon|Porygon|Omanyte|Omastar|Kabuto|Kabutops|Aerodactyl|Snorlax|Articuno|Zapdos|Moltres|Dratini|Dragonair|Dragonite|Mewtwo|Mew')
SPECIES_TYPE_PACKS = ('GPGPGPF-F-FYW-W-W-B-B-BYBPBPBPNYNYNYN-N-NYNYP-P-E-E-D-D-P-P-PDP-P-PDN-N-F-F-', 'N-N-PYPYGPGPGPBGBGBPBPD-D-N-N-W-W-K-K-F-F-W-W-WKS-S-S-K-K-K-GPGPGPWPWPRDRDRD', 'F-F-WSWSE-E-NYNYNYW-WIP-P-W-WIHPHPHPRDS-S-W-W-E-E-GSGSD-D-K-K-N-P-P-DRDRN-G-', 'N-W-W-W-W-W-WSS-BYISE-F-B-N-W-WYWIN-N-W-E-F-N-RWRWRWRWRYN-IYEYFYT-T-TYS-S-')
SPECIES_NAMES = [p.split('|') for p in SPECIES_NAME_PACKS]
TYPE_NAMES = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon']
TYPE_CODES = 'NFWGEIKPDYSBRHT'
AREA_NAMES = ['PINE TOWN', 'GREEN TRAIL', 'OLD FOREST', 'STONEHOLD', 'ECHO CAVE', 'BAYPORT', 'SUNSET PLAINS', 'VOLT CITY', 'DUSK WOODS', 'NIGHTFALL', 'SKY RIDGE', 'CROWN TOWER', 'LEGEND LAKE', 'SAFARI WILDS']
WILD_ENCOUNTER_POOLS = ['16 19 21 25 35 39 43 52', '1 4 7 10 13 16 19 21 23 25 27 29 32 37 39 43 46', '10 11 12 13 14 15 17 18 41 42 43 44 45 46 47 48 49 69 70 71 123 127', '23 24 27 28 50 51 66 67 74 75 76 95 104 105 111 112', '41 42 46 47 48 49 50 51 74 75 76 92 93 95 111 112 138 140 142', '54 55 60 61 62 72 73 79 80 86 87 90 91 98 99 116 117 118 119 120 121 129 130', '19 20 21 22 52 53 56 57 58 59 77 78 83 84 85 108 113 114 115 128 132 133', '25 26 35 36 39 40 52 53 81 82 100 101 125 133 135 137', '1 2 3 43 44 45 46 47 48 49 69 70 71 102 103 114 123 127 131', '23 24 29 30 31 32 33 34 41 42 88 89 92 93 94 96 97 109 110 122 124', '6 9 18 22 28 34 38 59 65 68 78 83 85 94 105 112 130 134 136 139 141 142 143 147 148 149', '3 6 9 31 34 38 45 62 65 68 71 73 76 80 82 94 103 112 121 130 131 139 141 142 143 149', '131 132 138 139 140 141 142 143 144 145 146 147 148 149 150 151', '1 4 7 25 26 52 54 56 58 63 66 72 74 77 79 81 83 86 88 90 92 95 98 100 102 104 106 107 108 111 113 114 115 120 122 123 124 125 126 127 128 129 131 132 133 134 135 136 137 142']
BATTLE_MOVES = [('Tackle', 'N', 40, 100), ('Quick Hit', 'N', 55, 95), ('Body Slam', 'N', 85, 85), ('Ember', 'F', 40, 100), ('Flame Burst', 'F', 75, 90), ('Water Jet', 'W', 45, 100), ('Tidal Wave', 'W', 75, 90), ('Leaf Whip', 'G', 45, 100), ('Solar Bloom', 'G', 80, 85), ('Spark', 'E', 45, 100), ('Thunderbolt', 'E', 75, 90), ('Frost Flake', 'I', 40, 100), ('Blizzard', 'I', 80, 85), ('Low Kick', 'K', 45, 100), ('Power Punch', 'K', 75, 90), ('Poison Sting', 'P', 45, 100), ('Venom Cloud', 'P', 75, 90), ('Mud Shot', 'D', 45, 100), ('Quake', 'D', 80, 90), ('Wing Gust', 'Y', 45, 100), ('Air Slash', 'Y', 75, 90), ('Mind Pulse', 'S', 45, 100), ('Psy Burst', 'S', 80, 85), ('Bug Bite', 'B', 45, 100), ('Swarm Rush', 'B', 75, 90), ('Stone Hit', 'R', 50, 95), ('Rock Slide', 'R', 80, 85), ('Haunt', 'H', 45, 100), ('Spirit Blast', 'H', 75, 90), ('Dragon Breath', 'T', 50, 95), ('Dragon Burst', 'T', 85, 85)]
TYPE_EFFECTIVENESS = {'N': {'R': 0.5, 'H': 0}, 'F': {'G': 2, 'B': 2, 'I': 2, 'R': 0.5, 'W': 0.5, 'F': 0.5, 'T': 0.5}, 'W': {'F': 2, 'R': 2, 'D': 2, 'W': 0.5, 'G': 0.5, 'T': 0.5}, 'G': {'W': 2, 'R': 2, 'D': 2, 'F': 0.5, 'G': 0.5, 'P': 0.5, 'B': 0.5, 'Y': 0.5, 'T': 0.5}, 'E': {'W': 2, 'Y': 2, 'E': 0.5, 'G': 0.5, 'T': 0.5, 'D': 0}, 'I': {'G': 2, 'D': 2, 'Y': 2, 'T': 2, 'W': 0.5, 'I': 0.5, 'F': 0.5}, 'K': {'N': 2, 'R': 2, 'I': 2, 'P': 0.5, 'Y': 0.5, 'S': 0.5, 'B': 0.5, 'H': 0}, 'P': {'G': 2, 'B': 2, 'P': 0.5, 'D': 0.5, 'R': 0.5, 'H': 0.5}, 'D': {'F': 2, 'E': 2, 'P': 2, 'R': 2, 'G': 0.5, 'B': 0.5, 'Y': 0}, 'Y': {'G': 2, 'B': 2, 'K': 2, 'E': 0.5, 'R': 0.5}, 'S': {'K': 2, 'P': 2, 'S': 0.5}, 'B': {'G': 2, 'S': 2, 'F': 0.5, 'K': 0.5, 'P': 0.5, 'Y': 0.5, 'H': 0.5}, 'R': {'F': 2, 'I': 2, 'Y': 2, 'B': 2, 'K': 0.5, 'D': 0.5}, 'H': {'H': 2, 'S': 2, 'N': 0}, 'T': {'T': 2}}
EVOLUTION_RULES = {1: (16, 2), 2: (32, 3), 4: (16, 5), 5: (36, 6), 7: (16, 8), 8: (36, 9), 10: (7, 11), 11: (10, 12), 13: (7, 14), 14: (10, 15), 16: (18, 17), 17: (36, 18), 19: (20, 20), 21: (20, 22), 23: (22, 24), 25: (28, 26), 27: (22, 28), 29: (16, 30), 30: (32, 31), 32: (16, 33), 33: (32, 34), 35: (28, 36), 37: (28, 38), 39: (28, 40), 41: (22, 42), 43: (21, 44), 44: (32, 45), 46: (24, 47), 48: (31, 49), 50: (26, 51), 52: (28, 53), 54: (33, 55), 56: (28, 57), 58: (30, 59), 60: (25, 61), 61: (35, 62), 63: (16, 64), 64: (38, 65), 66: (28, 67), 67: (38, 68), 69: (21, 70), 70: (32, 71), 72: (30, 73), 74: (25, 75), 75: (38, 76), 77: (40, 78), 79: (37, 80), 81: (30, 82), 84: (31, 85), 86: (34, 87), 88: (38, 89), 90: (30, 91), 92: (25, 93), 93: (38, 94), 96: (26, 97), 98: (28, 99), 100: (30, 101), 102: (32, 103), 104: (28, 105), 109: (35, 110), 111: (42, 112), 116: (32, 117), 118: (33, 119), 120: (32, 121), 129: (20, 130), 133: (25, 134), 138: (40, 139), 140: (40, 141), 147: (30, 148), 148: (55, 149)}
current_area = 0
player_x = 2
player_y = 6
coins = 700
capture_orbs = 8
great_capture_orbs = 2
healing_potions = 5
super_healing_potions = 1
earned_badges = 0
defeated_trainers = 0
collected_treasures = 0
champion_defeated = 0
party = []
storage_box = []
seen_species = [0] * 6
caught_species = [0] * 6
steps_taken = 0

def pokemon_name(n):
    a = (n - 1) // 38
    b = (n - 1) % 38
    return SPECIES_NAMES[a][b]

def pokemon_types(n):
    a = (n - 1) // 38
    b = 2 * ((n - 1) % 38)
    s = SPECIES_TYPE_PACKS[a]
    return (s[b], s[b + 1])

def type_name(c):
    if c == '-':
        return '-'
    return TYPE_NAMES[TYPE_CODES.index(c)]

def has_species_flag(bits, n):
    n -= 1
    return bits[n // 26] & 1 << n % 26 != 0

def set_species_flag(bits, n):
    n -= 1
    bits[n // 26] |= 1 << n % 26

def count_species_flags(bits):
    c = 0
    for n in range(1, 152):
        if has_species_flag(bits, n):
            c += 1
    return c

def clamp(v, a, b):
    if v < a:
        return a
    if v > b:
        return b
    return v
PREVIOUS_EVOLUTIONS = {}
for source, step in EVOLUTION_RULES.items():
    PREVIOUS_EVOLUTIONS[step[1]] = source
PREVIOUS_EVOLUTIONS[135] = 133
PREVIOUS_EVOLUTIONS[136] = 133

def evolution_strength_bonus(sid):
    stage = 0
    cur = sid
    while cur in PREVIOUS_EVOLUTIONS and stage < 2:
        stage += 1
        cur = PREVIOUS_EVOLUTIONS[cur]
    special = 22 if sid >= 144 else 10 if sid in (131, 142, 143) else 0
    return stage * 11 + special

def max_health(mon):
    sid, lv = (mon[0], mon[1])
    return 17 + lv * 3 + sid * 7 % 25 + evolution_strength_bonus(sid) // 2

def attack_stat(mon):
    return 18 + mon[1] * 2 + mon[0] * 11 % 24 + evolution_strength_bonus(mon[0])

def defense_stat(mon):
    return 17 + mon[1] * 2 + mon[0] * 13 % 25 + evolution_strength_bonus(mon[0])

def speed_stat(mon):
    return 10 + mon[1] * 2 + mon[0] * 17 % 40 + evolution_strength_bonus(mon[0]) // 2

def create_pokemon(sid, lv):
    mon = [sid, lv, 0, 0]
    mon[2] = max_health(mon)
    return mon

def first_healthy_party_index():
    for i in range(len(party)):
        if party[i][2] > 0:
            return i
    return -1

def available_moves(mon):
    a, b = pokemon_types(mon[0])
    i = TYPE_CODES.index(a)
    low = 0 if i == 0 else 3 + (i - 1) * 2
    high = 2 if i == 0 else low + 1
    m3 = high if mon[1] >= 17 else low
    j = TYPE_CODES.index(b) if b != '-' else 0
    m4 = (0 if j == 0 else 3 + (j - 1) * 2) if b != '-' else 2
    return [0, 1, m3, m4]

def type_multiplier(move_type, mon):
    t1, t2 = pokemon_types(mon[0])
    d = TYPE_EFFECTIVENESS.get(move_type, {})
    return d.get(t1, 1) * d.get(t2, 1)
overworld_is_drawn = False
battle_screen_is_drawn = False
displayed_battle_pokemon = None
last_draw_color = None
BG = (238, 243, 235)
BAR = (42, 88, 92)
FOOT = (216, 231, 219)
INK = (25, 33, 40)
WHITE = (255, 255, 255)
SELECT = (46, 113, 108)
UNSELECT = (223, 233, 224)

def set_pen_color(r, g, b):
    global last_draw_color
    color = (r, g, b)
    if color != last_draw_color:
        set_color(r, g, b)
        last_draw_color = color

def draw_filled_rectangle(x, y, w, h, color):
    set_pen_color(color[0], color[1], color[2])
    fill_rect(x, y, w, h)

def draw_label(x, y, s):
    ui_text(s, int(x), int(y), 32, PAPER, max_width=1100)

def draw_screen(title):
    global overworld_is_drawn, battle_screen_is_drawn
    overworld_is_drawn = False
    battle_screen_is_drawn = False
    ui_frame(title, 'Explore, battle, collect and become the champion.', 'KANTO 151')

def show_message(*lines):
    draw_screen('ADVENTURE UPDATE')
    ui_box(205, 310, 1510, 548, CARD, 32, (68, 107, 111))
    ui_pill('NEW MESSAGE', 285, 359, TEAL)
    y = 440
    font = ui_font(47, True)
    for content in lines:
        words = str(content).split()
        assembled = ''
        for word in words:
            candidate = (assembled + ' ' + word).strip()
            if font.size(candidate)[0] > 1290 and assembled:
                ui_text(assembled, 290, y, 47, PAPER, True)
                y += 74
                assembled = word
            else:
                assembled = candidate
        if assembled:
            ui_text(assembled, 290, y, 47, PAPER, True, max_width=1250)
            y += 74
    ui_text('PRESS ENTER OR ANY CONTROL KEY', 291, 782, 26, MINT, True)
    ui_footer()
    wait_key()

def menu_layout(count, first):
    return (288, 90)

def draw_menu_row(options, index, selected, first, top, step):
    j = index - first
    y = top + j * step
    if selected:
        ui_box(108, y, 1090, 75, TEAL, 18)
        ui_box(108, y + 8, 7, 59, GOLD, 3)
        ui_text('›', 144, y + 11, 37, GOLD, True)
        color = PAPER
    else:
        ui_box(108, y, 1090, 75, CARD, 18)
        color = (196, 220, 217)
    label = str(options[index])
    ui_text(label, 207, y + 16, 35, color, selected, 936)
    if selected:
        ui_text('ENTER', 1126, y + 26, 18, (211, 246, 232), True, align='right')

def choose_menu(title, options, initial=0):
    if not options:
        return -1
    count = len(options)
    selected = clamp(initial, 0, count - 1)
    while True:
        first = selected // 7 * 7
        ui_frame(title, 'Choose an option to continue.', 'MENU')
        ui_box(75, 255, 1160, 686, DARK, 26, (51, 80, 86))
        top, step = menu_layout(count, first)
        for index in range(first, min(first + 7, count)):
            draw_menu_row(options, index, index == selected, first, top, step)
        ui_box(1290, 255, 554, 686, CARD, 26)
        ui_pill('ADVENTURE STATUS', 1332, 301, TEAL)
        ui_text('Kanto Quest', 1334, 376, 48, PAPER, True)
        ui_text('151 creatures. 14 regions.', 1336, 436, 29, (167, 193, 192))
        ui_rule(1334, 501, 458)
        ui_text('BADGES', 1337, 534, 24, MUTED, True)
        ui_text(f'{earned_badge_count()} / 4', 1341, 572, 47, GOLD, True)
        ui_text('COINS', 1600, 534, 24, MUTED, True)
        ui_text(str(coins), 1600, 579, 43, MINT, True)
        ui_rule(1334, 645, 458)
        ui_text('LOCATION', 1337, 681, 23, MUTED, True)
        ui_text(AREA_NAMES[current_area].title(), 1337, 722, 36, PAPER, True, 447)
        ui_text(f'{count} choice(s)  •  {selected + 1} selected', 1337, 868, 23, MUTED)
        ui_footer('↑ / ↓   Select     ENTER   Confirm     ESC   Back      1–6   Quick select     F11   Fullscreen')
        key = wait_key()
        if key == KEY_UP:
            selected = (selected - 1) % count
        elif key == KEY_DOWN:
            selected = (selected + 1) % count
        elif key == KEY_CONFIRM:
            return selected
        elif key == KEY_CANCEL:
            return -1
        elif key in (KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE, KEY_SIX):
            number = (KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE, KEY_SIX).index(key)
            if number < count:
                return number

def draw_health_bar(x, y, w, mon):
    ui_health_bar(x, y, w, 23, mon[2], max_health(mon))

def draw_pokemon_icon(x, y, mon, scale=1):
    """Original type-based creature illustration, vector-drawn at high resolution."""
    species = mon[0]
    kind = TYPE_CODES.index(pokemon_types(species)[0])
    colors = [(170, 169, 151), (242, 120, 73), (92, 168, 221), (102, 198, 119), (245, 210, 88), (165, 222, 241), (211, 144, 99), (185, 133, 202), (194, 162, 110), (123, 184, 225), (207, 155, 224), (168, 204, 107), (173, 165, 143), (145, 117, 201), (152, 144, 217)]
    main = colors[kind]
    dark = tuple((max(0, n - 69) for n in main))
    light = tuple((min(255, n + 46) for n in main))
    size = max(1, float(scale))
    r = int(68 * size)
    x, y = (int(x), int(y))

    def oval(color, px, py, rw, rh):
        pygame.draw.ellipse(canvas, color, (int(px), int(py), int(rw), int(rh)))
    oval((18, 36, 42), x - r, y + r // 2, r * 2, r // 2)
    for offset in (-0.54, 0.32):
        oval(dark, x + int(r * offset), y + int(r * 0.55), r // 3, r // 2)
    if kind in (1, 4, 14):
        pygame.draw.polygon(canvas, dark, [(x + r // 2, y + r // 4), (x + r + 35, y - r // 3), (x + r + 5, y - r // 2)])
        pygame.draw.polygon(canvas, GOLD, [(x + r // 2, y + r // 4), (x + r + 10, y - r // 3), (x + r + 2, y - r // 2)])
    if kind in (2, 5, 9):
        oval(dark, x - r - 30, y - r // 2, r // 2, r)
        oval(dark, x + r // 2, y - r // 2, r // 2, r)
        oval(light, x - r - 20, y - r // 3, r // 4, r // 2)
        oval(light, x + r // 2 + 10, y - r // 3, r // 4, r // 2)
    if kind in (3, 11):
        for dx in (-r // 3, r // 3):
            oval((48, 126, 77), x + dx - r // 4, y - r - r // 3, r // 2, r)
    if kind in (7, 13) or species in (25, 133, 135):
        for dx in (-int(r * 0.75), int(r * 0.38)):
            oval(dark, x + dx, y - int(r * 1.25), r // 2, r)
            oval(light, x + dx + r // 8, y - int(r * 1.13), r // 4, int(r * 0.65))
    if kind in (6, 8, 12):
        for dx in (-int(r * 0.61), int(r * 0.43)):
            pygame.draw.polygon(canvas, dark, [(x + dx, y - r // 2), (x + dx + r // 4, y - r - r // 3), (x + dx + r // 2, y - r // 2)])
    oval(dark, x - r, y - r, int(2 * r), int(2 * r))
    oval(main, x - r + 8, y - r + 7, int(2 * r - 16), int(2 * r - 16))
    oval(light, x - r // 2, y + r // 6, r, int(r * 0.67))
    if species in (1, 2, 3):
        oval((46, 134, 81), x - r // 2, y - r - int(r * 0.37), int(r * 1.07), int(r * 0.77))
        oval((90, 183, 101), x - r // 3, y - r - int(r * 0.37), int(r * 0.7), int(r * 0.46))
    if species in (4, 5, 6):
        oval((255, 211, 89), x + r - 12, y - r, 40, 53)
    if species in (7, 8, 9):
        oval((117, 95, 71), x + r // 4, y - r // 5, int(r * 0.75), int(r * 0.9))
    for dx in (-int(r * 0.39), int(r * 0.19)):
        oval(PAPER, x + dx, y - int(r * 0.36), int(r * 0.23), int(r * 0.31))
        oval((30, 52, 61), x + dx + int(r * 0.08), y - int(r * 0.31), int(r * 0.11), int(r * 0.19))
    pygame.draw.arc(canvas, (50, 67, 72), (x - int(r * 0.16), y + int(r * 0.16), int(r * 0.33), int(r * 0.29)), 0.15, 2.7, 4)

def render_battle(hero, enemy, trainer):
    global battle_screen_is_drawn, displayed_battle_pokemon, current_battle_hero, current_battle_enemy, current_battle_trainer
    current_battle_hero, current_battle_enemy, current_battle_trainer = (hero, enemy, trainer)
    ui_frame('TRAINER BATTLE' if trainer else 'WILD ENCOUNTER', 'Choose your next move wisely.', 'BATTLE')
    ui_box(70, 254, 1280, 702, (41, 75, 79), 29, (72, 108, 104))
    ui_box(100, 288, 1218, 618, (55, 102, 103), 22)
    ui_glow(1006, 493, 220, (112, 202, 161))
    ui_glow(391, 728, 200, (92, 170, 200))
    draw_pokemon_icon(1040, 501, enemy, 1.4)
    draw_pokemon_icon(405, 729, hero, 1.65)
    ui_box(140, 314, 460, 151, NAVY, 22)
    ui_box(795, 712, 470, 166, NAVY, 22)
    ui_text(pokemon_name(enemy[0]), 164, 335, 39, PAPER, True, 380)
    ui_pill('LV ' + str(enemy[1]), 480, 335, CARD_2, PAPER, 100)
    ui_text(pokemon_name(hero[0]), 821, 729, 37, PAPER, True, 300)
    ui_pill('LV ' + str(hero[1]), 1143, 732, CARD_2, PAPER, 100)
    battle_screen_is_drawn = True
    displayed_battle_pokemon = hero
    render_battle_health(hero, enemy)
    restore_battle_menu(hero, enemy, trainer)
    render_battle_footer('1  FIGHT          2  BAG          3  SWITCH          4  RUN')

def render_battle_health(hero, enemy):
    ui_box(160, 402, 405, 48, NAVY, 10)
    ui_health_bar(166, 412, 260, 24, enemy[2], max_health(enemy))
    ui_text(f'{enemy[2]} / {max_health(enemy)}', 547, 404, 22, PAPER, True, align='right')
    ui_box(815, 797, 430, 59, NAVY, 10)
    ui_health_bar(825, 817, 268, 24, hero[2], max_health(hero))
    ui_text(f'{hero[2]} / {max_health(hero)}', 1230, 808, 24, PAPER, True, align='right')

def render_battle_footer(label):
    ui_box(70, 971, 1780, 64, CARD, 16)
    ui_text(str(label), 104, 985, 28, PAPER, True, max_width=1704)

def show_battle_notice(label):
    render_battle_footer(label + '     •     PRESS ENTER')
    wait_key()

def draw_battle_menu_row(options, idx, selected):
    y = 432 + idx * 105
    ui_box(1436, y, 382, 84, TEAL if selected else CARD_2, 18)
    if selected:
        ui_box(1438, y + 14, 7, 55, GOLD, 3)
    ui_text(f'{idx + 1:02d}', 1464, y + 23, 26, GOLD if selected else MUTED, True)
    ui_text(options[idx], 1530, y + 17, 36, PAPER, selected, max_width=254)

def restore_battle_menu(hero, foe, trainer):
    ui_box(1391, 255, 460, 705, DARK, 27, (61, 88, 88))
    ui_pill('ACTION PANEL', 1435, 287, TEAL)
    ui_text('Choose action', 1438, 344, 36, PAPER, True)
    ui_text('Arrows • Enter • 1–4', 1438, 392, 24, MUTED)
    for j, label in enumerate(('Fight', 'Bag', 'Switch', 'Run')):
        draw_battle_menu_row(('Fight', 'Bag', 'Switch', 'Run'), j, False)

def choose_battle_action(hero, foe, trainer, title, options):
    if not battle_screen_is_drawn or hero is not displayed_battle_pokemon:
        render_battle(hero, foe, trainer)
    selected = 0
    count = len(options)
    while True:
        ui_box(1391, 255, 460, 705, DARK, 27, (61, 88, 88))
        ui_pill('BATTLE ACTION', 1435, 287, TEAL)
        ui_text(title.title(), 1438, 344, 38, PAPER, True, max_width=375)
        ui_text('Select with arrows or 1–4', 1438, 391, 24, MUTED)
        for index in range(count):
            draw_battle_menu_row(options, index, index == selected)
        key = wait_key()
        if key in (KEY_UP, KEY_LEFT):
            selected = (selected - 1) % count
        elif key in (KEY_DOWN, KEY_RIGHT):
            selected = (selected + 1) % count
        elif key == KEY_CONFIRM:
            restore_battle_menu(hero, foe, trainer)
            return selected
        elif key == KEY_CANCEL:
            restore_battle_menu(hero, foe, trainer)
            return -1
        elif key in (KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR):
            index = (KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR).index(key)
            if index < count:
                restore_battle_menu(hero, foe, trainer)
                return index

def draw_terrain_tile(x, y):
    kind = terrain_at(x, y)
    sx = MAP_X + x * TILE
    sy = MAP_Y + y * TILE
    i = x * 31 + y * 13 + current_area * 17
    if kind == '#':
        pygame.draw.rect(canvas, (47, 99, 71), (sx, sy, TILE, TILE))
        pygame.draw.rect(canvas, (30, 76, 55), (sx + 9, sy + 3, 46, 47))
        pygame.draw.rect(canvas, (98, 79, 60), (sx + 25, sy + 46, 14, 18))
        pygame.draw.rect(canvas, (61, 139, 76), (sx + 5, sy + 4, 13, 14))
    elif kind == 'g':
        pygame.draw.rect(canvas, (115, 178, 102), (sx, sy, TILE, TILE))
        pygame.draw.line(canvas, (50, 139, 75), (sx + 15, sy + 46), (sx + 15, sy + 20), 4)
        pygame.draw.line(canvas, (45, 128, 68), (sx + 32, sy + 42), (sx + 38, sy + 16), 4)
        pygame.draw.line(canvas, (76, 160, 82), (sx + 47, sy + 49), (sx + 53, sy + 29), 4)
    elif kind == '.':
        pygame.draw.rect(canvas, (215, 202, 161), (sx, sy, TILE, TILE))
        for px, py in ((11, 17), (39, 33), (49, 11)):
            pygame.draw.circle(canvas, (203, 185, 148), (sx + (px + i) % 57, sy + (py + i) % 55), 2)
    elif kind == 'w':
        pygame.draw.rect(canvas, (77, 151, 196), (sx, sy, TILE, TILE))
        pygame.draw.line(canvas, (131, 203, 223), (sx + 10, sy + 20), (sx + 47, sy + 20), 4)
        pygame.draw.line(canvas, (126, 199, 221), (sx + 17, sy + 43), (sx + 55, sy + 43), 4)
    elif kind == 'r':
        pygame.draw.rect(canvas, (119, 125, 116), (sx, sy, TILE, TILE))
        pygame.draw.polygon(canvas, (176, 175, 152), [(sx + 9, sy + 50), (sx + 25, sy + 12), (sx + 52, sy + 20), (sx + 57, sy + 51)])
        pygame.draw.line(canvas, (95, 99, 97), (sx + 36, sy + 26), (sx + 29, sy + 46), 4)
    else:
        draw_landmark(kind, sx, sy)
    # No tile outlines: neighboring terrain cells meet edge-to-edge.

def draw_player():
    sx = MAP_X + player_x * TILE
    sy = MAP_Y + player_y * TILE
    factor = TILE / 64.0

    def r(x, y, w, h, color, rounding=0):
        pygame.draw.rect(canvas, color, (sx + round(x * factor), sy + round(y * factor), round(w * factor), round(h * factor)), border_radius=round(rounding * factor))

    def circ(x, y, radius, color):
        pygame.draw.circle(canvas, color, (sx + round(x * factor), sy + round(y * factor)), round(radius * factor))
    pygame.draw.ellipse(canvas, (36, 69, 64), (sx + round(7 * factor), sy + round(53 * factor), round(50 * factor), round(9 * factor)))
    r(21, 28, 26, 27, (41, 82, 178), 5)
    circ(33, 24, 17, (235, 182, 133))
    r(14, 8, 38, 12, (194, 76, 85), 6)
    r(14, 18, 39, 7, (236, 227, 206), 3)
    circ(26, 24, 2, (37, 53, 61))
    circ(40, 24, 2, (37, 53, 61))

def render_overworld():
    global overworld_is_drawn
    ui_frame(AREA_NAMES[current_area].title(), 'Explore the region. Walk into buildings to interact.', 'OVERWORLD')
    ui_box(MAP_X - 11, MAP_Y - 11, MAP_W + 22, MAP_H + 22, (39, 76, 76), 20)
    for y in range(12):
        for x in range(20):
            draw_terrain_tile(x, y)
    draw_player()
    ui_box(PANEL_X, 268, 603, 678, CARD, 24)
    ui_pill('TRAINER OVERVIEW', PANEL_X + 36, 297, TEAL)
    ui_text('Your adventure', PANEL_X + 36, 357, 39, PAPER, True)
    ui_rule(PANEL_X + 36, 420, 529)
    ui_text('BADGES', PANEL_X + 36, 448, 25, MUTED, True)
    ui_text(f'{earned_badge_count()} / 4', PANEL_X + 36, 489, 49, GOLD, True)
    ui_text('COINS', PANEL_X + 324, 448, 25, MUTED, True)
    ui_text(str(coins), PANEL_X + 324, 489, 49, MINT, True)
    ui_rule(PANEL_X + 36, 552, 529)
    ui_text('ACTIVE PARTY', PANEL_X + 36, 577, 26, MUTED, True)
    for index, mon in enumerate(party[:4]):
        yy = 624 + index * 77
        ui_box(PANEL_X + 29, yy, 542, 67, DARK, 13)
        ui_text(pokemon_name(mon[0]), PANEL_X + 51, yy + 9, 27, PAPER, True, 333)
        ui_text(f'Lv {mon[1]}', PANEL_X + 522, yy + 12, 23, MINT, align='right')
        ui_health_bar(PANEL_X + 50, yy + 49, 485, 10, mon[2], max_health(mon))
    ui_footer('ARROWS / WASD  Move      ENTER  Menu      ESC  Pause')
    overworld_is_drawn = True

def earned_badge_count():
    return (earned_badges & 1 > 0) + (earned_badges & 2 > 0) + (earned_badges & 4 > 0) + (earned_badges & 8 > 0)

def terrain_at(x, y):
    if y < 0 or y > 11:
        return '#'
    if x == 0 or x == 19:
        return '.' if y == 6 else '#'
    if y == 0 or y == 11:
        return '#'
    if x == 6 and y == 3 and (current_area in (0, 3, 5, 7, 9, 11)):
        return 'H'
    if x == 13 and y == 3 and (current_area in (0, 3, 5, 7, 9)):
        return 'S'
    if x == 10 and y == 3 and (current_area in (3, 5, 7, 9, 11)):
        return 'G'
    if x == 5 and y == 6 and (current_area in (1, 2, 4, 6, 8, 10, 11)):
        return 'T' if not defeated_trainers & 1 << current_area else '.'
    if x == 15 and y == 9 and (current_area != 0):
        return 'I' if not collected_treasures & 1 << current_area else '.'
    if current_area == 12 and x == 10 and (y == 2):
        return 'C'
    if y == 6 or x == 10:
        return '.'
    if current_area in (5, 12) and (x + y * 3 + current_area) % 7 == 0:
        return 'w'
    if current_area in (4, 10, 11) and (x * 3 + y + current_area) % 7 == 0:
        return 'r'
    if (x * 7 + y * 13 + current_area * 11) % 19 == 0:
        return '#'
    if current_area in (0, 3, 5, 7, 9, 11):
        return 'g' if (x * 3 + y * 5) % 7 == 0 else '.'
    return 'g' if (x * 5 + y * 11 + current_area) % 7 < 5 else '.'

def is_blocked(x, y):
    return terrain_at(x, y) in ('#', 'w', 'r')

def can_enter_area(nextarea):
    if nextarea >= 14:
        return False
    if nextarea >= 12 and (not champion_defeated):
        show_message('Beat the Crown Champion', 'to reach the postgame!')
        return False
    for milestone, flag in ((4, 1), (6, 2), (8, 4), (10, 8)):
        if nextarea >= milestone and (not earned_badges & flag):
            show_message('The gate is locked.', 'Earn the next gym badge!')
            return False
    return True

def move_player(dx, dy):
    global current_area, player_x, player_y, steps_taken, overworld_is_drawn
    x = player_x + dx
    y = player_y + dy
    if y < 1 or y > 10:
        return
    if x < 0:
        if current_area == 0:
            return
        current_area -= 1
        player_x = 18
        player_y = 6
        overworld_is_drawn = False
        return
    if x > 19:
        if not can_enter_area(current_area + 1):
            return
        current_area += 1
        player_x = 1
        player_y = 6
        overworld_is_drawn = False
        return
    if is_blocked(x, y):
        return
    oldx = player_x
    oldy = player_y
    player_x = x
    player_y = y
    steps_taken += 1
    if overworld_is_drawn:
        draw_terrain_tile(oldx, oldy)
        draw_player()
    t = terrain_at(x, y)
    if t == 'H':
        for p in party:
            p[2] = max_health(p)
        show_message('Your party is healed!')
    elif t == 'S':
        visit_shop()
    elif t == 'G':
        challenge_gym()
    elif t == 'T':
        start_trainer_battle()
    elif t == 'I':
        collect_treasure()
    elif t == 'C':
        start_legendary_encounter()
    elif t == 'g' and current_area != 0:
        rate = 21 if current_area != 13 else 33
        if randint(1, 100) <= rate:
            start_wild_encounter()

def collect_treasure():
    global collected_treasures, capture_orbs, healing_potions, coins, great_capture_orbs
    collected_treasures |= 1 << current_area
    if current_area % 3 == 0:
        great_capture_orbs += 2
        show_message('Found 2 Great Orbs!')
    elif current_area % 3 == 1:
        healing_potions += 3
        show_message('Found 3 Potions!')
    else:
        coins += 300
        capture_orbs += 2
        show_message('Found 300 coins', 'and 2 Capture Orbs!')

def visit_shop():
    global coins, capture_orbs, great_capture_orbs, healing_potions, super_healing_potions
    while True:
        j = choose_menu('SHOP - %d COINS' % coins, ['Orb 100 (%d)' % capture_orbs, 'Great Orb 300 (%d)' % great_capture_orbs, 'Potion 120 (%d)' % healing_potions, 'Super Potion 350 (%d)' % super_healing_potions, 'Leave'])
        if j < 0 or j == 4:
            return
        price = (100, 300, 120, 350)[j]
        if coins < price:
            show_message('Not enough coins!')
            continue
        coins -= price
        if j == 0:
            capture_orbs += 1
        elif j == 1:
            great_capture_orbs += 1
        elif j == 2:
            healing_potions += 1
        else:
            super_healing_potions += 1
        show_message('Purchase successful!')

def perform_attack(a, d, mid):
    nam, typ, power, acc = BATTLE_MOVES[mid]
    if randint(1, 100) > acc:
        return (nam + ' missed!', 0)
    a1, a2 = pokemon_types(a[0])
    mul = type_multiplier(typ, d)
    if mul == 0:
        return ('No effect!', 0)
    stab = 1.25 if typ == a1 or typ == a2 else 1
    crit = 1.45 if randint(1, 16) == 1 else 1
    damage = int(((2 * a[1] / 5 + 2) * power * attack_stat(a) / (defense_stat(d) * 50) + 2) * stab * crit * mul * randint(85, 100) / 100)
    damage = max(1, damage)
    d[2] = max(0, d[2] - damage)
    text1 = nam + ' -' + str(damage) + ' HP'
    if mul > 1:
        text1 += ' SUPER!'
    elif mul < 1:
        text1 += ' resisted'
    return (text1, damage)

def award_experience(mon, foe_level):
    mon[3] += max(3, foe_level // 2 + 3)
    needed = mon[1] * 2 + 5
    if mon[1] < 75 and mon[3] >= needed:
        mon[3] -= needed
        mon[1] += 1
        mon[2] = max_health(mon)
        show_message(pokemon_name(mon[0]) + ' grew to', 'level %d!' % mon[1])
        try_evolution(mon)

def try_evolution(mon):
    old = mon[0]
    if old not in EVOLUTION_RULES:
        return
    level, to = EVOLUTION_RULES[old]
    if mon[1] < level:
        return
    if old == 133:
        j = choose_menu('EEVEE IS EVOLVING!', ['Vaporeon', 'Jolteon', 'Flareon', 'Cancel'])
        if j < 0 or j == 3:
            return
        to = (134, 135, 136)[j]
    mon[0] = to
    mon[2] = max_health(mon)
    set_species_flag(seen_species, to)
    set_species_flag(caught_species, to)
    show_message(pokemon_name(old) + ' evolved into', pokemon_name(to) + '!')

def apply_healing_item(mon, superp=False):
    global healing_potions, super_healing_potions
    if mon[2] <= 0:
        show_message('Fainted creatures need', 'a healing station.')
        return False
    if mon[2] >= max_health(mon):
        show_message('Already at full HP!')
        return False
    if superp:
        if super_healing_potions <= 0:
            show_message('No Super Potions!')
            return False
        super_healing_potions -= 1
        heal = 100
    else:
        if healing_potions <= 0:
            show_message('No Potions!')
            return False
        healing_potions -= 1
        heal = 35
    mon[2] = min(max_health(mon), mon[2] + heal)
    show_message('Healed ' + pokemon_name(mon[0]) + '!')
    return True

def open_battle_bag(enemy):
    global capture_orbs, great_capture_orbs
    j = choose_menu('BATTLE BAG', ['Capture Orb x%d' % capture_orbs, 'Great Orb x%d' % great_capture_orbs, 'Potion x%d' % healing_potions, 'Super Potion x%d' % super_healing_potions, 'Cancel'])
    if j < 0 or j == 4:
        return 0
    if j in (0, 1):
        if len(party) >= 6 and len(storage_box) >= 30:
            show_message('Party and box are full!')
            return 0
        if j == 0:
            if capture_orbs <= 0:
                show_message('No Orbs left!')
                return 0
            capture_orbs -= 1
            boost = 0
        else:
            if great_capture_orbs <= 0:
                show_message('No Great Orbs left!')
                return 0
            great_capture_orbs -= 1
            boost = 25
        hp_fraction = (max_health(enemy) - enemy[2]) * 50 // max_health(enemy)
        chance = clamp(25 + hp_fraction + boost - enemy[1] // 2, 5, 90)
        if enemy[0] >= 144:
            chance = chance // 3
        if randint(1, 100) <= chance:
            capture_pokemon(enemy)
            return 2
        show_message('The Orb burst open!')
        return 1
    who = choose_party_pokemon('HEAL WHICH CREATURE?')
    if who < 0:
        return 0
    return 1 if apply_healing_item(party[who], j == 3) else 0

def capture_pokemon(enemy):
    got = [enemy[0], enemy[1], enemy[2], enemy[3]]
    set_species_flag(caught_species, got[0])
    set_species_flag(seen_species, got[0])
    if len(party) < 6:
        party.append(got)
        show_message('Caught ' + pokemon_name(got[0]) + '!', 'Added to your team.')
    else:
        storage_box.append([got[0], got[1], got[3]])
        show_message('Caught ' + pokemon_name(got[0]) + '!', 'Sent to storage box.')

def enemy_turn(foe, hero):
    m = available_moves(foe)
    chosen = m[randint(0, 3)]
    s, _ = perform_attack(foe, hero, chosen)
    render_battle_health(hero, foe)
    show_battle_notice(pokemon_name(foe[0])[:9] + ': ' + s)
    if hero[2] <= 0:
        show_battle_notice(pokemon_name(hero[0]) + ' fainted!')

def run_battle(foes, is_trainer=False, reward=0):
    global coins, current_area, player_x, player_y
    if first_healthy_party_index() < 0:
        show_message('Your party cannot fight.', 'Heal at a red H station!')
        return False
    for foe in foes:
        set_species_flag(seen_species, foe[0])
        render_battle(party[first_healthy_party_index()], foe, is_trainer)
        show_battle_notice(('Trainer: ' if is_trainer else 'Wild: ') + pokemon_name(foe[0]) + '!')
        while foe[2] > 0:
            index = first_healthy_party_index()
            if index < 0:
                show_message('Your party fainted!', 'Returning to Pine Town.')
                current_area = 0
                player_x = 2
                player_y = 6
                for q in party:
                    q[2] = max_health(q)
                return False
            hero = party[index]
            j = choose_battle_action(hero, foe, is_trainer, 'YOUR TURN', ['Fight', 'Bag', 'Switch', 'Run'])
            if j == 0:
                ms = available_moves(hero)
                options = []
                for mid in ms:
                    m = BATTLE_MOVES[mid]
                    options.append(m[0] + ' ' + str(m[2]))
                m = choose_battle_action(hero, foe, is_trainer, 'CHOOSE MOVE', options)
                if m < 0:
                    continue
                enemy_acted = False
                if speed_stat(hero) < speed_stat(foe) and randint(1, 3) == 1:
                    enemy_turn(foe, hero)
                    enemy_acted = True
                    if hero[2] <= 0:
                        continue
                s, _ = perform_attack(hero, foe, ms[m])
                render_battle_health(hero, foe)
                show_battle_notice(pokemon_name(hero[0])[:9] + ': ' + s)
                if foe[2] <= 0:
                    break
                if not enemy_acted:
                    enemy_turn(foe, hero)
            elif j == 1:
                if is_trainer:
                    j2 = choose_menu('TRAINER BATTLE', ['Potion', 'Super Potion', 'Back'])
                    if j2 < 0 or j2 == 2:
                        continue
                    idx = choose_party_pokemon('HEAL WHO?')
                    if idx < 0:
                        continue
                    if apply_healing_item(party[idx], j2 == 1):
                        render_battle(hero, foe, is_trainer)
                        enemy_turn(foe, hero)
                else:
                    used = open_battle_bag(foe)
                    if used == 2:
                        return True
                    if used == 1:
                        render_battle(hero, foe, is_trainer)
                        enemy_turn(foe, hero)
            elif j == 2:
                k = choose_party_pokemon('SWITCH INTO?', True)
                if k < 0 or party[k][2] <= 0:
                    continue
                if k != index:
                    party.insert(0, party.pop(k))
                    render_battle(party[0], foe, is_trainer)
                    enemy_turn(foe, party[0])
            elif j == 3:
                if is_trainer:
                    show_message('Cannot flee from trainers!')
                elif randint(1, 100) < 75:
                    show_message('Escaped safely!')
                    return False
                else:
                    render_battle(hero, foe, is_trainer)
                    show_battle_notice('Could not escape!')
                    enemy_turn(foe, hero)
            else:
                continue
        show_battle_notice('Defeated ' + pokemon_name(foe[0]) + '!')
        award_experience(party[first_healthy_party_index()], foe[1])
    coins += reward
    if reward:
        show_message('Victory! +%d coins' % reward)
    return True

def start_wild_encounter():
    if current_area == 13:
        sid = randint(1, 151)
    else:
        ids = WILD_ENCOUNTER_POOLS[current_area].split()
        sid = int(ids[randint(0, len(ids) - 1)])
    level = clamp(4 + current_area * 4 + randint(-2, 3), 2, 68)
    if current_area == 13:
        level = randint(30, 64)
    foe = create_pokemon(sid, level)
    run_battle([foe], False, 30 + current_area * 8)

def start_trainer_battle():
    global defeated_trainers
    if defeated_trainers & 1 << current_area:
        return
    pool = WILD_ENCOUNTER_POOLS[current_area].split()
    p = []
    lvl = clamp(4 + current_area * 4, 4, 53)
    for j in range(2 + current_area // 7):
        p.append(create_pokemon(int(pool[(j * 7 + current_area) % len(pool)]), lvl + j))
    if run_battle(p, True, 150 + current_area * 60):
        defeated_trainers |= 1 << current_area
        show_message('Trainer defeated!', 'Your path is clear.')
        save_progress()

def challenge_gym():
    global earned_badges, champion_defeated
    if current_area == 11:
        if champion_defeated:
            show_message('The Champion welcomes', 'a rematch!')
        p = [create_pokemon(149, 48), create_pokemon(131, 49), create_pokemon(143, 50), create_pokemon(150, 53)]
        if run_battle(p, True, 3000):
            champion_defeated = 1
            show_message('YOU ARE THE CHAMPION!', 'Legend Lake and Safari open!')
            save_progress()
        return
    params = {3: ('Granite', 1, [(74, 12), (95, 14), (76, 16)]), 5: ('Marina', 2, [(60, 20), (121, 22), (130, 24)]), 7: ('Volt', 4, [(25, 28), (82, 30), (125, 33)]), 9: ('Shade', 8, [(92, 37), (93, 39), (94, 42)])}
    if current_area not in params:
        return
    leader, bit, data = params[current_area]
    if earned_badges & bit:
        show_message('Gym leader ' + leader + ':', 'You already won this badge.')
        return
    j = choose_menu('GYM LEADER ' + leader, ['Challenge', 'Not yet'])
    if j != 0:
        return
    enemies = []
    for sid, level in data:
        enemies.append(create_pokemon(sid, level))
    if run_battle(enemies, True, 500 + 200 * earned_badge_count()):
        earned_badges |= bit
        show_message('Won a new badge!', 'Badges: %d/4' % earned_badge_count())
        save_progress()

def start_legendary_encounter():
    pool = [144, 145, 146, 150, 151]
    n = pool[randint(0, 4)]
    show_message('A rare presence stirs...')
    run_battle([create_pokemon(n, 58 + randint(0, 6))], False, 800)

def choose_party_pokemon(title, alive_only=False):
    options = []
    ids = []
    for i in range(len(party)):
        p = party[i]
        if not alive_only or p[2] > 0:
            options.append(pokemon_name(p[0])[:15] + ' L%d' % p[1])
            ids.append(i)
    if not options:
        show_message('No available creatures.')
        return -1
    chosen = choose_menu(title, options)
    return ids[chosen] if chosen >= 0 else -1

def open_party_menu():
    while True:
        if not party:
            return
        opts = [f'{pokemon_name(p[0])}  •  Lv {p[1]}  •  {p[2]}/{max_health(p)} HP' for p in party]
        j = choose_menu('YOUR PARTY', opts)
        if j < 0:
            return
        mon = party[j]
        a, b = pokemon_types(mon[0])
        ui_frame(pokemon_name(mon[0]), f'Pokédex #{mon[0]:03d}  •  Party slot {j + 1}', 'POKÉMON')
        ui_box(75, 280, 986, 646, CARD, 28)
        ui_pill('CREATURE DETAILS', 121, 319, TEAL)
        ui_text('Level', 134, 401, 28, MUTED, True)
        ui_text(str(mon[1]), 133, 444, 56, GOLD, True)
        ui_text('Type', 380, 401, 28, MUTED, True)
        ui_text(type_name(a) + ' / ' + type_name(b), 377, 455, 39, PAPER, True, 630)
        ui_rule(130, 530, 865)
        ui_text('HEALTH', 134, 570, 26, MUTED, True)
        ui_text(f'{mon[2]} / {max_health(mon)}', 935, 568, 29, PAPER, True, align='right')
        ui_health_bar(132, 619, 867, 25, mon[2], max_health(mon))
        ui_text('EXPERIENCE', 134, 695, 26, MUTED, True)
        needed = mon[1] * 2 + 5
        ui_text(f'{mon[3]} / {needed}', 935, 695, 29, PAPER, True, align='right')
        ui_health_bar(132, 744, 867, 23, mon[3], needed)
        ui_box(1120, 280, 723, 646, DARK, 28)
        ui_glow(1482, 594, 236, (84, 173, 157))
        draw_pokemon_icon(1483, 600, mon, 1.72)
        ui_text('PRESS ENTER TO MANAGE', 1481, 862, 27, MINT, True, align='center')
        ui_footer('ENTER  Manage creature      ESC  Return')
        wait_key()
        ch = choose_menu(pokemon_name(mon[0]), ['Make leader', 'Use Potion', 'Super Potion', 'Back'])
        if ch == 0:
            party.insert(0, party.pop(j))
        elif ch == 1:
            apply_healing_item(mon, False)
        elif ch == 2:
            apply_healing_item(mon, True)

def choose_storage_pokemon(action):
    if not storage_box:
        return -1
    start = 0
    while True:
        part = storage_box[start:start + 5]
        options = [pokemon_name(p[0])[:17] + ' L%d' % p[1] for p in part]
        options.append('Next page')
        j = choose_menu(action + ' %d/%d' % (start + 1, len(storage_box)), options)
        if j < 0:
            return -1
        if j == len(part):
            start += 5
            if start >= len(storage_box):
                start = 0
        else:
            return start + j

def open_storage():
    while True:
        ch = choose_menu('STORAGE: %d / 30' % len(storage_box), ['Withdraw', 'Deposit', 'Release', 'Back'])
        if ch < 0 or ch == 3:
            return
        if ch == 0:
            if not storage_box:
                show_message('Your storage is empty.')
                continue
            if len(party) >= 6:
                show_message('Your party is full.')
                continue
            j = choose_storage_pokemon('WITHDRAW')
            if j < 0:
                continue
            item = storage_box.pop(j)
            mon = create_pokemon(item[0], item[1])
            mon[3] = item[2]
            party.append(mon)
            show_message('Withdrawn ' + pokemon_name(mon[0]) + '!')
        elif ch == 1:
            if len(party) <= 1:
                show_message('Keep at least one creature!')
                continue
            if len(storage_box) >= 30:
                show_message('Your box is full!')
                continue
            j = choose_party_pokemon('DEPOSIT WHO?')
            if j < 0:
                continue
            mon = party.pop(j)
            storage_box.append([mon[0], mon[1], mon[3]])
            show_message('Stored ' + pokemon_name(mon[0]) + '!')
        elif ch == 2:
            if not storage_box:
                show_message('Your storage is empty.')
                continue
            j = choose_storage_pokemon('RELEASE')
            if j < 0:
                continue
            n = pokemon_name(storage_box[j][0])
            c = choose_menu('RELEASE ' + n[:17] + '?', ['No, keep it', 'Yes, release'])
            if c == 1:
                storage_box.pop(j)
                show_message(n + ' was released.', 'Dex entry is retained.')

def open_pokedex():
    page = 0
    while True:
        ui_frame('POKÉDEX', f'151 species • Seen {count_species_flags(seen_species)} • Caught {count_species_flags(caught_species)}', 'COLLECTION')
        ui_box(76, 255, 1115, 696, CARD, 26)
        ui_pill(f'PAGE {page + 1} / 16', 118, 288, TEAL)
        for index in range(10):
            number = page * 10 + index + 1
            if number > 151:
                break
            yy = 369 + index * 54
            detected = has_species_flag(seen_species, number)
            acquired = has_species_flag(caught_species, number)
            if index % 2 == 0:
                ui_box(108, yy - 6, 1050, 48, CARD_2, 9)
            ui_text(f'{number:03d}', 130, yy + 2, 23, GOLD, True)
            ui_text(pokemon_name(number) if detected else 'Undiscovered', 232, yy, 27, PAPER if detected else MUTED, detected, 700)
            ui_pill('CAUGHT' if acquired else 'SEEN' if detected else 'UNKNOWN', 975, yy - 4, TEAL if acquired else MID, width=148)
        ui_box(1261, 255, 585, 696, DARK, 26)
        ui_text('Complete the Pokédex', 1298, 324, 37, PAPER, True, 512)
        ui_rule(1298, 382, 506)
        ui_text('Explore new regions', 1299, 424, 29, MINT, True)
        ui_text('to discover rare creatures.', 1299, 473, 25, PAPER)
        ui_text('Use LEFT / RIGHT', 1299, 614, 28, GOLD, True)
        ui_text('to change pages.', 1299, 652, 28, PAPER)
        ui_text('Press ENTER to inspect', 1299, 739, 26, MUTED)
        ui_text('a visible entry.', 1299, 778, 26, MUTED)
        ui_footer('← / →  Page      ENTER  Select entry      ESC  Return')
        key = wait_key()
        if key == KEY_CANCEL:
            return
        if key == KEY_LEFT:
            page = (page - 1) % 16
        if key == KEY_RIGHT:
            page = (page + 1) % 16
        if key == KEY_CONFIRM:
            choices = [f'{page * 10 + i + 1:03d}  ' + (pokemon_name(page * 10 + i + 1) if has_species_flag(seen_species, page * 10 + i + 1) else '???') for i in range(min(10, 151 - page * 10))]
            pick = choose_menu('SELECT POKÉDEX ENTRY', choices)
            if pick >= 0:
                n = page * 10 + pick + 1
                if has_species_flag(seen_species, n):
                    first, second = pokemon_types(n)
                    show_message(f'{n:03d}  {pokemon_name(n)}', f'{type_name(first)} / {type_name(second)}', 'Caught' if has_species_flag(caught_species, n) else 'Seen only')
                else:
                    show_message('This Pokémon has not been discovered yet.')

def show_trainer_card():
    ui_frame('TRAINER CARD', 'Your progress through Kanto Quest 151.', 'PROFILE')
    ui_box(85, 260, 1743, 688, CARD, 30)
    stats = [('BADGES', f'{earned_badge_count()} / 4'), ('COINS', str(coins)), ('POKÉDEX SEEN', f'{count_species_flags(seen_species)} / 151'), ('POKÉDEX CAUGHT', f'{count_species_flags(caught_species)} / 151'), ('STEPS TAKEN', f'{steps_taken:,}'), ('CHAMPION', 'YES' if champion_defeated else 'NOT YET')]
    for i, (label, value) in enumerate(stats):
        col = i % 3
        row = i // 3
        x = 126 + col * 552
        y = 317 + row * 232
        ui_box(x, y, 520, 192, DARK, 22)
        ui_text(label, x + 33, y + 32, 27, MUTED, True)
        ui_text(value, x + 31, y + 85, 49, MINT if i != 0 else GOLD, True, 445)
    ui_pill('CURRENT REGION', 127, 787, TEAL)
    ui_text(AREA_NAMES[current_area].title(), 129, 852, 37, PAPER, True)
    ui_footer('ENTER / ESC  Return')
    wait_key()

def show_controls():
    show_message('ARROWS / WASD: walk & select', 'ENTER: select / game menu', 'ESC / BACKSPACE: go back')
    show_message('Walk in tall grass to battle', 'H heals, S is a shop', 'G gym, T trainer, I treasure')
    show_message('Defeat four gyms & Champion', 'Catch all 151 Kanto species', 'Save data: kanto_save.json')

def open_game_menu():
    while True:
        j = choose_menu('ADVENTURE MENU', ['Party', 'Pokedex', 'Bag / Shop', 'Storage PC', 'Trainer / Save', 'Return'])
        if j < 0 or j == 5:
            return
        if j == 0:
            open_party_menu()
        elif j == 1:
            open_pokedex()
        elif j == 2:
            show_message('Orbs: %d / %d' % (capture_orbs, great_capture_orbs), 'Potions: %d / %d' % (healing_potions, super_healing_potions), 'Coins: %d' % coins)
        elif j == 3:
            open_storage()
        elif j == 4:
            sub = choose_menu('TRAINER / SAVE', ['Trainer card', 'Save game', 'Help', 'Back'])
            if sub == 0:
                show_trainer_card()
            elif sub == 1:
                save_with_confirmation()
            elif sub == 2:
                show_controls()

def save_progress():
    """Atomically write the current adventure to one local JSON file."""
    state = {'version': 1, 'area': current_area, 'player': {'x': player_x, 'y': player_y}, 'coins': coins, 'inventory': {'capture_orbs': capture_orbs, 'great_capture_orbs': great_capture_orbs, 'healing_potions': healing_potions, 'super_healing_potions': super_healing_potions}, 'badges': earned_badges, 'defeated_trainers': defeated_trainers, 'collected_treasures': collected_treasures, 'champion_defeated': champion_defeated, 'steps_taken': steps_taken, 'party': party, 'storage_box': storage_box, 'seen_species': seen_species, 'caught_species': caught_species}
    temporary_file = SAVE_FILE.with_suffix('.tmp')
    try:
        with temporary_file.open('w', encoding='utf-8') as stream:
            json.dump(state, stream, indent=2)
        temporary_file.replace(SAVE_FILE)
        return True
    except (OSError, ValueError, TypeError):
        return False

def save_with_confirmation():
    if save_progress():
        show_message('Adventure saved!', 'Resume from the title.')
    else:
        show_message('Save failed.', 'Check the save file location.')

def load_progress():
    """Load the desktop save after checking its shape and core values."""
    global current_area, player_x, player_y, coins, capture_orbs
    global great_capture_orbs, healing_potions, super_healing_potions
    global earned_badges, defeated_trainers, collected_treasures
    global champion_defeated, steps_taken, party, storage_box
    global seen_species, caught_species
    try:
        with SAVE_FILE.open('r', encoding='utf-8') as stream:
            state = json.load(stream)
        new_party = state['party']
        new_box = state['storage_box']
        new_seen = state['seen_species']
        new_caught = state['caught_species']
        if state['version'] != 1:
            return False
        if not (1 <= len(new_party) <= 6 and len(new_box) <= 30):
            return False
        if any((len(pokemon) != 4 or not 1 <= pokemon[0] <= 151 for pokemon in new_party)):
            return False
        if any((len(pokemon) != 3 or not 1 <= pokemon[0] <= 151 for pokemon in new_box)):
            return False
        if len(new_seen) != 6 or len(new_caught) != 6:
            return False
        position = state['player']
        if not (0 <= state['area'] < len(AREA_NAMES) and 0 <= position['x'] < 20 and (1 <= position['y'] <= 10)):
            return False
        items = state['inventory']
        current_area = state['area']
        player_x, player_y = (position['x'], position['y'])
        coins = state['coins']
        capture_orbs = items['capture_orbs']
        great_capture_orbs = items['great_capture_orbs']
        healing_potions = items['healing_potions']
        super_healing_potions = items['super_healing_potions']
        earned_badges = state['badges']
        defeated_trainers = state['defeated_trainers']
        collected_treasures = state['collected_treasures']
        champion_defeated = state['champion_defeated']
        steps_taken = state['steps_taken']
        party, storage_box = (new_party, new_box)
        seen_species, caught_species = (new_seen, new_caught)
        return True
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        return False

def choose_starter():
    global party
    j = choose_menu('CHOOSE STARTER', ['Bulbasaur - Grass', 'Charmander - Fire', 'Squirtle - Water'])
    if j < 0:
        j = 0
    sid = (1, 4, 7)[j]
    party = [create_pokemon(sid, 6)]
    set_species_flag(seen_species, sid)
    set_species_flag(caught_species, sid)
    show_message('Welcome to Kanto Quest!', pokemon_name(sid) + ' joins your party!', 'Explore, train and catch 151!')

def start_new_game():
    global current_area, player_x, player_y, coins, capture_orbs, great_capture_orbs, healing_potions, super_healing_potions
    global earned_badges, defeated_trainers, collected_treasures, champion_defeated, steps_taken, party, storage_box, seen_species, caught_species
    current_area = 0
    player_x = 2
    player_y = 6
    coins = 700
    capture_orbs = 8
    great_capture_orbs = 2
    healing_potions = 5
    super_healing_potions = 1
    earned_badges = 0
    defeated_trainers = 0
    collected_treasures = 0
    champion_defeated = 0
    steps_taken = 0
    party = []
    storage_box = []
    seen_species = [0] * 6
    caught_species = [0] * 6
    choose_starter()
    save_progress()

def main():
    global overworld_is_drawn
    while True:
        j = choose_menu('KANTO QUEST 151', ['Continue save', 'New adventure', 'Controls / help', 'Exit'])
        if j == 0:
            if not load_progress():
                show_message('No compatible save.', 'Start a new adventure!')
                continue
        elif j == 1:
            if load_progress():
                check = choose_menu('OVERWRITE SAVE?', ['Yes - new game', 'No - go back'])
                if check != 0:
                    continue
            start_new_game()
        elif j == 2:
            show_controls()
            continue
        else:
            return
        overworld_is_drawn = False
        while True:
            if not overworld_is_drawn:
                render_overworld()
            k = wait_key()
            if k == KEY_UP:
                move_player(0, -1)
            elif k == KEY_DOWN:
                move_player(0, 1)
            elif k == KEY_LEFT:
                move_player(-1, 0)
            elif k == KEY_RIGHT:
                move_player(1, 0)
            elif k in (KEY_CONFIRM, KEY_FIVE):
                open_game_menu()
            elif k == KEY_CANCEL:
                c = choose_menu('PAUSE', ['Save and title', 'Resume'])
                if c == 0:
                    if save_progress():
                        show_message('Saved! See you soon.')
                    else:
                        show_message('Save failed!')
                    break

# ---------------------------------------------------------------
# OneCompiler UI: compact, properly spaced 960 x 540 layout.
# The original game rules and save code above remain unchanged.
# ---------------------------------------------------------------

def ui_frame(title, subtitle='', section='ADVENTURE'):
    canvas.fill(NAVY)
    ui_box(0, 0, 960, 56, (19, 35, 44), 0)
    ui_box(26, 14, 29, 29, TEAL, 7)
    ui_text('K', 40, 16, 20, PAPER, True, align='center')
    ui_text('KANTO  /  QUEST', 67, 18, 19, PAPER, True)
    ui_box(796, 13, 138, 29, CARD_2, 15)
    ui_text(section, 865, 18, 16, MINT, True, align='center', max_width=122)
    ui_text(str(title).title(), 31, 68, 33, PAPER, True, 875)
    if subtitle:
        ui_text(subtitle, 33, 113, 19, MUTED, max_width=880)


def ui_footer(help_text='ARROWS / WASD  Navigate     ENTER  Select     ESC  Back'):
    ui_rule(28, 507, 904, (51, 82, 90))
    ui_text(help_text, 34, 514, 17, (173, 199, 197), max_width=897)


def ui_pill(text, x, y, color=TEAL, text_color=PAPER, width=None):
    f=ui_font(15, True)
    width=width or f.size(str(text))[0]+24
    ui_box(x,y,width,26,color,13)
    ui_text(text,x+width//2,y+4,15,text_color,True,align='center')


def show_message(*lines):
    global overworld_is_drawn, battle_screen_is_drawn
    overworld_is_drawn = battle_screen_is_drawn = False
    ui_frame('Adventure update', 'A new event in your journey.', 'MESSAGE')
    ui_box(32,155,896,325,CARD,19,(65,102,108))
    ui_pill('NEW MESSAGE',58,174)
    y=221
    for line in lines:
        text=str(line)
        words=text.split()
        current=''
        for word in words:
            candidate=(current+' '+word).strip()
            if ui_font(27,True).size(candidate)[0]>815 and current:
                ui_text(current,62,y,27,PAPER,True)
                y+=45
                current=word
            else: current=candidate
        if current:
            ui_text(current,62,y,27,PAPER,True,810)
            y+=49
    ui_text('PRESS ENTER TO CONTINUE',63,443,18,MINT,True)
    ui_footer()
    wait_key()


def menu_layout(count,first):
    visible=min(7,max(0,count-first))
    height=40+max(0,visible-1)*45
    return 151+(330-height)//2,45


def draw_menu_row(options,index,selected,first,top,step):
    yy=top+(index-first)*step
    ui_box(49,yy,528,40,TEAL if selected else CARD_2,10)
    if selected:
        ui_box(49,yy+6,5,28,GOLD,2)
        ui_text('›',66,yy+7,22,GOLD,True)
    ui_text(str(options[index]),91 if selected else 68,yy+6,25,PAPER if selected else (198,224,221),selected,461)


def choose_menu(title, options, initial=0):
    if not options:return -1
    count=len(options);selected=clamp(initial,0,count-1)
    while True:
        first=(selected//7)*7
        ui_frame(title,'Choose an option to continue.','MENU')
        ui_box(30,151,564,330,DARK,16,(53,84,90))
        top,step=menu_layout(count,first)
        for n in range(first,min(first+7,count)):
            draw_menu_row(options,n,n==selected,first,top,step)
        ui_box(613,151,317,330,CARD,16)
        ui_pill('ADVENTURE STATUS',636,169)
        ui_text('Your adventure',637,214,27,PAPER,True,270)
        ui_rule(637,254,267)
        ui_text('BADGES',639,267,15,MUTED,True)
        ui_text(f'{earned_badge_count()} / 4',639,291,29,GOLD,True)
        ui_text('COINS',787,267,15,MUTED,True)
        ui_text(str(coins),787,291,29,MINT,True)
        ui_rule(637,336,267)
        ui_text('LOCATION',639,353,15,MUTED,True)
        ui_text(AREA_NAMES[current_area].title(),638,377,24,PAPER,True,272)
        ui_text(f'{selected+1} of {count} selected',638,445,17,MUTED)
        ui_footer('↑ / ↓  Choose     ENTER  Select     ESC  Back      1–6  Quick select')
        key=wait_key()
        if key==KEY_UP:selected=(selected-1)%count
        elif key==KEY_DOWN:selected=(selected+1)%count
        elif key==KEY_CONFIRM:return selected
        elif key==KEY_CANCEL:return -1
        elif key in (KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR,KEY_FIVE,KEY_SIX):
            q=(KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR,KEY_FIVE,KEY_SIX).index(key)
            if q<count:return q


def draw_terrain_tile(x,y):
    kind=terrain_at(x,y)
    sx=MAP_X+x*TILE;sy=MAP_Y+y*TILE
    num=x*31+y*13+current_area*17
    if kind=='#':
        pygame.draw.rect(canvas,(49,105,69),(sx,sy,TILE,TILE))
        pygame.draw.rect(canvas,(28,77,51),(sx+5,sy+2,17,20))
        pygame.draw.rect(canvas,(108,83,57),(sx+12,sy+20,5,7))
    elif kind=='g':
        pygame.draw.rect(canvas,(123,181,106),(sx,sy,TILE,TILE))
        for dx,dy in ((5,5),(15,10),(9,18)):
            pygame.draw.line(canvas,(52,136,67),(sx+dx,sy+dy+5),(sx+dx+2,sy+dy),2)
    elif kind=='.':
        pygame.draw.rect(canvas,(214,201,163),(sx,sy,TILE,TILE))
        pygame.draw.circle(canvas,(196,182,148),(sx+6+(num%12),sy+6+(num%7)),1)
    elif kind=='w':
        pygame.draw.rect(canvas,(69,147,193),(sx,sy,TILE,TILE))
        pygame.draw.line(canvas,(154,211,224),(sx+4,sy+9),(sx+19,sy+9),2)
    elif kind=='r':
        pygame.draw.rect(canvas,(118,125,120),(sx,sy,TILE,TILE))
        pygame.draw.polygon(canvas,(170,174,155),[(sx+4,sy+23),(sx+12,sy+4),(sx+23,sy+20)])
    else:draw_landmark(kind,sx,sy)
    # No tile outlines: neighboring terrain cells meet edge-to-edge.


def draw_player():
    sx=MAP_X+player_x*TILE;sy=MAP_Y+player_y*TILE
    pygame.draw.ellipse(canvas,(31,66,65),(sx+4,sy+23,19,4))
    pygame.draw.rect(canvas,(43,83,183),(sx+7,sy+12,14,13),border_radius=2)
    pygame.draw.circle(canvas,(240,185,131),(sx+14,sy+11),8)
    pygame.draw.rect(canvas,(202,73,80),(sx+4,sy+5,20,6),border_radius=2)
    pygame.draw.rect(canvas,(249,239,211),(sx+5,sy+9,18,3))


def render_overworld():
    global overworld_is_drawn
    ui_frame(AREA_NAMES[current_area].title(),'Explore the region. Enter buildings to interact.','OVERWORLD')
    ui_box(23,137,554,340,(40,79,77),13)
    for y in range(12):
        for x in range(20):draw_terrain_tile(x,y)
    draw_player()
    ui_box(602,137,331,340,CARD,13)
    ui_pill('TRAINER OVERVIEW',623,155)
    ui_text('Your adventure',624,191,26,PAPER,True)
    ui_rule(625,228,282)
    ui_text('BADGES',626,240,15,MUTED,True)
    ui_text(f'{earned_badge_count()} / 4',626,258,29,GOLD,True)
    ui_text('COINS',788,240,15,MUTED,True)
    ui_text(str(coins),788,258,29,MINT,True)
    ui_rule(625,299,282)
    ui_text('ACTIVE PARTY',626,308,16,MUTED,True)
    for idx,mon in enumerate(party[:4]):
        yy=335+idx*34
        ui_box(623,yy,287,31,DARK,7)
        ui_text(pokemon_name(mon[0]),634,yy+4,18,PAPER,True,194)
        ui_text('Lv '+str(mon[1]),896,yy+5,16,MINT,align='right')
        ui_health_bar(634,yy+24,263,4,mon[2],max_health(mon))
    ui_footer('ARROWS / WASD  Move     ENTER  Menu     ESC  Pause')
    overworld_is_drawn=True


def render_battle(hero,enemy,trainer):
    global battle_screen_is_drawn,displayed_battle_pokemon,current_battle_hero,current_battle_enemy,current_battle_trainer
    current_battle_hero,current_battle_enemy,current_battle_trainer=hero,enemy,trainer
    ui_frame('TRAINER BATTLE' if trainer else 'WILD ENCOUNTER','Choose your next move wisely.','BATTLE')
    ui_box(27,145,575,321,(43,82,83),17,(68,110,106))
    ui_box(43,161,543,290,(53,105,107),12)
    ui_glow(452,270,90,(104,193,161))
    ui_glow(185,370,90,(94,169,202))
    draw_pokemon_icon(455,271,enemy,0.68)
    draw_pokemon_icon(182,376,hero,0.72)
    battle_screen_is_drawn=True;displayed_battle_pokemon=hero
    render_battle_health(hero,enemy)
    restore_battle_menu(hero,enemy,trainer)
    render_battle_footer('1 FIGHT       2 BAG       3 SWITCH       4 RUN')


def render_battle_health(hero,enemy):
    ui_box(57,176,224,77,NAVY,12)
    ui_text(pokemon_name(enemy[0]),69,180,22,PAPER,True,155)
    ui_text('Lv '+str(enemy[1]),269,182,17,MINT,align='right')
    ui_health_bar(69,216,132,11,enemy[2],max_health(enemy))
    ui_text(f'{enemy[2]}/{max_health(enemy)}',267,211,16,PAPER,True,align='right')
    ui_box(310,368,255,77,NAVY,12)
    ui_text(pokemon_name(hero[0]),323,373,22,PAPER,True,164)
    ui_text('Lv '+str(hero[1]),550,373,17,MINT,align='right')
    ui_health_bar(323,413,147,10,hero[2],max_health(hero))
    ui_text(f'{hero[2]}/{max_health(hero)}',551,407,16,PAPER,True,align='right')


def render_battle_footer(label):
    ui_box(28,474,905,30,CARD,7)
    ui_text(label,40,478,19,PAPER,True,870)


def show_battle_notice(label):
    render_battle_footer(str(label)+'   -   PRESS ENTER')
    wait_key()


def draw_battle_menu_row(options,idx,selected):
    y=260+idx*46
    ui_box(638,y,278,40,TEAL if selected else CARD_2,9)
    if selected:ui_box(638,y+5,5,30,GOLD,2)
    ui_text(f'{idx+1:02}',651,y+8,20,GOLD if selected else MUTED,True)
    ui_text(options[idx],697,y+5,24,PAPER,selected,206)


def restore_battle_menu(hero,foe,trainer):
    ui_box(620,145,311,321,DARK,16,(63,92,94))
    ui_pill('BATTLE ACTION',639,163)
    ui_text('Arrow keys / Enter',642,234,17,MUTED)
    for idx,action in enumerate(('Fight','Bag','Switch','Run')):
        draw_battle_menu_row(('Fight','Bag','Switch','Run'),idx,False)


def choose_battle_action(hero,foe,trainer,title,options):
    if not battle_screen_is_drawn or hero is not displayed_battle_pokemon:
        render_battle(hero,foe,trainer)
    selected=0;count=len(options)
    while True:
        restore_battle_menu(hero,foe,trainer)
        ui_text(str(title).title(),642,199,25,PAPER,True,267)
        for idx in range(count):draw_battle_menu_row(options,idx,idx==selected)
        key=wait_key()
        if key in (KEY_UP,KEY_LEFT):selected=(selected-1)%count
        elif key in (KEY_DOWN,KEY_RIGHT):selected=(selected+1)%count
        elif key==KEY_CANCEL:
            restore_battle_menu(hero,foe,trainer);return -1
        elif key==KEY_CONFIRM:
            restore_battle_menu(hero,foe,trainer);return selected
        elif key in (KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR):
            q=(KEY_ONE,KEY_TWO,KEY_THREE,KEY_FOUR).index(key)
            if q<count:
                restore_battle_menu(hero,foe,trainer);return q


def open_party_menu():
    while True:
        if not party:return
        opts=[f'{pokemon_name(p[0])}  • Lv {p[1]} •  {p[2]}/{max_health(p)} HP' for p in party]
        idx=choose_menu('YOUR PARTY',opts)
        if idx<0:return
        mon=party[idx];a,b=pokemon_types(mon[0])
        ui_frame(pokemon_name(mon[0]),f'Pokédex #{mon[0]:03}   •   Party slot {idx+1}','POKÉMON')
        ui_box(30,153,575,325,CARD,16)
        ui_pill('CREATURE DETAILS',52,170)
        ui_text('LEVEL',57,213,18,MUTED,True)
        ui_text(str(mon[1]),58,235,38,GOLD,True)
        ui_text('TYPE',230,213,18,MUTED,True)
        ui_text(type_name(a)+' / '+type_name(b),230,241,25,PAPER,True,340)
        ui_rule(56,291,519)
        ui_text('HEALTH',58,308,17,MUTED,True)
        ui_text(f'{mon[2]} / {max_health(mon)}',569,307,18,PAPER,True,align='right')
        ui_health_bar(59,337,511,15,mon[2],max_health(mon))
        need=mon[1]*2+5
        ui_text('EXPERIENCE',58,376,17,MUTED,True)
        ui_text(f'{mon[3]} / {need}',569,374,18,PAPER,True,align='right')
        ui_health_bar(59,409,511,15,mon[3],need)
        ui_box(627,153,306,325,DARK,16)
        ui_glow(779,310,119,(85,173,159))
        draw_pokemon_icon(779,314,mon,0.94)
        ui_text('ENTER TO MANAGE',780,451,18,MINT,True,align='center')
        ui_footer('ENTER   Manage creature      ESC   Return')
        wait_key()
        choice=choose_menu(pokemon_name(mon[0]),['Make leader','Use Potion','Super Potion','Back'])
        if choice==0:party.insert(0,party.pop(idx))
        elif choice==1:apply_healing_item(mon,False)
        elif choice==2:apply_healing_item(mon,True)


def open_pokedex():
    page=0
    while True:
        ui_frame('POKÉDEX',f'151 species   •   Seen {count_species_flags(seen_species)}   •   Caught {count_species_flags(caught_species)}','COLLECTION')
        ui_box(30,149,580,335,CARD,15)
        ui_pill(f'PAGE {page+1} / 16',49,164)
        for idx in range(10):
            number=page*10+idx+1
            if number>151:break
            y=204+idx*26
            if idx%2==0:ui_box(44,y-2,550,25,CARD_2,5)
            detected=has_species_flag(seen_species,number)
            captured=has_species_flag(caught_species,number)
            ui_text(f'{number:03}',55,y+1,17,GOLD,True)
            ui_text(pokemon_name(number) if detected else 'Undiscovered',117,y,19,PAPER if detected else MUTED,detected,335)
            status='CAUGHT' if captured else 'SEEN' if detected else '—'
            ui_text(status,575,y+2,15,MINT if captured else MUTED,True,align='right')
        ui_box(629,149,302,335,DARK,15)
        ui_text('Complete the',649,179,25,PAPER,True)
        ui_text('Pokédex',649,209,25,PAPER,True)
        ui_rule(648,245,264)
        ui_text('Explore new regions',650,270,21,MINT,True)
        ui_text('to discover creatures.',650,301,20,PAPER)
        ui_text('LEFT / RIGHT',650,354,20,GOLD,True)
        ui_text('Change pages',650,385,19,PAPER)
        ui_text('ENTER: inspect entry',650,446,18,MUTED)
        ui_footer('← / →  Change page     ENTER  Select entry     ESC  Return')
        key=wait_key()
        if key==KEY_CANCEL:return
        if key==KEY_LEFT:page=(page-1)%16
        if key==KEY_RIGHT:page=(page+1)%16
        if key==KEY_CONFIRM:
            options=[f'{page*10+i+1:03}  '+(pokemon_name(page*10+i+1) if has_species_flag(seen_species,page*10+i+1) else '???') for i in range(min(10,151-page*10))]
            selected=choose_menu('SELECT POKÉDEX ENTRY',options)
            if selected>=0:
                n=page*10+selected+1
                if has_species_flag(seen_species,n):
                    first,second=pokemon_types(n)
                    show_message(f'{n:03} {pokemon_name(n)}',type_name(first)+' / '+type_name(second),'Caught' if has_species_flag(caught_species,n) else 'Seen only')
                else:show_message('This Pokémon has not been discovered yet.')


def show_trainer_card():
    ui_frame('TRAINER CARD','Your progress through Kanto Quest 151.','PROFILE')
    cards=[('BADGES',f'{earned_badge_count()} / 4'),('COINS',str(coins)),('SEEN',f'{count_species_flags(seen_species)} / 151'),('CAUGHT',f'{count_species_flags(caught_species)} / 151'),('STEPS',str(steps_taken)),('CHAMPION','YES' if champion_defeated else 'NOT YET')]
    for idx,(label,value) in enumerate(cards):
        x=31+(idx%3)*306;y=156+(idx//3)*133
        ui_box(x,y,289,117,CARD,15)
        ui_text(label,x+18,y+18,18,MUTED,True)
        ui_text(value,x+18,y+54,31,MINT if idx else GOLD,True,255)
    ui_box(31,437,901,45,DARK,11)
    ui_text('LOCATION: '+AREA_NAMES[current_area].title(),52,448,23,PAPER,True,840)
    ui_footer('ENTER / ESC  Return')
    wait_key()


if __name__ == '__main__':
    try:
        initialize_display()
        main()
    except GameExit:
        pass
    except Exception:
        import traceback
        traceback.print_exc()
        raise
    finally:
        pygame.quit()
