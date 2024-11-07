from typing import overload
import ghidra.util.task
import java.lang


class MonitoredRunnable(object):
    """
    Similar to a Runnable except the #monitoredRun(TaskMonitor) method is given a
     monitor to report progress and check for cancellation.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def monitoredRun(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Runs this runnable, given a monitor to report progress and check for cancellation.
        @param monitor the monitor.
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

