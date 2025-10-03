init python:
    # Логика смены дня
    def day_change():
        global day, forest_stages, forest_room_list, default_forest_room_list
        day += 1
        # Перерасчёт стадий леса
        calculating_stages()
        # Генерация ингредиентов на все комнаты леса
        generate_rooms_ingredients()
        add_notification(f"День {day} начался!")
        # renpy.notify(f"День {day} начался!")

    def change_time(time = None):
        global time_id
        if time is not None:
            time_id = time
        if time_id == 2:
            day_change()
        time_id = (time_id + 1) % 3

define npc_state = ['man', 'women']
define npc_path = 'images/characters/npc/'
define npc_sex = choice(npc_state)

label transition(to):
    call hide_gui

    $ renpy.jump(to)
    

# Метка дома
label home:
    $ is_ball_active = True
    python:
        update_unlock_recipes()
        if ing_count_limit >= 6:
            for i in active_quest['main']:
                if i['quest_id'] == 'm0':
                    active_quest['main'].remove(i)
                    active_quest['main'].append(get_quest_by_id('m1'))
                    add_item_to_inventory(inventory, 4, 1)  # Добавляем рецепт зелья бреда
                    update_unlock_recipes()
        if is_potion_crafted:
            for i in active_quest['main']:
                if i['quest_id'] == 'm1':
                    active_quest['main'].remove(i)
                    active_quest['main'].append(get_quest_by_id('m2'))
                    is_lilly_know = True



    if time_id == 0:
        show home day with fade
    elif time_id == 1:
        show home evening with fade
    elif time_id == 2:
        show home night with fade

    call show_gui 

    menu:
        "Лечь спать":
            call hide_gui 
            python:
                change_time()
            jump home
            return
        "Пойти на работу" if time_id == 0:
            call hide_gui 
            jump work
            return
        "Спуститься в подвал":
            call hide_gui 
            hide home night with fade
            call transition("basement") 
            return
        "Пойти в город":
            if time_id == 0:
                call hide_gui 
                hide home day with fade
            elif time_id == 1:
                call hide_gui 
                hide home evening with fade
            elif time_id == 2:
                call hide_gui 
                hide home night with fade
            $ is_ball_active = False
            call screen map
            jump home
            return

label work:
    # Эта метка вызывается при нажатии на кнопку работы.
    # Здесь будет логика работы с рандомными НПС для заработка небольших денег.
    call hide_gui

    "Вы решили немного поработать, и перемещаетесь в свою лавку у дома."

    hide home with fade
    scene black
    show work with fade

    "Не проходит много времени, как вы уже на месте. \nВы начинаете работать, и вскоре к вам подходит первый клиент."
    python:
        money_earned = 0
        def generate_random_npc():
            global npc_path, npc_sex
            npc_path = 'images/characters/npc/'
            npc_sex = choice(npc_state)
            if npc_sex == 'man':
                npc_path += f'npc man{randint(1, 4)}.png'
            else:
                npc_path += f'npc women{randint(1, 2)}.png'

        def generate_random_potion_for_work():
            global money_earned, npc_potion

            npc_potion = ''

            rnd = randint(0, 100)

            money_earned += rnd

            if rnd <= 20:
                npc_potion = 'зелье от тошноты и головной боли'
            elif rnd <= 40:
                npc_potion = 'зелье против вредителей'
            elif rnd <= 60:
                npc_potion = 'зелье для улучшения сна'
            elif rnd <= 80:
                npc_potion = 'зелье для улучшения памяти'
            else:
                npc_potion = 'зелье для улучшения настроения'

    python:
        generate_random_npc()
        generate_random_potion_for_work()

    show expression npc_path as npc:
        yzoom 1.5
        xzoom 1.5
        yanchor 0
        xalign 0.5
    
    if npc_sex == 'man':
        "К вам зашёл мужчина с желанием купить зелье."
    else:
        "К вам зашла женщина с желанием купить зелье."

    "Клиент хочет приобрести: [npc_potion]."

    "Вы начинаете рассказывать о свойствах зелья, и клиент заинтересованно слушает вас."

    "После небольшой беседы, клиент решает купить зелье, благодарит вас за помощь и уходит."

    hide npc

    "Вы продолжаете работать, и вскоре к вам подходит следующий клиент."

    python:
        generate_random_npc()
        generate_random_potion_for_work()

    show expression npc_path as npc:
        yzoom 1.5
        xzoom 1.5
        yanchor 0
        xalign 0.5
    
    if npc_sex == 'man':
        "К вам зашёл мужчина с желанием купить зелье."
    else:
        "К вам зашла женщина с желанием купить зелье."

    "Клиент хочет приобрести: [npc_potion]."

    "Вы, как всегда, рассказываете о свойствах зелья, и клиент очень заинтересованно слушает вас."

    "После небольшой беседы, клиент решает купить зелье, благодарит вас за помощь и уходит."

    hide npc

    "Остаток дня вы продолжаете работать, удовлетворяя потребность жителей деревни в зельях."

    "В конце дня вы подсчитываете заработанные деньги."

    "Вы заработали [money_earned] монет."

    python:
        money += money_earned
        add_notification(f"Вы заработали {money_earned} монет. Всего: {money} монет.")
        # renpy.notify(f"Вы заработали {money_earned} монет. Всего: {money} монет.")
        change_time(1)  # Меняем время на ночь

    "Вы возвращаетесь домой, чувствуя себя удовлетворённым от проделанной работы."

    scene black with fade
    hide work

    jump home

    return
