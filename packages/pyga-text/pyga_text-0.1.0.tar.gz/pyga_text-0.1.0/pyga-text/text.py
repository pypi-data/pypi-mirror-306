# pyga_text/text.py

class Perso:
    def __init__(self, atributos, nome):
        self.atributos = atributos
        self.nome = nome

    def speak(self, mensagem):
        print(f"{self.nome}: {mensagem}")

class Game:
    def __init__(self):
        self.persos = []

    def perso(self, atributos, nome):
        """Cria um novo personagem."""
        return Perso(atributos, nome)

    def setperso(self, perso):
        """Adiciona um personagem à lista de personagens."""
        self.persos.append(perso)

    def init(self):
        """Inicia o jogo."""
        print("Iniciando o jogo...")

    def tex(self, texto):
        """Exibe um texto no console."""
        print(texto)

    def end(self):
        """Finaliza o jogo."""
        print("Fim do jogo.")