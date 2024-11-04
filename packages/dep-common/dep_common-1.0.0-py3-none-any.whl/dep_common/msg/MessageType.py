class MessageType:
    VALUES =  {
        "sim": 1,
        "dim": 2,
        "dam": 3,
        "dcm": 4
    } 
    SYSTEM_INFORMATION_MESSAGE = VALUES["sim"]
    DATA_INFORMATION_MESSAGE   = VALUES["dim"]
    DATA_ACKNOWLEDGE_MESSAGE   = VALUES["dam"]
    DATA_CONTENT_MESSAGE       = VALUES["dcm"]