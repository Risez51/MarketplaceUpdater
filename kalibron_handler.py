import api_config
from xml.dom import minidom
from xml.dom.minidom import Document
import urllib.request

from product import Product


class KalibronHandler:

    def get_products(self) -> list[Product]:
        link: str = api_config.XML_LINK
        xml_document = self.get_dom(link)
        offers = xml_document.getElementsByTagName('offer')
        print('Получен список товаров с tdkalibron.ru - XML')
        result_products = []
        for offer in offers:
            product = Product()
            for node in offer.childNodes:
                if node.nodeType == 1:
                    if node.tagName == 'id':
                        product.offer_id = self.__get_node_value(node)
                    elif node.tagName == 'price':
                        product.price_kalibron = round(float(node.getAttribute('price')) * 1.2)
                    elif node.tagName == 'qty':
                        product.quantity_kalibron = self.__get_node_value(node)
            result_products.append(product)
        print(f'Найдено товаров: {len(result_products)} шт.')
        print('----------------------------------------------------------------------------------')
        return result_products

    @staticmethod
    def __get_node_value(node) -> str:
        if node.firstChild:
            return str(node.firstChild.data)

    @staticmethod
    def get_dom(file_location: str) -> Document:
        try:
            if 'http' in file_location:
                downloaded_file = urllib.request.urlopen(file_location).read()
                dom = minidom.parseString(downloaded_file)
                dom.normalize()
                return dom
            else:
                dom = minidom.parse(file_location)
                dom.normalize()
                return dom
        except Exception as e:
            print(e)
