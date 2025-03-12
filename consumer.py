from pylsl import StreamInlet, resolve_stream
#Resolve the stream on the network
streams= resolve_stream('type', 'EEG')
#Create an inlet to recieve data

inlet= StreamInlet(streams[0])

print ("Now receiving data...")

while True:
    sample, timestamp= inlet.pull_sample()
    print("fTimestamp: {timestamp}, Sample: {sample}")
