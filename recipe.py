from construct import Container
from itertools import compress


def apply(fun, *iterables):
    for args in zip(*iterables):
        fun(*args)

def rev(x):
    if type(x) == str:
        return bytes().fromhex(x.replace(" ", ""))
    else:
        return " ".join(map("{:0>2x}".format, x))

class D2Container(Container):
    def __init__(self, names, nums, index, reformer, i, line):
        Container.__init__(self)
        data = line.strip("\n").split("\t")
        self.__dict__ = (reformer or (lambda x: x))(dict(compress(zip(names, data), nums)))
        if index and data[index] and data[index].isdecimal():
            i = int(data[index])
        elif index:
            i = None
        self.__dict__["_id"] = i

def read_d2_file(fname, fields=None, idname=None, reformer=None):
    with open(fname) as f:
        names = f.readline().strip().replace(" ", "_").split("\t")
        nums = tuple(map(lambda name: name in (fields or names), names))
        index = idname and names.index(idname)
        return tuple(map(lambda x: D2Container(names, nums, index, reformer, *x), enumerate(f)))


if __name__ == "__main__":
    print(read_d2_file("txt\\exp\\cubetype.txt", ("cube_item_class,")))

    print(rev(b'\xa1\xd9\x00(H@\xf0\xb0\x00(k\x06'))
    print(rev(b'\xa1\xe9\x00\x90\xe0\xc80\xb0\x00(\xdc\x02'))
    print(rev(b'\xa1\xd1\x0008\xc8\xe8\xb0\x00\x187\x05'))
    print()
    print(rev(b'!28\xc8\xe8\x00\x00\x00\x00'))
    print(rev(b'!*H@\x00\x00\x00\x00'))
