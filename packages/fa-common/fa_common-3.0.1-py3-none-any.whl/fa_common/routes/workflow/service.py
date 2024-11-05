from typing import List, Optional

import httpx
from fastapi import BackgroundTasks

from fa_common import get_logger
from fa_common.config import get_settings
from fa_common.enums import WorkflowEnums
from fa_common.exceptions import BadRequestError, UnImplementedError
from fa_common.models import StorageLocation
from fa_common.routes.modules.models import ModuleDocument
from fa_common.routes.modules.types import ModuleVersion
from fa_common.routes.project.service import get_project_for_user
from fa_common.routes.user.models import UserDB
from fa_common.workflow.argo_client import ArgoClient
from fa_common.workflow.enums import JobSubmitMode
from fa_common.workflow.local_client import LocalWorkflowClient
from fa_common.workflow.models import JobTemplate, LocalWorkflowRun, WorkflowCallBack, WorkflowRun
from fa_common.workflow.service import WorkflowService
from fa_common.workflow.utils import get_workflow_client

from .types import RequestCallback

logger = get_logger()


async def run_workflow(background_tasks: BackgroundTasks, job: JobTemplate) -> WorkflowRun:
    module_name = job.module.name
    module_ver = job.module.version
    if isinstance(module_ver, ModuleVersion):
        module_ver = module_ver.name

    job.module = await ModuleDocument.get_version(module_name, module_ver)

    if job.submit_mode == JobSubmitMode.ISOLATED:
        workflow_client: ArgoClient = get_workflow_client(mode=WorkflowEnums.Type.ARGO)
        # res: WorkflowRun = await workflow_client.run_job(job_base=job)
        # return res
    elif job.submit_mode in (JobSubmitMode.LOCAL, JobSubmitMode.ISOLATED_LOCAL):
        workflow_client: LocalWorkflowClient = get_workflow_client(mode=WorkflowEnums.Type.LOCAL)  # type: ignore
        # background_tasks.add_task(run_local_job_in_background, job, workflow_client)  # type: ignore
        # _id = id(job)
        # # Fixme: Duplication between Workflow run and local workflow run
        # return WorkflowRun(
        #     workflow_id=str(_id),
        #     mode=job.submit_mode,
        #     message="Local Job started in background.",
        #     detail=LocalWorkflowRun(id=str(_id), template=job),
        # )

    else:
        raise BadRequestError(f"Unknown submit mode: {job.submit_mode}")

    return await workflow_client.run_job(job_base=job)


async def get_workflow(
    workflow_id: str,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    storage_location: StorageLocation | None = None,
    output: bool = False,
    file_refs: bool = False,
    namespace: Optional[str] = None,
) -> WorkflowRun:
    if mode == WorkflowEnums.Type.LOCAL:
        raise UnImplementedError("Get workflow is not implemented for local runs.")

    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.get_workflow(
        storage_location=storage_location,
        workflow_id=workflow_id,
        output=output,
        file_refs=file_refs,
        namespace=namespace,
    )


async def get_workflow_log(
    workflow_id: str,
    storage_location: StorageLocation,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    namespace: Optional[str] = None,
):
    if mode == WorkflowEnums.Type.LOCAL:
        raise UnImplementedError("Getting workflow logs is not implemented for local runs.")

    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.get_workflow_log(
        workflow_id=workflow_id,
        storage_location=storage_location,
        namespace=namespace,
    )


async def delete_workflow(
    workflow_id: str,
    storage_location: StorageLocation,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    namespace: Optional[str] = None,
):
    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.delete_workflow(
        workflow_id=workflow_id,
        storage_location=storage_location,
        namespace=namespace,
        force_data_delete=True,
    )


async def callback(items: List[WorkflowCallBack], result: LocalWorkflowRun, task_id: int):
    for item in items:
        headers = {"x-api-key": item.api_key} if item.api_key else {}
        data = RequestCallback(
            workflow=result.model_dump(),
            metadata=item.metadata,
            message="Local Job completed!",
            background_task_id=task_id,
        )
        async with httpx.AsyncClient() as client:
            await client.post(item.url, json=data.model_dump(), headers=headers)


async def run_local_job_in_background(job: JobTemplate, workflow_client: LocalWorkflowClient):
    logger.info(f"Starting background job for job ID: {id(job)}")
    try:
        result = await workflow_client.run_job(job_base=job)
        logger.info(f"Job completed with result: {result}")
        if job.callbacks:
            await callback(items=job.callbacks, result=result, task_id=id(job))
            logger.info("Callback has been executed successfully.")
    except Exception as e:
        logger.error(f"Error occurred: {e!s}")
        raise


async def validate_workflow_params(
    current_user: UserDB, project_id: Optional[str] = None, mode: WorkflowEnums.Type | None = None
) -> tuple[StorageLocation, str | None, WorkflowEnums.Type]:
    """Gets the correct storage location, namespace, and mode for the workflow or raises an error if user/project is invalid.

    Parameters
    ----------
    current_user : UserDB
        _description_
    project_id : Optional[str], optional
        _description_, by default None
    mode : WorkflowEnums.Type | None, optional
        _description_, by default None

    Returns
    -------
    tuple[StorageLocation, str | None, WorkflowEnums.Type]
        _description_

    Raises
    ------
    BadRequestError
        _description_
    """

    settings = get_settings()
    mode = mode if mode is not None else settings.WORKFLOW_TYPE
    if mode is None:
        raise BadRequestError("A default workflow mode is not set in the settings and none was provided.")
    namespace = settings.ARGO_NAMESPACE

    if project_id is not None:
        project = await get_project_for_user(current_user, project_id)  # noqa
        storage_location = WorkflowService.get_workflow_storage_location_from_settings_proj(project_id)
    else:
        storage_location = WorkflowService.get_workflow_storage_location_from_settings_user(current_user.sub)

    return storage_location, namespace, mode


# async def verify_api_key(x_api_key: str = Header(...)):
#     if x_api_key != wb_settings.MASTER_API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid API Key")
#     return x_api_key
