import pika, json

## upload file to mongodb databse using gridfs, put message in rambbitmq and downsetream service can c# consume message 
def upload(f, fs, channel, access):
  try:
    # put file into mongodb and return id object  if successful  
    fid = fs.put(f)
  except Exception as err:
    return "internal server error", 500

#this  msg will put on queue contains fid for griddfs,mp3_id,and access userinfo contain unique email 
  message = {
    "video_fid": str(fid),
    "mp3_fid": None,
    "username": access["username"],
  }
# put this message on channel, producer send messagage to default exchange which is direct excahnge it# has one special property every queue is created is bound to exchange with routing key which is queue# name 
  try:
    channel.basic_publish(
      # default exchange is used 
      exchange="",
      # routing key is name of queue
      routing_key="video",
      # it serialize the python object into string, it is oppostite of json loads
      body=json.dumps(message),
      properties=pika.BasicProperties(
         # it means queue is durable and to make msg durable we need to set this configuration 
        delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
      ),
    )
  except:
    # if meddage is not put on queue, delete the file put in mongodb  
    fs.delete(fid)
    return "internal server error", 500
