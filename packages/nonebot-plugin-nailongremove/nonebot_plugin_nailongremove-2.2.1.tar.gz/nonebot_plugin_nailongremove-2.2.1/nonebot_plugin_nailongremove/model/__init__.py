from typing import Awaitable, Callable, Literal, NoReturn, Tuple, Union
from typing_extensions import TypeAlias

import numpy as np
from nonebot.utils import run_sync

from ..config import ModelType, config


def raise_extra_import_error(e: BaseException, group: str) -> NoReturn:
    raise ImportError(
        f"Possibly missing required libraries, "
        f"Please run `pip install nonebot-plugin-nailongremove[{group}]` "
        f"in your project's environment to install.",
    ) from e


CheckResultTuple: TypeAlias = Union[
    Tuple[bool, None],
    Tuple[Literal[True], np.ndarray],
]
CheckResult: TypeAlias = Union[bool, CheckResultTuple]

check_image_sync: Callable[[np.ndarray], CheckResult]

if config.nailong_model is ModelType.CLASSIFICATION:
    from .classification import check_image as check_image_sync

elif config.nailong_model is ModelType.TARGET_DETECTION:
    try:
        from .target_detection import check_image as check_image_sync
    except ImportError as e:
        raise_extra_import_error(e, "model1")

else:
    raise ValueError("Invalid model type")


check_image: Callable[[np.ndarray], Awaitable[CheckResult]] = run_sync(check_image_sync)
