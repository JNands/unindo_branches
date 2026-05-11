import random
import time
import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional

def linha(tamanho=60):
    print('=' * tamanho)



def titulo(texto):
    linha()
    print(texto.center(60))
    linha()



def pausa(segundos=1):
    time.sleep(segundos)

@dataclass
class Item:
    nome: str
    tipo: str
    valor: int
    descricao: str
    poder: int = 0

    def exibir(self):
        print(f'Nome: {self.nome}')
        print(f'Tipo: {self.tipo}')
        print(f'Valor: {self.valor}')
        print(f'Poder: {self.poder}')
        print(f'Descrição: {self.descricao}')


class Inventario:
    def __init__(self):
        self.itens: List[Item] = []

    def adicionar_item(self, item: Item):
        self.itens.append(item)
        print(f'Item {item.nome} adicionado ao inventário!')

    def remover_item(self, nome_item: str):
        for item in self.itens:
            if item.nome.lower() == nome_item.lower():
                self.itens.remove(item)
                print(f'Item {item.nome} removido!')
                return item
        print('Item não encontrado!')
        return None

    def listar_itens(self):
        titulo('INVENTÁRIO')

        if not self.itens:
            print('Inventário vazio!')
            return

        for i, item in enumerate(self.itens, start=1):
            print(f'{i}. {item.nome} ({item.tipo}) - Poder {item.poder}')

    def calcular_valor_total(self):
        return sum(item.valor for item in self.itens)


class Personagem:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.experiencia = 0
        self.experiencia_para_subir = 100
        self.ouro = 100

        self.hp_max = 100
        self.hp = self.hp_max

        self.mana_max = 50
        self.mana = self.mana_max

        self.forca = 10
        self.defesa = 5
        self.inteligencia = 5
        self.agilidade = 5

        self.inventario = Inventario()
        self.habilidades = []
        self.missoes = []

    def exibir_status(self):
        titulo(f'STATUS DE {self.nome.upper()}')
        print(f'Classe: {self.classe}')
        print(f'Nível: {self.nivel}')
        print(f'XP: {self.experiencia}/{self.experiencia_para_subir}')
        print(f'HP: {self.hp}/{self.hp_max}')
        print(f'Mana: {self.mana}/{self.mana_max}')
        print(f'Força: {self.forca}')
        print(f'Defesa: {self.defesa}')
        print(f'Inteligência: {self.inteligencia}')
        print(f'Agilidade: {self.agilidade}')
        print(f'Ouro: {self.ouro}')

    def atacar(self, inimigo):
        dano = random.randint(self.forca - 2, self.forca + 5)
        dano_real = max(1, dano - inimigo.defesa)

        inimigo.hp -= dano_real

        print(f'{self.nome} atacou {inimigo.nome} causando {dano_real} de dano!')

        if inimigo.hp <= 0:
            print(f'{inimigo.nome} foi derrotado!')
            self.ganhar_xp(inimigo.xp_recompensa)
            self.ouro += inimigo.ouro
            print(f'Você ganhou {inimigo.ouro} moedas de ouro!')

    def ganhar_xp(self, quantidade):
        self.experiencia += quantidade
        print(f'{self.nome} ganhou {quantidade} XP!')

        while self.experiencia >= self.experiencia_para_subir:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia -= self.experiencia_para_subir
        self.experiencia_para_subir = int(self.experiencia_para_subir * 1.5)

        self.hp_max += 20
        self.mana_max += 10
        self.forca += 3
        self.defesa += 2
        self.inteligencia += 2
        self.agilidade += 2

        self.hp = self.hp_max
        self.mana = self.mana_max

        titulo('LEVEL UP!')
        print(f'{self.nome} subiu para o nível {self.nivel}!')

    def usar_pocao(self):
        cura = 30
        self.hp = min(self.hp_max, self.hp + cura)
        print(f'{self.nome} recuperou {cura} de HP!')


