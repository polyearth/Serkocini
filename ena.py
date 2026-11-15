import pygame


class Lighting:

  def __init__(self, width, height):
    self.width = width
    self.height = height

    self.darkness_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    self.normal_radius = 70
    self.big_radius = 120 

    self.normal_light_surf = self.create_smooth_circle(self.normal_radius)
    self.big_light_surf = self.create_smooth_circle(self.big_radius)

    self.matches_left = 10 
    self.is_super_bright = False
    self.timer = 0.0

  def create_smooth_circle(self, radius):
    diameter = radius * 2
    surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

    for r in range(radius, 0, -1):
      alpha = int(255 * (1.0 - (r / radius) ** 1.2))
      pygame.draw.circle(surf, (0, 0, 0, alpha), (radius, radius), r)

    return surf

  def trigger_match(self):
    if self.matches_left > 0 and not self.is_super_bright:
      self.matches_left -= 1
      self.is_super_bright = True
      self.timer = 5.0  
      print("Aizdedzināts sērkociņš! Atlikuši:", self.matches_left)

  def update(self, dt):
    if self.is_super_bright:
      self.timer -= dt
      if self.timer <= 0:
        self.is_super_bright = False

  def draw(self, surface, screen_player_x, screen_player_y):
    self.darkness_surf.fill((0, 0, 0, 255))

    current_light_surf = (
        self.big_light_surf if self.is_super_bright else self.normal_light_surf
    )
    current_radius = self.big_radius if self.is_super_bright else self.normal_radius

    light_x = screen_player_x + 8 - current_radius
    light_y = screen_player_y + 8 - current_radius

    self.darkness_surf.blit(
        current_light_surf,
        (light_x, light_y),
        special_flags=pygame.BLEND_RGBA_SUB,
    )

    surface.blit(self.darkness_surf, (0, 0))

    font = pygame.font.SysFont(None, 16)
    match_text = font.render(
        f"Serkocini: {self.matches_left}", True, (255, 165, 0)
    )
    surface.blit(match_text, (5, 5))