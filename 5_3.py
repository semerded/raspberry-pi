import time

datum_tijd = time.ctime()
print(datum_tijd) # datum en tijd

tijd = time.time() # millis van raspberry pi
print(tijd) # tijd sinds epoch

tijdzone = time.tzname
print(tijdzone) # tijdzone


# import math

# print(math.pi)
# print(math.sqrt(math.pi))
# cirkelOmtrek = int(input("omtrek van cirkel: "))
# print(f"cirkel met diameter {cirkelOmtrek}cm heeft een omtrek van {math.pi * cirkelOmtrek}cm")
# print(round(math.pi * cirkelOmtrek))