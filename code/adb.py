class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.title_side = '-'*12

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """ 開啟資料庫連線
        """
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('fruit.db')
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """ 關閉資料庫連線
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def get_today(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def get_max_id(self, arg_table, arg_column):
        """ 取得資料最新編號
        """
        self.cur.execute("SELECT MAX({}) FROM {}".format(arg_column, arg_table))
        row_id = self.cur.fetchone()[0]
        if row_id == None:
            return 1
        return row_id + 1

    def get_count_id(self, arg_table, arg_column, arg_value):
        """ 檢查資料編號是否存在
        """
        self.cur.execute("SELECT COUNT(*) FROM {} WHERE {}='{}'".format(arg_table, arg_column, arg_value))
        return self.cur.fetchone()[0]

    def list_all_fruits(self):
        """水果列表
        """
        self.cur.execute("SELECT * FROM FRUIT")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def insert_or_update_fruit(self, in_code, in_fruit, in_pri_pack, in_pri_box):
        """水果增修
        """
        self.cur.execute("SELECT COUNT(*) FROM FRUIT WHERE FRUIT_CODE=?", (in_code,))
        count_result = self.cur.fetchone()[0]
        if count_result == 0:
            self.cur.execute("INSERT INTO FRUIT VALUES (?, ?, ?, ?)", 
                (in_code, in_fruit, in_pri_pack, in_pri_box))
        elif count_result > 0:
            self.cur.execute("UPDATE FRUIT SET FRUIT_NAME=?, PRICE_PACK=?, PRICE_BOX=? WHERE FRUIT_CODE=?", 
                (in_fruit, in_pri_pack, in_pri_box, in_code))
        return self.conn.commit()


    def query_fruit(self, in_fruit):
        """查詢水果
        """
        self.cur.execute("SELECT * FROM FRUIT WHERE FRUIT_NAME LIKE '%{}%'".format(in_fruit))
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def delete_fruit(self,arg_word):
        """刪除水果
        """
        self.cur.execute("DELETE FROM FRUIT WHERE FRUIT=?", (in_fruit,))
        return self.conn.commit()

    def transaction_history(self):
        """交易紀錄
        """
        self.cur.execute("SELECT * FROM SALES")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def list_all_store(self):
        """商店據點列表
        """
        self.cur.execute("SELECT * FROM STORE")
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def insert_or_update_store(self, in_id, in_store, in_address, in_tel, in_hours):
        """商店增修
        """
        self.cur.execute("SELECT COUNT(*) FROM STORE WHERE STORE_ID=?", (in_id,))
        count_result = self.cur.fetchone()[0]
        if count_result == 0:
            self.cur.execute("INSERT INTO STORE VALUES (?, ?, ?, ?, ?)", 
                (in_id, in_store, in_address, in_tel, in_hours))
        elif count_result > 0:
            self.cur.execute("UPDATE STORE SET STORE_NAME=?, STORE_ADDRESS=?, STORE_TEL=?, BUSINESS_HOURS=? WHERE STORE_ID=?", 
                (in_store, in_address, in_tel, in_hours, in_id))
        return self.conn.commit()

    def delete_store(self, in_id):
        self.cur.execute("DELETE FROM STORE WHERE STORE_ID=?", (in_id,))
        return self.conn.commit()

    def check_store_location(self, in_id, in_store):
        """商店據點查詢 A ''
        """
        in_id = '' if in_id == '' else '%{}%'.format(in_id)
        in_store = '' if in_store == '' else '%{}%'.format(in_store)
        self.cur.execute("SELECT * FROM STORE WHERE STORE_ID LIKE ? OR STORE_NAME LIKE ?", (in_id, in_store))
        print(self.cur.fetchall())

    def list_transaction_history(self, account_id):
        """交易紀錄列表
        """
        account_id = ''.join(('%', account_id, '%'))
        self.cur.execute("SELECT * FROM SALES WHERE MEMBER_ID LIKE ?", (account_id,))
        all_rows = self.cur.fetchall()
        if len(all_rows) > 0:
            for row in all_rows:
                print(row)
        else:
            print(account, '查無任何交易紀錄')

    def list_member_profile(self, account_id):
        """會員資料列表
        """
        # 改成 LIKE 模糊查詢
        self.cur.execute("SELECT * FROM MEMBERS WHERE MEMBER_ID=?", (account_id,))
        all_rows = self.cur.fetchall()
        for row in all_rows:
            print(row)
        print()

    def show_member_profile(self, account_id):
        """查詢會員資料
        """
        self.cur.execute("SELECT * FROM MEMBERS WHERE MEMBER_ID=?", (account_id,))
        member_info = self.cur.fetchone()
        print(member_info)
        print()

    def check_if_member_enrolled(self, account_id):
        """ 檢查會員是否註冊
        """
        self.cur.execute("SELECT COUNT(*) FROM MEMBERS WHERE MEMBER_ID=?", (account_id,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def insert_or_update_member(self, account_id):
        """ 增修會員
        """
        full_name = input('名稱: ')
        if full_name == 'q':
            return False

        while True:
            birth_year = input('出生年: ')
            if birth_year.isdigit():
                birth_year = int(birth_year)
                if 2020 >= birth_year >= 1950:
                    break
                else:
                    print('出生年應介於 1950-2020 之間')
            
        while True:          
            gender = input('性別(F.女性 M.男性): ').upper()    
            if gender in ('F', 'M'):
                break
            else:
                print('輸入錯誤')

        is_member = self.get_count_id('MEMBERS', 'MEMBER_ID', account_id)
        # 資料無誤，准許註冊            
        if is_member in (0, 1):
            if is_member == 0:
                self.cur.execute("INSERT INTO MEMBERS VALUES (?, ?, ?, ?)", 
                    (account_id, full_name, gender, birth_year))
            elif is_member == 1:
                self.cur.execute("UPDATE MEMBERS SET MEMBER_NAME=?, GENDER=?, BIRTH_YEAR=? WHERE MEMBER_ID=?", 
                    (full_name, gender, birth_year, account_id))
            self.conn.commit()
            return True
        else:
            return False

    def check_fruit_code(self, account_id):
        """確認水果代碼
        """
        self.cur.execute("SELECT COUNT(*) FROM FRUIT WHERE FRUIT_CODE=?", (account_id,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def buy_fruit(self, code):
        """水果選購
        """
        if self.check_fruit_code(code):
            self.cur.execute("SELECT * FROM FRUIT WHERE FRUIT_CODE LIKE ?", (code,))
            return self.cur.fetchone()

    def check_shopping_cart(self, account, shopping_cart):
        """結帳函式
        """
        today = self.get_today()
        folo_id = self.get_max_id('SALES','FOLIO')
        for order in shopping_cart:
            self.cur.execute("INSERT INTO SALES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (today, account, folo_id, order[0]) + order[3:])
        self.conn.commit()