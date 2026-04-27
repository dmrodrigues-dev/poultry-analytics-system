import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv()

bank = mysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = bank.cursor()
TABELAS_PERMITIDAS = ['lotes', 'producao', 'galpoes', 'financeiro', 'preproducao']


def mostrar_linhas(tabela, headers, tamanhos, order='asc'):
    '''
    :param tabela: nome da tabela
    :param headers: tupla ou lista com os nomes das colunas
    :param tamanhos: tupla ou lista com a mesma quantidade de colunas, em int
    :param order: 'asc' or 'desc' para ascendente ou descendente
    EXEMPLO: mostrar_linhas('lotes', ('Q.Inicial','Q.Atual'), (9,9))
    '''

    cursor.execute(f'select * from {tabela} order by id {order}')

    print('=' * 120)
    for header, tam_col in zip(headers, tamanhos):
        print(f'| {header.ljust(tam_col, ' ')} ', end='')
    print('|')

    for linha in cursor.fetchall():
        for dado, tam_col in zip(linha, tamanhos):
            print(f'| {str(dado).ljust(tam_col,' ')} ', end='')
        print('|')
    print('='*120)


def verificar_tab(tabela):
    '''
    :param tabela: Tabela que será analisada se está na lista de permitidas
    :return:
    '''
    if tabela not in TABELAS_PERMITIDAS: # verifica se a tabela está na lista de tabelas
        print(f'  {tabela} não encontrada')
        return False
    else:
        return True


# na linha, default não é entendido pelo python, use None no seu lugar
def add_linha(tabela, linha):
    '''
    :param tabela: nome da tabela
    :param linha: tupla que será adicionada, deve conter a quantidade exata de colunas, na ordem correta
    '''
    if not verificar_tab(tabela):
        return

    placeholders = ', '.join(['%s'] * len(linha))  # '%s, %s, %s, %s' para uma linha com 4 itens
    cursor.execute(f'insert into {tabela} values ({placeholders})', linha)  # é mais seguro do que f strings


def del_linha(tabela, id):
    '''
    :param tabela: nome da tabela
    :param id: identificador da linha (chave primária)
    '''
    if not verificar_tab(tabela):
        return

    confirm = ''
    while confirm != 's':
        confirm = input('Confirmar Deleção? [s/n]').lower()
        if confirm == 'n':
            return

    cursor.execute(f'delete from {tabela} where id =%s', (id,))


def updt_linha(tabela, coluna, dado, id):
    '''
    :param tabela: nome da tabela
    :param coluna: coluna do dado a ser mudado
    :param dado: novo dado da linha
    :param id: identificador da linha (chave primaria)
    '''
    if not verificar_tab(tabela):
        return

    cursor.execute(f'update {tabela} set {coluna} = %s where id = %s', (dado,id))


def retornar_dado(tabela, coluna, id):
    '''
    :param tabela: Tabela do dado desejado
    :param coluna: Coluna do dado desejado
    :param id: id (chave primária) do dado desejado
    :return: dado específico
    '''
    cursor.execute(f'select {coluna} from {tabela} where id = %s', (id,))
    dado = cursor.fetchone()
    return dado[0]


def receits_despesas_lucro():
    '''
    :return: Dicionário com receitas, despesas, lucro líquido e preço médio do ovo, nos últimos 30 dias
    '''
    cursor.execute(f"select sum(valor) from financeiro where categoria = 'Ovos' and dia >= curdate() - interval 30 day")
    receits = cursor.fetchall()
    receits = receits[0][0] if receits and receits[0][0] is not None else 0

    cursor.execute(f"select sum(valor) from financeiro where categoria != 'Ovos' and dia >= curdate() - interval 30 day")
    despesas = cursor.fetchall()
    despesas = despesas[0][0] if despesas and despesas[0][0] is not None else 0

    lucro = receits - despesas

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'Ovos' and dia >= curdate() - interval 30 day")
    qtd_ovos = cursor.fetchall()
    qtd_ovos = qtd_ovos[0][0] if qtd_ovos and qtd_ovos[0][0] is not None else 0
    ticket = (receits/qtd_ovos) if qtd_ovos>0 else 0
    return {'Receitas': receits, 'Despesas': despesas, 'Lucro': lucro, 'Preço médio do Ovo': round(ticket,2)}


