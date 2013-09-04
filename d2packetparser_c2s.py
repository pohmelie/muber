from construct import *
from list_d2_files import D2Skill


skills = D2Skill("skill")
sid = lambda name: ULInt32(name)
idpair = lambda name1, name2: Struct(None, sid(name1), sid(name2))
position = Struct(None, ULInt16("x"), ULInt16("y"))

action_to_a_object = Struct(None,
    Enum(ULInt32("object_type"),
        another_player = 0x00,
        town_folk_or_monster = 0x01,
        stash_wp_or_tp = 0x02,
        item = 0x04,
        doorway = 0x05
    ),
    sid("object_id")
)

chat = Struct(None,
    Enum(ULInt8("mode"),
        overhead = 0x00,
        normal = 0x01,
        whisper = 0x02
    ),
    Const(ULInt8(None), 0),
    Embed(Switch(None, lambda ctx: ctx.mode, {
                "overhead":Struct(None, CString("message"), Const(ULInt16(None), 0)),
                "normal":Struct(None, CString("message"), Const(ULInt16(None), 0)),
                "whisper":Struct(None,
                    CString("message"),
                    CString("char_name"),
                    Const(ULInt8(None), 0)
                )
            }
        )
    )
)

body_location = Enum(ULInt16("body_location"),
    head = 0x01,
    neck = 0x02,
    torso = 0x03,
    right_arm = 0x04,
    left_arm = 0x05,
    right_ring = 0x06,
    left_ring = 0x07,
    belt = 0x08,
    feet = 0x09,
    gloves = 0x0a
)

equip_swap = Struct(None,
    sid("object_id"),
    body_location,
    Const(ULInt16(None), 0)
)

npc_buy_sell_repair = Struct(None,
    sid("entity_id"),
    sid("item_id"),
    sid("tab"),
    sid("cost")
)

class GoldAdapter32(Adapter):
    def _encode(self, obj, context):
        return (obj >> 16) + ((obj & 0xffff) << 16)

    def _decode(self, obj, context):
        return (obj >> 16) + ((obj & 0xffff) << 16)

def Gold32(name):
    return GoldAdapter32(ULInt32(name))

speech_id = Enum(ULInt16("speech_id"),
    help_help_me = 0x0019,
    follow_me_come_on = 0x001a,
    this_is_yours_this_is_for_you = 0x001b,
    thanks_thank_you = 0x001c,
    ahh_oops_forgive_me = 0x001d,
    bye_good_bye = 0x001e,
    die_time_to_die = 0x001f,
    run_run_away = 0x0020
)

char_type = Enum(ULInt8("char_type"),
    amazon = 0x00,
    sorceress = 0x01,
    necromancer = 0x02,
    paladin = 0x03,
    barbarian = 0x04,
    druid = 0x05,
    assassin = 0x06
)

