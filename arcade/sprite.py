from .draw_commands import *
from .geometry import *


class SpriteList():
    """
    List of sprites.

    :Example:

    >>> import arcade
    >>> import random
    >>> arcade.open_window("Sprite Example", 600, 600)
    >>> scale = 0.002
    >>> meteor_list = arcade.SpriteList()
    >>> for i in range(100):
    ...     meteor = arcade.Sprite("examples/images/meteorGrey_big1.png", \
scale)
    ...     meteor.center_x = random.random() * 2 - 1
    ...     meteor.center_y = random.random() * 2 - 1
    ...     meteor_list.append(meteor)
    >>> arcade.set_background_color(arcade.color.WHITE)
    >>> arcade.start_render()
    >>> meteor_list.draw()
    >>> arcade.finish_render()
    >>> arcade.pause(0.5)
    >>> arcade.close_window()
    """
    def __init__(self):
        self.sprite_list = []

    def append(self, item):
        """
        Add a new sprite to the list.
        """
        self.sprite_list.append(item)
        item._register_sprite_list(self)

    def remove(self, item):
        """
        Remove a specific sprite from the list.
        """
        self.sprite_list.remove(item)

    def update(self):
        """
        Call the update() method on each sprite in the list.
        """
        for sprite in self.sprite_list:
            sprite.update()

    def draw(self):
        """
        Call the draw() method on each sprite in the list.
        """
        for sprite in self.sprite_list:
            sprite.draw()

    def __len__(self):
        return len(self.sprite_list)

    def __iter__(self):
        return iter(self.sprite_list)

    def pop(self):
        """
        Pop off the last sprite in the list.
        """
        return self.sprite_list.pop()