class Inimigo:
    def __init__(self, nome, nivel):
        self.nome = nome
        self.nivel = nivel

        self.hp_max = 50 + nivel * 20
        self.hp = self.hp_max

        self.forca = 5 + nivel * 2
        self.defesa = 2 + nivel

        self.xp_recompensa = 50 * nivel
        self.ouro = random.randint(10, 50) * nivel

    def atacar(self, jogador):
        dano = random.randint(self.forca - 2, self.forca + 4)
        dano_real = max(1, dano - jogador.defesa)

        jogador.hp -= dano_real

        print(f'{self.nome} atacou {jogador.nome} causando {dano_real} de dano!')


class SistemaCombate:
    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo

    def iniciar(self):
        titulo('COMBATE INICIADO')

        while self.jogador.hp > 0 and self.inimigo.hp > 0:
            print(f'\n{self.jogador.nome}: {self.jogador.hp} HP')
            print(f'{self.inimigo.nome}: {self.inimigo.hp} HP')

            print('\n1. Atacar')
            print('2. Usar Poção')
            print('3. Fugir')

            escolha = input('Escolha: ')

            if escolha == '1':
                self.jogador.atacar(self.inimigo)

            elif escolha == '2':
                self.jogador.usar_pocao()

            elif escolha == '3':
                chance = random.randint(1, 100)

                if chance <= 50:
                    print('Você fugiu!')
                    return
                else:
                    print('Falha ao fugir!')

            else:
                print('Opção inválida!')
                continue

            if self.inimigo.hp > 0:
                pausa(1)
                self.inimigo.atacar(self.jogador)

        if self.jogador.hp <= 0:
            titulo('GAME OVER')
            print('Você foi derrotado...')


@dataclass
class Missao:
    titulo: str
    descricao: str
    recompensa_ouro: int
    recompensa_xp: int
    concluida: bool = False

    def concluir(self, jogador):
        if not self.concluida:
            self.concluida = True
            jogador.ouro += self.recompensa_ouro
            jogador.ganhar_xp(self.recompensa_xp)

            titulo('MISSÃO CONCLUÍDA')
            print(f'Recompensa: {self.recompensa_ouro} ouro')
            print(f'Recompensa: {self.recompensa_xp} XP')


class Loja:
    def __init__(self):
        self.itens = [
            Item('Espada de Ferro', 'Arma', 100, 'Uma espada simples.', 10),
            Item('Machado Pesado', 'Arma', 200, 'Muito poderoso.', 20),
            Item('Armadura de Aço', 'Armadura', 150, 'Boa defesa.', 15),
            Item('Poção de Vida', 'Consumível', 30, 'Recupera HP.', 0),
            Item('Cajado Arcano', 'Arma', 300, 'Canaliza magia.', 25),
            Item('Anel Místico', 'Acessório', 250, 'Aumenta inteligência.', 12),
        ]

    def mostrar_itens(self):
        titulo('LOJA')

        for i, item in enumerate(self.itens, start=1):
            print(f'{i}. {item.nome} - {item.valor} ouro')

    def comprar(self, jogador, indice):
        if indice < 0 or indice >= len(self.itens):
            print('Item inválido!')
            return

        item = self.itens[indice]

        if jogador.ouro >= item.valor:
            jogador.ouro -= item.valor
            jogador.inventario.adicionar_item(item)
            print(f'Você comprou {item.nome}!')
        else:
            print('Ouro insuficiente!')


class Mapa:
    def __init__(self, largura=10, altura=10):
        self.largura = largura
        self.altura = altura
        self.grid = []

        self.gerar()

    def gerar(self):
        terrenos = ['Floresta', 'Deserto', 'Montanha', 'Planície', 'Lago']

        for y in range(self.altura):
            linha_mapa = []

            for x in range(self.largura):
                linha_mapa.append(random.choice(terrenos))

            self.grid.append(linha_mapa)

    def exibir(self):
        titulo('MAPA')

        for linha_ in self.grid:
            print(' | '.join(linha_))


