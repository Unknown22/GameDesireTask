class ShowRankingSite(object):
    
    @staticmethod
    def get_body(gameid, rank, date):
        body = ""
        body += "<div class=\"table\">\n"
        body += "   <table class=\"table-fill\">\n"
        body += "   <thead>\n"
        body += "       <tr>\n"
        body += "           <th class=\"text-center\" colspan=\"2\">GameID: " + gameid + "</th>\n"
        body += "       </tr>\n"
        body += "   </thead>\n"

        if date != None:
            body += "       <tr>\n"
            body += "           <th class=\"text-center\" colspan=\"2\">" + str(date.date()) + "</th>\n"
            body += "       </tr>\n"

        body += "       <tr>\n"
        body += "           <th class=\"text-center\">UID</th>\n"
        body += "           <th class=\"text-center\">Game Result</th>\n"
        body += "       </tr>\n"

        for r in rank:
            body += "       <tr>\n"
            body += "           <td class=\"text-center\">" + str(r['UID']) + "</td>\n"
            body += "           <td class=\"text-center\">" + str(r['game_result']) + "</td>\n"
            body += "       </tr>\n"

        body += "   </table>\n"
        body += "</div>\n"
        return body

    @staticmethod
    def get_css():
        css = ""
        css += "<style type=\"text/css\">\n"

        css += "body {\n"
        css += "background-color: #3e94ec;\n"
        css += "font-family: helvetica, arial, sans-serif;\n"
        css += "font-size: 16px;\n"
        css += "font-weight: 400;\n"
        css += "text-rendering: optimizeLegibility;\n"
        css += "}\n\n"

        css += ".table-fill {\n"
        css += "background: white;\n"
        css += "border-radius:3px;\n"
        css += "border-collapse: collapse;\n"
        css += "height: 320px;\n"
        css += "margin: auto;\n"
        css += "max-width: 600px;\n"
        css += "padding:5px;\n"
        css += "width: 100%;\n"
        css += "box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);\n"
        css += "animation: float 5s infinite;\n"
        css += "}\n\n"
 
        css += "th {\n"
        css += "color:#D5DDE5;\n"
        css += "background:#1b1e24;\n"
        css += "border-bottom:4px solid #9ea7af;\n"
        css += "border-right: 1px solid #343a45;\n"
        css += "font-size:23px;\n"
        css += "font-weight: 100;\n"
        css += "padding:24px;\n"
        css += "text-align:left;\n"
        css += "text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);\n"
        css += "vertical-align:middle;\n"
        css += "}\n\n"

        css += "th:first-child {\n"
        css += "border-top-left-radius:3px;\n"
        css += "}\n\n"
 
        css += "th:last-child {\n"
        css += "border-top-right-radius:3px;\n"
        css += "border-right:none;\n"
        css += "}\n\n"
  
        css += "tr {\n"
        css += "border-top: 1px solid #C1C3D1;\n"
        css += "border-bottom-: 1px solid #C1C3D1;\n"
        css += "color:#666B85;\n"
        css += "font-size:16px;\n"
        css += "font-weight:normal;\n"
        css += "text-shadow: 0 1px 1px rgba(256, 256, 256, 0.1);\n"
        css += "}\n\n"
 
        css += "tr:hover td {\n"
        css += "background:#4E5066;\n"
        css += "color:#FFFFFF;\n"
        css += "border-top: 1px solid #22262e;\n"
        css += "border-bottom: 1px solid #22262e;\n"
        css += "}\n\n"
 
        css += "tr:first-child {\n"
        css += "border-top:none;\n"
        css += "}\n\n"

        css += "tr:last-child {\n"
        css += "border-bottom:none;\n"
        css += "}\n\n"
 
        css += "tr:nth-child(odd) td {\n"
        css += "background:#EBEBEB;\n"
        css += "}\n\n"
 
        css += "tr:nth-child(odd):hover td {\n"
        css += "background:#4E5066;\n"
        css += "}\n\n"

        css += "tr:last-child td:first-child {\n"
        css += "border-bottom-left-radius:3px;\n"
        css += "}\n\n"
 
        css += "tr:last-child td:last-child {\n"
        css += "border-bottom-right-radius:3px;\n"
        css += "}\n\n"
 
        css += "td {\n"
        css += "background:#FFFFFF;\n"
        css += "padding:20px;\n"
        css += "text-align:left;\n"
        css += "vertical-align:middle;\n"
        css += "font-weight:300;\n"
        css += "font-size:18px;\n"
        css += "text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);\n"
        css += "border-right: 1px solid #C1C3D1;\n"
        css += "}\n\n"

        css += "td:last-child {\n"
        css += "border-right: 0px;\n"
        css += "}\n\n"

        css += "th.text-left {\n"
        css += "text-align: left;\n"
        css += "}\n\n"

        css += "th.text-center {\n"
        css += "text-align: center;\n"
        css += "}\n\n"

        css += "th.text-right {\n"
        css += "text-align: right;\n"
        css += "}\n\n"

        css += "td.text-left {\n"
        css += "text-align: left;\n"
        css += "}\n\n"

        css += "td.text-center {\n"
        css += "text-align: center;\n"
        css += "}\n\n"

        css += "td.text-right {\n"
        css += "text-align: right;\n"
        css += "}\n\n"

        css += "</style>\n"

        return css