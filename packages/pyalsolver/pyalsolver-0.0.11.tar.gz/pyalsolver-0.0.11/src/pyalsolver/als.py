import numpy as np
import concurrent.futures
from functools import partial
from numba import njit
from enum import Enum, auto


class ENGINE(Enum):
    NUMPY = auto()
    NUMBA = auto()
    PARALLEL = auto()


class ALSMF:
    def __init__(
        self,
        lmbda=0.1,
        tau=1,
        gamma=0.1,
        k=20,
    ):
        self.lmbda = lmbda  # U & V reg
        self.tau = tau  # rmse error
        self.gamma = gamma
        self.k = k

    def fit(
        self,
        Rui_train,
        Riu_train,
        Rui_valid,
        n_epochs=20,
        engine=ENGINE.NUMBA,
        verbose=False,
    ):
        lmbda = self.lmbda
        tau = self.tau
        gamma = self.gamma

        k = self.k
        m, n = Rui_train.shape
        self.reg = (lmbda, tau, gamma)

        U = np.random.normal(0, np.sqrt(1 / k), (m, k))
        V = np.random.normal(0, np.sqrt(1 / k), (n, k))
        b_U = np.zeros(m)
        b_V = np.zeros(n)
        V[:, 0] = Rui_train.mat.mean(axis=0)  # Avg. rating for each movie

        train_rmse_history = []
        valid_rmse_history = []
        loss_history = []
        # Repeat until convergence
        for epoch in range(n_epochs):
            # Fix V and estimate U
            reg = (lmbda, tau, gamma)

            if engine is ENGINE.PARALLEL:
                U = _update_latent_parallel(Rui_train, V, b_U, b_V, reg)
                V = _update_latent_parallel(
                    Riu_train,
                    U,
                    b_V,
                    b_U,
                    reg,
                )
                b_U = _update_bias_parallel(Rui_train, U, V, b_V, reg)
                b_V = _update_bias_parallel(Riu_train, V, U, b_U, reg)

            elif engine is ENGINE.NUMBA:
                U = _update_latent_numba(
                    Rui_train.mat.data,
                    Rui_train.mat.indptr,
                    Rui_train.mat.indices,
                    V,
                    b_U,
                    b_V,
                    reg,
                )
                V = _update_latent_numba(
                    Riu_train.mat.data,
                    Riu_train.mat.indptr,
                    Riu_train.mat.indices,
                    U,
                    b_V,
                    b_U,
                    reg,
                )
                b_U = _update_bias_numba(
                    Rui_train.mat.data,
                    Rui_train.mat.indptr,
                    Rui_train.mat.indices,
                    U,
                    V,
                    b_V,
                    reg,
                )
                b_V = _update_bias_numba(
                    Riu_train.mat.data,
                    Riu_train.mat.indptr,
                    Riu_train.mat.indices,
                    V,
                    U,
                    b_U,
                    reg,
                )
            else:
                U = _update_latent(Rui_train, V, b_U, b_V, reg, 0, U.shape[0])
                V = _update_latent(Riu_train, U, b_V, b_U, reg, 0, V.shape[0])
                b_U = _update_bias(Rui_train, U, V, b_V, reg, 0, U.shape[0])
                b_V = _update_bias(Riu_train, V, U, b_U, reg, 0, V.shape[0])

            loss = criterion(Rui_train, U, V, b_U, b_V, reg)
            train_rmse = rmse(Rui_train, U, V, b_U, b_V)
            valid_rmse = rmse(Rui_valid, U, V, b_U, b_V)
            train_rmse_history.append(train_rmse)
            valid_rmse_history.append(valid_rmse)
            loss_history.append(loss)
            if verbose:
                print(
                    f"[Epoch {epoch+1}/{n_epochs}] loss: {loss} train RMSE: {train_rmse}, valid RMSE: {valid_rmse}"
                )
        if verbose:
            print("Algorithm converged")

        self.Rui_train = Rui_train
        self.U = U
        self.V = V
        self.b_U = b_U
        self.b_V = b_V

        # Adjusted
        self.item_popularity = np.array(Riu_train.mat.sum(axis=1)).flatten()
        self.item_rating_counts = np.array(Riu_train.mat.getnnz(axis=1)).flatten()
        self.global_mean = Rui_train.mat.mean()

        self.user_rating_counts = np.array(Rui_train.mat.getnnz(axis=1)).flatten()

        return train_rmse_history, valid_rmse_history, loss_history

    def recommend(self, user_id, topk=20, min_popularity=10, include_rated=False):
        """
        Enhanced recommendation function with popularity-aware scoring and filtering

        Parameters:
        -----------
        user_id : int
            ID of the user to make recommendations for
        topk : int
            Number of recommendations to return
        min_popularity : int
            Minimum number of ratings for an item to be recommended
        include_rated : bool
            Whether to include items the user has already rated

        Returns:
        --------
        tuple : (scores, item_ids)
            Tuple containing arrays of scores and corresponding item IDs
        """
        # Calculate base recommendation scores
        base_scores = self.U[user_id] @ self.V.T + 0.05 * self.b_V

        # Create a mask for items that meet the minimum popularity threshold
        popular_items_mask = self.item_rating_counts >= min_popularity

        # Create a mask for items not rated by the user (if exclude_rated is True)
        if not include_rated:
            # Get indices of items rated by this user
            rated_items_mask = np.zeros(len(base_scores), dtype=bool)
            rated_indices = self.Rui_train.getrow(user_id)[1]
            rated_items_mask[rated_indices] = True

            # Combine popularity and unrated items masks
            valid_items_mask = popular_items_mask & ~rated_items_mask
        else:
            valid_items_mask = popular_items_mask

        # Apply the mask to scores
        adjusted_scores = base_scores.copy()
        adjusted_scores[~valid_items_mask] = float("-inf")

        # Get top-k items
        reco_item_ids = (-adjusted_scores).argsort()[:topk]
        return adjusted_scores[reco_item_ids], reco_item_ids

    def coldstart(self, ratings, item_ids, topk=20, min_popularity=10):
        """
        Enhanced cold-start recommendation with popularity-aware scoring

        Parameters:
        -----------
        ratings : np.array
            User's ratings for known items
        item_ids : np.array
            IDs of items rated by the user
        topk : int
            Number of recommendations to return
        min_popularity : int
            Minimum number of ratings for an item to be recommended
        """
        k = self.V.shape[1]
        u, b_u = np.random.normal(0, np.sqrt(1 / k), self.U.shape[1]), np.zeros(1)
        lmbda, tau, gamma = self.reg
        I = np.eye(k)

        # Learn user preferences
        for n_iter in range(7):
            # Update user latent factors
            V_user = self.V[item_ids, :]
            A = tau * np.dot(V_user.T, V_user) + lmbda * I
            b = tau * np.dot(ratings - b_u - self.b_V[item_ids], V_user)
            u = np.linalg.solve(A, b)

            # Update user bias
            nui = ratings.shape[0]
            A = ratings - u @ self.V[item_ids, :].T - self.b_V[item_ids]
            b_u = tau * np.sum(A) / (tau * nui + gamma)

        # Calculate base scores
        base_scores = u @ self.V.T + 0.05 * self.b_V

        # Get top-k items
        adjusted_scores = base_scores
        popular_items_mask = self.item_rating_counts >= min_popularity
        adjusted_scores[~popular_items_mask] = float("-inf")

        reco_item_ids = (-adjusted_scores).argsort()[:topk]
        return adjusted_scores[reco_item_ids], reco_item_ids


