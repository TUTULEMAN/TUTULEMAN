class Order:
    def __init__(self, trader_id, price, quantity):
        self.trader_id = trader_id
        self.price = price
        self.quantity = quantity

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order, order_type):
        if not self.validate_order(order):
            return
        if order_type == 'buy':
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda x: x.price, reverse=True)
        elif order_type == 'sell':
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda x: x.price)
        self.match_orders()

    def validate_order(self, order):
        return order.price > 0 and order.quantity > 0

    def match_orders(self):
        while self.buy_orders and self.sell_orders and self.buy_orders[0].price >= self.sell_orders[0].price:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]
            quantity = min(buy_order.quantity, sell_order.quantity)
            print(f'Matched {quantity} from {buy_order.trader_id} (buy) and {sell_order.trader_id} (sell)')
            buy_order.quantity -= quantity
            sell_order.quantity -= quantity
            if buy_order.quantity == 0:
                self.buy_orders.pop(0)
            if sell_order.quantity == 0:
                self.sell_orders.pop(0)

    def view_book(self):
        print('Buy orders:')
        for order in self.buy_orders:
            print(f'Trader: {order.trader_id}, Price: {order.price}, Quantity: {order.quantity}')
        print('Sell orders:')
        for order in self.sell_orders:
            print(f'Trader: {order.trader_id}, Price: {order.price}, Quantity: {order.quantity}')
