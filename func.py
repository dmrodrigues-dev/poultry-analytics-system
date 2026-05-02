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


def obter_linhas(tabela, order='asc'):
    '''
    :param tabela: nome da tabela
    :param order: 'asc' or 'desc' para ascendente ou descendente
    EXEMPLO: mostrar_linhas('lotes', ('Q.Inicial','Q.Atual'), (9,9))
    '''
    if not verificar_tab(tabela):
        return

    cursor.execute(f'select * from {tabela} order by id {order}')
    return cursor.fetchall()


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


def del_linha(tabela, linha_id):
    '''
    :param tabela: nome da tabela
    :param linha_id: identificador da linha (chave primária)
    '''
    if not verificar_tab(tabela):
        return

    confirm = ''
    while confirm != 's':
        confirm = input('Confirmar Deleção? [s/n]').lower()
        if confirm == 'n':
            return

    cursor.execute(f'delete from {tabela} where id =%s', (linha_id,))


def updt_linha(tabela, coluna, dado, linha_id):
    '''
    :param tabela: nome da tabela
    :param coluna: coluna do dado a ser mudado
    :param dado: novo dado da linha
    :param linha_id: identificador da linha (chave primaria)
    '''
    if not verificar_tab(tabela):
        return

    cursor.execute(f'update {tabela} set {coluna} = %s where id = %s', (dado,linha_id))


def retornar_dado(tabela, coluna, linha_id):
    '''
    :param tabela: Tabela do dado desejado
    :param coluna: Coluna do dado desejado
    :param linha_id: id (chave primária) do dado desejado
    :return: dado específico
    '''
    if not verificar_tab(tabela):
        return

    cursor.execute(f'select {coluna} from {tabela} where id = %s', (linha_id,))
    dado = cursor.fetchone()
    return dado[0]


def obter_rdl():
    cursor.execute("select coalesce(sum(valor), 0) as receitas, "
                   "coalesce((select sum(valor) from financeiro where categoria != 'Ovos' and dia >= curdate() - interval 30 day), 0) as despesas, "
                   "(coalesce(sum(valor), 0) / nullif(sum(qtd), 0)) as preco_ovo "
                   "from financeiro where categoria = 'Ovos' and dia >= curdate() - interval 30 day")
    return cursor.fetchall()[0]


def receitas_despesas_lucro():
    '''
    :return: Dicionário com receitas, despesas, lucro líquido e preço médio do ovo, nos últimos 30 dias
    '''

    receitas,despesas,ticket = obter_rdl()
    res = {'Receitas': receitas,
           'Despesas': despesas,
           'Lucro': receitas - despesas,
           'Preço médio do Ovo': round(ticket, 2) if ticket is not None else 0}
    return res


def estoque():
    '''
    :return: Dicionário com estoque de ovos e rações
    '''
    est = {'Ovos': 0,
           'R.Pre-Ini': 0,
           'R.Inicial': 0,
           'R.Crescim': 0,
           'R.Postura': 0}

    cursor.execute("select categoria, coalesce(sum(qtd), 0) from financeiro group by categoria;")
    # lista com linhas, cada linha com uma categoria e uma quantidade comprada
    fetch = cursor.fetchall()  # lista com linhas, cada linha com uma categoria e uma quantidade comprada
    financeiro = {i[0]: i[1] for i in fetch}

    cursor.execute("select coalesce(sum(ovos_inteiros), 0), coalesce(sum(consumo_racao), 0) from producao")
    # lista com soma dos ovos produzidos e ração de postura consumida, respectivamente
    fetch = cursor.fetchall()[0]
    producao = {'Ovos': fetch[0], 'R.Postura': fetch[1]}

    cursor.execute("select categoria, coalesce(sum(consumo_racao),0) from preproducao group by categoria")
    # lista com linhas, cada linha com uma categoria e uma quantidade consumida na tabela prep
    fetch = cursor.fetchall()
    producao.update({i[0]: i[1] for i in fetch})

    # prod - financ para ovos
    # financ - prod para rações
    for i in est:
        if i == 'Ovos':
            est[i] = producao.get('Ovos', 0) - financeiro.get('Ovos',0)
        else:
            est[i] = financeiro.get(i,0) - producao.get(i,0)
    return est


