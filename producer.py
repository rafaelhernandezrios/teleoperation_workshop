from pylsl import StreamInfo, StreamOutlet
import time
import random
# Define String info
info=StreamInfo('EEG', 'EEG', 8, 100, 'float32', 'myuid34234')
#Create an outlet for streaming
outlet= StreamOutlet(info)
print("Now sending data...")
#Send random data to the stream
while True:
    sample= [random.random() for _ in range(8)]
    outlet.push_sample(sample)
    time.sleep(0.01)
