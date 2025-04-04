import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    color = (0, 0, 255)
    bg_color = (0, 0, 0)
    points = []

    tool = 'draw'  # what we draw with: brush, circle, rectangle, eraser
    drawing_shape = False
    shape_start = (0, 0)
    shape_end = (0, 0)

    canvas = pygame.Surface((640, 480))  # "canvas"
    canvas.fill(bg_color)

    while True:
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                return

            # tool and color selection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: tool = 'draw'
                if event.key == pygame.K_2: tool = 'circle'
                if event.key == pygame.K_3: tool = 'rect'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_r: color = (255, 0, 0)
                if event.key == pygame.K_g: color = (0, 255, 0)
                if event.key == pygame.K_b: color = (0, 0, 255)

            # mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shape_start = event.pos
                    drawing_shape = True
                if event.button == 4: radius = min(200, radius + 1)  # wheel up
                if event.button == 5: radius = max(1, radius - 1)    # wheel down

            # mouse released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape:
                    shape_end = event.pos
                    if tool in ['circle', 'rect']:
                        draw_shape(canvas, tool, shape_start, shape_end, color if tool != 'eraser' else bg_color)
                    drawing_shape = False

        # draw with brush or eraser
        if pygame.mouse.get_pressed()[0] and tool in ['draw', 'eraser']:
            pos = pygame.mouse.get_pos()
            points.append((pos, tool, color if tool != 'eraser' else bg_color, radius))
            points = points[-256:]  # limit the list to prevent lag

        # show the canvas
        screen.blit(canvas, (0, 0))

        # draw everything drawn with the brush
        for pt, t, col, r in points:
            pygame.draw.circle(screen, col, pt, r)

        # if drawing a shape — show how it will look
        if drawing_shape and tool in ['circle', 'rect']:
            shape_end = pygame.mouse.get_pos()
            draw_shape(screen, tool, shape_start, shape_end, color if tool != 'eraser' else bg_color, preview=True)

        pygame.display.flip()
        clock.tick(60)

# draw a shape
def draw_shape(surface, tool, start, end, color, preview=False):
    temp_surface = surface if not preview else surface.copy()

    if tool == 'circle':
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        rx = abs(start[0] - end[0]) // 2
        ry = abs(start[1] - end[1]) // 2
        r = (rx + ry) // 2
        pygame.draw.circle(temp_surface, color, center, r, 0 if not preview else 2)

    elif tool == 'rect':
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                           abs(start[0] - end[0]), abs(start[1] - end[1]))
        pygame.draw.rect(temp_surface, color, rect, 0 if not preview else 2)

    if preview:
        surface.blit(temp_surface, (0, 0))

main()