from .models import order_data

class AgctruckingDBRouter:
    def db_for_read (self, model, **hints):
        if (model == order_data):
            return 'agc'
        return None

    def db_for_write (self, model, **hints):
        if (model == order_data):
            return 'agc'
        return None
