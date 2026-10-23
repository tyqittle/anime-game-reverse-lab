extends Node
# Progress and DP economy layered over the existing open-source combat scene.

const SAVE_PATH := "user://arknights_td/progress.json"
var has_clear := false
var wins := 0
var in_battle := false
var regeneration := 0.0


func _ready() -> void:
    _load_progress()
    get_tree().scene_changed.connect(_on_scene_changed)
    call_deferred("_check_scene")


func _check_scene() -> void:
    if get_tree().current_scene != null:
        _on_scene_changed(get_tree().current_scene)


func _on_scene_changed(scene: Node) -> void:
    in_battle = scene.name == "MapTemplate"
    if not in_battle:
        return
    Global.is_gameover = false
    Global.turret_prices = {"gatling": 12, "single": 18, "missile": 23}
    Global.money = 36
    regeneration = 0.0
    var overlay = load("res://arknights/battle_hud.gd").new()
    scene.add_child(overlay)


func _process(delta: float) -> void:
    if not in_battle or Global.is_gameover:
        return
    regeneration += delta
    if regeneration >= 1.3:
        var earned := int(regeneration / 1.3)
        regeneration -= float(earned) * 1.3
        Global.money = mini(99, Global.money + earned)


func record_clear() -> void:
    if has_clear:
        wins += 1
    else:
        has_clear = true
        wins = 1
    _save_progress()


func _load_progress() -> void:
    if not FileAccess.file_exists(SAVE_PATH):
        return
    var saved = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
    if saved is Dictionary and int(saved.get("version", 0)) == 1:
        has_clear = bool(saved.get("has_clear", false))
        wins = clampi(int(saved.get("wins", 0)), 0, 999999)


func _save_progress() -> void:
    DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://arknights_td"))
    var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if file == null:
        push_warning("Cannot save local progress: " + str(FileAccess.get_open_error()))
        return
    file.store_string(JSON.stringify({"version": 1, "has_clear": has_clear, "wins": wins}))
    file.close()
