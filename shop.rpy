default is_shop_filter_active = False
default is_inventory_filter_active = False

init python:
    def process_shop_transaction(item, transaction_type, amount, player_inventory, shop_inventory_list):
        # Основная функция, обрабатывающая логику покупки/продажи
        global money
        item_id = item.get('id')

        if transaction_type == 'buy':
            buy_price = item.get('price', 10) # <-- ИЗМЕНЕНИЕ: Используем 'price'
            total_cost = amount * buy_price
            
            if money < total_cost:
                renpy.notify("Недостаточно денег!")
                return
            
            shop_item = find_item_in_list(shop_inventory_list, item_id)
            if not shop_item or shop_item.get('count', 0) < amount:
                renpy.notify("В магазине нет столько предметов!")
                return
            
            money -= total_cost
            remove_item_from_inventory(shop_inventory_list, item_id, amount)
            add_item_to_inventory(player_inventory, item_id, amount)
            renpy.notify(f"Куплено {amount} x {item['name']}")

        elif transaction_type == 'sell':
            buy_price = item.get('price', 10) # <-- ИЗМЕНЕНИЕ: Берем 'price' для расчета
            sell_price = calculate_sell_price(buy_price) # <-- ИЗМЕНЕНИЕ: Рассчитываем цену продажи
            total_gain = amount * sell_price
            
            player_item = find_item_in_list(player_inventory, item_id)
            if not player_item or player_item.get('count', 0) < amount:
                renpy.notify("У вас нет столько предметов для продажи!")
                return

            money += total_gain
            remove_item_from_inventory(player_inventory, item_id, amount)
            add_item_to_inventory(shop_inventory_list, item_id, amount)
            renpy.notify(f"Продано {amount} x {item['name']}")

        renpy.restart_interaction()

# --- Экран подтверждения количества ---
screen shop_confirm_transaction(item, transaction_type, shop_inventory):
    zorder 202
    modal True

    default transaction_amount = 1

    frame:
        align (0.5, 0.5)
        padding (25, 25)
        background Frame("gui/inventory/clear_frame.png", 15, 15)

        vbox:
            spacing 15
            xalign 0.5

            text f"Сколько {item['name']} вы хотите { 'купить' if transaction_type == 'buy' else 'продать' }?": 
                size 24
                color "FFFFFF"
                xalign 0.5
            
            hbox:
                xalign 0.5
                spacing 20
                textbutton "-" action SetScreenVariable("transaction_amount", max(1, transaction_amount - 1)) text_color "FFFFFF" text_hover_color "FFD000"
                text "[transaction_amount]": 
                    size 26
                    ypos 10
                    color "FFFFFF"
                textbutton "+" action SetScreenVariable("transaction_amount", min(item['count'], transaction_amount + 1)) text_color "FFFFFF" text_hover_color "FFD000"

            $ total_cost = 0
            if transaction_type == 'buy':
                $ total_cost = transaction_amount * item.get('price', 10) # <-- ИЗМЕНЕНИЕ: Используем 'price'
            else:
                $ sell_price = calculate_sell_price(item.get('price', 10)) # <-- ИЗМЕНЕНИЕ: Рассчитываем цену продажи
                $ total_cost = transaction_amount * sell_price
            
            text f"Итоговая цена: [total_cost] монет" color "FFFFFF"

            hbox:
                xalign 0.5
                spacing 20
                # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
                # Отмена теперь закрывает и окно выбора предмета
                textbutton "Отмена" action [Hide("shop_confirm_transaction"), SetScreenVariable('selected_item', None)] text_color "FFFFFF" text_hover_color "FFD000"
                # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
                # Передаем глобальный 'inventory' и локальный 'shop_inventory' в функцию
                textbutton "Подтвердить" action [
                    Function(process_shop_transaction, item=item, transaction_type=transaction_type, amount=transaction_amount, player_inventory=inventory, shop_inventory_list=shop_inventory), 
                    Hide("shop_confirm_transaction"), 
                    SetScreenVariable('selected_item', None)
                    ] text_color "FFFFFF" text_hover_color "FFD000"
                
    

