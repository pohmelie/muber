from construct import *
from d2packetparser_c2s import sid
from recipe import *


d2item_header = Embed(Struct(None,
        Enum(ULInt8("action"),
            lying_on_ground_just_dropped = 0x00,
            picked_up_from_ground_to_cursor = 0x01,
            dropped_by_player = 0x02,
            lying_on_ground = 0x03,
            moved_in_cube_inventory = 0x04,
            put_onto_cursor = 0x05,
            item_on_cursor_was_equipped = 0x06,
            removed_from_equipment_slot = 0x08,
            swap_cursor_slot = 0x09,
            merge_items = 0x0a,
            added_to_shop = 0x0b,
            removed_from_shop = 0x0c,
            swap_cursor_inventory = 0x0d,
            put_into_belt = 0x0e,
            removed_from_belt = 0x0f,
            swap_cursor_belt = 0x10,
            cursor_item_when_entering = 0x12,
            item_is_socketed_into_another = 0x13,
            item_just_inserted_into_another = 0x15,
            equipment_swap = 0x17
        ),
        ULInt8("length_of_packet"),
        Enum(ULInt8("category"),
            helm = 0x00,
            armor = 0x01,
            weapon = 0x05,
            bow = 0x06,
            shield = 0x07,
            other = 0x10
        ),
        sid("item_id"),
    )
)

def extb(d, bita, count=1):
    getb = lambda d, bita: (d[bita >> 3] >> (bita & 7)) & 1
    ret = 0
    while count:
        count = count - 1
        ret = (ret << 1) + getb(d, bita + count)
    return ret

buffers = ("inventory", "body", "belt", "ground", "cursor", "world", "sockets")
containers = ("unspecified", "inventory", "npc_trade", "trade_screen", "horadric_cube", "stash")
qualities = ("unspecified", "inferior", "normal", "superior", "magic", "set", "rare", "unique", "crafted")

def d2item_body_stats_extract(ctx):
    d = ctx.data

    identifiedv = bool(extb(d, 4))
    etherialv = bool(extb(d, 22))
    item_has_no_levelv = bool(extb(d, 21))
    destinationv = buffers[extb(d, 42, 3)]

    shift = 0
    if destinationv == "ground":
        xv = extb(d, 45, 16)
        yv = extb(d, 61, 16)
        contv = containers[0]
        shift = 17
    else:
        xv = extb(d, 49, 4)
        yv = extb(d, 53, 4)
        contv = containers[extb(d, 57, 3)]

    codev = "".join(map(lambda i: chr(extb(d, 60 + shift + 8 * i, 8)), range(3)))
    ilvlv = qualityv = 0
    if codev != "gld" and not item_has_no_levelv:
        qualityv = extb(d, 102 + shift, 4)
        ilvlv = extb(d, 95 + shift, 7)

    return Container(
        etherial = etherialv,
        identified = identifiedv,
        item_has_no_level = item_has_no_levelv,
        destination = destinationv,
        x = xv,
        y = yv,
        container = contv,
        code = codev,
        quality = qualities[qualityv],
        ilvl = ilvlv
    )

d2item_body = Embed(Struct(None,
        Anchor("tail"),
        Bytes("data", lambda ctx: ctx.length_of_packet - (ctx.tail - ctx.start_fun)),
        Value("item", d2item_body_stats_extract)
    )
)
