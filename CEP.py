import pandas as pd
from abc import ABC, abstractmethod
import os

# Class to create account of users and save their details in a file.


class user_account:
    def __init__(self):
        self.user_details = []
        self.loggedin = False

    def register(self):
        self.name = input('Enter your name = ')
        self.ph = int(input('Enter phone number = '))
        self.email = input("Enter your email = ")
        self.address = input('Enter your address = ')
        self.username = input("Enter username = ")
        self.pw = input('Enter passwaord b/w 5 to 10 characters = ')
        if len(str(self.pw)) < 5 or len(str(self.pw)) > 10:
            print("invalid password!!!")
            self.pw = input("Enter passwaord b/w 5 to 10 characters = ")
        self.user_details = [self.name, self.email,
                             self.ph, self.address, self.username, self.pw]

    def user_file(self):
        with open(f'{self.username}.txt', 'w') as f:
            f.write(str(self.user_details[0])+' '+str(self.user_details[1])+' '+str(self.user_details[2])+' '+str(
                self.user_details[3])+' '+str(self.user_details[4])+' '+str(self.user_details[5]))

    def login(self):
        self.username = input("Enter Username: ")
        self.pw = input("Enter Passwaord: ")
        try:
            f = open(f'{self.username}.txt')
        except FileNotFoundError:
            print('This user does not exist!!!')
            choice = input('Do you want to create new account? (YES/NO) :')
            if choice == 'YES' or choice == 'Yes' or choice == 'yes':
                print()
                print('Create New Account...')
                self.register()
                self.user_file()
                administration.write_account_holder_details(self)
                self.login()
            elif choice == 'NO' or choice == 'No' or choice == 'no':
                print('Enter valid username')
                self.login()
        else:
            with open(f'{self.username}.txt', 'r') as f:
                details = f.read()
                self.user_details = details.split('\n')
                if str(self.username) in str(self.user_details):
                    if str(self.pw) in str(self.user_details):
                        self.loggedin = True
        if self.loggedin == True:
            print(f'{self.username} logged in')
        else:
            print("wrong details")

    def display(self):
        self.username = input('Enter name of the user =')
        with open(f'{self.username}.txt', 'r') as f:
            try:
                f = open(f'{self.username}.txt')
            except FileNotFoundError:
                print('This user does not exist!!!')
                print('Enter valid username')
                self.display()
            else:
                details = f.read()
                details = details.split()
                print()
                print(f'{self.username}\'s shopping history...')
                print('Name =', details[0])
                print('Email Address =', details[1])
                print('Phone No. =', details[2])
                print('Address =', details[3])


# Class of administration of the store.
# This class will be aggregated with class user_account.
class administration(user_account):    
    
    def products_details(self):
        self.products = {
            "Product name": ["Mouse", 'Keyboard', 'HeadPhones', 'LED', 'Printer', 'Harddrive', 'RAM', 'Scanner', 'Mouse Pad', 'Web Cam'],
            'Price in RS/.': [600, 800, 1200, 10000, 5000, 2000, 3000, 4000, 200, 500],
            'Quantity': [10, 15, 20, 25, 20, 30, 30, 15, 50, 20],
        }
        self.df = pd.DataFrame(self.products)
        self.df.index = [i for i in range(1, len(self.df.values)+1)]
        return self.df

    def add_product(self):
        name = input('Enter product to be added :')
        price = int(input('Price of the product :'))
        quantity = int(input('quantity of product: '))
        # self.df.loc[len(self.df.index)]=[name,price]
        self.df = self.df.append(
            {'Product name': name, 'Price in RS/.': price, 'Quantity': quantity}, ignore_index=True)
        self.df.index = [i for i in range(1, len(self.df.values)+1)]
        return self.df

    def remove_product(self):
        name = input('Enter product to remove :')
        filt = self.df[self.df['Product name'] == name].index
        self.df.drop(filt, inplace=True)
        return self.df
    
    def increase_quantity(self):
        name = input('product name: ')
        quantity = int(input('quantity of product: '))
        a = self.products['product name'].index(name)
        self.products['quantity'][a] = self.products['quantity'][a]+quantity
        self.df = pd.DataFrame(self.products)
        return self.df

    def decrease_quantity(self):
        name = input('product name: ')
        quantity = int(input('quantity of product: '))
        a = self.products['product name'].index(name)
        self.products['quantity'][a] = self.products['quantity'][a]-quantity
        self.df = pd.DataFrame(self.products)
        return self.df

    def increase_price(self):
        name = input('product name: ')
        price = int(input('price of product: '))
        a = self.products['product name'].index(name)
        self.products['price'][a] = self.products['price'][a]+price
        self.df = pd.DataFrame(self.products)
        return self.df

    def decrease_price(self):
        name = input('product name: ')
        price = int(input('price of product: '))
        a = self.products['product name'].index(name)
        self.products['price'][a] = self.products['price'][a]-price
        self.df = pd.DataFrame(self.products)
        return self.df

    def write_account_holder_details(self):
        a=getattr(u,'username')
        with open(f'{a}.txt', 'r') as fr:
            try:
                fr = open(f'{a}.txt')
            except FileNotFoundError:
                print('This user does not exist!!!')
                print('Enter valid username')
                self.write_account_holder_details()
            else:
                details = fr.read()
                user_details = details.split('\n')
                with open(f'Account Holders.txt', 'a+') as fw:
                    for line in user_details:
                        fw.write(line+'\n')

    def read_account_holder_details(self):
        with open('Account Holders.txt', 'r') as f:
            details = f.read()
            user_details = details.split('\n')
            for line in user_details:
                print('Name Email Contact Address Username Password')
                print(line)


