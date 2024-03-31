import pygame
import random

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Parámetros de la simulación (valores iniciales)
population_size = 300
initial_infected = 5
exposure_rate = 0.03
infection_rate = 0.1
recovery_rate = 0.05
mortality_rate = 0.01

# Inicialización de Pygame
pygame.init()

# Tamaño de la pantalla
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulación de Pandemia MSEIR")

clock = pygame.time.Clock()


class Person:
    def __init__(self, x, y, status="S"):
        """
        Constructor de la clase Person.

        Args:
            x (int): Posición horizontal.
            y (int): Posición vertical.
            status (str): Estado inicial de la persona (por defecto: "S" - Susceptible).
        """
        self.x = x
        self.y = y
        self.status = status
        self.days_infected = 0

    def draw(self):
        """Dibuja a la persona en la pantalla según su estado."""
        if self.status == "S":
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 5)
        elif self.status == "E":
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 5)
        elif self.status == "I":
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)
        elif self.status == "R":
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)

    def move(self):
        """Mueve a la persona en una dirección aleatoria."""
        self.x += random.uniform(-1, 1)
        self.y += random.uniform(-1, 1)

    def infect(self):
        """Infecta a la persona si está expuesta."""
        if self.status == "S" and random.random() < exposure_rate:
            self.status = "E"

    def check_infection(self):
        """Comprueba si la persona expuesta se convierte en infectada."""
        if self.status == "E":
            self.days_infected += 1
            if self.days_infected >= 3 and random.random() < infection_rate:
                self.status = "I"

    def check_recovery(self):
        """Comprueba si la persona infectada se recupera o fallece."""
        if self.status == "I" and random.random() < recovery_rate:
            if random.random() < mortality_rate:
                self.status = "D"
            else:
                self.status = "R"


# Lista de personas
population = []
for _ in range(population_size):
    x = random.randint(0, width)
    y = random.randint(0, height)
    population.append(Person(x, y))

# Infectar a un número inicial de personas
for _ in range(initial_infected):
    population[_].status = "I"

# Función para crear botones
def draw_button(x, y, width, height, text, action):
    """
    Dibuja un botón en la pantalla y maneja su interacción.

    Args:
        x (int): Posición horizontal del botón.
        y (int): Posición vertical del botón.
        width (int): Ancho del botón.
        height (int): Altura del botón.
        text (str): Texto que se muestra en el botón.
        action (function): Función a ejecutar cuando se hace clic en el botón.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, GREEN, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BLUE, (x, y, width, height))

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf, text_rect = text_objects(text, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

# Función para mostrar texto en botones
def text_objects(text, font):
    """
    Crea una superficie de texto para mostrar en un botón.

    Args:
        text (str): Texto a mostrar.
        font (pygame.font.Font): Fuente del texto.

    Returns:
        pygame.Surface, pygame.Rect: Superficie de texto y rectángulo que la contiene.
    """
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

# Función para aumentar la población
def increase_population():
    """Aumenta el tamaño de la población y reinicia la simulación."""
    global population_size
    population_size += 50
    reset_simulation()

# Función para disminuir la población
def decrease_population():
    """Disminuye el tamaño de la población y reinicia la simulación."""
    global population_size
    if population_size > 50:
        population_size -= 50
        reset_simulation()

# Función para reiniciar la simulación con la nueva población
def reset_simulation():
    """Reinicia la simulación con los nuevos parámetros."""
    global population
    population = []
    for _ in range(population_size):
        x = random.randint(0, width)
        y = random.randint(0, height)
        population.append(Person(x, y))
    # Infectar a un número inicial de personas
    for _ in range(initial_infected):
        population[_].status = "I"

# Función principal
def main():
    """Función principal del programa."""
    running = True
    while running:
        screen.fill(WHITE)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar y mover personas
        for person in population:
            person.move()
            person.infect()
            person.check_infection()
            person.check_recovery()
            person.draw()

        # Dibujar botones
        draw_button(20, 20, 150, 50, "+ Individuos", increase_population)
        draw_button(830, 20, 150, 50, "- Individuos", decrease_population)

        # Función para aumentar el número inicial de infectados
        def increase_initial_infected():
            global initial_infected
            initial_infected += 1
            reset_simulation()

        # Función para disminuir el número inicial de infectados
        def decrease_initial_infected():
            global initial_infected
            if initial_infected > 1:
                initial_infected -= 1
                reset_simulation()

        # Dibujar botones para el número inicial de infectados
        draw_button(200, 20, 200, 50, "+ Infectados", increase_initial_infected)
        draw_button(630, 20, 200, 50, "- Infectados", decrease_initial_infected)

        # Función para aumentar la tasa de exposición
        def increase_exposure_rate():
            global exposure_rate
            exposure_rate += 0.01
            reset_simulation()

        # Función para disminuir la tasa de exposición
        def decrease_exposure_rate():
            global exposure_rate
            if exposure_rate > 0.01:
                exposure_rate -= 0.01
                reset_simulation()

        # Dibujar botones para la tasa de exposición
        draw_button(20, 90, 200, 50, "+ Tasa de Exposición", increase_exposure_rate)
        draw_button(830, 90, 200, 50, "- Tasa de Exposición", decrease_exposure_rate)

        # Función para aumentar la tasa de infección
        def increase_infection_rate():
            global infection_rate
            infection_rate += 0.01
            reset_simulation()

        # Función para disminuir la tasa de infección
        def decrease_infection_rate():
            global infection_rate
            if infection_rate > 0.01:
                infection_rate -= 0.01
                reset_simulation()

        # Dibujar botones para la tasa de infección
        draw_button(20, 160, 200, 50, "+ Tasa de Infección", increase_infection_rate)
        draw_button(830, 160, 200, 50, "- Tasa de Infección", decrease_infection_rate)

        # Función para aumentar la tasa de recuperación
        def increase_recovery_rate():
            global recovery_rate
            recovery_rate += 0.01
            reset_simulation()

        # Función para disminuir la tasa de recuperación
        def decrease_recovery_rate():
            global recovery_rate
            if recovery_rate > 0.01:
                recovery_rate -= 0.01
                reset_simulation()

        # Dibujar botones para la tasa de recuperación
        draw_button(20, 230, 200, 50, "+ Tasa de Recuperación", increase_recovery_rate)
        draw_button(830, 230, 200, 50, "- Tasa de Recuperación", decrease_recovery_rate)

        # Función para aumentar la tasa de mortalidad
        def increase_mortality_rate():
            global mortality_rate
            mortality_rate += 0.01
            reset_simulation()

        # Función para disminuir la tasa de mortalidad
        def decrease_mortality_rate():
            global mortality_rate
            if mortality_rate > 0.01:
                mortality_rate -= 0.01
                reset_simulation()

        # Dibujar botones para la tasa de mortalidad
        draw_button(20, 300, 200, 50, "+ Tasa de Mortalidad", increase_mortality_rate)
        draw_button(830, 300, 200, 50, "- Tasa de Mortalidad", decrease_mortality_rate)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
