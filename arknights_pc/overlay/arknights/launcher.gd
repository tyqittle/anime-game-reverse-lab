extends Control
# Main menu for the Arknights-inspired single-player experiment.
# The combat stage comes from the pinned Outpost Assault open-source engine.

func _ready() -> void:
    var background := ColorRect.new()
    background.color = Color("#0b1720")
    background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(background)

    var root := VBoxContainer.new()
    root.anchor_left = 0.09
    root.anchor_right = 0.91
    root.anchor_top = 0.09
    root.anchor_bottom = 0.94
    root.add_theme_constant_override("separation", 20)
    add_child(root)

    var title := Label.new()
    title.text = "离线战术试验场   /   RHODES FIELD LAB"
    title.add_theme_font_size_override("font_size", 34)
    title.add_theme_color_override("font_color", Color("#e1f4fc"))
    root.add_child(title)

    var sub := Label.new()
    sub.text = "以真实 MIT 开源塔防项目为底座 · 本地演示 · 非官方明日方舟客户端"
    sub.add_theme_font_size_override("font_size", 15)
    sub.add_theme_color_override("font_color", Color("#83a7b5"))
    root.add_child(sub)

    var status := Label.new()
    status.text = "最高战绩：" + ("已通关" if AKBridge.has_clear else "尚未通关") + "     累计完成：" + str(AKBridge.wins)
    status.add_theme_font_size_override("font_size", 21)
    root.add_child(status)

    var slots := HBoxContainer.new()
    slots.add_theme_constant_override("separation", 12)
    root.add_child(slots)

    var records: Array = []
    var path := "res://arknights/assets/manifest.json"
    if FileAccess.file_exists(path):
        var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
        if parsed is Dictionary:
            records = parsed.get("slots", [])

    for index in range(3):
        var item: Dictionary = records[index] if index < records.size() and records[index] is Dictionary else {}
        var card := VBoxContainer.new()
        card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        slots.add_child(card)
        var pic := TextureRect.new()
        pic.custom_minimum_size = Vector2(180, 230)
        pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
        pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
        var portrait = str(item.get("portrait", ""))
        if portrait.begins_with("res://") and ResourceLoader.exists(portrait):
            pic.texture = load(portrait) as Texture2D
        card.add_child(pic)
        var caption := Label.new()
        caption.text = str(item.get("name", ["先锋", "狙击", "术师"][index]))
        caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        caption.add_theme_font_size_override("font_size", 18)
        card.add_child(caption)
        var role := Label.new()
        role.text = str(item.get("role", "测试单位"))
        role.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        role.add_theme_color_override("font_color", Color("#97aeb9"))
        card.add_child(role)

    var start := Button.new()
    start.text = "开始第一关  /  START OPERATION"
    start.custom_minimum_size = Vector2(300, 58)
    start.pressed.connect(_start)
    root.add_child(start)

    var note := Label.new()
    note.text = "场景、寻路、波次、目标、炮塔及射击全部沿用 Outpost Assault 原始代码。\n此版本只使用三个职业映射演示；没有宣称已实现原版干员技能或原版关卡。"
    note.add_theme_color_override("font_color", Color("#7899a9"))
    root.add_child(note)


func _start() -> void:
    get_tree().change_scene_to_file("res://scenes/maps/map_template.tscn")
