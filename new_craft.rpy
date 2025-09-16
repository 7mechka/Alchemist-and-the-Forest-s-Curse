# define cauldron_load = []
# define slot_count = 6
# define cauldron_recipe_load = []

# init python:
#     cauldron_load = []
#     cauldron_recipe_load = []
#     def use_ingredient(item):
#         found = False
#         for used in cauldron_recipe_load:
#             if used['ing_id'] == item['ing_id']:
#                 used['count'] += 1
#                 inventory[inventory.index(item)]['count'] -= 1
#                 if inventory[inventory.index(item)]['count'] <= 0:
#                     inventory.remove(item)
#                 found = True
#                 break        
#         if not found:
#             new_used = {
#                 "count": 1,
#                 "ing_id": item['ing_id'],
#             }
#             cauldron_recipe_load.append(new_used)
#             inventory[inventory.index(item)]['count'] -= 1
#             if inventory[inventory.index(item)]['count'] <= 0:
#                 inventory.remove(item)
#     def insert_to_load(item):
#         global cauldron_load, slot_count
#         if len(cauldron_load) < slot_count:
#             cauldron_load.append(item)
#             use_ingredient(item)

#     def remove_from_load(item):
#         global cauldron_load, slot_count
#         if item in cauldron_load:
#             for used in cauldron_recipe_load:
#                 if used['ing_id'] == item['ing_id']:
#                     used['count'] -= 1
#                     if item in inventory:
#                         inventory[inventory.index(item)]['count'] += 1
#                     else:
#                         add_item(item['id'], 1)
#                     if used['count'] <= 0:
#                         cauldron_recipe_load.remove(used)
#                     break
#             cauldron_load.remove(item)

#     def potion_craft_logic():
#         global is_potion_crafted, is_lilly_potion_crafted, cauldron_load, unlock_recipes, recipes, cauldron_recipe_load
#         is_crafted = False 
#         for i in unlock_recipes:
#             tmp_recipe = {frozenset(d.items()) for d in i['ing_list']}
#             tmp_used = {frozenset(d.items()) for d in cauldron_recipe_load}    
#             if tmp_recipe == tmp_used:
#                 renpy.notify(f"Вы сварили: {i['name']}!")
#                 if i['potion_id'] == 6:
#                     is_lilly_potion_crafted = True
#                 is_crafted = True
#                 is_potion_crafted = True
#                 add_item(i['potion_id'], 1)
#                 cauldron_load = []
#                 cauldron_recipe_load = []
#                 return
#         if not is_crafted:
#             for i in recipes:
#                 tmp_recipe = {frozenset(d.items()) for d in i['ing_list']}
#                 tmp_used = {frozenset(d.items()) for d in cauldron_recipe_load}    
#                 if tmp_recipe == tmp_used:
#                     random_number = randint(0, 100)
#                     if random_number <= 20:  # 20% шанс на успех
#                         renpy.notify(f"Вы сварили: {i['name']}!")
#                         if i['potion_id'] == 6:
#                             is_lilly_potion_crafted = True
#                         is_crafted = True
#                         is_potion_crafted = True
#                         add_item(i['potion_id'], 1)
#                         cauldron_load = []
#                         cauldron_recipe_load = []
#                         return
#                     else:
#                         renpy.notify("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
#                         cauldron_load = []
#                         cauldron_recipe_load = []
#                         return
#                     break
#                 else:
#                     renpy.notify("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
#                     cauldron_load = []
#                     cauldron_recipe_load = []
#                     return
#         else:
#             renpy.notify("Вы не сварили зелье. Попробуйте использовать другие ингредиенты или получить рецепт.")
#             cauldron_load = []
#             cauldron_recipe_load = []
#             return
# screen craft_screen():
#     modal True
#     add 'gui/inventory/gui_gpt.png'

#     $ load_coords = [
#         (55, 445),
#         (220, 525),
#         (385, 450),
#         (395, 310),
#         (230, 225),
#         (60, 305)
#     ]

#     $ tmp_list = []
#     for i in inventory:
#         if i["type"] == "ingredient":
#             $ tmp_list.append(i)

#     $ count = 0
#     for i in range(3):
#         for j in range(7):
#             if count >= len(tmp_list):
#                 continue
#             imagebutton:
#                 idle im.Scale(tmp_list[count]["icon"], 75, 75)
#                 hover im.Scale(tmp_list[count]["icon_hover"], 75, 75)
#                 action Function(insert_to_load, tmp_list[count])
#                 pos (1133 + (j * 100), 172 + (i * 95))
#                 xysize (80, 80)
#             $ count += 1

#     textbutton "Изготовить":
#         pos (1500, 800)
#         action Function(potion_craft_logic)

#     textbutton "Отмена":
#         pos (1100, 800)
#         action [Return(False), Hide("new_craft_screen")]

#     for i in range(0, slot_count):
#         if i < len(cauldron_load):
#             imagebutton:
#                 idle im.Scale(cauldron_load[i]["icon"], 100, 100)
#                 hover im.Scale(cauldron_load[i]["icon_hover"], 100, 100)
#                 action Function(remove_from_load, cauldron_load[i])
#                 pos load_coords[i]
#                 xysize (100, 100)

