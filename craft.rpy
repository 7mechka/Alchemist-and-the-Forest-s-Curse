define cauldron_load = []
define slot_count = 3
define cauldron_recipe_load = []

init python:
    cauldron_load = []
    cauldron_recipe_load = []
    def use_ingredient(item):
        found = False
        for used in cauldron_recipe_load:
            if used['ing_id'] == item['ing_id']:
                used['count'] += 1
                inventory[inventory.index(item)]['count'] -= 1
                if inventory[inventory.index(item)]['count'] <= 0:
                    inventory.remove(item)
                found = True
                break        
        if not found:
            new_used = {
                "count": 1,
                "ing_id": item['ing_id'],
            }
            cauldron_recipe_load.append(new_used)
            inventory[inventory.index(item)]['count'] -= 1
            if inventory[inventory.index(item)]['count'] <= 0:
                inventory.remove(item)
    def insert_to_load(item):
        global cauldron_load, slot_count
        if len(cauldron_load) < slot_count:
            cauldron_load.append(item)
            use_ingredient(item)

    def remove_from_load(item):
        global cauldron_load, slot_count
        if item in cauldron_load:
            for used in cauldron_recipe_load:
                if used['ing_id'] == item['ing_id']:
                    used['count'] -= 1
                    if item in inventory:
                        inventory[inventory.index(item)]['count'] += 1
                    else:
                        add_item(item['id'], 1)
                    if used['count'] <= 0:
                        cauldron_recipe_load.remove(used)
                    break
            cauldron_load.remove(item)

    def open_mini_game():
            # показать второй поверх
            renpy.show_screen("mixing_game", callback=set_result)

    def set_result(value):
            renpy.hide_screen("mixing_game")
            potion_craft_logic(value)


    def potion_craft_logic(is_crafted=False):
        global is_potion_crafted, is_lilly_potion_crafted, cauldron_load, unlock_recipes, recipes, cauldron_recipe_load

        if is_crafted == True:
            for i in unlock_recipes:
                tmp_recipe = {frozenset(d.items()) for d in i['ing_list']}
                tmp_used = {frozenset(d.items()) for d in cauldron_recipe_load}    
                if tmp_recipe == tmp_used:
                    add_notification(f"Вы сварили: {i['name']}!")
                    # renpy.notify(f"Вы сварили: {i['name']}!")
                    if i['potion_id'] == 6:
                        is_lilly_potion_crafted = True
                    is_crafted = True
                    is_potion_crafted = True
                    add_item(i['potion_id'], 1)
                    cauldron_load = []
                    cauldron_recipe_load = []
                    return
            for i in recipes:
                tmp_recipe = {frozenset(d.items()) for d in i['ing_list']}
                tmp_used = {frozenset(d.items()) for d in cauldron_recipe_load}    
                if tmp_recipe == tmp_used:
                    random_number = randint(0, 100)
                    if random_number <= 20:  # 20% шанс на успех
                        add_notification(f"Вы сварили: {i['name']}!")
                        # renpy.notify(f"Вы сварили: {i['name']}!")
                        if i['potion_id'] == 6:
                            is_lilly_potion_crafted = True
                        is_crafted = True
                        is_potion_crafted = True
                        add_item(i['potion_id'], 1)
                        cauldron_load = []
                        cauldron_recipe_load = []
                        return
                    else:
                        add_notification("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
                        # renpy.notify("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
                        cauldron_load = []
                        cauldron_recipe_load = []
                        return
                    break
                else:
                    add_notification("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
                    # renpy.notify("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
                    cauldron_load = []
                    cauldron_recipe_load = []
                    return
        elif is_crafted == False:
            add_notification("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
            # renpy.show_screen("notification","Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
            cauldron_load = []
            cauldron_recipe_load = []
            return

default unlock_recipes = []
# Список рецептов зелий
default recipes = [
    # Зелье бреда ID 3 
    {
        "name": itemList[3]['name'],
        "description": itemList[3]['description'],
        "ing_list": itemList[4]['ing_list'],
        'potion_id': 3,  # ID зелья, которое будет создано
    },
    # Зелье смеха ID 6
    {
        "name": itemList[6]['name'],
        "description": itemList[6]['description'],
        "ing_list": itemList[7]['ing_list'],
        'potion_id': 6,  # ID зелья, которое будет создано
    },
    # Зелье проявления 8
    {
        "name": itemList[8]['name'],
        "description": itemList[8]['description'],
        "ing_list": itemList[9]['ing_list'],
        'potion_id': 8,  # ID зелья, которое будет создано
    },
]

screen craft_screen():
    modal True
    add 'gui/inventory/gui_gpt_clear.png'

    $ load_coords = [
        (55, 445),
        (220, 525),
        (385, 450),
        (395, 310),
        (230, 225),
        (60, 305)
    ]

    $ is_slots_full = len(cauldron_load) >= slot_count

    $ tmp_list = []
    for i in inventory:
        if i["type"] == "ingredient":
            $ tmp_list.append(i)

    $ count = 0
    for i in range(3):
        for j in range(7):
            if count >= len(tmp_list):
                continue
            imagebutton:
                idle im.Scale(tmp_list[count]["icon"], 75, 75)
                hover im.Scale(tmp_list[count]["icon_hover"], 75, 75)
                if is_slots_full:
                    action NullAction()
                else:
                    action [
                        Show('blocker'),
                        Show('item_transfer_animation', None, tmp_list[count], (1133 + (j * 100), 172 + (i * 95)), load_coords[len(cauldron_load)], _tag="item_transfer_animation_%s"%tmp_list[count]['id'], cb=insert_to_load, arg=tmp_list[count]),
                        # Function(renpy.pause, 1.0),
                        # Function(insert_to_load, tmp_list[count])
                        ]
                hovered Function(show_tooltip_for_item, tmp_list[count]["name"], tmp_list[count]["description"])
                unhovered Function(renpy.hide_screen, "tooltip_screen")
                pos (1133 + (j * 100), 172 + (i * 95))
                xysize (80, 80)
                at item_transform
            $ count += 1

    textbutton "Изготовить":
        pos (1500, 800)
        action Function(open_mini_game)

    textbutton "Отмена":
        pos (1100, 800)
        action [Return(False), Hide("new_craft_screen")]

    for i in range(0, slot_count):
        if i < len(cauldron_load):
            imagebutton:
                idle im.Scale(cauldron_load[i]["icon"], 100, 100)
                hover im.Scale(cauldron_load[i]["icon_hover"], 100, 100)
                action [
                    Show('blocker'),
                    Function(remove_from_load, cauldron_load[i]),
                    Show('item_disapear_animation', None, cauldron_load[i], load_coords[i], _tag="item_disapear_animation_%s"%cauldron_load[i]['id']),
                    # Function(remove_from_load, cauldron_load[i])
                    ]
                pos load_coords[i]
                xysize (100, 100)

transform fly_to(x1, y1, x2, y2, t=1.0):
    xpos x1
    ypos y1
    alpha 1.0
    linear t xpos x2 ypos y2 alpha 0.0


# Метка для подвала
label basement:
    show basement basic with fade
    $ ingredient_count = 0
    $ used_ingredient_list = []  # Сбрасываем список при каждом входе
    
    call show_gui

    # Проверяем есть ли вообще ингредиенты
    python:
        has_ingredients = any(
            item['type'] == 'ingredient' and item['count'] > 0 
            for item in inventory
        )
    
    menu:
        "Посмотреть рецепты":
            call screen inventory_screen(filter="recipe")
            jump basement
            
        "Варить зелье" if has_ingredients:
            call screen craft_screen
            jump basement
            
        "Варить зелье" if not has_ingredients:
            "У вас нет ингредиентов для варки!"
            jump basement
            
        "Вернуться домой":
            call hide_gui
            hide basement basic with fade
            call hide_gui
            show black
            call transition("home")

init python:
    def calculateDistance2(x1, x2):
        return x1 - x2

screen item_transfer_animation(item, from_pos, to_pos, cb=None, arg=None):
    zorder 95

    fixed:
        xysize 80,80
        add "gui/inventory/sparkle.png":
            at transform:
                xcenter 1.5
                ycenter 1.5
                zoom 1.8
                alpha 0.65
                alignaround (.5,.5)
                linear 4 rotate 360
                rotate 0
                repeat

        add item['icon'] 

        default distX = int(calculateDistance2(from_pos[0],to_pos[0]) / 2)
        default distY = int(calculateDistance2(to_pos[1],from_pos[1]) /2)
        at transform:
            subpixel True
            zoom 1.25
            pos from_pos
            anchor (.5,.5)
            around (from_pos[0]+distX,from_pos[1]+distY)
            parallel:
                easein 1 xpos to_pos[0]+20 ypos to_pos[1]+15 counterclockwise
                pause 0.25
                easein 0.3 yoffset +10 alpha 0
            parallel:
                easein 1.5 zoom 0.5
    
    if cb:
        timer 1.3 action [Function(cb, arg), Hide("item_transfer_animation_%s"%item['id'])]

    else:
        timer 1.3 action Hide("item_transfer_animation_%s"%item['id'])

screen item_disapear_animation(item, from_pos):
    zorder 95

    fixed:
        xysize 80,80

        add item['icon'] 

        at transform:
            subpixel True
            zoom 1.25
            pos from_pos
            anchor (.5,.5)
            parallel:
                easein 1 ypos from_pos[1]-50 alpha 0
            parallel:
                easein 1.5 zoom 0.5
    
    timer 1.3 action Hide("item_disapear_animation_%s"%item['id'])

screen blocker():
    modal True   # перехватывает все действия игрока
    zorder 9999  # выше всего
    # Можно даже добавить прозрачный фон:
    add Solid("#0000")  # полностью прозрачный

    timer 1.7 action Hide("blocker")  # скрыть через 2 секунды