## Offline save & pause extension for official MIT-licensed Godot JRPG demo.
## Uses the ORIGINAL upstream scenes, combat engine, tiles, sprites, and dialogue.
extends Node

const SAVE_DIRECTORY := "user://offline_game"
const SAVE_FILE := "user://offline_game/slot1.json"
const BACKUP_FILE := "user://offline_game/slot1.backup.json"
const VERSION := 1

var menu: PanelContainer
var status: Label
var _ready_for_save := false
var _last_position := Vector2(-999999.0, -999999.0)
var _save_timer := 0.0
var _message_timer := 0.0

func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS
    _setup_interface()
    call_deferred("_initial_restore")

func _process(delta: float) -> void:
    if _message_timer > 0.0:
        _message_timer -= delta
        if _message_timer <= 0.0:
            status.text = "F5 保存 | F9 读取 | Esc 菜单 | 本机单机"
    if not _ready_for_save or get_tree().paused:
        return
    _save_timer += delta
    if _save_timer >= 6.0:
        _save_timer = 0.0
        var hero := _player()
        if hero != null and hero.position.distance_to(_last_position) > 0.1:
            save_game(true)

func _unhandled_key_input(event: InputEvent) -> void:
    if not event is InputEventKey or not event.pressed or event.echo:
        return
    match event.keycode:
        KEY_F5:
            save_game(false)
            get_viewport().set_input_as_handled()
        KEY_F9:
            load_game(false)
            get_viewport().set_input_as_handled()
        KEY_ESCAPE:
            toggle_pause()
            get_viewport().set_input_as_handled()

func _player() -> Node2D:
    var scene := get_tree().current_scene
    if scene == null:
        return null
    # Upstream removes Exploration during battle; avoid corrupt mid-combat saves.
    return scene.get_node_or_null(^"Exploration/Grid/Player") as Node2D

func _grid() -> TileMapLayer:
    var hero := _player()
    if hero == null:
        return null
    return hero.get_parent() as TileMapLayer

func _message(value: String) -> void:
    status.text = value
    _message_timer = 4.0

func save_game(silent: bool = false) -> bool:
    var hero := _player()
    var grid := _grid()
    if hero == null or grid == null:
        _message("请先返回探索地图再存档")
        return false
    var defeated := {}
    for pawn in grid.get_children():
        if pawn is Walker and pawn != hero:
            defeated[pawn.name] = bool(pawn.lost)
    var cell := grid.local_to_map(hero.position)
    var data := {"version": VERSION, "cell": [cell.x, cell.y],
                 "defeated": defeated, "timestamp": Time.get_datetime_string_from_system()}
    if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(SAVE_DIRECTORY)) != OK:
        _message("本地存档目录创建失败")
        return false
    if FileAccess.file_exists(SAVE_FILE):
        DirAccess.copy_absolute(ProjectSettings.globalize_path(SAVE_FILE),
                                ProjectSettings.globalize_path(BACKUP_FILE))
    var handle := FileAccess.open(SAVE_FILE, FileAccess.WRITE)
    if handle == null:
        _message("本地存档写入失败")
        return false
    handle.store_string(JSON.stringify(data, "  "))
    handle.close()
    _last_position = hero.position
    if not silent:
        _message("本地进度已保存")
    return true

func _initial_restore() -> void:
    await get_tree().process_frame
    await get_tree().process_frame
    _ready_for_save = true
    if FileAccess.file_exists(SAVE_FILE):
        load_game(true)

func load_game(silent: bool = false) -> bool:
    var hero := _player()
    var grid := _grid()
    if hero == null or grid == null:
        _message("只能在探索地图读取进度")
        return false
    if not FileAccess.file_exists(SAVE_FILE):
        if not silent:
            _message("没有本地存档，继续新游戏")
        return false
    var handle := FileAccess.open(SAVE_FILE, FileAccess.READ)
    if handle == null:
        _message("读取本地存档失败")
        return false
    var data = JSON.parse_string(handle.get_as_text())
    handle.close()
    if not data is Dictionary or data.get("version") != VERSION:
        _message("本地存档格式错误")
        return false
    var pair = data.get("cell")
    if not pair is Array or pair.size() != 2:
        _message("存档坐标错误")
        return false
    if not (pair[0] is int or pair[0] is float) or not (pair[1] is int or pair[1] is float):
        _message("存档坐标类型错误")
        return false
    if abs(float(pair[0])) > 10000 or abs(float(pair[1])) > 10000:
        _message("存档坐标超出范围")
        return false
    var target := Vector2i(int(pair[0]), int(pair[1]))
    var previous := grid.local_to_map(hero.position)
    if target != previous and grid.get_cell_source_id(target) != -1:
        _message("目标格被占据，未移动角色")
        return false
    if target != previous:
        grid.set_cell(previous, -1)
        grid.set_cell(target, 0, Vector2i.ZERO)
        hero.position = grid.map_to_local(target)
    var defeated = data.get("defeated", {})
    if defeated is Dictionary:
        for pawn in grid.get_children():
            if pawn is Walker and defeated.has(pawn.name):
                pawn.lost = bool(defeated[pawn.name])
    _last_position = hero.position
    _save_timer = 0.0
    if not silent:
        _message("已读取本地存档")
    return true

func toggle_pause() -> void:
    var enabled := not menu.visible
    menu.visible = enabled
    get_tree().paused = enabled

func _quit_game() -> void:
    save_game(true)
    get_tree().paused = false
    get_tree().quit()

func _setup_interface() -> void:
    var canvas := CanvasLayer.new()
    canvas.layer = 95
    canvas.process_mode = Node.PROCESS_MODE_ALWAYS
    get_tree().root.add_child.call_deferred(canvas)
    var main := Control.new()
    main.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    main.mouse_filter = Control.MOUSE_FILTER_IGNORE
    canvas.add_child(main)
    status = Label.new()
    status.text = "F5 保存 | F9 读取 | Esc 菜单 | 本机单机"
    status.position = Vector2(12, 12)
    status.add_theme_color_override("font_color", Color.WHITE)
    status.add_theme_color_override("font_shadow_color", Color.BLACK)
    main.add_child(status)
    menu = PanelContainer.new()
    menu.visible = false
    menu.set_anchors_preset(Control.PRESET_CENTER)
    menu.offset_left = -200
    menu.offset_right = 200
    menu.offset_top = -150
    menu.offset_bottom = 150
    main.add_child(menu)
    var column := VBoxContainer.new()
    column.add_theme_constant_override("separation", 12)
    menu.add_child(column)
    var heading := Label.new()
    heading.text = "开源 JRPG · 离线单机"
    heading.add_theme_font_size_override("font_size", 25)
    heading.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    column.add_child(heading)
    _button(column, "继续游戏", toggle_pause)
    _button(column, "保存进度 (F5)", _save_button)
    _button(column, "读取存档 (F9)", _load_button)
    _button(column, "退出游戏", _quit_game)

func _button(column: VBoxContainer, label: String, callback: Callable) -> void:
    var button := Button.new()
    button.text = label
    button.custom_minimum_size = Vector2(340, 42)
    column.add_child(button)
    button.pressed.connect(callback)

func _save_button() -> void:
    save_game(false)

func _load_button() -> void:
    load_game(false)
