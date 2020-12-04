from adb import DB

class customer:
    def __init__(self):
        self.menu_title = '買家'
        self.menu = {
            'a':'登入或註冊',
            'b':'商品選購',
            'c':'商品目錄查詢',
            'd':'商店據點查詢',
            'e':'交易紀錄查詢',
            'f':'會員資料',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda c, s: self.login_or_signup(c, s),
            'b': lambda c, s: self.pick_out_and_buy(c, s),
            'c': lambda c, s: self.catalog_search(c, s),
            'd': lambda c, s: self.store_location(c, s),
            'e': lambda c, s: self.transaction_history(c, s),
            'f': lambda c, s: self.member_profile(c, s),

        }
        self.divider = '='*20
        self.shopping_cart = []
        self.account = ''

    def show_menu(self):
        """ 主選單
        """
        print(self.divider)
        print(self.menu_title)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def store_location(self, db, func_title):
        """ 商店據點查詢
        """
        while True:
            option = input('1.查詢 2.列表 exit.離開: ')
            if option == 'exit':
                break
            else:
                if option == '2':
                    db.list_all_store()
                    continue
                elif option == '1':
                    in_store = input('請輸入店家名稱: ')
                    db.check_store_location(in_store)
                else:
                    print('輸入錯誤')
        return func_title       
    def catalog_search(self, db, func_title):
        """商品目錄查詢
        """
        while True:
            option = input('1.查詢 2.列表 exit.離開: ')
            if option == 'exit':
                break
            else:
                if option == '2':
                    db.list_all_fruits()
                    continue
                elif option == '1':
                    in_store = input('查詢商品: ')
                    db.query_fruit(in_store)
                else:
                    print('輸入錯誤')
        return func_title
    def transaction_history(self, db, func_title):
        """交易紀錄查詢
        """
        db.list_transaction_history(self.account)
        return func_title

    def member_profile(self, db, func_title):
        """會員資料
        """
        while True:
            option = input('1.修改 2.查詢 exit.離開: ')
            if option == 'exit':
                break
            else:
                qaccount =input('請輸入會員編號: ')
                if option == '2':
                    db.show_member_profile(qaccount)
                elif option == '1':
                    db.insert_or_update_member(qaccount)
                else:
                    print('輸入錯誤')
        return func_title
            
    def login_or_signup(self, db, func_title):
        """登入或註冊
        """
        qaccount = input('請輸入會員編號: ')
        if db.check_if_member_enrolled(qaccount):
            self.account = qaccount
            db.list_member_profile(self.account)
            self.menu_title = '買家 ' + self.account      
        else:
            if db.insert_or_update_member(qaccount):
                print('註冊成功')

    def show_cart(self):
        print('購物車內所有商品: ')
        for row in self.shopping_cart:
            print(row)
        print()

    def pick_out_and_buy(self, db, func_title):
        """商品選購
        """
        db.list_all_fruits()
        while True:
            option = input('1.請輸入欲選購之商品代碼 2.檢視購物車 3.結帳 4.暫離: ')
            if option == '2':
                self.show_cart()
            elif option == '3':
                self.show_cart()
                # 結帳
                db.check_shopping_cart(self.account, self.shopping_cart)
                break
            elif option == '4':
                break
            else:
                code = option
                chosen = db.buy_fruit(code)
                if chosen == None: 
                    print('輸入錯誤')
                else:
                    pack_or_box = input('包裝類型? 1.個裝 2.盒裝: ')
                    numbers = int(input('數量: '))
                    if pack_or_box == '1':
                        order = ('個裝', numbers, chosen[2], 0, 0, numbers * chosen[2])
                    elif pack_or_box == '2':
                        order = ('盒裝', 0, 0, numbers, chosen[3], numbers * chosen[3])
                    chosen = chosen[:2] + order
                    self.shopping_cart.append(chosen)
                    print(chosen ,'已加入購物車')
            

with DB() as db:
    acustomer = customer()
    while True:
        func_id, func_name = acustomer.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            acustomer.menu_func[func_id](db,func_name)
            print()