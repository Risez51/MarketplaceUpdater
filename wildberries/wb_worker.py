from wildberries.wb_handler import WbHandler
from kalibron_handler import KalibronHandler
import api_config


class WbWorker:
    def __init__(self):
        # Получение списка продуктов из xml калиброна
        self.__kalibron_products = KalibronHandler().get_products_wb()
        self.result_products = []
        self.get_result_products()

    def get_result_products(self):
        self.result_products = WbHandler().get_products_list()
        skus = [product.skus for product in self.result_products]
        data_stock_info = {
            "skus": skus
        }
        stock_info = WbHandler().send_request_post(api_config.WB_URL_STOCK_QUANTITY, data_stock_info)
        for product in self.result_products:
            for stock_product in stock_info['stocks']:
                if product.skus == stock_product['sku']:
                    product.wb_quantity = stock_product['amount']
        price_info = WbHandler().send_request_get(api_config.WB_URL_PRICE_INFO)
        for product in self.result_products:
            for price_item in price_info:
                if product.nm_id == price_item['nmId']:
                    product.wb_price = price_item['price']
        for wb_product in self.result_products:
            for tdk_product in self.__kalibron_products:
                if tdk_product.vendor_code == wb_product.vendor_code:
                    wb_product.kalibron_price = tdk_product.kalibron_price
                    wb_product.kalibron_quantity = tdk_product.kalibron_quantity
                    break
            if wb_product.kalibron_price == '':
                wb_product.kalibron_price = 0
            if wb_product.kalibron_quantity == '':
                wb_product.kalibron_quantity = 0

    def update_price(self):
        data = [product.convert_to_price_update() for product in self.result_products]
        print(data)
        # Раскомментировать для обновления
        # WbHandler().send_request_post(api_config.WB_URL_PRICE_UPLOAD, data)

    def update_stock(self):
        data = [product.convert_to_stock_update() for product in self.result_products]
        data = {'stocks': data}
        print(data)
        # Раскомментировать для обновления
        # WbHandler().send_request_put(api_config.WB_URL_STOCK_UPLOAD, {'stocks': data})