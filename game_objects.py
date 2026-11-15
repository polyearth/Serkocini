import random
import pygame


class GameObjectManager:

  def __init__(self, screen_width, screen_height, wall_mask):
    self.screen_width = screen_width
    self.screen_height = screen_height

    self.key_size = (32, 32)

    try:
      self.key1_img = pygame.transform.scale(
          pygame.image.load("pirmaAtslega.png").convert_alpha(), self.key_size
      )
      self.key2_img = pygame.transform.scale(
          pygame.image.load("otraAtslega.png").convert_alpha(), self.key_size
      )
      self.key3_img = pygame.transform.scale(
          pygame.image.load("tresaAtslega.png").convert_alpha(), self.key_size
      )
    except Exception as e:
      print("Kļūda ielādējot atslēgas:", e)
      fallback = pygame.Surface(self.key_size)
      fallback.fill((255, 255, 0))
      self.key1_img = self.key2_img = self.key3_img = fallback

    self.has_key1 = False
    self.has_key2 = False
    self.has_key3 = False

    self.key1_collected = False
    self.key2_collected = False
    self.key3_collected = False

    self.door1_unlocked = False
    self.door2_unlocked = False
    self.door3_unlocked = False

   
    self.door1_rect = pygame.Rect(515, 13, 44, 22)
    self.door2_rect = pygame.Rect(14, 289, 20, 46)

    self.door3_rect = pygame.Rect(785, 280, 20, 44)

  
    self.key1_x, self.key1_y = self.spawn_random_key(wall_mask, min_dist=0)
    self.key2_x, self.key2_y = self.spawn_random_key(
        wall_mask, self.key1_x, self.key1_y, min_dist=100
    )
    self.key3_x, self.key3_y = self.spawn_random_key(
        wall_mask, self.key2_x, self.key2_y, min_dist=100
    )

    self.key1_rect = pygame.Rect(
        self.key1_x, self.key1_y, self.key_size[0], self.key_size[1]
    )
    self.key2_rect = pygame.Rect(
        self.key2_x, self.key2_y, self.key_size[0], self.key_size[1]
    )
    self.key3_rect = pygame.Rect(
        self.key3_x, self.key3_y, self.key_size[0], self.key_size[1]
    )

  def spawn_random_key(self, wall_mask, avoid_x=None, avoid_y=None, min_dist=80):
    while True:
      rx = random.randint(40, self.screen_width - 40)
      ry = random.randint(40, self.screen_height - 40)

      if avoid_x is not None and avoid_y is not None:
        dist = ((rx - avoid_x) ** 2 + (ry - avoid_y) ** 2) ** 0.5
        if dist < min_dist:
          continue

      if wall_mask:
        surf = pygame.Surface(self.key_size)
        surf.fill((255, 255, 255)) 
        mask = pygame.mask.from_surface(surf)
        
        if not wall_mask.overlap(mask, (rx, ry)):
          return rx, ry
      else:
        return rx, ry

  def update(self, player_x, player_y, player_size):
    player_rect = pygame.Rect(
        player_x, player_y, player_size[0], player_size[1]
    )

    if not self.key1_collected and player_rect.colliderect(self.key1_rect):
      self.has_key1 = True
      self.key1_collected = True
      print("Pirmā atslēga (melno durvju) savākta!")

    if not self.key2_collected and player_rect.colliderect(self.key2_rect):
      self.has_key2 = True
      self.key2_collected = True
      print("Otrā atslēga (violeto durvju) savākta!")

    if not self.key3_collected and player_rect.colliderect(self.key3_rect):
      self.has_key3 = True
      self.key3_collected = True
      print("Trešā atslēga (brūno durvju) savākta!")

    if not self.door1_unlocked and player_rect.colliderect(self.door1_rect):
      if self.has_key1:
        self.door1_unlocked = True
        return "enter_istaba1"

    if not self.door2_unlocked and player_rect.colliderect(self.door2_rect):
      if self.has_key2:
        self.door2_unlocked = True
        return "enter_istaba2"

    if not self.door3_unlocked and player_rect.colliderect(self.door3_rect):
      if self.has_key3:
        self.door3_unlocked = True
        return "enter_istaba3"

    return None

  def draw_objects(self, surface, camera_x, camera_y):
    if not self.key1_collected:
      surface.blit(
          self.key1_img, (self.key1_x - camera_x, self.key1_y - camera_y)
      )
    if not self.key2_collected:
      surface.blit(
          self.key2_img, (self.key2_x - camera_x, self.key2_y - camera_y)
      )
    if not self.key3_collected:
      surface.blit(
          self.key3_img, (self.key3_x - camera_x, self.key3_y - camera_y)
      )