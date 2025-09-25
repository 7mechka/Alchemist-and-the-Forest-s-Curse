# Список инвентаря
default inventory = []

init python:
    def get_item_by_id(id, List = itemList, count=1):
        for item in List:
            if item['id'] == id:
                returned_item = item.copy()
                returned_item['count'] = count
                return returned_item


    def calculate_sell_price(buy_price):
        # Рассчитываем половину цены
        half_price = buy_price // 2
        # Округляем до ближайшего числа, кратного 5
        sell_price = int(round(half_price / 5.0) * 5)
        return sell_price

    def get_item_by_id(id, List=None, count=1):
        if List is None:
            List = itemList
        for item in List:
            if item['id'] == id:
                returned_item = item.copy()
                returned_item['count'] = count
                return returned_item
        return None

    def find_item_in_list(inventory_list, item_id):
        # Вспомогательная функция для поиска предмета в конкретном списке
        for item in inventory_list:
            if item.get('id') == item_id:
                return item
        return None

    def add_item_to_inventory(target_inventory, item_id, amount=1):
        # Функция для добавления предмета в любой инвентарь (игрока или магазина)
        base_item = get_item_by_id(item_id)
        if not base_item:
            renpy.notify(f"Ошибка: Предмет с id '{item_id}' не найден.")
            return

        existing_item = find_item_in_list(target_inventory, item_id)
        if existing_item:
            existing_item['count'] += amount
        else:
            new_item = base_item.copy()
            new_item['count'] = amount
            target_inventory.append(new_item)

    def remove_item_from_inventory(target_inventory, item_id, amount=1):
        # Функция для удаления предмета из любого инвентаря
        item_to_remove = find_item_in_list(target_inventory, item_id)
        if not item_to_remove:
            renpy.notify("Ошибка: Попытка убрать несуществующий предмет.")
            return

        item_to_remove['count'] -= amount
        if item_to_remove['count'] <= 0:
            target_inventory.remove(item_to_remove)

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
        xysize (95, 93)
        yalign 0.05
        xalign 0.945
        idle 'gui/inventory/inventory_button_idle.png'
        hover 'gui/inventory/inventory_button_active.png'
        if is_inventory_open:
            action [SetScreenVariable('is_inventory_open', False), Hide("new_inventory_screen"), Hide("choice_filter")]
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

        add "gui/inventory/inventory_clear.png":
            xalign 1.0
            ypos 80

        text "Инвентарь" xpos 1515 ypos 148 size 32 color "FFD000" font gui.name_text_font

        if is_choice_active == False:
            textbutton filter_text + " >":
                text_size 22
                text_color "FFD000"
                pos (1410, 572)
                action [SetScreenVariable('is_choice_active', True), Show("choice_filter")]
                text_hover_color "FFFFFF"

        $ count = 0
        for i in range(5):
            for j in range(6):
                if len(filtered_list) == 0:
                    textbutton "":
                        pos (-9999, -9999)
                        action NullAction()
                    break
                if count >= len(filtered_list):
                    continue
                imagebutton:
                    idle im.Scale(filtered_list[count]["icon"], 50, 50)
                    hover im.Scale(filtered_list[count]["icon_hover"], 50, 50)
                    action NullAction()
                    hovered Function(show_tooltip_for_item, filtered_list[count]["name"], filtered_list[count]["description"], filtered_list[count]["count"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (1400 + (j * 70)+5, 220 + (i * 76)-5)
                    xysize (60, 60)
                    at item_transform
                $ count += 1

        hbox:
            add im.Scale('gui/inventory/coins.png', 25, 25)
            xalign 0.88
            ypos 580
            text str(money) size 22 xpos 10 color "FFD000" font gui.name_text_font
            at item_transform
    

transform inventory_open:
    xanchor 0.9999
    zoom 0
    yoffset 50
    xalign 0.93
    ypos 70
    ease 0.4 zoom 1.0 yoffset 0
    on hide:
        ease 0.4 zoom 0 yoffset 50

screen choice_filter():
    zorder 201
    modal False
    frame:
        background "#59595988"  # полупрозрачный фон
        pos (1410, 540)

        vbox:
            textbutton "Ингредиенты":
                text_size 22
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="ingredients")]
                text_hover_color "FFFFFF"

            textbutton "Мелочь":
                text_size 22
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="misc")]
                text_hover_color "FFFFFF"

            textbutton "Рецепты":
                text_size 22
                text_color "FFD000"
                action [Hide("choice_filter"), SetScreenVariable('is_choice_active', False) ,Show("new_inventory_screen", filter="recipe")]
                text_hover_color "FFFFFF"

transform item_transform:
    subpixel True
    on hover:
        easein 0.7 zoom 1.1
    on idle:
        easein 0.7 zoom 1.0

style common_text is text:
    font "Montserrat-Regular.ttf"