from typing import List
from typing import overload
import ghidra.features.base.memsearch.matcher
import java.lang


class SearchHistory(object):
    """
    Class for managing memory search history. It maintains a list of previously used ByteMatchers to
     do memory searching. Each ByteMatcher records the input search text and the search settings used
     to create it.
    """





    @overload
    def __init__(self, maxHistory: int): ...

    @overload
    def __init__(self, other: ghidra.features.base.memsearch.gui.SearchHistory): ...



    def addSearch(self, matcher: ghidra.features.base.memsearch.matcher.ByteMatcher) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getHistoryAsArray(self) -> List[ghidra.features.base.memsearch.matcher.ByteMatcher]: ...

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
    def historyAsArray(self) -> List[ghidra.features.base.memsearch.matcher.ByteMatcher]: ...