# Class of the shopping cart.
# This class will be inherited from class user_account.
class shopping_cart(user_account):

    def __init__(self):
        self.cart = []
        self.product_list = []
        self.quantity_list = []
        self.price_list = []

        self.totalprice = 0

    def menu(self):
        products = {"Product name": ["Mouse", 'Keyboard', 'HeadPhones', 'LED', 'Printer', 'Harddrive', 'RAM', 'Scanner', 'Mouse Pad', 'Web Cam'],
                    'Price in RS/.': [600, 800, 1200, 10000, 5000, 2000, 3000, 4000, 200, 500],
                    'Quantity': [10, 15, 20, 25, 20, 30, 30, 15, 50, 20],
                    }
        df = pd.DataFrame(products)
        df.index = [i for i in range(1, len(df.values)+1)]
        print(df)
        print('Press 11 to proceed for checkout...')

    def shopping(self):
        opt = int(input('Enter your choice: '))
        if opt == 1:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*600
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Mouse', 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 2:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*800
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Keyboard',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 3:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*1200
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Headphones',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 4:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*10000
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'LED', 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 5:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*5000
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Printer',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 6:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*2000
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Harddrive',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 7:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*3000
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'RAM', 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 8:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*4000
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Scanner',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 9:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*200
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Mouse Pad',
                 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 10:
            self.product = input('Enter name of product: ')
            self.product_list.append(self.product)
            self.quantity = int(input('Enter quantity: '))
            self.quantity_list.append(self.quantity)
            self.price = self.quantity*500
            self.price_list.append(self.price)
            self.totalprice = self.totalprice+self.price
            a = {'product': 'Webcam', 'quantity': self.quantity, 'price': self.price}
            self.cart.append(a)
            self.shopping()
        if opt == 11:
            #print('Your shopping cart details...')
            self.cart_info()
            choice = input('Do you wish to do more shopping? (YES/NO) :')
            if choice == 'yes' or choice == 'YES' or choice == 'Yes':
                self.menu()
                self.shopping()
            else:
                print(f'Total bill = {self.totalprice}')
                print('THANKS FOR SHOPPING !!!')

    def add_product(self):
        print('Add Product')
        self.menu()
        self.shopping()

    def remove_product(self):
        self.cart_info()
        a=getattr(u,'username')
        self.product = input('Enter product to remove =')
        j = 0
        for i in self.product_list:
            if i == self.product:
                self.product_list.remove(self.product)
                break
            else:
                j += 1

        self.totalprice = self.totalprice-self.price_list[j]
        self.quantity_list.remove(self.quantity_list[j])
        self.price_list.remove(self.price_list[j])
        self.cart_info()
        self.user_file()

    def cart_info(self):
        print()
        #username = input('Enter your username =')
        a=getattr(u,'username')
        print()
        print(f'{a}\'s shopping cart...')
        cart = {'Product': self.product_list, 'Quantity': self.quantity_list,
                'Price': self.price_list
                }
        cart_df = pd.DataFrame(cart)
        cart_df.index = [i for i in range(1, len(self.product_list)+1)]
        print(cart_df)
        print()
        return

    def product_review(self):
        self.reviewer = input('Enter your username: ')
        self.stars = int(input('Rate the products (0-5) :'))
        self.rating = "*"*self.stars
        self.review = input('Write your review :')

    def print_view(self):
        print(f'{self.reviewer}\'s review: {self.review}')
        print(f'Ratings = {self.rating}')

    def user_file(self):
        print()
        a=getattr(u,'username')
        print()
        with open(f'{a} products.txt', 'w') as f:
            for i in self.product_list:
                f.write(str(i) + ' ')

        with open(f'{a} quantity.txt', 'w') as f:
            for i in self.quantity_list:
                f.write(str(i) + ' ')

        with open(f'{a} price.txt', 'w') as f:
            for i in self.price_list:
                f.write(str(i) + ' ')
    
    def user_history(self):
        a=getattr(u,'username')
        with open(f'{a} products history.txt','a+') as f:
            for i in self.product_list:
                f.write(i + ' ')
        
        with open(f'{a} price history.txt','a+') as f:
            for i in self.price_list:
                f.write(str(i) + ' ')
        
        with open(f'{a} quantity history.txt','a+') as f:
            for i in self.quantity_list:
                f.write(str(i) + ' ')

    def display(self):
        super().display()
        with open(f'{self.username} products history.txt', 'r') as f:
            details = f.read()
            details1 = details.split()

        with open(f'{self.username} quantity history.txt', 'r') as f:
            details = f.read()
            details2 = details.split()

        with open(f'{self.username} price history.txt', 'r') as f:
            details = f.read()
            details3 = details.split()

        cart = {'Product': details1, 'Quantity': details2,
                'Price': details3
                }
        cart_df = pd.DataFrame(cart)
        cart_df.index = [i for i in range(1, len(details1)+1)]
        print(cart_df)

    def clear_cart(self):
        self.cart.clear()
        self.product_list.clear()
        self.quantity_list.clear()
        self.price_list.clear()
        return


