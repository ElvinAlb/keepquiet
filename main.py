from utils import *
from screen import *
from motion_detect import *
import time
import datetime
import paho.mqtt.client as mqtt
import json

snd_pin = 1             # détecteur de son
pir_pin = 4             # détecteur de mouvement
buz_pin = 2             # alarme sonore
led_pin = 3             # alarme visuelle

pinMode(snd_pin,"INPUT")    # pin A1
pinMode(pir_pin,"INPUT")    # pin D4
pinMode(buz_pin,"OUTPUT")   # pin 
pinMode(led_pin,"OUTPUT")   # pin D3

elapsed = 0


buffer_size = 10
db_threshold = 54
db_buffer = deque(maxlen=buffer_size)

BROKER = "broker.hivemq.com"
TOPIC_PUB = "keepquiet/status"

#Initialisation MQTT
client = mqtt.Client()
client.connect(BROKER, 1883, 60)
client.loop_start()


while True :
    try :
        motion_detected, elapsed = check_motion_activity(pir_pin,elapsed)
        if motion_detected:
            sound_value = get_sound_level(snd_pin)
            db = round(convert_analog_to_db(sound_value),2)
            message = get_noise_message(db)

            print_screen(message, db)

            db_buffer.append(db)
            buzzer_alert(db_threshold, buffer_size, db_buffer, buz_pin, led_pin)

            payload_dict = {
                "db": round(db, 2),
                "etat": message,
                "timestamp": datetime.datetime.now().isoformat()
            }
            payload_json = json.dumps(payload_dict)

            client.publish(TOPIC_PUB, payload_json)
        else:
            print("🔕 En veille - mesure du son suspendue.")
            setText("")
            setRGB(0,0,0)

        time.sleep(1)


    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        break
    except IOError:
        print('Input/Output error')

client.loop_stop()
client.disconnect()
digitalWrite(buz_pin, 0)
digitalWrite(led_pin, 0)
setText("Bye Bye !")
setRGB(0, 0, 0)