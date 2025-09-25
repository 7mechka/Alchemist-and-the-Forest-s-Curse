screen info_window(message):
    modal True
    zorder 300

    # лёгкая затемнённость задника (~15%)
    add Solid("#00000026")

    # Внешний фрейм = рамка (цвет рамки)
    frame:
        background Solid("#AAAAAA")   # цвет рамки
        padding (3, 3)                     # толщина рамки = 3px
        xalign 0.5
        yalign 0.5

        # Внутренний фрейм = тело окна (тёмно-серый, 75% прозрачности)
        frame:
            background Solid("#333333C0")  # #333333 с альфой C0 (~75%)
            padding (20, 20)
            xmaximum 0.8
            ymaximum 0.8

            vbox:
                spacing 15
                xalign 0.5

                text message:
                    size 28
                    color "#FFFFFF"
                    xmaximum 0.8
                    
                    # text автоматически переносится; можно добавить `slow_cps`/`layout` при необходимости

                textbutton "Ок":
                    xalign 0.5
                    action Hide("info_window")

default notif_queue = []
default active_notifs = []
default notif_id_counter = 0

init python:
    def add_notification(msg, duration=3.5):
        """
        Добавляем уведомление в очередь, но не более 3 одинаковых
        """
        global notif_queue, active_notifs

        # считаем сколько раз уже есть такое сообщение
        count = 0
        for e in notif_queue:
            if e["msg"] == msg:
                count += 1
        for e in active_notifs:
            if e["msg"] == msg:
                count += 1

        if count >= 3:
            return  # не добавляем, если уже есть 3

        notif_queue.append({"msg": msg, "duration": duration})
        _show_next_notification()

    def _show_next_notification():
        """
        Если на экране меньше 4 уведомлений — показать следующее
        """
        global notif_queue, active_notifs, notif_id_counter

        if len(active_notifs) < 4 and notif_queue:
            item = notif_queue.pop(0)

            tag = f"notif_{notif_id_counter}"
            notif_id_counter += 1

            entry = {"msg": item["msg"], "duration": item["duration"], "tag": tag}
            active_notifs.append(entry)

            renpy.show_screen("notification", notif_msg=entry["msg"], duration=entry["duration"], tag=entry['tag'], _tag=tag)
    def _close_notification(tag):
        """
        Скрыть уведомление по тэгу
        """
        global active_notifs

        renpy.hide_screen(tag)

        for e in list(active_notifs):
            if e["tag"] == tag:
                active_notifs.remove(e)
                break

        _show_next_notification()

screen notification(notif_msg, duration, tag):
    # Текущий тег экрана Ren’Py прокидывает автоматически
    $ tag = tag

    # вычисляем позицию этого уведомления (0..3)
    $ idx = 0
    for i, e in enumerate(active_notifs):
        if e["tag"] == tag:
            $ idx = i
            break

    frame:
        xpos 10
        ypos 10 + idx * 50
        background Frame(Solid("#333333C0"), 3, 3)
        padding (10, 8)

        text notif_msg size 20 color "#fff" xmaximum 340 

        at notif_anim

    # авто-закрытие
    timer duration action Function(_close_notification, tag)

transform notif_anim:
    on show:
        alpha 0.0
        linear 0.2 alpha 1.0
    on hide:
        linear 0.2 alpha 0.0

init python:
    def show_tooltip_for_item(name, desc, count=1):
        # Берём текущую позицию мыши и смещаем, чтобы тултип не ёлозил под курсором
        x, y = renpy.get_mouse_pos()
        x += 16
        y += 16

        # Прячем предыдущий тултип немедленно (без анимации),
        # чтобы гарантированно пересоздать экран с новыми аргументами.
        # renpy.hide_screen("tooltip_screen")

        # Показываем новый экран с аргументами
        renpy.show_screen("tooltip_screen", name, desc, count, (x, y))


# Экран подсказки
# Экран тултипа
screen tooltip_screen(name, desc, count, position=(0,0)):
    zorder 400
    frame at tooltip_style:
        style_prefix "tooltip"
        xysize (250, None)
        if position[0] - 250 <= 0:
            xpos position[0] + 250
            ypos position[1]
        else:
            pos position
        vbox:
            spacing 5
            text f"{name} {count}x" style "tooltip_name"
            text desc style "tooltip_desc"

# Стили для тултипа
style tooltip_frame is frame:
    background "#0008"  # полупрозрачный фон
    padding (10, 5)

style tooltip_name is text:
    font gui.name_text_font
    size 22
    color "#ffcc66"     # мягкий жёлтый (можно поменять)
    bold True

style tooltip_desc is text:
    size 18
    color "#fff"

# TRANSFORMS
transform tooltip_style:
    on show:
        alpha 0.0
        zoom 0.5
        anchor (1.0, 0.0)
        parallel:
            easein 0.12 alpha 1.0
        parallel:
            easein 0.12 zoom 1.0
    on hide:
        alpha 1.0
        zoom 1.0
        anchor (1.0, 0.0)
        parallel:
            easeout 0.12 alpha 0.0
        parallel:
            easeout 0.12 zoom 0.5

