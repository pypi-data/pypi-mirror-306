import asyncio
from copy import deepcopy
from typing import Any, Optional

from fa_common.models import StorageLocation

from .base_client import WorkflowBaseClient
from .local_utils import run_prefect_jobs
from .models import JobTemplate, LocalWorkflowRun, WorkflowRun


class LocalWorkflowClient(WorkflowBaseClient):
    """
    Singleton client for interacting with local-workflows.
    Is a wrapper over the existing local-workflows python client to provide specialist functions for
    the Job/Module workflow.

    Please don't use it directly, use `fa_common.workflow.utils.get_workflow_client`.
    """

    __instance = None
    # local_workflow_client = None

    def __new__(cls) -> "LocalWorkflowClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            # app = get_current_app()
            # cls.__instance.local_workflow_client = app.local_workflow_client  # type: ignore
        return cls.__instance

    # FIXME: Base case currently expects an ArgoWorkflowRun but should use a generic baseclass
    async def run_job(self, job_base: JobTemplate, verbose: bool = True) -> WorkflowRun:
        if isinstance(job_base.inputs, list):
            jobs = []
            for i, inp in enumerate(job_base.inputs):
                job = deepcopy(job_base)
                job.custom_id = i + 1
                job.name = f"{job.name}-subjob-{i+1}"
                job.inputs = inp
                jobs.append(job)
        else:
            jobs = [job_base]

        flow_run = run_prefect_jobs(jobs, flow_name=job_base.module.name, ignore_clean_up=True, return_state=True)
        # flow_run_name = f"{job_base.module.name}: {flow_run.id}"
        return WorkflowRun(
            workflow_id=str(flow_run.id),
            mode=job_base.submit_mode,
            message=flow_run.message,
            status=flow_run.type.value,
            detail=LocalWorkflowRun(id=str(flow_run.id), state=flow_run.type.value, message=flow_run.message, template=job_base),
        )
        # return

    async def get_workflow(
        self,
        workflow_id: str,
        storage_location: StorageLocation | None = None,
        output: bool = False,
        file_refs: bool = True,
        namespace: Optional[str] = None,
        verbose: bool = True,
    ) -> WorkflowRun:
        """
        This Python function defines an abstract method `get_workflow` that retrieves
        information about a workflow run.
        """
        print("get_workflow is currently a placeholder")
        await asyncio.sleep(0)

        raise NotImplementedError("get_workflow is not implemented for local runs.")

    async def delete_workflow(self, workflow_id: str, storage_location: StorageLocation, **kwargs) -> bool:
        """
        :param force_data_delete: if True, if workflow does not exist in the records,
        it would yet continue with deletion of artifacts and output data.
        """
        print("delete_workflow is currently a placeholder")
        await asyncio.sleep(0)
        raise NotImplementedError("delete_workflow is not implemented for local runs.")

    async def _delete_workflow_artifacts(self, workflow_id: str, **kwargs):
        """This method deletes artifacts of a workflow."""
        print("_delete_workflow_artifacts is currently a placeholder")
        await asyncio.sleep(0)

    async def retry_workflow(self, workflow_id: str, user_id: Optional[str] = None):
        """Retry the workflow."""
        print("retry_workflow is currently a placeholder")
        await asyncio.sleep(0)
        raise NotImplementedError("retry_workflow is not implemented for local runs.")

    async def get_workflow_log(
        self,
        workflow_id: str,
        storage_location: StorageLocation,
        namespace: str | None = None,
    ) -> dict[Any, Any]:
        """
        This abstract method defines an asynchronous function to retrieve
        the workflow log based on the workflow ID, with optional parameters
        for bucket ID and namespace.
        """
        print("get_workflow_log is currently a placeholder")
        await asyncio.sleep(0)
        return {}
