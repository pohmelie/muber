from construct import *
from d2packetparser_c2s import sid, char_type
from d2packetparser_items import *
from list_entities import Entity
from list_chat_colors import Color
from list_d2_files import D2Attribute, D2Object, D2Skill, D2Monstat, D2Montype


object_class_code = D2Object("entity_class_code")
skills = D2Skill("skill")
attr_code = D2Attribute("attribute")
entity_type = Entity("entity_type")
color = Color("color")

def xy16(pre=""):
    pre = pre and pre + "_"
    return Embed(Struct(None,
            ULInt16(pre + "x"),
            ULInt16(pre + "y")
        )
    )

def etype_eid(pre=""):
    pre = pre and pre + "_"
    return Embed(Struct(None,
            Entity(pre + "entity_type"),
            #ULInt8(pre + "entity_type"),
            sid(pre + "entity_id")
        )
    )

map_add_rem = Struct(None,
    xy16(),
    ULInt8("area_id")
)

s2c_packets = Struct(None,
    Anchor("start_fun"),
    Enum(UBInt8("fun"),
        setup = 0x01,
        load_successful = 0x02,
        seed = 0x03,
        enter_game = 0x04,
        unload_complete = 0x05,
        game_exit = 0x06,
        map_add = 0x07,
        map_rem = 0x08,
        door_assign = 0x09,
        lost_sight = 0x0a,
        handshake = 0x0b,
        show_dmg = 0x0c,
        action_effect = 0x0d,
        object_state = 0x0e,
        entity_move = 0x0f,
        entity_to_entity = 0x10,
        report_kill = 0x11,
        reassign = 0x15,
        pot = 0x18,
        gold_byte = 0x19,
        exp_byte = 0x1a,
        exp_word = 0x1b,
        exp_dword = 0x1c,
        attr_byte = 0x1d,
        attr_word = 0x1e,
        attr_dword = 0x1f,
        player_attr = 0x20,
        update_item_oskill = 0x21,
        skill_book_count = 0x22,
        skill_select = 0x23,
        chat = 0x26,
        npc_interact = 0x27,
        quest_tree = 0x28,
        game_quest_info = 0x29,
        npc_transaction = 0x2a,
        sound = 0x2c,
        update_item_stats = 0x3e,
        use_stackable_item = 0x3f,
        mouse_clear = 0x42,
        relator_1 = 0x47,
        relator_2 = 0x48,
        entity_attack_entity = 0x4c,
        entity_attack_location = 0x4d,
        merc_for_hire = 0x4e,
        stat_merc_list = 0x4f,
        object_assign = 0x51,
        quest_log_info = 0x52,
        game_refresh = 0x53,
        player_assign = 0x59,
        event_notify = 0x5a,
        player_in_game = 0x5b,
        player_quit_game = 0x5c,
        tele_state = 0x60,
        wp_state = 0x63,
        kill_count = 0x65,
        npc_move = 0x67,
        npc_to_target = 0x68,
        npc_state_assign = 0x69,
        npc_action = 0x6b,
        npc_attack = 0x6c,
        npc_stop = 0x6d,
        about_player = 0x75,
        overhead_clear = 0x76,
        trade = 0x77,
        who_trade = 0x78,
        gold_trade = 0x79,
        summon_log = 0x7a,
        bind_skill_to_hotkey = 0x7b,
        use_item = 0x7c,
        party_update = 0x7f,
        merc_owner = 0x81,
        tele_owner = 0x82,
        quest_event = 0x89,
        entity_request_chat = 0x8a,
        party_invite_status = 0x8b,
        player_relationship = 0x8c,
        party_number = 0x8d,
        corpse_assign = 0x8e,
        pong = 0x8f,
        party_pulse = 0x90,
        skill_log = 0x94,
        resources = 0x95,
        walk_verify = 0x96,
        weapon_switch = 0x97,
        skill_triggered = 0x99,
        merc_attr_byte = 0x9e,
        merc_attr_word = 0x9f,
        merc_attr_dword = 0xa0,
        merc_attr_add_byte = 0xa1,
        merc_attr_add_word = 0xa2,
        baal_spawn = 0xa4,
        aura_effect = 0xa7,
        set_state = 0xa8,
        end_state = 0xa9,
        entity_info_add = 0xaa,
        entity_heal = 0xab,
        npc_assign = 0xac,
        warden = 0xae,
        compression = 0xaf,
        game_termination = 0xb0,
        timeout_full = 0xb4,
        stats_confirmation = 0xcb,
        movement_confirmation = 0xcc,

        #item actions
        world_item_action = 0x9c,
        owner_item_action = 0x9d,

        #unknown, but length
        unknown_0x50 = 0x50,
        unknown_0x5e = 0x5e,
        unknown_0x5f = 0x5f,
        unknown_0x7e = 0x7e,
        unknown_0x91 = 0x91,
        unknown_0xa5 = 0xa5,
        unknown_0xc1 = 0xc1,
        unknown_0xca = 0xca,

        _default_ = "unknown"
    ),
    Embed(Switch(None, lambda ctx: ctx.fun, {
                "setup":Struct(None,
                    Enum(ULInt8("difficulty"),
                        normal = 0x00,
                        nightmare = 0x01,
                        hell = 0x02
                    ),
                    Const(ULInt8(None), 0x04),
                    Enum(ULInt8("diff_core_flag"),
                        hardcore = 0x08,
                        nightmare = 0x10,
                        hell = 0x20
                    ),
                    Enum(ULInt16("ladder_expo_flag"),
                        lod = 0x10,
                        ladder = 0x20
                    ),
                    Enum(ULInt8("expo"),
                        classic = 0x00,
                        lod = 0x01
                    ),
                    Enum(ULInt16("ladder"),
                        no = 0x00,
                        yes = 0x01
                    )
                ),
                "load_successful":Struct(None, Pass),
                "seed":Struct(None,
                    ULInt8("act"),
                    ULInt32("seed_1"),
                    ULInt16("area_id"),
                    ULInt32("seed_2")
                ),
                "enter_game":Struct(None, Pass),
                "unload_complete":Struct(None, Pass),
                "game_exit":Struct(None, Pass),
                "map_add":map_add_rem,
                "map_rem":map_add_rem,
                "door_assign":Struct(None,
                    etype_eid(),
                    ULInt8("side"),
                    ULInt16("x"),
                    ULInt16("y")
                ),
                "lost_sight":Struct(None, etype_eid()),
                "handshake":Struct(None, etype_eid()),
                "show_dmg":Struct(None,
                    etype_eid(),
                    ULInt8("effect_state"),
                    ULInt8("sfx"),
                    ULInt8("life_percent")
                ),
                "action_effect":Struct(None,
                    etype_eid(),
                    ULInt8("effect_state"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("graphic_sound_code")
                ),
                "object_state":Struct(None,
                    etype_eid(),
                    Const(ULInt8(None), 0x03),
                    Flag("changeable"),
                    ULInt32("entity_state")
                ),
                "entity_move":Struct(None,
                    etype_eid(),
                    ULInt8("movement_type"),
                    xy16("going_to"),
                    ULInt8("knockback"),
                    xy16("going_from")
                ),
                "entity_to_entity":Struct(None,
                    etype_eid(),
                    ULInt8("movement_type"),
                    etype_eid("going_to"),
                    xy16()
                ),
                "report_kill":Struct(None,
                    etype_eid(),
                    ULInt16("killed_by")
                ),
                "reassign":Struct(None,
                    etype_eid(),
                    xy16(),
                    Flag("reassign")
                ),
                "pot":BitStruct(None,
                    BitField("life", 15),
                    BitField("mana", 15),
                    BitField("stamina", 15),
                    BitField("x", 15),
                    BitField("unknown1", 1),
                    BitField("y", 15),
                    BitField("unknown2", 36),
                ),
                "gold_byte":Struct(None, ULInt8("amount")),
                "exp_byte":Struct(None, ULInt8("amount")),
                "exp_word":Struct(None, ULInt16("amount")),
                "exp_dword":Struct(None, ULInt32("amount")),
                "attr_byte":Struct(None, attr_code, ULInt8("amount")),
                "attr_word":Struct(None, attr_code, ULInt16("amount")),
                "attr_dword":Struct(None, attr_code, ULInt32("amount")),
                "player_attr":Struct(None,
                    ULInt32("player_id"),
                    attr_code,
                    ULInt32("amount")
                ),
                "update_item_oskill":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("base_level"),
                    ULInt8("bonus_amount"),
                    ULInt8("unknown2")
                ),
                "skill_book_count":Struct(None,
                    entity_type,
                    #ULInt8("entity_type"),
                    ULInt8("unknown1"),
                    ULInt32("entity_id"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("stats_amount"),
                    ULInt16("unknown2")
                ),
                "skill_select":Struct(None,
                    etype_eid(),
                    Enum(ULInt8("skill_side"),
                        right = 0x00,
                        left = 0x01
                    ),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt32("unknown")
                ),
                "chat":Struct(None,
                    Enum(ULInt16("chat_type"),
                        open_chat = 0x01,
                        recv_whisp = 0x02,
                        system = 0x04,
                        overhead = 0x05,
                        sent_whisp = 0x06,
                    ),
                    etype_eid(),
                    color,
                    ULInt8("char_level"),
                    CString("char_name"),
                    CString("message")
                ),
                "npc_interact":Struct(None,
                    etype_eid(),
                    Bytes("unknown", 34)
                ),
                "quest_tree":Struct(None, Bytes("quest_info", 103 - 1)),
                "game_quest_info":Struct(None, Bytes("quest_info", 97 - 1)),
                "npc_transaction":Struct(None,
                    ULInt8("trade_type"),
                    ULInt8("result"),
                    ULInt32("unknown"),
                    sid("npc_id"),
                    ULInt32("gold_in_inventory")
                ),
                "sound":Struct(None, etype_eid(), ULInt16("sound_id")),
                "update_item_stats":Struct(None, Bytes("data", 34 - 1)),
                "use_stackable_item":Struct(None,
                    ULInt8("unknown1"),
                    sid("item_entity_id"),
                    ULInt16("unknown2")
                ),
                "mouse_clear":Struct(None, etype_eid()),
                "relator_1":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    ULInt32("unknown2")
                ),
                "relator_2":Struct(None,
                    ULInt16("unknown1"),
                    sid("entity_id"),
                    ULInt32("unknown2")
                ),
                "entity_attack_entity":Struct(None,
                    etype_eid("attacker"),
                    #ULInt16("skill_code"),
                    skills,
                    ULInt8("skill_level"),
                    etype_eid("defender"),
                    Const(ULInt16(None), 0x00)
                ),
                "entity_attack_location":Struct(None,
                    etype_eid(),
                    #ULInt16("skill_code"),
                    skills,
                    Const(ULInt16(None), 0x00),
                    ULInt8("skill_level"),
                    xy16(),
                    Const(ULInt16(None), 0x00)
                ),
                "merc_for_hire":Struct(None,
                    ULInt16("merc_id"),
                    ULInt32("unknown")
                ),
                "stat_merc_list":Struct(None, Pass),
                "object_assign":Struct(None,
                    etype_eid(),
                    object_class_code,
                    xy16(),
                    ULInt8("state"),
                    ULInt8("interaction"),
                ),
                "quest_log_info":Struct(None, Bytes("data", 42 - 1)),
                "game_refresh":Struct(None,
                    ULInt32("possible_player_slot"),
                    ULInt8("some_boolean"),
                    ULInt32("some_counter")
                ),
                "player_assign":Struct(None,
                    sid("player_id"),
                    char_type,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    xy16()
                ),
                "event_notify":Struct(None,
                    Enum(ULInt8("event"),
                        dropped_due_timeout = 0x00,
                        dropped_due_errors = 0x01,
                        joined_the_game = 0x02,
                        quit_the_game = 0x03,
                        not_in_the_game = 0x04,
                        not_logged_in_the_game = 0x05,
                        was_slain = 0x06,
                        player_relations = 0x07,
                        busy = 0x08,
                        wait_a_short_time = 0x09,
                        item_in_box = 0x0a,
                        not_listenning_you = 0x0d,
                        not_enough_mana = 0x0e,
                        realm_goind_down = 0x0f,
                        wait_before_host = 0x10,
                        soj_sold = 0x11,
                        diablo_walks = 0x12
                    ),
                    Enum(ULInt8("action"),
                        neutral = 0x00,
                        teaming = 0x02,
                        friendly = 0x04,
                        nasty = 0x08,
                        remove = 0x09
                    ),
                    sid("some_number_or_id"),
                    entity_type,
                    #ULInt8("entity_type"),
                    CString("A"),
                    Bytes("_unused1", lambda ctx: 15 - len(ctx.A)),
                    CString("B"),
                    Bytes("_unused2", lambda ctx: 15 - len(ctx.B)),
                ),
                "player_in_game":Struct(None,
                    ULInt16("pack_len"),
                    sid("player_id"),
                    char_type,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    ULInt16("char_level"),
                    ULInt16("party_number"),
                    Padding(lambda ctx: ctx.pack_len - 28)
                ),
                "player_quit_game":Struct(None, sid("player_sid")),
                "tele_state":Struct(None,
                    Enum(ULInt8("state"),
                        unused_town_area = 0x00,
                        unused_area = 0x03,
                        used_town_area = 0x05,
                        used_area = 0x07
                    ),
                    ULInt8("area_id"),
                    sid("teleport_id")
                ),
                "wp_state":Struct(None,
                    sid("wp_id"),
                    Const(ULInt16(None), 0x0102),
                    Bytes("wp_avaliblity", 14)
                ),
                "kill_count":Struct(None,
                    sid("entity_id"),
                    ULInt16("count")
                ),
                "npc_move":Struct(None,
                    sid("npc_id"),
                    ULInt8("movement_type"),
                    xy16(),
                    Bytes("unknown", 6)
                ),
                "npc_to_target":Struct(None,
                    sid("npc_id"),
                    ULInt8("movement_type"),
                    xy16(),
                    etype_eid("target"),
                    Bytes("unknown", 6)
                ),
                "npc_state_assign":Struct(None,
                    sid("npc_id"),
                    ULInt8("npc_state"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("unknown")
                ),
                "npc_action":Struct(None,
                    sid("npc_id"),
                    ULInt8("action_type"),
                    Const(Bytes(None, 6), b"\x00\x00\x00\x00\x00\x00"),
                    xy16()
                ),
                "npc_attack":Struct(None,
                    sid("npc_id"),
                    #ULInt16("skill_code"),
                    skills,
                    etype_eid("defender"),
                    xy16()
                ),
                "npc_stop":Struct(None,
                    sid("npc_id"),
                    xy16(),
                    ULInt8("life_percent")
                ),
                "about_player":Struct(None,
                    sid("player_id"),
                    ULInt16("party_id"),
                    ULInt16("char_level"),
                    ULInt16("relationship_flag"),
                    Flag("in_your_party"),
                    Const(ULInt8(None), 0)
                ),
                "overhead_clear":Struct(None, etype_eid()),
                "trade":Struct(None, ULInt8("button_action")),
                "who_trade":Struct(None,
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    sid("player_id")
                ),
                "gold_trade":Struct(None,
                    Flag("verifyed"),
                    ULInt32("amount")
                ),
                "summon_log":Struct(None,
                    Enum(ULInt8("action"),
                        remove = 0x00,
                        add = 0x01
                    ),
                    ULInt8("skill_number"),
                    ULInt16("summoned_class"),
                    sid("player_id"),
                    sid("summoned_id")
                ),
                "bind_skill_to_hotkey":Struct(None,
                    ULInt8("slot"),
                    ULInt8("skill"),
                    ULInt8("side"),
                    Const(ULInt32(None), 0xffffffff)
                ),
                "use_item":Struct(None,
                    ULInt8("type"),
                    sid("item_id")
                ),
                "party_update":Struct(None,
                    entity_type,
                    #ULInt8("entity_type"),
                    ULInt16("life_percent"),
                    sid("entity_id"),
                    ULInt16("area_id")
                ),
                "merc_owner":Struct(None,
                    Const(ULInt16(None), 0x5207),
                    etype_eid(),
                    sid("merc_id"),
                    ULInt32("unknown1"),
                    ULInt32("unknown2")
                ),
                "tele_owner":Struct(None,
                    sid("player_owner_id"),
                    CString("char_name"),
                    #Padding(lambda ctx: 15 - len(ctx.char_name))
                    Bytes("_unused", lambda ctx: 15 - len(ctx.char_name)),
                    sid("tp_id_your_side"),
                    sid("tp_id_other_side")
                ),
                "quest_event":Struct(None, ULInt8("event_id")),
                "entity_request_chat":Struct(None, etype_eid()),
                "party_invite_status":Struct(None,
                    sid("player_id"),
                    ULInt8("relation_status")
                ),
                "player_relationship":Struct(None,
                    sid("player_id_1"),
                    sid("player_id_2"),
                    ULInt16("relationship_flag")
                ),
                "party_number":Struct(None,
                    sid("player_id"),
                    ULInt16("party_number")
                ),
                "corpse_assign":Struct(None,
                    Enum(ULInt8("event"),
                        remove = 0x00,
                        add = 0x01
                    ),
                    sid("player_id"),
                    sid("corpse_id")
                ),
                "pong":Struct(None, Bytes("server_response", 32)),
                "party_pulse":Struct(None,
                    sid("player_id"),
                    ULInt32("mini_map_x"),
                    ULInt32("mini_map_y")
                ),
                "skill_log":Struct(None,
                    ULInt8("count"),
                    sid("player_id"),
                    Array(lambda ctx: ctx.count, Struct("skill",
                            #ULInt16("skill_code"),
                            skills,
                            ULInt8("skill_level")
                        )
                    )
                ),
                "resources":BitStruct(None,
                    BitField("life", 15),
                    BitField("mana", 15),
                    BitField("stamina", 15),
                    BitField("x", 15),
                    BitField("unknown1", 1),
                    BitField("y", 15),
                    BitField("unknown2", 20),
                ),
                "walk_verify":BitStruct(None,
                    BitField("stamina", 15),
                    BitField("location_x", 15),
                    BitField("unknown1", 1),
                    BitField("location_y", 15),
                    BitField("unknonw2", 18)
                ),
                "weapon_switch":Struct(None, Pass),
                "skill_triggered":Struct(None, Bytes("data", 16 - 1)),
                "merc_attr_byte":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt8("amount")
                ),
                "merc_attr_word":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt16("amount")
                ),
                "merc_attr_dword":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt32("amount")
                ),
                "merc_attr_add_byte":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt8("amount")
                ),
                "merc_attr_add_word":Struct(None,
                    attr_code,
                    sid("merc_id"),
                    ULInt16("amount")
                ),
                "baal_spawn":Struct(None, ULInt16("uniq_code_class")),
                "aura_effect":Struct(None, etype_eid(), ULInt8("effect_code")),
                "set_state":Struct(None,
                    etype_eid(),
                    ULInt8("length_of_packet"),
                    ULInt8("state"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 7)
                ),
                "end_state":Struct(None, etype_eid(), ULInt8("state")),
                "entity_info_add":Struct(None,
                    etype_eid(),
                    ULInt8("length_of_packet"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 6)
                ),
                "entity_heal":Struct(None, etype_eid(), ULInt8("life_percent")),
                "npc_assign":Struct(None,
                    sid("npc_id"),
                    D2Monstat("npc_class_code"),
                    D2Montype("npc_class_code", "npc_type"),
                    xy16(),
                    ULInt8("life_percent"),
                    ULInt8("length_of_packet"),
#                    LBitStruct("info",
#                        LNibble("animation_mode"),
#                        Flag("section2_exists"),
#                        If(lambda ctx: ctx["section2_exists"],
#                            LBitField("npc_stats", lambda ctx: ctx["_"]["npc_type"]["stats_length"])
#                        ),
#                        Flag("section3_exists"),
#                        If(lambda ctx: ctx["section3_exists"],
#                            Struct("npc_flags",
#                                Flag("champion"),
#                                Flag("unique"),
#                                Flag("super_unique"),
#                                Flag("minion"),
#                                Flag("ghostly")
#                            )
#                        ),
#                        Padding(2),
#                    )
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 12)
                ),
                "warden":Struct(None,
                    ULInt8("length_of_packet"),
                    Bytes("stats_list", lambda ctx: ctx.length_of_packet - 1 - 1)
                ),
                "compression":Struct(None, Flag("active")),
                "game_termination":Struct(None, Pass),
                "timeout_full":Struct(None, Enum(ULInt32("reason"),
                        bad_char_version = 0x01,
                        bad_char_quest_data = 0x02,
                        bad_char_wp_data = 0x03,
                        bad_char_stats_data = 0x04,
                        bad_char_skill_data = 0x05,
                        unable_to_join = 0x06,
                        bad_char_inventory = 0x07,
                        bad_char_bodies = 0x08,
                        bad_header = 0x09,
                        bad_char_merc = 0x0a,
                        bad_intro = 0x0b,
                        bad_item = 0x0c,
                        bad_char_dead_body_item = 0x0d,
                        generic_bad_file = 0x0e,
                        game_is_full = 0x0f,
                        bad_game_version = 0x10,
                        must_kill_norm_baal = 0x11,
                        must_kill_night_baal = 0x12,
                        soft_cant_to_hard = 0x13,
                        hard_cant_to_soft = 0x14,
                        dead_hard_cant = 0x15,
                        unknown_failure = 0x16,
                        classic_cant_exp = 0x17,
                        exp_cant_classic = 0x18,
                        failed_to_join = 0x19,
                        unable_to_enter_the_game = 0x1a
                    )
                ),
                "stats_confirmation":Struct(None,
                    ULInt32("hp"),
                    ULInt32("mp"),
                    ULInt32("stamina"),
                    ULInt32("x"),
                    ULInt32("y"),
                    ULInt16("unknown")
                ),
                "movement_confirmation":Struct(None,
                    ULInt32("stamina"),
                    ULInt32("x"),
                    ULInt32("y"),
                    SLInt8("dx"),
                    SLInt8("dy")
                ),

                #item actions
                "world_item_action":Struct(None,
                    d2item_header,
                    d2item_body
                ),
                "owner_item_action":Struct(None,
                    d2item_header,
                    etype_eid("owner"),
                    d2item_body
                ),

                #unknown, but length
                "unknown_0x50":Struct(None, Bytes("data", 15 - 1)),
                "unknown_0x5e":Struct(None, Bytes("data", 38 - 1)),
                "unknown_0x5f":Struct(None, Bytes("data", 5 - 1)),
                "unknown_0x7e":Struct(None, Bytes("data", 5 - 1)),
                "unknown_0x91":Struct(None, Bytes("data", 26 - 1)),
                "unknown_0xa5":Struct(None, Bytes("data", 8 - 1)),
                "unknown_0xc1":Struct(None, Pass),
                "unknown_0xca":Struct(None, Bytes("data", 25 - 1)),
                "unknown_0xcb":Struct(None, Bytes("data", 23 - 1)),
            },
            default = Struct(None,
                Pointer(lambda ctx: ctx.start_fun, HexDumpAdapter(GreedyRange(ULInt8("data")))),
                GreedyRange(ULInt8(None))
            )
        )
    )
)


