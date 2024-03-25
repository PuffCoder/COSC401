
class Car:
    def __init__(self, brand, year):
        self.brand = brand  # 汽车品牌
        self.year = year    # 生产年份

    def display_info(self):
        print(f"这辆车是{self.year}年生产的{self.brand}。")


car1 =  Car("Toyota","2018");
car1.display_info()

