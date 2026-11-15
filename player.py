import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.size = (16, 16)
        
        self.animations = {
            "paKreisi": [
                pygame.transform.scale(pygame.image.load("paKreisi0.png"), self.size),
                pygame.transform.scale(pygame.image.load("paKreisi1.png"), self.size),
                pygame.transform.scale(pygame.image.load("paKreisi2.png"), self.size)
            ],
            "paLabi": [
                pygame.transform.scale(pygame.image.load("paLabi0.png"), self.size),
                pygame.transform.scale(pygame.image.load("paLabi1.png"), self.size),
                pygame.transform.scale(pygame.image.load("paLabi2.png"), self.size)
            ],
            "uzAugsu": [
                pygame.transform.scale(pygame.image.load("uzAugsu0.png"), self.size),
                pygame.transform.scale(pygame.image.load("uzAugsu1.png"), self.size),
                pygame.transform.scale(pygame.image.load("uzAugsu2.png"), self.size)
            ],
            "uzLeju": [
                pygame.transform.scale(pygame.image.load("uzLeju0.png"), self.size),
                pygame.transform.scale(pygame.image.load("uzLeju1.png"), self.size),
                pygame.transform.scale(pygame.image.load("uzLeju2.png"), self.size)
            ]
        }
        
        self.current_direction = "uzLeju"
        self.anim_index = 0
        self.anim_timer = 0

        try:
            self.wall_img = pygame.image.load("mainmapWalls.png").convert_alpha()
            self.wall_mask = pygame.mask.from_surface(self.wall_img)
        except Exception as e:
            print("Nevarēja ielādēt sienas.png:", e)
            self.wall_mask = None

        self.player_surf = pygame.Surface(self.size)

    def handle_input(self, screen_width, screen_height):
      keys = pygame.key.get_pressed()
      is_moving = False

      dx = 0
      dy = 0

      if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= self.speed
        self.current_direction = "paKreisi"
        is_moving = True
      if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += self.speed
        self.current_direction = "paLabi"
        is_moving = True
      if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= self.speed
        self.current_direction = "uzAugsu"
        is_moving = True
      if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += self.speed
        self.current_direction = "uzLeju"
        is_moving = True

      if self.wall_mask:
        current_image = self.animations[self.current_direction][self.anim_index]
        player_mask = pygame.mask.from_surface(current_image)

        # 1. Pārvietojamies pa X asi
        self.x += dx
        if self.wall_mask.overlap(player_mask, (int(self.x), int(self.y))):
          self.x -= dx  # Atgriežam atpakaļ, ja ir sadursme

        # 2. Pārvietojamies pa Y asi
        self.y += dy
        if self.wall_mask.overlap(player_mask, (int(self.x), int(self.y))):
          self.y -= dy  # Atgriežam atpakaļ, ja ir sadursme
      else:
        self.x += dx
        self.y += dy

    
      margin = 5
      if self.x < margin:
        self.x = margin
      elif self.x > screen_width - margin - self.size[0]:
        self.x = screen_width - margin - self.size[0]

      if self.y < margin:
        self.y = margin
      elif self.y > screen_height - margin - self.size[1]:
        self.y = screen_height - margin - self.size[1]

      if is_moving:
        self.anim_timer += 1
        if self.anim_timer > 10:
          self.anim_index = (self.anim_index + 1) % 3
          self.anim_timer = 0
      else:
        self.anim_index = 0

    def draw(self, surface):
        current_image = self.animations[self.current_direction][self.anim_index]
        surface.blit(current_image, (self.x, self.y))