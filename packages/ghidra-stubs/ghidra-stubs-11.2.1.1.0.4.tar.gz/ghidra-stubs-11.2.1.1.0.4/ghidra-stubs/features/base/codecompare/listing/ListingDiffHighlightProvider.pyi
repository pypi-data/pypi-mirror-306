from typing import List
from typing import overload
import docking.widgets.fieldpanel.support
import ghidra.app.util
import ghidra.app.util.viewer.field
import java.lang


class ListingDiffHighlightProvider(object, ghidra.app.util.ListingHighlightProvider):
    NO_HIGHLIGHTS: List[docking.widgets.fieldpanel.support.Highlight]



    def __init__(self, listingDiff: ghidra.program.util.ListingDiff, side: ghidra.util.datastruct.Duo.Side, comparisonOptions: ghidra.features.base.codecompare.listing.ListingCodeComparisonOptions):
        """
        Constructor for this highlight provider.
        @param listingDiff the ListingDiff to use to determine where there are differences that 
         need highlighting.
        @param side LEFT or RIGHT
         false means the highlights are for the second listing.
        @param comparisonOptions the tool options that indicate the current 
         background colors for the Listing code comparison panel.
        """
        ...



    def createHighlights(self, text: unicode, field: ghidra.app.util.viewer.field.ListingField, cursorTextOffset: int) -> List[docking.widgets.fieldpanel.support.Highlight]: ...

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

