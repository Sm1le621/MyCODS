import math
def earth(t1, t2, g1, g2):
    t1 = math.radians(t1)
    t2 = math.radians(t2)
    g1 = math.radians(g1)
    g2 = math.radians(g2)
    distance = 6371.01 * math.acos(math.sin(t1)*math.sin(t2) + math.cos(t1)*math.cos(t2)*math.cos(g1-g2))
    return distance

q = ''
while True:
    point1 = input("Введіть довготу і широту першу та другу точку на земной кулі(через пропуск): ")
    q = input("Щоб вийти із програми 'q': ")
    if q == 'q':
        break
    point1_ = point1.split(' ')
    t1 = int(point1_[0])
    g1 = int(point1_[1])
    t2 = int(point1_[2])
    g2 = int(point1_[3])
    dist = earth(t1, t2, g1, g2)
    print(f"відстань від точки ({t1};{g1}) до точки ({t2};{g2}) становить {round(dist, 1)} км.")