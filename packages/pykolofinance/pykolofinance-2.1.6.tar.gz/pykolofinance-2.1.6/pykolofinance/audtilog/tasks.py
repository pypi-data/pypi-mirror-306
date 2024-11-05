from bson import json_util
from django.conf import settings
from elasticsearch import Elasticsearch

from core.celery import APP

from pykolofinance.audtilog.mongo_connector import get_database

dbname = get_database()
log_items = settings.APP_NAME.lower()
collection_name = dbname[log_items]


@APP.task()
def send_logs_to_logger(data):
    try:
        collection_name.insert_one(data)
        # elastic_search = Elasticsearch(hosts=settings.MONGODB_LOGGER_URL)
        # result = elastic_search.index(index=settings.APP_NAME.lower(), body=data)
        return {
            'app_name': log_items,
            'data': data,
        }
    except Exception as e:
        print(f"Failed to Log Data: {e}")


@APP.task()
def send_log_to_auditlogger(data):
    pass