# --- Экран выбора действия с предметом (купить/продать) ---
screen shop_item_action(item, source, shop_inventory):
    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
    # zorder повышен, убран modal и фон
    zorder 201
    modal False
    
    frame:
        # Размещаем по центру сверху
        xalign 0.624
        ypos 220
        padding (25, 25)
        background Frame("gui/inventory/clear_frame.png", 15, 15)

        vbox:
            spacing 10
            xalign 0.5

            add im.Scale(item["icon"], 100, 100) xalign 0.5
            text item["name"]: 
                size 26 
                xalign 0.5
                color "FFD000"
                font gui.name_text_font

            hbox:
                spacing 20
                xalign 0.5
                textbutton f"Купить\n{item.get('price', 10)} монет": # <-- ИЗМЕНЕНИЕ: Используем 'price'
                    action Show("shop_confirm_transaction", item=item, transaction_type='buy', shop_inventory=shop_inventory)
                    sensitive source == 'shop'
                    text_size 28
                    if source != 'shop':
                        text_color "#808080" 
                    else:
                        text_color "FFFFFF"
                    text_hover_color "FFD000"
                
                $ sell_price = calculate_sell_price(item.get('price', 10)) # <-- ИЗМЕНЕНИЕ: Рассчитываем цену продажи для кнопки
                textbutton f"Продать\n{sell_price} монет":
                    action Show("shop_confirm_transaction", item=item, transaction_type='sell', shop_inventory=shop_inventory)
                    sensitive source == 'player'
                    text_size 28
                    if source != 'player':
                        text_color "#808080" 
                    else:
                        text_color "FFFFFF"
                    text_hover_color "FFD000"
    
    # Закрытие окна по Escape теперь убирает выбранный предмет
    key "game_menu" action SetScreenVariable('selected_item', None)

