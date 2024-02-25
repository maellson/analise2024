import streamlit as st
import pandas as pd
import plotly.express as px


# pagina na horizontal
st.set_page_config(layout='wide')
# código

df = pd.read_csv("relatrorio2024.csv", sep=";",
                 decimal=".", encoding="cp1252", dtype={34: str})
df['Inscricao'] = df['setor'].astype(str) + '.' + df['quadra'].astype(
    str) + '.' + df['lote'].astype(str) + '.' + df['Unidade'].astype(str)
# df.columns

novoDF = df[['Matrícula', 'Bairro', 'setor', 'quadra',
             'lote', 'Unidade', 'Inscricao', 'area_calculo',
             'area_edif_unid', 'area_lote', 'area_priv_unid', 'cod_condominio',
             'fracao_ideal', 'Aliquota', 'vlr_iptu', 'vlr_m2_terreno',
             'vlr_venal_terr', 'vlr_m2_edif', 'vlr_venal_edif', 'tipo_imovel',
             'situacao', 'pedologia', 'tipo_construcao', 'ocupacao']].copy()


# Renomeando a coluna
# Renomeando colunas sem usar inplace=True
novoDF = novoDF.rename(columns={'Matrícula': 'matricula'})
novoDF = novoDF.rename(columns={'Unidade': 'unidade'})
novoDF = novoDF.rename(columns={'Bairro': 'bairro'})

# novoDF.columns
# print(df['area_lote'].dtypes)


novoDF['matricula'] = novoDF['matricula'].apply(lambda x: f"{x:.0f}")

# fim código primeira parte


# Adicionando um título ao aplicativo
st.title('Análise de Imóveis')

# Adicionando um subtítulo para a seção de filtragem
st.header('Filtragem de Imóveis no Centro com Lote Menor que 100m²')

# Explicação do que será feito
st.write('A seguir, apresentamos os registros de imóveis localizados no bairro "Centro",' +
         'cuja área do lote é menor que 100m². Este filtro permite identificar imóveis' +
         'com lotes relativamente pequenos na região central.')

# Realiza o filtro
filtro_centro = novoDF[(novoDF['bairro'] == 'CENTRO')
                       & (novoDF['area_lote'] < 100)]

# Exibe o DataFrame filtrado
st.write(filtro_centro)


# Título do aplicativo
st.header('Análise de Imóveis por Setor, Quadra e Lote')
st.write('soma de valores por lote')

# Entradas dinâmicas
setor_especificado = st.text_input('Setor', '001')
quadra_especificada = st.text_input('Quadra', '01')
lote_especificado = st.text_input('Lote', '001')

# Botão para aplicar filtros
if st.button('Aplicar Filtros'):
    # Convertendo entradas para inteiros antes do filtro
    setor_especificado_int = int(setor_especificado)
    quadra_especificada_int = int(quadra_especificada)
    lote_especificado_int = int(lote_especificado)
    # Filtrando o DataFrame
    filtrado_df = novoDF[(novoDF['setor'] == setor_especificado_int) &
                         (novoDF['quadra'] == quadra_especificada_int) &
                         (novoDF['lote'] == lote_especificado_int)]

    # imprime o filtro
    st.write(filtrado_df)

    # Contando o número de unidades. poderia usar o len(filtrado_df)
    num_unidades = filtrado_df.shape[0]

    # Calculando as somas
    soma_area_lote = filtrado_df['area_lote'].sum()
    soma_area_edif = filtrado_df['area_edif_unid'].sum()
    soma_vlr_iptu = filtrado_df['vlr_iptu'].sum()

    # Exibindo os resultados
    st.markdown(f'**Quantidade de Unidades:**  {num_unidades}')
    st.markdown(f'**Soma da Área do Lote:** {soma_area_lote} m²')
    st.markdown(f'**Soma da Área Edificada:** {soma_area_edif} m²')
    st.markdown(f'**Soma do Valor do IPTU: R$** {soma_vlr_iptu:,.2f}')

    st.subheader(
        'Seguindao a filtragem para encontrarmso a unidade com maior área e com a menor área²')

    # Explicação do que será feito
    st.write('A seguir, apresentamos os registros de imóveis localizados no bairro "Centro",' +
             'cuja área do lote é menor que 100m². Este filtro permite identificar imóveis' +
             'com lotes relativamente pequenos na região central.')
    # Calculando estatísticas descritivas
    media_area = filtrado_df['area_lote'].mean()
    max_area = filtrado_df['area_lote'].max()
    min_area = filtrado_df['area_lote'].min()

    # Encontrando as unidades com a maior e menor área
    unidade_max_area = filtrado_df[filtrado_df['area_lote'] == max_area]
    unidade_min_area = filtrado_df[filtrado_df['area_lote'] == min_area]

    # Exibindo os resultados
    st.markdown(f"**Média da Área do Lote:** {media_area:.2f} m²")
    st.markdown(f'**Maior Área do Lote:** {max_area} m²')
    st.subheader('**Unidade(s) com a Maior Área do Lote:**')
    st.write(unidade_max_area)

    st.markdown(f'**Menor Área do Lote:** {min_area} m²')
    st.subheader('**Unidade(s) com a Menor Área do Lote:**')
    st.write(unidade_min_area)

    if filtrado_df.empty:
        st.write("Nenhum registro encontrado com os filtros aplicados.")
    else:
        # Botões para gerar cada gráfico após o filtro
        if st.button('Gerar Gráfico de Outliers em Área do Lote'):
            fig1 = px.box(filtrado_df, y='area_lote', points="all", notched=True,
                          title="Boxplot de Área do Lote")
            st.plotly_chart(fig1, use_container_width=True)

        if st.button('Gerar Gráfico de Outliers em Valores de IPTU'):
            fig2 = px.box(filtrado_df, y='vlr_iptu', points="all", notched=True,
                          title="Boxplot de Valores de IPTU")
            st.plotly_chart(fig2, use_container_width=True)

        if st.button('Gerar Gráfico de Dispersão entre Área para Cálculo e Valor do IPTU'):
            fig3 = px.scatter(filtrado_df, x='area_calculo', y='vlr_iptu',
                              hover_data=['matricula'],
                              title="Dispersão entre Área para Cálculo e Valor do IPTU")
            st.plotly_chart(fig3, use_container_width=True)


# novo projet continuação área de graficos
