import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tablero Control Operaciones", layout="wide")
st.title("📊 Tablero de Control de Operaciones")

archivo = st.file_uploader("Cargue el archivo Excel", type=["xlsx","xls"])

if archivo:
    df = pd.read_excel(archivo)

    df.columns = [str(c).strip() for c in df.columns]

    fecha_col = 'Fecha Grabación Pago'
    proveedor_col = 'PROVEEDOR'
    negocio_col = 'Nombre Negocio'
    gestor_col = 'Gestor responsable negocios'

    if fecha_col in df.columns:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')

    st.sidebar.header('Filtros')

    proveedores = st.sidebar.multiselect('Proveedor', sorted(df[proveedor_col].dropna().astype(str).unique())) if proveedor_col in df.columns else []
    gestores = st.sidebar.multiselect('Gestor', sorted(df[gestor_col].dropna().astype(str).unique())) if gestor_col in df.columns else []

    df_filtrado = df.copy()
    if proveedores:
        df_filtrado = df_filtrado[df_filtrado[proveedor_col].astype(str).isin(proveedores)]
    if gestores:
        df_filtrado = df_filtrado[df_filtrado[gestor_col].astype(str).isin(gestores)]

    c1,c2,c3=st.columns(3)
    c1.metric('Total Operaciones', len(df_filtrado))
    c2.metric('Proveedores', df_filtrado[proveedor_col].nunique())
    c3.metric('Negocios', df_filtrado[negocio_col].nunique())

    st.subheader('Operaciones por Proveedor')
    prov = df_filtrado.groupby(proveedor_col).size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
    st.plotly_chart(px.bar(prov, x=proveedor_col, y='Operaciones'), use_container_width=True)

    st.subheader('Operaciones por Fecha de Grabación')
    fec = df_filtrado.groupby(fecha_col).size().reset_index(name='Operaciones')
    st.plotly_chart(px.line(fec, x=fecha_col, y='Operaciones', markers=True), use_container_width=True)

    col1,col2=st.columns(2)
    with col1:
        st.subheader('Operaciones por Negocio')
        neg = df_filtrado.groupby(negocio_col).size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
        st.plotly_chart(px.bar(neg, x='Operaciones', y=negocio_col, orientation='h'), use_container_width=True)
    with col2:
        st.subheader('Operaciones por Gestor')
        ges = df_filtrado.groupby(gestor_col).size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
        st.plotly_chart(px.bar(ges, x='Operaciones', y=gestor_col, orientation='h'), use_container_width=True)

    st.subheader('Detalle')
    st.dataframe(df_filtrado, use_container_width=True)
