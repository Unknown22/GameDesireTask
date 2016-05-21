import tornado.ioloop
import tornado.web
import json
from operator import itemgetter
import datetime


all_results = []

class AddResult(tornado.web.RequestHandler):

    def get(self):
        self.correct_result = True

        gameid = self.get_argument("gameid")
        uid = self.get_argument("uid")
        end_timestamp = int(self.get_argument("end_timestamp"))
        game_result = self.get_argument("game_result")

        self.check_arguments_correct(end_timestamp, game_result, gameid, uid)

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


    def check_arguments_correct(self, end_timestamp, game_result, gameid, uid):
        self.check_gameid(gameid)
        self.check_uid(uid)
        self.check_end_timestamp(end_timestamp)
        self.check_game_result(game_result)


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


class ShowRanking(tornado.web.RequestHandler):

    def get(self):
        gameid, date = self.get_arguments()
        rank = self.get_ranking(gameid)

        if date != None:
            rank_d = self.get_daily_ranking(rank, date)
            for r in rank_d:
                self.write(str(r['UID']) + ": ")
                self.write(str(r['game_result']))
                self.write("<br>")
        else:
            for r in rank:
                self.write(str(r['UID']) + ": ")
                self.write(str(r['game_result']))
                self.write("<br>")


    def get_daily_ranking(self, rank, date):
        rank_d = []
        for r in rank:
            end_timestamp_date = datetime.datetime.fromtimestamp(r['end_timestamp'])
            if date.date() == end_timestamp_date.date():
                rank_d.append(r)
        return rank_d


    def get_arguments(self):
        gameid = self.get_argument("gameid")
        day = self.get_argument("d", None)
        month = self.get_argument("m", None)
        year = self.get_argument("y", None)

        if day != None and month != None and year != None:
            date = self.check_correct_date(day, month, year)
            if date != None:
                self.write(str(date.date()) + "<br>")
        else:
            date = None

        return (gameid, date)


    def check_correct_date(self, day, month, year):
        correct_date = True
        
        if day != None:
            try:
                day = int(day)
            except:
                self.write("Invalid day parameter<br>")
                correct_date = False
        
        if month != None:
            try:
                month = int(month)
            except:
                self.write("Invalid month parameter<br>")
                correct_date = False
        
        if year != None:
            try:
                year = int(year)
            except:
                self.write("Invalid year parameter<br>")
                correct_date = False
        
        if correct_date == True:
            try:
                date = datetime.datetime(year, month, day)
            except Exception as e:
                date = None
                self.write(str(e))

        return date

    def get_ranking(self, gameid):
        rank = []
        
        if gameid != None:
            for result in all_results:
                if json.loads(result)['GAMEID'] == gameid:
                    rank.append(json.loads(result))
        else:
            self.write("Invalid GAMEID<br>")
        
        rank.sort(key=itemgetter('game_result'), reverse=True)

        return rank


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/add", AddResult),
        (r"/show_ranking", ShowRanking),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()