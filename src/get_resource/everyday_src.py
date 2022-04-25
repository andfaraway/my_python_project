from src.get_resource import desktop_images
from src.get_resource import get_source_to_sql


def start():
    get_source_to_sql.getOnesContent()
    desktop_images.download()
