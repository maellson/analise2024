import streamlit as st
import pandas as pd
import plotly.express as px


# pagina na horizontal
st.set_page_config(layout='wide')
# código

df = pd.read_csv("lancamento_2024.csv", sep=";",
                 decimal=".", encoding="cp1252", dtype={34: str})
# df.columns
df['Inscricao'] = df['setor'].astype(str) + '.' + df['quadra'].astype(
    str) + '.' + df['lote'].astype(str) + '.' + df['Unidade'].astype(str)

# df['vlr_iptu_maelson'] = if(df['area_lote'])


novoDF = df[['Matrícula', 'Bairro', 'setor', 'quadra',
             'lote', 'Unidade', 'Inscricao', 'area_calculo',
             'area_edif_unid', 'area_lote', 'area_priv_unid', 'cod_condominio',
             'fracao_ideal', 'Aliquota', 'vlr_iptu', 'vlr_m2_terreno',
             'vlr_venal_terr', 'vlr_m2_edif', 'vlr_venal_edif', 'vlr_tcr', 'tipo_imovel',
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
# st.header('Filtragem de Imóveis no Centro com Lote Menor que 100m²')

# Explicação do que será feito
# st.write('A seguir, apresentamos os registros de imóveis localizados no bairro "Centro",' +
#         'cuja área do lote é menor que 100m². Este filtro permite identificar imóveis' +
#         'com lotes relativamente pequenos na região central.')

# Realiza o filtro
filtro_centro = novoDF[(novoDF['bairro'] == 'CENTRO')
                       & (novoDF['area_lote'] < 100)]

# Exibe o DataFrame filtrado
# st.write(filtro_centro)


# Título do aplicativo
st.header('Análise de Imóveis por Setor, Quadra e Lote e Valor iptu')
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
    if filtrado_df.empty:
        st.write("Nenhum registro encontrado com os filtros aplicados.")
    else:
        # Armazenar o DataFrame filtrado em session_state para uso posterior
        st.session_state['filtrado_df'] = filtrado_df
        st.session_state['filtro_aplicado'] = True
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
            ' Estatística descritiva dos filtro aplicados')

        # Explicação do que será feito
        st.write('A seguir, apresentamos os registros de imóveis conforme o filtro aplicado,'
                 + 'demonstradno toda a estatística descritiva do lote, da área para cálculo,'
                 + ' da área privativa e dos valores de IPTU.')

        # Calculando estatísticas descritivas de área de calculo
        media_area = filtrado_df['area_lote'].mean()
        max_area = filtrado_df['area_lote'].max()
        min_area = filtrado_df['area_lote'].min()
        # calculando estatísticas descritiva de valor de iptu
        # 'area_priv_unid'
        media_vlr_iptu = filtrado_df['vlr_iptu'].mean()
        max_vlr_iptu = filtrado_df['vlr_iptu'].max()
        min_vlr_iptu = filtrado_df['vlr_iptu'].min()

        # calculando estatísticas descritiva da area e cálculo
        media_area_calculo = filtrado_df['area_calculo'].mean()
        max_area_calculo = filtrado_df['area_calculo'].max()
        min_area_calculo = filtrado_df['area_calculo'].min()

        # calculando estatísticas descritiva da area da unidade
        media_area_priv_unid = filtrado_df['area_priv_unid'].mean()
        max_area_priv_unid = filtrado_df['area_priv_unid'].max()
        min_area_priv_unid = filtrado_df['area_priv_unid'].min()

        # Encontrando as unidades com a maior e menor área
        unidade_max_area = filtrado_df[filtrado_df['area_lote']
                                       == max_area]
        unidade_min_area = filtrado_df[filtrado_df['area_lote']
                                       == min_area]

        # Encontrando as unidades com a maior e menor área para calculo
        unidade_max_area_calculo = filtrado_df[filtrado_df['area_calculo']
                                               == max_area_calculo]
        unidade_min_area_calculo = filtrado_df[filtrado_df['area_calculo']
                                               == min_area_calculo]

        # Encontrando as unidades com a maior e menor área de unidade privativa
        unidade_max_area_priv_unid = filtrado_df[filtrado_df['area_priv_unid']
                                                 == max_area_priv_unid]
        unidade_min_area_priv_unid = filtrado_df[filtrado_df['area_priv_unid']
                                                 == min_area_priv_unid]

        # Encontrando as unidades com a maior e menor valor IPTU
        unidade_max_vlr_iptu = filtrado_df[filtrado_df['vlr_iptu']
                                           == max_vlr_iptu]
        unidade_min_vlr_iptu = filtrado_df[filtrado_df['vlr_iptu']
                                           == min_vlr_iptu]
        # Exibindo os resultados
        st.markdown(
            "<h2 style='text-align: center;'><b>Análise da área do Lote</b></h2>", unsafe_allow_html=True)

        st.markdown(f"**Média da Área do Lote:** {media_area:.2f} m²")
        st.markdown(f'**Maior Área do Lote:** {max_area} m²')
        st.markdown('#### **Unidade(s) com a Maior Área do Lote:**')
        st.write(unidade_max_area)
        st.markdown(f'**Menor Área do Lote:** {min_area} m²')
        st.markdown('#### **Unidade(s) com a Menor Área do Lote:**')
        st.write(unidade_min_area)

        # controle de área para Cálculo
        st.markdown(
            "<h2 style='text-align: center;'><b>Análise da área para cálculo</b></h2>", unsafe_allow_html=True)

        st.markdown(
            f"**Média da Área do Lote para calculo:** {media_area_calculo:.2f} m²")
        st.markdown(
            f'**Maior Área do Lote para calculo:** {max_area_calculo} m²')
        st.markdown(
            '#### **Unidade(s) com a Maior Área do Lote para calculo:**')
        st.write(unidade_max_area_calculo)
        st.markdown(
            f'**Menor Área do Lote para calculo:** {min_area_calculo} m²')
        st.markdown(
            '#### **Unidade(s) com a Menor Área do Lote para calculo:**')
        st.write(unidade_min_area_calculo)

        # controle de área privativa unidade
        st.markdown(
            "<h2 style='text-align: center;'><b>Análise da área Privativa da Unidade</b></h2>", unsafe_allow_html=True)

        st.markdown(
            f"**Média da Área privativa da unidade:** {media_area_priv_unid:.2f} m²")
        st.markdown(
            f'**Maior Área privativa da unidade:** {max_area_priv_unid} m²')
        st.markdown(
            '#### **Unidade(s) com a Maior Área privativa da unidade:**')
        st.write(unidade_max_area_priv_unid)
        st.markdown(
            f'**Menor Área privativa da unidade:** {min_area_priv_unid} m²')
        st.markdown(
            '#### **Unidade(s) com a Menor Área privativa da unidade:**')
        st.write(unidade_min_area_priv_unid)

        # controle de valor de iptu
        st.markdown(
            "<h2 style='text-align: center;'><b>Análise do valor do IPTU do Lote</b></h2>", unsafe_allow_html=True)

        st.markdown(
            f"**Média da Valor IPTU do Lote: R$** {media_vlr_iptu:.2f}")
        st.markdown(f'**Maior Valor IPTU do Lote: R$** {max_vlr_iptu}')
        st.markdown('#### **Unidade(s) com a Maior Valor IPTU:**')
        st.write(unidade_max_vlr_iptu)
        st.markdown(f'**Menor Valor IPTU: R$** {min_vlr_iptu}')
        st.markdown(f'#### **Unidade(s) com o Menor Valor IPTU:**')
        st.write(unidade_min_vlr_iptu)


# Verificar se o filtro foi aplicado e se há dados para mostrar
if 'filtro_aplicado' in st.session_state and st.session_state['filtro_aplicado']:
    filtrado_df = st.session_state['filtrado_df']


# # Seu código para mostrar a análise e os botões dos gráficos aqui, por exemplo:
#     if st.button('Gerar Gráfico de Outliers em Área do Lote'):
#         # Seu código para gerar e mostrar o gráfico aqui
#         fig1 = px.box(filtrado_df, y='area_lote', points="all", notched=True,
#                       title="Boxplot de Área do Lote")
#         st.plotly_chart(fig1, use_container_width=True)

#     if st.button('Gerar Gráfico de Outliers em Valores de IPTU'):
#         fig2 = px.box(filtrado_df, y='vlr_iptu', points="all", notched=True,
#                       title="Boxplot de Valores de IPTU")
#         st.plotly_chart(fig2, use_container_width=True)

#     if st.button('Gerar Gráfico de Dispersão entre Área para Cálculo e Valor do IPTU'):
#         fig3 = px.scatter(filtrado_df, x='area_calculo', y='vlr_iptu',
#                           hover_data=['matricula'],
#                           title="Dispersão entre Área para Cálculo e Valor do IPTU")
#         st.plotly_chart(fig3, use_container_width=True) """


# novo projet continuação área de graficos