c2s_packets = Struct(None,
    Anchor("start_fun"),
    Enum(UBInt8("fun"),
        walk = 0x01,
        walk_to_a_object = 0x02,
        run = 0x03,
        run_to_a_object = 0x04,
        left_skill_on_location = 0x05,
        left_skill_on_object = 0x06,
        shift_left_skill_on_object = 0x07,
        left_skill_on_location_repeat = 0x08,
        left_skill_on_object_repeat = 0x09,
        shift_left_skill_on_object_repeat = 0x0a,
        unknown_0b = 0x0b,
        right_skill_on_location = 0x0c,
        right_skill_on_object = 0x0d,
        shift_right_skill_on_object = 0x0e,
        right_skill_on_location_repeat = 0x0f,
        right_skill_on_object_repeat = 0x10,
        shift_right_skill_on_object_repeat = 0x11,
        unknown_12 = 0x12,
        interact_with_object = 0x13,
        send_overhead_chat = 0x14,
        send_normal_chat = 0x15,
        pick_up_object_from_ground = 0x16,
        drop_object_from_cursor_to_the_ground = 0x17,
        place_object_in_a_location = 0x18,
        pick_up_object_from_storage = 0x19,
        put_on_a_body_item = 0x1a,
        swap_two_handed_item = 0x1b,
        remove_a_body_item = 0x1c,
        replace_a_body_item = 0x1d,
        swap_two_one_handed_with_a_two_handed = 0x1e,
        replace_a_storage_object = 0x1f,
        interact_with_an_inventory_object = 0x20,
        stack_items = 0x21,
        unstack_items = 0x22,
        item_to_belt = 0x23,
        item_from_belt = 0x24,
        switch_belt_item = 0x25,
        use_belt_item = 0x26,
        identify_an_object = 0x27,
        socket_item = 0x28,
        scroll_to_book = 0x29,
        object_to_cube = 0x2a,
        finalize_town_folk_interaction_request = 0x2f,
        cancel_town_folk_interaction = 0x30,
        quest_message = 0x31,
        buy_item_from_npc = 0x32,
        sell_item_to_npc = 0x33,
        identify_item_with_npc = 0x34,
        repair = 0x35,
        hire_merc = 0x36,
        identify_from_gamble = 0x37,
        town_folk_interaction_selection = 0x38,
        purchase_life = 0x39,
        add_stat_point = 0x3a,
        add_skill_point = 0x3b,
        select_skill = 0x3c,
        highlight_a_door = 0x3d,
        activate_scroll_of_inifuss = 0x3e,
        send_char_speech = 0x3f,
        request_quest_log = 0x40,
        resurrect = 0x41,
        staff_in_orifice = 0x44,
        change_tp_location = 0x45,
        merc_interact = 0x46,
        move_merc = 0x47,
        turns_off_busy_state = 0x48,
        waypoint_interaction = 0x49,
        bring_merc_wp_tp = 0x4b,
        transmorgify = 0x4c,
        npc_speech = 0x4d,
        button_click = 0x4f,
        drop_gold = 0x50,
        bind_hotkey_to_skill = 0x51,
        turn_stamina_on = 0x53,
        turn_stamina_off = 0x54,
        quest_complete = 0x58,
        register_town_folk_interaction = 0x59,
        set_player_relations = 0x5d,
        party_request = 0x5e,
        update_player_position = 0x5f,
        swap_weapons = 0x60,
        merc_item_action = 0x61,
        resurrect_merc = 0x62,
        object_to_belt = 0x63,
        send_logon_info = 0x68,
        exit_game = 0x69,
        enter_game = 0x6b,
        ping = 0x6d,
        _default_ = "unknown"
    ),
    Embed(Switch(None, lambda ctx: ctx.fun, {
                "walk":position,
                "walk_to_a_object":action_to_a_object,
                "run":position,
                "run_to_a_object":action_to_a_object,
                "left_skill_on_location":position,
                "left_skill_on_object":action_to_a_object,
                "shift_left_skill_on_object":action_to_a_object,
                "left_skill_on_location_repeat":position,
                "left_skill_on_object_repeat":action_to_a_object,
                "shift_left_skill_on_object_repeat":action_to_a_object,
                "unknown_0b":Struct(None, Pass),
                "right_skill_on_location":position,
                "right_skill_on_object":action_to_a_object,
                "shift_right_skill_on_object":action_to_a_object,
                "right_skill_on_location_repeat":position,
                "right_skill_on_object_repeat":action_to_a_object,
                "shift_right_skill_on_object_repeat":action_to_a_object,
                "unknown_12":Struct(None, Pass),
                "interact_with_object":action_to_a_object,
                "send_overhead_chat":chat,
                "send_normal_chat":chat,
                "pick_up_object_from_ground":Struct(None,
                    sid("request_id"),
                    sid("object_id"),
                    Enum(ULInt32("object_direction"),
                        to_inventory = 0x00,
                        to_cursor = 0x01
                    )
                ),
                "drop_object_from_cursor_to_the_ground":Struct(None, sid("object_id")),
                "place_object_in_a_location":Struct(None,
                    sid("object_id"),
                    ULInt32("x"),
                    ULInt32("y"),
                    Enum(ULInt32("object_direction"),
                        inventory = 0x00,
                        trade = 0x02,
                        cube = 0x03,
                        stash = 0x04
                    )
                ),
                "pick_up_object_from_storage":Struct(None, sid("object_id")),
                "put_on_a_body_item":equip_swap,
                "swap_two_handed_item":equip_swap,
                "remove_a_body_item":Struct(None, body_location),
                "replace_a_body_item":equip_swap,
                "swap_two_one_handed_with_a_two_handed":equip_swap,
                "replace_a_storage_object":Struct(None,
                    sid("new_object_id"),
                    sid("old_object_id"),
                    ULInt32("x"),
                    ULInt32("y")
                ),
                "interact_with_an_inventory_object":Struct(None,
                    sid("object_id"),
                    ULInt32("x"),
                    ULInt32("y")
                ),
                "stack_items":idpair("item_to_stack_id", "item_where_it_stacks_id"),
                "unstack_items":Struct(None, sid("object_id")),
                "item_to_belt":Struct(None,
                    sid("object_id"),
                    ULInt32("belt_slot_number")
                ),
                "item_from_belt":Struct(None, sid("object_id")),
                "switch_belt_item":idpair("old_item_id", "new_item_id"),
                "use_belt_item":Struct(None,
                    sid("object_id"),
                    ULInt32("shift_key_state"),
                    ULInt32("unknown"),
                ),
                "identify_an_object":idpair("object_id", "scroll_id"),
                "socket_item":idpair("item_to_socket_id", "socketable_item_id"),
                "scroll_to_book":idpair("scroll_id", "book_id"),
                "object_to_cube":idpair("object_id", "cube_id"),
                "finalize_town_folk_interaction_request":idpair("request_id", "town_folks_id"),
                "cancel_town_folk_interaction":idpair("request_id", "town_folks_id"),
                "quest_message":idpair("id", "message"),
                "buy_item_from_npc":npc_buy_sell_repair,
                "sell_item_to_npc":npc_buy_sell_repair,
                "identify_item_with_npc":Struct(None, sid("entity_id")),
                "repair":npc_buy_sell_repair,
                "hire_merc":idpair("entity_id", "merc_id"),
                "identify_from_gamble":Struct(None, sid("item_id")),
                "town_folk_interaction_selection":Struct(None,
                    Enum(sid("request_id"),
                        imbue = 0x00,
                        trade = 0x01,
                        gamble = 0x02
                    ),
                    sid("town_folk_id"),
                    ULInt32("unknown")
                ),
                "purchase_life":Struct(None, sid("npc_id")),
                "add_stat_point":Struct(None, ULInt16("stat_id")),
                "add_skill_point":Struct(None, skills),
                "select_skill":Struct(None,
                    skills,
                    Enum(ULInt16("skill_side"),
                        right = 0x0000,
                        left = 0x8000
                    ),
                    ULInt32("unknown")
                ),
                "highlight_a_door":Struct(None, sid("object_id")),
                "activate_scroll_of_inifuss":Struct(None, sid("object_id")),
                "send_char_speech":Struct(None, speech_id),
                "request_quest_log":Struct(None, Pass),
                "resurrect":Struct(None, Pass),
                "staff_in_orifice":Struct(None,
                    ULInt32("orifice_entity_kind"),
                    sid("orifice_id"),
                    sid("staff_id"),
                    ULInt32("entity_state")
                ),
                "change_tp_location":idpair("entity_id", "location_id"),
                "merc_interact":Struct(None,
                    sid("merc_id"),
                    sid("entity_id"),
                    ULInt32("entity_type")
                ),
                "move_merc":Struct(None,
                    sid("merc_id"),
                    ULInt32("x"),
                    ULInt32("y")
                ),
                "turns_off_busy_state":Struct(None, Pass),
                "waypoint_interaction":Struct(None,
                    sid("waypoint_id"),
                    Enum(sid("area_id"),
                        close_menu = 0x00,

                        rogue_encampment = 0x01,
                        cold_plains = 0x03,
                        stony_fields = 0x04,
                        dark_wood = 0x05,
                        black_marsh = 0x06,
                        outer_cloister = 0x1b,
                        jail_level_1 = 0x1d,
                        inner_cloister = 0x20,
                        catacombs_level_2 = 0x23,

                        lut_gholein = 0x28,
                        sewers_level_2 = 0x30,
                        dry_hills = 0x2a,
                        halls_of_dead_level_2 = 0x39,
                        far_oasis = 0x2b,
                        lost_city = 0x2c,
                        palace_cellar_level_1 = 0x34,
                        arcain_sanctuary = 0x4a,
                        canyon_of_the_magi = 0x2e,

                        kurast_docks = 0x4b,
                        spider_forest = 0x4c,
                        great_marsh = 0x4d,
                        flayer_jungle = 0x4e,
                        lower_kurast = 0x4f,
                        kurast_bazaar = 0x50,
                        upper_kurast = 0x51,
                        travincal = 0x53,
                        durance_of_hate_level_2 = 0x65,

                        the_pandeminoum_fortress = 0x67,
                        city_of_damned = 0x6a,
                        river_of_flame = 0x6b,

                        harrogath = 0x6d,
                        frigid_highlands = 0x6f,
                        arreat_plateau = 0x70,
                        crystalline_passage = 0x71,
                        glacial_trail = 0x73,
                        halls_of_pain = 0x7b,
                        frozen_tundra = 0x75,
                        the_ancients_way = 0x76,
                        worldstone_keep_level_2 = 0x81
                    )
                ),
                "bring_merc_wp_tp":Struct(None,
                    sid("player_type"),
                    sid("merc_id")
                ),
                "transmorgify":Struct(None, sid("object_id")),
                "npc_speech":Struct(None, ULInt16("sound_id")),
                "button_click":Struct(None,
                    Enum(ULInt16("request_id"),
                        cancel_trade = 0x02,
                        accept_trade = 0x03,
                        press_accept = 0x04,
                        unclick_accept = 0x07,
                        refresh = 0x08,
                        close_stash = 0x12,
                        gold_from_stash_to_inventory = 0x13,
                        gold_from_inventory_to_stash = 0x14,
                        close_cube = 0x17,
                        press_transmute = 0x18
                    ),
                    Gold32("gold")
                ),
                "drop_gold":Struct(None,
                    sid("player_id"),
                    ULInt32("gold")
                ),
                "bind_hotkey_to_skill":Struct(None,
                    ULInt8("skill_id"),
                    Enum(ULInt8("side"),
                        right = 0x00,
                        left = 0x80
                    ),
                    ULInt16("hotkey"),
                    Const(ULInt32(None), 0xffffffff)
                ),
                "turn_stamina_on":Struct(None, Pass),
                "turn_stamina_off":Struct(None, Pass),
                "quest_complete":Struct(None, ULInt16("quest_id")),
                "register_town_folk_interaction":Struct(None,
                    sid("request_id"),
                    sid("town_folk_id"),
                    ULInt32("x"),
                    ULInt32("y")
                ),
                "set_player_relations":Struct(None,
                    ULInt8("request_id"),
                    Embed(Switch(None, lambda ctx: ctx.request_id, {
                            0x01:Struct(None, Enum(ULInt8("action_type"),
                                loot_off = 0x00,
                                loot_on = 0x01
                            )),
                            0x02:Struct(None, Enum(ULInt8("action_type"),
                                hear_on = 0x00,
                                hear_off = 0x01
                            )),
                            0x03:Struct(None, Enum(ULInt8("action_type"),
                                squelch_off = 0x00,
                                squelch_on = 0x01
                            )),
                            0x04:Struct(None, Enum(ULInt8("action_type"),
                                hostile_off = 0x00,
                                hostile_on = 0x01
                            ))
                        }
                    )),
                    sid("player_id")
                ),
                "party_request":Struct(None,
                    Enum(ULInt8("action_type"),
                        invite = 0x06,
                        cancel = 0x07,
                        accept = 0x08
                    ),
                    sid("player_id")
                ),
                "update_player_position":Struct(None,
                    ULInt16("x"),
                    ULInt16("y")
                ),
                "swap_weapons":Struct(None, Pass),
                "merc_item_action":Struct(None,
                    Enum(ULInt16("action"),
                        put = 0x00,
                        get_helm = 0x01,
                        get_shield = 0x02,
                        get_body = 0x03,
                        get_weapon = 0x04
                    )
                ),
                "resurrect_merc":Struct(None, sid("npc_id")),
                "object_to_belt":Struct(None, sid("object_id")),
                "send_logon_info":Struct(None,
                    ULInt32("d2gs_hash"),
                    ULInt16("d2gs_token"),
                    char_type,
                    ULInt32("version"),
                    Const(ULInt32(None), 0xED5DCC50),
                    Const(ULInt32(None), 0x91A519B6),
                    Const(ULInt8(None), 0),
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name))
                ),
                "exit_game":Struct(None, Pass),
                "enter_game":Struct(None, Pass),
                "ping":Struct(None,
                    ULInt32("tickcount"),
                    ULInt32("delay"),
                    ULInt32("warden_response")
                )
            },
            default = Struct(None,
                Pointer(lambda ctx: ctx.start_fun, HexDumpAdapter(GreedyRange(ULInt8("data")))),
                GreedyRange(ULInt8(None))
            )
        )
    )
)

