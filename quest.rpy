init -20 python:
    def ing_count_increment():
        global ing_count_limit
        ing_count_limit += 1

default active_quests = []      # Список ID активных заданий
default completed_quests = []   # Список ID выполненных заданий

define diff_0_quest_item_list = [
    {
        'id': 0,
        'count': 3,
        'type': 'single'
    },
    {
        'id': 1,
        'count': 3,
        'type': 'single'
    },
    {
        'type': 'multi',
        'content': [
            {
                'id': 1,
                'count': 1
            },
            {
                'id': 0,
                'count': 1
            },
        ]
    }
]

default ing_count_limit = 6

default is_ball_active = False

default is_lilly_know = False

default is_lilly_meet = False

default is_potion_crafted = False

default is_lilly_potion_crafted = False

default is_s0_complete = False

# define quest_list = {
#     'main': [
#         {
#             'name': 'Поиск ингредиентов',
#             'desc': 'Вы новенький в этом городе, но с большими амбициями и знаниями зельеварения. \nОднако, чтобы варить зелья, нужны ингредиенты, но у вас их нет. \nМожет, есть где-то в этой деревне место, где можно бесплатно получить простые растительные ингредиенты?',
#             'quest_id': 'm0'
#         },
#         {
#             'name': 'Первое зелье',
#             'desc': 'Раздобыв базовые ингредиенты, можно приступить к варке зелий! Однако есть проблемы, вы утеряли почти все свои записи и рецепты зелий... \nВы можете попытать удачи, и случайно сварить зелье, просто бросая всё подряд в котёл... \nИли купить в какого-то торговца полноценный рецепт зелья... Выбор за вами! Хотя кое что можно вспомнить...',
#             'quest_id': 'm1'
#         },
#         {
#             'name': 'Первое знакомство',
#             'desc': 'Очевидно, что в новом для вас месте вы будете отшельником для окружающих и самого себя, но ведь это можно исправить, верно? \nВы, конечно, не славитесь социальными навыками, но хотя бы какое-то знакомство завести нужно. \nКоли вам и дальше варить и продавать зелья в этой деревне, да и жить тоже, может, по крайне мере, стоит познакомиться с местными магазинчиками и торговцами? \nВ частности, будет полезным познакомится с местным травником?',
#             'quest_id': 'm2'
#         },
#     ],
#     'side': [
#         {
#             'name': 'Зелье для травника',
#             'desc': 'Травница Лила попросила вас сварить простенькое зелье. Было бы грубо отказать, тем более за бесплатный рецепт зелья, верно?',
#             'quest_id': 's0'
#         }
#     ]
# }

# default active_quest = {
#     'main': [
#         {
#             'name': 'Поиск ингредиентов',
#             'desc': 'Вы новенький в этом городе, но с большими амбициями и знаниями в зельеварении. \nОднако, чтобы варить зелья, нужны ингредиенты, но у вас их нет. \nМожет, есть где-то в этой деревне место, где можна бесплатно получить простые растительные ингредиенты?',
#             'quest_id': 'm0'
#         },
#     ],
#     'side' : []
# }

init python:
    import json

    # --- 1. ЗАГРУЗКА ВСЕХ КВЕСТОВ ИЗ JSON ПРИ СТАРТЕ ИГРЫ ---
    all_quests = {}
    try:
        # Получаем правильный путь к файлу
        quests_file_path = renpy.loader.get_path("quests.json")
        with open(quests_file_path, 'r', encoding='utf-8') as f:
            all_quests_raw = json.load(f)
            # Преобразуем список квестов в удобный словарь для быстрого доступа по ID
            for category in all_quests_raw.values():
                for quest in category:
                    all_quests[quest['quest_id']] = quest
    except Exception as e:
        # Если файл не найден или в нем ошибка, выводим уведомление
        renpy.notification("Ошибка загрузки квестов: {}".format(e))


    # --- 2. УДОБНЫЕ ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ КВЕСТАМИ ---

    def get_quest_by_id(quest_id):
        """Возвращает полную информацию о квесте по его ID."""
        return all_quests.get(quest_id)

    def start_quest(quest_id):
        """
        Добавляет квест в список активных, если он существует,
        не активен и не был выполнен ранее.
        """
        if quest_id not in all_quests:
            print("Попытка начать несуществующий квест: {}".format(quest_id))
            return

        if quest_id not in active_quests and quest_id not in completed_quests:
            active_quests.append(quest_id)
            renpy.notify("Новое задание: {}".format(all_quests[quest_id]['name']))

    def complete_quest(quest_id):
        """Перемещает квест из активных в выполненные."""
        if quest_id in active_quests:
            active_quests.remove(quest_id)
            completed_quests.append(quest_id)
            renpy.notify("Задание выполнено: {}".format(all_quests[quest_id]['name']))

    def is_quest_active(quest_id):
        """Проверяет, активен ли квест."""
        return quest_id in active_quests

    def is_quest_completed(quest_id):
        """Проверяет, был ли квест уже выполнен."""
        return quest_id in completed_quests

    def get_active_quests_details():
        """Возвращает список полных данных всех активных квестов."""
        return [get_quest_by_id(qid) for qid in active_quests]


