import asyncio
import pygame
from ena import Lighting
from game_objects import GameObjectManager
from istaba1 import Istaba1
from istaba2 import Istaba2
from istaba3 import Istaba3
from player import Player

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Serkocinu Spele - Hakatons")

try:
  pygame.mixer.music.load("Run-Amok(chosic_com).mp3")
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play(-1)
except Exception as e:
  print("Mūzika nav atrasta:", e)

virtual_width = 250
virtual_height = 200
virtual_screen = pygame.Surface((virtual_width, virtual_height))
clock = pygame.time.Clock()


def reset_game():
  global player, lighting, game_objects, istaba1, istaba2, istaba3, current_room, current_bg, bg_width, bg_height, start_ticks, main_wall_mask
  player = Player(400, 300)
  main_wall_mask = player.wall_mask  
  lighting = Lighting(virtual_width, virtual_height)
  game_objects = GameObjectManager(main_bg_width, main_bg_height, main_wall_mask)
  istaba1 = Istaba1()
  istaba2 = Istaba2()
  istaba3 = Istaba3()
  current_room = "main"
  current_bg = main_bg
  bg_width, bg_height = main_bg_width, main_bg_height
  start_ticks = pygame.time.get_ticks()


main_bg = pygame.image.load("mainmap.png").convert()
main_bg_width, main_bg_height = main_bg.get_size()

game_state = "MENU"
start_ticks = 0
main_wall_mask = None

reset_game()


async def main():
  global game_state, start_ticks, current_room, current_bg, bg_width, bg_height
  running = True
  last_time = pygame.time.get_ticks()

  while running:
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0
    last_time = current_time

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if event.type == pygame.KEYDOWN:
        if game_state == "MENU":
          if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            reset_game()
            game_state = "PLAYING"
        elif game_state in ["WIN", "GAME_OVER"]:
          if event.key == pygame.K_r:
            game_state = "MENU"
        elif game_state == "PLAYING":
          if event.key == pygame.K_q:
            lighting.trigger_match()

    virtual_screen.fill((15, 15, 20))

    if game_state == "MENU":
      font_title = pygame.font.SysFont(None, 32)
      font_sub = pygame.font.SysFont(None, 18)

      t1 = font_title.render("SERKOCIŅU SPĒLE", True, (255, 215, 0))
      t2 = font_sub.render("Nospied ENTER, lai sāktu", True, (200, 200, 200))
      t3 = font_sub.render("Atrodi 3 atslēgas un istabas 4 minūtēs!", True, (150, 150, 150))

      virtual_screen.blit(t1, (virtual_width // 2 - t1.get_width() // 2, 50))
      virtual_screen.blit(t2, (virtual_width // 2 - t2.get_width() // 2, 100))
      virtual_screen.blit(t3, (virtual_width // 2 - t3.get_width() // 2, 140))

    elif game_state == "PLAYING":
      elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
      time_left = max(0, 240 - int(elapsed_seconds))

      if time_left <= 0:
        game_state = "GAME_OVER"

      player.handle_input(bg_width, bg_height)
      lighting.update(dt)

      if current_room == "main":
        action = game_objects.update(player.x, player.y, player.size)
        if action == "enter_istaba1":
          current_room = "istaba1"
          current_bg = istaba1.bg_img
          bg_width, bg_height = istaba1.width, istaba1.height
          istaba1.enter(player)
        elif action == "enter_istaba2":
          current_room = "istaba2"
          current_bg = istaba2.bg_img
          bg_width, bg_height = istaba2.width, istaba2.height
          istaba2.enter(player)
        elif action == "enter_istaba3":
          current_room = "istaba3"
          current_bg = istaba3.bg_img
          bg_width, bg_height = istaba3.width, istaba3.height
          istaba3.enter(player)

        if istaba1.completed and istaba2.completed and istaba3.completed:
          game_state = "WIN"

      elif current_room == "istaba1":
        if istaba1.update(player, lighting):
          current_room = "main"
          current_bg = main_bg
          bg_width, bg_height = main_bg_width, main_bg_height
          player.wall_mask = main_wall_mask  # <--- Salabots!
          player.x, player.y = 530, 45
      elif current_room == "istaba2":
        if istaba2.update(player, lighting):
          current_room = "main"
          current_bg = main_bg
          bg_width, bg_height = main_bg_width, main_bg_height
          player.wall_mask = main_wall_mask  # <--- Salabots!
          player.x, player.y = 30, 310
      elif current_room == "istaba3":
        if istaba3.update(player, lighting):
          current_room = "main"
          current_bg = main_bg
          bg_width, bg_height = main_bg_width, main_bg_height
          player.wall_mask = main_wall_mask  # <--- Salabots!
          player.x, player.y = 760, 300

    
      camera_x = max(0, min(player.x - virtual_width // 2, bg_width - virtual_width))
      camera_y = max(0, min(player.y - virtual_height // 2, bg_height - virtual_height))
      screen_player_x = player.x - camera_x
      screen_player_y = player.y - camera_y

      
      virtual_screen.blit(current_bg, (-camera_x, -camera_y))
      
      if current_room == "main":
        game_objects.draw_objects(virtual_screen, camera_x, camera_y)
      elif current_room == "istaba1":
        istaba1.draw(virtual_screen, camera_x, camera_y)
      elif current_room == "istaba2":
        istaba2.draw(virtual_screen, camera_x, camera_y)
      elif current_room == "istaba3":
        istaba3.draw(virtual_screen, camera_x, camera_y)

      current_player_img = player.animations[player.current_direction][player.anim_index]
      virtual_screen.blit(current_player_img, (screen_player_x, screen_player_y))
      lighting.draw(virtual_screen, screen_player_x, screen_player_y)

      font_timer = pygame.font.SysFont(None, 16)
      timer_surf = font_timer.render(f"Laiks: {time_left // 60}:{time_left % 60:02d}", True, (255, 100, 100))
      virtual_screen.blit(timer_surf, (virtual_width - 65, 5))

    elif game_state == "WIN":
      font_win = pygame.font.SysFont(None, 28)
      t = font_win.render("APSVEICAM! TU UZVARĒJI!", True, (255, 215, 0))
      sub = pygame.font.SysFont(None, 16).render("Nospied R, lai atgrieztos izvēlnē", True, (200, 200, 200))
      virtual_screen.blit(t, (virtual_width // 2 - t.get_width() // 2, 70))
      virtual_screen.blit(sub, (virtual_width // 2 - sub.get_width() // 2, 120))

    elif game_state == "GAME_OVER":
      font_lose = pygame.font.SysFont(None, 28)
      t = font_lose.render("LAIKS BEIDZĀS! TU MIRSI", True, (255, 50, 50))
      sub = pygame.font.SysFont(None, 16).render("Nospied R, lai mēģinātu vēlreiz", True, (200, 200, 200))
      virtual_screen.blit(t, (virtual_width // 2 - t.get_width() // 2, 70))
      virtual_screen.blit(sub, (virtual_width // 2 - sub.get_width() // 2, 120))

    scaled_surf = pygame.transform.scale(virtual_screen, (screen_width, screen_height))
    screen.blit(scaled_surf, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    await asyncio.sleep(0)

  pygame.quit()


asyncio.run(main())