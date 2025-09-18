init python:
    def calculateDistance2(x1, x2):
        return x1 - x2

screen item_transfer_animation(item, from_pos, to_pos, cb=None, arg=None):
    zorder 95

    fixed:
        xysize 80,80
        add "gui/inventory/sparkle.png":
            at transform:
                xcenter 1.5
                ycenter 1.5
                zoom 1.8
                alpha 0.65
                alignaround (.5,.5)
                linear 4 rotate 360
                rotate 0
                repeat

        add item['icon'] 

        default distX = int(calculateDistance2(from_pos[0],to_pos[0]) / 2)
        default distY = int(calculateDistance2(to_pos[1],from_pos[1]) /2)
        at transform:
            subpixel True
            zoom 1.25
            pos from_pos
            anchor (.5,.5)
            around (from_pos[0]+distX,from_pos[1]+distY)
            parallel:
                easein 1 xpos to_pos[0]+20 ypos to_pos[1]+15 counterclockwise
                pause 0.25
                easein 0.3 yoffset +10 alpha 0
            parallel:
                easein 1.5 zoom 0.5
    
    if cb:
        timer 1.3 action [Function(cb, arg), Hide("item_transfer_animation_%s"%item['id'])]

    else:
        timer 1.3 action Hide("item_transfer_animation_%s"%item['id'])

screen item_disapear_animation(item, from_pos):
    zorder 95

    fixed:
        xysize 80,80

        add item['icon'] 

        at transform:
            subpixel True
            zoom 1.25
            pos from_pos
            anchor (.5,.5)
            parallel:
                easein 1 ypos from_pos[1]-50 alpha 0
            parallel:
                easein 1.5 zoom 0.5
    
    timer 1.3 action Hide("item_disapear_animation_%s"%item['id'])

screen blocker():
    modal True   # перехватывает все действия игрока
    zorder 9999  # выше всего
    # Можно даже добавить прозрачный фон:
    add Solid("#0000")  # полностью прозрачный

    timer 1.7 action Hide("blocker")  # скрыть через 2 секунды