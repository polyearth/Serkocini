import random
import pygame


class Istaba3:

  def __init__(self):
    self.active = False
    self.completed = False

    try:
      self.bg_img = pygame.image.load("istaba3.png").convert()
      self.width, self.height = self.bg_img.get_size()
    except Exception:
      self.width, self.height = 800, 600
      self.bg_img = pygame.Surface((self.width, self.height))
      self.bg_img.fill((30, 30, 30))

    try:
      self.wall_img = pygame.image.load("istaba3Walls.png").convert_alpha()
      self.wall_mask = pygame.mask.from_surface(self.wall_img)
    except Exception:
      self.wall_mask = None

    self.match_size = (16, 16)
    try:
      self.match_img = pygame.transform.scale(
          pygame.image.load("serkocini.png").convert_alpha(), self.match_size
      )
    except Exception:
      self.match_img = pygame.Surface(self.match_size)
      self.match_img.fill((255, 140, 0))

    self.match_collected = False
    self.match_x, self.match_y = self.spawn_match()
    self.match_rect = pygame.Rect(
        self.match_x, self.match_y, self.match_size[0], self.match_size[1]
    )

  def spawn_match(self):
    for _ in range(500):
      rx = random.randint(40, max(41, self.width - 40))
      ry = random.randint(40, max(41, self.height - 40))
      if self.wall_mask:
        surf = pygame.Surface(self.match_size)
        mask = pygame.mask.from_surface(surf)
        if not self.wall_mask.overlap(mask, (rx, ry)):
          return rx, ry
      else:
        return rx, ry
    return self.width // 2, self.height // 2

  def enter(self, player):
    self.active = True
    player.wall_mask = self.wall_mask
    player.x = self.width // 2
    player.y = self.height - 60

  def update(self, player, lighting):
    if not self.active:
      return False
    player_rect = pygame.Rect(
        player.x, player.y, player.size[0], player.size[1]
    )
    if not self.match_collected and player_rect.colliderect(self.match_rect):
      self.match_collected = True
      self.completed = True
      self.active = False
      if hasattr(lighting, "matches_left"):
        lighting.matches_left += 1
      print("Sērkociņš atrasts 3. istabā!")
      return True
    return False

  def draw(self, surface, camera_x, camera_y):
    if not self.match_collected:
      surface.blit(
          self.match_img, (self.match_x - camera_x, self.match_y - camera_y)
      )