def obter_lote_prod():
    cursor.execute(f"select lotes.id,"
                   f"lotes.qtd_atual as plantel,"
                   f"avg(p.taxa) as postura,"
                   f"(coalesce(sum(p.mortalidade), 0)*100 / max(lotes.qtd_inicial)) as mortalidade,"
                   f"avg(p.consumo_racao / (p.ovos_inteiros / nullif(p.taxa / 100, 0))) as r_ave_dia  from producao as p "
                   f"join lotes on lotes.id = p.id_lote "
                   f"where dia >= curdate() - interval 30 day and lotes.racao = 'R.Postura' "
                   f"group by lotes.id; ")
    return cursor.fetchall()


def montar_lote_prod(lote):
    caracteristicas = {'ID': lote[0],
                       'Plantel': lote[1],
                       'Taxa de Postura': round(float(lote[2]), 2),
                       'Taxa de Mortalidade': round(float(lote[3]), 2),
                       'Consumo de Ração/Ave': round(float(lote[4]), 2),
                       'Postura': True}
    return caracteristicas


def obter_lote_prep():
    cursor.execute(f"select lotes.id,"
                   f"lotes.racao as categoria,"
                   f"lotes.qtd_atual as plantel,"
                   f"("
                   f"	select preproducao.peso from preproducao "
                   f"	where id_lote = lotes.id "
                   f"    order by preproducao.dia desc "
                   f"    limit 1) as peso,"
                   f"(coalesce(sum(prep.mortalidade), 0)*100 / max(lotes.qtd_inicial)) as mortalidade from preproducao as prep "
                   f"join lotes on lotes.id = prep.id_lote "
                   f"where dia >= curdate() - interval 30 day and lotes.racao != 'R.Postura' "
                   f"group by lotes.id; ")
    return cursor.fetchall()


def montar_lote_prep(lote):
    caracteristicas = {'ID': lote[0],
                       'Categoria': lote[1],
                       'Plantel': lote[2],
                       'Peso': lote[3],
                       'Taxa de Mortalidade': lote[4],
                       'Postura': False}
    return caracteristicas


def dash_lotes():
    '''
    :return: Lista com ID, plantelm taxas de postura e mortalidade, e consumo ave/dia de cada lote nos últimos 30 dias
    '''
    lotes = []

    linhas_prod = obter_lote_prod()
    for lote in linhas_prod:
        lotes.append(montar_lote_prod(lote))

    linhas_prep = obter_lote_prep()
    for lote in linhas_prep:
        lotes.append(montar_lote_prep(lote))

    return lotes


def total():
    '''
    :return: Dicionário com plantel total e taxas de postura e mortalidade da granja nos últimos 30 dias
    '''
    res = {'Plantel Total': '',
           'Taxa de Postura Total': '',
           'Taxa de Mortalidade Total': ''}

    cursor.execute("select coalesce(sum(qtd_atual),0) from lotes")
    res['Plantel Total'] = cursor.fetchall()[0][0]

    cursor.execute("select coalesce(avg(taxa), 0) from producao where dia >= curdate() - interval 30 day")
    res['Taxa de Postura Total'] = round(cursor.fetchall()[0][0], 2)

    cursor.execute("select ("
                   "	coalesce((select sum(mortalidade) from producao where dia >= curdate() - interval 30 day), 0) +"
                   "	coalesce((select sum(mortalidade) from preproducao where dia >= curdate() - interval 30 day), 0)"
                   "	) * 100 / (select sum(qtd_inicial) from lotes)")
    res['Taxa de Mortalidade Total'] = round(cursor.fetchall()[0][0], 2)

    return res
