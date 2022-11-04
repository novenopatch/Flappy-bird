import json
from Enumeration import SaveData
from datetime import datetime

class Save():
    def __init__(self):
        self.file_name = "config.json"
        self.data = {
            'high score': 0, 'score': 0,'last run':datetime.now(),
            'screen height':1024,'screen width':576,
            'frame rate':120
        }
        self.restore_data()
    def update_scores(self,score:tuple):
        self.data['score'] = score[0]
        self.data['high score'] =score[1]
    def save_data(self):
        self.data['last run'] =str(datetime.now())
        with open(self.file_name, 'w') as file:

            json.dump(self.data, file)

    def get_data(self, data: SaveData):
        if data == SaveData.SCORE:
            return self.data['score']
        elif data == SaveData.HIGH_SCORE:
            return self.data['high score']
        elif data == SaveData.SCREEN_WIDTH:
            return self.data['screen width']
        elif data == SaveData.SCREEN_HEIGHT:
            return self.data['screen height']
        elif data == SaveData.FRAME_RATE:
            return self.data['frame rate']

    def restore_data(self):
        try:
            with open(self.file_name) as file:
                self.data = json.load(file)
        except Exception as e:
            pass
            #print(e)
