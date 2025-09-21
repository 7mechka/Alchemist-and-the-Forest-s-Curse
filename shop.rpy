default is_shop_filter_active = False
default is_inventory_filter_active = False

screen shop_screen(shop_inventory, shop_name, shop_filter='ingredients', inventory_filter='ingredients'):
    zorder 200
    modal True
    frame:
        $ shop_filter_text = ''

        if shop_filter == 'ingredients':
            $ shop_filter_text = 'Ингредиенты'
        elif shop_filter == 'misc':
            $ shop_filter_text = 'Мелочь'
        elif shop_filter == 'recipe':
            $ shop_filter_text = 'Рецепты'

        $ shop_filtered_list = []
        
        if shop_filter == "ingredients":
            for i in shop_inventory:
                if i["type"] == "ingredient":
                    $ shop_filtered_list.append(i)
        elif shop_filter == "misc":
            for i in shop_inventory:
                if i["type"] == "misc" or i["type"] == "potion":
                    $ shop_filtered_list.append(i)
        elif shop_filter == "recipe":
            for i in shop_inventory:
                if i["type"] == "recipe":
                    $ shop_filtered_list.append(i)

        background "#0000"  # полупрозрачный фон

        add "gui/inventory/new_inventory_clear.png":
            xalign 0.01
            ypos 140

        if is_shop_filter_active == False:
            textbutton shop_filter_text + " ▼":
                text_size 26
                text_color "FFD000"
                pos (160, 690)
                action [SetScreenVariable('is_shop_filter_active', True), Show("shop_choice_filter", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter=inventory_filter)]
                text_hover_color "FFFFFF"


        $ shop_list = shop_filtered_list
        $ count = 0
        for i in range(4):
            for j in range(7):
                if len(shop_filtered_list) == 0:
                    textbutton "":
                        pos (-9999, -9999)
                        action NullAction()
                    break
                if count >= len(shop_filtered_list):
                    break
                imagebutton:
                    idle im.Scale(shop_filtered_list[count]["icon"], 75, 75)
                    hover im.Scale(shop_filtered_list[count]["icon_hover"], 75, 75)
                    action NullAction()
                    hovered Function(show_tooltip_for_item, shop_filtered_list[count]["name"], shop_filtered_list[count]["description"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (150 + (j * 77), 280 + (i * 85))
                    xysize (80, 80)
                    at item_transform
                $ count += 1

    frame:
        $ inventory_filter_text = ''

        if inventory_filter == 'ingredients':
            $ inventory_filter_text = 'Ингредиенты'
        elif inventory_filter == 'misc':
            $ inventory_filter_text = 'Мелочь'
        elif inventory_filter == 'recipe':
            $ inventory_filter_text = 'Рецепты'

        $ inventory_filtered_list = []
        if inventory_filter == "ingredients":
            for i in inventory:
                if i["type"] == "ingredient":
                    $ inventory_filtered_list.append(i)
        elif inventory_filter == "misc":
            for i in inventory:
                if i["type"] == "misc" or i["type"] == "potion":
                    $ inventory_filtered_list.append(i)
        elif inventory_filter == "recipe":
            for i in inventory:
                if i["type"] == "recipe":
                    $ inventory_filtered_list.append(i)

        background "#0000"  # полупрозрачный фон

        add "gui/inventory/new_inventory_clear.png":
            xalign 1.1
            ypos 140

        if is_inventory_filter_active == False:
            textbutton inventory_filter_text + " ▼":
                text_size 26
                text_color "FFD000"
                pos (1315, 690)
                action [SetScreenVariable('is_inventory_filter_active', True), Show("inventory_choice_filter", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter=inventory_filter)]
                text_hover_color "FFFFFF"

        $ count = 0
        for i in range(4):
            for j in range(7):
                if len(inventory_filtered_list) == 0:
                    textbutton "":
                        pos (-9999, -9999)
                        action NullAction()
                    break
                if count >= len(inventory_filtered_list):
                    continue
                imagebutton:
                    idle im.Scale(inventory_filtered_list[count]["icon"], 75, 75)
                    hover im.Scale(inventory_filtered_list[count]["icon_hover"], 75, 75)
                    action NullAction()
                    hovered Function(show_tooltip_for_item, inventory_filtered_list[count]["name"], inventory_filtered_list[count]["description"])
                    unhovered Function(renpy.hide_screen, "tooltip_screen")
                    pos (1300 + (j * 77), 280 + (i * 85))
                    xysize (80, 80)
                    at item_transform
                $ count += 1

screen inventory_choice_filter(shop_inventory, shop_name, shop_filter, inventory_filter):
    zorder 201
    modal False
    frame:
        background "#0008"  # полупрозрачный фон
        pos (1315, 690)

        vbox:
            textbutton "Ингредиенты":
                text_size 26
                text_color "FFD000"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='ingredients')]
                text_hover_color "FFFFFF"

            textbutton "Мелочь":
                text_size 26
                text_color "FFD000"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='misc')]
                text_hover_color "FFFFFF"

            textbutton "Рецепты":
                text_size 26
                text_color "FFD000"
                action [Hide("inventory_choice_filter"), SetScreenVariable('is_inventory_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter=shop_filter, inventory_filter='recipe')]
                text_hover_color "FFFFFF"

screen shop_choice_filter(shop_inventory, shop_name, shop_filter, inventory_filter):
    zorder 201
    modal False
    frame:
        background "#0008"  # полупрозрачный фон
        # padding (10, 5)
        pos (160, 690)

        vbox:
            # spacing 10
            textbutton "Ингредиенты":
                text_size 26
                text_color "FFD000"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='ingredients', inventory_filter=inventory_filter)]
                text_hover_color "FFFFFF"

            textbutton "Мелочь":
                text_size 26
                text_color "FFD000"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='misc', inventory_filter=inventory_filter)]
                text_hover_color "FFFFFF"

            textbutton "Рецепты":
                text_size 26
                text_color "FFD000"
                action [Hide("shop_choice_filter"), SetScreenVariable('is_shop_filter_active', False) ,Show("shop_screen", None, shop_inventory=shop_inventory, shop_name=shop_name, shop_filter='recipe', inventory_filter=inventory_filter)]
                text_hover_color "FFFFFF"