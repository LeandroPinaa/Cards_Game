class Carta:
    Naipes = ["Paus","Ouros","Copas","Espadas"]
    Posicoes = [None,"Ás","2","3","4","5","6","7",
                "8","9","10","Valete","Rainha","Rei"]
    def __init__(self,naipe=0,posicao=0):
        self.naipe = naipe
        self.posicao = posicao
    def __str__(self):
        return (self.Posicoes[self.posicao] + " de " +
                self.Naipes[self.naipe])
    def __lt__(self, other):
        if self.naipe > other.naipe:
            return 1
        if self.naipe < other.naipe:
            return -1
        if self.posicao > other.posicao:
            return 1
        if self.posicao < other.posicao:
            return -1
        return True

class Baralho:
    def __init__(self):
        self.cartas = list()
        for naipe in range(4):
            for posicao in range(1,14):
                self.cartas.append(Carta(naipe,posicao))
    def ImprimirBaralho(self):
        for carta in self.cartas:
            print(carta)
    def __str__(self):
        for a in range(len(self.cartas)):
            print(self.cartas[a])
    def Embaralhar(self):
        from random import randrange
        for a in range(len(self.cartas)):
            b = randrange(0,len(self.cartas))
            self.cartas[a],self.cartas[b] = self.cartas[b],self.cartas[a]
    def RemoverCarta(self,carta):
        for a in self.cartas:
            if str(carta) == str(a):
                self.cartas.remove(a)
    def distribuirCarta(self):
        #posso atribuir uma var pra essa fun pegando a ultima(distribuindo de certa forma)
        #ou simplesmente tirar a ultima
        return self.cartas.pop()
    def EstaVazio(self):
        return (len(self.cartas) == 0)
    def __lt__(self, other):
        if self.naipe > other.naipe:
            return 1
        if self.naipe < other.naipe:
            return -1
        if self.posicao > other.posicao:
            return 1
        if self.posicao < other.posicao:
            return -1
        return True
    def DistribuirMuitas(self,maos,max=999):
        for i in range(max):
            if self.EstaVazio():
                break
            carta = self.distribuirCarta()
            mao = maos[i % len(maos)] #voltar pro cmc do deck caso ultrapasse
            mao.AddCarta(carta)

class Mao(Baralho):
    def __init__(self,nome=""):
        self.cartas = []
        self.nome = nome
    def AddCarta(self,carta):
        self.cartas.append(carta)

class JogoDeCartas:
    def __init__(self):
        self.baralho = Baralho()
        self.baralho.Embaralhar()

class MaoDeMico(Mao):
    def DescartarCasais(self):
        conta = 0
        cartasIniciais = self.cartas[:]
        for carta in cartasIniciais:
            casal = Carta(3 - carta.naipe,carta.posicao)
            for carta2 in self.cartas:
                if str(casal) == str(carta2):
                    self.cartas.remove(carta)
                    self.cartas.remove(carta2)
                    print(f"Mão de {self.nome}: {carta} faz par com {casal}")
                    conta += 1
                    break
        return conta

class Mico(JogoDeCartas):
    def ExibirMaos(self):
        for mao in self.maos:
            print(f"Mão de {mao.nome}:")
            mao.ImprimirBaralho()
            print()

    def removerTodosOsCasais(self):
        conta = 0
        for mao in self.maos:
            conta = conta + mao.DescartarCasais()
        return conta

    def JogarVez(self,i):
        if self.maos[i].EstaVazio():
            return 0
        vizinho = self.BuscarVizinho(i)
        novaCarta = self.maos[vizinho].distribuirCarta()
        self.maos[i].AddCarta(novaCarta)
        print(f"Mão {self.maos[i].nome} pegou {novaCarta}")
        conta = self.maos[i].DescartarCasais()
        self.maos[i].Embaralhar()
        return conta

    def BuscarVizinho(self, i):
        tamanho = len(self.maos)
        for next in range(1, tamanho):
            vizinho = (i + next) % tamanho #nunca ultrapassar
            if not self.maos[vizinho].EstaVazio():
                return vizinho

    def jogar(self,nomes):
        #remover a Rainha de Paus
        self.baralho.RemoverCarta(Carta(0,12))
        #fazer uma mão para cada jogador
        self.maos = list()
        for nome in nomes:
            self.maos.append(MaoDeMico(nome))
        # distribuir as cartas até deck acabar
        self.baralho.DistribuirMuitas(self.maos)
        print("---------- As cartas foram dadas")
        self.ExibirMaos()
        # remover casais iniciais
        casais = self.removerTodosOsCasais()
        print("\n---------- Os pares foram descartados, o jogo começa")
        self.ExibirMaos()
        #jogar até que 25 casais se formem
        vez = 0
        tamanho = len(self.maos)
        while casais < 25:
            casais += self.JogarVez(vez)
            vez = (vez + 1) % tamanho #vez voltar em 0 caso ultrapasse

        print("---------- Fim do jogo")
        self.ExibirMaos()

jogo = Mico()
jogo.jogar(['Leandro','Arthur','Victor','Igor'])
