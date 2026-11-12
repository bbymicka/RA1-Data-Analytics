"""Gera as análises do RA3 a partir dos CSVs preparados no RA1."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "ra3"
STATES = ["Maharashtra", "Karnataka", "Kerala"]
COLORS = ["#126b82", "#ad4c23", "#754e9e"]
START, END = "2020-04-01", "2021-08-11"
TEST_START = "2021-06-01"
TESTING_SNAPSHOT = "2021-08-09"


def load(name):
    path = ROOT / "data" / "processed" / f"{name}.csv"
    return pd.read_csv(path, parse_dates=["date"]).sort_values("date")


def plot_time(ax, ylabel, title):
    ax.set(ylabel=ylabel, xlabel="Mês/ano do registro", title=title)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4, maxticks=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
    ax.grid(axis="y", alpha=0.25)


def save(fig, filename):
    fig.savefig(OUTPUT / filename, dpi=145, facecolor="white")
    plt.close(fig)


def analyze_cases(cases):
    series = cases[cases["state"].isin(STATES)].pivot(
        index="date", columns="state", values=["confirmed", "cured", "deaths"]
    ).asfreq("D")
    # Diferenciar antes do recorte permite usar 31/03 no cálculo de 01/04.
    daily = series["confirmed"].diff().loc[START:END, STATES]
    stats = daily.agg(["count", "mean", "median", "std", "min", "max"]).T
    stats["amplitude"] = stats["max"] - stats["min"]
    stats["negativos"] = daily.lt(0).sum()
    print("\nVariação diária dos confirmados por estado")
    print(stats.round(2).to_string())
    print("\nPicos da média móvel de sete dias")
    smoothed = daily.rolling(7).mean()
    print(pd.DataFrame({"data": smoothed.idxmax(), "valor": smoothed.max().round(2)}))
    print("\nAcumulados no último dia")
    print(series.loc[END].unstack(0).loc[STATES].to_string())

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), layout="constrained")
    for ax, (field, title) in zip(
        axes, [("confirmed", "Confirmados"), ("cured", "Recuperados"), ("deaths", "Óbitos")]
    ):
        for state, color in zip(STATES, COLORS):
            ax.plot(series.loc[START:END].index, series[field][state].loc[START:END] / 1e6,
                    label=state, color=color)
        plot_time(ax, "Registros (milhões)", title)
    axes[0].legend(loc="upper left", ncols=3)
    fig.suptitle("Evolução dos registros acumulados em três estados", fontweight="bold")
    save(fig, "01_casos.png")

    fig, ax = plt.subplots(figsize=(9, 4.6), layout="constrained")
    low = np.floor(daily.min().min() / 5000)
    high = np.ceil(daily.max().max() / 5000)
    bins = np.arange(low, high + 1) * 5
    for state, color in zip(STATES, COLORS):
        ax.hist(daily[state].dropna() / 1000, bins=bins, histtype="step",
                linewidth=2, color=color, label=state)
    ax.set(title="Distribuição da variação diária dos casos confirmados",
           xlabel="Diferença entre boletins consecutivos (mil casos)", ylabel="Dias por faixa")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    print("\nDias com variação inferior a 10 mil casos")
    print(daily.lt(10000).sum().to_string())
    save(fig, "02_distribuicao.png")
    return daily


def analyze_testing(testing):
    snapshot = testing.loc[testing["date"].eq(TESTING_SNAPSHOT)].dropna(subset=["total_samples"])
    ranked = snapshot.set_index("state")["total_samples"].sort_values(ascending=False)
    print(f"\nTestes em {TESTING_SNAPSHOT} — {len(ranked)} territórios com valor")
    print(ranked.head(8).to_string())

    fig, axes = plt.subplots(2, 1, figsize=(10, 7.6), layout="constrained")
    for state, color in zip(STATES, COLORS):
        state_series = testing.loc[testing["state"].eq(state)].set_index("date").asfreq("D")
        axes[0].plot(state_series.index, state_series["total_samples"] / 1e6,
                     color=color, label=state)
    plot_time(axes[0], "Amostras (milhões)", "Amostras testadas acumuladas em três estados")
    axes[0].legend(loc="upper left")
    top = ranked.head(8).sort_values()
    axes[1].barh(top.index, top / 1e6, color="#126b82")
    axes[1].set(title="Oito maiores totais entre os territórios com registro em 09/08/2021",
                xlabel="Amostras acumuladas (milhões)", ylabel="Estado ou território")
    axes[1].grid(axis="x", alpha=0.25)
    save(fig, "03_testes.png")


def analyze_vaccination(vaccination):
    doses = {"first_dose_administered": "Primeira dose", "second_dose_administered": "Segunda dose"}
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.4), sharey=True, layout="constrained")
    for ax, state in zip(axes, STATES):
        state_series = vaccination.loc[vaccination["state"].eq(state)].set_index("date").asfreq("D")
        for (field, label), color in zip(doses.items(), COLORS):
            ax.plot(state_series.index, state_series[field] / 1e6, label=label, color=color)
        plot_time(ax, "Doses (milhões)" if ax is axes[0] else "", state)
    axes[0].legend(loc="upper left")
    fig.suptitle("Primeiras e segundas doses acumuladas em 2021", fontweight="bold")
    print("\nÚltimo registro com ambas as doses preenchidas")
    complete = vaccination[vaccination["state"].isin(STATES)].dropna(subset=list(doses))
    latest = complete.groupby("state").tail(1).set_index("state")
    print(latest.loc[STATES, ["date", *doses]].to_string())
    save(fig, "04_vacinacao.png")


def evaluate_model(daily):
    # Em cada data-alvo t, o boletim mais recente disponível é o de t-1.
    lag = daily.shift(1)
    features = ["variacao_ontem", "media_7_dias_anteriores"]
    data = pd.DataFrame({
        "observado": daily, features[0]: lag, features[1]: lag.rolling(7).mean(),
    }).dropna()
    train = data.loc[data.index < TEST_START]
    test = data.loc[data.index >= TEST_START].copy()
    if train.empty or test.empty:
        raise ValueError("A regressão exige observações nos períodos de treino e teste.")

    # Mínimos quadrados ordinários com uma coluna para o intercepto.
    train_matrix = np.column_stack([np.ones(len(train)), train[features]])
    coefficients = np.linalg.lstsq(train_matrix, train["observado"], rcond=None)[0]
    test["regressao"] = coefficients[0] + test[features].to_numpy() @ coefficients[1:]
    test["persistencia"] = test[features[0]]
    print(f"\nTreino: {len(train)} dias ({train.index.min():%d/%m/%Y} a {train.index.max():%d/%m/%Y})")
    print(f"Teste: {len(test)} dias ({test.index.min():%d/%m/%Y} a {test.index.max():%d/%m/%Y})")
    for prediction in ["regressao", "persistencia"]:
        error = test[prediction] - test["observado"]
        print(f"{prediction}: MAE = {error.abs().mean():.2f}, RMSE = {np.sqrt(error.pow(2).mean()):.2f}")
    test.to_csv(OUTPUT / "previsoes.csv", index_label="data_alvo", float_format="%.6f")

    fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")
    ax.plot(test.index, test["observado"] / 1000, color="#26364d", label="Observado")
    ax.plot(test.index, test["regressao"] / 1000, color="#ad4c23", label="Regressão", linestyle="--")
    plot_time(ax, "Variação diária (mil casos)", "Maharashtra · Previsões de um dia no período de teste")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.set_xlabel("Dia/mês do registro em 2021")
    ax.legend()
    save(fig, "05_previsao.png")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases, testing, vaccination = (load(name) for name in ["casos", "testes", "vacinacao"])
    daily = analyze_cases(cases)
    analyze_testing(testing)
    analyze_vaccination(vaccination)
    evaluate_model(daily["Maharashtra"])
    print(f"\nSaídas em {OUTPUT}")


if __name__ == "__main__":
    main()
