from typing import overload
import ghidra.program.model.data
import java.lang


class DataTypeNamingUtil(object):








    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def generateMangledSignature(functionDefinition: ghidra.program.model.data.FunctionDefinitionDataType) -> unicode:
        """
        Generate a simple mangled function signature.  Generated string will start with
         {@code _func}.
        @param functionDefinition function definition is used for generating the name
        @return generated name
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def setMangledAnonymousFunctionName(functionDefinition: ghidra.program.model.data.FunctionDefinitionDataType) -> unicode:
        """
        Generate a simple mangled function definition name and apply it to the specified
         functionDefinition.  Generated name will start with {@code _func}.
        @param functionDefinition function definition whose name should be set
        @return name applied to functionDefinition
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

