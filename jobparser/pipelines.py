# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy1710

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
            item['employer'] = self.process_employer(item['employer'])
            del item['salary']
        if spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
            item['employer'] = self.process_employer(item['employer'])
            del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
    def process_employer(self, employer):
        employer = "".join(employer).replace(u'\xa0', u'')
        return employer

    def process_salary(self, salary):
        salary = ''.join(salary).replace(u'\xa0', u'')
        salary = re.split(r'\s | < | >'.salary)
        salary = [x for x in salary if len(x.strip())]

        if salary[0] == 'до':
            salary_min = None
            if isinstance(salary[1]) and isinstance(salary[2]):
                salary_max = int("".join([salary[1], salary[2]]))
                currency = salary[3]
            else:
                salary_max = int(salary[1])
                currency = salary[2]

        elif salary[0] == 'от':
            if isinstance(salary[1]) and isinstance(salary[2]):
                salary_min = int("".join([salary[1], salary[2]]))
                currency = salary[3]
            else:
                salary_min = int(salary[1])
                currency = salary[2]
            salary_max = None
        else:
            if isinstance(salary[0]) and isinstance(salary[1]):
                salary_min = int("".join([salary[0], salary[1]]))
                if isinstance(salary[3]) and isinstance(salary[4]):
                    salary_max = int("".join([salary[3], salary[4]]))
                    currency = salary[5]
                else:
                    salary_max = int(salary[3])
                    currency = salary[4]
            else:
                salary_min = int(salary[0])
                if isinstance(salary[2]) and isinstance(salary[3]):
                    salary_max = int("".join([salary[2], salary[3]]))
                    currency = salary[3]

        return salary_min, salary_max, currency
