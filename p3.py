import os
import sys

import pygame
import requests

screen = pygame.display.set_mode((600, 450))
running = True
value_changed = True
ll = 37.57
ll_2 = 55.703118
spn = 0.005
spn_2 = 0.00111
zoom_coeff = 1
clock = pygame.time.Clock()


def openn(x, y, m1, m2, format_='map'):
    global screen
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l={}".format(str(x), str(y),
                                                                                     str(m1),
                                                                                     str(m2),
                                                                                     format_)
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()

    os.remove(map_file)

    pygame.init()


pygame.init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                value_changed = True
                zoom_coeff *= 0.75
                if zoom_coeff < 0:
                    zoom_coeff = 0
                spn -= 0.005 * zoom_coeff
                spn_2 -= 0.005 * zoom_coeff
                if spn < 0:
                    spn = 0
                    zoom_coeff = 1
                if spn_2 < 0:
                    spn_2 = 0
                    zoom_coeff = 1
            if event.key == pygame.K_PAGEDOWN:
                value_changed = True
                zoom_coeff *= 1.8
                spn += 0.005 * zoom_coeff
                spn_2 += 0.005 * zoom_coeff
                if spn > 76:
                    spn, spn_2 = 75, 75
                    zoom_coeff /= 1.8
    if value_changed:
        openn(ll, ll_2, spn, spn_2)
        value_changed = False
