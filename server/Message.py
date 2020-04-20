class Frame:
    """Frame superclass used to define all message frames"""

    frame_types = {"base": 0, "connect": 1, "connack": 2, "disconnect": 3, "data": 4}
    frame_type = 0

    def __init__(self, message):
        self.header = message[0]
        self.content = message[1]

    def __str__(self):
        return (
            f"{list(self.frame_types.keys())[self.frame_type].upper()} Frame with contents: {self.content}"
        )


class ConnectFrame(Frame):
    """Connect Frame subclass, sent by client to broker when connection"""
    conn_types = {"subscribe":0, "publish":1}
    def __init__(self, message):
        super(ConnectFrame, self).__init__(message)
        self.frame_type = 1
        self.conn_type, self.topic = self.content.split(" ... ", 1)
        self.conn_type = self.conn_types[self.conn_type.lower()]


class ConnAckFrame(Frame):
    """Connection Acknowledge Frame, sent to client by broker 
    upon successful connection"""

    def __init__(self, conn_type):
        self.message = "ACK ... " + conn_type
        self.frame_type = 2

    def encode(self):
        return self.message.encode("utf-8")


class DiscFrame(Frame):
    """Disconnect Frame sent by client to broker"""

    def __init__(self, message):
        super(DiscFrame, self).__init__(message)
        self.frame_type = 3


class DataFrame(Frame):
    """Data Frame used to transmit data unilaterally 
    between client and broker"""

    def __init__(self, message):
        super(DataFrame, self).__init__(message)
        self.frame_type = 4
        self.topic, self.data = self.content.split(" ... ", 1)
