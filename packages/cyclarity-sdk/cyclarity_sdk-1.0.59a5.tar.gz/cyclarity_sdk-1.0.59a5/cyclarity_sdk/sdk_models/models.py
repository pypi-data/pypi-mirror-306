import os
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from cyclarity_sdk.sdk_models.types import ExecutionStatus  # noqa

''' Test step definitions'''


class ExecutionMetadata(BaseModel):
    execution_id: str
    agent_id: Optional[str] = None
    test_id: str
    step_id: Optional[str] = None
    step_name: Optional[str] = None
    step_version: Optional[str] = None


class ExecutionState(BaseModel):
    '''Data structure to be send via topic::execution-state'''
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: Optional[str] = ''


class RunningEnvType(str, Enum):
    IOT = "iot_device"
    BATCH = "batch"


'''Execution definitions'''


class PackageType(str, Enum):
    # Supported types for test step deployment
    PIP = "PIP"
    ZIP = "ZIP"


class MessageType(str, Enum):
    # Supported types for test step deployment
    LOG = "LOG"
    TEST_STATE = "TEST_STATE"
    EXECUTION_STATE = "EXECUTION_STATE"
    FINDING = "FINDING"
    TEST_ARTIFACT = "TEST_ARTIFACT"
    EXECUTION_OUTPUT = "EXECUTION_OUTPUT"


class CyclarityFile(BaseModel):
    '''CyclarityFile is a model for using files as in params for component'''
    file_name: str
    path: str = Field(default_factory=lambda: CyclarityFile.calculate_path())

    @staticmethod
    def calculate_path(file_name: str = '') -> str:
        # Get the directory path of the current file
        directory_path = os.path.dirname(os.path.abspath(__file__))
        # Combine the directory path with the file name
        return os.path.join(directory_path, file_name)

    def __init__(self, **data):
        super().__init__(**data)
        # Set path with the specific file_name for this instance
        self.path = self.calculate_path(self.file_name)