if __name__ == "__main__":
    data = b'''\x01\x87\x58\x63\x1a\x02\x02\x00\x00\x00\x18\x00\x00\x00\x06\x01\
\x00\x00\x00\x1e\x00\x00\x00\x0b\x15\x01\x00\x79\x6f\x62\x61\x00\x00\x00\x14\
\x00\x00\x79\x6f\x62\x61\x00\x00\x00\x16\x04\x00\x00\x00\x2e\x00\x00\x00\x00\
\x00\x00\x00\x1a\x2c\x00\x00\x00\x04\x00\x00\x00\x4f\x14\x00\x02\x00\xf0\x49\
\x50\x01\x00\x00\x00\x01\x00\x00\x00\x51\x40\x80\x05\x00\xff\xff\xff\xff\x5d\
\x04\x01\x01\x00\x00\x00\x61\x01\x00\x68\xD3\xB0\xB5\x2C\xD9\x03\x04\x0B\x00\
\x00\x00\x50\xCC\x5D\xED\xB6\x19\xA5\x91\x00\x72\x74\x74\x74\x68\x65\x61\x68\
\x65\x61\x68\x65\x61\x68\x72\x00\x68\xe9\xeb\x17\x20\x95\x02\x01\x65\x00\x00\
\x00\x50\xcc\x5d\xed\xb6\x19\xa5\x91\x00\x62\x72\x6f\x6f\x6d\x72\x69\x64\x65\
\x72\x00\x4b\x00\x00\x00\x00\x68\x93\xe5\x6c\x62\xa2\x03\x00\x65\x00\x00\x00\
\x50\xcc\x5d\xed\xb6\x19\xa5\x91\x00\x70\x6d\x61\x61\x00\x36\x7e\x3a\x18\xae\
\x6f\x4b\x00\x00\x00\x00\x68\xcc\xd5\xbd\x66\xe7\x03\x00\x0d\x00\x00\x00\x50\
\xcc\x5d\xed\xb6\x19\xa5\x91\x00\x70\x6d\x61\x61\x00\x36\x7e\x6a\x39\xaf\x6f\
\x4b\x00\x00\x00\x00\xff\xfe\xfd\xff\xfe\xfd\xff\xfe\xfd\xff\xfe\xfd'''
    c2s = OptionalGreedyRange(c2s_packets)
    print(c2s.parse(data))
