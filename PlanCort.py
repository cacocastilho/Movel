import math


class PlanCort:
    def __init__(self, espessuraPrincipal=16.0, espessuraFundo=6.0, densidadeRef=650.0):
        self.aUsa: float = 0                # altura usada [cm]
        self.espP = espessuraPrincipal      # Espessura principal [mm]
        self.espF = espessuraFundo          # Espessura fundo [mm]
        self.densidade = densidadeRef       # de 500 a 800 [kg/m3]
        self.lMax: float = 0                # largura [cm]
        self.aMax: float = 0                # altura [cm]
        self.pMax: float = 0                # profundidade [cm]
        self.cxn: int = 0                   # numero da caixa
        self.gvt: int = 0
        self.gevtr: int = 0

    def espaco(self, largura=190, altura=265, profundidade=60):
        self.lMax = largura
        self.aMax = altura
        self.pMax = profundidade

    def peca(self, tipo: int, nome: str, lat: float, com: float, borda: str = '-'):
        print(f'{tipo:2n} {lat*10.0:5.0f} mm {com*10.0:5.0f} mm Broda {borda:5} {nome}')

    """
    Cria uma caixa na horizontal com fundo que encaixe na dimensão aMax, pMax, lMax utilizando o espaço util entrado
    Caso o espaço util seja < 0 considera a dimensão como o que deve sobrar da caixa no espaço util
    Caso o espaço util seja == 0 considera a dimensão disponível completa
    util em cm, rebaixo em mm, 1 divisão == 2 espaços
    
    devolve o espaço interno Largura, Comprimento, Altura para divisões iguais  
    """
    def caixaH(self, tipo: str = 'h', divisao: int = 0, util: float = 40.0, rebaixo: float = 10.0):

        lEsp = self.lMax
        pEsp = self.pMax
        espParede = self.espP
        espFundo = self.espF
        aEsp = (util) if (util > 0) else (self.pMax - self.aUsa + (util if util < 0 else 0))

        self.cxn += 1
        self.peca(0, f'Caixa{self.cxn}.topo', lEsp, pEsp, 'L2C')
        self.peca(0, f'Caixa{self.cxn}.base', lEsp, pEsp, 'L2C')
        self.peca(0, f'Caixa{self.cxn}.lado.D', aEsp, pEsp, 'L')
        self.peca(0, f'Caixa{self.cxn}.lado.E', aEsp, pEsp, 'L')
        self.peca(1, f'Caixa{self.cxn}.fundo', lEsp - espParede / 10.0, aEsp + espParede / 10.0)

        self.aUsa += aEsp + (2 * espParede / 10.0)

        if divisao > 0:
            if tipo == 'h':  # Caixa com divisões na horizontal
                for x in range(divisao):
                    self.peca(0, f'Caixa{self.cxn}.divisão.V{x + 1}', aEsp, pEsp - (rebaixo + espFundo) / 10, 'L')
                return (lEsp - ((2 + divisao) * espParede / 10.0)) / (divisao + 1), aEsp, pEsp - (
                        rebaixo - espFundo) / 10

            elif tipo == 'v':  # Caixa com divisoes na vertical
                for x in range(divisao):
                    self.peca(0, f'Caixa{self.cxn}.divisão.H{x + 1}', lEsp - (2 * espParede / 10.0),
                              pEsp - (rebaixo + espFundo) / 10.0, 'L')
                return lEsp - (2 * espParede / 10.0), (aEsp - (divisao) * espParede / 10.0) / (divisao + 1), pEsp - (
                        rebaixo - espFundo) / 10
        pass

    def maleiro(self, tipo = 'sobrepor', util: float = 40, divisao=2):
        ret = self.caixaH('h', divisao, util, 15.0)

        # espaço para encaixe da porta de 3 mm de cada lado
        porta = math.sqrt(math.pow(util - 0.6, 2) - math.pow(self.espP / 10, 2))
        #self.peca(0, f'Caixa{self.cxn}.porta', hUtil - 0.6, self.lMax - (2*self.espP/10.0) - 0.6, '2L2C')
        self.peca(0, f'Caixa{self.cxn}.porta', self.lMax - (2 * self.espP / 10.0) - 0.6, porta, '2L2C')
        return ret
        pass

    """
    Calcula as gavetas de acordo com a lista de altura util (cm) de cada gaveta
    considera a distancia de montagem da ferragem (mm) e uma sobra (mm) atrás da gaveta
    o espelho vai sobrepor metade das duas laterais e terá um redução do puxador (mm) se for o caso
    gap (mm) entre cada gaveta
    """
    def gaveta(self, espaco, util: float = (20), ferragem=26, sobra=20, puxador=0, gap=5):
        lEsp, aEsp, pEsp = espaco if espaco else (self.lMax, self.aMax, self.pMax)

        # frente, fundo e espelho da gaveta
        frente = lEsp - (ferragem + 2 * self.espP)/10
        fundo = pEsp - (sobra + 3*self.espP)/10
        espelho = frente + (ferragem + self.espP)/10
        gapTotal = 0
        for x in util:
            self.gvt += 1
            altura = x + (self.espF - puxador)/10
            self.peca(0, f'Gaveta{self.gvt}.espelho', altura, espelho, ('2L2C' if puxador == 0 else '2LC'))
            self.peca(0, f'Gaveta{self.gvt}.frente', x, frente, '2LC')
            self.peca(0, f'Gaveta{self.gvt}.fundo', x, frente, '2LC')
            self.peca(0, f'Gaveta{self.gvt}.lado.D', x, fundo, 'C')
            self.peca(0, f'Gaveta{self.gvt}.lado.E', x, fundo, 'C')

            self.peca(1, f'Gaveta{self.gvt}.fundo', frente, fundo, '')
            gapTotal += altura + gap / 10

        self.gvtr += 0
        self.peca(0, f'Gaveteiro{self.gvtr}.lado.D', gapTotal, pEsp - self.espP / 10, 'L')
        self.peca(0, f'Gaveteiro{self.gvtr}.lado.E', gapTotal, pEsp - self.espP / 10, 'L')
        self.peca(0, f'Gaveteiro{self.gvtr}.topo', lEsp, pEsp - self.espP / 10, 'C')
        self.peca(0, f'Gaveteiro{self.gvtr}.base', lEsp, pEsp - self.espP / 10, 'C')

        if (aEsp < gapTotal + 2*self.EspP/10):
            print("Espaço insuficiente!")
        pass
