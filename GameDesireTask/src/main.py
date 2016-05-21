import tornado.ioloop
import tornado.web
import json
from operator import itemgetter
import datetime
import os

from ShowRankingSite import ShowRankingSite

all_results = []

class AddResult(tornado.web.RequestHandler):
    """
    Klasa obsługuje dodawanie rezultatów z gry.
    Przyjmuje z zapytania parametry gameid, uid, end_timestamp i game_result, np.
    http://localhost:8888/add?gameid=gomoku&uid=1123&end_timestamp=1462959258&game_result=12312
    
    Jeżeli jakiś parametr nie zostanie podany zostanie zwrócony błąd 400: Bad Request.
    Jeżeli jakiś parametr nie przejdzie walidacji zostanie wyświetlona odpowiednia informacja a próba dodania nieprawidłowego rezultatu zakończy się niepowodzeniem.
    """
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
        """
        Metoda waliduje poprawność podanych argumentów
        """
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
    """
    Klasa obsługuje ranking ogólny, dzienne rankingi oraz odpowiada za ich wyświetlanie w przeglądarce zgodnie z podanymi parametrami.
    Aby wyświetlić ranking ogólny w zapytaniu jako argument należy podać GAMEID, np.
    http://localhost:8888/show_ranking?gameid=gomoku
    Zostanie wyświetlony ranking ogólny z gry o id "gomoku"

    Aby wyświetlić ranking z konkretnego dnia należy podać dodatkowe parametry d, m oraz y (odpowiednio dzień, miesiąc i rok), np.
    http://localhost:8888/show_ranking?gameid=gomoku&d=11&m=5&y=2016
    Zostanie wyświetlony ranking z gry o id "gomoku". Ranking dotyczyć będzie tylko wyników z 11 maja 2016 roku.
    Jeżeli jakiś parametr daty będzie niepoprawny zostanie wyświetlona informacja o tym i zostanie wyświetlony ranking ogólny dla danej gry.
    """
    def get(self):
        gameid, date = self.get_arguments()
        rank = self.get_ranking(gameid)

        if date != None:
            rank_d = self.get_daily_ranking(rank, date)
            self.show_ranking(rank_d, gameid, date)
        else:
            self.show_ranking(rank, gameid)


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
        else:
            date = None

        return (gameid, date)

    def show_ranking(self, rank, gameid, date = None):
        root = os.path.dirname(__file__)

        self.write("<!DOCTYPE html>\n" + \
            "<html>\n" + \
            "<head>\n" + \
            "<meta charset=\"UTF-8\">\n" + \
            "<title>" + \
            gameid + " ranking"+ \
            "</title>\n" + \
            ShowRankingSite.get_css() + \
            "</head>\n" + \
            "<body>\n" + \
            ShowRankingSite.get_body(gameid, rank, date) + \
            "</body>\n" + \
            "</html>")
            

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


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/add", AddResult),
        (r"/show_ranking", ShowRanking),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()