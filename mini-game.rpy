default mix_value = 50.0
default mix_zone_min = 40.0
default mix_zone_max = 60.0
default mix_time_in_zone = 0.0
default mix_total_time = 30.0
default mix_elapsed = 0.0
default mix_running = False
default mix_required = 15.0
default mix_required_fraction = 0.5
default mix_drift_speed = 15.0
default _mix_last_update = 0.0
default _mix_result = None   # <- сюда запишем результат (True/False)

init python early:
    import time
    import renpy.store as store

    def start_mix_game(total_time=30.0, required_fraction=0.5, drift_speed=15.0,start_value=50.0, zone_min=40.0, zone_max=60.0):
        store.mix_total_time = float(total_time)
        store.mix_value = float(start_value)
        store.mix_zone_min = float(zone_min)
        store.mix_zone_max = float(zone_max)
        store.mix_time_in_zone = 0.0
        store.mix_elapsed = 0.0
        store.mix_running = True
        store._mix_last_update = time.time()
        store.mix_required_fraction = float(required_fraction)
        store.mix_required = store.mix_total_time * store.mix_required_fraction
        store.mix_drift_speed = float(drift_speed)
        store._mix_result = None

    def update_mix_tick():
        if not store.mix_running:
            return

        now = time.time()
        dt = now - store._mix_last_update
        if dt <= 0:
            dt = 0.0
        store._mix_last_update = now

        # Обновляем прошедшее время
        store.mix_elapsed += dt

        # Дрейф влево
        store.mix_value -= store.mix_drift_speed * dt
        if store.mix_value < 0.0:
            store.mix_value = 0.0
        if store.mix_value > 100.0:
            store.mix_value = 100.0

        # Время в зоне
        if store.mix_zone_min <= store.mix_value <= store.mix_zone_max:
            store.mix_time_in_zone += dt

        # Проверка конца игры
        if store.mix_elapsed >= store.mix_total_time:
            store.mix_running = False
            store._mix_result = (store.mix_time_in_zone >= store.mix_required)
            renpy.restart_interaction()

    def push_right(amount=8.0):
        store.mix_value = min(store.mix_value + float(amount), 100.0)

screen mixing_game(total_time=10.0, target_ratio=0.5, callback = None):
    zorder 100
    modal True
    # ----------- Игровые переменные -----------
    default gauge_value = 0.5       # Позиция стрелки (0.0 слева, 1.0 справа)
    default gauge_velocity = 0.0    # Скорость стрелки (от кликов)
    default time_in_zone = 0.0      # Суммарное время в зелёной зоне
    default remaining_time = total_time
    default game_started = False    # Флаг: игра началась после первого клика

    # ----------- Настройки -----------
    $ drift_speed = 0.05    # Естественное смещение влево
    $ click_speed = 0.01     # Толчок вправо при клике
    $ decay = 0.8           # Затухание скорости
    $ zone_min = 0.4
    $ zone_max = 0.6

    # ----------- Таймер обновления (работает только после начала игры) -----------
    timer 0.05 repeat True action If(
        game_started, 
        [
            # Затухание импульса
            SetScreenVariable("gauge_velocity", gauge_velocity * decay),
            # Плавное движение стрелки + дрейф влево
            SetScreenVariable("gauge_value", min(1.0, max(0.0, gauge_value + gauge_velocity - drift_speed * 0.05))),
            # Подсчёт времени в зелёной зоне
            If(gauge_value >= zone_min and gauge_value <= zone_max,
                true=SetScreenVariable("time_in_zone", time_in_zone + 0.05),
                false=NullAction()),
            # Уменьшаем оставшееся время
            SetScreenVariable("remaining_time", max(0.0, remaining_time - 0.05))
        ],
        NullAction()
    )

    # ----------- Конец игры -----------
    if remaining_time <= 0.0 and game_started:
        $ success_time = total_time * target_ratio
        if time_in_zone >= success_time:
            text "Успех!\nВ зоне: [time_in_zone-1.0:.1f] сек (нужно [success_time:.1f])": 
                align (0.5, 0.5) size 40
            textbutton "ОК" align (0.5, 0.7) action [Hide('mixing_game'), Function(callback, True)]
        else:
            text "Провал!\nВ зоне: [time_in_zone:.1f] сек (нужно [success_time:.1f])":
                align (0.5, 0.5) size 40
            textbutton "ОК" align (0.5, 0.7) action [Hide('mixing_game'), Function(callback, False)]

    # ----------- Интерфейс игры -----------
    else:
        frame:
            align (0.5, 0.5)
            xysize (600, 400)
            has vbox
            spacing 30
            xalign 0.5
            yalign 0.5

            text "Осталось времени: [remaining_time:.1f]" size 30 xalign 0.5

            fixed:
                xysize (400, 40)
                # Фон шкалы
                add Solid("#cccccc") xysize (400, 40)
                # Зелёная зона
                add Solid("#00ff00") xpos int(400 * zone_min) ypos 0 xsize int(400 * (zone_max - zone_min)) ysize 40
                # Красная стрелка
                add Solid("#ff0000") xpos int(gauge_value * 400) ypos 0 xsize 5 ysize 40

            if not game_started:
                text "Кликай, чтобы удерживать стрелку в зелёной зоне!" size 25 xalign 0.5
            else:
                text "Кликай, чтобы удерживать стрелку в зелёной зоне!" size 25 xalign 0.5

    # ----------- Клик мыши -----------
    key "mousedown_1" action [
        SetScreenVariable("game_started", True),           # Первый клик запускает игру
        SetScreenVariable("gauge_velocity", gauge_velocity + click_speed)   # Добавляем импульс
    ]