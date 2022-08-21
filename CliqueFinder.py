import networkx
import pandas as pd
import numpy as np
from typing import Callable, List, Union


class CliqueFinder:
    def __init__(self,
                 corr_matrix: pd.DataFrame,
                 features_data: pd.DataFrame,
                 target_data: pd.Series
                 ) -> None:
        self.corr_matrix = corr_matrix
        self.features_data: pd.DataFrame = features_data
        self.target_data: pd.Series = target_data
        self.features: set = set(self.corr_matrix.columns)
        self.best_feature_set: set = set()
        self.cliques: List = list()

    def calculate_best_feature_set(self, feature_target_corr_func: Callable[[Union[pd.Series, np.array],
                                                                             Union[pd.Series, np.array]], Union[
                                                                                float, int]]) -> None:
        if len(self.cliques) == 0:
            raise Exception("No cliques. First you have to launch calculate_independent_cliques() "
                            "to calculate all possible cliques")
        max_value: float = 0
        target_feature_dependency_value = {}
        for feature in self.features:
            dependency_value = abs(feature_target_corr_func(self.features_data[feature], self.target_data))
            target_feature_dependency_value[feature] = dependency_value

        for clique in self.cliques:
            curr_value: float = 0
            for feature in clique:
                curr_value += target_feature_dependency_value[feature]
            if curr_value > max_value:
                max_value = curr_value
                self.best_feature_set = set(clique)

    def calculate_cliques(self, threshold: float) -> None:
        graph = self.corr_matrix.applymap(lambda x: 0 if (np.abs(x) > threshold) else 1)
        for i in range(len(graph)):  # all elements are connected to themselves
            graph.iloc[i, i] = 1
        connection_graph = networkx.Graph(graph)
        self.cliques = list(networkx.find_cliques(connection_graph))

    def fit(self, feature_target_corr_func: Callable[[Union[pd.Series, np.array],
                                                      Union[pd.Series, np.array]], Union[
                                                         float, int]],
            threshold: float = 0.8) -> None:
        self.calculate_cliques(threshold)
        self.calculate_best_feature_set(feature_target_corr_func)

    def get_best_clique(self) -> List[str]:
        return list(self.best_feature_set)

    def get_out_of_clique_features(self) -> List[str]:
        return list(self.features - self.best_feature_set)
