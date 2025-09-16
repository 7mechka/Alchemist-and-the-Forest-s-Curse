# Определение персонажей игры.
define hero = Character('Кристофер', color="#473cc2")
define u = Character('???', color="#8259ff")
define l = Character('Льюис', color="#9aae37")
define s = Character('Мысли', color="#5b5555")
define l = Character('Лилли', color="#59ffac")
default time_id = 2 # 0 — день, 1 — вечер, 2 — ночь
default used_ingredient_list = []
default ingredient_count = 0  # Счётчик использованных ингредиентов
default money = 100  # Начальное количество денег
default day = 1 


default lilly_shop = [
    get_item_by_id(0, itemList, 5),
    get_item_by_id(4, itemList, 1),
]