# NÃO é a pytube3 (lib morreu)
from pytube import Playlist
import os

if __name__ == "__main__":
    # Cria uma pasta para as músicas
    path = "MUSICAS"
    if path not in os.listdir():
        os.mkdir(path)

    # Solicita a URL da Playlist
    playlist = Playlist(input("Insira o link da sua playlist: "))

    # Baixa vídeo por vídeo da playlist
    print('Começando o Download..')
    for video in playlist.videos:
        # Baixa apenas o áudio (música)
        video.streams.filter(only_audio=True).first().download(path)
        # Formata o título para retirar chars indesejados pelo Windows
        for i in (',', '.', ':', ';', '"', "'", "#", "/", "\\"):
            video.title = video.title.replace(i, '')
        # Transforma o arquivo em .mp3
        os.rename("MUSICAS/" + video.title + ".mp4", "MUSICAS/" + video.title + ".mp3")

