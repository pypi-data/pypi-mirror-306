import pygame as pg

class Label():
    def __init__(self, text: str, font_color: tuple|str, rect: pg.Rect, centered: bool = False) -> None:
        self.text: str = text
        self.font_color: tuple|str = font_color
        self.rect: pg.Rect = rect
        self.centered: bool = centered

    def draw(self, surface: pg.Surface, font: pg.font.Font, parent_rect: pg.Rect = None, center_text: bool = False):
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
        self.background_color: tuple|str = background_color
        self.rect: pg.Rect = rect
        self.centered: bool = centered
        self.label: Label|None = label
        self.center_text: bool = center_text
        self.auto_size: bool = auto_size
        self.action: any = action

    def draw(self, surface: pg.surface, font: pg.font.Font):
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

    def handle_action(self):
        self.action()

