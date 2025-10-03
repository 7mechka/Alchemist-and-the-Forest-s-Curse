
init python:
    config.layers.append('not_hide')

    def start_transition(target):
        renpy.call("transition", target)

# Список ингредиентов, которые могут быть использованы в зельеварении
define ingredientList = [
    {
        "name": "Горьколист",
        "description": "Тёмно-зелёный лист с горьким вкусом, часто используется для простых зелий.",
        "ing_id": 0,
    },
    {
        "name": "Каменный бутон",
        "description": "Маленький серый бутон, крепкий как камень, растёт в темных местах.",
        "ing_id": 1,
    },
    {
        "name": "Росистый стебель",
        "description": "Тонкий стебель, всегда покрытый каплями росы, не любит темноту.",
        "ing_id": 2,
    },
    {
        "name": "Коптравка",
        "description": "Тёмная трава с запахом гари, распространённая в обычных лесах.",
        "ing_id": 3,
    },
    {
        "name": "Мотыльковая трава",
        "description": "Лёгкая трава, привлекающая ночных мотыльков, растёт в тени.",
        "ing_id": 4,
    },
    {
        "name": "Пыльнокорень",
        "description": "Корень, оставляющий на пальцах жёлтую пыль, растёт под деревьями.",
        "ing_id": 5,
    },
    {
        "name": "Светоягода",
        "description": "Тускло светящаяся маленькая ягода, которая никогда не выростет на солнце.",
        "ing_id": 6,
    },
    {
        "name": "Шиполоза",
        "description": "Обычная колючая лиана, быстро растёт, очень распространённая.",
        "ing_id": 7,
    },
    {
        "name": "Ржаволист",
        "description": "Листья цвета ржавчины, легко крошатся, но обладают сильным запахом.",
        "ing_id": 8,
    },
    {
        "name": "Туманник",
        "description": "Серый гриб, растущий в утренних туманах.",
        "ing_id": 9,
    },


    {
        "name": "Светолист", 
        "description": "Листья, мерцающие в темноте, будто впитали лунный свет.", 
        "ing_id": 10,
    },
    {
        "name": "Жалоцвет", 
        "description": "Растение с ядовитыми лепестками, используемое в зельях контроля.", 
        "ing_id": 11,
    },
    {
        "name": "Сердцетрава", 
        "description": "Редкий травяной побег, усиливающий чувство эмпатии.", 
        "ing_id": 12,
    },
    {
        "name": "Сонокуст", 
        "description": "Куст, чьи лепестки источают лёгкий усыпляющий аромат.", 
        "ing_id": 13,
    },
    {
        "name": "Искролист", 
        "description": "Листья, потрескивающие от крошечных электрических импульсов.", 
        "ing_id": 14,
    },
    {
        "name": "Ледоросль", 
        "description": "Покрыта инеем в любую погоду.", 
        "ing_id": 15,
    },
]

