# NÃO é a pytube3 (lib morreu)
from pytube import Playlist
import streamlit as st
import shutil
import os

if __name__ == "__main__":
    # Cria uma pasta para as músicas
    path = "MUSICAS"
    # Se a pasta já existir ele primeiro deleta
    if path in os.listdir():
        shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)

    # Solicita a URL da Playlist
    playlist = st.text_input("Insira o link da sua playlist: ")

    # Espera o usuário digitar a Playlist
    if not playlist:
        st.stop()

    try:
        # Cria a barra de progresso
        progresso = 0
        barra = st.progress(progresso)
        for video in Playlist(playlist).videos:
            qtd = len(Playlist(playlist))
            # Baixa apenas o áudio (música)
            video.streams.filter(only_audio=True).first().download(path)
            # Formata o título para retirar chars indesejados pelo Windows
            for i in (',', '.', ':', ';', '"', "'", "#", "/", "\\", "*"):
                video.title = video.title.replace(i, '')
            # Transforma o arquivo em .mp3
            os.rename("MUSICAS/" + video.title + ".mp4", "MUSICAS/" + video.title + ".mp3")
            # Aumenta uma porcentagem da barra
            progresso += int(100/qtd)
            barra.progress(progresso)

    except KeyError:
        st.warning("Insira uma playlist válida!")
    except FileExistsError:
        st.warning("Falha na recriação de pastas!")
