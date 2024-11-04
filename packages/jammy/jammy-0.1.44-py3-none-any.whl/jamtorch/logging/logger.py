from typing import Any

from jammy import logging

from ..distributed import get_rank, is_rank0

try:
    import torch_xla.core.xla_model as xm  # pylint: disable=import-error

    IS_TPU = True
except Exception as e:  # pylint: disable=broad-except
    IS_TPU = False

__all__ = ["get_logger"]


def get_logger(*args, **kwargs):
    if IS_TPU:
        if xm.get_ordinal == 0:
            return logging.get_logger(*args, **kwargs)
    elif is_rank0():
        return logging.get_logger(*args, **kwargs)

    return logging.fake_logger


def loguru_rank0_only_filter(record: Any) -> bool:
    rank0_only = record["extra"].get("rank0_only", True)
    if is_rank0() and rank0_only:
        return True
    if not rank0_only:
        record["message"] = f"[RANK {get_rank()}]" + record["message"]
    return not is_rank0