class SistemaCrafting:
    def __init__(self):
        self.receitas = {
            'Espada Flamejante': ['Espada de Ferro', 'Cristal de Fogo'],
            'Armadura Sagrada': ['Armadura de Aço', 'Essência Divina'],
            'Cajado Supremo': ['Cajado Arcano', 'Pedra Mágica'],
        }

    def craftar(self, jogador, item_resultado):
        if item_resultado not in self.receitas:
            print('Receita inexistente!')
            return

        ingredientes = self.receitas[item_resultado]
        nomes_inventario = [item.nome for item in jogador.inventario.itens]

        for ingrediente in ingredientes:
            if ingrediente not in nomes_inventario:
                print(f'Falta o ingrediente: {ingrediente}')
                return

        for ingrediente in ingredientes:
            jogador.inventario.remover_item(ingrediente)

        novo_item = Item(
            item_resultado,
            'Especial',
            1000,
            'Item raro criado por crafting.',
            50
        )

        jogador.inventario.adicionar_item(novo_item)

        titulo('CRAFTING')
        print(f'Você criou {item_resultado}!')


class EventoAleatorio:
    def __init__(self):
        self.eventos = [
            self.evento_tesouro,
            self.evento_armadilha,
            self.evento_comerciante,
            self.evento_bencao,
            self.evento_monstro,
        ]

    def executar(self, jogador):
        evento = random.choice(self.eventos)
        evento(jogador)

    def evento_tesouro(self, jogador):
        ouro = random.randint(50, 200)
        jogador.ouro += ouro

        titulo('TESOURO')
        print(f'Você encontrou {ouro} moedas de ouro!')

    def evento_armadilha(self, jogador):
        dano = random.randint(10, 30)
        jogador.hp -= dano

        titulo('ARMADILHA')
        print(f'Você sofreu {dano} de dano!')

    def evento_comerciante(self, jogador):
        titulo('COMERCIANTE')
        print('Um comerciante misterioso apareceu.')

        if jogador.ouro >= 20:
            jogador.ouro -= 20
            jogador.hp = min(jogador.hp_max, jogador.hp + 40)
            print('Você comprou uma refeição e recuperou HP!')
        else:
            print('Você não tinha ouro suficiente.')

    def evento_bencao(self, jogador):
        bonus = random.randint(1, 5)
        jogador.forca += bonus

        titulo('BÊNÇÃO')
        print(f'Sua força aumentou em {bonus}!')

    def evento_monstro(self, jogador):
        titulo('MONSTRO')
        print('Um monstro apareceu!')

        inimigo = Inimigo('Goblin Selvagem', jogador.nivel)
        combate = SistemaCombate(jogador, inimigo)
        combate.iniciar()


class SaveManager:
    @staticmethod
    def salvar(jogador, arquivo='savegame.json'):
        dados = {
            'nome': jogador.nome,
            'classe': jogador.classe,
            'nivel': jogador.nivel,
            'experiencia': jogador.experiencia,
            'ouro': jogador.ouro,
            'hp': jogador.hp,
            'hp_max': jogador.hp_max,
            'mana': jogador.mana,
            'mana_max': jogador.mana_max,
            'forca': jogador.forca,
            'defesa': jogador.defesa,
            'inteligencia': jogador.inteligencia,
            'agilidade': jogador.agilidade,
        }

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

        print('Jogo salvo com sucesso!')

    @staticmethod
    def carregar(arquivo='savegame.json'):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            jogador = Personagem(dados['nome'], dados['classe'])

            jogador.nivel = dados['nivel']
            jogador.experiencia = dados['experiencia']
            jogador.ouro = dados['ouro']
            jogador.hp = dados['hp']
            jogador.hp_max = dados['hp_max']
            jogador.mana = dados['mana']
            jogador.mana_max = dados['mana_max']
            jogador.forca = dados['forca']
            jogador.defesa = dados['defesa']
            jogador.inteligencia = dados['inteligencia']
            jogador.agilidade = dados['agilidade']

            print('Jogo carregado!')
            return jogador

        except FileNotFoundError:
            print('Nenhum save encontrado!')
            return None


