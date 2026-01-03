import pygame
import pygame_gui
import numpy as np

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Physics Simulation - Temperature States")

DARK_BG = (18, 18, 28)
PANEL_BG = (30, 30, 45)
PANEL_BORDER = (60, 60, 80)
ACCENT_BLUE = (100, 150, 255)
ACCENT_CYAN = (100, 255, 255)
ACCENT_ORANGE = (255, 150, 100)
ACCENT_RED = (255, 100, 100)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

SOLID_COLOR = (100, 150, 255)
LIQUID_COLOR = (100, 255, 255)
GAS_COLOR = (255, 150, 100)

font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

NUM_PARTICLES = 150
PARTICLE_RADIUS = 7
GRAVITY = 0.2
GRID_SPACING = 22
VISCOSITY = 0.98
ELASTICITY = 0.9
temperature = -100
CONTROL_PANEL_WIDTH = 320
SIMULATION_AREA_WIDTH = WIDTH - CONTROL_PANEL_WIDTH

try:
    pygame.mixer.music.load("music/sb_indreams(chosic.com).mp3")
    pygame.mixer.music.set_volume(0.2)
    music_available = True
except:
    music_available = False

manager = pygame_gui.UIManager((WIDTH, HEIGHT), theme_path=None)

theme = {
    "#panel": {
        "background_color": PANEL_BG,
        "border_width": 2,
        "border_color": PANEL_BORDER
    },
    "#title": {
        "font": {"size": 28, "style": "bold"},
        "text_color": WHITE
    },
    "#slider_label": {
        "font": {"size": 18},
        "text_color": LIGHT_GRAY
    },
    "#value_label": {
        "font": {"size": 20, "style": "bold"},
        "text_color": ACCENT_BLUE
    },
    "#state_label": {
        "font": {"size": 22, "style": "bold"},
        "text_color": ACCENT_CYAN
    },
    "#button": {
        "font": {"size": 18},
        "text_color": WHITE,
        "background_color": ACCENT_BLUE,
        "hovered_background_color": (120, 170, 255),
        "pressed_background_color": (80, 130, 235)
    },
    "#info_box": {
        "font": {"size": 14},
        "text_color": LIGHT_GRAY,
        "background_color": (25, 25, 35),
        "border_width": 1,
        "border_color": PANEL_BORDER
    }
}


def get_particle_color(temp):
    if temp < 0:
        return SOLID_COLOR
    elif 0 <= temp < 100:
        return LIQUID_COLOR
    else:
        return GAS_COLOR


def get_state_name(temp):
    if temp < 0:
        return "Твёрдое"
    elif 0 <= temp < 100:
        return "Жидкое"
    else:
        return "Газообразное"