def estoque():
    '''
    :return: Dicionário com estoque de ovos e rações
    '''
    cursor.execute(f"select sum(ovos_inteiros) from producao")
    fetch = cursor.fetchall()
    produzidos = int(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'Ovos'")
    fetch = cursor.fetchall()
    vendidos = int(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    ovos = produzidos - vendidos

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'R.Pre-Ini'")
    fetch = cursor.fetchall()
    comp_rac_pi = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cursor.execute(f"select sum(consumo_racao) from preproducao where categoria = 'R.Pre-Ini'")
    fetch = cursor.fetchall()
    cons_rac_pi = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    preini = comp_rac_pi - cons_rac_pi

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'R.Inicial'")
    fetch = cursor.fetchall()
    comp_rac_ini = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cursor.execute(f"select sum(consumo_racao) from preproducao where categoria = 'R.Inicial'")
    fetch = cursor.fetchall()
    cons_rac_ini = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    ini = comp_rac_ini - cons_rac_ini

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'R.Crescim'")
    fetch = cursor.fetchall()
    comp_rac_cres = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cursor.execute(f"select sum(consumo_racao) from preproducao where categoria = 'R.Crescim'")
    fetch = cursor.fetchall()
    cons_rac_cres = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cres = comp_rac_cres - cons_rac_cres

    cursor.execute(f"select sum(qtd) from financeiro where categoria = 'R.Postura'")
    fetch = cursor.fetchall()
    comp_rac_pos =  float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    cursor.execute(f"select sum(consumo_racao) from producao")
    fetch = cursor.fetchall()
    cons_rac_pos = float(fetch[0][0]) if fetch and fetch[0][0] is not None else 0

    pos = comp_rac_pos - cons_rac_pos

    est = {'Ovos': ovos, 'R.Pre-Ini': round(preini,2), 'R.Inicial': round(ini,2), 'R.Crescim': round(cres,2), 'R.Postura': round(pos,2)}
    return est


def dash_lotes():
    '''
    :return: Lista com ID, plantelm taxas de postura e mortalidade, e consumo ave/dia de cada lote nos últimos 30 dias
    '''
    lotes = []
    cursor.execute(f"select * from lotes")
    linhas = cursor.fetchall()
    for lote in linhas:
        if lote[8] != 'R.Postura':
            caracteristicas = {'ID': '',
                               'Categoria': lote[8],
                               'Plantel': '',
                               'Peso': '',
                               'Taxa de Mortalidade': '',
                               'Postura': False}

            caracteristicas['ID'] = lote[0]
            caracteristicas['Plantel'] = lote[6]

            cursor.execute('select peso from preproducao where id_lote = %s order by id desc', (lote[0],))
            peso = cursor.fetchall()
            caracteristicas['Peso'] = peso[0][0] if peso and peso[0][0] is not None else 0

            cursor.execute(f"select sum(mortalidade) from preproducao where id_lote = %s and dia >= curdate() - interval 30 day", (lote[0],))
            mor = cursor.fetchall()
            mor = mor[0][0] if mor and mor[0][0] is not None else 0
            mor = int(mor) if mor != None else 0
            taxa_mor = mor * 100 / int(lote[5])
            caracteristicas['Taxa de Mortalidade'] = round(taxa_mor, 2)

        else:
            caracteristicas = {'ID':'',
                            'Plantel':'',
                            'Taxa de Postura':'',
                            'Taxa de Mortalidade':'',
                            'Consumo de Ração/Ave':'',
                            'Postura': True}

            caracteristicas['ID'] = lote[0]
            caracteristicas['Plantel'] = lote[6]

            cursor.execute(f"select taxa from producao where id_lote = %s and dia >= curdate() - interval 30 day", (lote[0],))
            fetch = cursor.fetchall()
            lista =[i[0] for i in fetch]
            taxa_pos = (sum(lista)) / (len(lista) if lista != [] else 1)
            caracteristicas['Taxa de Postura'] = round(taxa_pos,2)

            cursor.execute(f"select sum(mortalidade) from producao where id_lote = %s and dia >= curdate() - interval 30 day", (lote[0],))
            mor = cursor.fetchall()
            mor = mor[0][0] if mor and mor[0][0] is not None else 0
            mor = int(mor) if mor != None else 0
            taxa_mor =  mor*100/int(lote[5])
            caracteristicas['Taxa de Mortalidade'] = round(taxa_mor,2)

            # consumo de ração por ave por lote
            lista = []
            cursor.execute(f'select * from producao where id_lote = %s and dia >= curdate() - interval 30 day', (lote[0],))
            linhas_consumo = cursor.fetchall()
            for tupla in linhas_consumo:
                consumo_dia = float(tupla[6])
                if float(tupla[9]) == 0:
                    continue
                plantel_lote = int(tupla[3]) / (float(tupla[9])/100)
                consumo_ave = consumo_dia / plantel_lote
                lista.append(consumo_ave)
            consumo = sum(lista) / (len(lista) if len(lista) != 0 else 1)
            caracteristicas['Consumo de Ração/Ave'] = round(consumo,2)

        lotes.append(caracteristicas)
    return lotes


def total():
    '''
    :return: Dicionário com plantel total e taxas de postura e mortalidade da granja nos últimos 30 dias
    '''
    res = {'Plantel Total': '',
           'Taxa de Postura Total': '',
           'Taxa de Mortalidade Total': ''}

    cursor.execute(f"select sum(qtd_atual) from lotes")
    soma = cursor.fetchall()
    soma = soma[0][0] if soma and soma[0][0] is not None else 0
    res['Plantel Total'] = soma


    cursor.execute(f"select taxa from producao where dia >= curdate() - interval 30 day")
    fetch = cursor.fetchall()
    lista = [i[0] for i in fetch]
    taxa_pos = (sum(lista)) / (len(lista) if lista != [] else 1)
    res['Taxa de Postura Total'] = round(taxa_pos,2)

    cursor.execute(f"select sum(mortalidade) from producao where dia >= curdate() - interval 30 day")
    mor = cursor.fetchall()
    mor = mor[0][0] if mor and mor[0][0] is not None else 0
    cursor.execute(f"select sum(qtd_inicial) from lotes")
    plantel_ini = cursor.fetchall()
    plantel_ini = plantel_ini[0][0] if plantel_ini and plantel_ini[0][0] is not None else 0
    mor = int(mor) if mor != None else 0
    taxa_mor =  mor*100/int(plantel_ini)
    res['Taxa de Mortalidade Total'] = round(taxa_mor,2)

    return res