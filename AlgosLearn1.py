class Product:
    def __init__(self, name, product_id, category, price):
        self.name = name
        self.product_id = product_id
        self.category = category
        self.price = price

class Inventory:
    def __init__(self):
        self.__products = {}
    
    def add_product(self, product):
        if product.product_id in self.__products:
            print("Error")
        else:
            self.__products[product.product_id] = product

    def find_by_id(self, product_id): # O(1)
        if product_id in self.__products:
            return self.__products[product_id] 
        else:
            return None
        
    def get_products_by_category(self, category): # O(n)
        product_list = []
        for j in self.__products.values():
            if category == j.category:
                product_list.append(j.name)
       
        return product_list
        

if __name__ == '__main__':
    sklad = Inventory()
    book = Product("GroksAlgoritms", "1GH4JH", "Books", 94)
    electronics = Product("MatPlate", "4SXHKD", "Electronics", 299)
    sklad.add_product(electronics)
    sklad.add_product(book)
    sklad.add_product(book)
    print(sklad.get_products_by_category("Electronics")) 
    print(sklad.get_products_by_category("Books"))
    print(f"Name: {sklad.find_by_id('1GH4JH').name} | Price: {sklad.find_by_id('1GH4JH').price}")
    print(sklad.find_by_id("JGKFSD"))