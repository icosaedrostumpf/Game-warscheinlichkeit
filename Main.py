import pygame
import random
import time
import pickle

#-515 62 -327 -base minecraft
# Initialize Pygame
pygame.init()

# Constants
CURRENTVERSION = "beta0.2"
Screen_width, Screen_height = 0, 0
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 180, 240)
BUTTON_UNLOCKED_COLOR = (35, 65, 90)
BUTTON_UNLOCKED_HOVER_COLOR = (50, 90, 120)
TEXT_COLOR = (255, 255, 255)
DICE_SIZE = 50
FPS = 360
UPGRADE_COST_BASE_MINMAX = 1.1
UPGRADE_COST_BASE_MULTIEXPO = 2

# Set up the screen
screen = pygame.display.set_mode((Screen_width, Screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Dice Roll Game")
Screen_width, Screen_height = screen.get_width(), screen.get_height()

# Fonts
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 28)

# Dice display position
dice_pos = (Screen_width // 2 - DICE_SIZE // 2, Screen_height // 2 - DICE_SIZE // 2 )

# Button setup
button_rect = pygame.Rect(Screen_width // 2 - 60, Screen_height - 80, 120, 50)
upgrade_button_rect = pygame.Rect(Screen_width - 200, 60, 150, 50)
upgrade_min_button_rect = pygame.Rect(Screen_width - 200, 175, 150, 50)
upgrade_multi_button_rect = pygame.Rect(Screen_width- 200, 290, 150, 50)
upgrade_expo_button_rect = pygame.Rect(Screen_width- 200, 405, 150, 50)
upgrade_anitime_button_rect = pygame.Rect(20, 185, 250, 50)
unlock_Auto_button_rect = pygame.Rect(20, 300, 250, 50)


# Game variables
score = 0
result = 0
rolling = False
animating = True
final_roll = None
animation_start_time = 0
animation_duration = 1  # Animation duration in seconds
max_dice_value = 6
min_dice_value = 1
multi_value = 1 
expo_value = 1
upgrade_max_cost = 10
upgrade_min_cost = 10
upgrade_multi_cost = 1000
upgrade_expo_cost = 100000
upgrade_anitime_cost = 1
Reset = False
resettimes = 0
unlock_automation_cost = 8

# Helper functions
def format_number_with_short_name(number):
    """
    Format a number with apostrophes as thousands separators 
    and use shorthand notation for large values.

    Args:
        number (int or float): The number to format.

    Returns:
        str: The formatted string.
    """
    if not isinstance(number, (int, float)):
        raise ValueError("Input must be an integer or a float.")
    
    # Define suffixes for large numbers
    suffixes = [
        (10**n, s) for n, s in [
            (303, "Cen"), (300, "Nn"), (297, "On"), (294, "Sn"), (291, "SxN"), (288, "Qin"), (285, "Qun"),
            (282, "Tn"), (279, "Dn"), (276, "Un"), (273, "Nog"), (270, "Noo"), (267, "Ooc"), (264, "Soo"),
            (261, "SxO"), (258, "QiO"), (255, "Quo"), (252, "ToO"), (249, "DoO"), (246, "UoO"), (243, "Oct"),
            (240, "NoS"), (237, "OoS"), (234, "SoS"), (231, "SxS"), (228, "QiS"), (225, "QuS"), (222, "ToS"),
            (219, "DoS"), (216, "UoS"), (213, "Sep"), (210, "NoH"), (207, "OoH"), (204, "SoH"), (201, "SxH"),   
            (198, "QiH"), (195, "QuH"), (192, "ToH"), (189, "DoH"), (186, "UoH"), (183, "Sex"), (180, "NoF"),
            (177, "OoF"), (174, "SoF"), (171, "SxF"), (168, "QiF"), (165, "QuF"), (162, "ToF"), (159, "DoF"),
            (156, "UoF"), (153, "Quin"), (150, "NoT"), (147, "OoT"), (144, "SoT"), (141, "SxT"), (138, "QiT"),
            (135, "QuT"), (132, "ToT"), (129, "DoT"), (126, "UoT"), (123, "Quad"), (120, "NoTr"), (117, "OoTr"),
            (114, "SoTr"), (111, "SxTr"), (108, "QiTr"), (105, "QuTr"), (102, "ToTr"), (99, "DoTr"), (96, "UoTr"),
            (93, "Trig"), (90, "NoV"), (87, "OoV"), (84, "SoV"), (81, "SxV"), (78, "QiV"), (75, "QuV"), (72, "ToV"),
            (69, "DoV"), (66, "UoV"), (63, "V"), (60, "Nd"), (57, "Od"), (54, "Spd"), (51, "Sed"), (48, "Qid"),
            (45, "Qud"), (42, "Td"), (39, "Dd"), (36, "Ud"), (33, "De"), (30, "No"), (27, "Oc"), (24, "Sp"),
            (21, "Sx"), (18, "Qi"), (15, "Qa"), (12, "T"), (9, "B"), (6, "M"), (3, "K")
        ]
    ]

    
    # Apply the correct suffix if applicable
    for value, suffix in suffixes:
        if number >= value:
            formatted = f"{number / value:.1f}".rstrip("0").rstrip(".")  # Avoid trailing .0
            return f"{formatted}{suffix}"
    
    # Default case: Use apostrophes for small numbers
    return f"{number:,}".replace(",", "'")


#save data
def save_data(Saveversion, data, filename="savefile.pkl"):
    """
    Saves data to a file using pickle.
    
    :param data: The data to be saved.
    :param filename: The name of the file to save data to (default is "savefile.pkl").
    """
    try:
        with open(filename, "wb") as file:
            pickle.dump((Saveversion, data), file)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

# Auto-click variables
auto_click_enabled = False
auto_click_interval = animation_duration  # Time in seconds between automatic rolls
last_auto_click_time = time.time()

def auto_click():
    global rolling, last_auto_click_time,animation_start_time
    if auto_click_enabled and not rolling:
        auto_click_interval = animation_duration
        current_time = time.time()
        if current_time - last_auto_click_time >= auto_click_interval:
            rolling = True
            animation_start_time = time.time()
            last_auto_click_time = current_time


#load data
def load_data(filename="savefile.pkl"):
    """
    Loads data from a pickle file.
    
    :param filename: The name of the file to load data from (default is "savefile.pkl").
    :return: The loaded data, or None if an error occurs.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Save file not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def Change_save_version(Old_version):
    if Old_version == "beta0.1":
        auto_click_enabled = False
        _,(score, result, rolling, animating, final_roll, animation_start_time,
                 animation_duration, max_dice_value, min_dice_value, multi_value,
                 expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost,
                 upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes) = load_data()
        return (CURRENTVERSION,(score, result, rolling, animating, final_roll, animation_start_time,
                 animation_duration, max_dice_value, min_dice_value, multi_value,
                 expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost,
                 upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes, auto_click_enabled))

#load data if possible
if load_data() != None:
    try:
        Saveversion,(score, result, rolling, animating, final_roll, animation_start_time,
                    animation_duration, max_dice_value, min_dice_value, multi_value,
                    expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost,
                    upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes, auto_click_enabled) = load_data()
    except ValueError:
        Oldver, _ = load_data()
        Saveversion,(score, result, rolling, animating, final_roll, animation_start_time,
                    animation_duration, max_dice_value, min_dice_value, multi_value,
                    expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost,
                    upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes, auto_click_enabled) = Change_save_version(Oldver)


def draw_text(text, pos, color=TEXT_COLOR, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos

    screen.blit(text_surface, text_rect)

def draw_button(rect, text, hover_color, default_color):
    color = hover_color if rect.collidepoint(pygame.mouse.get_pos()) else default_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = button_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def roll_dice_animation():
    global final_roll, rolling, score, animating, max_dice_value, min_dice_value, resettimes
    global result, animation_start_time, animation_duration, multi_value, expo_value, Reset
    global upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost

    if not rolling:
        if final_roll != None :
            if expo_value > 1:
                draw_text(f"({final_roll} x {multi_value}) ^ {expo_value} = {format_number_with_short_name(result)}", dice_pos, center=True)
            elif multi_value > 1:
                draw_text(f"{final_roll} x {multi_value} = {format_number_with_short_name(result)}", dice_pos, center=True)
            else:
                draw_text(f"{format_number_with_short_name(final_roll)}", dice_pos, center=True)
            return
        else:
            return


    current_time = time.time()
    if current_time - animation_start_time < animation_duration and not auto_click_enabled:
        animating = True
        dice_number = random.randint(min_dice_value, max_dice_value)
        draw_text(str(dice_number), dice_pos, center=True)
    else:
        try:
            animating = False
            final_roll = random.randint(min_dice_value, max_dice_value)
            rolling = False
            result = (final_roll * multi_value) ** expo_value
            result = round(result)
            score += result
        except OverflowError:
            Reset = True
            resettimes += 1
            score = 0
            result = 0
            rolling = False
            animating = True
            final_roll = None
            animation_start_time = 0
            max_dice_value = 6
            min_dice_value = 1
            multi_value = 1
            expo_value = 1
            upgrade_max_cost = 10
            upgrade_min_cost = 10
            upgrade_multi_cost = 1000
            upgrade_expo_cost = 100000
def Clicks(event):
    global score, rolling, animation_start_time, animation_duration, max_dice_value, upgrade_expo_cost
    global min_dice_value, multi_value, expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost
    global upgrade_anitime_cost, resettimes
    if button_rect.collidepoint(event.pos) and not rolling:
        rolling = True
        animation_start_time = time.time()
        return

    if upgrade_button_rect.collidepoint(event.pos) and score >= upgrade_max_cost:
        max_dice_value += 1
        score -= upgrade_max_cost
        score = round(score)
        upgrade_max_cost = UPGRADE_COST_BASE_MINMAX * upgrade_max_cost
        upgrade_max_cost = round(upgrade_max_cost)
        return

    if upgrade_min_button_rect.collidepoint(event.pos) and score >= upgrade_min_cost and min_dice_value < max_dice_value:
        min_dice_value += 1
        score -= upgrade_min_cost
        score = round(score)
        upgrade_min_cost = UPGRADE_COST_BASE_MINMAX * upgrade_min_cost
        upgrade_min_cost = round(upgrade_min_cost)
        return

    if upgrade_multi_button_rect.collidepoint(event.pos) and score >= upgrade_multi_cost:
        multi_value += 1
        score -= upgrade_multi_cost
        score = round(score)
        upgrade_multi_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_multi_cost
        upgrade_multi_cost = round(upgrade_multi_cost)
        return
    
    if upgrade_expo_button_rect.collidepoint(event.pos) and score >= upgrade_expo_cost:
        expo_value += 0.5
        expo_value = round(expo_value * 10) / 10
        score -= upgrade_expo_cost
        score = round(score)
        upgrade_expo_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_expo_cost
        upgrade_expo_cost = round(upgrade_expo_cost)
        return
    if Reset:
        if upgrade_anitime_button_rect.collidepoint(event.pos) and resettimes >= upgrade_anitime_cost:
            animation_duration = animation_duration/2
            resettimes -= upgrade_anitime_cost
            upgrade_anitime_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_anitime_cost
            return
        if unlock_Auto_button_rect.collidepoint(event.pos) and resettimes >= unlock_automation_cost and not(auto_click_enabled):
            auto_click_enabled = True
            resettimes = resettimes - unlock_automation_cost
            return
    

def pygame_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            Clicks(event)
def draw_All():
    global score, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_max_cost
    global upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, upgrade_anitime_cost
    # Draw buttons
    draw_button(button_rect, "Roll", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_button_rect, "Upgrade Max", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_min_button_rect, "Upgrade Min", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_multi_button_rect, "Upgrade Multi", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_expo_button_rect, "Upgrade Expo", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    if Reset:
        draw_button(upgrade_anitime_button_rect, "Upgrade Animation Time", BUTTON_HOVER_COLOR, BUTTON_COLOR)
        if auto_click_enabled:
            draw_button(unlock_Auto_button_rect, "Automation unlocked", BUTTON_UNLOCKED_HOVER_COLOR, BUTTON_UNLOCKED_COLOR)
        else:
            draw_button(unlock_Auto_button_rect, "Unlock Automation", BUTTON_HOVER_COLOR, BUTTON_COLOR)
        pass

    # Draw dice animation or final result
    roll_dice_animation()

    # Draw score
    draw_text(f"Score: {format_number_with_short_name(score)}", (20, 20))
    if Reset:
        draw_text(f"Resets Not Spent: {format_number_with_short_name(resettimes)}", (20, 70))

    # Draw upgrade info
    draw_text(f"Max: {format_number_with_short_name(max_dice_value)}", (Screen_width - 210, 0))
    draw_text(f"Cost: {format_number_with_short_name(upgrade_max_cost)}", (Screen_width - 210, 30))
    draw_text(f"Min: {format_number_with_short_name(min_dice_value)}", (Screen_width - 210, 115))
    draw_text(f"Cost: {format_number_with_short_name(upgrade_min_cost)}", (Screen_width - 210, 145))
    draw_text(f"Multi: {format_number_with_short_name(multi_value)}", (Screen_width - 210, 230))
    draw_text(f"Cost: {format_number_with_short_name(upgrade_multi_cost)}", (Screen_width - 210, 260))
    draw_text(f"Expo: {format_number_with_short_name(expo_value)}", (Screen_width - 210, 345))
    draw_text(f"Cost: {format_number_with_short_name(upgrade_expo_cost)}", (Screen_width - 210, 375))
    if Reset:
        draw_text(f"Current animation speed: {format_number_with_short_name(animation_duration)}s", (20, 120))
        draw_text(f"Cost: {format_number_with_short_name(upgrade_anitime_cost)} Reset{'s' if upgrade_anitime_cost != 1 else ''}", (20, 150))
        if not(auto_click_enabled):
            draw_text(f"Cost to unlock Automation: {format_number_with_short_name(unlock_automation_cost)}s", (20, 240))


# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)
    auto_click_interval = animation_duration

    #handels events
    pygame_events()
    auto_click()

    #draws everythoing
    draw_All()

    pygame.display.flip()
    clock.tick(FPS)
save_data(CURRENTVERSION, (score, result, rolling, animating, final_roll, animation_start_time,
                           animation_duration, max_dice_value, min_dice_value, multi_value,
                           expo_value, upgrade_max_cost, upgrade_min_cost, upgrade_multi_cost,
                           upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes, auto_click_enabled))

pygame.quit()
