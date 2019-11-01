# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from database.database import ApartmentsBase
from database.models import Apartments, Autors, ImagesUrls, Base

class AvitoParserPipeline(object):
    def __init__(self):
        bd_url = 'sqlite:///Apartments_Base.sqlite'
        self.bd = ApartmentsBase(Base, bd_url)
    def process_item(self, item, spider):
        if not self.bd.session.query(Autors).filter_by(url=item['autor_url']).first():
            autor = Autors(item['autor_url'], item['autor_name'])
            self.bd.session.add(autor)
            self.bd.session.commit()
        else:
            autor = self.bd.session.query(Autors).filter_by(url=item['autor_url']).first()
        apartment = Apartments(item['url'], item['name'], item['cost'], autor.id)
        if not self.bd.session.query(Apartments).filter_by(url=item['url']).first():
            self.bd.session.add(apartment)
            self.bd.session.commit()
        for itm in item['images']:
            img = ImagesUrls(apartment.id, itm)
            if not self.bd.session.query(ImagesUrls).filter_by(url=itm).first():
                self.bd.session.add(img)
                self.bd.session.commit()
        return item
