import contextlib

from pyautd3_link_soem.native_methods.autd3capi_link_soem import NativeMethods as Soem
from pyautd3_link_soem.native_methods.autd3capi_link_soem import ProcessPriority, SyncMode, TimerStrategy

from .adapter import EtherCATAdapter
from .local import SOEM
from .remote import RemoteSOEM
from .status import Status
from .thread_priority import ThreadPriority


def tracing_init() -> None:
    from pyautd3 import tracing_init as autd3_tracing_init

    autd3_tracing_init()
    with contextlib.suppress(BaseException):
        Soem().link_soem_tracing_init()


__all__ = ["SOEM", "RemoteSOEM", "Status", "ThreadPriority", "EtherCATAdapter", "ProcessPriority", "SyncMode", "TimerStrategy"]


__version__ = "29.0.0rc4"
