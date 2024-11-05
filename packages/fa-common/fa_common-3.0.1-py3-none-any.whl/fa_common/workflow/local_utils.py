import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from io import BytesIO
from typing import List

from fastapi import UploadFile
from prefect import flow, get_run_logger, task
from prefect.runtime import flow_run, task_run
from prefect.task_runners import ConcurrentTaskRunner

from fa_common.models import File
from fa_common.routes.modules.enums import ModuleRunModes
from fa_common.storage import get_storage_client
from fa_common.workflow.enums import FileType
from fa_common.workflow.models import JobTemplate, JobUploads, LocalTaskParams

dirname = os.path.dirname(__file__)


# ========================================================
#     # ####### #       ######  ####### ######   #####
#     # #       #       #     # #       #     # #     #
#     # #       #       #     # #       #     # #
####### #####   #       ######  #####   ######   #####
#     # #       #       #       #       #   #         #
#     # #       #       #       #       #    #  #     #
#     # ####### ####### #       ####### #     #  #####
# ========================================================
def filter_attributes(obj):
    import inspect
    import uuid
    from collections.abc import Iterable

    def is_simple(value):
        """Check if the value is a simple data type or a collection of simple data types."""
        if isinstance(value, (int, float, str, bool, type(None), uuid.UUID)):
            return True
        if isinstance(value, dict):
            return all(is_simple(k) and is_simple(v) for k, v in value.items())
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            return all(is_simple(item) for item in value)
        return False

    result = {}
    for attr in dir(obj):
        # Avoid magic methods and attributes
        if attr.startswith("__") and attr.endswith("__"):
            continue
        value = getattr(obj, attr)
        # Filter out methods and check if the attribute value is simple
        if not callable(value) and not inspect.isclass(value) and is_simple(value):
            result[attr] = value
    return result


# ========================================================
#     # ####### #       ######  ####### ######   #####
#     # #       #       #     # #       #     # #     #
#     # #       #       #     # #       #     # #
####### #####   #       ######  #####   ######   #####
#     # #       #       #       #       #   #         #
#     # #       #       #       #       #    #  #     #
#     # ####### ####### #       ####### #     #  #####
# ========================================================


def delete_directory(dir_path):
    """
    Deletes a directory along with all its contents.

    Args:
    dir_path (str): Path to the directory to be deleted.
    """
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist.")
        return

    try:
        shutil.rmtree(dir_path)
        print(f"Directory {dir_path} has been deleted successfully.")
    except Exception as e:
        print(f"Failed to delete {dir_path}. Reason: {e}")


# from config import ModuleSettings, set_global_settings


def ensure_directories_exist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist, creating...")
            os.makedirs(directory, exist_ok=True)  # The exist_ok=True flag prevents raising an error if the directory already exists.
            print(f"Directory {directory} created.")
        else:
            print(f"Directory {directory} already exists.")


def write_storage_files(file_content: BytesIO, target_path: str, filename: str):
    with open(os.path.join(target_path, filename), "wb") as file:
        file_content.seek(0)
        file.write(file_content.read())


def extract_zip_from_bytesio(file_content: BytesIO, target_path: str):
    file_content.seek(0)
    with zipfile.ZipFile(file_content, "r") as zip_ref:
        # Iterate over all the files and directories in the zip file
        for member in zip_ref.namelist():
            # Determine the full local path of the file
            file_path = os.path.normpath(os.path.join(target_path, member))

            # Check if the file has a directory path, if it does, create the directory
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # If the current member is not just a directory
            if not member.endswith("/"):
                # Open the zip file member, create a corresponding local file
                source = zip_ref.open(member)
                with open(file_path, "wb") as target:
                    shutil.copyfileobj(source, target)
                source.close()

    print("Extraction complete.")


