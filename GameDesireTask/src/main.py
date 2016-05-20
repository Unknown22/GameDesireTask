import tornado.ioloop
import tornado.web
import json

all_results = []

class AddResult(tornado.web.RequestHandler):
    def get(self, _result):
        split_result = _result.split('/')
        
        if self.check_correct(split_result):
            result = { 'GAMEID' : split_result[0],
                       'UID' : int(split_result[1]),
                       'end_timestamp': int(split_result[2]),
                       'game_result' : float(split_result[3])
                        }
            all_results.append(json.dumps(result, sort_keys=True))
            self.write("Result has been added")
        else:
            self.write("Result has not been added")

    def check_uid(self, data):
        if self.represents_int(data[1]) and int(data[1]) >= 0:
            pass
        else:
            self.write("Incorrect UID<br>")
            self.correct = False

    def check_game_result(self, data):
        if self.represents_float(data[3]):
            pass
        else:
            self.write("Incorrect game result<br>")
            self.correct = False

    def check_correct(self, data):
        self.correct = True
        self.check_uid(data)
        self.check_game_result(data)
        return self.correct
        
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
        (r"/add/([A-Za-z0-9_]*/-?[0-9]*/[0-9]*/.*)", AddResult),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()