if __name__ == "__main__":
    #f1 41 a0 a1 01 10 49 88 d8 b0 00 88 b3 05
    #1000 1111 1000 0010 0000 0101 1000 0101 1000 0000 0000 1000 1001 0010 0001 0001 0001 1011 0000 1101 0000 0000 0001 0001 1100 1101 1010 0000
    #1000
    #animation = 1
    #     1
    #section 2 exist
    #48 bits padding
    #      111 1000 0010 0000 0101 1000 0101 1000 0000 0000 1000 1001 0
    #33 bits padding
    #      111
    s = "ac 30 03 cd f1 b8 01 4a 27 9f 33 80 1b f1 41 a0 a1 01 10 49 88 d8 b0 00 88 b3 05"
    print(s2c_packets.parse(rev(s)))
    print(rev(b'!28\xc8\xe8\x00\x00\x00\x00'))
    print(rev(b'13\x94\x01\x11\x0f\x8axp\xa7\n\xbc\xea\xf9\xaa\xf0?\xcd?'))

    #21 32 38 c8 e8 00 00 00 00
    #
    #1000 0100 0100 1100 0001 1100 0001 0011 0001 0111 0000 0000 0000 0000
    #1000 - animation
    #     0 - section 2 doesn't exists
    #      1 - section 3 exists
    #       0 - champion
    #        0 - unique
    #          0 - super unique
    #           1 - minion
    #            0 - ghostly
    #             0 1100 000 - mode 1
    #                       1 1100 000 - mode 2
    #                                 1 0011 000 - mode 3
    #                                           1 0111 000 - mode 4
    #                                                     0 0000 000 - terminator

    #31 33 94 01 11 0f 8a 78 70 a7 0a bc ea f9 aa f0 3f cd 3f
    #1000 1100 1100 1100 0010 1001 1000 0000 1000 1000 1111 0000 0101 0001

    '''bbb = BitStruct(None, Nibble("x"), Nibble("y"))
    bbl = BitStruct(None, Nibble("x"), LNibble("y"))
    blb = BitStruct(None, LNibble("x"), Nibble("y"))
    bll = BitStruct(None, LNibble("x"), LNibble("y"))
    lbb = LBitStruct(None, Nibble("x"), Nibble("y"))
    lbl = LBitStruct(None, Nibble("x"), LNibble("y"))
    llb = LBitStruct(None, LNibble("x"), Nibble("y"))
    lll = LBitStruct(None, LNibble("x"), LNibble("y"))

    src = b"\xa1"
    print("source:", src)
    for i in (bbb, bbl, blb, bll, lbb, lbl, llb, lll):
        y = i.parse(b"\xa1")
        print(y)
        print(i.build(y))
        print()'''