def get_starts_ends(total_updates, num_workers):
    step = total_updates // num_workers
    starts = [s for s in range(0, total_updates - step, step)]
    ends = [s for s in range(step, total_updates, step)]
    ends[-1] += total_updates - (num_workers * step)

    return starts, ends


def _update_latent_parallel(Rui_train, V, b_U, b_V, reg):
    # calculate the start and end for each process

    starts, ends = get_starts_ends(Rui_train.shape[0], 6)
    U_ = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        update = partial(_update_latent, Rui_train, V, b_U, b_V, reg)
        results = executor.map(update, starts, ends)
        for result in results:
            U_.append(result)
    U = np.vstack(U_)
    return U


def _update_bias_parallel(Rui_train, U, V, b_V, reg):
    starts, ends = get_starts_ends(Rui_train.shape[0], 6)
    b_U_ = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        update = partial(_update_bias, Rui_train, U, V, b_V, reg)
        results = executor.map(update, starts, ends)
        for result in results:
            b_U_.append(result)
    b_U = np.concatenate(b_U_)
    return b_U


def _update_latent(Rui_train, V, b_U, b_V, reg, start_user, end_user):
    lmbda, tau, gamma = reg
    I = np.eye(V.shape[1])
    U_ = []
    for user in range(start_user, end_user):
        row = Rui_train.mat.getrow(user)
        nui = max(1, row.nnz)  # Number of items user i has rated

        # Least squares solution

        # Added Lines
        # -------------------------------------------------------------------

        # Select subset of V associated with movies reviewed by user u
        V_user = V[row.indices, :]
        # Select subset of row R_i associated with movies reviewed by user i
        A = tau * np.dot(V_user.T, V_user) + lmbda * nui * I  # *
        b = tau * np.dot(row.data - b_U[user] - b_V[row.indices], V_user)  #### MOD
        # b = tau * np.dot(row.data, V_user)
        # -------------------------------------------------------------------
        # U[:, user] = np.linalg.solve(A, b)
        U_.append(np.linalg.solve(A, b))
    return np.vstack(U_)


