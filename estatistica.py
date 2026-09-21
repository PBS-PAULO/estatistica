import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

st.set_page_config(page_title="Regra Empírica - Distribuição Normal", layout="wide")
st.title("📊 Análise Passo a Passo da Regra Empírica (68.2% - 95.4% - 99.7%)")

st.sidebar.header("Parâmetros de Entrada")
opcao = st.sidebar.radio("Como deseja inserir os dados?", ["Definir Média e Desvio Padrão", "Inserir Lista de Dados"])

if opcao == "Definir Média e Desvio Padrão":
    media = st.sidebar.number_input("Média (µ)", value=5.0)
    dp = st.sidebar.number_input("Desvio Padrão (σ)", value=5.0, min_value=0.001)
    dados = None
else:
    raw_input = st.sidebar.text_area("Cole os números (separados por vírgula ou espaço):", "10, 12, 15, 8, 9, 11, 14, 10, 13")
    try:
        dados = np.array([float(x) for x in raw_input.replace(",", " ").split()])
        media = float(np.mean(dados))
        dp = float(np.std(dados, ddof=1)) if len(dados) > 1 else 1.0
    except Exception:
        st.error("Por favor, insira números válidos.")
        st.stop()

# ==========================================
# CÁLCULOS PASSO A PASSO
# ==========================================
st.subheader("1. Memória de Cálculo e Análise Passo a Passo")

# Cálculo dos desvios para a direita (positivos)
p1 = media + 1 * dp
p2 = media + 2 * dp
p3 = media + 3 * dp

# Cálculo dos desvios para a esquerda (negativos)
n1 = media - 1 * dp
n2 = media - 2 * dp
n3 = media - 3 * dp

col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    st.markdown("### 🔹 Parâmetros Fundamentais")
    st.write(f"• **Média ($\mu$):** `{media:.4f}`")
    st.write(f"• **Desvio Padrão ($\sigma$):** `{dp:.4f}`")
    
    st.markdown("### 🔹 Cálculos dos Limites do Eixo X")
    st.write(f"• **$+1\sigma$:** $\mu + 1\sigma = {media:.2f} + 1({dp:.2f}) = {p1:.2f}$")
    st.write(f"• **$+2\sigma$:** $\mu + 2\sigma = {media:.2f} + 2({dp:.2f}) = {p2:.2f}$")
    st.write(f"• **$+3\sigma$:** $\mu + 3\sigma = {media:.2f} + 3({dp:.2f}) = {p3:.2f}$")
    st.write(f"• **$-1\sigma$:** $\mu - 1\sigma = {media:.2f} - 1({dp:.2f}) = {n1:.2f}$")
    st.write(f"• **$-2\sigma$:** $\mu - 2\sigma = {media:.2f} - 2({dp:.2f}) = {n2:.2f}$")
    st.write(f"• **$-3\sigma$:** $\mu - 3\sigma = {media:.2f} - 3({dp:.2f}) = {n3:.2f}$")

with col_calc2:
    st.markdown("### 🔹 Áreas e Intervalos da Regra Empírica")
    st.info(f"** Intervalo $\pm 1\sigma$ (68.2% dos dados):**\n Entre **{n1:.2f}** e **{p1:.2f}** (34.1% de cada lado da média)")
    st.warning(f"** Intervalo $\pm 2\sigma$ (95.4% dos dados):**\n Entre **{n2:.2f}** e **{p2:.2f}** (+13.6% em cada cauda intermédia)")
    st.error(f"** Intervalo $\pm 3\sigma$ (99.7% dos dados):**\n Entre **{n3:.2f}** e **{p3:.2f}** (+2.1% nas extremidades)")

# ==========================================
# CONSTRUÇÃO DO GRÁFICO
# ==========================================
st.subheader("2. Gráfico da Distribuição Normal (Curva de Gauss)")

fig, ax = plt.subplots(figsize=(12, 6))

# Vetor de pontos no eixo x
x = np.linspace(media - 4 * dp, media + 4 * dp, 1000)
y = stats.norm.pdf(x, media, dp)

# Desenhar curva principal
ax.plot(x, y, color='black', linewidth=2)

# Preenchimento das áreas
# 1 Sigma (Verde)
x_1s = np.linspace(n1, p1, 500)
ax.fill_between(x_1s, stats.norm.pdf(x_1s, media, dp), color='green', alpha=0.6, label='±1σ (68.2%)')

# 2 Sigma (Amarelo/Laranja)
x_2s_left = np.linspace(n2, n1, 200)
x_2s_right = np.linspace(p1, p2, 200)
ax.fill_between(x_2s_left, stats.norm.pdf(x_2s_left, media, dp), color='orange', alpha=0.6, label='±2σ (95.4%)')
ax.fill_between(x_2s_right, stats.norm.pdf(x_2s_right, media, dp), color='orange', alpha=0.6)

# 3 Sigma (Vermelho)
x_3s_left = np.linspace(n3, n2, 200)
x_3s_right = np.linspace(p2, p3, 200)
ax.fill_between(x_3s_left, stats.norm.pdf(x_3s_left, media, dp), color='red', alpha=0.6, label='±3σ (99.7%)')
ax.fill_between(x_3s_right, stats.norm.pdf(x_3s_right, media, dp), color='red', alpha=0.6)

# Linhas verticais para os desvios
pontos = [n3, n2, n1, media, p1, p2, p3]
rotulos_sigma = ['-3σ', '-2σ', '-1σ', 'μ', '1σ', '2σ', '3σ']

for pt, rot in zip(pontos, rotulos_sigma):
    ax.axvline(pt, color='gray', linestyle='--', alpha=0.7)

# Rotulagem do eixo X com valores numéricos e símbolos de sigma
ticks_labels = [f"{rot}\n({pt:.1f})" for pt, rot in zip(pontos, rotulos_sigma)]
ax.set_xticks(pontos)
ax.set_xticklabels(ticks_labels, fontsize=10, fontweight='bold')

# Textos com percentagens no gráfico
max_y = max(y)
ax.text(media - 0.5 * dp, max_y * 0.3, '34.1%', fontsize=11, color='white', fontweight='bold')
ax.text(media + 0.1 * dp, max_y * 0.3, '34.1%', fontsize=11, color='white', fontweight='bold')
ax.text(media - 1.6 * dp, max_y * 0.1, '13.6%', fontsize=10, color='black', fontweight='bold')
ax.text(media + 1.1 * dp, max_y * 0.1, '13.6%', fontsize=10, color='black', fontweight='bold')
ax.text(media - 2.6 * dp, max_y * 0.03, '2.1%', fontsize=9, color='black', fontweight='bold')
ax.text(media + 2.1 * dp, max_y * 0.03, '2.1%', fontsize=9, color='black', fontweight='bold')

ax.set_title(f"Regra Empírica — Média (μ) = {media:.2f} | Desvio Padrão (σ) = {dp:.2f}", fontsize=14)
ax.set_ylabel("Densidade de Probabilidade")
ax.legend(loc='upper right')

st.pyplot(fig)
