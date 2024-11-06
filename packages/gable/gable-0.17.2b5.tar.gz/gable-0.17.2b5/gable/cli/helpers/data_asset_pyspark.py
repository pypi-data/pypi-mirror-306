import json
import os
import re
from typing import Any, Optional, Tuple, Union

import click
import yaml
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.data_asset import (
    gather_pyspark_asset_data,
    get_abs_project_root_path,
    get_git_repo,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import (
    clone_to_temp_dir,
    get_git_repo_db,
    get_git_repo_info,
    get_origin_head_default_branch,
    get_pr_link,
    get_relative_file_path,
)
from gable.openapi import (
    CheckComplianceDataAssetsPySparkRequest,
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetResponse,
    ErrorResponse,
    ErrorResponseDeprecated,
    IngestDataAssetResponse,
    PySparkAsset,
    RegisterDataAssetPySparkRequest,
    ResponseType,
    SqlQueries,
)
from git import Repo
from loguru import logger


def register_pyspark_data_assets(
    ctx: ClickContext,
    spark_job_entrypoint: str,
    project_root: str,
    connection_string: Optional[str],
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    dry_run: bool,
) -> Tuple[Union[IngestDataAssetResponse, ErrorResponseDeprecated], bool, int]:
    project_name, relative_spark_job_entrypoint, git_repo_relative_project_root = (
        get_relative_paths(project_root, spark_job_entrypoint)
    )
    csv_schema_file = os.path.abspath(csv_schema_file) if csv_schema_file else None
    sca_results_dict, data_asset_sql = gather_pyspark_asset_data(
        get_abs_project_root_path(project_root),
        spark_job_entrypoint,
        csv_schema_file,
        csv_path_to_table_file,
        connection_string,
        ctx.obj.client,
    )
    git_ssh_repo = get_git_repo(project_root)
    git_repo = get_git_repo_db(get_abs_project_root_path(project_root), True)
    try:
        main_branch_data_asset_sql = get_main_branch_data_asset_sql(
            git_repo,
            ctx,
            spark_job_entrypoint=spark_job_entrypoint,
            git_repo_relative_project_root=git_repo_relative_project_root,
            project_root=get_abs_project_root_path(project_root),
            csv_schema_file=csv_schema_file,
            csv_path_to_table_file=csv_path_to_table_file,
            connection_string=connection_string,
        )
    except Exception as e:
        logger.warning(f"Error getting main branch data asset SQL: {e}")
        main_branch_data_asset_sql = None
    if sca_results_dict is {}:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
        )
    if data_asset_sql and main_branch_data_asset_sql:
        for sql in data_asset_sql.values():
            logger.debug("CURRENT\n" + sql)
        for sql in main_branch_data_asset_sql.values():
            logger.debug("MAIN\n" + sql)
    logger.info(
        f"{EMOJI.GREEN_CHECK.value} Pyspark data asset(s) found:\n{json.dumps(sca_results_dict, indent=4)}"
    )
    assets = [
        PySparkAsset(
            schema=event_schema,
            git_host=git_ssh_repo,
            project_name=project_name,
            spark_entrypoint=relative_spark_job_entrypoint,
            spark_table=event_name,
            sql_queries=(
                SqlQueries(
                    old=main_branch_data_asset_sql[event_name],
                    new=data_asset_sql[event_name],
                )
                if main_branch_data_asset_sql
                else None
            ),
        )
        for event_name, event_schema in sca_results_dict.items()
    ]
    if dry_run:
        logger.info("Dry run mode. Data asset registration not performed.")
    request = RegisterDataAssetPySparkRequest(
        dry_run=dry_run,
        assets=assets,
        prLink=get_pr_link(),
    )
    # click doesn't let us specify the type of ctx.obj.client in the Context:
    client: GableAPIClient = ctx.obj.client
    return client.post_data_asset_register_pyspark(request)


