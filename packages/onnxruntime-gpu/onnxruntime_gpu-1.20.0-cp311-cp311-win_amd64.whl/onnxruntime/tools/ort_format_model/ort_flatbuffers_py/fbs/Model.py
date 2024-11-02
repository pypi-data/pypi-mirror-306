# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Model(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Model()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsModel(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def ModelBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4F\x52\x54\x4D", size_prefixed=size_prefixed)

    # Model
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Model
    def IrVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int64Flags, o + self._tab.Pos)
        return 0

    # Model
    def OpsetImport(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from ort_flatbuffers_py.fbs.OperatorSetId import OperatorSetId
            obj = OperatorSetId()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def OpsetImportLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def OpsetImportIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # Model
    def ProducerName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Model
    def ProducerVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Model
    def Domain(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Model
    def ModelVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int64Flags, o + self._tab.Pos)
        return 0

    # Model
    def DocString(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Model
    def Graph(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from ort_flatbuffers_py.fbs.Graph import Graph
            obj = Graph()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def GraphDocString(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Model
    def MetadataProps(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from ort_flatbuffers_py.fbs.StringStringEntry import StringStringEntry
            obj = StringStringEntry()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def MetadataPropsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def MetadataPropsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        return o == 0

def ModelStart(builder):
    builder.StartObject(10)

def Start(builder):
    ModelStart(builder)

def ModelAddIrVersion(builder, irVersion):
    builder.PrependInt64Slot(0, irVersion, 0)

def AddIrVersion(builder, irVersion):
    ModelAddIrVersion(builder, irVersion)

def ModelAddOpsetImport(builder, opsetImport):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(opsetImport), 0)

def AddOpsetImport(builder, opsetImport):
    ModelAddOpsetImport(builder, opsetImport)

def ModelStartOpsetImportVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartOpsetImportVector(builder, numElems: int) -> int:
    return ModelStartOpsetImportVector(builder, numElems)

def ModelAddProducerName(builder, producerName):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(producerName), 0)

def AddProducerName(builder, producerName):
    ModelAddProducerName(builder, producerName)

def ModelAddProducerVersion(builder, producerVersion):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(producerVersion), 0)

def AddProducerVersion(builder, producerVersion):
    ModelAddProducerVersion(builder, producerVersion)

def ModelAddDomain(builder, domain):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(domain), 0)

def AddDomain(builder, domain):
    ModelAddDomain(builder, domain)

def ModelAddModelVersion(builder, modelVersion):
    builder.PrependInt64Slot(5, modelVersion, 0)

def AddModelVersion(builder, modelVersion):
    ModelAddModelVersion(builder, modelVersion)

def ModelAddDocString(builder, docString):
    builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(docString), 0)

def AddDocString(builder, docString):
    ModelAddDocString(builder, docString)

def ModelAddGraph(builder, graph):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(graph), 0)

def AddGraph(builder, graph):
    ModelAddGraph(builder, graph)

def ModelAddGraphDocString(builder, graphDocString):
    builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(graphDocString), 0)

def AddGraphDocString(builder, graphDocString):
    ModelAddGraphDocString(builder, graphDocString)

def ModelAddMetadataProps(builder, metadataProps):
    builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(metadataProps), 0)

def AddMetadataProps(builder, metadataProps):
    ModelAddMetadataProps(builder, metadataProps)

def ModelStartMetadataPropsVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartMetadataPropsVector(builder, numElems: int) -> int:
    return ModelStartMetadataPropsVector(builder, numElems)

def ModelEnd(builder):
    return builder.EndObject()

def End(builder):
    return ModelEnd(builder)
