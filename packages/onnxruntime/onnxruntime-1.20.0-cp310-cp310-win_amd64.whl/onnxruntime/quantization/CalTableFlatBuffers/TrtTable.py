# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CalTableFlatBuffers

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class TrtTable:
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAs(cls, buf, offset=0):  # noqa: N802
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TrtTable()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsTrtTable(cls, buf, offset=0):  # noqa: N802
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)

    # TrtTable
    def Init(self, buf, pos):  # noqa: N802
        self._tab = flatbuffers.table.Table(buf, pos)

    # TrtTable
    def Dict(self, j):  # noqa: N802
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from onnxruntime.quantization.CalTableFlatBuffers.KeyValue import KeyValue

            obj = KeyValue()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TrtTable
    def DictLength(self):  # noqa: N802
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TrtTable
    def DictIsNone(self):  # noqa: N802
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0


def Start(builder):  # noqa: N802
    builder.StartObject(1)


def TrtTableStart(builder):  # noqa: N802
    """This method is deprecated. Please switch to Start."""
    return Start(builder)


def AddDict(builder, dict):  # noqa: N802
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(dict), 0)


def TrtTableAddDict(builder, dict):  # noqa: N802
    """This method is deprecated. Please switch to AddDict."""
    return AddDict(builder, dict)


def StartDictVector(builder, numElems):  # noqa: N802
    return builder.StartVector(4, numElems, 4)


def TrtTableStartDictVector(builder, numElems):  # noqa: N802
    """This method is deprecated. Please switch to Start."""
    return StartDictVector(builder, numElems)


def End(builder):  # noqa: N802
    return builder.EndObject()


def TrtTableEnd(builder):  # noqa: N802
    """This method is deprecated. Please switch to End."""
    return End(builder)