# An abstract class which is inherited from class ABC.
class abstract(ABC):
    @abstractmethod
    def payment(self):
        pass

# Class inherited from abstract class.


class checkout(abstract):

    def payment(self):
        name = input('Enter your full name =')
        phone = input('Enter your contact number =')
        city = input('Enter your city =')
        area = input('Enter your area =')
        address = input('Enter your address =')
        print('How would you like to pay...',
              '\n1 : By Cash', '\n2 : By Credit Card.')
        choice = int(input('Enter your choice ='))
        if choice == 1:
            print()
            print('*'*5, 'YOUR PURCHASE RECEIPT', '*'*5)
            print('Name =', name)
            print('Contact No =', phone)
            print('Address =', address)
            print('City =', city)
            print('Area =', area)
            print('Payment Method = By Cash')
            a=getattr(u,'username')
            with open(f'{a} price.txt', 'r') as f:
                price = f.read()
                bill = price.split()
                i = 0
                for i in range(0, len(bill)):
                    bill[i] = int(bill[i])
                print('Total Bill =', sum(bill))
            print('Your order will be delivered in due time.')
            print(f'{a} logged out!!!')
        elif choice == 2:
            print('Enter credit card details...')
            pin = input('Enter pin =')
            print()
            print('*'*5, 'YOUR PURCHASE RECEIPT', '*'*5)
            print('Name =', name)
            print('Contact No =', phone)
            print('Address =', address)
            print('City =', city)
            print('Area =', area)
            print('Payment Method = By Card')
            a=getattr(u,'username')
            with open(f'{a} price.txt', 'r') as f:
                price = f.read()
                bill = price.split()
                i = 0
                for i in range(0, len(bill)):
                    bill[i] = int(bill[i])
                print('Total Bill =', sum(bill))
            print('Your order will be delivered in due time.')
            print(f'{a} logged out!!!')


u = user_account()
a = administration()
s = shopping_cart()
x = checkout()


print('*'*75)
print('*'*16, 'WELCOME TO BRAIN TECH COMPUTER STORE...', '*'*18)
print()
print()
while True:
    print('1 : LOGIN AS ADMINISTRATOR.', '\n2 : LOGIN AS USER.',
          '\n3 : CREATE NEW ACCOUNT.', '\n Press e to exit.')
    print()
    choice = input('Enter your choice =')
    print()
    if choice == str(1):
        while True:
            print('Do you want to...', '\n1 : Add Product.', '\n2 : Remove Product.', '\n3 : Increase Quantity.', '\n4 : Decrease Quantity.',
                  '\n5 : Increase Price.', '\n6 : Decrease Price.', '\n7 : Account Holders Details.','\n8 : Show user shopping history', '\nPress e to exit.')
            choice = input('Enter your choice =')
            if choice == str(1):
                print(a.products_details())
                print(a.add_product())
            elif choice == str(2):
                print(a.products_details())
                a.remove_product()
            elif choice == str(3):
                print(a.products_details())
                a.increase_quantity()
            elif choice == str(4):
                print(a.products_details())
                a.decrease_quantity()
            elif choice == str(5):
                print(a.products_details())
                a.increase_price()
            elif choice == str(6):
                print(a.products_details())
                a.decrease_price()
            elif choice == str(7):
                a.read_account_holder_details()
            elif choice == str(8):
                s.display()    
            elif choice == 'e':
                break

    elif choice == str(2):
        u.login()
        print()
        print(f'    WE HAVE THE FOLLOWING ITEMS...')
        print()
        s.menu()
        s.clear_cart()
        s.shopping()
        s.user_file()
        #s.user_history()
        while True:
            print('1 : Add product to your cart.', '\n2 : Remove product from your cart.',
                  '\n3 : Show cart details.', '\n4 : Give your feedback.','\n5 : Proceed to checkout.')
            choice = input('Enter your choice =')
            if choice == str(1):
                s.add_product()
                s.user_file()
            elif choice == str(2):
                s.remove_product()
            elif choice == str(3):
                s.cart_info()
            elif choice == str(4):
                print('GIVE YOUR FEEDBACK HERE...')
                s.product_review()
            elif choice == str(5):
                x.payment()
                s.user_history()
                print()
                break
    elif choice == str(3):
        u.register()
        u.user_file()
        a.write_account_holder_details()
        print()
    elif choice == 'e':
        print('HAVE A GOOD DAY!!! ')
        # s.clear_cart()
        break