class Sprite():
    """
    Class that represents a 'sprite' on-screen.

    :Example:

    >>> import arcade
    >>> arcade.open_window("Sprite Example", 800, 600)
    >>> scale = 0.002
    >>> ship_sprite = arcade.Sprite("examples/images/playerShip1_orange.png", \
scale)
    >>> arcade.set_background_color(arcade.color.WHITE)
    >>> arcade.start_render()
    >>> ship_sprite.draw()
    >>> arcade.finish_render()
    >>> # Enable the following to keep the window up after running.
    >>> # arcade.run()
    """
    def __init__(self, filename=None, scale=0, x=0, y=0, width=0, height=0):
        if width < 0:
            raise SystemError("Width of image can't be less than zero.")

        if height < 0:
            raise SystemError("Height of image can't be less than zero.")

        if width == 0 and height != 0:
            raise SystemError("Width can't be zero.")

        if height == 0 and width != 0:
            raise SystemError("Height can't be zero.")

        if filename is not None:
            self.texture = load_texture(filename, x, y,
                                        width, height)

            self.textures = [self.texture]
            self.width = self.texture.width * scale
            self.height = self.texture.height * scale
        else:
            self.textures = []
            self.width = 0
            self.height = 0

        self.cur_texture_index = 0
        self.scale = scale
        self.center_x = 0
        self.center_y = 0
        self.angle = 0.0

        self.change_x = 0
        self.change_y = 0
        self.change_angle = 0

        self.alpha = 1.0
        self.sprite_lists = []
        self.transparent = True

        # Physics
        self.apply_gravity = False

    def append_texture(self, texture):
        self.textures.append(texture)

    def set_texture(self, texture_no):
        self.texture = self.textures[texture_no]
        self.cur_texture_index = texture_no
        self.width = self.textures[texture_no].width * self.scale
        self.height = self.textures[texture_no].height * self.scale

    def set_position(self, center_x, center_y):
        """
        Set a sprite's position
        """
        self.center_x = center_x
        self.center_y = center_y

    def get_points(self):
        """
        Get the corner points for the rect that makes up the sprite.
        """
        x1, y1 = rotate(self.center_x - self.width / 2,
                        self.center_y - self.height / 2,
                        self.center_x,
                        self.center_y,
                        self.angle)
        x2, y2 = rotate(self.center_x + self.width / 2,
                        self.center_y - self.height / 2,
                        self.center_x,
                        self.center_y,
                        self.angle)
        x3, y3 = rotate(self.center_x + self.width / 2,
                        self.center_y + self.height / 2,
                        self.center_x,
                        self.center_y,
                        self.angle)
        x4, y4 = rotate(self.center_x - self.width / 2,
                        self.center_y + self.height / 2,
                        self.center_x,
                        self.center_y,
                        self.angle)

        return ((x1, y1), (x2, y2), (x3, y3), (x4, y4))

    points = property(get_points)

    def _get_bottom(self):
        """
        The lowest y coordinate.

        >>> import arcade
        >>> arcade.open_window("Sprite Example", 800, 600)
        >>> scale = 1/75
        >>> ship_sprite = \
arcade.Sprite("examples/images/playerShip1_orange.png", scale)
        >>> ship_sprite.center_y = 0
        >>> print(ship_sprite.bottom)
        -0.5
        >>> ship_sprite.bottom = 1
        >>> print(ship_sprite.bottom)
        1.0
        """
        points = self.get_points()
        return min(points[0][1], points[1][1], points[2][1], points[3][1])

    def _set_bottom(self, amount):
        """ The lowest y coordinate. """
        points = self.get_points()
        lowest = min(points[0][1], points[1][1], points[2][1], points[3][1])
        diff = lowest - amount
        self.center_y -= diff

    bottom = property(_get_bottom, _set_bottom)

    def _get_top(self):
        """
        The highest y coordinate.

        >>> import arcade
        >>> arcade.open_window("Sprite Example", 800, 600)
        >>> scale = 1/75
        >>> ship_sprite = \
arcade.Sprite("examples/images/playerShip1_orange.png", scale)
        >>> ship_sprite.center_y = 0
        >>> print(ship_sprite.top)
        0.5
        >>> ship_sprite.top = 1
        >>> print(ship_sprite.top)
        1.0
        """
        points = self.get_points()
        return max(points[0][1], points[1][1], points[2][1], points[3][1])

    def _set_top(self, amount):
        """ The highest y coordinate. """
        points = self.get_points()
        highest = max(points[0][1], points[1][1], points[2][1], points[3][1])
        diff = highest - amount
        self.center_y -= diff

    top = property(_get_top, _set_top)

    def _get_left(self):
        """
        Left-most coordinate.

        :Example:

        >>> import arcade
        >>> arcade.open_window("Sprite Example", 800, 600)
        >>> scale = 1/99
        >>> ship_sprite = \
arcade.Sprite("examples/images/playerShip1_orange.png", scale)
        >>> ship_sprite.center_x = 0
        >>> print(ship_sprite.left)
        -0.5
        >>> ship_sprite.left = 1
        >>> print(ship_sprite.left)
        1.0
        """
        points = self.get_points()
        return min(points[0][0], points[1][0], points[2][0], points[3][0])

    def _set_left(self, amount):
        """ The left most x coordinate. """
        points = self.get_points()
        leftmost = min(points[0][0], points[1][0], points[2][0], points[3][0])
        diff = amount - leftmost
        self.center_x += diff

    left = property(_get_left, _set_left)

    def _get_right(self):
        """
        Right-most coordinate

        :Example:

        >>> import arcade
        >>> arcade.open_window("Sprite Example", 800, 600)
        >>> scale = 1/99
        >>> ship_sprite = \
arcade.Sprite("examples/images/playerShip1_orange.png", scale)
        >>> ship_sprite.center_x = 0
        >>> print(ship_sprite.right)
        0.5
        >>> ship_sprite.right = 1
        >>> print(ship_sprite.right)
        1.0
        """

        points = self.get_points()
        return max(points[0][0], points[1][0], points[2][0], points[3][0])

    def _set_right(self, amount):
        """ The right most x coordinate. """
        points = self.get_points()
        rightmost = max(points[0][0], points[1][0], points[2][0], points[3][0])
        diff = rightmost - amount
        self.center_x -= diff

    right = property(_get_right, _set_right)

    def _get_texture(self):
        return self._texture

    def _set_texture(self, texture):
        if type(texture) is Texture:
            self._texture = texture
        else:
            raise SystemError("Can't set the texture to something that is " +
                              "not an instance of the Texture class.")

    texture = property(_get_texture, _set_texture)

    def _register_sprite_list(self, new_list):
        self.sprite_lists.append(new_list)

    def draw(self):
        """ Draw the sprite. """
        draw_texture_rect(self.center_x, self.center_y,
                          self.width, self.height,
                          self.texture, self.angle, self.alpha,
                          self.transparent)

    def update(self):
        """ Update the sprite. """
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

    def kill(self):
        """ Remove the sprite from all sprite lists. """
        for sprite_list in self.sprite_lists:
            if self in sprite_list:
                sprite_list.remove(self)


