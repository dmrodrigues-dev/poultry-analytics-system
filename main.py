import func
import os
from datetime import datetime


def input_int(texto):
    '''
    :param texto: String que exibirá no input
    :return: dado convertido em int
    '''
    while True:
        try:
            return int(input(texto))
        except:
            print('Valor Inválido...')

def input_float(texto):
    '''
    :param texto: String que exibirá no input
    :return: dado convertido em float
    '''
    while True:
        try:
            return float(input(texto))
        except:
            print('Valor Inválido...')

def input_data(texto):
    '''
    :param texto: String que exibirá no input
    :return: dado no formato %Y-%m-%d
    '''
    while True:
        try:
            return datetime.strptime(input(texto), '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            print('Valor Inválido...')


def limpar():
    '''
    Limpa o terminal
    '''
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass


def dash():
    '''
    Exibe o dashboard estatístico
    '''
    print('=' * 100)
    print(f'|{'Balanço Financeiro (30 dias)'.center(98)}|')
    print('=' * 100)

    rdl = func.receits_despesas_lucro()
    print(f'| Receitas           : {str(rdl['Receitas']).ljust(26,' ')} | Despesas           : {str(rdl['Despesas']).ljust(25,' ')} |')
    print(f'| Lucro              : {str(rdl['Lucro']).ljust(26,' ')} | Preço médio do ovo : {str(rdl['Preço médio do Ovo']).ljust(25,' ')} |')

    print('=' * 100)
    print(f'|{'Estatísticas da Granja (30 dias)'.center(98)}|')
    print('=' * 100)

    total = func.total()
    print(f'| Plantel Total             : {str(total['Plantel Total']).ljust(68, ' ')} |')
    print(f'| Taxa de Postura Total     : {str(total['Taxa de Postura Total']).ljust(19, ' ')} | Taxa de Mortalidade Total : {str(total['Taxa de Mortalidade Total']).ljust(18, ' ')} |')

    print('=' * 100)
    print(f'|{'Estatísticas dos Lotes (30 dias)'.center(98)}|')
    print('=' * 100)

    dados_lotes = func.dash_lotes()
    for lote in dados_lotes:
        if lote['Postura']:
            print(f'| Lote                 : {str(lote['ID']).ljust(24, ' ')} | Plantel              : {str(lote['Plantel']).ljust(23, ' ')} |')
            print(f'| Taxa de Postura      : {str(lote['Taxa de Postura']).ljust(24, ' ')} | Taxa de Mortalidade  : {str(lote['Taxa de Mortalidade']).ljust(23, ' ')} |')
            print(f'| Consumo de Ração/Ave : {str(lote['Consumo de Ração/Ave']).ljust(73, ' ')} |')
        else:
            print(f'| Lote                 : {str(lote['ID']).ljust(24, ' ')} | Plantel              : {str(lote['Plantel']).ljust(23, ' ')} |')
            print(f'| Categoria            : {str(lote['Categoria']).ljust(24, ' ')} | Taxa de Mortalidade  : {str(lote['Taxa de Mortalidade']).ljust(23, ' ')} |')
            print(f'| Peso médio           : {str(lote['Peso']).ljust(73, ' ')} |')
        print('=' * 100)

    print(f'|{'Estoque'.center(98)}|')
    print('=' * 100)

    estoq = func.estoque()
    print(f'| Ração Pré-Inicial : {str(estoq['R.Pre-Ini']).ljust(27, ' ')} | Ovos              : {str(estoq['Ovos']).ljust(26, ' ')} |')
    print(f'| Ração Inicial     : {str(estoq['R.Inicial']).ljust(27, ' ')} || Ração Crescimento: {str(estoq['R.Crescim']).ljust(26, ' ')} |')
    print(f'| Ração Postura     : {str(estoq['R.Postura']).ljust(76, ' ')} |')

    print('=' * 100)


def menu(titulo, opcoes, mensagem):
    '''
    Exibe um menu
    :param titulo: título do menu
    :param opcoes: Dicionário com opções de escolha do usuário
    :param mensagem: String que será exibida no input
    :return: opção escolhida pelo usuário
    '''
    print('='*100)
    print(f'|{titulo.center(98)}|')
    print('='*100)
    for chave,valor in opcoes.items():
        print(f'| [{chave}] - {valor.ljust(90,' ')} |')
    print('='*100)

    while True:
        escolha = input(mensagem).strip()
        if escolha.isdigit():
            if int(escolha) in opcoes:
                return int(escolha)
        print("  Opção inválida. Tente novamente.")


def atom_prod(linha):
    '''
    Atualiza o plantel do lote com base na mortalidade inserida na tabela producao
    :param linha: Lista que será adicionada na tabela producao
    '''
    func.add_linha('producao', tuple(linha))

    if int(linha[5]) > 0:
        atual = int(func.retornar_dado('lotes', 'qtd_atual', linha[1])) - int(linha[5])
        func.updt_linha('lotes', 'qtd_atual', atual, linha[1])


def atom_pre(linha):
    '''
    Atualiza o plantel do lote com base na mortalidade inserida na tabela preproducao
    :param linha: linha: Lista que será adicionada na tabela preproducao
    '''
    func.add_linha('preproducao', tuple(linha))

    if int(linha[3]) > 0:
        atual = int(func.retornar_dado('lotes', 'qtd_atual', linha[1])) - int(linha[3])
        func.updt_linha('lotes', 'qtd_atual', atual, linha[1])

def taxa_diaria(prod, id_lote):
    '''
    :param prod: produção de ovos inteiros do dia
    :param id_lote: id do lote
    :return: Taxa de postura do dia em float
    '''
    qtd = func.retornar_dado('lotes', 'qtd_atual', id_lote)

    return prod*100/qtd


def main():
    while True:
        limpar()
        escolha = menu('MENU', {1: 'Visualizar Estatísticas',
                                2: 'Administrar Produção',
                                3: 'Administrar Lotes Pré-Produção',
                                4: 'Administrar Movimentações',
                                5: 'Administrar Galpões',
                                6: 'Administrar Lotes',
                                7: 'Sair'}, '  Insira sua escolha: ')
        limpar()

        match escolha:
            case 1:
                dash()

            case 2:
                escolha_prod = menu('Produção', {1: 'Consultar Registros',
                                                 2: 'Anotar Produção de hoje',
                                                 3: 'Editar Registro',
                                                 4: 'Voltar'}, '  Insira sua escolha: ')

                match escolha_prod:
                    case 1:
                        try:
                            func.mostrar_linhas('producao', ('ID', 'Lote', 'Data', 'Ovos.Int', 'Ovos.Def',
                                                             'Mortes', 'Ração', 'Água', 'Obs', 'Postura(%)'),
                                                (5,4,10,8,8,6,5,5,28,10))
                        except Exception as e:
                            print(f'  Erro: {e}')
                    case 2:
                        linha = [None,
                                 input_int('  Lote: '),
                                 input_data('  Data: '),
                                 input_int('  Ovos Inteiros: '),
                                 input_int('  Ovos Quebrados: '),
                                 input_int('  Mortalidade: '),
                                 input_float('  Consumo de Ração: '),
                                 input_float('  Consumo de Água: '),
                                 input('  Observação: ')]
                        try:
                            taxa = taxa_diaria(int(linha[3]), int(linha[1]))
                            linha.append(taxa)
                            atom_prod(linha)
                            func.bank.commit()
                            print(' Registro Adicionado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 3:
                        id = input_int('  ID do registro a editar: ')
                        coluna = input('  Coluna do dado a editar: ')
                        dado = input('  Novo dado: ')
                        try:

                            if coluna == 'mortalidade':
                                lote = func.retornar_dado('producao', 'id_lote',id)
                                antigo = int(func.retornar_dado('lotes', 'qtd_atual',lote))
                                original = antigo + int(func.retornar_dado('producao', 'mortalidade',id))
                                novo = original - int(dado)
                                func.updt_linha('lotes', 'qtd_atual', novo, lote)
                            elif coluna == 'ovos_inteiros':
                                qtd_original = (int(func.retornar_dado('producao','ovos_inteiros',id))/
                                                (float(func.retornar_dado('producao','taxa',id))/100))
                                taxa = (int(dado) * 100) / qtd_original
                                func.updt_linha('producao', 'taxa', taxa, id)

                            func.updt_linha('producao', coluna, dado, id)
                            func.bank.commit()
                            print('  Registro Atualizado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 4:
                        pass

            case 3:
                escolha_pre = menu('Pré-Produção', {1: 'Consultar Registros',
                                                 2: 'Anotar Dados de hoje',
                                                 3: 'Editar Registro',
                                                 4: 'Voltar'}, '  Insira sua escolha: ')

                match escolha_pre:
                    case 1:
                        try:
                            func.mostrar_linhas('preproducao', ('ID', 'Lote', 'Data', 'Mortes'
                                                                    , 'Ração', 'Água', 'Peso', 'Categoria', 'Observação'),
                                                (5, 4, 10, 6, 6, 6, 5, 9, 41))
                        except Exception as e:
                            print(f'  Erro: {e}')
                    case 2:
                        linha = [None,
                                 input_int('  Lote: '),
                                 input_data('  Data: '),
                                 input_int('  Mortalidade: '),
                                 input_float('  Consumo de Ração: '),
                                 input_float('  Consumo de Água: '),
                                 input_float('  Peso médio: '),
                                 input('  Categoria: '),
                                 input('  Observação: ')]
                        try:
                            atom_pre(linha)
                            func.bank.commit()
                            print(' Registro Adicionado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 3:
                        id = input_int('  ID do registro a editar: ')
                        coluna = input('  Coluna do dado a editar: ')
                        dado = input('  Novo dado: ')
                        try:

                            if coluna == 'mortalidade':
                                lote = func.retornar_dado('preproducao', 'id_lote', id)
                                antigo = int(func.retornar_dado('lotes', 'qtd_atual', lote))
                                original = antigo + int(func.retornar_dado('preproducao', 'mortalidade', id))
                                novo = original - int(dado)
                                func.updt_linha('lotes', 'qtd_atual', novo, lote)

                            func.updt_linha('preproducao', coluna, dado, id)
                            func.bank.commit()
                            print('  Registro Atualizado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 4:
                        pass

            case 4:
                escolha_mov = menu('financeiro', {1: 'Consultar Movimentações',
                                                  2: 'Registrar Nova Movimentação',
                                                  3: 'Editar Registro',
                                                  4: 'Deletar Registro',
                                                  5: 'Voltar'}, '  Insira sua escolha: ')
                match escolha_mov:
                    case 1:
                        try:
                            func.mostrar_linhas('financeiro', ('ID', 'Data', 'Categoria', 'Quantidade',
                                                               'Valor', 'Fornecedor/Comprador', 'Obs'),
                                                (5, 10, 9, 10, 8, 27, 29))
                        except Exception as e:
                            print(f'  Erro: {e}')
                    case 2:
                        linha = [None,
                                 input_data('  Data: '),
                                 input('  Categoria: '),
                                 input_float('  Quantidade: '),
                                 input_float('  Valor: '),
                                 input('  Fornecedor/Comprador: '),
                                 input('  Obs: ')]
                        try:
                            func.add_linha('financeiro', tuple(linha))
                            func.bank.commit()
                            print('  Nova Movimentação Registrada!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 3:
                        id = input_int('  ID da movimentação a Editar: ')
                        coluna = input('  Coluna do dado a editar: ')
                        dado = input('  Novo Dado: ')
                        try:
                            func.updt_linha('financeiro', coluna, dado, id)
                            func.bank.commit()
                            print('  Registro atualizado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 4:
                        id = input_int(f'  ID do Registro a deletar: ')
                        try:
                            func.del_linha('financeiro', id)
                            func.bank.commit()
                            print('  Registro deletado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 5:
                        pass

            case 5:
                escolha_galp = menu('Galpões', {1: 'Consultar Galpões',
                                                2: 'Cadastrar Novo Galpão',
                                                3: 'Editar Galpão',
                                                4: 'Deletar Galpão',
                                                5: 'Voltar'}, '  Insira sua escolha: ')
                match escolha_galp:
                    case 1:
                        try:
                            func.mostrar_linhas('galpoes', ('ID', 'Área do galpão'), (2,111))
                        except Exception as e:
                            print(f'  Erro: {e}')
                    case 2:
                        linha = [None, input_float(f'  Área(m²): ')]
                        try:
                            func.add_linha('galpoes', tuple(linha))
                            func.bank.commit()
                            print('  Novo Galpão cadastrado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 3:
                        id = input_int('  ID do galpão a editar: ')
                        area = input_float('  Nova área do galpão: ')
                        try:
                            func.updt_linha('galpoes', 'area', area, id)
                            func.bank.commit()
                            print('  Área do Galpão atualizada!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 4:
                        id = input_int('  ID do galpão a deletar: ')
                        try:
                            func.del_linha('galpoes', id)
                            func.bank.commit()
                            print('  Galpão deletado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 5:
                        pass

            case 6:
                escolha_lote = menu('lotes', {1: 'Consultar Lotes',
                                                2: 'Cadastrar Novo Lote',
                                                3: 'Editar Lote',
                                                4: 'Deletar Lote',
                                                5: 'Voltar'}, '  Insira sua escolha: ')
                match escolha_lote:
                    case 1:
                        try:
                            func.mostrar_linhas('lotes', ('ID','Galpão','Nascimento','Início Prod.',
                                                          'Descarte', 'Q.Inicial','Q.Atual','Fornecedor','Ração'),
                                                (2,6,10,12,10,9,9,25,9))
                        except Exception as e:
                            print(f'  Erro: {e}')
                    case 2:
                        linha = [None,
                                 input_int('  ID do Galpão: '),
                                 input_data('  Data de Nascimento: '),
                                 input_data('  Início da Produção: '),
                                 input_data('  Data de Descarte: '),
                                 input_int('  Quantidade Inicial: '),
                                 input_int('  Quantidade Atual: '),
                                 input('  Fornecedor: '),
                                 input('  Ração Utilizada: ')]
                        try:
                            func.add_linha('lotes', tuple(linha))
                            func.bank.commit()
                            print('  Novo Lote cadastrado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 3:
                        id = input_int('  ID do lote a Editar: ')
                        coluna = input('  Coluna do dado a editar: ')
                        dado = input('  Novo Dado: ')
                        try:
                            func.updt_linha('lotes', coluna, dado, id)
                            func.bank.commit()
                            print('  Lote atualizado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 4:
                        id = input_int(f'  ID do Lote a deletar: ')
                        try:
                            func.del_linha('lotes', id)
                            func.bank.commit()
                            print('  Lote deletado!')
                        except Exception as e:
                            func.bank.rollback()
                            print(f'  Erro: {e}')
                    case 5:
                        pass

            case 7:
                print('  Fechando programa, até a próxima...')
                break

        input('Pressione qualquer tecla para continuar...')


if __name__ == '__main__':
    main()