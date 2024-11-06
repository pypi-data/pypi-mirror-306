"""
Vertex Experiments
"""

from datetime import datetime
from google.cloud import aiplatform


# pylint: disable=raise-missing-from, too-many-instance-attributes, too-many-arguments


class VertexExperiment:
    """Class for logging results of experiments on Vertex Experiments.
    Parameters:
        name_experiment(str): Name of Vertex Experiments instacne.
        model_name(str): Type of evaluated model.
        metrics(dict): Dictionary with calculated metrics.
        confusion_matrix(array): Raw confusion matrix for logging.
        model_params(dict): Model hyperparams for logging.
        data_path(str): Directory for data in dvc.
        labels(array): Array of labels for confusion matrix.
    """

    def __init__(
        self,
        name_experiment,
        model_name,
        metrics,
        confusion_matrix,
        model_params,
        data_path,
        labels,
        project="sts-notebooks",
        location="europe-west4",
    ):
        self.name_experiment = name_experiment
        self.model_name = model_name.lower()
        self.metrics = metrics
        self.model_params = model_params
        self.data_path = data_path
        self.labels = labels
        self.project = project
        self.location = location
        self.confusion_matrix = confusion_matrix

    def log_confusion_matrix(self):
        """Calculate and write confusion matrix in vertex experiment."""
        aiplatform.log_classification_metrics(
            labels=self.labels.tolist(),
            matrix=self.confusion_matrix.tolist(),
            display_name="confusion-matrix",
        )

    def log_experiment_results_to_vertex(self):
        """The function saves all values (params, metrics) on Vertex experiments.
        Raises
        ------
        TypeError
        """

        try:
            aiplatform.init(
                project=self.project,
                location=self.location,
                experiment=self.name_experiment,
                experiment_tensorboard=False,
            )
            run_name = f"""{self.model_name
                            }{datetime.now().strftime("%Y%m%d%H%M%S")}"""
            aiplatform.start_run(run_name)

            extended_params = self.model_params
            extended_params["data_path"] = self.data_path

            aiplatform.log_params(extended_params)
            aiplatform.log_metrics(self.metrics)
            self.log_confusion_matrix()
            aiplatform.end_run()

        except TypeError:
            aiplatform.end_run()
            experiment_run = aiplatform.ExperimentRun(
                run_name=run_name,
                experiment=self.name_experiment,
                project=self.project,
                location=self.location,
            )
            experiment_run.delete()
            raise TypeError(f"TypeError: Change parameters. Experiment_run {run_name} was removed.")

        except:
            aiplatform.end_run()
            experiment_run = aiplatform.ExperimentRun(
                run_name=run_name,
                experiment=self.name_experiment,
                project=self.project,
                location=self.location,
            )
            experiment_run.delete()
            raise RuntimeError(f"UnspecifiedRuntimeError: Experiment_run {run_name} was removed.")
