import requests
import json
import api_config
from wildberries.wb_product import Product


class WbHandler:
    def __init__(self):
        self.products: list[Product] = []

    def get_products_list(self) -> list[Product]:
        data = {
            "sort": {
                "cursor": {
                    "limit": 1000
                },
                "filter": {
                    "withPhoto": -1
                }
            }
        }
        result_products = []
        items = self.send_request_post(api_config.WB_URL_PRODUCTS_INFO, data)
        for item in items['data']['cards']:
            product = Product()
            product.nm_id = item['nmID']
            product.vendor_code = item['vendorCode']
            for size in item['sizes']:
                product.skus = size['skus'][0]
            result_products.append(product)
        return result_products

    @staticmethod
    def send_request_post(url: str, data):
        answer = requests.post(url, json=data, headers=api_config.WB_HEADERS)
        content = answer.content
        content = json.loads(content.decode('utf-8'))
        return content

    @staticmethod
    def send_request_get(url: str):
        answer = requests.get(url, headers=api_config.WB_HEADERS)
        content = answer.content
        content = json.loads(content.decode('utf-8'))
        return content

    @staticmethod
    def send_request_put(url: str, data):
        answer = requests.put(url, data=data, headers=api_config.WB_HEADERS)
        content = answer.content
        content = json.loads(content.decode('utf-8'))
        return content

