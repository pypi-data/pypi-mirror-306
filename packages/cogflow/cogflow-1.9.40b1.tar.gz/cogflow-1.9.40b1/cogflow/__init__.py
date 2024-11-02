"""
Cogflow module sets up a pipeline for handling datasets and machine learning models
using multiple plugins. It includes functions for creating, registering, evaluating,
and serving models, as well as managing datasets.

Key components include:

Mlflow Plugin: For model tracking, logging, and evaluation.
Kubeflow Plugin: For pipeline management and serving models.
Dataset Plugin: For dataset registration and management.
Model Plugin: For saving model details.
Configurations: Constants for configuration like tracking URIs, database credentials, etc.

Key Functions:

Model Management:

register_model: Register a new model.
log_model: Log a model.
load_model: Load a model.
delete_registered_model: Delete a registered model.
create_registered_model: Create a new registered model.
create_model_version: Create a new version of a registered model.


Run Management

start_run: Start a new.
end_run: End the current.
log_param: Log a parameter to the current run.
log_metric: Log a metric to the current run.

Evaluation and Autologging

evaluate: Evaluate a model.
autolog: Enable automatic logging of parameters, metrics, and models.

Search and Query

search_registered_models: Search for registered models.
search_model_versions: Search for model versions.
get_model_latest_version: Get the latest version of a registered model.
get_artifact_uri: Get the artifact URI of the current or specified run.

Dataset Management

link_model_to_dataset: Link a model to a dataset.
save_dataset_details: Save dataset details.
save_model_details_to_db: Save model details to the database.

Pipeline and Component Management

pipeline: Create a new Kubeflow pipeline.
create_component_from_func: Create a Kubeflow component from a function.
client: Get the Kubeflow client.
load_component_from_url: Load a Kubeflow component from a URL.

Model Serving

serve_model_v1: Serve a model using Kubeflow V1.
serve_model_v2: Serve a model using Kubeflow V2.
get_model_url: Get the URL of a served model.
delete_served_model: Delete a served model.

MinIO Operations

create_minio_client: Create a MinIO client.
query_endpoint_and_download_file: Query an endpoint and download a file from MinIO.
save_to_minio: Save file content to MinIO.
delete_from_minio: Delete an object from MinIO.

Dataset Registration

register_dataset: Register a dataset.
"""

import json
import os
import time
from typing import Union, Any, List, Optional, Dict, Mapping
import random
import string
import numpy as np
import pandas as pd
import requests
from kfp_server_api import ApiException
from mlflow.models import ModelSignature, ModelInputExample
from scipy.sparse import csr_matrix, csc_matrix
from kfp.components import InputPath, OutputPath
from kfp.dsl import ParallelFor
from .v2 import *
from . import pluginmanager, plugin_config
from .plugin_config import (
    TRACKING_URI,
    TIMER_IN_SEC,
    ML_TOOL,
    ACCESS_KEY_ID,
    SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    ML_DB_USERNAME,
    ML_DB_PASSWORD,
    ML_DB_HOST,
    ML_DB_PORT,
    ML_DB_NAME,
    COGFLOW_DB_USERNAME,
    COGFLOW_DB_PASSWORD,
    COGFLOW_DB_HOST,
    COGFLOW_DB_PORT,
    COGFLOW_DB_NAME,
    MINIO_ENDPOINT_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_ACCESS_KEY,
    API_BASEPATH,
)
from .plugins.dataset_plugin import DatasetMetadata, DatasetPlugin
from .plugins.kubeflowplugin import CogContainer, KubeflowPlugin
from .plugins.mlflowplugin import MlflowPlugin
from .plugins.notebook_plugin import NotebookPlugin
from .pluginmanager import PluginManager
from .util import make_post_request, is_valid_s3_uri


pyfunc = MlflowPlugin().pyfunc
mlflow = MlflowPlugin().mlflow
sklearn = MlflowPlugin().sklearn
cogclient = MlflowPlugin().cogclient
tensorflow = MlflowPlugin().tensorflow
pytorch = MlflowPlugin().pytorch
models = MlflowPlugin().models
lightgbm = MlflowPlugin().lightgbm
xgboost = MlflowPlugin().xgboost

add_model_access = CogContainer().add_model_access
kfp = KubeflowPlugin().kfp


def create_minio_client():
    """
    Creates a MinIO client object.

    Returns:
        Minio: The MinIO client object.
    """
    return DatasetPlugin().create_minio_client()


def query_endpoint_and_download_file(url, output_file, bucket_name):
    """
    Queries an endpoint and downloads a file from MinIO.

    Args:
        url (str): The URL to query.
        output_file (str): The output file path.
        bucket_name (str): The MinIO bucket name.

    Returns:
        bool: True if the file was successfully downloaded, False otherwise.
    """
    return DatasetPlugin().query_endpoint_and_download_file(
        url=url, output_file=output_file, bucket_name=bucket_name
    )


