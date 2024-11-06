"""
Model class
"""

import pandas as pd
import numpy as np

from .classifier import Classifier
from .metrics import Metrics
from .confusion_matrix import ConfusionMatrix
from .experiments import VertexExperiment
from .hyperopt import Hyperopt

# pylint: disable=attribute-defined-outside-init
# pylint: disable=raise-missing-from
# pylint: disable=invalid-name
# pylint: disable=dangerous-default-value
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-instance-attributes


class Modeling:
    """Modeling, metrics and vertex logging.
    Parameters:
        model (model Constructor, callable): Model from library to create instance as our classifier.
        X_train, X_test, y_train, y_test (pd.DataFrame, pd.DataFrame, pd.Series, pd.Series): Data for train and test model.
        is_binary_class (bool): Information if classifier is binary -> metrics calculations depend on that.
        main_metric(str): Metric to optimize by hyperopt.
        params (dict): Hyperparameters for classifier initiation.
        proba (float): For binary classification, threshold for classifing case as True.
        own_metrics(dict): Own metrics, given as 'metric_name': metric_function(y_test, y_pred).
        metrics_average(str): Average to calcualte global precision and recall from many classes (for non-binary classification).
        beta(float): Value of beta for fbeta_score. Default 2.
        fbeta_average(str): Average to calculate global fbeta_score from many classes (for non-binary classification).
        fbeta_weights(list): Weights for fbeta_score to be specified for each class (both for binary or non-binary classification).
        name_experiment(str): Name of Vertex Experiments instacne.
        data_path(str): Directory for data in dvc.
        labels(array): Array of labels for confusion matrix.
    """

    def __init__(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        is_binary_class: bool,
        main_metric: str,
        model_params: dict = None,
        proba: float = 0.5,
        own_metrics: dict = None,
        metrics_average="binary",
        beta=2,
        fbeta_average="binary",
        fbeta_weights=[0.5, 0.5],
        name_experiment: str = None,
        data_path: str = None,
        labels: list = None,
    ):

        self.classifier = Classifier(
            model, X_train, X_test, y_train, y_test, is_binary_class, model_params, proba
        )
        self.metricser = Metrics(
            self.classifier,
            main_metric=main_metric,
            metrics_average=metrics_average,
            beta=beta,
            fbeta_average=fbeta_average,
            fbeta_weights=fbeta_weights,
            own_metrics=own_metrics,
        )
        self.confusion_matrixer = ConfusionMatrix(self.classifier)
        if labels:
            self.labels = labels
        else:
            self.labels = np.sort(y_test[y_test.columns[0]].unique()).astype(str)
        self.name_experiment = name_experiment
        self.data_path = data_path
        self.project = "sts-notebooks"
        self.location = "europe-west4"
        self.log_vertex_experiments()

    def log_vertex_experiments(self):
        """Log results of model to Vertex Experiments."""
        if not self.metricser.metrics:
            self.metricser.calculate_metrics()
        vertex_experiment = VertexExperiment(
            self.name_experiment,
            self.classifier.model_name,
            self.metricser.metrics,
            self.confusion_matrixer.get_raw_confusion_matrix(),
            self.classifier.hyperparams_model(),
            self.data_path,
            self.labels,
        )
        vertex_experiment.log_experiment_results_to_vertex()
        self.get_general_metrics()

    def calculate_hyperopt_best_params(
        self, space, n_startup_jobs, hyperopt_iter, is_loss_function=False
    ):
        """Get best params for model.

        Args and return type described in Hyperopt class definition.
        """
        self.hyperopt = Hyperopt(self.classifier, self.metricser, is_loss_function=is_loss_function)
        self.hyperopt.calculate_hyperopt_best_params(space, n_startup_jobs, hyperopt_iter)

    def get_general_metrics(self):
        """Get all metrics and combined confusion_matrix."""
        print(self.metricser.get_main_metric())
        print(self.metricser.metrics)
        self.confusion_matrixer.plot_combined_confusion_matrix()
