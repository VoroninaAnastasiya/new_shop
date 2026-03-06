import json
import datetime
import decimal
import uuid


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # datetime → ISO 8601 строка
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()

        # Decimal → float
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        # UUID → строка
        if isinstance(obj, uuid.UUID):
            return str(obj)

        # fallback
        return super().default(obj)