def _update_bias(Rui_train, U, V, b_V, reg, start_user, end_user):
    lmbda, tau, gamma = reg
    b_U_ = []
    for user in range(start_user, end_user):
        row = Rui_train.mat.getrow(user)
        nui = row.nnz

        A = row.data - U[user, :] @ V[row.indices, :].T - b_V[row.indices]
        # b_U[user] = tau * np.sum(A) / (tau * nui + gamma)
        b_U_.append(tau * np.sum(A) / (tau * nui + gamma))
    return np.stack(b_U_)


def rmse(R, U, V, b_U, b_V):
    ratings = R.ratings
    user_ids, item_ids = np.array(R.user_ids), np.array(R.item_ids)
    mse = 0.0
    for i in range(ratings.shape[0]):
        user, item = user_ids[i], item_ids[i]
        mse += (ratings[i] - np.dot(U[user], V[item]) - b_U[user] - b_V[item]) ** 2
    return np.sqrt(mse / ratings.shape[0])


def criterion(R, U, V, b_U, b_V, reg):
    lmbda, tau, gamma = reg
    ratings = R.ratings
    user_ids, item_ids = np.array(R.user_ids), np.array(R.item_ids)
    mse = 0.0
    for i in range(ratings.shape[0]):
        user, item = user_ids[i], item_ids[i]
        mse += (ratings[i] - np.dot(U[user], V[item]) - b_U[user] - b_V[item]) ** 2
    return (
        tau / (2 * ratings.shape[0]) * mse
        + lmbda / 2 * (np.sum(U * U) / U.shape[0])
        + lmbda / 2 * (np.sum(V * V) / V.shape[0])
        + gamma / 2 * (np.sum(b_U * b_U) / U.shape[0])
        + gamma / 2 * (np.sum(b_V * b_V) / V.shape[0])
    )


@njit(cache=True)
def _update_latent_numba(data, indptr, indices, V, b_U, b_V, reg):
    lmbda, tau, gamma = reg
    num_factors = V.shape[1]
    U_ = np.zeros((b_U.shape[0], num_factors))
    I = np.eye(num_factors)  # Identity matrix for regularization

    for user_idx in range(b_U.shape[0]):
        start, end = indptr[user_idx], indptr[user_idx + 1]
        ratings = data[start:end]
        items = indices[start:end]
        # https://link.springer.com/chapter/10.1007/978-3-540-68880-8_32
        # Popular itme Regularization to be added later
        # nui = max(1, end - start)  # Number of items rated by the user

        V_user = V[items, :]  # Get item factors for items rated by the user

        # Compute A and b for the linear system A * U = b
        A = (
            tau * np.dot(V_user.T, V_user) + lmbda * I
        )  # * nui (To be added as a feature)
        b = tau * np.dot(ratings - b_U[user_idx] - b_V[items], V_user)

        # Solve for the latent factors for this user
        U_[user_idx, :] = np.linalg.solve(A, b)

    return U_


@njit(cache=True)
def _update_bias_numba(data, indptr, indices, U, V, b_V, reg):
    lmbda, tau, gamma = reg
    b_U_ = np.zeros(U.shape[0])
    for user_idx in range(U.shape[0]):
        start, end = indptr[user_idx], indptr[user_idx + 1]
        ratings = data[start:end]
        items = indices[start:end]
        nui = end - start

        A = ratings - U[user_idx, :] @ V[items, :].T - b_V[items]
        b_U_[user_idx] = tau * np.sum(A) / (tau * nui + gamma)
    return b_U_
