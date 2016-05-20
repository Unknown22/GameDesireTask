import tornado.ioloop
import tornado.web
import json

all_results = []

class AddResult(tornado.web.RequestHandler):

    def get(self):
        self.correct_result = True

        gameid = self.get_argument("gameid")
        uid = self.get_argument("uid")
        end_timestamp = int(self.get_argument("end_timestamp"))
        game_result = self.get_argument("game_result")

        self.check_gameid(gameid)
        self.check_uid(uid)
        self.check_end_timestamp(end_timestamp)
        self.check_game_result(game_result)

        if self.correct_result:
            result = { 'GAMEID' : gameid,
                       'UID' : int(uid),
                       'end_timestamp': end_timestamp,
                       'game_result' : float(game_result)
                        }
            all_results.append(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
            self.write("Result has been added")
        else:
            self.write("Result has not been added")

    def check_gameid(self, gameid):
        if gameid != None:
            pass
        else:
            self.correct_result = False
            self.write("Invalid GAMEID<br>")

    def check_uid(self, uid):
        if self.represents_int(uid):
             if int(uid) >= 0:
                 pass
             else:
                self.correct_result = False
                self.write("Invalid UID<br>") 
        else:
            self.correct_result = False
            self.write("Invalid UID<br>")     

    def check_end_timestamp(self, end_timestamp):
        if end_timestamp != None:
            pass
        else:
            self.correct_result = False
            self.write("Incorrect end timestamp<br>")      

    def check_game_result(self, game_result):
        if self.represents_float(game_result):
            pass
        else:
            self.write("Incorrect game result<br>")
            self.correct_result = False
        
    def represents_int(self, test_int):
        try:
            int(test_int)
            return True
        except ValueError:
            return False

    def represents_float(self, test_float):
        try:
            float(test_float)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/add", AddResult)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()