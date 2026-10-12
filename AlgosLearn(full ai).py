from collections import deque


class Planet:

    def __init__(self, name):
        self.name = name
        self.connections = []  # Список соседних планет

    def add_connection(self, other_planet):
        # Врата двусторонние: соединяем в обе стороны
        if other_planet not in self.connections:
            self.connections.append(other_planet)
        if self not in other_planet.connections:
            other_planet.append(self) if hasattr(
                other_planet, "append"
            ) else other_planet.connections.append(self)


class SpaceMap:

    def find_shortest_path(self, start_planet, target_planet):
        # 1. Если старт и финиш — одна и та же планета
        if start_planet == target_planet:
            return [start_planet.name]

        # 2. Очередь хранит списки (маршруты). Начинаем с пути из одной стартовой планеты.
        queue = deque([[start_planet]])

        # 3. Множество посещенных планет, чтобы не ходить по кругу (например, Земля -> Марс -> Земля)
        visited = set([start_planet])

        while queue:
            # Достаем САМЫЙ СТАРЫЙ маршрут из очереди
            current_path = queue.popleft()

            # Смотрим на последнюю планету в текущем маршруте
            current_planet = current_path[-1]

            # Перебираем всех соседей этой планеты
            for neighbor in current_planet.connections:

                # Если мы нашли целевую планету — добавляем её в путь и возвращаем результат!
                if neighbor == target_planet:
                    full_path = current_path + [neighbor]
                    # Возвращаем список имён планет для красивого вывода
                    return [planet.name for planet in full_path]

                # Если в этой планете мы еще не были
                if neighbor not in visited:
                    visited.add(neighbor)

                    # Создаем НОВЫЙ маршрут, добавляя соседа в конец, и отправляем в очередь
                    new_path = list(current_path) + [neighbor]
                    queue.append(new_path)

        # Если очередь опустела, а путь так и не нашли (как с Плутоном)
        return None


# ==========================================
# Проверка работы
# ==========================================
if __name__ == "__main__":
    # Создаем планеты
    earth = Planet("Земля")
    moon = Planet("Луна")
    mars = Planet("Марс")
    venus = Planet("Венера")
    jupiter = Planet("Юпитер")
    saturn = Planet("Сатурн")
    pluto = Planet("Плутон")

    # Настраиваем связи (врата)
    earth.add_connection(moon)
    earth.add_connection(mars)
    mars.add_connection(jupiter)
    moon.add_connection(venus)
    jupiter.add_connection(saturn)
    venus.add_connection(saturn)

    space_map = SpaceMap()

    # Тест 1: Путь от Земли до Сатурна
    path = space_map.find_shortest_path(earth, saturn)
    print("Маршрут Земля -> Сатурн:", path)
    # Выведет: ['Земля', 'Луна', 'Венера', 'Сатурн'] или ['Земля', 'Марс', 'Юпитер', 'Сатурн'] (оба пути по 3 прыжка!)

    # Тест 2: Путь от Земли до изолированного Плутона
    path_to_pluto = space_map.find_shortest_path(earth, pluto)
    print("Маршрут Земля -> Плутон:", path_to_pluto)
    # Выведет: None
