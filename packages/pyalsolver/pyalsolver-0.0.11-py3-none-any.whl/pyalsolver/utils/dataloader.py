import pandas as pd
import scipy
from sklearn.model_selection import train_test_split
import requests
import zipfile
import io
import pathlib
import os


class CSR:
    def __init__(self, ratings, user_ids, item_ids, shape):
        self.mat = scipy.sparse.csr_matrix((ratings, (user_ids, item_ids)), shape=shape)
        self.ratings = ratings
        self.user_ids = user_ids
        self.item_ids = item_ids
        self.shape = shape


class MovieLens:
    def __init__(self, data_path, verbose=True):
        # './dataset/ml-100k/u.data'
        dataset_name = os.path.basename(os.path.dirname(data_path))
        if dataset_name == "ml-100k":
            header = ["user_id", "item_id", "rating", "timestamp"]
            df = pd.read_csv(os.path.join(data_path, "u.data"), sep="\t", names=header)

            df_movies = pd.read_csv(
                "./datasets/ml-100k/u.item",
                usecols=[0, 1],
                sep="|",
                names=["item_id", "title"],
                encoding="latin-1",
            )
        elif dataset_name == "ml-25m" or dataset_name == "ml-32m":
            df = pd.read_csv(os.path.join(data_path, "ratings.csv"))

            df.rename(columns={"userId": "user_id", "movieId": "item_id"}, inplace=True)

            df_movies = pd.read_csv(os.path.join(data_path, "movies.csv"))

            self.item_id_to_genre = {
                id: df_movies.genres[i].split("|")[0]
                for i, id in enumerate(df_movies.movieId.to_numpy())
            }
            self.item_id_to_title = {
                id: df_movies.title[i]
                for i, id in enumerate(df_movies.movieId.to_numpy())
            }

        n_users = df.user_id.unique().shape[0]
        n_items = df.item_id.unique().shape[0]
        self.n_users, self.n_items = n_users, n_items
        if verbose:
            print(
                "Number of users = "
                + str(n_users)
                + " | Number of movies = "
                + str(n_items)
            )

        user_id_to_idx = {}
        idx_to_user_id = []
        for i, user_id in enumerate(df["user_id"].unique()):
            user_id_to_idx[user_id] = i
            idx_to_user_id.append(user_id)

        self.user_id_to_idx, self.idx_to_user_id = user_id_to_idx, idx_to_user_id

        item_id_to_idx = {}
        idx_to_item_id = []
        for i, movie_id in enumerate(df["item_id"].unique()):
            item_id_to_idx[movie_id] = i
            idx_to_item_id.append(movie_id)

        self.item_id_to_idx, self.idx_to_item_id = item_id_to_idx, idx_to_item_id

        df_train, df_test = train_test_split(df, test_size=0.2)
        df_test, df_valid = train_test_split(df_test, test_size=0.5)
        if verbose:
            print(
                f"Train: {len(df_train)}, Valid: {len(df_valid)}, Test: {len(df_test)}"
            )

        # train
        user_ids_train = [
            user_id_to_idx[userId] for userId in df_train["user_id"].to_numpy()
        ]
        item_ids_train = [
            item_id_to_idx[item_id] for item_id in df_train["item_id"].to_numpy()
        ]
        ratings_train = df_train["rating"].to_numpy()
        ### Valid
        user_ids_valid = [
            user_id_to_idx[userId] for userId in df_valid["user_id"].to_numpy()
        ]
        item_ids_valid = [
            item_id_to_idx[item_id] for item_id in df_valid["item_id"].to_numpy()
        ]
        ratings_valid = df_valid["rating"].to_numpy()
        ### Test
        user_ids_test = [
            user_id_to_idx[userId] for userId in df_test["user_id"].to_numpy()
        ]
        item_ids_test = [
            item_id_to_idx[item_id] for item_id in df_test["item_id"].to_numpy()
        ]
        ratings_test = df_test["rating"].to_numpy()

        self.Rui_train = CSR(
            ratings_train, user_ids_train, item_ids_train, (n_users, n_items)
        )
        self.Riu_train = CSR(
            ratings_train, item_ids_train, user_ids_train, (n_items, n_users)
        )

        self.Rui_valid = CSR(
            ratings_valid, user_ids_valid, item_ids_valid, (n_users, n_items)
        )
        self.Riu_valid = CSR(
            ratings_valid, item_ids_valid, user_ids_valid, (n_items, n_users)
        )

        self.Rui_test = CSR(
            ratings_test, user_ids_test, item_ids_test, (n_users, n_items)
        )


def download_dataset(dataset_name):
    dataset_name_to_url = {
        # "ml-1m": "https://files.grouplens.org/datasets/movielens/ml-1m.zip",
        "ml-100k": "https://files.grouplens.org/datasets/movielens/ml-100k.zip",
        "ml-25m": "https://files.grouplens.org/datasets/movielens/ml-25m.zip",
        "ml-32m": "https://files.grouplens.org/datasets/movielens/ml-32m.zip",
    }

    assert (
        dataset_name in dataset_name_to_url
    ), f"{dataset_name} is not one of {list(dataset_name_to_url.keys())}"

    #
    if pathlib.Path(f"./datasets/{dataset_name}/").exists():
        print(f"{dataset_name} already downloaded")
        return f"./datasets/{dataset_name}/"

    # create datasets directory if it doesn't exist
    path = pathlib.Path("./datasets")
    path.mkdir(parents=True, exist_ok=True)

    url = dataset_name_to_url[dataset_name]

    # Step 1: Download the zip file
    print(f"Downloading {dataset_name}....")
    response = requests.get(url, stream=True, timeout=10)
    if response.status_code == 200:
        # Step 2: Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("./datasets/")  # Specify where to extract files
        print(f"{dataset_name} downloaded and extracted in ./datasets/{dataset_name}/")
    else:
        print("Failed to download the file.")
        return

    return f"./datasets/{dataset_name}/"
