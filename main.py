import time

import PIL

import services

our_turn_indicator_img: PIL.Image.Image = PIL.Image.open("screenshots/assets/our_turn_indicator.png").convert('RGB')

POINTS_COORDS = [1290, 744, 1383, 777]

INCOMING_TILE_COORDS = (77, 725)
OUTGOING_TILE_COORDS = (1717, 725)

HAND_MIDDLE_COORDS = (910, 1014)

SERI_AC_BUTTON_COORDS = (1800, 270)
CIFT_AC_BUTTON_COORDS = (1800, 370)
INSERT_TILES_BUTTON_COORDS = (1800, 580)
SERI_DIZ_BUTTON_COORDS = (1850, 930)
CIFT_DIZ_BUTTON_COORDS = (75, 930)

GIVE_TILE_BACK_COORDS = (77, 470)

WITHDRAW_TILE_COORDS = (1335, 600)

TILES_LEFT_IN_THE_MIDDLE_CORDS = (1317, 614, 1360, 646)


def sort_hand():
    services.click(SERI_DIZ_BUTTON_COORDS)


def take_incoming_tile():
    services.hold_click_while_carrying(INCOMING_TILE_COORDS, OUTGOING_TILE_COORDS)


def give_tile_back():
    services.click(give_tile_back())


def withdraw_tile():
    services.click(WITHDRAW_TILE_COORDS)


def read_points() -> int:
    read = services.read_text(POINTS_COORDS)
    print(read)
    try:
        return int(read)
    except ValueError:
        time.sleep(0.5)
        return read_points()


def remaining_tiles() -> int:
    return int(services.read_text(TILES_LEFT_IN_THE_MIDDLE_CORDS))


def insert_tiles():
    services.click(INSERT_TILES_BUTTON_COORDS)


def seri_ac():
    services.click(SERI_AC_BUTTON_COORDS)


while True:
    timer_icon = services.take_screenshot((0, 0, *our_turn_indicator_img.size))

    # check if it matches our timer screenshot, if not, restart
    if not services.images_are_similar(timer_icon, our_turn_indicator_img):
        print("not equal to our ")
        time.sleep(5.0)
        continue

    print("equal")
    time.sleep(3.0)
    open_hand = False

    base_points = read_points()

    # take the incoming tile and see if our points increase and we can open our hand
    take_incoming_tile()
    sort_hand()

    points = read_points()

    if points > base_points and points >= 101:
        open_hand = True

    else:
        give_tile_back()
        withdraw_tile()
        sort_hand()

        points = read_points()
        # if remaining tiles are less than 4, open hand
        if remaining_tiles() < 4 and points > 101:
            open_hand = True

    if open_hand:
        seri_ac()
        insert_tiles()

    time.sleep(15.0)
