import os
import sys
import random
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                new_enemy = Enemy(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    f = open('data/record.txt', 'w+')
    f.seek(0)
    f.write(str(highest_score))
    f.close()
    pygame.quit()
    sys.exit()


def restart_game():
    global alive
    alive = False


def death_screen():
    intro_text = ["Вы нарушили все 3 правила", "",
                  "Первое правило не трогать капибар",
                  "Второе правило не трогать капибар",
                  "Третье правило не трогать капибар", "",
                  "Дэб не смог этого пережить", f"Вас счет {score}", f"Ваш лучший счет {highest_score}",
                  "Нажмите любую кнопку для рестарта"]

    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    global easy_mode
                    easy_mode = False
                else:

                    easy_mode = True
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Escape from capybara", "",
                  "Первое правило не трогать капибар",
                  "Второе правило не трогать капибар",
                  "Третье правило не трогать капибар",
                  "okay i pull up", "lets go to the afteparty", "ЛКМ - легкий режим", "ПКМ - хардкор"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    global easy_mode
                    easy_mode = False
                else:

                    easy_mode = True
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, pos_x, pos_y):
        screen.fill((0, 0, 0))
        self.pos = (pos_x, pos_y)

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, pos_x, pos_y):
        screen.fill((0, 0, 0))
        self.pos = (pos_x, pos_y)

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        if self.pos == player.pos:
            restart_game()


def move(hero, direction):
    pos_x = hero.pos[0]
    pos_y = hero.pos[1]
    print(pos_x, pos_y)

    if direction == 'up' and (lmap[pos_y - 1][pos_x] == '.' or lmap[pos_y - 1][pos_x] == '@'):
        hero.move(pos_x, pos_y - 1)

    if direction == 'down' and (lmap[pos_y + 1][pos_x] == '.' or lmap[pos_y + 1][pos_x] == '@'):
        hero.move(pos_x, pos_y + 1)

    if direction == 'left' and (lmap[pos_y][pos_x - 1] == '.' or lmap[pos_y][pos_x - 1] == '@'):
        hero.move(pos_x - 1, pos_y)

    if direction == 'right' and (lmap[pos_y][pos_x + 1] == '.' or lmap[pos_y][pos_x + 1] == '@'):
        hero.move(pos_x + 1, pos_y)


player = None
pygame.init()
size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Escape from capybara")
# группы спрайтов
enemy_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')

}
player_image = load_image('mar.png')
enemy_image = load_image('enemy.png')

tile_width = tile_height = 50
clock = pygame.time.Clock()
easy_mode = True
running = True
alive = True
st_screen = True
score = 0
highest_score = int(open("data/record.txt", "r").read())

while running:
    enemy_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    if st_screen:
        start_screen()
        st_screen = False
    else:
        death_screen()

    alive = True
    ft = 0
    highest_score = max(score, highest_score)
    score = 0
    lmap = load_level('map.txt')
    player, level_x, level_y = generate_level(lmap)
    if easy_mode:
        while alive:

            while random.randint(1, 17) == 1:
                new_enemy = Enemy(19, random.randint(1, 14))
            ft += 1
            if ft % 15 == 0:
                score += 1
                for i in enemy_group:
                    i.move(i.pos[0] - 1, i.pos[1])
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    alive = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move(player, 'up')
                    if event.key == pygame.K_DOWN:
                        move(player, 'down')
                    if event.key == pygame.K_LEFT:
                        move(player, 'left')
                    if event.key == pygame.K_RIGHT:
                        move(player, 'right')

            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)

            enemy_group.draw(screen)

            clock.tick(FPS)
            pygame.display.flip()
    else:

        while alive:

            while random.randint(1, 3) == 1:
                new_enemy = Enemy(19, random.randint(1, 14))
            ft += 1
            if ft % 5 == 0:
                score += 1
                for i in enemy_group:
                    i.move(i.pos[0] - 1, i.pos[1])
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    alive = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move(player, 'up')
                    if event.key == pygame.K_DOWN:
                        move(player, 'down')
                    if event.key == pygame.K_LEFT:
                        move(player, 'left')
                    if event.key == pygame.K_RIGHT:
                        move(player, 'right')

            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)

            enemy_group.draw(screen)

            clock.tick(FPS)
            pygame.display.flip()
f = open('data/record.txt', 'w+')
f.seek(0)
f.write(str(highest_score))
f.close()