def build_main_ui():
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((SIMULATION_AREA_WIDTH, 0), (CONTROL_PANEL_WIDTH, HEIGHT)),
        starting_height=1,
        manager=manager,
        object_id="#panel"
    )

    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 15), (CONTROL_PANEL_WIDTH - 30, 40)),
        text="⚙️ Управление",
        manager=manager,
        container=panel,
        object_id="#title"
    )

    temp_section_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 80), (CONTROL_PANEL_WIDTH - 30, 25)),
        text="🌡️ Температура",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )

    celsius_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 110), (CONTROL_PANEL_WIDTH - 30, 22)),
        text="°C (Цельсий)",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )
    
    celsius_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((15, 135), (CONTROL_PANEL_WIDTH - 30, 25)),
        start_value=temperature,
        value_range=(-100, 150),
        manager=manager,
        container=panel
    )
    
    celsius_value = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 165), (CONTROL_PANEL_WIDTH - 30, 28)),
        text=f"{temperature:.1f} °C",
        manager=manager,
        container=panel,
        object_id="#value_label"
    )

    kelvin_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 200), (CONTROL_PANEL_WIDTH - 30, 22)),
        text="K (Кельвин)",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )
    
    kelvin_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((15, 225), (CONTROL_PANEL_WIDTH - 30, 25)),
        start_value=temperature + 273,
        value_range=(173, 423),
        manager=manager,
        container=panel
    )
    
    kelvin_value = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 255), (CONTROL_PANEL_WIDTH - 30, 28)),
        text=f"{temperature + 273:.1f} K",
        manager=manager,
        container=panel,
        object_id="#value_label"
    )

    state_section_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 310), (CONTROL_PANEL_WIDTH - 30, 25)),
        text="📊 Статистика",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )

    state_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 340), (CONTROL_PANEL_WIDTH - 30, 30)),
        text=f"Состояние: {get_state_name(temperature)}",
        manager=manager,
        container=panel,
        object_id="#state_label"
    )
    
    fps_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 375), (CONTROL_PANEL_WIDTH - 30, 25)),
        text="FPS: 60",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )

    particle_count_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 400), (CONTROL_PANEL_WIDTH - 30, 25)),
        text=f"Частиц: {NUM_PARTICLES}",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )

    controls_section_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((15, 450), (CONTROL_PANEL_WIDTH - 30, 25)),
        text="🎮 Управление",
        manager=manager,
        container=panel,
        object_id="#slider_label"
    )

    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, 480), (CONTROL_PANEL_WIDTH - 30, 45)),
        text="🔄 Перезапустить (R)",
        manager=manager,
        container=panel,
        object_id="#button"
    )
    
    music_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, 535), (CONTROL_PANEL_WIDTH - 30, 45)),
        text="🎵 Музыка: выкл",
        manager=manager,
        container=panel,
        object_id="#button"
    )
    
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((15, 590), (CONTROL_PANEL_WIDTH - 30, 45)),
        text="❌ Выход",
        manager=manager,
        container=panel,
        object_id="#button"
    )

    info_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((15, 650), (CONTROL_PANEL_WIDTH - 30, 220)),
        html_text=(
            "<b>💡 Подсказки</b><br><br>"
            "• <b>Слайдеры</b> — изменение температуры<br>"
            "• <b>R</b> — перезапуск частиц<br>"
            "• <b>Цвета частиц:</b><br>"
            "  🔵 Синий = Твёрдое<br>"
            "  🔷 Голубой = Жидкое<br>"
            "  🔶 Оранжевый = Газ"
        ),
        manager=manager,
        container=panel,
        object_id="#info_box"
    )

    return {
        "panel": panel,
        "celsius_slider": celsius_slider,
        "celsius_value": celsius_value,
        "kelvin_slider": kelvin_slider,
        "kelvin_value": kelvin_value,
        "state_label": state_label,
        "fps_label": fps_label,
        "reset_button": reset_button,
        "music_button": music_button,
        "quit_button": quit_button,
        "particle_count_label": particle_count_label
    }


