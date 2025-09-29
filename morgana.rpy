define morgana_pose_list = ['morgana-pos1', 'morgana-pos2']
define morgana_eyes_list = [
    "morgana-eyes-simple", # 0
    "morgana-eyes-smile",  # 1
    "morgana-eyes-close"  # 2
]
define morgana_mouth_list = [
    "morgana-mouth-simple", # 0
    "morgana-mouth-smile",  # 1
    "morgana-mouth-angry"  # 2
]


screen morgana_sprite(pos=0, mouth=0, eyes=0, crown=0, x_pos = 0.5):
    add 'characters/morgana/'+morgana_pose_list[pos]+".png" at default_transform xalign x_pos
    add 'characters/morgana/'+morgana_mouth_list[mouth]+".png" at default_transform xalign x_pos
    add 'characters/morgana/'+morgana_eyes_list[eyes]+".png" at default_transform xalign x_pos
    if crown != 0:
        add 'characters/morgana/morgana-crown.png' at default_transform xalign x_pos