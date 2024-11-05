import json
from bson import ObjectId


# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)  # Convert ObjectId to string
#         return super(JSONEncoder, self).default(obj)
