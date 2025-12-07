import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def plot_grouped_metrics() -> None:
    """
    Plots grouped bar chart of Brier score and log loss for moneyline based predictions by league.
    Normalizes Brier scores and log loss using [0,1] scale.

    Args:
        None
    
    Returns:
        None
    """

    leagues = ["MLB", "NFL", "NBA", "NHL"]

    brier_scores = []
    log_losses = []

    for league in leagues:

        df = pd.read_csv(f"processed_data/{league.lower()}.csv")

        # only second-half games
        df = df[df["second_half"] == 1].copy()

        # compute Brier score
        brier = float(((df["ml_prob"] - df["result"]) ** 2).mean())
        brier_scores.append(brier)

        # compute log loss
        preds = df["ml_prob"].astype(float).clip(1e-15, 1 - 1e-15)
        y = df["result"]
        log_loss = float(-(y * np.log(preds) + (1 - y) * np.log(1 - preds)).mean())
        log_losses.append(log_loss)


    # normalize both metrics to [0, 1] using min-max
    def minmax(arr):
        arr = np.array(arr)
        return (arr - arr.min()) / (arr.max() - arr.min())

    brier_norm = minmax(brier_scores)
    log_norm = minmax(log_losses)


    # plot
    brier_colors = ["darkred", "darkgreen", "darkorange", "darkblue"]
    logloss_colors = ["lightcoral", "lightgreen", "navajowhite", "lightskyblue"]
    x = np.arange(len(leagues))
    width = 0.35

    plt.figure(figsize=(10, 6))

    for i in range(len(leagues)):
        # brier bar
        plt.bar(
            x[i] - width/2,
            brier_norm[i],
            width,
            label="Brier (normalized)" if i == 0 else "",
            color=brier_colors[i]
        )

        # log loss bar
        plt.bar(
            x[i] + width/2,
            log_norm[i],
            width,
            label="Log Loss (normalized)" if i == 0 else "",
            color=logloss_colors[i]
        )

    plt.xticks(x, leagues, fontsize=12)
    plt.ylabel("Normalized Score", fontsize=14)
    plt.title("Moneyline Brier Score vs Log Loss by League", fontsize=16)
    plt.legend(loc="lower right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("figures/brier_vs_log.png")
    plt.close()



if __name__ == "__main__":
    plot_grouped_metrics()