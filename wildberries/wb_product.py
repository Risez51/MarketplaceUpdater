class Product:
    def __init__(self):
        # Наш код товара
        self.vendor_code = ''
        # Код товара на вб
        self.nm_id = ''
        # Цена на сайте калиброн
        self.kalibron_price = ''
        # Остатки товара калиброн
        self.kalibron_quantity = ''
        # Цена товара на вб
        self.wb_price = ''
        # Остатки товара на вб
        self.wb_quantity = ''
        # SKUs
        self.skus = ''

    def __str__(self):
        return f'Артикул_tdk: {self.vendor_code};' \
               f'Артикул_wb: {self.nm_id};' \
               f'Цена_tdk: {self.kalibron_price};' \
               f'Цена_wb: {self.wb_price};' \
               f'Остаток_tdk: {self.kalibron_quantity};' \
               f'Остаток_wb: {self.wb_quantity};' \
               f'Штрихкод: {self.skus}'

    def convert_to_price_update(self):
        return {'nmId': self.nm_id,
                'price': self.kalibron_price}

    def convert_to_stock_update(self):
        return {'sku': self.skus,
                'amount': self.__calculate_quantity(self.kalibron_quantity)}

    @staticmethod
    def __calculate_quantity(quantity) -> int:
        result = 0
        if int(quantity) >= 10:
            result = int(int(quantity) / 100 * 20)
        return result