from typing import overload
import ghidra.features.base.memsearch.searcher
import ghidra.program.model.address
import ghidra.util.datastruct
import ghidra.util.task
import java.lang
import java.util.function


class MemorySearcher(object):
    """
    Class for searching bytes from a byteSource (memory) using a ByteMatcher. It handles
     breaking the search down into a series of searches, handling gaps in the address set and
     breaking large address ranges down into manageable sizes.
 
     It is created with a specific byte source, matcher, address set, and search limit. Clients can
     then either call the #findAll(Accumulator, TaskMonitor) method or use it to incrementally
     search using #findNext(Address, TaskMonitor), 
     #findPrevious(Address, TaskMonitor), or #findOnce(Address, boolean, TaskMonitor).
    """





    @overload
    def __init__(self, byteSource: ghidra.features.base.memsearch.bytesource.AddressableByteSource, matcher: ghidra.features.base.memsearch.matcher.ByteMatcher, addresses: ghidra.program.model.address.AddressSet, searchLimit: int):
        """
        Constructor
        @param byteSource the source of the bytes to be searched
        @param matcher the matcher that can find matches in a byte sequence
        @param addresses the address in the byte source to search
        @param searchLimit the max number of hits before stopping
        """
        ...

    @overload
    def __init__(self, byteSource: ghidra.features.base.memsearch.bytesource.AddressableByteSource, matcher: ghidra.features.base.memsearch.matcher.ByteMatcher, addresses: ghidra.program.model.address.AddressSet, searchLimit: int, chunkSize: int):
        """
        Constructor
        @param byteSource the source of the bytes to be searched
        @param matcher the matcher that can find matches in a byte sequence
        @param addresses the address in the byte source to search
        @param searchLimit the max number of hits before stopping
        @param chunkSize the maximum number of bytes to feed to the matcher at any one time.
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def findAll(self, accumulator: ghidra.util.datastruct.Accumulator, monitor: ghidra.util.task.TaskMonitor) -> bool:
        """
        Searches all the addresses in this search's {@link AddressSetView} using the byte matcher to
         find matches. As each match is found (and passes any filters), the match is given to the 
         accumulator. The search continues until either the entire address set has been search or
         the search limit has been reached.
        @param accumulator the accumulator for found matches
        @param monitor the task monitor
        @return true if the search completed searching through the entire address set.
        """
        ...

    def findNext(self, start: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> ghidra.features.base.memsearch.searcher.MemoryMatch:
        """
        Searches forwards starting at the given address until a match is found or
         the end of the address set is reached. It does not currently wrap the search.
        @param start the address to start searching
        @param monitor the task monitor
        @return the first match found or null if no match found.
        """
        ...

    def findOnce(self, start: ghidra.program.model.address.Address, forward: bool, monitor: ghidra.util.task.TaskMonitor) -> ghidra.features.base.memsearch.searcher.MemoryMatch:
        """
        Searches forwards or backwards starting at the given address until a match is found or
         the start or end of the address set is reached. It does not currently wrap the search.
        @param start the address to start searching
        @param forward if true, search forward, otherwise, search backwards.
        @param monitor the task monitor
        @return the first match found or null if no match found.
        """
        ...

    def findPrevious(self, start: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> ghidra.features.base.memsearch.searcher.MemoryMatch:
        """
        Searches backwards starting at the given address until a match is found or
         the beginning of the address set is reached. It does not currently wrap the search.
        @param start the address to start searching
        @param monitor the task monitor
        @return the first match found or null if no match found.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setMatchFilter(self, filter: java.util.function.Predicate) -> None:
        """
        Sets any match filters. The filter can be used to exclude matches that don't meet some
         criteria that is not captured in the byte matcher such as alignment and code unit type.
        @param filter the predicate to use to filter search results
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def matchFilter(self) -> None: ...  # No getter available.

    @matchFilter.setter
    def matchFilter(self, value: java.util.function.Predicate) -> None: ...