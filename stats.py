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

    def __eq__(self, p):
        if not isinstance(p,str):
            return False

        if self.clientIP == p:
            return True
        else:
            return False

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
    #print("String is not valid: %s" % (str.strip()))
    return False


def getHLSPath(str):
    m = re.search("GET [\D+[0-9]*\D*]*.m3u8", str)
    if m is not None:
        return m.group(0)[4:]
    else:
        return None
    return None


if __name__ == "__main__":

  numofmins = 3

  print("Start")
  with open('../access.log') as f:
      f.readlines()

      try:
          resetTimer = time.time() + (numofmins * 60)
          streams = {}

          for i in myfile(f):

              if len(i) > 0 and validLogEntry(i):
                  logstr = i.strip()
                  ip = getip(logstr)
                  path = getHLSPath(logstr)
                  l = logEntry(ip = ip, stream = path)

                  if path in streams.keys():
                      streamClients = streams[path]
                      if ip not in streamClients:
                          streamClients.append(l)
                          streams[path] = streamClients
                  else:
                      streams[path] = [l]
              else:
                  print("---")
                  time.sleep(10)

              for x in streams.keys():
                  numofviewers = len(streams[x])
                  if numofviewers > 0:
                      print("%s has %d viewers" % (x,numofviewers))
                  idx = -1
                  for viewer in streams[x]:
                      if viewer.time - resetTimer <= -(numofmins * 60):
                          idx += 1
                          print("Found an expired viewer %d" % idx)
                      else:
                          print("No more expired users in this stream")
                          break
                  if idx > -1:
                      if idx + 1 == len(streams[x]):
                          streams[x] = []
                      else:
                          streams[x] = streams[x][idx + 1:]

              if resetTimer < time.time():
                  resetTimer = time.time() + (numofmins * 60)
                  print("Timer reset")

      except KeyboardInterrupt as e:
            f.close()
            print("Closing the log File")
