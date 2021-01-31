# DAO: Data Access Object
import math
from models import AddressBookEntry


class Pagination:
    def __init__(self, total_count, total_page, datas):
        self.total_count = total_count
        self.total_page = total_page
        self.datas = datas


class AddressBookDao:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_total_count(self):
        query = 'select count(*) from addressbook'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_list(self, start, perpage):
        query = f"select * from addressbook order by name limit {start},{perpage}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()  # 데이터가 있을때: ((,,),...), 없을때: ()
        # 컴프리핸션을 이용한 변환
        return (AddressBookEntry(*row) for row in rows)

    def get_page(self, page, perpage):
        start = (page-1)*perpage
        total_count = self.get_total_count()
        total_page = math.ceil(total_count/perpage)
        rows = self.get_list(start, perpage)

        return Pagination(total_count, total_page, rows)

    def get(self, num):
        query = f"select * from addressbook where num={num}"
        self.cursor.execute(query)
        row = self.cursor.fetchone()  # (튜플) or None
        if row:
            return AddressBookEntry(*row)
        else:
            return None

    def search(self, keyword):
        keyword = keyword.lower()
        query = f"select * from addressbook where lower(name) like '%{keyword}%'"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return (AddressBookEntry(*row) for row in rows)

    def add(self, name, phone, email, addr):
        query = f"insert into addressbook (name,phone,email,addr) values ('{name}','{phone}','{email}','{addr}')"
        return self.cursor.execute(query)
        


        
    def update(self,num,name,phone,email,addr):
        query = f"UPDATE addressbook SET name='{name}', phone ='{phone}', email='{email}', addr='{addr}' WHERE num = '{num}'"
        return self.cursor.execute(query)

    def delete(self,name):
        query = f"DELETE FROM addressbook WHERE name = '{name}'"
        return self.cursor.execute(query)
