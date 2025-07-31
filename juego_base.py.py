import pygame
import random
import sys

pygame.init()  # Inicializa todos los módulos de pygame necesarios (pantalla, sonido, etc.)

# Configuración de pantalla
ANCHO = 600                  # Ancho de la ventana del juego en píxeles
ALTO = 400                   # Alto de la ventana del juego en píxeles
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego con las dimensiones dadas
pygame.display.set_caption("Juego Mejorado - pygame")  # Título que aparecerá en la ventana

# Definición de colores en tuplas
BLANCO = (255, 255, 255)  
AZUL = (0, 0, 255)        
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
VERDE = (0, 200, 0)

# Definición del jugador y enemigo 
# Crea un rectángulo para representar al jugador en la pantalla
jugador = pygame.Rect(50, 150, 50, 50)  # (x, y, ancho, alto)
color_jugador = AZUL                    # Color inicial del jugador (azul)
velocidad_jugador = 5                   # Velocidad con la que se mueve el jugador (pixeles por frame)

# Crea un rectángulo para el enemigo que aparece inicialmente en el borde derecho
enemigo = pygame.Rect(ANCHO, random.randint(0, ALTO - 50), 50, 50)  # Comienza en el borde derecho (x = ANCHO) y en una posición aleatoria en el eje Y.
velocidad_enemigo = 3  # Velocidad a la que el enemigo se mueve hacia la izquierda

# Configuración para mostrar texto y manejar la puntuación
fuente = pygame.font.SysFont(None, 36)  # Fuente para mostrar texto (sin fuente específica, tamaño 36)
puntos = 0                             # Inicializa la puntuación en cero
inicio_ticks = pygame.time.get_ticks()  # Marca el tiempo en milisegundos al iniciar el juego (para contar el tiempo transcurrido)

#  Control del reloj y sonidos 
reloj = pygame.time.Clock()  # Reloj para controlar la velocidad del juego (frames por segundo)
# Carga sonidos para puntos y colisiones
sonido_punto = pygame.mixer.Sound(pygame.mixer.Sound('punto.wav'))
sonido_colision = pygame.mixer.Sound(pygame.mixer.Sound('colision.wav'))

# Función para mostrar un menú de inicio
def mostrar_menu():
    pantalla.fill(BLANCO)  # Limpia la pantalla con color blanco
    titulo = fuente.render("Presiona ESPACIO para comenzar", True, NEGRO)  # Texto que aparece en el menú
    # Dibuja el texto centrado horizontalmente y cerca del centro vertical
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 20))
    pygame.display.update()  # Actualiza la pantalla para que se vea el menú

    esperando = True
    # Espera hasta que el jugador presione la tecla espacio para comenzar el juego
    while esperando:
        for evento in pygame.event.get(): #Recoge todos los evventos generados por usuario,
            if evento.type == pygame.QUIT:  # verifica Si se cierra la ventana, termina el juego
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE: #si se preciosabarra espaciadora
                esperando = False  # se rompre el bucle de while y comienza el juego

# Mostrar menú antes de iniciar el juego 
mostrar_menu()

# Bucle principal del juego
while True:
    # Manejo de eventos (teclado, cerrar ventana, etc.)
    for evento in pygame.event.get(): #revisa los eventos que ocurren en la ventana del juego
        if evento.type == pygame.QUIT:  # Si se presiona X cierra la ventana, termina el juego
            pygame.quit()
            sys.exit() #se detiene el programa

    # Movimiento del jugador basado en teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and jugador.top > 0:
        jugador.move_ip(0, -velocidad_jugador)  # Mover hacia arriba si no está en el borde superior
    if teclas[pygame.K_DOWN] and jugador.bottom < ALTO:
        jugador.move_ip(0, velocidad_jugador)   # Mover hacia abajo si no está en el borde inferior
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.move_ip(-velocidad_jugador, 0)  # Mover hacia la izquierda si no está en el borde izquierdo
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.move_ip(velocidad_jugador, 0)   # Mover hacia la derecha si no está en el borde derecho

    # Movimiento del enemigo
    enemigo.move_ip(-velocidad_enemigo, 0)  # Mover enemigo hacia la izquierda
    # Cuando el enemigo sale completamente por la izquierda, lo reposiciona a la derecha en una posición y aleatoria en Y
    if enemigo.right < 0:
        enemigo.left = ANCHO  # Se mueve al borde derecho (fuera de pantalla)
        enemigo.top = random.randint(0, ALTO - 50)  # Se posiciona en una posición vertical aleatoria
        puntos += 1  # Incrementa puntos por haber evitado al enemigo
        sonido_punto.play()  # Reproduce sonido de punto

    # Detectar colisión 
    if jugador.colliderect(enemigo):  # Si el jugador colisiona con el del enemigo
        color_jugador = ROJO  # Cambia color del jugador a rojo para indicar daño
        sonido_colision.play()  # Reproduce sonido de colisión
        print("¡Colisión! Puntos totales:", puntos)  # Muestra en consola la puntuación final
        pygame.time.delay(2000)  # Pausa 2 segundos para que el jugador vea el cambio y sonido
        pygame.quit()  # Cierra pygame
        sys.exit()     # Termina el programa

    # Calcular tiempo transcurrido en segundos 
    segundos = (pygame.time.get_ticks() - inicio_ticks) // 1000

    # Dibujar todos los elementos en pantalla 
    pantalla.fill(BLANCO)  # Limpia la pantalla para el nuevo frame
    pygame.draw.rect(pantalla, color_jugador, jugador)  # Dibuja el jugador (rectángulo azul o rojo)
    pygame.draw.rect(pantalla, ROJO, enemigo)           # Dibuja el enemigo (rectángulo rojo)

    # Dibuja la puntuación en la esquina superior izquierda
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    pantalla.blit(texto_puntos, (10, 10))

    # Dibuja el tiempo transcurrido en la esquina superior derecha
    texto_tiempo = fuente.render(f"Tiempo: {segundos}s", True, NEGRO)
    pantalla.blit(texto_tiempo, (ANCHO - 160, 10))

    pygame.display.update()  # Actualiza la pantalla para mostrar los cambios
    reloj.tick(60)           # Controla que el juego corra a 60 frames por segundo
