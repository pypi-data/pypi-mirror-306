# ALSolver
![logo](https://github.com/user-attachments/assets/3c5208df-78ea-428a-beab-5193ec562189)

**ALSolver implements alternating least squares for matrix factorization to be used for building a recommender system**


## Installation

```console
pip install pyalsolver
```

## Development

ALSolver is managed by [uv](https://github.com/astral-sh/uv). So to start clone this repo and run:
```console
$ uv venv --python 3.12
$ uv sync
```

After any edits or updates, run ruff to fix any formatting or lining issues:

```console
$ uv run ruff format
$ uv run ruff check
```



## Usage
### Loading Data
```python
from pyalsolver.utils import MovieLens, download_dataset,
# This will download the dataset if it doesn't exist 
# or return its path if it exists
data_path = download_dataset('ml-32m')
print(data_path)
ml_dataset = MovieLens(
        data_path 
)
```
### Training a model
 ```python
from pyalsolver import ALSMF, ENGINE
from pyalsolver.utils import plot_rmse_history
model = ALSMF(0.2, 0.01, 0.01, k=20)
train_rmse_history, valid_rmse_history, loss_history = model.fit(
    ml_dataset.Rui_train, ml_dataset.Riu_train, ml_dataset.Rui_valid, 
    n_epochs=10, engine=ENGINE.NUMBA
)

# to plot rmse history

plot_rmse_history(20, train_rmse_history, valid_rmse_history)
```

### Recommending Movies to an already existing user

```python
uid = 10
pred_ratings, pred_item_indices = model.recommend(uid, topk=30)
pred_item_ids = [ml_dataset.idx_to_item_id[i] for i in pred_item_indices]
pred_item_titles = [ml_dataset.item_id_to_title[i] for i in pred_item_ids]
print(pred_ratings)
print(pred_item_titles)
```

### Coldstart a user with a single rating

```python
import numpy as np
pred_ratings, pred_item_indices = model.coldstart(
    np.array([5]), 
    np.array([628]), 
    topk=40,
    min_popularity=50  # Only consider items with at least 50 ratings
)
pred_item_ids = [ml_dataset.idx_to_item_id[i] for i in pred_item_indices]
pred_item_titles = [ml_dataset.item_id_to_title[i] for i in pred_item_ids]
print(pred_ratings)
print(pred_item_titles)
```

The packages provide three engines for computation:
1. `ENGINE.NUMPY`: uses NumPy and is recommended for small datasets
2. `ENGINE_NUMBA`: uses jitted numba code with not python objects and is recommended for large datasets.
3. `ENGINE_PARALLEL`: uses Python process parallelization for spinning up multiple processes that work to update different portions of the latent. It is only recommended if the overhead of spinning up a new process doesn't exceed the time of computing one iteration

