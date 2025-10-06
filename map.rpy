screen map():
    zorder 200
    modal True
    frame:
        background None
        style 'empty'
        use show_map_button
        use show_inventory_button
        use show_quest_button
    
    frame at map_open:
        yalign 0.8
        xalign 0.5
        background Frame("gui/inventory/clear_frame.png", 10, 10)

        frame:
            background Frame("gui/map.png", 5, 5, radius=30) xsize 1475 ysize 830

            textbutton "Дом":
                pos (840, 680)
                text_color "FFFFFF"
                text_hover_color "FFD000"
                action [Function(close_map), Function(hide_gui), Function(renpy.call, "transition", "home")]
            
            textbutton "Лес":
                pos (180, 350)
                text_color "FFFFFF"
                text_hover_color "FFD000"
                action [Function(close_map), Function(hide_gui), Function(renpy.call, "transition", "forest_handler")]

            if is_lilly_know == True:
                if is_lilly_meet == False:
                    textbutton "Травник":
                        pos (500, 300)
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                        action [Function(close_map), Function(hide_gui), Jump("lilly_home")]
                else:
                    textbutton 'Лилли':
                        pos (500, 300)
                        text_color "FFFFFF"
                        text_hover_color "FFD000"
                        action [Function(close_map), Function(hide_gui), Jump("lilly_home")]

image map_button_hover = 'gui/inventory/map_button_active.png'
image map_button_idle = 'gui/inventory/map_button_idle.png'

default is_map_open = False

screen show_map_button():
    button:
        xysize (95, 93)
        yalign 0.05
        xalign 0.815

        style "empty"

        add 'gui/inventory/map_button_idle.png'

        hovered [Function(renpy.show, "map_button_hover", at_list=[map_button_fade_transition], layer='screens', zorder=201)]
        unhovered [Function(renpy.hide, "map_button_hover", layer='screens')]

        if is_map_open:
            action [Function(close_all)]
        else:
            action [Function(close_all), Function(open_map), Function(hide_gui)]

transform map_button_fade_transition:
    xysize (95, 93)
    yalign 0.05
    xalign 0.815
    on show:
        alpha 0.0
        linear 0.1 alpha 1.0
    on hide:
        linear 0.1 alpha 0.0

transform map_open:
    xanchor 0.9999
    zoom 0
    yoffset -760
    xalign 0.8
    ease 0.4 zoom 1.0 yoffset 0 xalign 0.5
    on hide:
        ease 0.4 zoom 0 yoffset -760 xalign 0.8