def save_to_minio(file_content, output_file, bucket_name):
    """
    Saves file content to MinIO.

    Args:
        file_content (bytes): The content of the file to save.
        output_file (str): The output file path.
        bucket_name (str): The MinIO bucket name.

    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    return DatasetPlugin().save_to_minio(
        file_content=file_content, output_file=output_file, bucket_name=bucket_name
    )


def delete_from_minio(object_name, bucket_name):
    """
    Deletes an object from MinIO.

    Args:
        object_name (str): The name of the object to delete.
        bucket_name (str): The MinIO bucket name.

    Returns:
        bool: True if the object was successfully deleted, False otherwise.
    """
    return DatasetPlugin().delete_from_minio(
        object_name=object_name, bucket_name=bucket_name
    )


def register_dataset(details: DatasetMetadata):
    """
    Registers a dataset with the given details.

    Args:
        details (DatasetMetadata): The details of the dataset to register.

    Returns:
        bool: True if the dataset was successfully registered, False otherwise.
    """
    return DatasetPlugin().register_dataset(details=details)


def get_dataset(name: str):
    """
    get a dataset with the given name.
    """
    return DatasetPlugin().get_dataset(name=name)


def delete_registered_model(model_name):
    """
    Deletes a registered model.

    Args:
        model_name (str): The name of the model to delete.

    Returns:
        bool: True if the model was successfully deleted, False otherwise.
    """
    return MlflowPlugin().delete_registered_model(model_name=model_name)


def evaluate(
    data,
    *,
    model_name: str,
    model_uri: str,
    targets,
    model_type: str,
    dataset_path=None,
    feature_names: list = None,
    evaluators=None,
    evaluator_config=None,
    custom_metrics=None,
    custom_artifacts=None,
    validation_thresholds=None,
    baseline_model=None,
    env_manager="local",
):
    """
    Evaluates a model.

    Args:
        model_name: The name of model to evaluate.
        model_uri (str): The URI of the model.
        data: The data to evaluate the model on.
        model_type: The type of the model.
        targets: The targets of the model.
        dataset_path: The path to the dataset.
        feature_names: The names of the features.
        evaluators: The evaluators to use.
        evaluator_config: The configuration for the evaluator.
        custom_metrics: Custom metrics to use.
        custom_artifacts: Custom artifacts to use.
        validation_thresholds: Validation thresholds to use.
        baseline_model: The baseline model to compare against.
        env_manager: The environment manager to use.

    Returns:
        dict: The evaluation results.
    """
    result = MlflowPlugin().evaluate(
        model=model_uri,
        data=data,
        model_type=model_type,
        targets=targets,
        dataset_path=dataset_path,
        feature_names=feature_names,
        evaluators=evaluators,
        evaluator_config=evaluator_config,
        custom_metrics=custom_metrics,
        custom_artifacts=custom_artifacts,
        validation_thresholds=validation_thresholds,
        baseline_model=baseline_model,
        env_manager=env_manager,
    )

    PluginManager().load_config()
    # Construct URLs
    url_metrics = os.getenv(plugin_config.API_BASEPATH) + "/validation/metrics"
    url_artifacts = os.getenv(plugin_config.API_BASEPATH) + "/validation/artifact"

    # Attempt to make POST requests, continue regardless of success or failure
    try:
        metrics = result.metrics
        metrics.update({"model_name": model_name})
        make_post_request(url_metrics, data=metrics)
    except Exception as exp:
        print(f"Failed to post metrics: {exp}")

    serialized_artifacts = NotebookPlugin().serialize_artifacts(result.artifacts)

    # Update artifacts with model name
    serialized_artifacts.update({"model_name": model_name})

    # Now you can use serialized_artifacts in your HTTP request
    try:
        make_post_request(url_artifacts, data=serialized_artifacts)
    except Exception as exp:
        print(f"Failed to post artifacts: {exp}")

    return result


def search_registered_models(
    filter_string: Optional[str] = None,
    max_results: int = 100,
    order_by: Optional[List[str]] = None,
    page_token: Optional[str] = None,
):
    """
    Searches for registered models.

    This method allows you to search for registered models using optional filtering criteria,
    and retrieve a list of registered models that match the specified criteria.

    Args:
        filter_string (Optional[str]): A string used to filter the registered models. The filter
                string can include conditions on model name, tags and other attributes. For example,
                "name='my_model' AND tags.key='value'". If not provided, all registered
                models are returned.
        max_results (int): The maximum number of results to return. Defaults to 100.
        order_by (Optional[List[str]]): A list of property keys to order the results by.
            For example, ["name ASC", "version DESC"].
        page_token (Optional[str]): A token to specify the page of results to retrieve. This is
            useful for pagination when there are more results than can be returned in a single call.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a registered model that
        matches the search criteria. Each dictionary contains details about the registered model,
        such as its name, creation timestamp, last updated timestamp, tags, and description.
    """
    return MlflowPlugin().search_registered_models(
        filter_string=filter_string,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )


def load_model(model_uri: str, dst_path=None):
    """
    Loads a model from the specified URI.

    Args:
        model_uri (str): The URI of the model to load.
        dst_path (str, optional): The destination path to load the model to.

    Returns:
        Any: The loaded model object.
    """
    return MlflowPlugin().load_model(model_uri=model_uri, dst_path=dst_path)


def register_model(
    model_uri: str,
    model: str,
    await_registration_for: int = 300,
    *,
    tags: Optional[Dict[str, Any]] = None,
):
    """
    Registers the given model with Mlflow.

    This method registers a model with Mlflow using the specified model URI. Optionally,
    tags can be added to the registered model for better organization and metadata tracking.

    Args:
        model_uri (str): The URI of the Mlflow model to register.
        model (str): The name under which to register the model in the Mlflow Model Registry.
        await_registration_for (int, optional): The duration, in seconds, to wait for the model
        version to finish being created and be in the READY status. Defaults to 300 seconds.
        tags (Optional[Dict[str, Any]], optional): A dictionary of key-value pairs to tag the
        registered model with. Tags can be useful for organizing and filtering models in the
         registry.

    Returns:
        ModelVersion: An instance of `ModelVersion` representing the registered model version.
    """
    return MlflowPlugin().register_model(
        model=model,
        model_uri=model_uri,
        await_registration_for=await_registration_for,
        tags=tags,
    )


def autolog():
    """
    Enables automatic logging of parameters, metrics, and models.
    """
    return MlflowPlugin().autolog()


def create_registered_model(
    model: str, tags: Optional[Dict[str, Any]] = None, description: Optional[str] = None
):
    """
    Create a registered model in the Mlflow Model Registry.

    This method creates a new registered model in the Mlflow Model Registry with the given name.
    Optionally, tags and a description can be added to provide additional metadata about the model.

    Args:
        model (str): The name of the registered model.
        tags (Optional[Dict[str, Any]], optional): A dictionary of key-value pairs to tag
        the registered model with. Tags can be useful for organizing and filtering models in the
        registry.
        description (Optional[str], optional): A description of the registered model. This can
        provide additional context about the model's purpose, usage, or any other relevant
        information.

    Returns:
        RegisteredModel: An instance of `RegisteredModel` representing the created registered model.
    """
    return MlflowPlugin().create_registered_model(
        model=model, tags=tags, description=description
    )


def create_model_version(
    model: str,
    source: str,
    run_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None,
    run_link: Optional[str] = None,
    description: Optional[str] = None,
    await_creation_for: int = 300,
):
    """
    Create a model version for a registered model in the Mlflow Model Registry.

    This method registers a new version of an existing registered model with the given
    source path or URI.
    Optionally, additional metadata such as run ID, tags, run link, and description can be provided.
    The `await_creation_for` parameter allows specifying a timeout for waiting for the model version
    creation to complete.

    Args:
        model (str): The name of the registered model.
        source (str): The source path or URI of the model. This is the location where the model
        artifacts are stored.
        run_id (Optional[str], optional): The ID of the run associated with this model version.
            This can be useful for tracking the lineage of the model version.
        tags (Optional[Dict[str, Any]], optional): A dictionary of key-value pairs to tag the
        model version with. Tags can help in organizing and filtering model versions.
        run_link (Optional[str], optional): A URI link to the run. This can provide quick access to
        the run details.
        description (Optional[str], optional): A description of the model version. This can provide
        additional context
            about the changes or improvements in this version.
        await_creation_for (int, optional): The time in seconds to wait for the model version
        creation to complete.
            Defaults to 300 seconds.

    Returns:
        ModelVersion: An instance of `ModelVersion` representing the created model version.
    """
    return MlflowPlugin().create_model_version(
        model=model,
        source=source,
        run_id=run_id,
        tags=tags,
        run_link=run_link,
        description=description,
        await_creation_for=await_creation_for,
    )


def set_tracking_uri(tracking_uri):
    """
    Sets the tracking URI.

    Args:
        tracking_uri (str): The tracking URI to set.
    """
    return MlflowPlugin().set_tracking_uri(tracking_uri=tracking_uri)


def set_experiment(
    experiment_name: Optional[str] = None, experiment_id: Optional[str] = None
):
    """
    Set the active experiment.

    This method sets the specified experiment as the active experiment.
    The active experiment is the one to which subsequent runs will be logged.
    You can specify the experiment by name or by ID.

    Args:
        experiment_name (Optional[str]): The name of the experiment to set as active.
            If `experiment_name` is provided, it takes precedence over `experiment_id`.
        experiment_id (Optional[str]): The ID of the experiment to set as active.
            If `experiment_name` is not provided, `experiment_id` will be used to set
            the active experiment.

    Returns:
        None
    """
    return MlflowPlugin().set_experiment(
        experiment_name=experiment_name, experiment_id=experiment_id
    )


def get_artifact_uri(artifact_path: Optional[str] = None):
    """
    Get the artifact URI of the current or specified  run.

    This method returns the URI of the artifact directory for the current run or for
    the specified artifact path.

    Args:
        artifact_path (Optional[str]): The path of the artifact within the run's artifact directory.
            If not provided, the method returns the URI of the current run's artifact directory.

    Returns:
        str: The URI of the specified artifact path or the current run's artifact directory.
    """
    PluginManager().load_config()

    return MlflowPlugin().get_artifact_uri(artifact_path=artifact_path)


def start_run(
    run_id: Optional[str] = None,
    experiment_id: Optional[str] = None,
    run_name: Optional[str] = None,
    nested: bool = False,
    tags: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
):
    """
    Starts a run.

    This method starts a new run or resumes an existing run if a run_id is provided.

    Args:
        run_id (Optional[str]): The ID of the run to resume. If not provided, a new run is started.
        experiment_id (Optional[str]): The ID of the experiment under which to create the run.
        run_name (Optional[str]): The name of the Mlflow run.
        nested (bool): Whether to create the run as a nested run of the parent run.
        tags (Optional[Dict[str, Any]]): A dictionary of tags to set on the run.
        description (Optional[str]): A description for the run.

    Returns:
        The Run object corresponding to the started or resumed run.
    """
    return MlflowPlugin().start_run(
        run_id=run_id,
        experiment_id=experiment_id,
        run_name=run_name,
        nested=nested,
        tags=tags,
        description=description,
    )


def end_run():
    """
    Ends the current run.

    Returns:
        str: The ID of the ended run.
    """
    return MlflowPlugin().end_run()


def log_param(key: str, value: Any):
    """
    Logs a parameter to the current run.

    Args:
        key (str): The key of the parameter.
        value (Any): The value of the parameter.
    """
    return MlflowPlugin().log_param(key=key, value=value)


def log_metric(
    key: str,
    value: float,
    step: Optional[int] = None,
):
    """
    Logs a metric to the current run.

    Args:
        key (str): The key of the metric.
        value (float): The value of the metric.
        step (int, optional): The step at which the metric was logged.
    """
    return MlflowPlugin().log_metric(
        key=key,
        value=value,
        step=step,
    )


def log_model(
    sk_model,
    artifact_path,
    conda_env=None,
    code_paths=None,
    serialization_format="cloudpickle",
    registered_model_name=None,
    signature: ModelSignature = None,
    input_example: Union[
        pd.DataFrame,
        np.ndarray,
        dict,
        list,
        csr_matrix,
        csc_matrix,
        str,
        bytes,
        tuple,
    ] = None,
    await_registration_for=300,
    pip_requirements=None,
    extra_pip_requirements=None,
    pyfunc_predict_fn="predict",
    metadata=None,
):
    """
    Logs a model.

    Args:
        sk_model: The scikit-learn model to log.
        artifact_path (str): The artifact path to log the model to.
        conda_env (str, optional): The conda environment to use.
        code_paths (list, optional): List of paths to include in the model.
        serialization_format (str, optional): The format to use for serialization.
        registered_model_name (str, optional): The name to register the model under.
        signature (ModelSignature, optional): The signature of the model.
        input_example (Union[pd.DataFrame, np.ndarray, dict, list, csr_matrix, csc_matrix, str,
         bytes, tuple], optional): Example input.
        await_registration_for (int, optional): Time to wait for registration.
        pip_requirements (list, optional): List of pip requirements.
        extra_pip_requirements (list, optional): List of extra pip requirements.
        pyfunc_predict_fn (str, optional): The prediction function to use.
        metadata (dict, optional): Metadata for the model.
    """
    result = MlflowPlugin().log_model(
        sk_model=sk_model,
        artifact_path=artifact_path,
        conda_env=conda_env,
        code_paths=code_paths,
        serialization_format=serialization_format,
        registered_model_name=registered_model_name,
        signature=signature,
        input_example=input_example,
        await_registration_for=await_registration_for,
        pip_requirements=pip_requirements,
        extra_pip_requirements=extra_pip_requirements,
        pyfunc_predict_fn=pyfunc_predict_fn,
        metadata=metadata,
    )

    try:

        # If registered_model_name is not provided, generate it
        if registered_model_name is None:
            # Check if sk_model is a string
            if isinstance(sk_model, str):
                registered_model_name = sk_model
            else:
                # Generate a random string to use as the model name
                registered_model_name = "".join(
                    random.choices(string.ascii_letters + string.digits, k=10)
                )
        response = NotebookPlugin().save_model_details_to_db(registered_model_name)
        print("response_modeldetailstodb", response)
        model_id = response["data"]["id"]
        # print("model_id", model_id)
        if result.model_uri:
            artifact_uri = get_artifact_uri(artifact_path=result.artifact_path)
            # Construct the model URI
            print("model_uri_before_modeluritodb", artifact_uri)
            NotebookPlugin().save_model_uri_to_db(model_id, model_uri=artifact_uri)
    except Exception as exp:
        print(f"Failed to log model details to DB: {exp}")

    return result


def log_model_with_dataset(
    sk_model,
    artifact_path,
    dataset: DatasetMetadata,
    conda_env=None,
    code_paths=None,
    serialization_format="cloudpickle",
    registered_model_name=None,
    signature: ModelSignature = None,
    input_example: Union[
        pd.DataFrame,
        np.ndarray,
        dict,
        list,
        csr_matrix,
        csc_matrix,
        str,
        bytes,
        tuple,
    ] = None,
    await_registration_for=300,
    pip_requirements=None,
    extra_pip_requirements=None,
    pyfunc_predict_fn="predict",
    metadata=None,
):
    """
    Logs a model along with its dataset.

    Args:
        sk_model: The scikit-learn model to log.
        artifact_path (str): The artifact path to log the model to.
        dataset (DatasetMetadata): The dataset metadata.
        conda_env (str, optional): The conda environment to use.
        code_paths (list, optional): List of paths to include in the model.
        serialization_format (str, optional): The format to use for serialization.
        registered_model_name (str, optional): The name to register the model under.
        signature (ModelSignature, optional): The signature of the model.
        input_example (Union[pd.DataFrame, np.ndarray, dict, list, csr_matrix, csc_matrix, str,
         bytes, tuple], optional): Example input.
        await_registration_for (int, optional): Time to wait for registration.
        pip_requirements (list, optional): List of pip requirements.
        extra_pip_requirements (list, optional): List of extra pip requirements.
        pyfunc_predict_fn (str, optional): The prediction function to use.
        metadata (dict, optional): Metadata for the model.
    """
    return DatasetPlugin().log_model_with_dataset(
        sk_model=sk_model,
        artifact_path=artifact_path,
        dataset=dataset,
        conda_env=conda_env,
        code_paths=code_paths,
        serialization_format=serialization_format,
        registered_model_name=registered_model_name,
        signature=signature,
        input_example=input_example,
        await_registration_for=await_registration_for,
        pip_requirements=pip_requirements,
        extra_pip_requirements=extra_pip_requirements,
        pyfunc_predict_fn=pyfunc_predict_fn,
        metadata=metadata,
    )


def link_model_to_dataset(dataset_id, model_id):
    """
    Links a model to a dataset.

    Args:
        dataset_id (str): The ID of the dataset.
        model_id (str): The ID of the model.
    """
    return NotebookPlugin().link_model_to_dataset(
        dataset_id=dataset_id, model_id=model_id
    )


def save_model_uri_to_db(model_id, model_uri):
    """
    Save the model URI to the database.

    :param model_id: ID of the model to update.
    :param model_uri: URI of the model to save.
    :return: Response from the database save operation.
    """
    return NotebookPlugin().save_model_uri_to_db(model_id=model_id, model_uri=model_uri)


def save_dataset_details(dataset):
    """
    Saves dataset details.

    Args:
        dataset: The dataset details to save.

    Returns:
        str: Information message confirming the dataset details are saved.
    """
    return DatasetPlugin().save_dataset_details(dataset=dataset)


def save_model_details_to_db(registered_model_name):
    """
    Saves model details to the database.

    Args:
        registered_model_name (str): The name of the registered model.

    Returns:
        str: Information message confirming the model details are saved.
    """
    return NotebookPlugin().save_model_details_to_db(
        registered_model_name=registered_model_name
    )


def get_model_latest_version(registered_model_name):
    """
    Gets the latest version of a registered model.

    Args:
        registered_model_name (str): The name of the registered model.

    Returns:
        str: The latest version of the registered model.
    """
    return NotebookPlugin().get_model_latest_version(
        registered_model_name=registered_model_name
    )


def search_model_versions(
    filter_string: Optional[str] = None,
):
    """
    Searches for model versions in the model registry based on the specified filters.

    Args:
        filter_string (Optional[str], optional): A string specifying the conditions
        that the model versions must meet.
            It is used to filter the model versions. Examples of filter strings
            include "name='my-model'" or "name='my-model' and version='1'".
            If not provided, all model versions are returned.
            Defaults to None.

    Returns:
        List[dict]: A list of dictionaries, each representing a model version that meets
        the filter criteria. Each dictionary contains information about the model version,
        including its name, version number, creation time, run ID, and other metadata.
    """
    return MlflowPlugin().search_model_versions(filter_string=filter_string)


def pipeline(name=None, description=None):
    """
    Creates a new Kubeflow pipeline.

    Args:
        name (str, optional): The name of the pipeline.
        description (str, optional): The description of the pipeline.

    Returns:
        str: Information message confirming the pipeline creation.
    """
    return KubeflowPlugin().pipeline(name=name, description=description)


def create_component_from_func(
    func,
    output_component_file=None,
    base_image="hiroregistry/cogflow:latest",
    packages_to_install=None,
    annotations: Optional[Mapping[str, str]] = None,
):
    """
    Creates a Kubeflow component from a function.

    Args:
        func: The function to create the component from.
        output_component_file (str, optional): The output file for the component.
        base_image (str, optional): The base image to use. Defaults to
        "hiroregistry/cogflow:latest".
        packages_to_install (list, optional): List of packages to install.
        annotations: Optional. Allows adding arbitrary key-value data to the
        component specification.

    Returns:
        str: Information message confirming the component creation.
    """
    return KubeflowPlugin().create_component_from_func(
        func=func,
        output_component_file=output_component_file,
        base_image=base_image,
        packages_to_install=packages_to_install,
        annotations=annotations,
    )


def client():
    """
    Gets the Kubeflow client.

    Returns:
        KubeflowClient: The Kubeflow client object.
    """
    return KubeflowPlugin().client()


def serve_model_v2(model_uri: str, name: str = None):
    """
    Serves a model using Kubeflow V2.

    Args:
        model_uri (str): The URI of the model to serve.
        name (str, optional): The name of the model to serve.

    Returns:
        str: Information message confirming the model serving.
    """
    return KubeflowPlugin().serve_model_v2(model_uri=model_uri, name=name)


def serve_model_v1(model_uri: str, name: str = None):
    """
    Serves a model using Kubeflow V1.

    Args:
        model_uri (str): The URI of the model to serve.
        name (str, optional): The name of the model to serve.

    Returns:
        str: Information message confirming the model serving.
    """
    return KubeflowPlugin().serve_model_v1(model_uri=model_uri, name=name)


def get_model_url(model_name: str):
    """
    Gets the URL of a served model.

    Args:
        model_name (str): The name of the served model.

    Returns:
        str: The URL of the served model.
    """
    return KubeflowPlugin().get_served_model_url(isvc_name=model_name)


def load_component(file_path=None, url=None, text=None):
    """Loads component from text, file or URL and creates a task factory
    function.

    Only one argument should be specified.

    Args:
        file_path: Path of local file containing the component definition.
        url: The URL of the component file data.
        text: A string containing the component file data.

    Returns:
        A factory function with a strongly-typed signature.
        Once called with the required arguments, the factory constructs a
        pipeline task instance (ContainerOp).
    """
    non_null_args_count = len(
        [name for name, value in locals().items() if value is not None]
    )
    if non_null_args_count != 1:
        raise ValueError("Need to specify exactly one source")
    if file_path:
        return KubeflowPlugin().load_component_from_file(file_path=file_path)
    if url:
        return KubeflowPlugin().load_component_from_url(url=url)
    if text:
        return KubeflowPlugin().load_component_from_text(text=text)
    raise ValueError("Need to specify a source")


def delete_pipeline(pipeline_id):
    """
    method deletes the pipeline
    :param pipeline_id: pipeline id
    :return:
    """
    # list the runs based on pipeline_id
    run_info = NotebookPlugin.list_runs_by_pipeline_id(pipeline_id)
    run_ids = [run["uuid"] for run in run_info["data"]]

    # delete the runs from kfp and db based on pipeline_id
    try:
        KubeflowPlugin().delete_runs(run_ids)
        NotebookPlugin.delete_run_details_from_db(pipeline_id)
    except ApiException as exp:
        print(f"Failed to delete run for the pipeline id {pipeline_id}: {exp}")

    # list the pipeline versions and delete from kfp
    pipeline_version_response = KubeflowPlugin().list_pipeline_versions(
        pipeline_id=pipeline_id
    )
    if pipeline_version_response.versions:
        pipeline_version_details = pipeline_version_response.versions

        pipeline_version_ids = [version.id for version in pipeline_version_details]
        print("Pipeline Version IDs to delete:", pipeline_version_ids)

        # Delete each pipeline version
        for version_id in pipeline_version_ids:
            try:
                KubeflowPlugin().delete_pipeline_version(version_id=version_id)
                print(f"Deleted pipeline version: {version_id}")
            except ApiException as exp:
                print(f"Failed to delete pipeline version {version_id}: {exp}")
    else:
        print(
            f"No pipeline versions found for the specified pipeline ID {pipeline_id}."
        )

    # Delete the pipeline itself
    try:
        KubeflowPlugin().delete_pipeline(pipeline_id=pipeline_id)
        print(f"Deleted pipeline: {pipeline_id}")
    except ApiException as exp:
        print(f"Failed to delete pipeline {pipeline_id}: {exp}")

    NotebookPlugin.delete_pipeline_details_from_db(pipeline_id)


def cogcomponent(
    output_component_file=None,
    base_image="hiroregistry/cogflow:latest",
    packages_to_install=None,
    annotations: Optional[Mapping[str, str]] = None,
):
    """
    Decorator to create a Kubeflow component from a Python function.

    Args:
        output_component_file (str, optional): Path to save the component YAML file.
        Defaults to None.
        base_image (str, optional): Base Docker image for the component. Defaults to
        "hiroregistry/cogflow:latest".
        packages_to_install (List[str], optional): List of additional Python packages
        to install in the component.
        Defaults to None.
        annotations: Optional. Allows adding arbitrary key-value data to the component
        specification.

    Returns:
        Callable: A wrapped function that is now a Kubeflow component.
    """

    def decorator(func):
        return create_component_from_func(
            func=func,
            output_component_file=output_component_file,
            base_image=base_image,
            packages_to_install=packages_to_install,
            annotations=annotations,
        )

    return decorator


def create_run_from_pipeline_func(
    pipeline_func,
    arguments: Optional[Dict[str, Any]] = None,
    run_name: Optional[str] = None,
    experiment_name: Optional[str] = None,
    namespace: Optional[str] = None,
    pipeline_root: Optional[str] = None,
    enable_caching: Optional[bool] = None,
    service_account: Optional[str] = None,
):
    """
        method to create a run from pipeline function
    :param pipeline_func:
    :param arguments:
    :param run_name:
    :param experiment_name:
    :param namespace:
    :param pipeline_root:
    :param enable_caching:
    :param service_account:
    :return:
    """
    run_details = KubeflowPlugin().create_run_from_pipeline_func(
        pipeline_func=pipeline_func,
        arguments=arguments,
        run_name=run_name,
        experiment_name=experiment_name,
        namespace=namespace,
        pipeline_root=pipeline_root,
        enable_caching=enable_caching,
        service_account=service_account,
    )
    # Poll the run status
    while not KubeflowPlugin().is_run_finished(run_details.run_id):
        status = KubeflowPlugin().get_run_status(run_details.run_id)
        print(f"Run {run_details.run_id} status: {status}")
        time.sleep(plugin_config.TIMER_IN_SEC)

    return run_details


def get_pipeline_and_experiment_details(run_id):
    """
        method to return pipeline,run_details,task_details,experiments details based on run_id
    :param run_id: run_id of the run
    :return: dictionary with all the details of pipeline,run_details,task_details,experiments
    """
    try:
        # Get the run details using the run_id
        run_detail = KubeflowPlugin().client().get_run(run_id)
        # Extract run details
        run = run_detail.run
        pipeline_id = run.pipeline_spec.pipeline_id
        experiment_id = run.resource_references[0].key.id
        run_details = {
            "uuid": run.id,
            "display_name": run.name,
            "name": run.name,
            "description": run.description,
            "experiment_uuid": experiment_id,
            "pipeline_uuid": pipeline_id,
            "createdAt_in_sec": run.created_at,
            "scheduledAt_in_sec": run.scheduled_at,
            "finishedAt_in_sec": run.finished_at,
            "state": run.status,
        }

        # Get experiment details using the experiment_id
        experiment = (
            KubeflowPlugin().client().get_experiment(experiment_id=experiment_id)
        )

        experiment_details = {
            "uuid": experiment.id,
            "name": experiment.name,
            "description": experiment.description,
            "createdAt_in_sec": experiment.created_at,
        }

        # Get pipeline details using the pipeline_id
        pipeline_info = KubeflowPlugin().client().get_pipeline(pipeline_id=pipeline_id)

        pipeline_details = {
            "uuid": pipeline_info.id,
            "createdAt_in_sec": pipeline_info.created_at,
            "name": pipeline_info.name,
            "description": pipeline_info.description,
            "parameters": pipeline_info.parameters,
            "experiment_uuid": experiment.id,
            "pipeline_spec": run.pipeline_spec.workflow_manifest,
            "status": run.status,
        }

        workflow_manifest = run_detail.pipeline_runtime.workflow_manifest
        workflow = json.loads(workflow_manifest)

        # Extract the task details
        tasks = workflow["status"]["nodes"]

        task_details = []
        for task_id, task_info in tasks.items():
            task_detail = {
                "uuid": task_id,
                "name": task_info.get("displayName"),
                "state": task_info.get("phase"),
                "runuuid": run.id,
                "startedtimestamp": task_info.get("startedAt"),
                "finishedtimestamp": task_info.get("finishedAt"),
                "createdtimestamp": task_info.get("createdAt"),
            }
            task_details.append(task_detail)

        steps = workflow["status"]["nodes"]
        model_uris = []

        for step_name, step_info in steps.items():
            print(f"step={step_name}")
            if step_info["type"] == "Pod":
                outputs = step_info.get("outputs", {}).get("parameters", [])
                for output in outputs:
                    print(f"Artifact: {output['name']}")
                    print(f"URI: {output['value']}")
                    if is_valid_s3_uri(output["value"]):
                        model_uris.append(output["value"])
                    else:
                        print("Not valid model-uri")
        model_uris = list(set(model_uris))

        model_ids = []
        for model_uri in model_uris:
            PluginManager().load_config()
            # Define the URL
            url = os.getenv(plugin_config.API_BASEPATH) + "/models/uri"
            data = {"uri": model_uri}
            json_data = json.dumps(data)
            headers = {"Content-Type": "application/json"}
            # Make the GET request
            response = requests.get(url, data=json_data, headers=headers, timeout=100)

            # Check if the request was successful
            if response.status_code == 200:
                # Print the response content
                # print('Response Content:')
                model_ids.append(response.json()["data"])
            else:
                print(f"Failed to retrieve data: {response.status_code}")

        return {
            "run_details": run_details,
            "experiment_details": experiment_details,
            "pipeline_details": pipeline_details,
            "task_details": task_details,
            "model_ids": model_ids,
        }
    except Exception as e:
        return e


def log_artifact(local_path: str, artifact_path: Optional[str] = None):
    """
    Log a local file or directory as an artifact of the currently active run. If no run is
    active, this method will create a new active run.

    :param local_path: Path to the file to write.
    :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
    """
    return MlflowPlugin().log_artifact(
        local_path=local_path, artifact_path=artifact_path
    )


original_pyfunc_log_model = pyfunc.log_model


def custom_log_model(
    artifact_path,
    registered_model_name=None,
    loader_module=None,
    data_path=None,
    code_path=None,
    conda_env=None,
    python_model=None,
    artifacts=None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    await_registration_for=300,
    pip_requirements=None,
    extra_pip_requirements=None,
    metadata=None,
    **kwargs,
):
    """
    Custom wrapper around cogflow.pyfunc.log_model with extended signature.

    Args:
        artifact_path (str): The location where model artifacts should be saved.
        loader_module (str, optional): The module that defines how to load the model.
        data_path (str, optional): Path to the data used by the model.
        code_path (str or list, optional): Path(s) to custom code dependencies.
        conda_env (str or dict, optional): Conda environment specification.
        python_model (object, optional): Custom Python model class.
        artifacts (dict, optional): Additional artifacts to log.
        registered_model_name (str, optional): Name of the registered model.
        signature (ModelSignature, optional): Model signature (input/output schema).
        input_example (ModelInputExample, optional): Example input for the model.
        await_registration_for (int, optional): Time to wait for model registration.
        pip_requirements (list, optional): List of pip requirements.
        extra_pip_requirements (list, optional): Additional pip requirements.
        metadata (dict, optional): Additional metadata to log.
        **kwargs: Additional arguments for cogflow.pyfunc.log_model.
    """

    # Call the original cogflow.pyfunc.log_model
    result = original_pyfunc_log_model(
        artifact_path=artifact_path,
        loader_module=loader_module,
        data_path=data_path,
        code_path=code_path,
        conda_env=conda_env,
        python_model=python_model,
        artifacts=artifacts,
        registered_model_name=registered_model_name,
        signature=signature,
        input_example=input_example,
        await_registration_for=await_registration_for,
        pip_requirements=pip_requirements,
        extra_pip_requirements=extra_pip_requirements,
        metadata=metadata,
        **kwargs,
    )

    try:

        # If registered_model_name is not provided, generate it
        if registered_model_name is None:
            # Check if sk_model is a string
            if isinstance(python_model, str):
                registered_model_name = python_model
            else:
                # Generate a random string to use as the model name
                registered_model_name = "".join(
                    random.choices(string.ascii_letters + string.digits, k=10)
                )
        response = NotebookPlugin().save_model_details_to_db(registered_model_name)
        # print("response", response)
        model_id = response["data"]["id"]
        # print("model_id", model_id)
        if result.model_uri:
            artifact_uri = get_artifact_uri(artifact_path=result.artifact_path)
            # Construct the model URI
            # print("model_uri", artifact_uri)
            NotebookPlugin().save_model_uri_to_db(model_id, model_uri=artifact_uri)
    except Exception as exp:
        print(f"Failed to log model details to DB: {exp}")

    return result


# Reassign the custom function to cogflow.pyfunc.log_model
pyfunc.log_model = custom_log_model


def get_served_model_url(isvc_name: str):
    """
    Gets the URL of a served model.

    Args:
        isvc_name (str): The name of the served model.

    Returns:
        str: The URL of the served model.
    """
    return KubeflowPlugin().get_served_model_url(isvc_name=isvc_name)


def delete_served_model(isvc_name: str):
    """
    Deletes a served model.

    Args:
        isvc_name (str): The name of the model to delete.

    Returns:
        str: Information message confirming the deletion of the served model.
    """
    return KubeflowPlugin().delete_served_model(isvc_name=isvc_name)


def serve_model_v2_url(model_uri: str, name: str = None):
    """
    Serves a model using Kubeflow V2.

    Args:
        model_uri (str): The URI of the model to serve.
        name (str, optional): The name of the model to serve.

    Returns:
        str: Information message confirming the model serving.
    """
    try:
        KubeflowPlugin().serve_model_v2(model_uri=model_uri, name=name)
        return get_served_model_url(isvc_name=name)
    except Exception as exp:
        return f"Failed to serve model: {exp}"


def serve_model_v1_url(model_uri: str, name: str = None):
    """
    Serves a model using Kubeflow V1.

    Args:
        model_uri (str): The URI of the model to serve.
        name (str, optional): The name of the model to serve.

    Returns:
        str: Information message confirming the model serving.
    """
    try:
        KubeflowPlugin().serve_model_v1(model_uri=model_uri, name=name)
        return get_served_model_url(isvc_name=name)
    except Exception as exp:
        return f"Failed to serve model: {exp}"


def log_model_by_model_file(model_file_path, model_name):
    """
        log_model in cogflow with the model_file
    :param model_file_path: file_path of model
    :param model_name: name of the model
    :return:
        data = {
            "artifact_uri" : 'artifact_uri of the model',
            "version" : "model version"
        }
    """

    return NotebookPlugin().log_model_by_model_file(model_file_path=model_file_path, model_name=model_name)


def deploy_model(model_name, model_version, isvc_name):
    """

    :param model_name: name of the model
    :param model_version: version of the model
    :param isvc_name: service name to be created for the deployed model
    :return:
    """
    return NotebookPlugin().deploy_model(model_name=model_name, model_version=model_version, isvc_name=isvc_name)


def list_pipelines_by_name(pipeline_name):
    """
    Lists all versions and runs of the specified pipeline by name.

    Args:
        pipeline_name (str): The name of the pipeline to fetch details for.

    Returns:
        dict: A dictionary containing the pipeline ID, versions,
         and runs of the specified pipeline.

    Raises:
        ValueError: If the pipeline name is invalid or not found.
        Exception: For any other issues encountered during the fetch operations.
    """

    NotebookPlugin().list_pipelines_by_name(pipeline_name=pipeline_name)


__all__ = [
    # Methods from MlflowPlugin class
    "InputPath",
    "OutputPath",
    "ParallelFor",
    "pyfunc",
    "mlflow",
    "sklearn",
    "cogclient",
    "tensorflow",
    "pytorch",
    "models",
    "lightgbm",
    "xgboost",
    # Method from CogContainer class
    "add_model_access",
    "kfp",
    "v2",
]
