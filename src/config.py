from google.cloud.logging import Client
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Self
from typing_extensions import Annotated
from nexo.types.dict import OptStrToStrDict
from nexo.types.string import OptStr
from .enums import LogLevel


class LogConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dir: Annotated[str, Field(..., description="Log's directory")]
    level: Annotated[LogLevel, Field(LogLevel.INFO, description="Log's level")] = (
        LogLevel.INFO
    )

    google_cloud_logging: Annotated[
        Client | None, Field(None, description="Google cloud logging")
    ] = None

    labels: Annotated[
        OptStrToStrDict, Field(None, description="Log labels. (Optional)")
    ] = None

    aggregate_file_name: Annotated[
        OptStr, Field(None, description="Log aggregate file name")
    ] = None

    individual_log: Annotated[
        bool, Field(True, description="Whether to have individual log")
    ] = True

    @model_validator(mode="after")
    def validate_aggregate_file_name(self) -> Self:
        if isinstance(self.aggregate_file_name, str):
            if not self.aggregate_file_name.endswith(".log"):
                self.aggregate_file_name += ".log"

        return self
