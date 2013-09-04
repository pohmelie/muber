from construct import *
from recipe import *
from math import log


def _factory(fname, default_fields=None, idn=None, reformer=None):
    lst = None
    class _Adapter(Adapter):
        def _encode(self, obj, ctx):
            return obj._id

        def _decode(self, obj, ctx):
            nonlocal lst
            lst = lst or read_d2_file(fname, default_fields, idn, reformer)
            return lst[obj]
    return _Adapter

D2Attribute = lambda name: _factory("txt\\exp\\ItemStatCost.txt", ("Stat", "ValShift"), "ID")(ULInt8(name))
D2Object = lambda name: _factory("txt\\exp\\objects.txt", ("Name", "description_-_not_loaded"), "Id")(ULInt16(name))
D2Skill = lambda name: _factory("txt\\exp\\skills.txt", ("skill", "charclass"), "Id")(ULInt16(name))
D2Monstat = lambda name: _factory("txt\\exp\\monstats.txt", ("namco", "Type"), "PopulateId")(ULInt16(name))

def D2Montype_reformer(d):
    ifields = ("BL_Dir", "S3_Dir", "GH_Dir", "WL_Dir", "A1_Dir", "DT_Dir",
        "S2_Dir", "A2_Dir", "SC_Dir", "RN_Dir", "S4_Dir", "NU_Dir", "S1_Dir",
        "SQ_Dir", "DD_Dir", "KB_Dir"
    )
    rd = {}
    padding = 0
    for k, v in d.items():
        if k in ifields:
            padding = padding + int(log(int(v), 2))
        else:
            rd[k] = v
    rd["stats_length"] = padding
    return rd

def D2Montype(class_code_name, name):
    f = _factory("txt\\exp\\MonType.txt", None, None, D2Montype_reformer)
    return f(Value(name, lambda ctx: ctx[class_code_name]["_id"]))
