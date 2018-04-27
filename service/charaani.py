from logging import getLogger

import requests
from bs4 import BeautifulSoup


try:
    LOGLEVEL
except NameError:
    LOGLEVEL = "INFO"

logger = getLogger(__name__)
logger.setLevel(LOGLEVEL)


class Charaani:
    urls = {
            'top': 'https://akb48.chara-ani.com/top.aspx',
            'login': 'https://akb48.chara-ani.com/login.aspx',
            'logout': 'https://akb48.chara-ani.com/logout.aspx',
            'history': 'https://akb48.chara-ani.com/akb_history.aspx',
            }

    def login(self, username, password):
        print('login(%s, %s)' % (username, password))
        self.s = requests.Session()
        pre = self.s.get(self.urls['login'])
        hidden_data = self._find_hidden(pre.text)
        postdata = hidden_data
        postdata['ScriptManager1'] = 'ScriptManager1%7CbtnLogin'
        postdata['txID'] = username
        postdata['txPASSWORD'] = password
        postdata['btnLogin.x'] = '173'
        postdata['btnLogin.y'] = '30'
        res = self.s.post(self.urls['login'], data=postdata)

        soup = BeautifulSoup(res.text, "html.parser")
        username_el = soup.find(attrs={"id": "lblUserName"})
        if username_el is None:
            logger.info("login faild")
            return
        self.displayName = username_el.text

        print(self.displayName)
        self.cookies = res.cookies

    def is_login(self):
        try:
            self.cookies
        except AttributeError:
            return False
        res = self.s.get(self.urls['top'], cookies=self.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        username_el = soup.find(attrs={"id": "lblUserName"})
        if username_el is None:
            return False
        return True


    def fetch_recode(self, maxpage=3):
        page = 1
        print('fetch')
        res = self.s.get(self.urls['history'], cookies=self.cookies)
        records = self._scrape_recods(res.text)
        self.cookies = res.cookies
        while page <= 3:
            page = page + 1
            postdata = self._find_hidden(res.text)
            postdata['__EVENTARGUMENT'] = 'Page$%s' % page
            postdata['__EVENTTARGET'] = 'dgvList'
            res = self.s.post(self.urls['history'],
                              cookies=self.cookies,
                              data=postdata)
            records = records + self._scrape_recods(res.text)

        return records

    def _scrape_recods(self, html):
        soup = BeautifulSoup(html, "html.parser")
        history_table_el = soup.find("table", attrs={"class", "history_table"})
        cols = history_table_el.find_all("tr")
        records = []
        for col in cols:
            if col.get("class") is not None:
                continue
            rows = col.find_all("td")
            if len(rows) != 8:
                continue
            record = {
                    "id": rows[1].text,
                    "num": rows[4].text,
                    "state": rows[6].text,
                    }
            row2 = rows[2].text.split(" ")
            record['date'] = row2[0]
            record['member'] = row2[1]
            record['bu'] = row2[2]
            print(record)
            records.append(record)
        print(records)
        return records

    def _find_hidden(self, html):
        soup = BeautifulSoup(html, "html.parser")
        input_els = soup.find_all("input")
        hidden_data = {}
        for input_el in input_els:
            _type = input_el.get("type")
            if _type in "hidden":
                hidden_data[input_el.get("name")] = input_el.get("value")

        return hidden_data


if __name__ == '__main__':
    c = Charaani()
    c.login("username", "password")
    if c.is_login():
        c.fetch_recode()
    else:
        print("login fail")

