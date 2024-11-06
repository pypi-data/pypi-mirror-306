from typing import Any

from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_app.utils.abstract_kernel import AbstractKernel


class AbstractKernelChild(BaseModel):
    kernel: "AbstractKernel"