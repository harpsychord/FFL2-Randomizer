from enum import Enum
import mmap
from FFL2R_manager_scripts import ScriptManager
from FFL2R_manager_maps import MapManager

# World here doesn't mean any unique technical data, but rather
# a design. FFL2 has around a dozen or so "Worlds" that use specific
# data. This file exists as a way to manage and edit easily.
class WorldManager:
    def __init__(self):
        self.WORLD_NAME_STARTADDR = 0x3f6f0
        self.PRISMADDR = 0x3e600

        #pillar world, map index in door, out door, map index trigger set prism
        #in door, world, map index out door, teleport scripts, name addr, teleport unlock script location, prism count
        self.pillar = {
            "Ashura"   :    self.Pillar(2, 23, 6, 98, 5, 1),
            "Giant"    :    self.Pillar(3, 40, 6, 104, 5, 2),
            "Apollo"   :    self.Pillar(4, 56, 6, 193, 5, 3),
            "Guardian" :    self.Pillar(5, 84, 6, 230, 5, 4),
            "Monster"  :    self.Pillar(6, 100, 9, 235, 8, 5),
            "Venus"    :    self.Pillar(7, 103, 6, 280, 5, 6),
            "Race"     :    self.Pillar(8, 125, 6, 286, 5, 7),
            "Edo"      :    self.Pillar(9, 136, 6, 315, 5, 8),
            "Nasty"    :    self.Pillar(10, 161, 6, 134, 5, 9),
            "Valhalla" :    self.Pillar(11, 163, 5, 391, 4, None)
            }

        self.world = {
            "Ashura's World"   : self.World(2, 99, False, 22, 0, [99,100], [0x3f6f0, 0x3f700], (330, 134, 2), 147, 7),
            "Giant World"      : self.World(3, 105, False, 39, 3, [101], [0x3f710], (339, 502, 1), 148, 3),
            "Apollo's World"   : self.World(4, 194, False, 55, 1, [102, 103], [0x3f720, 0x3f730], (492, 339, 2), 149, 10),
            "Guardian Base"    : self.World(5, 87, True, 83, 0, [104], [0x3f740], (10, 41, 1), 150, 4),    
            "Monster World"    : self.World(6, 237, False, 99, 1, None, None, None, 151, 2),
            "Venus' World"     : self.World(7, 281, False, 210, 2, [105], [0x3f750], (412, 105, 1), 152, 11),
            "Race World"       : self.World(8, 287, False, 124, 0, [106], [0x3f760], (78, 77, 1), 153, 4),
            "Edo"              : self.World(9, 316, False, 135, 0, [107], [0x3f770], (117, 273, 1), 154, 4),
            "Nasty Dungeon"    : self.World(None, 387, False, 160, 0, [108], [0x3f780], (94, 12, 1), 155, 1),
            "Valhalla Palace"  : self.World(None, 390, False, 162, 1, [109], [0x3f790], (132, 25, 1), 156, 8)
            }

        self.finalStore = {
            "First Town"    :   (1, 7, 6),
            "Second Town"   :   (1, 10, 4),
            "Desert Town"   :   (2, 25, 4),
            "Ashura Town"   :   (2, 28, 4),
            "Giant Town"    :   (3, 42, 4),
            "Port Town"     :   (4, 59, 4),
            "Lynn Town"     :   (4, 67, 4),
            "Guardian Base" :   (5, 85, 4),
            "Monster World" :   (6, 101, 4),
            "Venus World 1" :   (7, 107, 4),
            "Venus World 2" :   (7, 107, 12),
            "Race World"    :   (8, 127, 4),
            "Edo 1"         :   (9, 153, 2),
            "Edo 2"         :   (9, 159, 2)
            }


        self.locations = {
            "Opening Cutscene"                                      : self.Location(self.LocationType.SCRIPT_MAGI, [0, 1, 172], self.PrismIndex.FIRST_WORLD),
            "Char 2's Parent"                                       : self.Location(self.LocationType.SCRIPT_ITEM_SPECIAL, [0, 275, 39], self.PrismIndex.FIRST_WORLD),
            "First Cave, First Platform, Left"                      : self.Location(self.LocationType.NPC_ITEM, [5, 2], self.PrismIndex.FIRST_WORLD),
            "First Cave, First Platform, Right"                     : self.Location(self.LocationType.NPC_ITEM, [5, 3], self.PrismIndex.FIRST_WORLD),
            "First Cave, Near Exit, North"                          : self.Location(self.LocationType.NPC_ITEM, [5, 4], self.PrismIndex.FIRST_WORLD),
            "First Cave, Near Exit, South"                          : self.Location(self.LocationType.NPC_ITEM, [5, 5], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 2"                    : self.Location(self.LocationType.NPC_ITEM, [13, 0], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Northwest"         : self.Location(self.LocationType.NPC_ITEM, [14, 0], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Southwest"         : self.Location(self.LocationType.NPC_ITEM, [14, 1], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Northeast"         : self.Location(self.LocationType.NPC_ITEM, [14, 2], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Southeast"         : self.Location(self.LocationType.NPC_ITEM, [14, 3], self.PrismIndex.FIRST_WORLD),
            #the npc removal happens after, uses original npc counts
            "Ruins of the Ancient Gods, Floor 4, Main North"        : self.Location(self.LocationType.EMPTY, [15, 5], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Main West"         : self.Location(self.LocationType.EMPTY, [15, 6], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Main East"         : self.Location(self.LocationType.EMPTY, [15, 7], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault Northeast"   : self.Location(self.LocationType.NPC_MAGI, [15, 8], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault Southeast"   : self.Location(self.LocationType.NPC_MAGI, [15, 9], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault West"        : self.Location(self.LocationType.NPC_MAGI, [15, 10], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, North of Entrance" : self.Location(self.LocationType.NPC_ITEM, [15, 11], self.PrismIndex.FIRST_WORLD),
            #Ashura's Base, Wanderers
            "Ashura's Base, Floor 3"                                : self.Location(self.LocationType.NPC_ITEM, [18, 4], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Floor 4"                                : self.Location(self.LocationType.NPC_ITEM, [19, 4], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [20, 0], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit Southeast"                         : self.Location(self.LocationType.NPC_MAGI, [20, 5], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit Northeast"                         : self.Location(self.LocationType.NPC_MAGI, [20, 6], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit West"                              : self.Location(self.LocationType.NPC_MAGI, [20, 7], self.PrismIndex.FIRST_WORLD),
            "Ashura's Tower, Floor 4"                               : self.Location(self.LocationType.NPC_ITEM, [32, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Floor 7"                               : self.Location(self.LocationType.NPC_ITEM, [35, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Floor 9"                               : self.Location(self.LocationType.NPC_ITEM, [37, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Southwest"              : self.Location(self.LocationType.NPC_ITEM, [38, 4], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Southeast"              : self.Location(self.LocationType.NPC_ITEM, [38, 5], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Northwest"              : self.Location(self.LocationType.NPC_ITEM, [38, 6], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Northeast"              : self.Location(self.LocationType.NPC_ITEM, [38, 7], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 1"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 2"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 3], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 3"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 6], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 4"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 9], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 5"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 12], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 6"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 15], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 7"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 18], self.PrismIndex.ASHURA_WORLD),
            "Dad in Giant's World"                                  : self.Location(self.LocationType.SCRIPT_MAGI, [0, 339, 303], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Magi House North"                          : self.Location(self.LocationType.NPC_MAGI, [45, 0], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Magi House South"                          : self.Location(self.LocationType.NPC_MAGI, [45, 1], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Micron House West"                         : self.Location(self.LocationType.NPC_ITEM, [46, 0], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Micron House East"                         : self.Location(self.LocationType.NPC_ITEM, [46, 1], self.PrismIndex.GIANT_WORLD),
            #"Giant Town, Micron Potion Location"                    : self.Location(self.LocationType.SCRIPT_ITEM_FORCED, [0, 29, 11], self.PrismIndex.GIANT_WORLD),
            "Ki's Assistant"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 308, 34], self.PrismIndex.FIRST_WORLD_RETURN),
            "Ki's Stomach"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 31, 0], self.PrismIndex.KIS_BODY),
            "Ki's Heart"                                            : self.Location(self.LocationType.SCRIPT_MAGI, [0, 32, 0], self.PrismIndex.KIS_BODY),
            "Ki's Left Hand"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 33, 0], self.PrismIndex.KIS_BODY),
            "Ki's Right Hand"                                       : self.Location(self.LocationType.SCRIPT_MAGI, [0, 34, 0], self.PrismIndex.KIS_BODY),
            "Ki's Left Foot"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 35, 0], self.PrismIndex.KIS_BODY),
            "Ki's Right Foot"                                       : self.Location(self.LocationType.SCRIPT_MAGI, [0, 36, 0], self.PrismIndex.KIS_BODY),
            "Ki's Brain"                                            : self.Location(self.LocationType.SCRIPT_MAGI, [0, 37, 0], self.PrismIndex.KIS_BODY),
            "Meeting Apollo"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 350, 76], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 3 West"                        : self.Location(self.LocationType.NPC_ITEM, [63, 0], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 3 East"                        : self.Location(self.LocationType.NPC_ITEM, [63, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 4"                             : self.Location(self.LocationType.NPC_ITEM, [64, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit West"                           : self.Location(self.LocationType.NPC_MAGI, [65, 0], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit East"                           : self.Location(self.LocationType.NPC_MAGI, [65, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit TrueEye"                        : self.Location(self.LocationType.NPC_MAGI_SPECIAL, [65, 2], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Entrance"                                : self.Location(self.LocationType.NPC_ITEM, [70, 0], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Floor 3"                                 : self.Location(self.LocationType.NPC_ITEM, [72, 0], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Dunatis Floor"                           : self.Location(self.LocationType.NPC_ITEM, [74, 2], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 3"                                : self.Location(self.LocationType.NPC_ITEM, [78, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 4 West"                           : self.Location(self.LocationType.NPC_ITEM, [79, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 4 East"                           : self.Location(self.LocationType.NPC_ITEM, [79, 1], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [80, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 6"                                : self.Location(self.LocationType.NPC_ITEM, [81, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor North"                      : self.Location(self.LocationType.NPC_MAGI, [82, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor East"                       : self.Location(self.LocationType.NPC_MAGI, [82, 1], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor West"                       : self.Location(self.LocationType.NPC_MAGI, [82, 2], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 1"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 59], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 2"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 62], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 3"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 65], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 4"                                        : self.Location(self.LocationType.SCRIPT_ITEM, [0, 492, 68], self.PrismIndex.APOLLOS_WORLD),
            "Guardian Base Storage, North-center"                   : self.Location(self.LocationType.EMPTY, [97, 0], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Northwest"                      : self.Location(self.LocationType.EMPTY, [97, 1], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Center"                         : self.Location(self.LocationType.EMPTY, [97, 2], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Northeast"                      : self.Location(self.LocationType.EMPTY, [97, 3], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, South"                          : self.Location(self.LocationType.EMPTY, [97, 4], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Commando"                                : self.Location(self.LocationType.SCRIPT_MAGI, [0, 400, 59], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Magician"                                : self.Location(self.LocationType.SCRIPT_MAGI, [0, 401, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Manticore"                               : self.Location(self.LocationType.SCRIPT_MAGI, [0, 402, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Ogre"                                    : self.Location(self.LocationType.SCRIPT_MAGI, [0, 404, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Dad's Death, Final Gift"                               : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 282], self.PrismIndex.MONSTER_WORLD),
            "Dad's Death, Ninja"                                    : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 745], self.PrismIndex.MONSTER_WORLD),
            "Dad's Death, Lynn's Mom"                               : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 1185], self.PrismIndex.APOLLOS_WORLD_RETURN),
            "Sewer, Entrance"                                       : self.Location(self.LocationType.NPC_ITEM, [110, 0], self.PrismIndex.VENUS_WORLD),
            #"Hermit Crab Drop"                                      : self.Location(self.LocationType.SCRIPT_ITEM, [0, 438, 14], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 2"                                        : self.Location(self.LocationType.NPC_ITEM, [111, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 5 West"                                   : self.Location(self.LocationType.NPC_ITEM, [114, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 5 East"                                   : self.Location(self.LocationType.NPC_ITEM, [114, 1], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Northwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Southwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 1], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Northeast"                       : self.Location(self.LocationType.NPC_MAGI, [116, 2], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Northwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 4], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Northeast"                       : self.Location(self.LocationType.NPC_MAGI, [116, 5], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Southwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 6], self.PrismIndex.VENUS_WORLD),
            #Sewer, Monster-in-a-box
            "Venus Volcano, Floor 5, Lava"                          : self.Location(self.LocationType.NPC_ITEM, [121, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 5, Land"                          : self.Location(self.LocationType.NPC_ITEM, [121, 2], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 6, West"                          : self.Location(self.LocationType.NPC_ITEM, [122, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 6, East"                          : self.Location(self.LocationType.NPC_ITEM, [122, 2], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, Isolated"                         : self.Location(self.LocationType.NPC_ITEM, [123, 4], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, West"                             : self.Location(self.LocationType.NPC_MAGI,[123, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, East"                             : self.Location(self.LocationType.NPC_MAGI,[123, 2], self.PrismIndex.VENUS_WORLD),
            "Leon's Theft"                                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 420, 28], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 1"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 0], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 2"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 3], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 3"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 6], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 4"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 9], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 5"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 12], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 6"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 15], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 7"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 18], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 8"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 43, 106], self.PrismIndex.VENUS_WORLD),
            "Race - Adamant"                                        : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 457, 36], self.PrismIndex.RACE_WORLD),
            "Race - Tortoise"                                       : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 458, 36], self.PrismIndex.RACE_WORLD),
            "Race - Lamia"                                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 459, 36], self.PrismIndex.RACE_WORLD),
            "Race - Watcher"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 460, 24], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Lamia)"                                : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 30], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Tortoise)"                             : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 37], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Adamant)"                              : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 44], self.PrismIndex.RACE_WORLD),
            "Edo Castle, Floor 3, Center"                           : self.Location(self.LocationType.NPC_ITEM, [142, 0], self.PrismIndex.EDO),
            "Edo Castle, Floor 3, West"                             : self.Location(self.LocationType.NPC_ITEM, [142, 1], self.PrismIndex.EDO),
            "Edo Castle, Floor 3, East"                             : self.Location(self.LocationType.NPC_ITEM, [142, 2], self.PrismIndex.EDO),
            "Edo Castle, Floor 4"                                   : self.Location(self.LocationType.NPC_ITEM, [143, 0], self.PrismIndex.EDO),
            "Edo Castle, Floor 5"                                   : self.Location(self.LocationType.NPC_ITEM, [144, 0], self.PrismIndex.EDO),
            "Edo Castle, Shogun Floor"                              : self.Location(self.LocationType.NPC_ITEM, [145, 5], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Middle Deck"                    : self.Location(self.LocationType.NPC_ITEM, [150, 0], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Lower Deck, West"               : self.Location(self.LocationType.NPC_ITEM, [151, 2], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Lower Deck, East"               : self.Location(self.LocationType.NPC_ITEM, [151, 3], self.PrismIndex.EDO),
            #Edo, Hatamotos
            "Magnate Drop 1"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 103], self.PrismIndex.EDO),
            "Magnate Drop 2"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 106], self.PrismIndex.EDO),
            "Magnate Drop 3"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 109], self.PrismIndex.EDO),
            "Magnate Drop 4"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 112], self.PrismIndex.EDO),
            "Nasty Dungeon, Entrance, MAGI Chest"                   : self.Location(self.LocationType.SCRIPT_MAGI, [0, 94, 9], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 1"                      : self.Location(self.LocationType.NPC_ITEM, [202, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 2"                      : self.Location(self.LocationType.NPC_ITEM, [202, 4], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 3"                      : self.Location(self.LocationType.NPC_ITEM, [202, 5], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 4"                      : self.Location(self.LocationType.NPC_ITEM, [202, 6], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [203, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [203, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [203, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [203, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [204, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [204, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [204, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [204, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [205, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [205, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [205, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [205, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [206, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [206, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [206, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [206, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 5"                       : self.Location(self.LocationType.NPC_ITEM, [206, 4], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [207, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [207, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [207, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [207, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [208, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [208, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [208, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [208, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 1"                          : self.Location(self.LocationType.NPC_ITEM, [209, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 2"                          : self.Location(self.LocationType.NPC_ITEM, [209, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 3"                          : self.Location(self.LocationType.NPC_ITEM, [209, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 4"                          : self.Location(self.LocationType.NPC_ITEM, [209, 4], self.PrismIndex.NASTY_DUNGEON),
            "Vahalla, Entrance"                                     : self.Location(self.LocationType.NPC_ITEM, [164, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 2"                                      : self.Location(self.LocationType.NPC_ITEM, [165, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 4"                                      : self.Location(self.LocationType.NPC_ITEM, [167, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 5"                                      : self.Location(self.LocationType.NPC_ITEM, [168, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 6"                                      : self.Location(self.LocationType.NPC_ITEM, [169, 0], self.PrismIndex.VALHALLA),
            "Odin Drop 1"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 0], self.PrismIndex.VALHALLA),
            "Odin Drop 2"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 3], self.PrismIndex.VALHALLA),
            "Odin Drop 3"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 6], self.PrismIndex.VALHALLA),
            "Odin Drop 4"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 9], self.PrismIndex.VALHALLA),
            "Odin Drop 5"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 12], self.PrismIndex.VALHALLA),
            "Odin Drop 6"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 15], self.PrismIndex.VALHALLA),
            "Odin Drop 7"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 18], self.PrismIndex.VALHALLA),
            "Odin Drop 8"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 132, 15], self.PrismIndex.VALHALLA),
            "Final Dungeon, Entrance"                               : self.Location(self.LocationType.NPC_ITEM, [177, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 2"                                : self.Location(self.LocationType.NPC_ITEM, [178, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 4"                                : self.Location(self.LocationType.NPC_ITEM, [180, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [181, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 6"                                : self.Location(self.LocationType.NPC_ITEM, [182, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 7"                                : self.Location(self.LocationType.NPC_ITEM, [183, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 9"                                : self.Location(self.LocationType.NPC_ITEM, [185, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 10"                               : self.Location(self.LocationType.NPC_ITEM, [186, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, WarMach Chest"                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 71, 7], self.PrismIndex.FINAL_WORLD)
            #"Central Pillar, Tian-Lung drop"                          :
            #"Central Pillar, Fenrir drop"                             :
            }

    class LocationType(Enum):
        EMPTY = 0
        NPC_ITEM = 1
        NPC_ITEM_SPECIAL = 2
        NPC_MAGI = 3
        NPC_MAGI_SPECIAL = 4
        SCRIPT_ITEM = 5
        SCRIPT_ITEM_SPECIAL = 6
        SCRIPT_MAGI = 7
        SCRIPT_MAGI_SPECIAL = 8

    class PrismIndex(Enum):
        FIRST_WORLD = 0
        ASHURA_WORLD = 1
        FIRST_WORLD_RETURN = 2
        GIANT_WORLD = 3
        KIS_BODY = 4
        APOLLOS_WORLD = 5
        GUARDIAN_WORLD = 6
        MONSTER_WORLD = 7
        APOLLOS_WORLD_RETURN = 8
        VENUS_WORLD = 9
        RACE_WORLD = 10
        EDO = 11
        NASTY_DUNGEON = 12
        VALHALLA = 13
        FINAL_WORLD_FAKEOUT = 14
        FINAL_WORLD = 15


    class Pillar:
        def __init__(self, order:int, mapPillarID:int, doorInMapIndex:int, doorOut:int, mapPillarTriggerIndexPrism:int, nextPillarVar16Check:int|None):
            self.order = order
            self.mapPillarID = mapPillarID
            self.doorInMapIndex = doorInMapIndex
            self.doorOut = doorOut
            self.mapPillarTriggerIndexPrism = mapPillarTriggerIndexPrism
            self.nextPillarVar16Check = nextPillarVar16Check

    class World:
        def __init__(self, index:int, doorIn:int, isScript:bool, mapID:int, doorOutMapIndex:int, teleportScripts:list|None, 
                     nameAddr:list|None, scriptTeleportUnlockByte:tuple|None, prismScript:int, prismCount:int):
            self.index = index
            self.doorIn = doorIn
            self.isScript = isScript
            self.mapID = mapID
            self.doorOutMapIndex = doorOutMapIndex
            self.teleportScripts = teleportScripts
            self.nameAddr = nameAddr
            self.scriptTeleportUnlockByte = scriptTeleportUnlockByte
            self.prismScript = prismScript
            self.prismCount = prismCount

    class Location:
        def __init__(self, lType:Enum, data:list, pType:Enum):
            self.lType = lType
            self.data = data
            self.pType = pType

    def magiCheckRedo(self, scripts:ScriptManager, maps:MapManager, worldType:int):
        #most var16 incs are in the respective rescript events. 
        #repurpose 72/73 to teleport to appropriate guardian world
        maps.remNPC(15,4)
        scripts.replaceScript(0, 24, '00')
        maps.remNPC(39,1)
        scripts.replaceScript(0, 68, '00')
        scripts.insertIntoScriptAtEnd(0, 400, '12 10')
        scripts.insertIntoScriptAtEnd(0, 468, '12 10')
        scripts.insertIntoScriptAtEnd(0, 132, '12 10')
        maps.addNPC(172, 0, '50 0a e0 c1 35 f0')
        maps.remNPC(175, 0)
        scripts.replaceScript(0, 53, '1a 4b 19 00 44 00 19 00 45 00')
        scripts.replaceScript(0, 68, 'ff 36 03 d0 4e 92 8f ff b7 b6 06 36 03 c6 ba c0 79 5d 69 e3 8b 06 36 04 50 5f 83 e2 66 f3 00')
        scripts.replaceScript(0, 69, '14 10 0b 10 06 36 05 c8 e3 8b 8f f3 0b 0d 19 f0 01 ff 00 00')
        scripts.replaceScript(0, 70, 'ff d0 4e e0 8e 54 d6 81 e3 98 7f 06 58 67 69 50 53 5e 66 df d7 e6 06 5d 69 e3 8b 4f 70 52 d7 e2 66 f3 00')
        scripts.replaceScript(0, 72, '00')
        scripts.replaceScript(0, 104, '19 00 5f 14 0e 06 15 06 02 19 05 e5 0e 19 05 ec 00')
        scripts.replaceScript(0, 74, '00')
        scripts.replaceScript(0, 75, '00')
        scripts.replaceScript(0, 76, '00')
        scripts.replaceScript(0, 77, '00')
        scripts.removeFromScript(0, 142, 307, 310)
 
        for v in self.pillar.values():
            if (v.nextPillarVar16Check):
                if worldType != 3:
                    maps.map[v.mapPillarID].npcs[0][1] = v.nextPillarVar16Check
                else:
                    maps.map[v.mapPillarID].npcs[0][1] = 0x00
                maps.map[v.mapPillarID].npcs[0][4] = 0x00
                maps.map[v.mapPillarID].npcs[0][5]+=0x01
 
        maps.map[174].npcs[14] = bytearray.fromhex('4c 04 e0 dc 00 f1')

    def getPrismCounts(self, rom:mmap)->list:
        magiCounts = []
        for x in range (0,16):
            magiCounts.append(rom[self.PRISMADDR+x])
        return magiCounts