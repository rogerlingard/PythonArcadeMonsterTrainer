"""
monster trainer file, where we have grid based movement and menus that we navigate to start the game.
"""
import arcade
import random
# Set how many rows and columns we will have
ROW_COUNT = 5
COLUMN_COUNT = 100

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 60
HEIGHT = 60

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
WINDOW_WIDTH = (WIDTH + MARGIN) * 5 + MARGIN
WINDOW_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
WINDOW_TITLE = "Monster Trainer"    

# Had ChatGPT help me set up a menu view to start the game. We are basically drawing on the screen a prompt to start the game by hitting enter.
# When the enter, we make a new instance of the game view and call the setup method to initialize the game state.
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.starter_text = None
        self.enter_text = None
    
    def setup(self):
        self.starter_text = arcade.Text("Deliver the Cake", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50, font_size=35, anchor_x="center")
        self.enter_text = arcade.Text("Press ENTER to start", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font_size=20, anchor_x="center")
        self.info_text1 = arcade.Text("Use the arrow keys to move your character.", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, font_size=12, anchor_x="center")
        self.info_text2 = arcade.Text("Push the cake to the end to win.", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 70, font_size=12, anchor_x="center")
        
    def on_draw(self):
        self.clear()
        self.starter_text.draw()
        self.enter_text.draw()
        self.info_text1.draw()
        self.info_text2.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)