class IAInimigo:
    def decidir_acao(self, inimigo, jogador):
        if inimigo.hp < inimigo.hp_max * 0.3:
            chance = random.randint(1, 100)

            if chance <= 40:
                print(f'{inimigo.nome} tentou fugir!')
                return 'fugir'

        return 'atacar'


class Arena:
    def __init__(self, jogador):
        self.jogador = jogador
        self.round = 1

    def iniciar(self):
        titulo('ARENA')

        while self.jogador.hp > 0:
            print(f'Round {self.round}')

            inimigo = Inimigo(
                f'Gladiador {self.round}',
                self.round
            )

            combate = SistemaCombate(self.jogador, inimigo)
            combate.iniciar()

            if self.jogador.hp <= 0:
                break

            recompensa = self.round * 100
            self.jogador.ouro += recompensa

            print(f'Recompensa da arena: {recompensa} ouro')

            self.round += 1

            continuar = input('Continuar arena? (s/n): ')

            if continuar.lower() != 's':
                break


class Banco:
    def __init__(self):
        self.taxa_juros = 0.05

    def depositar(self, jogador, valor):
        if valor <= jogador.ouro:
            jogador.ouro -= valor
            print(f'{valor} ouro depositado.')
        else:
            print('Ouro insuficiente.')

    def aplicar_juros(self, valor):
        return valor + (valor * self.taxa_juros)


class Bestiario:
    def __init__(self):
        self.monstros = {
            'Goblin': {
                'hp': 50,
                'forca': 10,
                'descricao': 'Criatura pequena e agressiva.'
            },
            'Dragão': {
                'hp': 500,
                'forca': 80,
                'descricao': 'Uma besta lendária.'
            },
            'Esqueleto': {
                'hp': 70,
                'forca': 15,
                'descricao': 'Morto-vivo antigo.'
            },
            'Lobo Sombrio': {
                'hp': 120,
                'forca': 25,
                'descricao': 'Predador das florestas escuras.'
            },
        }

    def exibir(self):
        titulo('BESTIÁRIO')

        for nome, info in self.monstros.items():
            print(f'\n{nome}')
            print(f'HP: {info["hp"]}')
            print(f'Força: {info["forca"]}')
            print(f'Descrição: {info["descricao"]}')




class SistemaClima:
    def __init__(self):
        self.climas = [
            'Ensolarado',
            'Chuvoso',
            'Tempestade',
            'Neblina',
            'Nevando'
        ]

    def gerar_clima(self):
        return random.choice(self.climas)


class NPC:
    def __init__(self, nome, dialogos):
        self.nome = nome
        self.dialogos = dialogos

    def falar(self):
        print(f'{self.nome}: {random.choice(self.dialogos)}')


