# NÃO é a pytube3 (lib morreu)
from pytube import Playlist
import streamlit as st
import shutil
import os

# Cria uma pasta para as músicas
def limpar_pasta(front=True):
    global PATH
    nao = False
    if front:
        st.title("Limpar pasta de músicas?")
        direita, esquerda = st.columns(2)
        sim = direita.button("Sim")
        nao = esquerda.button("Não")

        if not nao and not sim:
            st.stop()

        st.warning(f'{sim} ////// {nao}')

        if nao:
            baixar_playlist()

    # Se a pasta já existir ele primeiro deleta
    if not nao:
        if PATH in os.listdir():
            shutil.rmtree(PATH, ignore_errors=True)
        os.mkdir(PATH)

def baixar_playlist():
    global PATH

    # Solicita a URL da Playlist
    st.title("Baixar Playlist")
    playlist = st.text_input("Insira o link da sua playlist: ")
    botao = st.checkbox("Limpar pasta?")

    # Espera o usuário digitar a Playlist
    if not playlist:
        st.stop()

    try:
        # Cria a barra de progresso
        progresso = 0
        barra = st.progress(progresso)

        # Checa se o usuário quer limpar a pasta
        if botao:
            limpar_pasta(front=False)

        for video in Playlist(playlist).videos:
            qtd = len(Playlist(playlist))
            # Baixa apenas o áudio (música)
            video.streams.filter(only_audio=True).first().download(PATH)
            # Formata o título para retirar chars indesejados pelo Windows
            for i in (',', '.', ':', ';', '"', "'", "#", "/", "\\", "*"):
                video.title = video.title.replace(i, '')
            # Transforma o arquivo em .mp3
            os.rename("MUSICAS/" + video.title + ".mp4", "MUSICAS/" + video.title + ".mp3")
            # Aumenta uma porcentagem da barra
            progresso += int(100 / qtd)
            barra.progress(progresso)
        st.balloons()

    except KeyError:
        st.warning("Insira uma playlist válida!")
    except FileExistsError:
        st.warning("Foi encontrada uma música idêntica, limpe a pasta para continuar!")


if __name__ == "__main__":
    PATH = "MUSICAS"

    st.set_page_config(page_title="Baixar vídeos",
                       page_icon=None,
                       layout='centered',
                       initial_sidebar_state='expanded')

    st.sidebar.title('Páginas')

    paginas = {"Playlist": baixar_playlist, "Limpar pasta": limpar_pasta}

    pagina = st.sidebar.selectbox('Selecione a página', paginas.keys())

    paginas.get(pagina)()
