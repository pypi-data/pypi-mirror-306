from typing import List
from typing import overload
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.template
import ghidra.program.model.address
import ghidra.program.model.lang
import ghidra.program.model.lang.InjectPayload
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.xml
import java.lang


class InjectPayloadJumpAssist(ghidra.program.model.lang.InjectPayloadSleigh):




    def __init__(self, bName: unicode, sourceName: unicode): ...



    def encode(self, encoder: ghidra.program.model.pcode.Encoder) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getDummyPcode(addrFactory: ghidra.program.model.address.AddressFactory) -> ghidra.app.plugin.processors.sleigh.template.ConstructTpl:
        """
        Build a dummy p-code sequence to use in place of a normal parsed payload.
         A ConstructTpl is built out of Varnode and PcodeOp templates that can
         be assigned directly to the pcodeTemplate field of the payload.
         The sequence itself is non-empty, consisting of a single operation:
            tmp = tmp + 0;
        @param addrFactory is used to construct temp and constant Varnodes
        @return the final dummy template
        """
        ...

    def getInput(self) -> List[ghidra.program.model.lang.InjectPayload.InjectParameter]: ...

    def getName(self) -> unicode: ...

    def getOutput(self) -> List[ghidra.program.model.lang.InjectPayload.InjectParameter]: ...

    def getParamShift(self) -> int: ...

    def getPcode(self, program: ghidra.program.model.listing.Program, con: ghidra.program.model.lang.InjectContext) -> List[ghidra.program.model.pcode.PcodeOp]: ...

    def getSource(self) -> unicode: ...

    def getType(self) -> int: ...

    def hashCode(self) -> int: ...

    def inject(self, context: ghidra.program.model.lang.InjectContext, emit: ghidra.app.plugin.processors.sleigh.PcodeEmit) -> None: ...

    def isEquivalent(self, obj: ghidra.program.model.lang.InjectPayload) -> bool: ...

    def isErrorPlaceholder(self) -> bool: ...

    def isFallThru(self) -> bool: ...

    def isIncidentalCopy(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def restoreXml(self, parser: ghidra.xml.XmlPullParser, language: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

