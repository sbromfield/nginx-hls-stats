import time
import re


class logEntry:

    def __init__(self, ip, stream):
        self.name = "Nothing for now"
        self.stream = stream
        self.clientIP = ip
        self.time = time.time()

    def __contain__(self, p):
        if p == self.clientIP:
            return True

        return False

    def __str__(self):
        return "My IP is " + self.clientIP + " and stream path is " + self.stream


def myfile(thefile):
    while True:
        yield thefile.readline()


def getip(str):
    if str is not None:
        m = re.search("\d+.\d+.\d+.\d+",str)
        if m is not None:
            return m.group(0)
        else:
            return None
    return None


def validLogEntry(str):

    if ("GET" in str and ".m3u8" in str
            and "HTTP/1.1" in str):
        return True
    print("String is not valid: %s" % (str.strip()))
    return False


def getHLSPath(str):
    m = re.search("GET [\D+[0-9]*\D*]*.m3u8", str)
    if m is not None:
        return m.group(0)[4:]
    else:
        return None
    return None


if __name__ == "__main__":

  print("Start")
  with open('../access.log') as f:
      f.readlines()
      print("Going to sleep 10s")
      time.sleep(10)
      try:
          resetTimer = time.time() + (5 * 60)
          print("Starting reset timer %d" %(resetTimer))
          streams = {}

          for i in myfile(f):

              if len(i) > 0 and validLogEntry(i):
                  logstr = i.strip()
                  ip = getip(logstr)
                  path = getHLSPath(logstr)
                  l = logEntry(ip = ip, stream = path)

                  if path in streams.keys():
                      streamClients = streams[path]
                      print("IP is %s" %(ip))
                      print(client.clientIP == ip for client in streamClients)
                      if  (client.clientIP == ip for client in streamClients):
                          print("IP is %s" %(ip))
                          print(streamClients)
                          streamClients.append(l)
                          streams[path] = streamClients
                  else:
                      streams[path] = [l]

              else:
                  #print(time.time())
                  print("---")
                  time.sleep(10)

              for x in streams.keys():
                  if len(streams[x]) != 0:
                      print("%s has %d viewers" % (x,len(streams[x])))

                  mylist =mylist = []
                  for client in streams[x]:

                      if resetTimer - client.time >= 300:
                          print("removing")
                          continue
                      mylist.append(client)
                  print(mylist[0])
                  streams[x] = mylist


              if resetTimer < time.time():
                  resetTimer = time.time() + (5 *60)
                  #streams = {}
                  print("Timer reset")


      except KeyboardInterrupt as e:
            f.close()
            print("Closing the log File")
