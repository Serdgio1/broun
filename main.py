import pygame
import pygame_gui
import numpy as np

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Параметры экрана
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция частиц с температурой")

# Цвета
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
WHITE = (255,255,255)

# Fonts
font = pygame.font.Font(None, 36)  # Инициализация шрифта

# Параметры симуляции
NUM_PARTICLES = 150  # Количество частиц
PARTICLE_RADIUS = 7  # Радиус частицы
GRAVITY = 0.2  # Базовая гравитация
GRID_SPACING = 22  # Расстояние между частицами в сетке
VISCOSITY = 0.98  # Коэффициент вязкости
ELASTICITY = 0.9  # Коэффициент упругости (0.9 = небольшая потеря энергии)
temperature = -100  # Начальная температура (состояние)



# Load music file (замените "music.mp3" на ваш файл)
pygame.mixer.music.load("music/sb_indreams(chosic.com).mp3")  # Убедитесь, что файл находится в одной папке или укажите путь
pygame.mixer.music.set_volume(0.2)   # Установить громкость (0.0 до 1.0)

# Инициализация интерфейса
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, HEIGHT-150), (700, 30)),
    start_value=temperature,
    value_range=(-100, 150),
    manager=manager
)
slider2 = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, HEIGHT-85), (700, 30)),
    start_value=temperature+273,
    value_range=(173, 423),
    manager=manager
)

# Add labels to display slider values
label1 = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((100, HEIGHT-125), (600, 30)),
    text=f"Slider Celsius Value: {slider.get_current_value()}",
    manager=manager
)

label2 = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((100, HEIGHT-60), (600, 30)),
    text=f"Slider Kelvin Value: {slider2.get_current_value()}",
    manager=manager
)

# Load button image
button_repeat = pygame.image.load("images/Repeat-Right@2x.png")
button_repeat = pygame.transform.scale(button_repeat, (50, 50))  # Масштабирование кнопки
button_exit = pygame.image.load("images/img.png")
button_exit = pygame.transform.scale(button_exit, (50, 50))  # Масштабирование кнопки
button_music = pygame.image.load("images/Music-On@2x.png")
button_music = pygame.transform.scale(button_music, (50, 50))  # Масштабирование кнопки

# Button properties
button_rep = button_repeat.get_rect(topleft=(10, HEIGHT-170))  # Позиция кнопки
button_ex = button_exit.get_rect(topleft=(10, HEIGHT-100))  # Позиция кнопки
button_mus = button_music.get_rect(topleft=(WIDTH-70, HEIGHT-125))  # Позиция кнопки

# Функции