# --- Твой основной экран магазина с изменениями ---
screen shop_screen(shop_inventory, shop_name, shop_filter='ingredients', inventory_filter='ingredients'):
    zorder 200
    modal True
    
    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
    # Добавляем переменные для отслеживания выбранного предмета
    default selected_item = None
    default item_source = None

    # Отображаем окно действия, если предмет выбран
    if selected_item:
        use shop_item_action(item=selected_item, source=item_source, shop_inventory=shop_inventory)

    # Секция магазина (левая часть)
    frame:
        $ shop_filter_text = ''
        if shop_filter == 'ingredients': 
            $ shop_filter_text = 'Ингредиенты'
        elif shop_filter == 'misc': 
            $ shop_filter_text = 'Мелочь'
        elif shop_filter == 'recipe': 
            $ shop_filter_text = 'Рецепты'

        $ shop_filtered_list = [i for i in shop_inventory if (shop_filter == "ingredients" and i["type"] == "ingredient") or (shop_filter == "misc" and (i["type"] == "misc" or i["type"] == "potion")) or (shop_filter == "recipe" and i["type"] == "recipe")]

        background "#0000"
        add "gui/inventory/inventory_clear.png" xalign 0.3 ypos 160

        text shop_name xpos 640 ypos 230 size 32 color "FFD000" font gui.name_text_font

        if not is_shop_filter_active:
            textbutton shop_filter_text + " >":
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                pos (490, 652)
                action [SetScreenVariable('is_shop_filter_active', True), Show("shop_choice_filter", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter=inventory_filter)]

        $ count = 0
        for i in range(4):
            for j in range(7):
                if count >= len(shop_filtered_list): 
                    break
                $ current_item_from_shop = shop_filtered_list[count]
                imagebutton:
                    idle im.Scale(current_item_from_shop["icon"], 50, 50)
                    hover im.Scale(current_item_from_shop["icon_hover"], 50, 50)
                    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
                    # Теперь клик просто устанавливает переменные экрана
                    action [SetScreenVariable('selected_item', current_item_from_shop), SetScreenVariable('item_source', 'shop')]
                    hovered Function(show_tooltip_for_item, current_item_from_shop["name"], current_item_from_shop["description"], current_item_from_shop["count"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (480 + (j * 70)+6, 300 + (i * 76)-5)
                    xysize (60, 60)
                $ count += 1
            if count >= len(shop_filtered_list): 
                break

    # Кнопка закрытия магазина
    frame:
        xalign 0.624
        ypos 650
        padding (10, 10)
        background Frame("gui/inventory/clear_frame.png", 10, 10)
        textbutton "Закрыть магазин" action [Hide("shop_screen"), Return(None)] text_color "FFFFFF" text_hover_color "FFD000" text_size 24


    # Секция инвентаря (правая часть)
    frame:
        $ inventory_filter_text = ''
        if inventory_filter == 'ingredients': 
            $ inventory_filter_text = 'Ингредиенты'
        elif inventory_filter == 'misc': 
            $ inventory_filter_text = 'Мелочь'
        elif inventory_filter == 'recipe': 
            $ inventory_filter_text = 'Рецепты'

        $ inventory_filtered_list = [i for i in inventory if (inventory_filter == "ingredients" and i["type"] == "ingredient") or (inventory_filter == "misc" and (i["type"] == "misc" or i["type"] == "potion")) or (inventory_filter == "recipe" and i["type"] == "recipe")]
        
        background "#0000"
        add "gui/inventory/inventory_clear.png" xalign 1.0 ypos 160

        text "Инвентарь" xpos 1515 ypos 230 size 32 color "FFD000" font gui.name_text_font

        if not is_inventory_filter_active:
            textbutton inventory_filter_text + " >":
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                pos (1410, 652)
                action [SetScreenVariable('is_inventory_filter_active', True), Show("inventory_choice_filter", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter=inventory_filter)]

        $ count = 0
        for i in range(5):
            for j in range(6):
                if count >= len(inventory_filtered_list): 
                    break
                $ current_item_from_inventory = inventory_filtered_list[count]
                imagebutton:
                    idle im.Scale(current_item_from_inventory["icon"], 50, 50)
                    hover im.Scale(current_item_from_inventory["icon_hover"], 50, 50)
                    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
                    action [SetScreenVariable('selected_item', current_item_from_inventory), SetScreenVariable('item_source', 'player')]
                    hovered Function(show_tooltip_for_item, current_item_from_inventory["name"], current_item_from_inventory["description"], current_item_from_inventory["count"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (1400 + (j * 70)+5, 300 + (i * 76)-5)
                    xysize (60, 60)
                $ count += 1
            if count >= len(inventory_filtered_list): 
                break


    # Деньги игрока
    hbox:
        add im.Scale('gui/inventory/coins.png', 25, 25)
        xalign 0.88
        ypos 667
        text str(money) size 22 xpos 10 color "FFD000" font gui.name_text_font

# Экраны фильтров остаются без изменений
screen inventory_choice_filter(shop_inventory, shop_name, shop_filter, inventory_filter):
    zorder 202
    modal False
    frame:
        background "#59595988"
        pos (1410, 552)
        vbox:
            textbutton "Ингредиенты": 
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='ingredients')]
            textbutton "Мелочь": 
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='misc')]
            textbutton "Рецепты": 
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='recipe')]

screen shop_choice_filter(shop_inventory, shop_name, shop_filter, inventory_filter):
    zorder 202
    modal False
    frame:
        background "#59595988"
        pos (490, 552)
        vbox:
            textbutton "Ингредиенты":
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='ingredients', inventory_filter=inventory_filter)]
            textbutton "Мелочь":
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='misc', inventory_filter=inventory_filter)]
            textbutton "Рецепты":
                text_size 22
                text_color "FFD000"
                text_hover_color "FFFFFF"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='recipe', inventory_filter=inventory_filter)]

transform shop_left:
    xpos 0.1