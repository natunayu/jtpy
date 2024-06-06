import pygame

# Pygameを初期化
pygame.init()


# 接続されているジョイスティックとその詳細をリストアップする関数
def list_joysticks():
    joystick_count = pygame.joystick.get_count()
    joysticks = []

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        buttons = joystick.get_numbuttons()
        hats = joystick.get_numhats()

        joystick_info = {
            "index": i,
            "name": name,
            "axes": axes,
            "buttons": buttons,
            "hats": hats
        }

        joysticks.append(joystick_info)

    return joysticks


def joystick_event_handling():
    running = True
    layer = 0

    while running:
        # イベントキューを処理する

        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button pressed:", event.button)
            elif event.type == pygame.JOYAXISMOTION:
                if joystick.get_axis(event.axis) > 0.3:
                    print("axis", event.axis)
        pygame.time.wait(200)


# 接続されているジョイスティックとその詳細を取得
joysticks = list_joysticks()

# 詳細を表示
for joystick in joysticks:
    print(f"ジョイスティック {joystick['index']}: {joystick['name']}")
    print(f" - 軸の数: {joystick['axes']}")
    print(f" - ボタンの数: {joystick['buttons']}")
    print(f" - ハットの数: {joystick['hats']}\n")

# Pygameを初期化
pygame.init()

# ジョイスティックの初期化
pygame.joystick.init()

# 最初のジョイスティックを取得
joystick = pygame.joystick.Joystick(0)
joystick.init()

joystick_event_handling()


# Pygameを終了
pygame.quit()
