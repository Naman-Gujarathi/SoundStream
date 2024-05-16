import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    # convert message into python object
    message = json.loads(message)

    # created empty named temp file, we can use this file to write our video
    tf = tempfile.NamedTemporaryFile()
    # we get our video file from grid fsvideo and have it in out
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add video contents to empty file
    tf.write(out.read())
    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to the file
    # give patht to temp directory where temp file is stored and appedning desired mp3 file to path
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    # write audio file to path where it is created
    # write_audiofile created a temprory file
    audio.write_audiofile(tf_path)

    # save file to mongo gridfs
    # open the file and read the file
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    #remove temp file 
    os.remove(tf_path)

    # set mp3_fid set it to string version
    message["mp3_fid"] = str(fid)
    # put this message into mp3  messge queue
    try:
        channel.basic_publish(
            #default excahnge
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            # convert python object into json
            body=json.dumps(message),
            # to keep messge persisted before consumed 
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # if we cant message on the queue succssfully we have to delete the mp3 from mongodb
        fs_mp3s.delete(fid)
        return "failed to publish message"