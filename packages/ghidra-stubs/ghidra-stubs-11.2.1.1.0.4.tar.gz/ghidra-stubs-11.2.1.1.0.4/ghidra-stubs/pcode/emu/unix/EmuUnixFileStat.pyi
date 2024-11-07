from typing import overload
import ghidra.pcode.emu.unix
import java.lang


class EmuUnixFileStat(object):
    """
    Collects the  fields common to UNIX platforms
 
 
     See a UNIX manual for the exact meaning of each field.
 
 
     TODO: Should this be parameterized with T?
 
 
     TODO: Are these specific to Linux, or all UNIX?
    """

    MODE_R: int = 4
    MODE_W: int = 2
    MODE_X: int = 1
    st_atim_nsec: long
    st_atim_sec: long
    st_blksize: long
    st_blocks: long
    st_ctim_nsec: long
    st_ctim_sec: long
    st_dev: long
    st_gid: int
    st_ino: long
    st_mode: int
    st_mtim_nsec: long
    st_mtim_sec: long
    st_nlink: long
    st_rdev: long
    st_size: long
    st_uid: int



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hasPermissions(self, req: int, user: ghidra.pcode.emu.unix.EmuUnixUser) -> bool:
        """
        Check if the given user has the requested permissions on the file described by this stat
        @param req the requested permissions
        @param user the user requesting permission
        @return true if permitted, false if denied
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

