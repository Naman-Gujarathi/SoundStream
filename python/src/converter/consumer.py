import pika, sys, os, time
#mongoclient is used to create connection with mongodb server
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    # mongoclient creates connection to mongodb server  running on host host.minikube.internal on port 27017 kubernetes cluster at port 27017 
    client = MongoClient("host.minikube.internal", 27017)
    # client.videos access the videos database
    db_videos = client.videos
    # client.mp3s access the mp3 database
    db_mp3s = client.mp3s
    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        # pass body of message, gridfs video, gridfs mp3 and channel
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            # if failed to conver to mp3 negative acknowdgement is sent to message which is video queue and message not processed
            # delivery tag idnetifies the message that has been negatively acknowledge
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    # Consume message from video queue and call callback function whenver message is consumed
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")
    # it will run our consumer and consumer starts listen to channel where messge is put
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    # function will run untill press Ctrl + C     
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)