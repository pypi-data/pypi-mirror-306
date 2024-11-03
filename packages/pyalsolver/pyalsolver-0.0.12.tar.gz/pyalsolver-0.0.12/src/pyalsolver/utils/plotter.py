import matplotlib.pyplot as plt


def plot_rmse_history(n_epochs, train_rmse_history, valid_rmse_history):
    plt.plot(range(n_epochs), train_rmse_history, marker="o", label="Training RMSE")
    plt.plot(range(n_epochs), valid_rmse_history, marker="v", label="Valid RMSE")
    plt.title("ALS-WR Learning Curve")
    plt.xlabel("Number of Epochs")
    plt.ylabel("RMSE")
    plt.legend()
    plt.grid()
    plt.show()
