import math


class PlanCort:
    def __init__(self, espessuraPrincipal=16.0, espessuraFundo=6.0, densidadeRef=650.0):
        self.aUsa:float = 0                 # altura usada [cm]
        self.espP = espessuraPrincipal      # Espessura principal [mm]
        self.espF = espessuraFundo          # Espessura fundo [mm]
        self.densidade = densidadeRef       # de 500 a 800 [kg/m3]
        self.lMax: float = 0                # largura [cm]
        self.aMax: float = 0                # altura [cm]
        self.pMax: float = 0                # profundidade [cm]
        self.cxn: int = 0                   # numero da caixa

    def espaco(self, largura=190, altura=265, profundidade=60):
        self.lMax = largura
        self.aMax = altura
        self.pMax = profundidade

    def peca(self, tipo: int, nome: str, lat: float, com: float, borda: str = '-'):
        print(f'{tipo:2n} {lat*10.0:5.0f} mm {com*10.0:5.0f} mm Broda {borda:5} {nome}')

    """
    Cria uma caixa na horizontal com fundo que encaixe na dimensão aMax, pMax, lMax utilizando o espaço util entrado
    Caso o espaço util seja < 0 considera a dimensão como o que deve sobrar da caixa no espaço util
    Caso o espaço util seja == 0 considera a dimensão disponivel completa
    util em cm, rebaixo em mm, 1 divisão == 2 espaços
    
    devolve o espaço interno Largura, Comprimento, Altura para divisões iguais  
    """
    def caixaH(self, tipo: str = 'h', divisao: int = 0, util: float = 40.0, rebaixo: float = 10.0):
        if util == 0:
            util = self.pMax - self.aUsa
        elif util < 0:
            util = self.pMax - self.aUsa + util

        """
        lEsp = pass
        cEsp = pass
        aEsp = pass
        """

        self.cxn += 1
        self.peca(0, f'Caixa{self.cxn}.topo', self.lMax, self.pMax, 'L2C')
        self.peca(0, f'Caixa{self.cxn}.base', self.lMax, self.pMax, 'L2C')
        self.peca(0, f'Caixa{self.cxn}.lado.D', util, self.pMax, 'L')
        self.peca(0, f'Caixa{self.cxn}.lado.E', util, self.pMax, 'L')
        self.peca(1, f'Caixa{self.cxn}.fundo', self.lMax - self.espP/10.0, util + self.espP/10.0)

        self.aUsa += util + (2*self.espP/10.0)

        if divisao > 0:
            if tipo == 'h':         # Caixa com divisões na horizontal
                for x in range(divisao):
                    self.peca(0, f'Caixa{self.cxn}.divisão.H{x+1}', util, self.pMax - (rebaixo + self.espF)/10, 'L')
                return (self.lMax - ((2 + divisao) * self.espP/10.0)) / (divisao + 1), util, self.pMax - (rebaixo - self.espF)/10

            elif tipo == 'v':       # Caixa com divisoes na vertical
                for x in range(divisao):
                    self.peca(0, f'Caixa{self.cxn}.divisão.V{x+1}', self.lMax - (2*self.espP/10.0), self.pMax - (rebaixo + self.espF)/10.0, 'L')
                return self.lMax - (2*self.espP/10.0), (util - (divisao) * self.espP/10.0) / (divisao + 1), self.pMax - (rebaixo - self.espF)/10
        pass

    def maleiro(self, tipo = 'sobrepor', util: float = 40, divisao=2):
        ret = self.caixaH('h', divisao, util, 15.0)

        # espaço para encaixe da porta de 3 mm de cada lado
        porta = math.sqrt(math.pow(util - 0.6, 2) - math.pow(self.espP / 10, 2))
        #self.peca(0, f'Caixa{self.cxn}.porta', hUtil - 0.6, self.lMax - (2*self.espP/10.0) - 0.6, '2L2C')
        self.peca(0, f'Caixa{self.cxn}.porta', self.lMax - (2 * self.espP / 10.0) - 0.6, porta, '2L2C')
        return ret
        pass

    def gaveta(self, util: float = 20, qtd: int = 1):

        pass