def copy_directory(src, dest, ignore_dirs=["venv", ".venv", "__pycache__"]):
    """
    Copies all files and directories from src to dest, ignoring specified directories.

    Args:
    src (str): Source directory path.
    dest (str): Destination directory path.
    ignore_dirs (list): Directories to ignore.
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            if item not in ignore_dirs:
                copy_directory(s, d, ignore_dirs)
        else:
            shutil.copy2(s, d)


"""
  #####  #     # ######     #######    #     #####  #    #  #####
 #     # #     # #     #       #      # #   #     # #   #  #     #
 #       #     # #     #       #     #   #  #       #  #   #
  #####  #     # ######        #    #     #  #####  ###     #####
       # #     # #     #       #    #######       # #  #         #
 #     # #     # #     #       #    #     # #     # #   #  #     #
  #####   #####  ######        #    #     #  #####  #    #  #####

"""


async def init_working_directory(info: LocalTaskParams):
    logger = get_run_logger()
    module_runner = f"{info.module_path}/{info.module_version}"
    copy_directory(module_runner, info.working_dir, info.ignore_copy_dirs)

    logger.info(info.working_dir)
    chk_dirs = [
        info.working_dir,
        os.path.join(info.working_dir, info.input_path),
        os.path.join(info.working_dir, info.output_path),
    ]
    ensure_directories_exist(chk_dirs)


async def download_files(work_dir, sub_dir, files: List[File]):
    """
    The function `download_files` downloads files from a storage client and writes them to a specified
    directory.

    :param work_dir: The `work_dir` parameter represents the directory where the downloaded files will
    be stored. It is the main directory where the `sub_dir` will be created to store the downloaded
    files
    :param sub_dir: The `sub_dir` parameter in the `download_files` function represents the subdirectory
    within the `work_dir` where the downloaded files will be stored. It is used to specify the relative
    path within the `work_dir` where the files should be saved
    :param files: The `files` parameter is a list of `File` objects that contains information about the
    files to be downloaded. Each `File` object likely has attributes such as `bucket` (the storage
    bucket where the file is located) and `path` (the path to the file within the bucket)
    :type files: List[File]
    """
    storage_client = get_storage_client()
    target_path = os.path.join(work_dir, sub_dir)
    for file in files:
        file_content = await storage_client.get_file(file.bucket, file.id)
        if file_content:
            filename = os.path.basename(file.id)
            write_storage_files(file_content, target_path, filename)


async def download_module(info: LocalTaskParams):
    logger = get_run_logger()
    from fa_common.storage import get_storage_client

    storage_client = get_storage_client()
    target_path = os.path.join(info.module_path, info.module_version)

    if os.path.exists(target_path):
        logger.info(f"Module version already exists: {info.module_path}/{info.module_version}/")
        return

    # @NOTE: the "/" at the tail is quite important
    lst_objs = await storage_client.list_files(info.module_bucket, f"{info.module_remote_path}/{info.module_version}/")
    lst_files = list(filter(lambda f: not f.dir, lst_objs))

    if len(lst_files) == 0:
        raise ValueError(
            f"No content was found in the modules remote path: {info.module_bucket}/{info.module_remote_path}/{info.module_version}"
        )

    ensure_directories_exist([info.module_path, target_path])

    for file in lst_files:
        file_content = await storage_client.get_file(info.module_bucket, file.id)
        if file_content:
            if ".zip" in file.id:
                extract_zip_from_bytesio(file_content, target_path)
            else:
                filename = os.path.basename(file.id)
                write_storage_files(file_content, target_path, filename)
            logger.info("Module Ready to Use!")
            return
    raise ValueError(f"Module Not Found: {info.module_remote_path}/{info.module_version}")


async def write_params_to_file(info: LocalTaskParams, input_params, filetype: FileType = FileType.JSON, filename="param.json"):
    """
    Writes the input parameters required for a module in the pre-defined input path.

    Useful for scenarios where the module expects the input_params as input_file rather
    than directly passing the params.

    :param: input_params: dict of parameters
    """
    if filetype == FileType.JSON:
        with open(os.path.join(os.path.join(info.working_dir, info.input_path), filename), "w") as f:
            json.dump(input_params, f, indent=2)
        return

    if filetype == FileType.TXT:
        raise NotImplementedError("TXT file type handling not implemented.")

    if filetype == FileType.YAML:
        raise NotImplementedError("YAML file type handling not implemented.")

    raise ValueError("Unknown filetype")


async def run_standalone(info: LocalTaskParams):
    logger = get_run_logger()

    commands = [f"cd {info.working_dir}", *info.module_run_cmd]
    full_command = " && ".join(commands)

    try:
        result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
        result.check_returncode()
        # Adding 1 sec buffer to make sure the process is complete.
        await asyncio.sleep(1)
    except subprocess.CalledProcessError as e:
        logger.error("Command failed with exit code %s", e.returncode)
        logger.error("Output:\n%s", e.stdout)
        logger.error("Errors:\n%s", e.stderr)
        raise Exception(f"Subprocess failed with exit code {e.returncode}. Check logs for more details.") from e
        # raise Exception(f"Subprocess failed with exit code {e.returncode}")


def execute_function_from_script(script_name, func_name, script_path, *args, **kwargs):
    """
    Fetch and execute a function directly from a Python script located in a specific directory.

    Args:
        module_name (str): The name to assign to the module (does not need to match the file name).
        task_name (str): The name of the function to execute from the script.
        plugin_path (str): Full path to the Python script.
        *args: Positional arguments passed to the function.
        **kwargs: Keyword arguments passed to the function.

    Returns:
        Any: The result of the function execution.
    """
    import importlib.util

    try:
        # Construct full module file path
        module_path = os.path.join(script_path, script_name + ".py")

        # Load the module spec and module from the file location
        spec = importlib.util.spec_from_file_location(script_name, module_path)
        if spec is None:
            raise ImportError(f"Could not load spec for {script_name} at {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the function from the loaded module
        func = getattr(module, func_name)
        if not callable(func):
            raise TypeError(f"Attribute {func_name} of module {script_name} is not callable")

        # Execute the function with arguments
        return func(*args, **kwargs)
    except ImportError as e:
        raise ImportError(f"Unable to load module '{script_name}': {e}") from e
    except AttributeError as e:
        raise AttributeError(f"The script '{script_name}' does not have a function named '{func_name}': {e}") from e


async def upload_outputs(info: LocalTaskParams, upload_items: JobUploads):
    from pathlib import Path

    logger = get_run_logger()
    if upload_items.bucket_name is None:
        raise ValueError("For local runs, storage bucket name should be defined.")

    storage_client = get_storage_client()
    folder_path = Path(os.path.join(info.working_dir, info.output_path))
    for item in folder_path.rglob("*"):
        if item.is_file():
            parent_path = upload_items.custom_path if item.name in upload_items.selected_outputs else upload_items.default_path
            remote_path = "/".join([parent_path, flow_run.get_id(), task_run.get_name(), item.relative_to(folder_path).as_posix()]).replace(
                "//", "/"
            )
            file_path = os.path.join(folder_path, item.name)
            logger.info(f"Uploading {file_path} to remote destination {remote_path} in {upload_items.bucket_name}")
            with open(file_path, "rb") as f:
                upload_item = UploadFile(filename=item.name, file=f)
                await storage_client.upload_file(upload_item, upload_items.bucket_name, remote_path)

    logger.info(f"All files uploaded to {os.path.join(parent_path, flow_run.get_id())}")


async def cleanup(rm_folders):
    """This function aims to clean up working/temp directories."""
    for folder in rm_folders:
        delete_directory(folder)


"""
 #     # ####### ######  #    # ####### #       ####### #     #    ######  ####### ####### ### #     # ### ####### ### ####### #     #
 #  #  # #     # #     # #   #  #       #       #     # #  #  #    #     # #       #        #  ##    #  #     #     #  #     # ##    #
 #  #  # #     # #     # #  #   #       #       #     # #  #  #    #     # #       #        #  # #   #  #     #     #  #     # # #   #
 #  #  # #     # ######  ###    #####   #       #     # #  #  #    #     # #####   #####    #  #  #  #  #     #     #  #     # #  #  #
 #  #  # #     # #   #   #  #   #       #       #     # #  #  #    #     # #       #        #  #   # #  #     #     #  #     # #   # #
 #  #  # #     # #    #  #   #  #       #       #     # #  #  #    #     # #       #        #  #    ##  #     #     #  #     # #    ##
  ## ##  ####### #     # #    # #       ####### #######  ## ##     ######  ####### #       ### #     # ###    #    ### ####### #     #

