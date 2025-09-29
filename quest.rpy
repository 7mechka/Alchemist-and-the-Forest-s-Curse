init -20 python:
    def ing_count_increment():
        global ing_count_limit
        ing_count_limit += 1


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

define quest_list = {
    'main': [
        {
            'name': 'Поиск ингредиентов',
            'desc': 'Вы новенький в этом городе, но с большими амбициями и знаниями зельеварения. \nОднако, чтобы варить зелья, нужны ингредиенты, но у вас их нет. \nМожет, есть где-то в этой деревне место, где можно бесплатно получить простые растительные ингредиенты?',
            'quest_id': 'm0'
        },
        {
            'name': 'Первое зелье',
            'desc': 'Раздобыв базовые ингредиенты, можно приступить к варке зелий! Однако есть проблемы, вы утеряли почти все свои записи и рецепты зелий... \nВы можете попытать удачи, и случайно сварить зелье, просто бросая всё подряд в котёл... \nИли купить в какого-то торговца полноценный рецепт зелья... Выбор за вами! Хотя кое что можно вспомнить...',
            'quest_id': 'm1'
        },
        {
            'name': 'Первое знакомство',
            'desc': 'Очевидно, что в новом для вас месте вы будете отшельником для окружающих и самого себя, но ведь это можно исправить, верно? \nВы, конечно, не славитесь социальными навыками, но хотя бы какое-то знакомство завести нужно. \nКоли вам и дальше варить и продавать зелья в этой деревне, да и жить тоже, может, по крайне мере, стоит познакомиться с местными магазинчиками и торговцами? \nВ частности, будет полезным познакомится с местным травником?',
            'quest_id': 'm2'
        },
    ],
    'side': [
        {
            'name': 'Зелье для травника',
            'desc': 'Травница Лила попросила вас сварить простенькое зелье. Было бы грубо отказать, тем более за бесплатный рецепт зелья, верно?',
            'quest_id': 's0'
        }
    ]
}

default active_quest = {
    'main': [
        {
            'name': 'Поиск ингредиентов',
            'desc': 'Вы новенький в этом городе, но с большими амбициями и знаниями в зельеварении. \nОднако, чтобы варить зелья, нужны ингредиенты, но у вас их нет. \nМожет, есть где-то в этой деревне место, где можна бесплатно получить простые растительные ингредиенты?',
            'quest_id': 'm0'
        },
    ],
    'side' : []
}


init python:
    global active_quest, quest_list
    def generate_id_hint_quest():
        count = 0
        for i in active_quest['side']:
            if i['quest_id'][:2] == 'sh':
                count += 1
        return count

    def get_quest_by_id(id, List = quest_list):
        if id[0] == 'm':
            for item in List['main']:
                if item['quest_id'] == id:
                    returned_item = item.copy()
                    return returned_item
        if id[0] == 's':
            for item in List['side']:
                if item['quest_id'] == id:
                    returned_item = item.copy()
                    return returned_item

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

screen quest_screen(selected_quest_id = 'None', is_choice = False):
    add "gui/inventory/new_bg_quest2.png"
    zorder 200
    modal True

    # Кнопка закрытия
    imagebutton:
        idle "gui/inventory/inventory_exit_idle.png"
        hover "gui/inventory/inventory_exit_hover.png"
        if is_choice:
            action [Hide("quest_screen"), Return(0)]
        else:
            action Hide("quest_screen")
        pos (70, 70)

    vbox:
        pos(70, 180)
        xsize(200)
        spacing 50
        text 'Основные':
            pos(50,0)
            size 48
            color "ffd000"
        vbox:
            pos(50,-20)
            spacing 20
            for i in active_quest['main']:

                textbutton i['name']:
                    if selected_quest_id == i['quest_id']:
                        text_color "FFD000"
                    else:
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                    text_size 28
                    action [Hide("quest_screen"), Show("quest_screen", None, selected_quest_id = i['quest_id'], is_choice = is_choice)]
    vbox:
        pos(500, 180)
        $ desc_text = ''
        $ request_text = ''
        if selected_quest_id[0] == 'm':
            for i in active_quest['main']:
                if i['quest_id'] == selected_quest_id:
                    $ desc_text = i['desc']
                    if 'request' in i:
                        for j in i['request']:
                            $ request_text += f"- {j['name']} ({j['count']})\n"
        else:
            for i in active_quest['side']:
                if i['quest_id'] == selected_quest_id:
                    $ desc_text = i['desc']
                    if 'request' in i:
                        for j in i['request']:
                            $ request_text += f"- {j['name']} ({j['count']})\n"
        $ need_scroll = len(desc_text) >= 350
        viewport:
            xsize 940
            ysize 400  
            mousewheel True
            if need_scroll:
                scrollbars "vertical" 
            text desc_text:
                size 43
                xsize (940)
                color 'FFFFFF'
        text request_text:
            # Высота текста описания не больше 450, иначе прокрутка
            ypos (25)
            size 38
            color 'FFFFFF'
            xsize (940)
        if is_choice and selected_quest_id != 'None':
            textbutton 'Выбрать':
                text_color 'FFFFFF'
                text_hover_color "FF0000"
                action [Return(selected_quest_id)]



    vbox:
        pos(1480, 180)
        xsize(200)
        spacing 50
        text 'Побочные':
            pos(50,0)
            size 48
            color "ffd000"
        vbox:
            pos(50,-20)
            spacing 20
            for i in active_quest['side']:

                textbutton i['name']:
                    if selected_quest_id == i['quest_id']:
                        text_color "FFD000"
                    else:
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                    text_size 28
                    action [Hide("quest_screen"), Show("quest_screen", None, selected_quest_id = i['quest_id'], is_choice = is_choice)]

image quest_button_hover = 'gui/inventory/quest_button_active.png'
image quest_button_idle = 'gui/inventory/quest_button_idle.png'


screen show_quest_button():
    button:
        xysize (95, 93)
        yalign 0.05
        xalign 0.88

        style "empty"

        add 'gui/inventory/quest_button_idle.png'

        hovered [Function(renpy.show, "quest_button_hover", at_list=[quest_button_fade_transition], layer='screens')]
        unhovered [Function(renpy.hide, "quest_button_hover", layer='screens')]

        # idle 'gui/inventory/quest_button_idle.png'
        # hover 'gui/inventory/quest_button_active.png'
        action Show("quest_screen")

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