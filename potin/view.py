from db import dbskiutc_con as db
from potin.model import Potin
from utils.errors import Error


class PotinView():
    def __init__(self):
        self.con = db()

    """
    Returns list of Potin
    :return json of list of potin
    :raise Exception
    """
    def list(self, admin = False):
        try:
            with self.con:
                cur = self.con.cursor(Model = Potin)
                if admin:
                    sql = "SELECT * from potin WHERE approved = 0 ORDER BY id DESC"
                else:
                    sql = "SELECT * from potin WHERE approved = 1 ORDER BY id DESC"
                cur.execute(sql)
                response = cur.fetchall()
                count = 0
                result = {}
                for value in response:
                    potin = value.to_json()
                    #check if anonymous
                    if potin.get('isAnonymous'):
                        potin['sender'] = None
                    result[count] = potin
                    count += 1

                return result

        except Exception as e:
            print(e)
            return Error('Problem happen in query list').get_error()

    """
    Return a potin given an id
    :param id
    :raise Exception
    """
    def get(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = Potin)
                sql = "SELECT * from potin WHERE id = %s AND approved = 1"
                cur.execute(sql, id)
                response = cur.fetchone()
                if response is None:
                    return {}
                potin = response.to_json()
                #check if anonymous
                if potin.get('isAnonymous'):
                    potin['sender'] = None

                return potin

        except Exception as e:
            print(e)
            return Error('Problem happen in query get', 400).get_error()

    """
    Create a potin given datas model
    :param data
    """
    def create(self, data):
        try:
            with self.con:
                title = data.get('title')
                text = data.get('text')
                approved = data.get('approved')
                sender = data.get('sender')
                isAnonymous = data.get('isAnonymous')
                cur = self.con.cursor(Model = Potin)
                sql = "INSERT INTO potin (title, text, approved, sender, isAnonymous) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, (title, text, approved, sender, isAnonymous))
                self.con.commit()
                sql = "SELECT * FROM potin WHERE id = (SELECT MAX(id) FROM potin)"
                cur.execute(sql)
                last = cur.fetchone()

                return last.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in potin creation', 400).get_error()

    """
    Delete a potin given an id
    :param id
    """
    def delete(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = Potin)
                sql = "DELETE FROM potin WHERE id = %s"
                cur.execute(sql, id)
                self.con.commit()

                return self.list(admin=True)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in potin deletion', 400).get_error()

    """
    Update a potin given an id
    :param id
    """
    def update(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = Potin)
                sql = "UPDATE potin SET approved = 1 WHERE id = %s"
                cur.execute(sql, id)
                self.con.commit()

                return self.get(id)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened when updating potin', 400).get_error()
