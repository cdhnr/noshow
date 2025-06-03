import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="No-show", layout="wide")

st.title("Dashboard no-show das transportadoras")

caminho_arquivo = os.path.join("dados", "comparativo_entregas.xlsx")

if not os.path.exists(caminho_arquivo):
    st.error("Arquivo não encontrado: 'dados/comparativo_entregas.xlsx'")
    st.stop()

df = pd.read_excel(caminho_arquivo)
df.columns = df.columns.str.strip()

if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'])

st.sidebar.header("Filtros")
filial = st.sidebar.multiselect("Filial", df['Filial'].unique())
status = st.sidebar.multiselect("Status", df['Status'].unique())
transportadora = st.sidebar.multiselect("Transportadora", df['Transportadora'].unique())
motivo = st.sidebar.multiselect("Motivo", df['Motivo'].unique())
responsavel = st.sidebar.multiselect("Responsável", df['Responsável'].unique())

df_filtrado = df.copy()
if filial:
    df_filtrado = df_filtrado[df_filtrado['Filial'].isin(filial)]
if status:
    df_filtrado = df_filtrado[df_filtrado['Status'].isin(status)]
if transportadora:
    df_filtrado = df_filtrado[df_filtrado['Transportadora'].isin(transportadora)]
if motivo:
    df_filtrado = df_filtrado[df_filtrado['Motivo'].isin(motivo)]
if responsavel:
    df_filtrado = df_filtrado[df_filtrado['Responsável'].isin(responsavel)]

st.subheader("Visão Geral")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Registros", len(df_filtrado))
col2.metric("No-Shows", df_filtrado[df_filtrado["Status"] == "No-Show"].shape[0])
col3.metric("Comparecimentos", df_filtrado[df_filtrado["Status"] == "Compareceu"].shape[0])

cores_status = {
    'Compareceu': '#2ecc71',
    'No-Show': '#e74c3c'
}

st.subheader("Status por transportadora")
fig1 = px.bar(
    df_filtrado.groupby(['Transportadora', 'Status']).size().reset_index(name='Total'),
    x='Transportadora', y='Total', color='Status', barmode='group',
    color_discrete_map=cores_status,
    title='No-shows por transportadora'
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Evolução diária por status")
fig2 = px.line(
    df_filtrado.groupby(['Data', 'Status']).size().reset_index(name='Total'),
    x='Data', y='Total', color='Status',
    color_discrete_map=cores_status,
    title='Evolução diária'
)
st.plotly_chart(fig2, use_container_width=True)

df_noshow = df_filtrado[df_filtrado['Status'] == 'No-Show']
if not df_noshow.empty:
    st.subheader("Distribuição de no-show por filial")
    fig_pizza = px.pie(
        df_noshow,
        names='Filial',
        hole=0.4,
        title='Percentual de No-Show por Filial'
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)