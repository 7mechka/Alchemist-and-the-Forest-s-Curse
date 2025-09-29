define elsa_pose_list = ['elsa-pos1', 'elsa-pos2', 'elsa-pos2-phone']
define elsa_eyes_list = [
    'elsa-eye-simple', # 0
    'elsa-eye-angry',  # 1
    'elsa-eye-close',  # 2
    'elsa-eye-close-angry',  # 3
    'elsa-eye-close-left',  # 4
    'elsa-eye-close-right',  # 5
    'elsa-eye-shocked', # 6
    'elsa-eye-spy' # 7
    ]
define elsa_mouth_list = [
    'elsa-mouth-smile', # 0
    'elsa-mouth-simple', # 1
    'elsa-mouth-angry', # 2
    'elsa-mouth-shocked', # 3
    'elsa-mouth-smile-simple', # 4
    'elsa-mouth-spy' # 5
    ]
define elsa_jacket_list = ['elsa-jacket1', 'elsa-jacket2']

screen elsa_sprite(pos=0, mouth=0, eyes=0, jacket=0, pircing=0, phone=0, x_pos = 0.5):
    add 'characters/elsa/'+elsa_pose_list[pos]+".png" at default_transform xalign x_pos
    add 'characters/elsa/'+elsa_mouth_list[mouth]+".png" at default_transform xalign x_pos
    add 'characters/elsa/'+elsa_eyes_list[eyes]+".png" at default_transform xalign x_pos
    if jacket != 0:
        add 'characters/elsa/'+elsa_jacket_list[jacket-1]+".png" at default_transform xalign x_pos
    if pircing != 0:
        add 'characters/elsa/elsa-pircing.png' at default_transform xalign x_pos
    if phone != 0:
        add 'characters/elsa/elsa-phone.png' at default_transform xalign x_pos