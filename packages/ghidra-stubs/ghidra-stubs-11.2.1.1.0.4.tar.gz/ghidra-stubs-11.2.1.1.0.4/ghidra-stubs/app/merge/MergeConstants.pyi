from typing import overload
import java.lang


class MergeConstants(object):
    CONFLICT_COLOR: generic.theme.GColor
    HIGHLIGHT_COLOR: java.awt.Color
    LATEST: int = 1
    LATEST_TITLE: unicode = u'Latest'
    MY: int = 2
    MY_TITLE: unicode = u'Checked Out'
    ORIGINAL: int = 3
    ORIGINAL_TITLE: unicode = u'Original'
    PICKED_LATEST_CODE_UNITS: unicode = u'PickedLatestCodeUnits'
    PICKED_MY_CODE_UNITS: unicode = u'PickedMyCodeUnits'
    PICKED_ORIGINAL_CODE_UNITS: unicode = u'PickedOriginalCodeUnits'
    RESOLVED_CODE_UNITS: unicode = u'ResolvedCodeUnits'
    RESOLVED_LATEST_DTS: unicode = u'ResolvedLatestDataTypes'
    RESOLVED_LATEST_SYMBOLS: unicode = u'ResolvedLatestSymbols'
    RESOLVED_MY_DTS: unicode = u'ResolvedMyDataTypes'
    RESOLVED_MY_SYMBOLS: unicode = u'ResolvedMySymbols'
    RESOLVED_ORIGINAL_DTS: unicode = u'ResolvedOriginalDataTypes'
    RESOLVED_ORIGINAL_SYMBOLS: unicode = u'ResolvedOriginalSymbols'
    RESULT: int = 0
    RESULT_TITLE: unicode = u'Result'







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

