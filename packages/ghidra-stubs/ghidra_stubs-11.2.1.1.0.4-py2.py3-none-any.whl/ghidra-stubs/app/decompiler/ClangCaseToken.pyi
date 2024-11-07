from typing import Iterator
from typing import List
from typing import overload
import ghidra.app.decompiler
import ghidra.program.model.address
import ghidra.program.model.pcode
import ghidra.program.model.scalar
import java.awt
import java.lang


class ClangCaseToken(ghidra.app.decompiler.ClangToken):
    """
    A token representing a switch "case" label, or other constant not directly linked to data-flow.
     The token has an associated constant value and a data-type
    """





    def __init__(self, par: ghidra.app.decompiler.ClangNode): ...



    def Child(self, i: int) -> ghidra.app.decompiler.ClangNode: ...

    def Parent(self) -> ghidra.app.decompiler.ClangNode: ...

    @staticmethod
    def buildSpacer(par: ghidra.app.decompiler.ClangNode, indent: int, indentStr: unicode) -> ghidra.app.decompiler.ClangToken:
        """
        Add a spacer token to the given text grouping
        @param par is the text grouping
        @param indent is the number of levels to indent
        @param indentStr is a string representing containg the number of spaces in one indent level
        @return the new spacer token
        """
        ...

    @staticmethod
    def buildToken(node: int, par: ghidra.app.decompiler.ClangNode, decoder: ghidra.program.model.pcode.Decoder, pfactory: ghidra.program.model.pcode.PcodeFactory) -> ghidra.app.decompiler.ClangToken:
        """
        Decode one specialized token from the current position in an encoded stream.  This
         serves as a factory for allocating the various objects derived from ClangToken
        @param node is the particular token type (already) decoded from the stream
        @param par is the text grouping which will contain the token
        @param decoder is the decoder for the stream
        @param pfactory is used to look up p-code objects associated with tokens
        @return the new ClangToken
        @throws DecoderException for problems decoding the stream
        """
        ...

    def decode(self, decoder: ghidra.program.model.pcode.Decoder, pfactory: ghidra.program.model.pcode.PcodeFactory) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def flatten(self, __a0: List[object]) -> None: ...

    def getClangFunction(self) -> ghidra.app.decompiler.ClangFunction: ...

    def getClass(self) -> java.lang.Class: ...

    def getHighSymbol(self, highFunction: ghidra.program.model.pcode.HighFunction) -> ghidra.program.model.pcode.HighSymbol: ...

    def getHighVariable(self) -> ghidra.program.model.pcode.HighVariable: ...

    def getHighlight(self) -> java.awt.Color:
        """
        Get the background highlight color used to render this token, or null if not highlighted
        @return the Color or null
        """
        ...

    def getLineParent(self) -> ghidra.app.decompiler.ClangLine:
        """
        Get the element representing an entire line of text that contains this element
        @return the containing ClangLine
        """
        ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getPcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

    def getScalar(self) -> ghidra.program.model.scalar.Scalar: ...

    def getSwitchOp(self) -> ghidra.program.model.pcode.PcodeOp:
        """
        @return the BRANCHIND PcodeOp that jumps to this label
        """
        ...

    def getSyntaxType(self) -> int:
        """
        Get the "syntax" type (color) associated with this token (keyword, type, etc)
        @return the color code
        """
        ...

    def getText(self) -> unicode:
        """
        @return this token's display text as a string
        """
        ...

    def getVarnode(self) -> ghidra.program.model.pcode.Varnode: ...

    def hashCode(self) -> int: ...

    def isMatchingToken(self) -> bool:
        """
        @return true if this token should be displayed with "matching" highlighting
        """
        ...

    def isVariableRef(self) -> bool: ...

    def iterator(self, forward: bool) -> Iterator[ghidra.app.decompiler.ClangToken]:
        """
        Get an iterator over tokens starting with this ClangToken.  Tokens are returned in normal
         display order (forward=true) or in the reverse of normal display order (forward=false)
        @param forward is true for forward iterator, false for a backward iterator
        @return the Iterator object
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def numChildren(self) -> int: ...

    def setHighlight(self, val: java.awt.Color) -> None: ...

    def setLineParent(self, line: ghidra.app.decompiler.ClangLine) -> None:
        """
        Set (change) the line which this text element part of.
        @param line is the new ClangLine
        """
        ...

    def setMatchingToken(self, matchingToken: bool) -> None:
        """
        Set whether or not additional "matching" highlighting is applied to this token.
         Currently this means a bounding box is drawn around the token.
        @param matchingToken is true to enable highlighting, false to disable
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
    def highVariable(self) -> ghidra.program.model.pcode.HighVariable: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def pcodeOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

    @property
    def scalar(self) -> ghidra.program.model.scalar.Scalar: ...

    @property
    def switchOp(self) -> ghidra.program.model.pcode.PcodeOp: ...

    @property
    def variableRef(self) -> bool: ...

    @property
    def varnode(self) -> ghidra.program.model.pcode.Varnode: ...