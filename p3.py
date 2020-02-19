import os
import sys

import pygame
import requests

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
value_changed = True
ll = 37.57
ll_2 = 55.703118
spn = 0.005
spn_2 = 0.00111
zoom_coeff = 1
formatt = 'map'
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
input_box = pygame.Rect(5, 415, 520, 32)
search = pygame.Rect(527, 415, 69, 32)
color_inactive = pygame.Color('white')
color_active = (230, 230, 230)
color = color_inactive
search_color_inactive = (255, 204, 0)
search_color_active = (235, 172, 0)
search_color = search_color_inactive
active = False
text = ''
hold = False
button_hold = False
pt = None
back_hold = False
tick = 0
clock_tick = 15


def finder(text):
    global ll
    global ll_2
    global pt
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": text,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    if 'error' in json_response or len(json_response["response"]["GeoObjectCollection"][
                                           "featureMember"]) == 0:
        pt = '&pt={},{}'.format(ll, ll_2)
        return ll, ll_2
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    pt = '&pt={},{}'.format(toponym_longitude, toponym_lattitude)
    toponym_lattitude = float(toponym_lattitude)
    toponym_longitude = float(toponym_longitude)
    return toponym_longitude, toponym_lattitude


def openn(x, y, m1, m2, format_='map'):
    global screen
    global pt
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l={}".format(str(x), str(y),
                                                                                     str(m1),
                                                                                     str(m2),
                                                                                     format_)
    if pt is not None:
        map_request += pt
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
            if event.key == pygame.K_LCTRL:
                value_changed = True
                if formatt == 'map':
                    formatt = 'sat'
                elif formatt == 'sat':
                    formatt = 'sat,skl'
                elif formatt == 'sat,skl':
                    formatt = 'map'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            elif search.collidepoint(event.pos):
                button_hold = True
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.MOUSEBUTTONUP:
            if search.collidepoint(event.pos):
                ll, ll_2 = finder(text)
                text = ''
                active = False
                color = color_inactive
                value_changed = True
            button_hold = False
            search_color = search_color_inactive
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                ll += spn * 2
                value_changed = True
            if key[pygame.K_LEFT]:
                ll -= spn * 2
                value_changed = True
            if key[pygame.K_UP]:
                ll_2 += spn_2 * 2
                value_changed = True
            if key[pygame.K_DOWN]:
                ll_2 -= spn_2 * 2
                value_changed = True
            if active:
                if event.key == pygame.K_RETURN:
                    ll, ll_2 = finder(text)
                    text = ''
                    value_changed = True
                elif event.key == pygame.K_BACKSPACE:
                    clock_tick = 25
                    if len(text) != 0:
                        text = text[:-1]
                    back_hold = True
                else:
                    clock_tick = 25
                    text += event.unicode
                    hold = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                back_hold = False
            else:
                hold = False
            tick = 0
        if not search.collidepoint(pygame.mouse.get_pos()) and button_hold:
            search_color = search_color_inactive
        elif search.collidepoint(pygame.mouse.get_pos()) and button_hold:
            search_color = search_color_active
    if hold or back_hold:
        if hold:
            clock_tick = 25
        tick += 1
        if tick > 15:
            if hold:
                if len(text) != 0:
                    text += text[-1]
            else:
                if len(text) != 0:
                    text = text[:-1]
    if active and clock_tick in range(15, 30):
        txt_surface = font.render(text + '|', True, pygame.Color('black'))
    else:
        txt_surface = font.render(text, True, pygame.Color('black'))
    find_text = font.render('Найти', True, pygame.Color('black'))
    pygame.draw.rect(screen, color, input_box, 0)
    pygame.draw.rect(screen, search_color, search, 0)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    screen.blit(find_text, (531, 421))
    pygame.display.flip()
    if active:
        clock_tick += 1
    else:
        clock_tick = 15
    if clock_tick == 30:
        clock_tick = 0
    clock.tick(30)
    if value_changed:
        openn(ll, ll_2, spn, spn_2, formatt)
        value_changed = False
