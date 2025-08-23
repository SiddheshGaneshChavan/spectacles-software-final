import bcrypt
import os
import sys
import logging

log = logging.getLogger(__name__)

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode(), hashed_password)

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def set_window_icon(root, icon_filename="sunglasses.ico"):
    try:
        icon_path = resource_path(icon_filename)
        if os.path.isfile(icon_path):
            root.iconbitmap(icon_path)
        else:
            log.warning("Icon file not found: %s", icon_path)
    except Exception as e:
        log.warning("Could not set window icon: %s", e)
