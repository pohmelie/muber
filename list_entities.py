from construct import *
from recipe import *


entities_list = dict(
    player = 0,
    monster_npc_merc = 1,
    stash_wp_portal_chest = 2,
    missile = 3,
    item = 4,
    entrance = 5,
)
rentities_list = dict(map(reversed, entities_list.items()))

class EntityAdapter(Adapter):
    def _encode(self, obj, context):
        return entities_list.get(obj, obj)

    def _decode(self, obj, context):
        return rentities_list.get(obj, obj)

def Entity(name):
    return EntityAdapter(ULInt8(name))

