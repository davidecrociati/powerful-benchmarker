from .base_factory import BaseFactory
import pytorch_metric_learning.utils.logging_presets as logging_presets


class _RecordKeeperAdapter:
    """
    Lightweight shim to smooth API differences across record-keeper versions.

    Some versions of pytorch-metric-learning's hooks call
    RecordKeeper.update_records(..., parent_name=...), while newer
    record-keeper expects "input_group_name_for_non_objects" instead.

    This adapter accepts either keyword and forwards the call to the
    underlying record keeper with the expected argument name.
    """

    def __init__(self, rk):
        self._rk = rk

    def __getattr__(self, name):
        # Delegate any other attribute/method access to the wrapped object
        return getattr(self._rk, name)

    def update_records(self, *args, **kwargs):
        # Map deprecated/alternate kwarg to the currently supported one
        if "parent_name" in kwargs and "input_group_name_for_non_objects" not in kwargs:
            kwargs["input_group_name_for_non_objects"] = kwargs.pop("parent_name")
        return self._rk.update_records(*args, **kwargs)

class RecordKeeperFactory(BaseFactory):
    def _create_general(self, record_keeper_type):
        record_keeper, _, _ = logging_presets.get_record_keeper(**record_keeper_type)
        # Wrap with adapter to handle signature differences across versions
        return _RecordKeeperAdapter(record_keeper)