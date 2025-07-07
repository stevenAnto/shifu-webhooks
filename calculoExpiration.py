import datetime

expiration_ms = 1751984911000
expiration_sec = expiration_ms / 1000  # pasar a segundos

expiration_datetime = datetime.datetime.utcfromtimestamp(expiration_sec)
now_datetime = datetime.datetime.utcnow()

time_left = expiration_datetime - now_datetime

print(f"El webhook expirará el: {expiration_datetime} UTC")
print(f"Tiempo restante: {time_left} (días, horas, minutos, segundos)")
