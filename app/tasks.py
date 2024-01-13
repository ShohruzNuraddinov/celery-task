import threading
import urllib.request

from django.utils.crypto import get_random_string
from celery import shared_task
from app.models import ImageFile


def downloadImage(img_key):
    url = "https://picsum.photos/200/300"
    imgName = f"media/images/img_{img_key}.png"
    urllib.request.urlretrieve(url, imgName)


@shared_task
def image_save():
    # 1
    # for _ in range(100):
    #     random_key = get_random_string(12)
    #     downloadImage(random_key)
    #     ImageFile.objects.create(image=f'images/img_{random_key}.png')

    # 2-bulk
    # images = []
    # for _ in range(100):
    #     random_key = get_random_string(12)
    #     downloadImage(random_key)
    #     images.append(ImageFile(image=f'images/img_{random_key}.png'))

    # ImageFile.objects.bulk_create(images)

    # 3-thread
    threads = []
    images_list = []
    for _ in range(100):
        random_key = get_random_string(12)
        thread = threading.Thread(
            target=downloadImage, args=(random_key,))
        threads.append(thread)
        thread.start()
        images_list.append(
            ImageFile(image=f'images/img_{random_key}.png'))

    for thread in threads:
        thread.join()

    ImageFile.objects.bulk_create(images_list)

    # 1: 2.4 min
    # 2-bulk: 2.2 min
    # 3-thread: 5.4s
