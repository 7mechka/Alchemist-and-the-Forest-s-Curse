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

screen inventory_screen(page=1, filter="ingredients", item = None, context='inventory', source=inventory, shop="buy"):
    zorder 200
    modal True
    # Фон
    add "gui/inventory/new_bg.png"

    # Кнопка закрытия
    imagebutton:
        idle "gui/inventory/inventory_exit_idle.png"
        hover "gui/inventory/inventory_exit_hover.png"
        if context == 'craft' or context == 'shop' or filter == 'recipe':
            action Return(None)
        else:
            action Hide("inventory_screen")
        pos (70, 70)
    
    # Прорисовка ячеек инвентаря, 3 ряда по 5 штук
    for i in range(3):
        for j in range(5):
            imagebutton:
                idle "gui/inventory/inventory_frame_idle.png"
                hover "gui/inventory/inventory_frame_hover.png"
                action NullAction()
                pos (100 + (j * 240), 190 + (i * 240))
                xysize (206, 206)

    # Кнопка перелистывания страницы назад
    imagebutton:
        idle "gui/inventory/inventory_arrow_left_idle.png"
        hover "gui/inventory/inventory_arrow_left_hover.png"
        if page - 1 < 1:
            action NullAction()
        else:
            action Show("inventory_screen", None, page - 1, filter, item, context, source, shop)
        pos (100, 900)
        xysize (123, 106)

    # Кнопка перелистывания страницы вперед
    imagebutton:
        idle "gui/inventory/inventory_arrow_right_idle.png"
        hover "gui/inventory/inventory_arrow_right_hover.png"
        if page == 5:
            action NullAction()
        else:
            action Show("inventory_screen", None, page + 1, filter, item, context, source, shop)
        pos (550, 900)
        xysize (123, 106) 

    # Кнопка фильтра ингредиентов
    if filter != 'recipe':
        imagebutton:
            idle "gui/inventory/inventory_ingredients_idle.png"
            hover "gui/inventory/inventory_ingredients_hover.png"
            action Show("inventory_screen", None, page, "ingredients", None, context, source, shop)
            pos (1015, 900)
            xysize (106, 106)   

    # Кнопка фильтра мелочи
    if filter != 'recipe':
        imagebutton:
            idle "gui/inventory/inventory_misc_idle.png"
            hover "gui/inventory/inventory_misc_hover.png"
            action Show("inventory_screen", None, page, "misc", None, context, source, shop)
            pos (1155, 900)
            xysize (106, 106) 

    # Текст номера страницы инвентаря
    text str([page]):
        pos (380, 925)
        xysize (100, 100)
        size 40
        color "ffd000"

    # Деньги
    hbox:
        spacing 10
        pos (700, 910)
        xysize (200, 100)
        add "gui/inventory/coins.png"
        text str(money):
            size 40
            pos (-35, -5)  # Сдвиг текста вправо для выравнивания с иконкой
            color "ffd000"
    
    # Настройки пагинации
    default items_per_page = 15 
    default start_index = page * items_per_page - items_per_page
    default end_index = min(start_index + items_per_page, len(source))

    # Прорисовка мелочовки
    if filter == "misc":
        $ tmp_list = []
        if context == 'shop':
            for i in source:
                if i["type"] == "misc" or i["type"] == "recipe":
                    $ tmp_list.append(i)
        else:    
            for i in source:
                if i["type"] == "misc" or i["type"] == "potion":
                    $ tmp_list.append(i)
        for i in range(3):
            for j in range(5):
                $ slot_index = i * 5 + j  # Позиция в сетке (0-14)
                $ item_index = start_index + slot_index  # Реальный индекс в inventory
                if item_index < len(tmp_list):
                    imagebutton:
                        idle tmp_list[item_index]["icon"]
                        hover tmp_list[item_index]["icon_hover"]
                        action Show("inventory_screen", None, page, filter, tmp_list[item_index], context, source, shop)
                        pos (100 + (j * 240), 190 + (i * 240))
                        xysize (206, 206)
    # Прорисовка ингредиентов
    elif filter == "ingredients":
        $ tmp_list = []
        for i in source:
            if i["type"] == "ingredient":
                $ tmp_list.append(i)
        for i in range(3):
            for j in range(5):
                $ slot_index = i * 5 + j  # Позиция в сетке (0-14)
                $ item_index = start_index + slot_index  # Реальный индекс в inventory
                if item_index < len(tmp_list) and tmp_list[item_index]["type"] == "ingredient":
                    imagebutton:
                        idle tmp_list[item_index]["icon"]
                        hover tmp_list[item_index]["icon_hover"]
                        action Show("inventory_screen", None, page, filter, tmp_list[item_index], context, source, shop)
                        pos (100 + (j * 240), 190 + (i * 240))
                        xysize (206, 206)

    elif filter == 'recipe':
        $ tmp_list = []
        for i in source:
            if i["type"] == "recipe":
                $ tmp_list.append(i)
        for i in range(3):
            for j in range(5):
                $ slot_index = i * 5 + j  # Позиция в сетке (0-14)
                $ item_index = start_index + slot_index  # Реальный индекс в inventory
                if item_index < len(tmp_list) and tmp_list[item_index]["type"] == "recipe":
                    imagebutton:
                        idle tmp_list[item_index]["icon"]
                        hover tmp_list[item_index]["icon_hover"]
                        action Show("inventory_screen", None, page, filter, tmp_list[item_index], context, source, shop)
                        pos (100 + (j * 240), 190 + (i * 240))
                        xysize (206, 206)

    # Прорисовка выбраного предмета если такой есть
    if item: 
        vbox:
            pos (1410, 155)    
            spacing 20 
            add item["big_icon"]:
                xysize (300, 300)  
            vbox:
                text item["name"]:
                    ypos 40
                    xpos (-80 + ((450 - ((len(item["name"]) * 17) - 5)) // 2))
                    size 32
                    color "ffd000"
                text item["description"]:
                    pos (-80, 50)
                    xsize 500
                    color "ffd000"
            vbox:
                spacing 20
                pos (-80, 50)
                
                text "Количество: [item['count']]" size 24 color "ffd000"
                if "price" in item:
                    text "Цена: [item['price']] золота" size 24 color "ffd000"

            if context == 'craft':
                hbox:
                    spacing 10
                    pos (-80, 100)
                    textbutton "Использовать":
                        text_size 28
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                        action Return(item)
            
            if item['id'] == 5:
                hbox:
                    spacing 10
                    pos (-80, 100)
                    textbutton "Использовать":
                        text_size 28
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                        if is_ball_active == False:
                            action Function(add_notification, 'Шар для гадания можно использовать только дома')
                        else:
                            action [Hide("inventory_screen"), Call('ball_label')]

            elif context == 'shop':
                hbox:
                    spacing 10
                    pos (-80, 75)
                    if shop == "buy":
                        textbutton "Купить":
                            text_size 28
                            text_color "FFFFFF"
                            text_hover_color "FFD000"
                            action [Function(shop_manager, source, item, shop), Function(update_unlock_recipes)]
                    elif shop == "sell":
                        textbutton "Продать":
                            text_size 28
                            text_color "FFFFFF"
                            text_hover_color "FFD000"
                            action [Function(shop_manager, source, item, shop), Function(update_unlock_recipes)]

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
        # padding (10, 5)
        pos (1320, 690)

        vbox:
            # spacing 10
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