define itemList = [
    # Горьколист ID 0
    {
        "name": ingredientList[0]['name'],
        "description": ingredientList[0]['description'],
        "icon": "gui/ingredients/Bitterleaf_idle.png",
        "icon_hover": "gui/ingredients/Bitterleaf_hover.png",
        "big_icon": "gui/ingredients/Bitterleaf_big.png",
        "ing_id": ingredientList[0]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 0
    },
    # Каменный бутон ID 1
    {
        "name": ingredientList[1]['name'],
        "description": ingredientList[1]['description'],
        "icon": "gui/ingredients/Stonebud_idle.png",
        "icon_hover": "gui/ingredients/Stonebud_hover.png",
        "big_icon": "gui/ingredients/Stonebud_big.png",
        "ing_id": ingredientList[1]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 1
    },
    # Росистый стебель ID 2
    {
        "name": ingredientList[2]['name'],
        "description": ingredientList[2]['description'],
        "icon": "gui/ingredients/Dewstem_idle.png",
        "icon_hover": "gui/ingredients/Dewstem_hover.png",
        "big_icon": "gui/ingredients/Dewstem_big.png",
        "ing_id": ingredientList[2]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 2
    },
    # Зелье бреда ID 3
    {
        "name": "Зелье бреда",
        "description": "Зелье, которое вызывает галлюцинации, но не приводит к потере рассудка.",
        "icon": "gui/items/potion_idle.png",
        "icon_hover": "gui/items/potion_hover.png",
        "big_icon": "gui/items/potion_idle.png",
        'rarity': 'common',
        "count": 1,
        "type": "potion",
        "price": 100,
        'id': 3
    },
    # Рецепт: Зелье бреда ID 4 - Горьколист ID 0 1, Пыльнокорень ID 5 2
    {
        "name": "Рецепт: Зелье бреда",
        "description": "Рецепт создания зелья бреда.\nИнгредиенты:\n- Горьколист (1 шт.)\n- Пыльнокорень (2 шт.)",
        "shop_description": "Рецепт создания зелья бреда.",
        "icon": "gui/items/recipe_idle.png",
        "icon_hover": "gui/items/recipe_hover.png",
        "big_icon": "gui/items/recipe_idle.png",
        'rarity': 'common',
        "recipe_name": "Зелье бреда",
        'recipe_description': "Зелье, которое вызывает галлюцинации, но не приводит к потере рассудка.",
        "ing_list": [
            {
                "ing_id": ingredientList[0]['ing_id'],
                "count": 1,
            },
            {
                "ing_id": ingredientList[5]['ing_id'],
                "count": 2,
            }
        ],
        "count": 1,
        "type": "recipe",
        "price": 100,
        'potion_id': 3,
        'id': 4
    },
    # Шар предсказания ID 5
    {
        "name": "Шар предсказания",
        "description": "Мистический шар для предсказания. Может помочь с активными заданиями, но не бесплатно.",
        "icon": "gui/items/ball_idle.png",
        "icon_hover": "gui/items/ball_hover.png",
        "big_icon": "gui/items/ball_idle.png",
        'rarity': 'uncommon',
        "count": 1,
        "type": "misc",
        "price": 100,
        'id': 5
    },
    # Зелье смеха ID 6
    {
        "name": "Зелье смеха",
        "description": "Зелье, которое вызывает плохо контролируемый смех и резко поднимает настроение.",
        "icon": "gui/items/potion_idle.png",
        "icon_hover": "gui/items/potion_hover.png",
        "big_icon": "gui/items/potion_idle.png",
        'rarity': 'common',
        "count": 1,
        "type": "potion",
        "price": 120,
        'id': 6
    },
    # Рецепт: Зелье смеха ID 7 - Горьколист ID 0 1, Мотыльковая трава ID 4 1, Туманник ID 9 1
    {
        "name": "Рецепт: Зелье смеха",
        "description": "Рецепт создания зелья смеха.\nИнгредиенты:\n- Горьколист (1 шт.)\n- Мотыльковая трава (1 шт.)\n- Туманник (1 шт.)",
        "shop_description": "Рецепт создания зелья смеха.",
        "icon": "gui/items/recipe_idle.png",
        "icon_hover": "gui/items/recipe_hover.png",
        "big_icon": "gui/items/recipe_idle.png",
        'rarity': 'common',
        "recipe_name": "Зелье смеха",
        'recipe_description': "Зелье, которое вызывает плохо контролируемый смех и резко поднимает настроение.",
        "ing_list": [
            {
                "ing_id": ingredientList[0]['ing_id'],
                "count": 1,
            },
            {
                "ing_id": ingredientList[4]['ing_id'],
                "count": 1,
            },
            {
                "ing_id": ingredientList[9]['ing_id'],
                "count": 1,
            }
        ],
        "count": 1,
        "type": "recipe",
        "price": 100,
        'potion_id': 6,
        'id': 7
    },
    # Зелье проявления ID 8
    {
        "name": "Зелье проявления",
        "description": "Зелье, способное проявить в реальность то, что скрыто или желает быть скрытым. Иногда лучше не смотреть на то, чего не должен...",
        "icon": "gui/items/potion_idle.png",
        "icon_hover": "gui/items/potion_hover.png",
        "big_icon": "gui/items/potion_idle.png",
        'rarity': 'uncommon',
        "count": 1,
        "type": "potion",
        "price": 170,
        'id': 8
    },
    # Рецепт: Зелье проявления ID 9 - Коптравка ID 3 1, Туманник ID 9 1, Светолист ID 10 1
    {
        "name": "Рецепт: Зелье проявления",
        "description": "Рецепт создания зелья проявления.\nИнгредиенты:\n- Коптравка (1 шт.)\n- Туманник (1 шт.)\n- Светолист (1 шт.)",
        "shop_description": "Рецепт создания зелья проявления.",
        "icon": "gui/items/recipe_idle.png",
        "icon_hover": "gui/items/recipe_hover.png",
        "big_icon": "gui/items/recipe_idle.png",
        'rarity': 'uncommon',
        "recipe_name": "Зелье проявления",
        'recipe_description': "Зелье, способное проявить в реальность то, что скрыто или желает быть скрытым. Иногда лучше не смотреть на то, чего не должен...",
        "ing_list": [
            {
                "ing_id": ingredientList[3]['ing_id'],
                "count": 1,
            },
            {
                "ing_id": ingredientList[9]['ing_id'],
                "count": 1,
            },
            {
                "ing_id": ingredientList[10]['ing_id'],
                "count": 1,
            },
        ],
        "count": 1,
        "type": "recipe",
        "price": 120,
        'potion_id': 8,
        'id': 9
    },
    # Коптравка ID 10
    {
        "name": ingredientList[3]['name'],
        "description": ingredientList[3]['description'],
        "icon": "gui/ingredients/Sootgrass_idle.png",
        "icon_hover": "gui/ingredients/Sootgrass_hover.png",
        "big_icon": "gui/ingredients/Sootgrass_big.png",
        "ing_id": ingredientList[3]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 10
    },
    # Мотыльковая трава ID 11
    {
        "name": ingredientList[4]['name'],
        "description": ingredientList[4]['description'],
        "icon": "gui/ingredients/Mothweed_idle.png",
        "icon_hover": "gui/ingredients/Mothweed_hover.png",
        "big_icon": "gui/ingredients/Mothweed_big.png",
        "ing_id": ingredientList[4]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 11
    },
    # Пыльнокорень ID 12
    {
        "name": ingredientList[5]['name'],
        "description": ingredientList[5]['description'],
        "icon": "gui/ingredients/Dustroot_idle.png",
        "icon_hover": "gui/ingredients/Dustroot_hover.png",
        "big_icon": "gui/ingredients/Dustroot_big.png",
        "ing_id": ingredientList[5]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 12
    },
    # Светоягода ID 13
    {
        "name": ingredientList[6]['name'],
        "description": ingredientList[6]['description'],
        "icon": "gui/ingredients/Glowberry_idle.png",
        "icon_hover": "gui/ingredients/Glowberry_hover.png",
        "big_icon": "gui/ingredients/Glowberry_big.png",
        "ing_id": ingredientList[6]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 13
    },
    # Шиполоза ID 14
    {
        "name": ingredientList[7]['name'],
        "description": ingredientList[7]['description'],
        "icon": "gui/ingredients/Thornvine_idle.png",
        "icon_hover": "gui/ingredients/Thornvine_hover.png",
        "big_icon": "gui/ingredients/Thornvine_big.png",
        "ing_id": ingredientList[7]['ing_id'],
        'rarity': 'common',
        "count": 1, 
        "type": "ingredient",
        "price": 50,
        'id': 14
    },
    # Ржаволист ID 15
    {
        "name": ingredientList[8]['name'],
        "description": ingredientList[8]['description'],
        "icon": "gui/ingredients/Rustleaf_idle.png",
        "icon_hover": "gui/ingredients/Rustleaf_hover.png",
        "big_icon": "gui/ingredients/Rustleaf_big.png",
        "ing_id": ingredientList[8]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 15
    },
    # Туманник ID 16
    {
        "name": ingredientList[9]['name'],
        "description": ingredientList[9]['description'],
        "icon": "gui/ingredients/Fogcap_idle.png",
        "icon_hover": "gui/ingredients/Fogcap_hover.png",
        "big_icon": "gui/ingredients/Fogcap_big.png",
        "ing_id": ingredientList[9]['ing_id'],
        'rarity': 'common',
        "count": 1,
        "type": "ingredient",
        "price": 50,
        'id': 16
    },
    # Светолист ID 17
    {
        "name": ingredientList[10]["name"], 
        "description": ingredientList[10]["description"],
        "icon": "gui/ingredients/Lightleaf_idle.png", 
        "icon_hover": "gui/ingredients/Lightleaf_hover.png",
        "big_icon": "gui/ingredients/Lightleaf_big.png",
        "ing_id": ingredientList[10]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 17,
    },
    # Жалоцвет ID 18
    {
        "name": ingredientList[11]["name"], 
        "description": ingredientList[11]["description"],
        "icon": "gui/ingredients/Stingblossom_idle.png", 
        "icon_hover": "gui/ingredients/Stingblossom_hover.png",
        "big_icon": "gui/ingredients/Stingblossom_big.png",
        "ing_id": ingredientList[11]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 18,
    },
    # Сердцетрава ID 19
    {
        "name": ingredientList[12]["name"], 
        "description": ingredientList[12]["description"],
        "icon": "gui/ingredients/Heartgrass_idle.png", 
        "icon_hover": "gui/ingredients/Heartgrass_hover.png",
        "big_icon": "gui/ingredients/Heartgrass_big.png",
        "ing_id": ingredientList[12]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 19,
    },
    # Сонокуст ID 20
    {
        "name": ingredientList[13]["name"], 
        "description": ingredientList[13]["description"],
        "icon": "gui/ingredients/Sleepbush_idle.png", 
        "icon_hover": "gui/ingredients/Sleepbush_hover.png",
        "big_icon": "gui/ingredients/Sleepbush_big.png",
        "ing_id": ingredientList[13]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 20,
    },
    # Искролист ID 21
    {
        "name": ingredientList[14]["name"], 
        "description": ingredientList[14]["description"],
        "icon": "gui/ingredients/Sparkleaf_idle.png", 
        "icon_hover": "gui/ingredients/Sparkleaf_hover.png",
        "big_icon": "gui/ingredients/Sparkleaf_big.png",
        "ing_id": ingredientList[14]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 21,
    },
    # Ледоросль ID 22
    {
        "name": ingredientList[15]["name"], 
        "description": ingredientList[15]["description"],
        "icon": "gui/ingredients/Icevine_idle.png", 
        "icon_hover": "gui/ingredients/Icevine_hover.png",
        "big_icon": "gui/ingredients/Icevine_big.png",
        "ing_id": ingredientList[15]["ing_id"],
        "rarity": "uncommon",
        "count": 1,
        "type": "ingredient",
        "price": 75,
        "id": 22,
    },
]