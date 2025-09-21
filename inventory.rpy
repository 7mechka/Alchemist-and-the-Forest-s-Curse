# Список инвентаря
default inventory = []

init python:
    def add_item(id, count=1):
        global inventory
        item = get_item_by_id(id, itemList)
        if not item:
            add_notification("Предмет не найден в списке предметов!")
            return

        # Проверяем, есть ли уже такой предмет в инвентаре
        for inv_item in inventory:
            if inv_item['id'] == item['id']:
                inv_item['count'] += item['count']
                return
        
        # Если предмета нет, добавляем новый
        inventory.append(item)

    def shop_manager(shop_inventory, item, type):
        global money  
        if type == "buy":
            for shop_item in shop_inventory:
                if shop_item['name'] == item['name'] and shop_item['count'] > 0:
                    if money < shop_item['price']:
                        add_notification("Недостаточно денег для покупки!")
                        return
                    money -= shop_item['price']
                    shop_item['count'] -= 1
                    if shop_item['count'] == 0:
                        shop_inventory.remove(shop_item)
                    add_item(shop_item['id'], count=1)
                    add_notification(f"Куплено: {shop_item['name']}")
                    break
                else:
                    add_notification("Предмет не найден в инвентаре или его количество равно нулю!")
        elif type == "sell":
            for inv_item in inventory:
                if inv_item['name'] == item['name'] and inv_item['count'] > 0:
                    money += inv_item['price'] // 2
                    inv_item['count'] -= 1
                    if inv_item['count'] == 0:
                        inventory.remove(inv_item)
                    add_notification(f"Продано: {inv_item['name']}")
                    break
                else:
                    add_notification("Предмет не найден в инвентаре или его количество равно нулю!")

    def get_item_by_name(name, List, count=1):
        for item in List:
            if item['name'] == name:
                returned_item = item.copy()
                returned_item['count'] = count
                return returned_item

    def get_item_by_id(id, List = itemList, count=1):
        for item in List:
            if item['id'] == id:
                returned_item = item.copy()
                returned_item['count'] = count
                return returned_item

    def update_unlock_recipes():
        global unlock_recipes, inventory, recipes
        unlock_recipes = []
        for i in inventory:
            if i["type"] == "recipe":
                found = False
                for j in unlock_recipes:
                    if j["name"] == i["recipe_name"]:
                        found = True
                        break
                if not found:
                    unlock_recipes.append({
                        "name": i["recipe_name"],
                        "description": i["description"],
                        "ing_list": i["ing_list"],
                        "potion_id": i["potion_id"], 
                    })

default is_inventory_open = False

screen show_inventory_button():
    imagebutton:
        xysize (100, 100)
        yalign 0.05
        xalign 0.95
        idle 'gui/inventory_gui_button_idle.png'
        hover 'gui/inventory_gui_button_hover.png'
        if is_inventory_open:
            action [SetScreenVariable('is_inventory_open', False), Hide("new_inventory_screen")]
        else:
            action [SetScreenVariable('is_inventory_open', True), Show("new_inventory_screen")]

label open_inventory:

    call screen new_inventory_screen()
    return


default is_choice_active = False
screen new_inventory_screen(filter='ingredients'):
    zorder 200
    modal False

    $ filter_text = ''

    if filter == 'ingredients':
        $ filter_text = 'Ингредиенты'
    elif filter == 'misc':
        $ filter_text = 'Мелочь'
    elif filter == 'recipe':
        $ filter_text = 'Рецепты'

    $ filtered_list = []
    if filter == "ingredients":
        for i in inventory:
            if i["type"] == "ingredient":
                $ filtered_list.append(i)
    elif filter == "misc":
        for i in inventory:
            if i["type"] == "misc" or i["type"] == "potion":
                $ filtered_list.append(i)
    elif filter == "recipe":
        for i in inventory:
            if i["type"] == "recipe":
                $ filtered_list.append(i)

    frame at inventory_open:
        background "#0000"  # полупрозрачный фон

        add "gui/inventory/new_inventory_clear.png":
            xalign 1.1
            ypos 140

        if is_choice_active == False:
            textbutton filter_text + " ▼":
                text_size 26
                text_color "FFD000"
                pos (1315, 690)
                action [SetScreenVariable('is_choice_active', True), Show("choice_filter")]
                text_hover_color "FFFFFF"

        $ count = 0
        for i in range(4):
            for j in range(7):
                if len(filtered_list) == 0:
                    textbutton "":
                        pos (-9999, -9999)
                        action NullAction()
                    break
                if count >= len(filtered_list):
                    continue
                imagebutton:
                    idle im.Scale(filtered_list[count]["icon"], 75, 75)
                    hover im.Scale(filtered_list[count]["icon_hover"], 75, 75)
                    action NullAction()
                    hovered Function(show_tooltip_for_item, filtered_list[count]["name"], filtered_list[count]["description"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (1300 + (j * 77), 280 + (i * 85))
                    xysize (80, 80)
                    at item_transform
                $ count += 1
    

transform inventory_open:
    xanchor 0.9999
    zoom 0
    yoffset 50
    xalign 0.95
    ypos 70
    ease 0.4 zoom 1.0 yoffset 0
    on hide:
        ease 0.4 zoom 0 yoffset 50

screen choice_filter():
    zorder 201
    modal False
    frame:
        background "#0008"  # полупрозрачный фон
        pos (1320, 690)

        vbox:
            textbutton "Ингредиенты":
                text_size 26
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="ingredients")]
                text_hover_color "FFFFFF"

            textbutton "Мелочь":
                text_size 26
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="misc")]
                text_hover_color "FFFFFF"

            textbutton "Рецепты":
                text_size 26
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="recipe")]
                text_hover_color "FFFFFF"

transform item_transform:
    subpixel True
    on hover:
        easein 0.7 zoom 1.1
    on idle:
        easein 0.7 zoom 1.0