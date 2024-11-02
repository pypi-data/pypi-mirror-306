# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class KernelTypeStrResolver(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = KernelTypeStrResolver()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsKernelTypeStrResolver(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def KernelTypeStrResolverBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4F\x52\x54\x4D", size_prefixed=size_prefixed)

    # KernelTypeStrResolver
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # KernelTypeStrResolver
    def OpKernelTypeStrArgs(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from ort_flatbuffers_py.fbs.OpIdKernelTypeStrArgsEntry import OpIdKernelTypeStrArgsEntry
            obj = OpIdKernelTypeStrArgsEntry()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # KernelTypeStrResolver
    def OpKernelTypeStrArgsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # KernelTypeStrResolver
    def OpKernelTypeStrArgsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def KernelTypeStrResolverStart(builder):
    builder.StartObject(1)

def Start(builder):
    KernelTypeStrResolverStart(builder)

def KernelTypeStrResolverAddOpKernelTypeStrArgs(builder, opKernelTypeStrArgs):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(opKernelTypeStrArgs), 0)

def AddOpKernelTypeStrArgs(builder, opKernelTypeStrArgs):
    KernelTypeStrResolverAddOpKernelTypeStrArgs(builder, opKernelTypeStrArgs)

def KernelTypeStrResolverStartOpKernelTypeStrArgsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartOpKernelTypeStrArgsVector(builder, numElems: int) -> int:
    return KernelTypeStrResolverStartOpKernelTypeStrArgsVector(builder, numElems)

def KernelTypeStrResolverEnd(builder):
    return builder.EndObject()

def End(builder):
    return KernelTypeStrResolverEnd(builder)
