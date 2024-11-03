# DarkFream/global_config.py
_user_model = None

def set_user_model(model):
    global _user_model
    _user_model = model

def get_user_model():
    global _user_model
    return _user_model