# Инициализация частиц в сетке
def init_particles():
    global positions, velocities, states

    # Создание массивов для частиц
    positions = np.random.rand(NUM_PARTICLES, 2) * [WIDTH, (HEIGHT - 200) // 2]  # Начальные координаты частиц
    velocities = (np.random.rand(NUM_PARTICLES, 2) - 0.5) * 2  # Скорости частиц
    states = np.array(["solid"] * NUM_PARTICLES)  # Состояния частиц

    x_start, y_start = 50, 50  # Начальная точка сетки
    index = 0
    for y in range(y_start, HEIGHT -300, GRID_SPACING):
        for x in range(x_start, WIDTH - x_start, GRID_SPACING):
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
            if dist < 2 * PARTICLE_RADIUS:  # Условие столкновения
                resolve_collision(i, j)

        # Обновляем движения частиц
        if temperature < 0:
            # Твёрдое состояние с градацией тряски
            velocities[i] *= 0.9  # Замедляем движение
            intensity = (100-abs(temperature)) / 100.0  # Интенсивность тряски (от 0 до 1)
            positions[i][0] += np.random.uniform(-intensity, intensity)
            positions[i][1] += np.random.uniform(-intensity, intensity)
        elif 0 <= temperature < 100:
            # Жидкое состояние
            velocities[i][1] += GRAVITY  # Гравитация
            velocities[i] *= VISCOSITY  # Применяем вязкость

            # Ограничиваем частицы в нижней части экрана
            if positions[i][1] >= HEIGHT-200 - PARTICLE_RADIUS:
                positions[i][1] = HEIGHT -200- PARTICLE_RADIUS
                velocities[i][1] = 0  # Останавливаем падение

            positions[i] += velocities[i]

            # Движение у дна
            if positions[i][1] >= HEIGHT-200 - PARTICLE_RADIUS - 10:
                velocities[i][0] += (np.random.rand() - 0.5) * temperature/20  # Хаотичное движение влево-вправо
        else:
            # Газообразное состояние
            velocities[i][1] -= 3*GRAVITY  # Гравитация
            velocities[i] += (np.random.rand(2) - 0.5) * temperature/20  # Хаотичное движение
            positions[i] += velocities[i]

        # Ограничиваем движение частиц внутри экрана
        if positions[i][0] <= PARTICLE_RADIUS or positions[i][0] >= WIDTH - PARTICLE_RADIUS:
            velocities[i][0] *= -ELASTICITY
        if positions[i][1] <= PARTICLE_RADIUS:
            velocities[i][1] *= -ELASTICITY

        positions[i][0] = np.clip(positions[i][0], PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        positions[i][1] = np.clip(positions[i][1], PARTICLE_RADIUS, HEIGHT-200 - PARTICLE_RADIUS)

def resolve_collision(i, j):
    # Вектор между частицами
    delta = positions[i] - positions[j]
    distance = np.linalg.norm(delta)
    if distance == 0:  # Предотвращение деления на 0
        distance = 0.01
    normal = delta / distance

    # Разделяем частицы
    overlap = 2 * PARTICLE_RADIUS - distance
    positions[i] += normal * (overlap / 2)
    positions[j] -= normal * (overlap / 2)

    # Пересчёт скоростей после столкновения
    relative_velocity = velocities[i] - velocities[j]
    velocity_along_normal = np.dot(relative_velocity, normal)
    if velocity_along_normal > 0:  # Частицы расходятся, не нужно обрабатывать
        return

    impulse = -(1 + ELASTICITY) * velocity_along_normal
    impulse_vector = impulse * normal
    velocities[i] += impulse_vector / 2
    velocities[j] -= impulse_vector / 2

def draw_particles():
    for pos in positions:
        pygame.draw.circle(screen, BLUE, (int(pos[0]), int(pos[1])), PARTICLE_RADIUS)

def scene_settings():
    """Первая сцена: Настройка симуляции"""
    global NUM_PARTICLES, PARTICLE_RADIUS, GRID_SPACING
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Элементы интерфейса
    num_particles_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 300), (200, 30)),
        manager=manager
    )
    num_particles_input.set_text(str(NUM_PARTICLES))

    particle_radius_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 350), (200, 30)),
        manager=manager
    )
    particle_radius_input.set_text(str(PARTICLE_RADIUS))



    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 400), (200, 50)),
        text="Начать симуляцию",
        manager=manager
    )

    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        # Заголовок
        title = font.render("Настройка симуляции", True, WHITE)
        screen.blit(title, (300, 150))

        # Подписи
        screen.blit(font.render("Количество частиц:", True, WHITE), (100, 300))
        screen.blit(font.render("Радиус частиц:", True, WHITE), (150, 350))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Выход из приложения

            manager.process_events(event)

            # Переход к симуляции
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    try:
                        NUM_PARTICLES = int(num_particles_input.get_text())
                        PARTICLE_RADIUS = int(particle_radius_input.get_text())
                        GRID_SPACING = PARTICLE_RADIUS+15
                    except ValueError:
                        print("Введите корректные числа!")
                        continue
                    return True  # Переход к симуляции

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

# Основной цикл
running = True
clock = pygame.time.Clock()
f_music = False
scene_settings()
init_particles()

while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(BLACK)

    rect_x, rect_y = 0, HEIGHT-199  # Position of the rectangle
    rect_width, rect_height = WIDTH, 5  # Dimensions of the rectangle
    pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw button image
    screen.blit(button_repeat, button_rep.topleft)
    screen.blit(button_exit, button_ex.topleft)
    screen.blit(button_music, button_mus.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

        # Synchronize slider values with offset
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  # Updated to new API
            if event.ui_element == slider:
                slider2.set_current_value(slider.get_current_value() + 273)
            elif event.ui_element == slider2:
                slider.set_current_value(slider2.get_current_value() - 273)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                init_particles()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rep.collidepoint(event.pos):
                init_particles()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_ex.collidepoint(event.pos):
                running=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_mus.collidepoint(event.pos):
                f_music = not(f_music)
                if f_music:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            # Update labels
    label1.set_text(f"Slider Celsius Value: {slider.get_current_value():.2f}")
    label2.set_text(f"Slider Kelvin Value: {slider2.get_current_value():.2f}")
    # Обновляем значение температуры из слайдера
    temperature = slider.get_current_value()
    # Обновление частиц и интерфейса
    update_particles()
    draw_particles()
    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()



pygame.quit()
