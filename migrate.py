import os
import sys
import logging
import argparse
import nbtlib
from nbtlib.tag import *

"""
Migrating Minecraft Users to a new server Guide:

Dependencies:
- py -m pip install "nbtlib==1.12.1"
    - Attempted with latest version 2.0.4 and was recieving empty error messages... one day i'll figure out this bug
- tested on python 3.10.0
    - Will note nbtlib has been tested up to 3.9.0, but seems to be working for me here on 3.10.0

Notes:

- This will generate a log file in the directory it was ran from and name it 'player-migration.log'
- you can run this from which ever directory you like
- Program will validate both load path and save path exist before continuing. If either doesn't exist, this program will not create the dir and exit!
- There are some other player data points that are modified. They are found in the update function and each is commented.

Example cmd: 
py migrate.py -l "D:\Minecraft-1_20\world\playerdata" -s "D:\Minecraft-1_20\backup\playerdata" -x -100 -y 200 -z 300

py migrate.py -h
usage: migrate.py [-h] -l LOADPATH -s SAVEPATH -x XCORD -y YCORD -z ZCORD

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


"""

class Data:

    def __init__(self,loadpath,savepath,xcord,ycord,zcord,players):
        self.loadpath = loadpath
        self.savepath = savepath
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.players = players
        
    def player_files_list(self):
        logging.info('list_player_files')
        try:
            file_list = []
            for filename in os.listdir(str(self.loadpath)):
                if filename.endswith(".dat"):
                    file_list.append(filename)

            self.players = file_list
        except Exception as err:
            logging.error(f"Error occurred while listing files: {err}")
            sys.exit(1)
            
    def update(self):
    
        try:
            for player in self.players:
                logging.info(f'Updating file:\t\t\t{player}')
                playerdata = nbtlib.load(os.path.join(self.loadpath, player))
                
                #Remove LastDeathLocation
                playerdata[''].pop('LastDeathLocation',None)
                
                #Modify POS
                playerdata['']['Pos'][0] = Double(self.xcord)
                playerdata['']['Pos'][1] = Double(self.ycord)
                playerdata['']['Pos'][2] = Double(self.zcord)
                
                #Modify Dimension
                playerdata['']['Dimension'] = String('minecraft:overworld')
                
                #Modify foodExhaustionLevel
                playerdata['']['foodExhaustionLevel'] = Float(0)
                
                #Modify foodLevel
                playerdata['']['foodLevel'] = Int(20)
                
                #Modify foodStaturationLevel
                playerdata['']['foodStaturationLevel'] = Float(5)
                
                #Modify Health
                playerdata['']['Health'] = Float(20)
                
                #Modify HurtByTimestamp
                playerdata['']['HurtByTimestamp'] = Int(0)
                
                #Modify HurtTime
                playerdata['']['HurtTime'] = Short(0)
                
                #Modify OnGround
                playerdata['']['OnGround'] = Byte(1)
                
                #Modify PlayerGameType
                playerdata['']['PlayerGameType'] = Int(0)
                
                #Remove SpawnForced (Force spawn at bed location)
                playerdata[''].pop('SpawnForced',None)
                
                #Remove SpawnX (Bed Location x cord)
                playerdata[''].pop('SpawnX',None)
                
                #Remove SpawnY (Bed Location y cord)
                playerdata[''].pop('SpawnY',None)
                
                #Remove SpawnZ (Bed Location z cord)
                playerdata[''].pop('SpawnZ',None)
                
                #Save updates to Save Path
                playerdata.save(os.path.join(self.savepath, player))
                logging.info(f'Successfully updated file:\t{player}')
            
        except Exception as err:
            logging.error(f"Error occurred while updating player data: {err}")
            sys.exit(1)
        
        
def dir_path(path):
    try:
        if not os.path.isdir(path):
            raise ValueError(f"Invalid directory: {path}")
        return path
    except Exception as err:
        logging.error(f"Error occurred while confirming Path Dir: {err}")
        sys.exit(1)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='player-migration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s')
    
    logging.info("Starting program")
    
    #Parse Arguments
    parser = argparse.ArgumentParser(description = "MC Player Migration")
    
    parser.add_argument("-l", "--loadpath", type=dir_path, default = None, required=True, help = "Path to load Old PlayerData")
    parser.add_argument("-s", "--savepath", type=dir_path, default = None, required=True, help = "Path to Save Updated PlayerData")
    parser.add_argument("-x", "--xcord", default = None, required=True, help = "X Coordinate for spawn overwrite")
    parser.add_argument("-y", "--ycord", default = None, required=True, help = "Y Coordinate for spawn overwrite")
    parser.add_argument("-z", "--zcord", default = None, required=True, help = "Z Coordinate for spawn overwrite")
    
    args = parser.parse_args()
    
    #Save arguments to Data Class
    d = Data(args.loadpath,args.savepath,args.xcord,args.ycord,args.zcord,None)
    
    #Fetch Player Files
    d.player_files_list()
    
    #update files
    d.update()
    
    logging.info(f'Amazing! We\'re all done!')
    
