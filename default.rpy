# Определение персонажей игры.
define hero = Character('Кристофер', color="#473cc2")
define u = Character('???', color="#8259ff")
define s = Character('Мысли', color="#5b5555")
define l = Character('Лила', color="#59ffac")
define e = Character('Эльза', color="#59a6ff")
default time_id = 2 # 0 — день, 1 — вечер, 2 — ночь
default used_ingredient_list = []
default ingredient_count = 0  # Счётчик использованных ингредиентов
default money = 100  # Начальное количество денег
default day = 1 


default lilly_shop = [
    get_item_by_id(0, itemList, 5),
    get_item_by_id(4, itemList, 1),
    get_item_by_id(1, itemList, 4),
    get_item_by_id(3, itemList, 1),
]