from typing import Iterator
from typing import overload
import ghidra.program.model.address
import java.lang
import java.util
import java.util.function


class AddressRangeSplitter(object, ghidra.program.model.address.AddressRangeIterator):
    """
    AddressRangeIterator that takes a single address range and breaks it down into smaller
     address ranges of a specified maximum size. This is useful for clients that want to break
     down the processing of large address ranges into manageable chunks. For example, searching the
     bytes in memory can be broken so that chunks can be read into reasonably sized buffers.
    """





    def __init__(self, range: ghidra.program.model.address.AddressRange, splitSize: int, forward: bool):
        """
        Constructor
        @param range the address range to split apart
        @param splitSize the max size of each sub range
        @param forward if true, the sub ranges will be returned in address order; otherwise they
         will be returned in reverse address order.
        """
        ...

    def __iter__(self) -> Iterator[ghidra.program.model.address.AddressRange]: ...

    def equals(self, __a0: object) -> bool: ...

    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    def forEachRemaining(self, __a0: java.util.function.Consumer) -> None: ...

    def getClass(self) -> java.lang.Class: ...

    def hasNext(self) -> bool: ...

    def hashCode(self) -> int: ...

    def iterator(self) -> java.util.Iterator: ...

    def next(self) -> ghidra.program.model.address.AddressRange: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def remove(self) -> None: ...

    def spliterator(self) -> java.util.Spliterator: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

