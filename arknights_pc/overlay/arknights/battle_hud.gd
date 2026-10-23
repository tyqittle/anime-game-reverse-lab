extends CanvasLayer
# Battle HUD and image bindings on top of the real upstream Godot tower-defense map.
# Does not reimplement the pathfinding, attacks, towers, or enemy AI.

var status: Label
var details: Label
var finished := false
var clock := 0.0
var slots: Array = []


func _ready() -> void:
    layer = 6
    var path := "res://arknights/assets/manifest.json"
    if FileAccess.file_exists(path):
        var payload = JSON.parse_string(FileAccess.get_file_as_string(path))
        if payload is Dictionary:
            slots = payload.get("slots", [])
    var overlay := PanelContainer.new()
    overlay.position = Vector2(18, 18)
    overlay.custom_minimum_size = Vector2(490, 0)
    add_child(overlay)
    var content := VBoxContainer.new()
    overlay.add_child(content)
    var title := Label.new()
    title.text = "RHODES FIELD LAB  /  演示关卡 01"
    title.add_theme_font_size_override("font_size", 22)
    content.add_child(title)
    status = Label.new()
    content.add_child(status)
    details = Label.new()
    details.text = "点击地图上的炮塔基座 → 选干员职业并部署。\n攻塔行为与敌人寻路来自 Outpost Assault；这里是适配试验关卡。"
    content.add_child(details)
    var actions := HBoxContainer.new()
    content.add_child(actions)
    var restart := Button.new()
    restart.text = "重新开始"
    restart.pressed.connect(func() -> void: get_tree().reload_current_scene())
    actions.add_child(restart)
    var menu := Button.new()
    menu.text = "返回首页"
    menu.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://arknights/launcher.tscn"))
    actions.add_child(menu)

    var stage = get_parent()
    var spawner = stage.get_node_or_null("Spawner")
    if spawner != null:
        spawner.enemies_defeated.connect(_on_victory)
    var objective = stage.get_node_or_null("Objective")
    if objective != null:
        objective.destroyed.connect(_on_defeat)


func _process(delta: float) -> void:
    clock += delta
    if clock < 0.35:
        return
    clock = 0.0
    if status != null:
        status.text = "部署点 DP  " + str(Global.money) + "    |    先锋 12  ·  狙击 18  ·  术师 23" + ("    |    战斗结束" if finished else "")
    if not finished:
        _attach_chibis()


func _attach_chibis() -> void:
    var stage = get_parent()
    for node in stage.find_children("TurretSlot*", "Area2D", true, false):
        var turret: Node = node.get("turret")
        if turret == null or not is_instance_valid(turret):
            continue
        if turret.get_node_or_null("AKChibi") != null:
            continue
        var type_name := str(turret.name).to_lower()
        var image_path := ""
        for item in slots:
            if item is Dictionary and type_name.contains(str(item.get("turret", "-unmatched-"))):
                image_path = str(item.get("chibi", ""))
                break
        if not image_path.begins_with("res://") or not ResourceLoader.exists(image_path):
            continue
        var tex = load(image_path) as Texture2D
        if tex == null:
            continue
        var sprite := Sprite2D.new()
        sprite.name = "AKChibi"
        sprite.texture = tex
        var longest = maxf(float(tex.get_width()), float(tex.get_height()))
        sprite.scale = Vector2.ONE * (105.0 / maxf(longest, 1.0))
        sprite.position = Vector2(0, -30)
        sprite.z_index = 50
        turret.add_child(sprite)


func _on_victory() -> void:
    if finished:
        return
    finished = true
    AKBridge.in_battle = false
    AKBridge.record_clear()
    details.text = "作战完成 · 战绩已保存在本机。\n你可以返回首页查看累计通关次数。"


func _on_defeat() -> void:
    if finished:
        return
    finished = true
    AKBridge.in_battle = false
    details.text = "目标失守 · 本次没有解锁进度。\n点击重新开始，再部署干员。"
