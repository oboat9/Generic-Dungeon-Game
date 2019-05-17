import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:/Users/Owen Stevenson/AppData/Local/Programs/Python/Python37-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/Owen Stevenson/AppData/Local/Programs/Python/Python37-32/tcl/tk8.6"


executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="GenericNotDungeonGame",
    options = {"build_exe":{"packages":["pygame"],"include_files":["Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/manBlue_gun.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/tileGreen_39.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/bullet.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/zombie1_hold.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/spritesheet_tiles.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/maps/level1.tmx","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/maps/level2.tmx","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/maps/tile_maps/Kenny Topdown Pack.tsx","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/Player Dying.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/mainmenu.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/whitePuff18.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/whitePuff17.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/whitePuff16.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/whitePuff15.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/health_pack.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/splat green.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/splat red.png","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/ZOMBIE.TTF","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/playerhit.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/Bullet_Hit_Enemy.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/health_pack.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/menu_move.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/menu_select.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/player hurt.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/sfx_weapon_singleshot2.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/shotgun.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/splat-15.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/ZombieDying.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/snd/gun reload.wav","Z:/My Drive/Classrooms/Classroom 10/Computer Science 10/Programming/Final Project A/Generic-Dungeon-Game/img/ammo.png",]}}

    executables=executables

    )