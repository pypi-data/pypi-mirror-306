import math

class Util():
    def getNoOfPackages(n, decimals=0):
        multiplier = 10 ** decimals
        return int(math.ceil(n * multiplier) / multiplier)

    def getHeader(msg):
        return msg[0:3:1]

    def getPayload(msg):
        return msg[3::1]