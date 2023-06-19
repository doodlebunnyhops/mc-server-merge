# mc-server-merge
Python Script to migrate minecraft players to a new server so that they maintain inventory and spawn at a chosen location.

## Dependencies:
 - py -m pip install "nbtlib==1.12.1"
   - issues with latest [nbtlib](https://github.com/vberlier/nbtlib) 2.0.4   
 - python 3.10.0

## Usage

**`migrate.py [-h] -l LOADPATH -s SAVEPATH -x XCORD -y YCORD -z ZCORD`**

- Example cmd: `py migrate.py -l "C:\Minecraft\world\playerdata" -s "C:\Minecraft\backup\playerdata" -x -100 -y 200 -z 300`

- Help: `py migrate.py -h`

```text
MC Player Migration

options:
  -h, --help            show this help message and exit
  -l LOADPATH, --loadpath LOADPATH
                        Path to load Old PlayerData
  -s SAVEPATH, --savepath SAVEPATH
                        Path to Save Updated PlayerData
  -x XCORD, --xcord XCORD
                        X Coordinate for spawn overwrite
  -y YCORD, --ycord YCORD
                        Y Coordinate for spawn overwrite
  -z ZCORD, --zcord ZCORD
                        Z Coordinate for spawn overwrite
```

## Good to Know

- Copies all .dat files from old server (LoadPath), updates a few key tags, and saves the updated user to your Save Path.
  - .dat_old files are ignored.  
- Checks if LoadPath and SavePath exists before continuing, if either dir doesn't exist program will not attempt to create them and exit 1 with message `Error occurred while confirming Path Dir: {err}`
- Can be run from any directory, it will produce a log `player-migration.log` in the dir program was run from.
- Best to not have other NBT editor tools open when running, though I haven't had direct conflicts with [NBTExplorer](https://www.minecraftforum.net/forums/mapping-and-modding-java-edition/minecraft-tools/1262665-nbtexplorer-nbt-editor-for-windows-and-mac).

## Modified Player Data

Refer to [player.dat fromat](https://minecraft.fandom.com/wiki/Player.dat_format) documentation.

The goal here is for players to come on to a new minecraft server without concern that they were famished or dying when they were on the last server and keep what ever is on them. In addition we want to make it safe and avoid unexpected spawn locations into deathly traps.


1. **LastDeathLocation**: Remove, some plugins use this tag to allow easy `/back`. This could be deadlier after a migration...
2. **Pos**: Where player will spawn on join. This is where flags -x -y -z are injected. 
3. **Dimension**: Set to minecraft:overworld
4. **foodExhaustionLevel**: Set to 0. See [hunger](https://minecraft.fandom.com/wiki/Hunger) for more details. We want our players to be fed and ready to explore on a new map!
5. **foodLevel**: Set to 20
6. **foodStaturationLevel**: Set to 5
7. **Health**: Set to 20
8. **HurtByTimestamp**: Set to 0
9. **HurTime**: Set to 0
10. **OnGround**: Set to 1, True
11. **PlayerGameType**: Set to 0, Survival
12. **SpawnForced**: Remove. If player should spawn to their last bed location, even if it doesn't exist. Don't want an unintended death on our hands on a new map! 
13. **SpawnX**: Remove. X Coordinates for bed location.
14. **SpawnY**: Remove. Y Coordinates for bed location.
15. **SpawnZ**: Remove. Z Coordinates for bed location.
