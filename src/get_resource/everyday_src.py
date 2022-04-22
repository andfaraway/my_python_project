from . import desktop_images
from . import get_source_to_sql


def start():
    get_source_to_sql.getOnesContent()
    desktop_images.download()