"""


def generate_task_name():
    # flow_name = flow_run.flow_name
    # task_name = task_run.task_name

    parameters = task_run.parameters
    name = parameters["job_name"]

    return name


@task(
    name="single-run-module",
    description="This task runs a module. It only handles one run.",
    task_run_name=generate_task_name,
    retries=0,
    log_prints=True,
)
async def run_job_task(job: JobTemplate, job_name: str, ignore_clean_up: bool = False):
    if job.template_config.standalone_base_path:
        base_path = job.template_config.standalone_base_path
    else:
        base_path = os.path.join(os.getcwd(), "standalone")
    local_path = os.path.join(base_path, job.module.name)
    tmp_dir = tempfile.mkdtemp()
    repo_ref = job.module.version.module_meta.repo_ref

    if isinstance(repo_ref.run_meta.cmd, str):
        repo_ref.run_meta.cmd = [repo_ref.run_meta.cmd]

    if repo_ref.run_meta.mode == ModuleRunModes.VENV:
        if len(repo_ref.run_meta.cmd) > 1:
            raise ValueError("When using virtual envs to run a script, only one command line is acceptable.")

        repo_ref.run_meta.cmd[0] = f"{os.path.join(local_path, job.module.version.name)}/{repo_ref.run_meta.cmd[0]}"

    info = LocalTaskParams(
        standalone_base_path=base_path,
        module_path=local_path,
        module_name=job.module.name,
        module_bucket=repo_ref.bucket.bucket_name,
        module_remote_path=repo_ref.bucket.path_prefix,
        module_version=job.module.version.name,
        module_run_mode=repo_ref.run_meta.mode.value,
        module_run_cmd=repo_ref.run_meta.cmd,
        working_dir=tmp_dir,
        input_path=repo_ref.run_meta.input_path,
        output_path=repo_ref.run_meta.output_path,
        use_tmp_dir=repo_ref.use_tmp_dir,
        ignore_copy_dirs=repo_ref.ignore_copy,
    )

    for k, v in info.model_dump().items():
        task_run.parameters[k] = v

    input_params = job.inputs.parameters
    if isinstance(input_params, str):
        # If it is string then it should be a JSON_STR
        input_params = json.loads(input_params)

    if not isinstance(input_params, dict):
        raise ValueError("Input Parameters should be convertable to python dictionary.")

    try:
        await download_module(info)
        await init_working_directory(info)
        if len(job.inputs.files) > 0:
            await download_files(info.working_dir, info.input_path, job.inputs.files)

        if info.module_run_mode in (ModuleRunModes.SUBPROCESS, ModuleRunModes.VENV):
            await write_params_to_file(info, input_params, FileType.JSON, "param.json")
            await run_standalone(info)
        else:
            # WHEN RUNNING THROUGH A FUNCTION IN SCRIPTS FOLLOWING ASSUMTIONS ARE MADE:
            # 1. SCRIPT NAME: main.py
            # 2. SCRIPT FUNCTION: def main(input_params)
            execute_function_from_script(
                script_name="main", func_name="main", script_path=info.working_dir, input_params=input_params, working_dir=info.working_dir
            )

        await upload_outputs(info, job.uploads)
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await cleanup(rm_folders=[] if ignore_clean_up else [info.working_dir])

    return {"task_id": task_run.get_id(), "task_name": task_run.get_name()}


def generate_flow_run_name():
    # flow_name = flow_run.flow_name

    parameters = flow_run.parameters
    name = parameters["flow_name"]

    return f"{name}: {flow_run.get_id()}"


@flow(
    name="Run Jobs",
    task_runner=ConcurrentTaskRunner(),
    flow_run_name=generate_flow_run_name,
    description="This flow runs a batch of jobs locally and concurrently.",
)
def run_prefect_jobs(jobs: List[JobTemplate], flow_name: str, ignore_clean_up: bool = False):
    lst_tasks = []
    for i, job in enumerate(jobs):
        lst_tasks.append(run_job_task.submit(job=job, job_name=f"{job.name}-{i}", ignore_clean_up=ignore_clean_up))

    # return lst_tasks


# ==========================================================================================
####### ####### #     # ######  #          #    ####### #######     #####  ####### #     #
#    #       ##   ## #     # #         # #      #    #          #     # #       ##    #
#    #       # # # # #     # #        #   #     #    #          #       #       # #   #
#    #####   #  #  # ######  #       #     #    #    #####      #  #### #####   #  #  #
#    #       #     # #       #       #######    #    #          #     # #       #   # #
#    #       #     # #       #       #     #    #    #          #     # #       #    ##
#    ####### #     # #       ####### #     #    #    #######     #####  ####### #     #

# ==========================================================================================

# class LocalWorkflowRun(CamelModel):
#     id: WorkflowId = None
#     flow_run: Optional[WorkflowOutput] = None
#     template_config: Optional[WorkflowConfig | LocalTaskParams] = None
#     sub_flows: List['LocalWorkflowRun'] = []

#     def get_flow_params(self):
#         params = {}
#         for param in self.template_config.parameters:
#             params[param.name] = param.value
#         return LocalTaskParams(**params)

#     def get_flow_setup_template(self):
#         return {"workflow": self.template_config.model_dump()}


# class LocalTemplateGenerator:

#     @classmethod
#     def gen_local_batch_workflow(
#         cls,
#         jobs: List[JobTemplate],
#         run_mode: LocalRunModes,
#         ignore_clean_up: bool = True
#     ):
#         batch_manifest = {
#             "batchFlows": {
#                 "runner": run_mode.value,
#                 "items": []
#             }
#         }
#         templates_folder = tempfile.mkdtemp()
#         lst_sub_flows = []
#         for i, job in enumerate(jobs):
#             lst_sub_flows.append(
#                 LocalTemplateGenerator.gen_local_workflow(
#                     job=job,
#                     flow_template_folder=templates_folder,
#                     template_file_name=f'setup_{i}.yaml',
#                     rm_folders=[] if ignore_clean_up else ["working_dir", "tmp_dir"]
#                 )
#             )
#             batch_manifest.get("batchFlows").get("items").append(
#                 {"path": f'setup_{i}.yaml'}
#             )

#         # IMPORTANT NOTE: BE AWARE OF ON-EXIT EVENT WHEN CONCURRENT FLOWS ARE ENABLED
#             # AN SPECIAL TREATMEN WILL BE REQUIRED.
#         if not ignore_clean_up:
#             lst_sub_flows.append(
#                 LocalTemplateGenerator.gen_on_exit(
#                     rm_folders=[] if ignore_clean_up else ["flow_template_folder"],
#                     flow_template_folder=templates_folder,
#                     template_file_name='on_exit.yaml',
#                 )
#             )
#             batch_manifest.get("batchFlows").get("items").append(
#                 {"path": 'on_exit.yaml'}
#             )

#         with open(os.path.join(templates_folder, "batch.yaml"), 'w') as file:
#             yaml.safe_dump(batch_manifest, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

#         return LocalWorkflowRun(
#             sub_flows=lst_sub_flows,
#         )


#     @classmethod
#     def gen_on_exit(cls, rm_folders, flow_template_folder: str, template_file_name: str="on_exit.yaml"):
#         tmp_dir     = tempfile.mkdtemp()


#         info = LocalTaskParams(**{
#             "module_name"          : "onExitEvent",
#             "tmp_dir"              : tmp_dir,
#             "use_tmp_dir"          : True,
#             "flow_template_folder" : flow_template_folder,
#             "template_file_name"   : template_file_name,
#         })


#         base               = cls.gen_base_block(info, runner='sequential')
#         task_clean_up      = cls.gen_flow_cleanup(rm_folders)
#         base.get("workflow").get("tasks").append(task_clean_up)

#         template_write_dir = flow_template_folder if flow_template_folder else tmp_dir
#         with open(os.path.join(template_write_dir, template_file_name), 'w') as file:
#             yaml.safe_dump(base, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

#         return LocalWorkflowRun(template_config= WorkflowConfig(**base.get("workflow")))


#     @classmethod
#     def gen_local_workflow(
#         cls,
#         job: JobTemplate,
#         flow_template_folder: str = None,
#         template_file_name: str = "setup.yaml",
#         rm_folders: List[str]=["working_dir", "tmp_dir"]
#     ) -> LocalWorkflowRun:

#         base_path   = job.template_config.standalone_base_path
#         local_path  = os.path.join(base_path, job.module.name)
#         tmp_dir     = tempfile.mkdtemp()
#         repo_ref    = job.module.version.module_meta.repo_ref


#         if isinstance(repo_ref.run_meta.cmd, str):
#             repo_ref.run_meta.cmd = [repo_ref.run_meta.cmd]

#         if repo_ref.run_meta.mode == ModuleRunModes.VENV:
#             if (isinstance(repo_ref.run_meta.cmd, list)):
#                 if len(repo_ref.run_meta.cmd) > 1:
#                     raise ValueError("When using virtual envs to run a script, only one command line is acceptable.")

#             repo_ref.run_meta.cmd[0] = f"{os.path.join(local_path, job.module.version.name)}/{repo_ref.run_meta.cmd[0]}"


#         info = LocalTaskParams(**{
#             "standalone_base_path" : base_path,
#             "module_path"          : local_path,
#             "module_name"          : job.module.name,
#             "module_bucket"        : repo_ref.bucket.bucket_name,
#             "module_remote_path"   : repo_ref.bucket.base_path,
#             "module_version"       : job.module.version.name,
#             "module_run_mode"      : repo_ref.run_meta.mode.value,
#             "module_run_cmd"       : repo_ref.run_meta.cmd,
#             "tmp_dir"              : tmp_dir,
#             "input_path"           : repo_ref.run_meta.input_path,
#             "output_path"          : repo_ref.run_meta.output_path,
#             "use_tmp_dir"          : repo_ref.use_tmp_dir,
#             "flow_template_folder" : flow_template_folder,
#             "template_file_name"   : template_file_name,
#             "ignore_copy_dirs"     : repo_ref.ignore_copy
#         })


#         input_params = job.inputs.parameters
#         if isinstance(input_params, str):
#             # If it is string then it should be a JSON_STR
#             input_params = json.loads(input_params)

#         if not isinstance(input_params, dict):
#             raise ValueError("Input Parameters should be convertable to python dictionary.")

#         base               = cls.gen_base_block(info, runner='sequential')
#         task_get_module    = cls.gen_download_module()
#         task_work_dir      = cls.gen_working_directory(info)
#         task_clean_up      = cls.gen_flow_cleanup(rm_folders)

#         base.get("workflow").get("tasks").append(task_get_module)
#         base.get("workflow").get("tasks").append(task_work_dir)
#         if len(job.inputs.files) > 0:
#             # downloads = [file.id for file in job.inputs.files ]
#             task_download      = cls.gen_download_temp(job.inputs.files)
#             base.get("workflow").get("tasks").append(task_download)

#         if (info.module_run_mode == ModuleRunModes.SUBPROCESS or
#             info.module_run_mode == ModuleRunModes.VENV):
#             task_write_params  = cls.gen_write_param_files(input_params)
#             base.get("workflow").get("tasks").append(task_write_params)

#             task_run           = cls.gen_run_module_subprocess(info)
#         else:
#             task_run           = cls.gen_run_module_func(info, input_params)


#         base.get("workflow").get("tasks").append(task_run)
#         base.get("workflow").get("tasks").append(task_clean_up)

#         template_write_dir = flow_template_folder if flow_template_folder else tmp_dir
#         with open(os.path.join(template_write_dir, template_file_name), 'w') as file:
#             yaml.safe_dump(base, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

#         return LocalWorkflowRun(template_config= WorkflowConfig(**base.get("workflow")))


#     @classmethod
#     def gen_base_block(cls, info: LocalTaskParams, runner='sequential'):
#         flow_params = [{"name": k, "value": v} for k,v in info.model_dump().items()]
#         return {
#             "workflow": {
#                 "name": info.module_name,
#                 "runner": runner,
#                 "parameters": flow_params,
#                 "tasks": []
#             }
#         }

#     @classmethod
#     def gen_download_module(cls):
#         return {
#             "name": "pull-module-version",
#             "plugin_path": dirname, # os.path.join(config_module.get("STANDALONE_BASE_PATH"), "plugins"),
#             "module": "local_utils",
#             "task": "download_module",
#             "inputs": {
#                 "parameters": [
#                     {"name": "bucket_name", "value": "module_bucket", "type": "flow" },
#                     {"name": "module_local_path", "value": "module_path", "type": "flow"},
#                     {"name": "module_remote_path", "value": "module_remote_path", "type": "flow"},
#                     {"name": "version", "value": "module_version", "type": "flow"},
#                 ]
#             }
#         }


#     @classmethod
#     def gen_working_directory(cls, info):
#         return {
#             "name": "generate-working directory",
#             "plugin_path": dirname, # os.path.join(config_module.get("STANDALONE_BASE_PATH"), "plugins"),
#             "module": "local_utils",
#             "task": "init_working_directory",
#             "inputs": {
#                 "parameters": [{"name": "ignore_dirs", "value": info.ignore_copy_dirs}]
#             }
#         }

#     @classmethod
#     def gen_download_temp(cls, files: List[File]):
#         sources = []
#         for file in files:
#             sources.append(file.model_dump())

#         return {
#             "name": "download-required-files",
#             "plugin_path": dirname, # os.path.join(config_module.get("STANDALONE_BASE_PATH"), "plugins"),
#             "module": "local_utils",
#             "task": "download_files",
#             "inputs": {
#                 "parameters": [
#                     # {"name": "bucket_name", "value": settings.BUCKET_NAME},
#                     {"name": "work_dir", "value": "working_dir", "type": "flow"},
#                     {"name": "sub_dir", "value": "input_path", "type": "flow"},
#                     {"name": "sources", "value": sources},
#                 ]
#             }
#         }


#     @classmethod
#     def gen_write_param_files(cls, input_params):
#         return {
#             "name": "write-param-json",
#             "plugin_path": dirname, # os.path.join(config_module.get("STANDALONE_BASE_PATH"), "plugins"),
#             "module": "local_utils",
#             "task": "write_params_to_file",
#             "inputs": {
#                 "parameters": [
#                     {"name": "input_params", "value": input_params},
#                     {"name": "filetype", "value": "json"},
#                     {"name": "filename", "value": "param.json"}
#                 ]
#             }
#         }

#     @classmethod
#     def gen_run_module_func(cls, info, input_params):
#         """
#         Running an module function provides convenience, but the restriction is
#         you should use the base environment that is set for your app/api.
#         """
#         if info.use_tmp_dir:
#             plugin_path = info.get("tmp_dir")
#         else:
#             plugin_path = f"{info.module_path}/{info.module_version}"
#         return {
#             "name": "run-module-func",
#             "plugin_path": plugin_path,
#             "module": "main",
#             "task": "main",
#             "inputs": {
#                 "parameters": [{"name": "input_params", "value": input_params}]
#             }
#         }


#     @classmethod
#     def gen_run_module_subprocess(cls, info):
#         """
#         Use this to run:
#         - Executables
#         - Python modules that have isolated environments
#         """
#         return {
#             "name": "run-module-exe",
#             "module": "logic.actions",
#             "task": "run_standalone_script_modified",
#             "inputs": {
#                 "parameters": [
#                     {"name": "base_path", "value": info.tmp_dir},
#                     {"name": "package_name", "value": ""},
#                     {"name": "package_run_cmds", "value": info.module_run_cmd},
#                 ]
#             },
#         }

#     @classmethod
#     def gen_flow_cleanup(cls, rm_folders=List[str]):
#         return {
#             "name": "clean-up",
#             "plugin_path": dirname,
#             "module": "local_utils",
#             "task": "cleanup",
#             "inputs": {
#                 "parameters": [
#                     {"name": "rm_folders", "value": rm_folders}
#                 ]
#             },
#         }
