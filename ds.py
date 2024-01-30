import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importando a base de dados
df = pd.read_csv('Base_Mercadinho.csv', encoding='latin1', delimiter=';')

# Criando coluna lucro
df['Lucro'] = round( df['Preço Unitário'] - df['Custo Unitário'],2)

# Retirando duplicatas
coluna_sem_duplicatas = df['Produto'].drop_duplicates()
Categoria_sem_duplicatas = df['Categoria'].drop_duplicates()

# Adicionando um valor padrão vazio ao início da lista de opções
opcoes = [''] + list(coluna_sem_duplicatas)

# Selectbox na barra lateral
menu = st.sidebar.selectbox(':package: Selecione um Produto:', opcoes)

# Título
st.markdown("<h1 style='color: gray;'>Desempenho do Produto</h1>", unsafe_allow_html=True)
if menu:
    st.markdown(f"<h1 style='color: gray;'>{menu}</h1>", unsafe_allow_html=True)

# Tratando 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Criando novas colunas 'Ano' e 'Mes'
df['Ano'] = df['Data'].dt.year
df = df.sort_values('Ano', ascending=False)
df['Mes'] = df['Data'].dt.month
df = df.sort_values('Mes', ascending=False)
df['Dia'] = df['Data'].dt.day
df['Ano_Mes'] = df['Ano'].astype(str) + '-' + df['Mes'].astype(str)
df = df.sort_values('Ano_Mes', ascending=False)

# Tabela saldo no estoque 
df_filtrado = df.loc[(df['Produto'] == menu) ]
pivot_saldo = df_filtrado.pivot_table(index=['Produto'],values=['Movimentação'], aggfunc='sum')

# Renomeando a coluna 
pivot_saldo.rename(columns={'Movimentação': 'Saldo no Estoque'}, inplace=True)   
if menu:
    saldo_atual = pivot_saldo['Saldo no Estoque'].values[0]
    st.subheader(f"Saldo Atual: {saldo_atual:,.2f}", divider="gray")



menu2=st.sidebar.multiselect(':date: Selecione um Ano:', df_filtrado['Ano'].unique())

if menu2:
    # Tabela Receita Sidebar
    df_filtrado = df.loc[(df['Produto'] == menu) & (df['Tipo'] == 'S') & df['Ano'].isin(menu2)]
    pivot_Faturamento = round(df_filtrado.pivot_table(index=['Produto'],values=['Preço Unitário'], aggfunc='sum'),2)

    # Renomeando a coluna 
    pivot_Faturamento.rename(columns={'Preço Unitário': 'Receita'}, inplace=True)   

    Faturamento= pivot_Faturamento['Receita'].values[0]
    st.subheader(f"Faturamento Total: R$ {Faturamento:,.2f}", divider="gray")
    

if menu2:
    # Tabela Lucro Sidebar
    df_filtrado = df.loc[(df['Produto'] == menu) & (df['Tipo'] == 'S') & df['Ano'].isin(menu2)]
    pivot_Lucro = round(df_filtrado.pivot_table(index=['Produto'], values=['Lucro'], aggfunc='sum'),2)

    lucro= pivot_Lucro['Lucro'].values[0]
    st.subheader (f"Lucro: R$ {lucro:,.2f}", divider="gray")

if menu2:
    # Tabela dinâmica Vendas por Loja
    df_filtrado = df.loc[(df['Produto'] == menu) & (df['Tipo'] == 'S') & df['Ano'].isin(menu2)]
    pivot_loja = df_filtrado.pivot_table(index=['Produto', 'Nome Loja', 'Estado'], values=['Movimentação_ABS', 'Preço Unitário', 'Lucro'], aggfunc='sum')

    # Renomeando a coluna 
    pivot_loja.rename(columns={'Preço Unitário': 'Faturamento'}, inplace=True)
    pivot_loja.rename(columns={'Movimentação_ABS': 'Quantidade'}, inplace=True)

    st.write(pivot_loja)


if menu2:
    # Tabela dinâmica Vendas por Loja
    df_filtrado = df.loc[(df['Produto'] == menu) & (df['Tipo'] == 'S') & df['Ano'].isin(menu2)]
    pivot_loja_graf = df_filtrado.pivot_table(index=['Nome Loja'], values=['Movimentação_ABS', 'Preço Unitário', 'Lucro'], aggfunc='sum')

    # Renomeando a coluna 
    pivot_loja_graf.rename(columns={'Preço Unitário': 'Faturamento'}, inplace=True)
    pivot_loja_graf.rename(columns={'Movimentação_ABS': 'Quantidade'}, inplace=True)
    
    # Resetando o índice do DataFrame para que 'Produto', 'Nome Loja' e 'Estado' sejam colunas normais
    pivot_loja_reset = pivot_loja_graf.reset_index()

    # Definindo 'Nome Loja' como o índice do DataFrame
    pivot_loja_reset = pivot_loja_reset.set_index('Nome Loja')

    # Gráfico de barras

    st.bar_chart(pivot_loja_reset, use_container_width=True)   

if menu2:
    # Tabela dinâmica Faturamento por Ano e mês
    df_filtrado_ano = df_filtrado.loc[df_filtrado['Ano'].isin(menu2)]
    pivot_data_graf = df_filtrado_ano.pivot_table(index=['Ano_Mes'], values=['Movimentação_ABS', 'Preço Unitário', 'Lucro'], aggfunc='sum')

    # Renomeando a coluna 
    pivot_data_graf.rename(columns={'Preço Unitário': 'Faturamento'}, inplace=True)
    pivot_data_graf.rename(columns={'Movimentação_ABS': 'Quantidade'}, inplace=True)

    # Resetando o índice do DataFrame
    pivot_data_reset = pivot_data_graf.reset_index()

    # Definindo índice do DataFrame
    pivot_data_reset = pivot_data_reset.set_index('Ano_Mes')

    # Gráfico Linha
    st.subheader('Qtd de vendas x Lucro x Faturamento por ano e mês')
    st.line_chart(pivot_data_reset, use_container_width=True)  
if menu2:
    # Tabela dinâmica Faturamento por Ano e mês
    df_filtrado_ano = df_filtrado.loc[df_filtrado['Ano'].isin(menu2)]
    pivot_data = df_filtrado_ano.pivot_table(index=['Produto','Ano_Mes'], values=['Movimentação_ABS', 'Preço Unitário', 'Lucro'], aggfunc='sum')

    # Renomeando a coluna 
    pivot_data.rename(columns={'Preço Unitário': 'Faturamento'}, inplace=True)
    pivot_data.rename(columns={'Movimentação_ABS': 'Quantidade'}, inplace=True)

    st.write(pivot_data)
# Exibindo a primeira imagem do produto filtrado
if not df_filtrado['Imagem'].empty:
    st.sidebar.image(df_filtrado['Imagem'].iloc[0],use_column_width=True)




    