init python:
#     global active_quest, quest_list
#     def generate_id_hint_quest():
#         count = 0
#         for i in active_quest['side']:
#             if i['quest_id'][:2] == 'sh':
#                 count += 1
#         return count

#     def get_quest_by_id(id, List = quest_list):
#         if id[0] == 'm':
#             for item in List['main']:
#                 if item['quest_id'] == id:
#                     returned_item = item.copy()
#                     return returned_item
#         if id[0] == 's':
#             for item in List['side']:
#                 if item['quest_id'] == id:
#                     returned_item = item.copy()
#                     return returned_item

    def generate_hint_quest(quest_id, diff = 0):
        if diff == 0:
            random_item = choice(diff_0_quest_item_list)
            if random_item['type'] == 'single':
                item = get_item_by_id(random_item['id'])
                quest = get_quest_by_id(quest_id)
                active_quest['side'].append({
                    'name': 'Подсказка для задания!',
                    'desc': f"Для того, чтобы получить подсказку для задания {quest['name']}, нужно пожертвовать некоторыми предметами!",
                    'quest_id': f"sh{generate_id_hint_quest()}",
                    'request': [
                        {
                            'name': item['name'],
                            'id': item['id'],
                            'count': random_item['count']
                        }
                    ]
                })
            else:
                tmp_request = []
                for i in range(len(random_item['content'])):
                    item = get_item_by_id(random_item['content'][i]['id'])
                    tmp_request.append({
                        'name': item['name'],
                        'id': item['id'],
                        'count': random_item['content'][i]['count']
                    })
                quest = get_quest_by_id(quest_id)
                active_quest['side'].append({
                    'name': 'Подсказка для задания!',
                    'desc': f"Для того, чтобы получить подсказку для задания {quest['name']}, нужно пожертвовать некоторыми предметами!",
                    'quest_id': f"sh{generate_id_hint_quest()}",
                    'request': tmp_request
                })

    def pay_for_hint(quest_id):
        if quest_id[:2] != 'sh':
            return 0
        else:
            quest = get_quest_by_id(quest_id, active_quest)
            req = quest['request']
            is_found_list = []
            for i in range(len(req)):
                is_found_list.append(False)
            count = 0
            for i in inventory:
                for r in req:
                    if i['id'] == r['id'] and i['count'] >= r['count']:
                        is_found_list[count] = True
                        count += 1
                        break
            is_found_list = list(set(is_found_list))
            if len(is_found_list) <= 1 and is_found_list[0] == True:
                for i in inventory:
                    for j in req:
                        if i['id'] == j['id'] and i['count'] >= j['count']:
                            i['count'] -= j['count']
                            if i['count'] <= 0:
                                inventory.remove(i)
                            break
                return 1
            else:
                return 2

default is_quest_open = False

