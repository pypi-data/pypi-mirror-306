from typing import Any, Optional, Dict, Type

from pydantic import BaseModel, Field
from wexample_helpers.const.types import StringsList
from wexample_app.exception.kernel_exception import KernelException
from wexample_prompt.io_manager import IOManager
from wexample_filestate.file_state_manager import FileStateManager
from wexample_app.utils.abstract_command_resolver import AbstractCommandResolver
from wexample_app.utils.runner.abstract_command_runner import AbstractCommandRunner
from wexample_prompt.utils.prompt_response import PromptResponse
from wexample_app.utils.command_request import CommandRequest


class AbstractKernel(BaseModel):
    io: Optional[IOManager] = None
    entrypoint_path: str = Field(description="The main file placed at application root directory")
    resolvers: Dict[str, "AbstractCommandResolver"] = None
    runners: Dict[str, "AbstractCommandRunner"] = None
    env_config: Dict[str, Optional[str]] = None
    expected_env_items: Optional[StringsList] = [
        "APP_ENV"
    ]
    workdir: FileStateManager = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

        self.io = IOManager()

        self._init_workdir()
        self._init_env_values()
        self._init_resolvers()
        self._init_runners()

        # Validate configuration.
        self._check_env_values()

    def _init_env_values(self):
        from dotenv import dotenv_values

        self.env_config = dotenv_values(f"{self.workdir.get_resolved()}{self._get_dotenv_file_name()}")

    def _get_dotenv_file_name(self) -> str:
        from wexample_helpers.const.globals import FILE_NAME_ENV
        return FILE_NAME_ENV

    def _init_workdir(self):
        self.workdir = (self._get_workdir_state_manager_class()).create_from_path(
            path=self.entrypoint_path,
            config={},
            io=self.io
        )

    def _init_resolvers(self):
        self.resolvers = {
            class_definition.get_type(): class_definition(kernel=self)
            for class_definition in self._get_command_resolvers()
        }

    def _init_runners(self):
        self.runners = {
            class_definition.get_runner_name(): class_definition(kernel=self)
            for class_definition in self._get_command_runners()
        }

    def _get_workdir_state_manager_class(self) -> Type[FileStateManager]:
        return FileStateManager

    def _get_command_request_class(self) -> Type["CommandRequest"]:
        from wexample_app.utils.command_request import CommandRequest

        return CommandRequest

    def _check_env_values(self):
        from wexample_helpers.helpers.dict_helper import dict_get_first_missing_key
        first_missing_key = dict_get_first_missing_key(self.env_config, self.expected_env_items)
        if first_missing_key:
            raise KernelException(f"Missing {self._get_dotenv_file_name()} configuration {first_missing_key}")

    def _get_core_configuration_arguments(self) -> list[dict[str, Any]]:
        return []

    def _get_command_resolvers(self) -> list[Type["AbstractCommandResolver"]]:
        return []

    def _get_command_runners(self) -> list[Type["AbstractCommandRunner"]]:
        from wexample_app.utils.runner.python_command_runner import PythonCommandRunner

        return [
            # Default runner.
            PythonCommandRunner
        ]

    def execute_kernel_command(self, request: "CommandRequest") -> PromptResponse:
        return request.execute()

from wexample_app.utils.command import Command
Command.model_rebuild()
CommandRequest.model_rebuild()