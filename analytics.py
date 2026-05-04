import crud


def receitas_despesas_lucro():
    '''
    :return: Dicionário com receitas, despesas, lucro líquido e preço médio do ovo, nos últimos 30 dias
    '''

    receitas,despesas,ticket = crud.obter_rdl()
    res = {'Receitas': receitas,
           'Despesas': despesas,
           'Lucro': receitas - despesas,
           'Preço médio do Ovo': round(ticket, 2) if ticket is not None else 0}
    return res


def montar_estoque():
    '''
    :return: Dicionário com estoque de ovos e rações
    '''
    est = {'Ovos': 0,
           'R.Pre-Ini': 0,
           'R.Inicial': 0,
           'R.Crescim': 0,
           'R.Postura': 0}

    financeiro,producao = crud.obter_estoque()

    # prod - financ para ovos
    # financ - prod para rações
    for i in est:
        if i == 'Ovos':
            est[i] = producao.get('Ovos', 0) - financeiro.get('Ovos',0)
        else:
            est[i] = financeiro.get(i,0) - producao.get(i,0)
    return est


def montar_lote_prod(lote):
    '''
    :param lote: lista com id, plantel, taxa de postura, taxa de mortalidade e consumo de ração médio
    :return: dicionário com os dados organizados
    '''
    caracteristicas = {'ID': lote[0],
                       'Plantel': lote[1],
                       'Taxa de Postura': round(float(lote[2]), 2),
                       'Taxa de Mortalidade': round(float(lote[3]), 2),
                       'Consumo de Ração/Ave': round(float(lote[4]), 2),
                       'Postura': True}
    return caracteristicas


def montar_lote_prep(lote):
    '''
    :param lote: lista com id, categoria, plantel, peso atual e taxa de mortalidade
    :return: dicionário com os dados organizados
    '''
    caracteristicas = {'ID': lote[0],
                       'Categoria': lote[1],
                       'Plantel': lote[2],
                       'Peso': lote[3],
                       'Taxa de Mortalidade': round(float(lote[4]), 2),
                       'Postura': False}
    return caracteristicas


def dash_lotes():
    '''
    :return: Lista com ID, plantel, taxas de postura e mortalidade, e consumo ave/dia de cada lote nos últimos 30 dias
    '''
    lotes = []

    linhas_prod = crud.obter_lote_prod()
    for lote in linhas_prod:
        lotes.append(montar_lote_prod(lote))

    linhas_prep = crud.obter_lote_prep()
    for lote in linhas_prep:
        lotes.append(montar_lote_prep(lote))

    return lotes

def montar_total():
    '''
    :return: Dicionário com plantel total e taxas de postura e mortalidade da granja nos últimos 30 dias
    '''
    tot = crud.obter_total()
    res = {'Plantel Total': tot[0],
           'Taxa de Postura Total': tot[1],
           'Taxa de Mortalidade Total': tot[2]}

    return res