screen new_quest_screen(selected = None):
    zorder 200
    modal False

    fixed at [(quest_open if selected is None else null_transform), quest_close]:
        add "gui/inventory/quest_panel.png" xalign 1.0 yalign 2.0 

        fixed:
            xpos 450
            ypos 80

        
            text "Задания":
                xpos 880
                ypos 155
                size 40
                color "ffd000"
                font gui.name_text_font

            text "Активные задания":
                xpos 625
                ypos 255
                size 32
                color "ffd000"
                font gui.name_text_font

            text "Выбранное задание":
                xpos 1010
                ypos 255
                size 32
                color "ffd000"
                font gui.name_text_font

            vbox:
                $ active_quests_list = get_active_quests_details()
                if not active_quests_list:
                    pass
                else:
                    for i in active_quests_list:
                        textbutton i['name']:
                            if selected == i['quest_id']:
                                text_color "FFD000"
                            else:
                                text_color "FFFFFF"
                                text_hover_color "FFD000"
                            background "gui/inventory/quest_line.png"
                            xpos 595
                            ypos 335
                            text_size 28
                            bottom_padding 10
                            action [Show("new_quest_screen", None, selected = i['quest_id'])]
            vbox:
                $ desc_text = ''
                if selected != None:
                    $ selected_quest = get_quest_by_id(selected)
                    $ desc_text = selected_quest['desc']
                    
                $ need_scroll = len(desc_text) >= 350
                viewport:
                    xpos 1010
                    ypos 350
                    xsize 940
                    ysize 450  
                    mousewheel True
                    if need_scroll:
                        scrollbars "vertical" 
                    text desc_text:
                        size 22
                        xsize 305
                        color 'FFFFFF'

    key "K_ESCAPE" action [SetScreenVariable('is_quest_open', False), Hide("new_quest_screen"), Show('show_quest_button'), Show("show_inventory_button")]

transform quest_open:
    xanchor 0.9999
    zoom 0
    yoffset 100
    xalign 0.85
    ease 0.4 zoom 1.0 yoffset 0

transform null_transform:
    zoom 1.0

transform quest_close:
    on hide:
        ease 0.4 zoom 0 yoffset 100

image quest_button_hover = 'gui/inventory/quest_button_active.png'
image quest_button_idle = 'gui/inventory/quest_button_idle.png'

screen show_quest_button():
    button:
        xysize (95, 93)
        yalign 0.05
        xalign 0.88

        style "empty"

        add 'gui/inventory/quest_button_idle.png'

        hovered [Function(renpy.show, "quest_button_hover", at_list=[quest_button_fade_transition], layer='screens', zorder=201)]
        unhovered [Function(renpy.hide, "quest_button_hover", layer='screens')]

        if is_quest_open:
            action [Function(close_all)]
        else:
            action [Function(close_all), Function(open_quest)]

transform quest_button_fade_transition:
    xysize (95, 93)
    yalign 0.05
    xalign 0.88
    on show:
        alpha 0.0
        linear 0.1 alpha 1.0
    on hide:
        linear 0.1 alpha 0.0

label open_quest:
    call screen quest_screen()
    return

label ball_label:
    'Мистический шар для гадание испускает странные волны, эхом раздающиеся в вашей голове'

    "Словно сойдя с ума, эхо наслаивается друг на друга, и вы видите концептуальные мысли"

    "Этот шар может помочь вам с заданиями, но не бесплатно"

    menu:
        'Запросить подсказку':
            "Для какого задания вы хотите получить подсказку?"

            call screen quest_screen(is_choice = True)
            $ quest_id = _return

            if quest_id == 0:
                "Похоже, шар не может понять для какого задания вы хотите подсказку"
            elif quest_id != 'None':
                "В вашей голове всплывают образы того, чего хочет шар за подсказку..."
                python:
                    generate_hint_quest(quest_id)
            else:
                "Похоже, шар не может понять для какого задания вы хотите подсказку"
        'Заплатить за подсказку':
            "Выберите задание-подсказку"
            call screen quest_screen(is_choice = True)
            $ quest_id = _return
            if quest_id == 0:
                "Похоже, шар не может понять для какого задания вы хотите подсказку"
                jump home
            python:
                res =  pay_for_hint(quest_id)
            if res == 0:
                "Не получилось завершить задание-подсказку"
            elif res == 1:
                "Задание успешно завершено, и подсказка получена"
                python:
                    for i in active_quest['side']:
                        if i['quest_id'] == quest_id:
                            active_quest['side'].remove(i)
            else:
                'У вас недостаточно предметов для уплаты!'
        "Ничего":
            "Шар медленно успокаивается, ожидая вашего следующего запроса"
            
    
    jump home