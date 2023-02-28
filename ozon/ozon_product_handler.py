from ozon.ozon_product import Product
import api_config


class ProductHandler:

    @staticmethod
    def get_products_from_price_items(ozon_items_list: list):
        result_products = []
        for ozon_item_list in ozon_items_list:
            for ozon_item in ozon_item_list['result']['items']:
                product = Product()
                product.offer_id = ozon_item['offer_id']
                product.product_id = ozon_item['product_id']
                product.price_ozon = ozon_item['price']['price']
                product.old_price_ozon = ozon_item['price']['old_price']
                result_products.append(product)
        return result_products

    @staticmethod
    def get_products_from_stock_items(ozon_items_list: list):
        result_products = []
        # Итерация по списку с ozon товарами
        product_count = 0
        for ozon_item_list in ozon_items_list:
            for ozon_item in ozon_item_list['result']['items']:
                product = Product()
                product.offer_id = ozon_item['offer_id']
                product.product_id = ozon_item['product_id']
                # Итерация по складам FBS|FBO
                for current_stock in ozon_item['stocks']:
                    # Если склад FBS - заполняется остаток
                    if current_stock['type'] == 'fbs':
                        product.quantity_ozon = current_stock['present']
                result_products.append(product)
        return result_products

    @staticmethod
    def get_merged_products_for_price(ozon_products: list[Product], kalibron_products: list[Product]) -> list[Product]:
        result_products = []
        for ozon_product in ozon_products:
            for kalibron_product in kalibron_products:
                if ozon_product.offer_id == kalibron_product.offer_id:
                    ozon_product.price_kalibron = kalibron_product.price_kalibron
                    break
            result_products.append(ozon_product)
        return result_products

    def get_merged_products_for_stock(self, ozon_products: list[Product],
                                      kalibron_products: list[Product]) -> list[Product]:
        result_products = []
        for ozon_product in ozon_products:
            for kalibron_product in kalibron_products:
                if ozon_product.offer_id == kalibron_product.offer_id:
                    ozon_product.quantity_kalibron = self.__calculate_quantity(kalibron_product.quantity_kalibron)
                    break
            result_products.append(ozon_product)
        return result_products

    @staticmethod
    def __calculate_quantity(quantity):
        result = 0
        if int(quantity) >= 20:
            result = int(int(quantity) / 100 * 20)
        return result

    @staticmethod
    def get_prepared_products_for_price_update(products: list[Product]) -> list[list]:
        limit_count = 0
        result_products: list[list] = []
        result_products_limit = []
        for product in products:
            if product.price_ozon != product.price_kalibron:
                product_for_send = {'auto_action_enabled': 'UNKNOWN',
                                    'currency_code': 'RUB',
                                    'min_price': '',
                                    'offer_id': str(product.offer_id),
                                    'old_price': str(round(product.price_kalibron * 1.06)),
                                    'price': str(product.price_kalibron),
                                    'product_id': product.product_id}
                result_products_limit.append(product_for_send)
                limit_count += 1
                if limit_count == api_config.OZON_PRICE_UPDATE_LIMIT:
                    result_products.append(result_products_limit)
                    result_products_limit = []
                    limit_count = 0
            if products[-1] == product:
                result_products.append(result_products_limit)
        return result_products

    @staticmethod
    def get_prepared_products_for_stock_update(merged_products: list[Product]) -> list[list]:
        limit_count = 0
        result_products: list[list] = []
        result_products_limit = []
        for product in merged_products:
            if product.quantity_ozon != product.quantity_kalibron:
                product_for_send = {"offer_id": str(product.offer_id),
                                    "product_id": int(product.product_id),
                                    "stock": int(product.quantity_kalibron),
                                    "warehouse_id": api_config.OZON_WAREHOUSE_ID}

                result_products_limit.append(product_for_send)
                limit_count += 1
                if limit_count == api_config.OZON_STOCK_UPDATE_LIMIT:
                    result_products.append(result_products_limit)
                    result_products_limit = []
                    limit_count = 0
            if merged_products[-1] == product:
                result_products.append(result_products_limit)
        return result_products
