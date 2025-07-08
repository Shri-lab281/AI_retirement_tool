import matplotlib.pyplot as plt
import streamlit as st

def plot_projection(age, retirement_age, savings, monthly_saving, corpus_target):
    years = list(range(age, retirement_age + 1))
    balances = []
    for _ in years:
        savings += monthly_saving * 12
        savings *= 1.08
        balances.append(savings)

    plt.figure(figsize=(10, 4))
    plt.plot(years, balances, label="Projected Savings", linewidth=3)
    plt.axhline(corpus_target, color='red', linestyle='--', label='Target Corpus')
    plt.xlabel("Age")
    plt.ylabel("Savings (₹)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def plot_savings_vs_corpus(savings_projection, target_corpus):
    years = list(range(1, len(savings_projection) + 1))
    target_line = [target_corpus] * len(savings_projection)

    fig, ax = plt.subplots()
    ax.plot(years, savings_projection, label="Projected Savings", color='green', marker='o')
    ax.plot(years, target_line, label="Target Corpus", color='red', linestyle='--')
    ax.set_xlabel("Years Until Retirement")
    ax.set_ylabel("₹ Amount")
    ax.set_title("Projected Growth vs Required Retirement Corpus")
    ax.legend()
    ax.grid(True)
    return fig
