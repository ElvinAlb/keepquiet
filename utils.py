import time
import os
import math
from grovepi import *
from grove_rgb_lcd import *
from collections import deque
from mail import send_email_alert

def get_sound_level(sound_sensor):
    pinMode(sound_sensor,"INPUT")
    sound_value = analogRead(sound_sensor)
    #print(f'Son : {sound_value}')
    return sound_value

def convert_analog_to_db(sound_value):
    if sound_value > 0 :
                db = 20 * math.log10(sound_value)
    else: 
        db = 0

    #print(f'{round(db, 2)} dB')
    return db

def get_noise_message(db):
    db = db
    if db <= 34:
        return f'calme'
    elif db <= 40:
        return f'chill'
    elif db <= 46:
        return f'normal'
    elif db <= 54:
        return f'bruyant'
    elif db > 54:
        return f'critique'    

def buzzer_alert(db_threshold, buffer_size, db_buffer, buzzer_pin, red_led_pin):
    if len(db_buffer) == buffer_size and all(val > db_threshold for val in db_buffer):
            print(f"🔴 ALERTE : {db_threshold} dB pendant {buffer_size} secondes !")
            alert_flash_with_buzzer(red_led_pin, buzzer_pin)
            body = "Niveau sonore critique détecté par KeepQuiet !"
            subject = "🚨 Alerte KeepQuiet"
            to_email = "elvin.albertos@student.junia.com"
            send_email_alert(subject, body, to_email)
            print("✉️ Mail envoyé")
            db_buffer.clear()


def alert_flash_with_buzzer(led_pin, buzzer_pin, flashes=6, delay=0.2):
    pinMode(led_pin, "OUTPUT")
    pinMode(buzzer_pin, "OUTPUT")

    for _ in range(flashes):
        digitalWrite(led_pin, 1)
        digitalWrite(buzzer_pin, 1)
        time.sleep(delay)
        digitalWrite(led_pin, 0)
        digitalWrite(buzzer_pin, 0)
        time.sleep(delay)

def check_motion_activity(pir_pin, elapsed, timeout=10):
    """
    Vérifie la présence toutes les secondes.
    Retourne True si activité détectée récemment, sinon False pour activer la veille.
    
    :param pir_pin: pin numérique connecté au capteur PIR
    :param timeout: durée en secondes sans mouvement avant la mise en veille
    :return: True (actif) ou False (veille)
    """
    pinMode(pir_pin, "INPUT")
    last_motion_time = time.time()

    if digitalRead(pir_pin):
        last_motion_time = time.time()  # Réinitialise le timer si mouvement
        print("Mouvement détecté.")
        elapsed =0
    elapsed += 1
    print(elapsed)
    if elapsed < timeout:
        return True, elapsed  # Système actif
    else:
        print("💤 Aucun mouvement depuis 60s → mise en veille.")
        return False, elapsed  # Mise en veille

def print_screen(message, db):
     
    setText(f'{message}\n{db}')
    if message in [ "calme", "chill", "normal"]:
            setRGB(0,255,0)
    elif message == "bruyant":
            setRGB(255,255,0)
    elif message == "critique":
            setRGB(255,0,0)

def send_email_alert(subject, body, to_email):
    

    # Envoi via Postfix
    try:
        os.system(f'echo "{body}" | mail -s "{subject}" {to_email}')
    except Exception as e:
        print(f"❌ Échec de l'envoi de l'email : {e}")