class TurningSprite(Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) \
            - 90


class PlatformerSpriteSheetSprite(Sprite):
    """
    Sprite for platformer games that supports animations.
    """
    def __init__(self):
        super().__init__()
        self.last_change_x = self.center_x
        self.facing = "right"
        self.left_walk_textures = []
        self.right_walk_textures = []
        self.up_walk_textures = []
        self.down_walk_textures = []
        self.jump_textures = []
        self.left_stand_textures = []
        self.right_stand_textures = []
        self.up_stand_textures = []
        self.down_stand_textures = []

        self.cur_texture_index = 0
        self.texture_change_distance = 0
        self.speed = 0.003

    def update(self):
        """
        Logic for selecting the proper texture to use.
        """
        if self.change_y == 0.0:
            if self.change_x < 0:
                if abs(self.last_change_x - self.center_x) > \
                        self.texture_change_distance:
                    if self.cur_texture_index in self.left_textures:
                        pos = self.left_textures.index(self.cur_texture_index)\
                            + 1
                    else:
                        pos = 0
                    if pos >= len(self.left_textures):
                        pos = 0
                    self.set_texture(self.left_textures[pos])
                    self.last_change_x = self.center_x

            elif self.change_x > 0:
                if abs(self.last_change_x - self.center_x) \
                        > self.texture_change_distance:
                    if self.cur_texture_index in self.right_textures:
                        i = self.cur_texture_index
                        pos = self.right_textures.index(i) + 1
                    else:
                        pos = 0
                    if pos >= len(self.right_textures):
                        pos = 0
                    self.set_texture(self.right_textures[pos])
                    self.last_change_x = self.center_x
            else:
                if self.facing == "right":
                    self.set_texture(self.right_stand_textures[0])
                if self.facing == "left":
                    self.set_texture(self.left_stand_textures[0])

        else:
            if self.facing == "right":
                self.set_texture(self.jump_right_textures[0])
            if self.facing == "left":
                self.set_texture(self.jump_left_textures[0])

    def set_left_walk_textures(self, texture_index_list):
        self.left_textures = texture_index_list

    def set_right_walk_textures(self, texture_index_list):
        self.right_textures = texture_index_list

    def set_left_jump_textures(self, texture_index_list):
        self.jump_left_textures = texture_index_list

    def set_right_jump_textures(self, texture_index_list):
        self.jump_right_textures = texture_index_list

    def set_left_stand_textures(self, texture_index_list):
        self.left_stand_textures = texture_index_list

    def set_right_stand_textures(self, texture_index_list):
        self.right_stand_textures = texture_index_list

    def go_left(self):
        self.change_x = -self.speed

    def stop_left(self):
        if self.change_x < 0:
            self.change_x = 0

    def go_right(self):
        self.change_x = self.speed

    def stop_right(self):
        if self.change_x > 0:
            self.change_x = 0

    def face_left(self):
        if self.facing != "left":
            self.facing = "left"

    def face_right(self):
        if self.facing != "right":
            self.facing = "right"

    def jump(self):
        self.change_y = self.jump_speed