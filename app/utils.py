import threading
import urllib.request
import time
from django.utils.crypto import get_random_string


def downloadImage(imgPath, fileName):
    print("Downloading Image from ", imgPath)
    urllib.request.urlretrieve(imgPath, fileName)
    print("Completed Download")


def createThread(i, url):
    imgName = "media/images/image-" + str(i) + ".jpg"
    downloadImage(url, imgName)


def main():
    url = "https://picsum.photos/200/300"
    t = time.time()
    # create an array which will store a reference to
    # all of our threads
    threads = []

    # create 10 threads, append them to our array of threads
    # and start them off
    for i in range(100):
        thread = threading.Thread(
            target=createThread, args=(get_random_string(6), url,))
        threads.append(thread)
        thread.start()

    # ensure that all the threads in our array have completed
    # their execution before we log the total time to complete
    for i in threads:
        i.join()

    # calculate the total execution time
    t1 = time.time()
    totalTime = t1 - t
    print("Total Execution Time {}".format(totalTime))


main()
