import pygame
import random
import time
import pickle


# Initialize Pygame
pygame.init()

# Constants
CURRENTVERSION = "beta0.1"
Screen_width, Screen_height = 0, 0
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 180, 240)
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
upgrade_cost = 10
upgrade_min_cost = 10
upgrade_multi_cost = 1000
upgrade_expo_cost = 100000
upgrade_anitime_cost = 1
Reset = False
resettimes = 0

# Helper functions
def format_number_with_apostrophes(number):
    """
    Format an integer into a string with apostrophes as thousands separators.

    Args:
        number (int): The integer to format.

    Returns:
        str: The formatted string with apostrophes as separators.
    """
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

#load data if possible
if load_data() != None:
    Saveversion,(score, result, rolling, animating, final_roll, animation_start_time, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes) = load_data()
    


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
    global final_roll, rolling, score, animating, result, animation_start_time, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, Reset, resettimes

    if not rolling:
        if final_roll != None :
            if expo_value > 1:
                draw_text(f"({final_roll} x {multi_value}) ^ {expo_value} = {format_number_with_apostrophes(result)}", dice_pos, center=True)
            elif multi_value > 1:
                draw_text(f"{final_roll} x {multi_value} = {format_number_with_apostrophes(result)}", dice_pos, center=True)
            else:
                draw_text(f"{format_number_with_apostrophes(final_roll)}", dice_pos, center=True)
            return
        else:
            return


    current_time = time.time()
    if current_time - animation_start_time < animation_duration:
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
            upgrade_cost = 10
            upgrade_min_cost = 10
            upgrade_multi_cost = 1000
            upgrade_expo_cost = 100000

def pygame_events():
    global score, result, rolling, animating, final_roll, animation_start_time, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, upgrade_anitime_cost, running, resettimes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not rolling:
                rolling = True
                animation_start_time = time.time()

            if upgrade_button_rect.collidepoint(event.pos) and score >= upgrade_cost:
                max_dice_value += 1
                score -= upgrade_cost
                score = round(score)
                upgrade_cost = UPGRADE_COST_BASE_MINMAX * upgrade_cost
                upgrade_cost = round(upgrade_cost)

            if upgrade_min_button_rect.collidepoint(event.pos) and score >= upgrade_min_cost and min_dice_value < max_dice_value:
                min_dice_value += 1
                score -= upgrade_min_cost
                score = round(score)
                upgrade_min_cost = UPGRADE_COST_BASE_MINMAX * upgrade_min_cost
                upgrade_min_cost = round(upgrade_min_cost)

            if upgrade_multi_button_rect.collidepoint(event.pos) and score >= upgrade_multi_cost:
                multi_value += 1
                score -= upgrade_multi_cost
                score = round(score)
                upgrade_multi_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_multi_cost
                upgrade_multi_cost = round(upgrade_multi_cost)
            
            if upgrade_expo_button_rect.collidepoint(event.pos) and score >= upgrade_expo_cost:
                expo_value += 0.5
                expo_value = round(expo_value * 10) / 10
                score -= upgrade_expo_cost
                score = round(score)
                upgrade_expo_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_expo_cost
                upgrade_expo_cost = round(upgrade_expo_cost)
            if Reset:
                if upgrade_anitime_button_rect.collidepoint(event.pos) and resettimes >= upgrade_anitime_cost:
                    animation_duration = animation_duration/2
                    resettimes -= upgrade_anitime_cost
                    upgrade_anitime_cost = UPGRADE_COST_BASE_MULTIEXPO * upgrade_anitime_cost

def draw_All():
    global score, result, rolling, animating, final_roll, animation_start_time, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, upgrade_anitime_cost
    # Draw buttons
    draw_button(button_rect, "Roll", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_button_rect, "Upgrade Max", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_min_button_rect, "Upgrade Min", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_multi_button_rect, "Upgrade Multi", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    draw_button(upgrade_expo_button_rect, "Upgrade Expo", BUTTON_HOVER_COLOR, BUTTON_COLOR)
    if Reset:
        draw_button(upgrade_anitime_button_rect, "Upgrade Animation Time", BUTTON_HOVER_COLOR, BUTTON_COLOR)
        pass

    # Draw dice animation or final result
    roll_dice_animation()

    # Draw score
    draw_text(f"Score: {format_number_with_apostrophes(score)}", (20, 20))
    if Reset:
        draw_text(f"Resets Not Spent: {format_number_with_apostrophes(resettimes)}", (20, 70))

    # Draw upgrade info
    draw_text(f"Max: {format_number_with_apostrophes(max_dice_value)}", (Screen_width - 210, 0))
    draw_text(f"Cost: {format_number_with_apostrophes(upgrade_cost)}", (Screen_width - 210, 30))
    draw_text(f"Min: {format_number_with_apostrophes(min_dice_value)}", (Screen_width - 210, 115))
    draw_text(f"Cost: {format_number_with_apostrophes(upgrade_min_cost)}", (Screen_width - 210, 145))
    draw_text(f"Multi: {format_number_with_apostrophes(multi_value)}", (Screen_width - 210, 230))
    draw_text(f"Cost: {format_number_with_apostrophes(upgrade_multi_cost)}", (Screen_width - 210, 260))
    draw_text(f"Expo: {format_number_with_apostrophes(expo_value)}", (Screen_width - 210, 345))
    draw_text(f"Cost: {format_number_with_apostrophes(upgrade_expo_cost)}", (Screen_width - 210, 375))
    if Reset:
        draw_text(f"Current animation speed: {format_number_with_apostrophes(animation_duration)}s", (20, 120))
        draw_text(f"Cost: {format_number_with_apostrophes(upgrade_anitime_cost)} Reset{'s' if upgrade_anitime_cost != 1 else ''}", (20, 150))


# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)

    #handels events
    pygame_events()

    #draws everythoing
    draw_All()

    pygame.display.flip()
    clock.tick(FPS)
save_data(CURRENTVERSION, (score, result, rolling, animating, final_roll, animation_start_time, animation_duration, max_dice_value, min_dice_value, multi_value, expo_value, upgrade_cost, upgrade_min_cost, upgrade_multi_cost, upgrade_expo_cost, upgrade_anitime_cost, Reset, resettimes))

pygame.quit()