class Jogo:
    def __init__(self):
        self.jogador = None
        self.loja = Loja()
        self.mapa = Mapa()
        self.crafting = SistemaCrafting()
        self.eventos = EventoAleatorio()
        self.bestiario = Bestiario()
        self.clima = SistemaClima()

    def criar_personagem(self):
        titulo('CRIAR PERSONAGEM')

        nome = input('Digite seu nome: ')

        print('Classes disponíveis:')
        print('1. Guerreiro')
        print('2. Mago')
        print('3. Arqueiro')

        escolha = input('Escolha sua classe: ')

        classes = {
            '1': 'Guerreiro',
            '2': 'Mago',
            '3': 'Arqueiro'
        }

        classe = classes.get(escolha, 'Aventureiro')

        self.jogador = Personagem(nome, classe)

        titulo('PERSONAGEM CRIADO')
        self.jogador.exibir_status()

    def menu_principal(self):
        while True:
            titulo('MENU PRINCIPAL')

            print('1. Ver status')
            print('2. Explorar')
            print('3. Loja')
            print('4. Inventário')
            print('5. Mapa')
            print('6. Crafting')
            print('7. Arena')
            print('8. Bestiário')
            print('9. Salvar')
            print('10. Sair')

            opcao = input('Escolha: ')

            if opcao == '1':
                self.jogador.exibir_status()

            elif opcao == '2':
                self.explorar()

            elif opcao == '3':
                self.menu_loja()

            elif opcao == '4':
                self.jogador.inventario.listar_itens()

            elif opcao == '5':
                self.mapa.exibir()

            elif opcao == '6':
                self.menu_crafting()

            elif opcao == '7':
                arena = Arena(self.jogador)
                arena.iniciar()

            elif opcao == '8':
                self.bestiario.exibir()

            elif opcao == '9':
                SaveManager.salvar(self.jogador)

            elif opcao == '10':
                print('Saindo do jogo...')
                break

            else:
                print('Opção inválida!')

            input('\nPressione ENTER para continuar...')

    def explorar(self):
        titulo('EXPLORAÇÃO')

        clima = self.clima.gerar_clima()
        print(f'Clima atual: {clima}')

        chance = random.randint(1, 100)

        if chance <= 60:
            inimigos = [
                'Goblin',
                'Esqueleto',
                'Bandido',
                'Lobo Selvagem'
            ]

            nome_inimigo = random.choice(inimigos)
            inimigo = Inimigo(nome_inimigo, self.jogador.nivel)

            combate = SistemaCombate(self.jogador, inimigo)
            combate.iniciar()

        else:
            self.eventos.executar(self.jogador)

    def menu_loja(self):
        self.loja.mostrar_itens()

        try:
            escolha = int(input('Escolha item (0 cancelar): '))

            if escolha > 0:
                self.loja.comprar(self.jogador, escolha - 1)

        except ValueError:
            print('Entrada inválida!')

    def menu_crafting(self):
        titulo('CRAFTING')

        receitas = list(self.crafting.receitas.keys())

        for i, receita in enumerate(receitas, start=1):
            print(f'{i}. {receita}')

        try:
            escolha = int(input('Escolha receita: '))
            receita = receitas[escolha - 1]

            self.crafting.craftar(self.jogador, receita)

        except:
            print('Erro no crafting!')


def fibonacci(n):
    if n <= 0:
        return []

    sequencia = [0, 1]

    while len(sequencia) < n:
        sequencia.append(sequencia[-1] + sequencia[-2])

    return sequencia[:n]


def numero_primo(numero):
    if numero < 2:
        return False

    for i in range(2, int(math.sqrt(numero)) + 1):
        if numero % i == 0:
            return False

    return True



def gerar_primos(limite):
    return [n for n in range(2, limite + 1) if numero_primo(n)]


class Estatisticas:
    def __init__(self):
        self.monstros_derrotados = 0
        self.ouro_coletado = 0
        self.itens_encontrados = 0
        self.dano_total = 0
        self.tempo_jogado = 0

    def exibir(self):
        titulo('ESTATÍSTICAS')
        print(f'Monstros derrotados: {self.monstros_derrotados}')
        print(f'Ouro coletado: {self.ouro_coletado}')
        print(f'Itens encontrados: {self.itens_encontrados}')
        print(f'Dano total: {self.dano_total}')
        print(f'Tempo jogado: {self.tempo_jogado} segundos')


def main():
    titulo('RPG SUPREMO PYTHON')

    print('1. Novo jogo')
    print('2. Carregar jogo')

    escolha = input('Escolha: ')

    jogo = Jogo()

    if escolha == '1':
        jogo.criar_personagem()

    elif escolha == '2':
        jogador = SaveManager.carregar()

        if jogador:
            jogo.jogador = jogador
        else:
            jogo.criar_personagem()

    else:
        jogo.criar_personagem()

    jogo.menu_principal()


if __name__ == '__main__':
    main()
