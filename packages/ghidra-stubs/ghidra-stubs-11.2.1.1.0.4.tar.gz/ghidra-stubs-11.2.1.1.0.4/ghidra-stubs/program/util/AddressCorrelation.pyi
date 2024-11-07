from typing import overload
import ghidra.program.model.address
import ghidra.program.util
import ghidra.util.task
import java.lang


class AddressCorrelation(object):
    """
    Interface representing the address mapping for any means of correlating addresses
     between a source program and a destination program.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCorrelatedDestinationRange(self, sourceAddress: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.util.AddressCorrelationRange:
        """
        Returns the AddressRange of a set of addresses in the destination
         program that correlates to corresponding range in the source program.
        @param sourceAddress the source program address
        @param monitor the task monitor
        @return the destination program address range, or null if there is not address range mapped
        @throws CancelledException if cancelled
        """
        ...

    def getName(self) -> unicode:
        """
        This method is no longer part of the API.  Leaving a default implementation to reduce 
         breaking clients.
        @return the simple class name of the implementing class
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def name(self) -> unicode: ...