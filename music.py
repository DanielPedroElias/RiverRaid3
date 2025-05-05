### Modulo de musicas do jogo (apenas para musicas de fundo. Efeitos sonoros foram feitos a mao utilizando o Pyxel)

# music.py
import pygame.mixer

# inicializa o mixer só uma vez
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# caminhos das faixas
MENU_TRACK = "music/menu_bgm.wav"
GAME_TRACK = "music/game_bgm.wav"

# controle interno de qual faixa está tocando
_current_track = None

def _load_and_play(path, loop=-1, volume=0.6):
    global _current_track
    if _current_track == path:
        return
    pygame.mixer.music.stop()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)
    _current_track = path

def play_menu_music():
    """Toca em loop a música de menu (só carrega se for diferente)."""
    _load_and_play(MENU_TRACK)

def play_game_music():
    """Toca em loop a música do jogo."""
    _load_and_play(GAME_TRACK)

def stop_music():
    """Para qualquer música que esteja tocando."""
    global _current_track
    pygame.mixer.music.stop()
    _current_track = None