#Used the help of ChatGPT with this view, mainly because this view is called after the camera is moved. This view creates a new camera view 
#so that the text is in the center of the screen. 
class GamerOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_over_text = None
        self.restart_text = None  
        self.camera = arcade.camera.Camera2D()       

    def setup(self):
        self.game_over_text = arcade.Text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40, font_size=35, anchor_x="center", anchor_y="center")
        self.restart_text = arcade.Text("Press ENTER to restart", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font_size=20, anchor_x="center", anchor_y="center")
        self.quit_text = arcade.Text("Press Backspace to quit", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 25, font_size=20, anchor_x="center", anchor_y="center")
        pass

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.game_over_text.draw()
        self.restart_text.draw()
        self.quit_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)
        if key == arcade.key.BACKSPACE:
            arcade.close_window()


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()

        self.background_color = arcade.color.BLACK

        #For the grid logic I mainly followed this website https://api.arcade.academy/en/3.3.1/example_code/array_backed_grid_sprites_2.html#array-backed-grid-sprites-2
        self.grid = []
        self.grid_sprites = []
        self.grid_sprite_list = arcade.SpriteList()
        self.last_spawn = 0
        self.spawn_distance = 2
        

        self.player_list = arcade.SpriteList()
        self.player = None

        self.cake_list = arcade.SpriteList()
        self.cake = None

        #using ChatGPT to help me figure out how to add sound files to the program. We are basically making the empty variables here and adding the sound to them in setup.
        self.push_sound = None
        self.cake_hit_sound = None
        self.win_sound = None
        self.player_hit_sound = None

        # Create a list of solid-color sprites to represent each grid location
        #I added 
        for row in range(ROW_COUNT):
            self.grid.append([])
            sprite_row = []
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, color=arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                sprite_row.append(sprite)
            self.grid_sprites.append(sprite_row)
        self.camera = arcade.camera.Camera2D()

    def get_screen_position(self, grid_x, grid_y):
        x = grid_x * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        y = grid_y * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        return x, y


    def setup(self):

        player_img = "images/ball_guy.png"
        self.player = arcade.Sprite(player_img, scale=0.035)
        self.player_row = 2
        self.player_column = 0
        x, y = self.get_screen_position(self.player_column, self.player_row)
        self.player.center_x = x
        self.player.center_y = y 

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        cake_img = "images/cake.png"
        self.cake = arcade.Sprite(cake_img, scale=0.035)
        self.cake_row = 2
        self.cake_column = 2
        x, y = self.get_screen_position(self.cake_column, self.cake_row)
        self.cake.center_x = x
        self.cake.center_y = y

        self.cake_list = arcade.SpriteList()
        self.cake_list.append(self.cake)
        self.spike_list = arcade.SpriteList()

        self.push_sound = arcade.load_sound("sounds/push.mp3")
        self.cake_hit_sound = arcade.load_sound("sounds/cake_hit.mp3")
        self.player_hit_sound = arcade.load_sound("sounds/player_hit.mp3")
        self.win_sound = arcade.load_sound("sounds/win.mp3")

    def on_draw(self):
        self.clear()

        # Activate the camera
        self.camera.use()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()
        self.cake_list.draw()
        self.spike_list.draw()
        self.player_list.draw()
        
    
    # Copilot helped me implement the player movement and camera movement.
    # For the player movement, we check which key is being pressed, and we then update the move column and row accordingly. We then add the column value to the player column value to move 
    # The player moves in a direction one grid square. We check to see if the player is going out of the bounds, and if they are, we do not move them.
    def on_key_press(self, key, modifiers):
        move_column = 0
        move_row = 0
        if key == arcade.key.RIGHT:
            move_column = 1
        elif key == arcade.key.LEFT:
            move_column = -1
        elif key == arcade.key.UP:
            move_row = 1
        elif key == arcade.key.DOWN:
            move_row = -1
        else:
            return
        
        new_player_column = self.player_column + move_column
        new_player_row = self.player_row + move_row
        if not self.in_bounds(new_player_row, new_player_column):
            return
        # We then check to see if the new column or row we are moving to is the same row as the cake. If it is, then we get new cake columns and rows so that we move the cake accordingly, just like the platter moved.
        # We check to see if the cake is in bounds, and if it is, then we move the cake to its new position.
        if new_player_column == self.cake_column and new_player_row == self.cake_row:
            new_cake_column = self.cake_column + move_column
            new_cake_row = self.cake_row + move_row
            if self.in_bounds(new_cake_row, new_cake_column):
                self.cake_column = new_cake_column
                self.cake_row = new_cake_row
                cake_x, cake_y = self.get_screen_position(self.cake_column, self.cake_row)
                self.cake.center_x = cake_x
                self.cake.center_y = cake_y
                arcade.play_sound(self.push_sound)

        self.player_column = new_player_column
        self.player_row = new_player_row
        x, y = self.get_screen_position(self.player_column, self.player_row)
        self.player.center_x = x
        self.player.center_y = y
    
    def on_update(self, delta_time):
        self.camera_movement()
        
        if arcade.check_for_collision_with_list(self.player, self.cake_list):
           self.cake.position = (self.get_screen_position(self.player_column + 1, self.player_row)[0], self.cake.position[1])
        
        if arcade.check_for_collision_with_list(self.cake, self.spike_list):
            arcade.play_sound(self.cake_hit_sound)
            game_over = GamerOverView()
            game_over.setup()
            self.window.show_view(game_over)
            return

        if arcade.check_for_collision_with_list(self.player, self.spike_list):
            arcade.play_sound(self.player_hit_sound)
            game_over = GamerOverView()
            game_over.setup()
            self.window.show_view(game_over)
            return
        
        # Here we are making the new spikes as long as the last spawn and the spawn distance added together are less than the player's column. This basically means we just spawn the spikes before the player on the screen.
        # We do this so that we are not spawning spikes behind us, but in front of us instead
        if self.player_column > self.last_spawn + self.spawn_distance:
            self.spawn_spike()
            self.spawn_spike()
            self.last_spawn = self.player_column

        #When we get the cake to the end, then we do the win view.
        if self.cake_column == COLUMN_COUNT - 1:
            arcade.play_sound(self.win_sound)
            win = YouWinView()
            win.setup()
            self.window.show_view(win)
            return

    #I used ChatGPT to help with this function. We are making a spike sprite, and making them spawn in 4 columns away from the player, so they spawn off-screen
    #We then use a random int to spawn the spike in a random row. We do not spawn a spike if it is going to spawn outside of the grid.
    #Then we get the x, y coordinates that are within the grid cells, and then center the spike inside the grid cell. Lastly, we appended the spike sprite to the spike sprite list. 
    def spawn_spike(self):
        spike = arcade.Sprite("images/spike.png", scale=0.38)

        spawn_column = self.player_column + 4
        spawn_row = random.randint(0, 5)

        if spawn_column > COLUMN_COUNT - 1:
            return 
        
        x, y = self.get_screen_position(spawn_column, spawn_row)
        spike.center_x = x
        spike.center_y = y

        self.spike_list.append(spike)


    def in_bounds(self, row, column):
        return 0 <= row < ROW_COUNT and 0 <= column < COLUMN_COUNT

    # Had the help of ChatGPT with the camera movement to move it with the player and also center it around the grid that we had.
    # We update the position each time we move and dynamically make it snap to the player's position so we can always have a view of the player.
    def camera_movement(self):
        self.camera.position = (self.get_screen_position(self.player_column + 2, self.player_row)[0], 165)


# I used ChatGPT here to make a quick win view so that I could finish this project in my set time limit. The view basically makes a camera and then draws the text to the view.
# We make the camera center the text in the middle of the screen, so that the user can see it. Then we listen if the user presses Enter, and if they do, we make the gameView and start it again.
class YouWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.win_text = None
        self.restart_text = None
        self.camera = arcade.camera.Camera2D()

    def setup(self):
        self.win_text = arcade.Text(
            "YOU WIN!",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 40,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )
        self.restart_text = arcade.Text(
            "Press ENTER to play again",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )
        self.quit_text = arcade.Text(
            "Press Backspace to quit",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 25,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.win_text.draw()
        self.restart_text.draw()
        self.quit_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            game.setup()
            self.window.show_view(game)
        if key == arcade.key.BACKSPACE:
            arcade.close_window()

def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu = MenuView()
    menu.setup() 
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()