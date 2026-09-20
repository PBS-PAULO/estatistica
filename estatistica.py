import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Calculadora Estatística", layout="wide")
st.title("📊 Painel de Análise Estatística Interativa")

modo = st.sidebar.radio("Modo de Entrada", ["Digitar/Colar Dados", "Simulação Gaussiana/Normal"])

nome_var = st.sidebar.text_input("Nome da Variável", "Medição")

dados = []

if modo == "Digitar/Colar Dados":
    texto_dados = st.text_area("Cole os números separados por espaço, vírgula ou quebra de linha:", "10, 12, 15, 8, 9, 11, 14, 10, 13")
    if texto_dados:
        try:
            dados = [float(x) for x in texto_dados.replace(",", " ").split()]
        except ValueError:
            st.error("Por favor, insira apenas valores numéricos.")

else:
    col1, col2, col3 = st.columns(3)
    media_input = col1.number_input("Média (µ)", value=5.0)
    dp_input = col2.number_input("Desvio Padrão (σ)", value=5.0, min_value=0.1)
    n_input = col3.number_input("Tamanho da Amostra (n)", value=100, step=10)
    
    np.random.seed(42)
    dados = np.random.normal(media_input, dp_input, int(n_input))

if len(dados) > 0:
    dados = np.array(dados)
    media = np.mean(dados)
    mediana = np.median(dados)
    dp_s = np.std(dados, ddof=1) if len(dados) > 1 else 0
    var_s = np.var(dados, ddof=1) if len(dados) > 1 else 0

    st.subheader(f"Resultados para: {nome_var}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Amostra (n)", len(dados))
    c2.metric("Média", f"{media:.4f}")
    c3.metric("Mediana", f"{mediana:.4f}")
    c4.metric("Desvio Padrão (s)", f"{dp_s:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(dados, kde=True, stat="density", ax=axes[0], color="skyblue")
    axes[0].axvline(media, color='r', linestyle='-', label=f'Média ({media:.2f})')
    axes[0].axvline(mediana, color='g', linestyle=':', label=f'Mediana ({mediana:.2f})')
    axes[0].set_title("Histograma e Densidade")
    axes[0].legend()

    sns.boxplot(x=dados, ax=axes[1], color="lightgreen")
    axes[1].set_title("Boxplot (Outliers)")

    st.pyplot(fig)