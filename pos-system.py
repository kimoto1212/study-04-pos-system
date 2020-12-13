import pandas as pd
import datetime

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

    # 商品名を返す
    def get_item_name(self):
        return self.item_name
    # 商品価格を返す
    def get_price(self):
        return self.price



### オーダークラス
class Order:
    def __init__(self,item_master):
        # 商品コードリスト
        self.item_order_list=[]
        # 商品名リスト
        self.item_name_list = []
        # 商品の個数リスト
        self.item_quantity_list=[]
        # 商品の価格リスト
        self.item_price_list = []
        # 合計金額
        self.total_fee=0
        # 合計個数
        self.sum=0
        # 商品クラスの関数の呼び出しができるリストitem_masterを格納する
        self.item_master=item_master

    # 商品コード受け取り
    def add_item_order(self,item_code):
        self.item_order_list.append(item_code)

    # 商品個数受け取り
    def add_item_quantity(self,item_quantity):
        self.item_quantity_list.append(item_quantity)

    def view_item_list(self):
        print("オーダー登録した商品の一覧")
        for (item,i,quantity) in zip(self.item_order_list,range(0,len(self.item_master)),self.item_quantity_list):
            print("商品コード:{}".format(item))
            print("商品名:{}".format(self.item_master[i].get_item_name()))
            self.item_name_list.append(self.item_master[i].get_item_name())
            print("商品価格:{}".format(self.item_master[i].get_price()))
            self.item_price_list.append(self.item_master[i].get_price())
            # 個数の合計を計算
            self.sum+=int(quantity)
            # 合計金額を計算
            self.total_fee+=int(self.item_master[i].get_price())*int(quantity)
        print("\n合計金額:{}".format(self.total_fee))
        print("商品の合計個数:{}".format(self.sum))


    def change_calculation(self,eposit_amount):
        # お釣りの計算
        self.chamge = int(eposit_amount) - self.total_fee
        print("お釣りは{}です".format(self.chamge))

        now = datetime.datetime.now()
        receipt_file_name = "./log_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"
        with open(receipt_file_name, "w") as f:
            f.write("商品名,商品価格\n")
            for (name,price,quantity) in zip(self.item_name_list,self.item_price_list,self.item_quantity_list):
                f.write("{}...{}円 × {}\n".format(name,price,quantity))
            f.write("\n合計個数...{}個\n".format(self.sum))
            f.write("合計金額...{}円\n".format(self.total_fee))
            f.write("お預かり金額...{}円\n".format(eposit_amount))
            f.write("お釣り...{}円\n".format(self.chamge))




### メイン処理
def main():
    # マスタ登録

    item_master=[]
    # csv読み取り
    df = pd.read_csv("./Master_registration.csv")
    # 商品名だけ取り出す
    item_name = df["name"]
    # 商品価格だけ取り出す
    item_price = df["price"]
    # マスタ登録開始
    for (i,name,price) in zip(range(1,len(item_name)+1),item_name,item_price):
        item_master.append(Item(("00"+str(i)),name,price))
        # print(("00"+str(i)),name,price)

    # オーダー登録
    order=Order(item_master)
    for i in range(0,len(item_master)):
        input_oder = str(input("商品コードを入力して下さい："))
        input_quantity = str(input("商品の個数を入力して下さい："))
        order.add_item_order(input_oder)
        order.add_item_quantity(input_quantity)


    # オーダー表示
    order.view_item_list()

    eposit_amount = input("お客様からのお預かり金額を入力してください：")
    order.change_calculation(eposit_amount)

if __name__ == "__main__":
    main()