def check_compliance_pyspark_data_asset(
    ctx: ClickContext,
    spark_job_entrypoint: str,
    project_root: str,
    connection_string: Optional[str],
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    response_type: ResponseType,
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetResponse],
]:
    project_name, relative_spark_job_entrypoint, git_repo_relative_project_root = (
        get_relative_paths(project_root, spark_job_entrypoint)
    )
    csv_schema_file = os.path.abspath(csv_schema_file) if csv_schema_file else None
    sca_results_dict, data_asset_sql = gather_pyspark_asset_data(
        get_abs_project_root_path(project_root),
        spark_job_entrypoint,
        csv_schema_file,
        csv_path_to_table_file,
        connection_string,
        ctx.obj.client,
    )
    git_ssh_repo = get_git_repo(project_root)
    git_repo = get_git_repo_db(get_abs_project_root_path(project_root), True)
    try:
        main_branch_data_asset_sql = get_main_branch_data_asset_sql(
            git_repo,
            ctx,
            spark_job_entrypoint=spark_job_entrypoint,
            git_repo_relative_project_root=git_repo_relative_project_root,
            project_root=get_abs_project_root_path(project_root),
            csv_schema_file=csv_schema_file,
            csv_path_to_table_file=csv_path_to_table_file,
            connection_string=connection_string,
        )
    except Exception as e:
        logger.warning(f"Error getting main branch data asset SQL: {e}")
        main_branch_data_asset_sql = None
    if sca_results_dict is {}:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to check! You can use the --debug or --trace flags for more details.",
        )
    if data_asset_sql and main_branch_data_asset_sql:
        for sql in data_asset_sql.values():
            logger.debug("CURRENT\n" + sql)
        for sql in main_branch_data_asset_sql.values():
            logger.debug("MAIN\n" + sql)
    assets = [
        PySparkAsset(
            schema=event_schema,
            git_host=git_ssh_repo,
            project_name=project_name,
            spark_entrypoint=relative_spark_job_entrypoint,
            spark_table=event_name,
            sql_queries=(
                SqlQueries(
                    old=main_branch_data_asset_sql[event_name],
                    new=data_asset_sql[event_name],
                )
                if main_branch_data_asset_sql
                else None
            ),
        )
        for event_name, event_schema in sca_results_dict.items()
    ]
    request = CheckComplianceDataAssetsPySparkRequest(
        assets=assets,
        responseType=response_type,
        prLink=get_pr_link(),
    )
    # click doesn't let us specify the type of ctx.obj.client in the Context:
    client: GableAPIClient = ctx.obj.client
    return client.post_check_compliance_data_assets_pyspark(request)


def get_spark_job_entrypoint_file(spark_job_entrypoint: str) -> str:
    """Remove any arguments that are passed into the entrypoint script (not our CLI args, args expected by the customer)
    Returns Just the PySpark script file path"""
    return re.split(r"\s+", spark_job_entrypoint)[0]


def get_relative_paths(
    project_root: str, spark_job_entrypoint: str
) -> Tuple[str, str, str]:
    """Returns the name of the Python project, the relative path to the PySpark script from the project root, and the project
    root relative to the git repository root."""
    spark_job_entrypoint_no_args = os.path.join(
        project_root, get_spark_job_entrypoint_file(spark_job_entrypoint)
    )
    git_repo_info = get_git_repo_info(spark_job_entrypoint_no_args)
    relative_spark_job_entrypoint = get_relative_file_path(
        git_repo_info, spark_job_entrypoint_no_args
    )
    relative_project_root = get_relative_file_path(
        git_repo_info, get_abs_project_root_path(project_root)
    )
    project_name = os.path.basename(relative_project_root)
    return (
        project_name,
        re.sub(r"^/", "", relative_spark_job_entrypoint),
        relative_project_root,
    )


def get_nested_value(d: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in d:
            d = d[key]
        else:
            return None
    return d


def read_config_file(
    config_file: click.File, config_entrypoint: str, config_args: Optional[str] = None
) -> str:
    try:
        config_file_yaml: dict[str, Any] = yaml.safe_load(config_file)  # type: ignore
        spark_job_entrypoint = get_nested_value(
            config_file_yaml, config_entrypoint.split(".")
        )
        spark_job_args = (
            get_nested_value(config_file_yaml, config_args.split("."))
            if config_args
            else None
        )

        return spark_job_entrypoint + (
            f' {" ".join(spark_job_args)}' if spark_job_args else ""
        )

    except yaml.scanner.ScannerError as exc:  # type: ignore
        # This should be a custom exception for user errors
        raise click.ClickException(f"Error parsing YAML file: {config_file}")


def get_main_branch_data_asset_sql(
    git_repo: Repo,
    ctx: ClickContext,
    spark_job_entrypoint: str,
    git_repo_relative_project_root: str,
    project_root: str,
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    connection_string: Optional[str],
):
    if os.environ.get("CI", "false") == "true":
        git_repo.git.checkout("main")
    else:
        # Clone the git repo to a temporary directory and checkout the main branch
        temp_git_repo, temp_git_repo_dir = clone_to_temp_dir(
            git_repo, get_origin_head_default_branch(git_repo)
        )
        project_root = os.path.join(temp_git_repo_dir, git_repo_relative_project_root)
    _, data_asset_sql = gather_pyspark_asset_data(
        project_root,
        spark_job_entrypoint,
        csv_schema_file,
        csv_path_to_table_file,
        connection_string,
        ctx.obj.client,
    )
    return data_asset_sql
