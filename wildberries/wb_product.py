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
        if self.nm_id == 113298574:
            price = int(self.kalibron_price)
            if price > 0:
                return {'nmId': self.nm_id,
                        'price': int(self.kalibron_price) + 67}
            else:
                return {'nmId': self.nm_id,
                        'price': int(self.kalibron_price)}
        else:
            if int(self.kalibron_price) > 0:
                return {'nmId': self.nm_id,
                        'price': int(self.kalibron_price) + 66}
            else:
                return {'nmId': self.nm_id,
                        'price': int(self.kalibron_price)}

    def convert_to_stock_update(self):
        #if self.__calculate_quantity(self.kalibron_quantity) > 0:
        return {'sku': self.skus,
                'amount': self.__calculate_quantity(self.kalibron_quantity)}

    @staticmethod
    def __calculate_quantity(quantity) -> int:
        result = 0
        if int(quantity) >= 10:
            result = int(int(quantity) / 100 * 20)
        return result

    def convert_to_excel(self):
        return {'Артикул_tdk': self.vendor_code,
                'Артикул_wb': self.nm_id,
                'Цена_tdk': self.kalibron_price,
                'Цена_wb': self.wb_price,
                'Остаток_tdk': self.__calculate_quantity(self.kalibron_quantity),
                'Остаток_wb': self.wb_quantity,
                'Штрихкод': self.skus}

