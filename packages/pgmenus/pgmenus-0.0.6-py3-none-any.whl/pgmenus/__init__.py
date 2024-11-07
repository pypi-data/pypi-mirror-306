import pygame as pg

class Label():
    def __init__(self, text: str, font_color: tuple|str, rect: pg.Rect, centered: bool = False) -> None:
        self.text:          str         = text
        self.font_color:    tuple|str   = font_color
        self.rect:          pg.Rect     = rect
        self.centered:      bool        = centered


    def draw(self, surface: pg.Surface, font: pg.font.Font, parent_rect: pg.Rect = None, center_text: bool = False) -> None:
        text = font.render(
            self.text,
            True,
            self.font_color
        )
        text_rect = text.get_rect()
        if self.centered:
            text_rect.center = (
                self.rect.x,
                self.rect.y
            )
        if parent_rect:
            text_rect.x += parent_rect.x
            text_rect.y += parent_rect.y
            if center_text:
                text_rect.x += (parent_rect.width - text_rect.width) // 2
                text_rect.y += (parent_rect.height - text_rect.height) // 2
        surface.blit(text, text_rect)



class Button():
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None) -> None:
        self.background_color:  tuple|str   = background_color
        self.rect:              pg.Rect     = rect
        self.centered:          bool        = centered
        self.label:             Label|None  = label
        self.center_text:       bool        = center_text
        self.auto_size:         bool        = auto_size
        self.action:            any         = action


    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        new_rect = self.rect
        if self.auto_size:
            if self.label != None:
                text = font.render(
                    self.label.text,
                    True,
                    self.label.font_color
                )
                text_rect = text.get_rect()
                new_rect.width = text_rect.width + 10 ####

        if self.centered:
            new_rect.x -= new_rect.width//2
            new_rect.y -= new_rect.height//2
        pg.draw.rect(
            surface,
            self.background_color,
            new_rect
        )
        if self.label != None:
            self.label.draw(surface, font, self.rect, self.center_text)


    def handle_action(self) -> None:
        self.action()



class Slider():
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None) -> None:
        self.background_color:  tuple|str   = background_color
        self.rect:              pg.Rect     = rect
        self.centered:          bool        = centered
        self.label:             Label|None  = label
        self.center_text:       bool        = center_text
        self.auto_size:         bool        = auto_size
        self.action:            any         = action
        self.value:             int         = 50
        self.min_value:         int         = 0
        self.max_value:         int         = 100


    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        new_rect = self.rect
        if self.auto_size:
            if self.label != None:
                text = font.render(
                    self.label.text,
                    True,
                    self.label.font_color
                )
                text_rect = text.get_rect()
                new_rect.width = text_rect.width + 10 ####

        if self.centered:
            new_rect.x -= new_rect.width//2
            new_rect.y -= new_rect.height//2

        self.padding = 5
        # BG (Background)
        pg.draw.rect(
            surface,
            self.background_color,
            new_rect
        )
        # MG (Middleground)
        pg.draw.rect(
            surface,
            'white',
            pg.Rect(
                new_rect.x + self.padding,
                new_rect.y + self.padding,
                new_rect.width - 2 * self.padding,
                new_rect.height - 2 * self.padding
            )
        )
        # FG (Foreground) -> Handle
        pg.draw.circle(
            surface,
            self.background_color,
            (new_rect.x + new_rect.width * self.value/self.max_value, new_rect.y + new_rect.height/2),
            (new_rect.height - 2 * self.padding)/2
        )
        if self.label != None:
            self.label.draw(surface, font, self.rect, self.center_text)


    def handle_action(self) -> None:
        self.action(self.value) # send the value to the action function.


    # update value
    def update(self) -> None:
        mouse_pos = mx, my = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Mouse hovers over the slide
            relative_pos = rel_x, rel_y = mx - self.rect.x, my - self.rect.y
            value = rel_x / self.rect.width * 100 # in percentage - [0;100].
            self.value = value # set the new acquired value.
            self.handle_action()

