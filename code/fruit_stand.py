from adb import DB

class FruitStand():
    def __init__(self):
        self.menu_title = '賣家'
        self.menu = {
            'a':'商店資訊(列表/修改)',
            'b':'商品管理',
            'c':'交易紀錄(條件查詢/統計)',
            'd':'會員資料(列表)',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda c, s: self.store_info(c, s),
            'b': lambda c, s: self.manage_goods(c, s),
            'c': lambda c, s: self.transaction_history(c, s),
            'd': lambda c, s: self.members(c, s),
        }
        self.divider = '='*20

    def show_menu(self):

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

    def store_info(self, db, func_title):
        """商店資訊(列表/修改)
        """
        print('商店資訊')
        while True:
            subot = input('1.增修 2.查詢 3.刪除 4.列表 exit.離開: ')
            if subot == 'exit':
                break
            else:
                if subot == '4':
                    db.list_all_store()
                    continue

                if subot in ('1','2','3'):
                    in_id = input('商店ID:') 

                if subot == '1': 
                    in_store = input('商店名稱:')
                    in_address = input('商店地址:')
                    in_tel = input('商店電話:')
                    in_hours = input('營業時間:')
                    db.insert_or_update_store(in_id, in_store, in_address, in_tel, in_hours)
                    db.check_store_location(in_id, in_store)
                elif subot == '2':
                    in_store = input('商店名稱:')
                    db.check_store_location(in_id, in_store)
                elif subot == '3':
                    db.delete_store(in_id)
                else:
                    print('輸入錯誤')
            return func_title
    def manage_goods(self, db, func_title):
        """商品管理
        """
        print('商品管理')
        while True:
            subot = input('1.增修 2.查詢 3.刪除 4.列表 exit.離開: ')
            if subot == 'exit':
                break
            else:
                if subot == '4':
                    db.list_all_fruits()
                    continue

                if subot in('1','2','3'):
                    in_fruit = input('水果:') 

                if subot == '1': 
                    in_code = input('水果代碼:')
                    in_pri_pack = int(input('水果個裝價錢:'))
                    in_pri_box = int(input('水果盒裝價錢:'))
                    db.insert_or_update_fruit(in_code, in_fruit, in_pri_pack, in_pri_box)
                    db.check_fruit_out(in_code)
                elif subot == '2':
                    db.check_fruit_out(in_fruit)
                elif subot == '3':
                    db.delete_fruit(in_fruit)
                else:
                    print('輸入錯誤')
            return func_title
    def transaction_history(self, db, func_title):
        """交易紀錄(條件查詢)
        """
        account_id = input('請輸入會員編號: ')
        print('交易紀錄')
        db.list_transaction_history(account_id)
        return func_title

    def members(self, db, func_title):
        """會員資料(列表)
        """
        print('會員資料')
        db.list_member_profile()
        return func_title

with DB() as db:
    afruitstand = FruitStand()
    while True:
        func_id, func_name = afruitstand.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            afruitstand.menu_func[func_id](db,func_name)
            print()