def init_particles():
    global positions, velocities, states

    positions = np.random.rand(NUM_PARTICLES, 2) * [SIMULATION_AREA_WIDTH - 100, (HEIGHT - 200) // 2]
    velocities = (np.random.rand(NUM_PARTICLES, 2) - 0.5) * 2
    states = np.array(["solid"] * NUM_PARTICLES)

    x_start, y_start = 50, 50
    index = 0
    for y in range(y_start, HEIGHT - 300, GRID_SPACING):
        for x in range(x_start, SIMULATION_AREA_WIDTH - x_start, GRID_SPACING):
            if index >= NUM_PARTICLES:
                break
            positions[index] = [x, y]
            velocities[index] = [0, 0]
            index += 1


def update_particles():
    global velocities, positions, states

    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < 2 * PARTICLE_RADIUS:
                resolve_collision(i, j)

        if temperature < 0:
            velocities[i] *= 0.9
            intensity = (100 - abs(temperature)) / 100.0
            positions[i][0] += np.random.uniform(-intensity, intensity)
            positions[i][1] += np.random.uniform(-intensity, intensity)
        elif 0 <= temperature < 100:
            velocities[i][1] += GRAVITY
            velocities[i] *= VISCOSITY

            if positions[i][1] >= HEIGHT - 200 - PARTICLE_RADIUS:
                positions[i][1] = HEIGHT - 200 - PARTICLE_RADIUS
                velocities[i][1] = 0

            positions[i] += velocities[i]

            if positions[i][1] >= HEIGHT - 200 - PARTICLE_RADIUS - 10:
                velocities[i][0] += (np.random.rand() - 0.5) * temperature / 20
        else:
            velocities[i][1] -= 3 * GRAVITY
            velocities[i] += (np.random.rand(2) - 0.5) * temperature / 20
            positions[i] += velocities[i]

        if positions[i][0] <= PARTICLE_RADIUS or positions[i][0] >= SIMULATION_AREA_WIDTH - PARTICLE_RADIUS:
            velocities[i][0] *= -ELASTICITY
        if positions[i][1] <= PARTICLE_RADIUS:
            velocities[i][1] *= -ELASTICITY

        positions[i][0] = np.clip(positions[i][0], PARTICLE_RADIUS, SIMULATION_AREA_WIDTH - PARTICLE_RADIUS)
        positions[i][1] = np.clip(positions[i][1], PARTICLE_RADIUS, HEIGHT - 200 - PARTICLE_RADIUS)


def resolve_collision(i, j):
    delta = positions[i] - positions[j]
    distance = np.linalg.norm(delta)
    if distance == 0:
        distance = 0.01
    normal = delta / distance

    overlap = 2 * PARTICLE_RADIUS - distance
    positions[i] += normal * (overlap / 2)
    positions[j] -= normal * (overlap / 2)

    relative_velocity = velocities[i] - velocities[j]
    velocity_along_normal = np.dot(relative_velocity, normal)
    if velocity_along_normal > 0:
        return

    impulse = -(1 + ELASTICITY) * velocity_along_normal
    impulse_vector = impulse * normal
    velocities[i] += impulse_vector / 2
    velocities[j] -= impulse_vector / 2


def draw_particles():
    particle_color = get_particle_color(temperature)
    
    for pos in positions:
        x, y = int(pos[0]), int(pos[1])
        
        glow_color = tuple(max(0, c - 30) for c in particle_color)
        pygame.draw.circle(screen, glow_color, (x, y), PARTICLE_RADIUS + 1)
        
        pygame.draw.circle(screen, particle_color, (x, y), PARTICLE_RADIUS)
        
        highlight_color = tuple(min(255, c + 50) for c in particle_color)
        pygame.draw.circle(screen, highlight_color, (x, y), max(2, PARTICLE_RADIUS - 3))


def draw_simulation_area():
    for y in range(0, HEIGHT - 200, 10):
        intensity = int(18 + (y / (HEIGHT - 200)) * 10)
        color = (intensity, intensity, min(40, intensity + 5))
        pygame.draw.rect(screen, color, (0, y, SIMULATION_AREA_WIDTH, 10))
    
    floor_y = HEIGHT - 200
    pygame.draw.line(screen, (100, 100, 100), (0, floor_y + 1), (SIMULATION_AREA_WIDTH, floor_y + 1), 2)
    pygame.draw.line(screen, WHITE, (0, floor_y), (SIMULATION_AREA_WIDTH, floor_y), 2)
    
    pygame.draw.line(screen, PANEL_BORDER, (SIMULATION_AREA_WIDTH, 0), (SIMULATION_AREA_WIDTH, HEIGHT), 3)


def draw_ui_separators():
    x = SIMULATION_AREA_WIDTH + 15
    width = CONTROL_PANEL_WIDTH - 30
    pygame.draw.line(screen, PANEL_BORDER, (x, 65), (x + width, 65), 2)
    pygame.draw.line(screen, PANEL_BORDER, (x, 295), (x + width, 295), 2)
    pygame.draw.line(screen, PANEL_BORDER, (x, 435), (x + width, 435), 2)


def scene_settings():
    global NUM_PARTICLES, PARTICLE_RADIUS, GRID_SPACING
    settings_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    settings_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((WIDTH // 2 - 250, HEIGHT // 2 - 200), (500, 400)),
        starting_height=1,
        manager=settings_manager
    )

    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 20), (460, 50)),
        text="⚙️ Настройка симуляции",
        manager=settings_manager,
        container=settings_panel
    )

    num_particles_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 90), (200, 30)),
        text="Количество частиц:",
        manager=settings_manager,
        container=settings_panel
    )

    num_particles_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((230, 90), (250, 35)),
        manager=settings_manager,
        container=settings_panel
    )
    num_particles_input.set_text(str(NUM_PARTICLES))

    particle_radius_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 140), (200, 30)),
        text="Радиус частиц:",
        manager=settings_manager,
        container=settings_panel
    )

    particle_radius_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((230, 140), (250, 35)),
        manager=settings_manager,
        container=settings_panel
    )
    particle_radius_input.set_text(str(PARTICLE_RADIUS))

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((150, 250), (200, 50)),
        text="🚀 Начать симуляцию",
        manager=settings_manager,
        container=settings_panel
    )

    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill(DARK_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            settings_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    try:
                        NUM_PARTICLES = int(num_particles_input.get_text())
                        PARTICLE_RADIUS = int(particle_radius_input.get_text())
                        GRID_SPACING = PARTICLE_RADIUS + 15
                        if NUM_PARTICLES < 1 or NUM_PARTICLES > 500:
                            raise ValueError("Количество частиц должно быть от 1 до 500")
                        if PARTICLE_RADIUS < 3 or PARTICLE_RADIUS > 20:
                            raise ValueError("Радиус должен быть от 3 до 20")
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                        continue
                    return True

        settings_manager.update(time_delta)
        settings_manager.draw_ui(screen)
        pygame.display.flip()


running = True
clock = pygame.time.Clock()
f_music = False

if scene_settings():
    init_particles()
    ui_elements = build_main_ui()
    
    while running:
        time_delta = clock.tick(60) / 1000.0
        fps = clock.get_fps()
        
        screen.fill(DARK_BG)
        
        draw_simulation_area()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            manager.process_events(event)

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == ui_elements["celsius_slider"]:
                    new_temp = ui_elements["celsius_slider"].get_current_value()
                    ui_elements["kelvin_slider"].set_current_value(new_temp + 273)
                    temperature = new_temp
                elif event.ui_element == ui_elements["kelvin_slider"]:
                    new_temp = ui_elements["kelvin_slider"].get_current_value() - 273
                    ui_elements["celsius_slider"].set_current_value(new_temp)
                    temperature = new_temp

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui_elements["reset_button"]:
                    init_particles()
                elif event.ui_element == ui_elements["music_button"]:
                    f_music = not f_music
                    if f_music and music_available:
                        pygame.mixer.music.play(-1)
                        ui_elements["music_button"].set_text("🎵 Музыка: вкл")
                    else:
                        pygame.mixer.music.stop()
                        ui_elements["music_button"].set_text("🎵 Музыка: выкл")
                elif event.ui_element == ui_elements["quit_button"]:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_particles()

        ui_elements["celsius_value"].set_text(f"{temperature:.1f} °C")
        ui_elements["kelvin_value"].set_text(f"{temperature + 273:.1f} K")
        ui_elements["state_label"].set_text(f"Состояние: {get_state_name(temperature)}")
        ui_elements["fps_label"].set_text(f"FPS: {int(fps)}")

        update_particles()
        
        draw_particles()
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        
        draw_ui_separators()

        pygame.display.flip()

pygame.quit()
