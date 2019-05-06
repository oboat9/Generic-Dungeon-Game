import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:/Users/Owen Stevenson/AppData/Local/Programs/Python/Python37-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/Owen Stevenson/AppData/Local/Programs/Python/Python37-32/tcl/tk8.6"


executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="GenericNotDungeonGame",
    options = {"build_exe":{"packages":["pygame"],"include_files":["Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/manBlue_gun.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/tileGreen_39.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/bullet.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/zombie1_hold.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/spritesheet_tiles.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/maps/level1.tmx","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/maps/tile_maps/Kenny Topdown Pack.tsx","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/Player Dying.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/mainmenu.wav"]}},

    executables=executables

    )