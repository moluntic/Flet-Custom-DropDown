import asyncio
from dataclasses import dataclass
import flet as ft 


@dataclass
class EventSelect:
    index: int
    label: str


class _ButtonSwitcher(ft.GestureDetector):
    DEFAULT_COLOR_TEXT = 'white,0.5'
    PRESSED_COLOR_TEXT = 'white,1'
    def __init__(self, index: int = 0, label: str = "Menu", width:int = 100, on_click=None):
        super().__init__()
        self.index = index
        self.on_click = on_click
        self.label = label
        self.width = width
        self.content = self._content()
        self.on_tap_down = self._on_tap
        self.on_tap_up = self._on_tap_up
        self.on_exit = self._on_exit

    def _on_tap(self,e):
        self.container.opacity = 0.7
        self.container.update()
    
    def _on_tap_up(self,e):
        if self.on_click:
            self.on_click(self.index)
        self.container.opacity = 1
        self.container.update()
    
    def _on_exit(self,e):
        self.container.scale = 1
        self.container.opacity = 1
        self.container.update()

    def _content(self):
        self.text = ft.Text(
                self.label,
                color=self.DEFAULT_COLOR_TEXT,
            )
        self.container = ft.Container(
            expand=True,
            content=self.text,
            opacity=1,
            animate_opacity=ft.Animation(duration=200, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=5, right=5),
        )
        return self.container
    
    def switch_style_pressed(self):
        self.text.color = self.PRESSED_COLOR_TEXT
        self.text.update()
    
    def switch_style_normal(self):
        self.text.color = self.DEFAULT_COLOR_TEXT
        self.text.update()

class _Menus(ft.Container):
    def __init__(self, width: int = 300, labels: list[str] = [], on_click: callable = None):
        super().__init__()
        self._on_click = on_click
        self.labels = labels
        self.width = width
        self.height = 50
        self.margin = ft.margin.only(left=5)
        self.alignment = ft.alignment.center
        
        self.content = self._container()
    
    def _container(self):
        return ft.Container(
            bgcolor='white,0.1',
            height=30,
            border_radius=self.height/2,
            content=self._content()
        )

    def _content(self):
        self.row = ft.Row([
            _ButtonSwitcher(
                label=label,
                index=i,
                width=self.width / len(self.labels),
                on_click=self._on_click)
            for i, label in enumerate(self.labels)], spacing=0)
        return self.row

class LiquidContainer(ft.GestureDetector):
    def __init__(self, width: int, on_selected: callable = None):
        super().__init__()
        self.on_selected = on_selected
        self.buttons: list[_ButtonSwitcher] = []
        self.height = 50
        self.__height = 20
        self._width = width
        self.left = 0
        self._drag_start_left = None
        self._drag_start_local_x = None
        self.on_horizontal_drag_start = self._on_drag_start
        self.on_horizontal_drag_update = self._on_drag_update
        self.on_horizontal_drag_end = self._on_drag_end
        self.animate_position = ft.Animation(duration=200, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
        self._current_idx = round(self.left / self._width)
        self.content = self._container()
    
    def dragging_container(self):
        self.liquid_con.width = self._width
        self.liquid_con.height = self.__height * 2
        self.liquid_con.border.top.color = 'white,0.3'
        self.liquid_con.shadow.color = 'black,1'

    def non_dragging_container(self):
        self.liquid_con.border.top.color = 'white,0.0'
        self.liquid_con.shadow.color = 'black,0'
        self.liquid_con.update()
    
    def correct_position_size(self, idx):
        self.left = idx * self._width
        self._current_idx = idx
        if idx == 0:
            self.liquid_con.width = self._width - 10
            self.left += 10
        elif self.parent and idx == int(round(self.parent.width / self._width)) - 1:
            self.liquid_con.width = self._width - 10
        else:
            self.liquid_con.width = self._width
        self.liquid_con.height = self.__height
        self._drag_start_left = self.left
        self.non_dragging_container()

    def _on_drag_start(self, e):
        self.dragging_container()
        self.liquid_con.update()
        self._drag_start_left = self.left
        self._drag_start_local_x = e.local_x
        self._current_idx = round(self.left / self._width)
        max_idx = int(round(self.parent.width / self._width)) - 1 if self.parent else 0
        if self._current_idx == 0:
            self.left = 5
            self.update()
            self._drag_start_left = self.left
        elif self._current_idx == max_idx:
            self.left = self._current_idx * self._width - 5
            self._drag_start_left = self.left
            self.update()

    def toggle_style_button(self, index: int):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.switch_style_pressed()
            else:
                btn.switch_style_normal()

    def _on_drag_update(self, e):
        if self._drag_start_left is None or self._drag_start_local_x is None:
            return

        new_left = self._drag_start_left + (e.local_x - self._drag_start_local_x)
        if self.parent:
            max_idx = round(self.parent.width / self._width) - 1
            max_left = max_idx * self._width
        else:
            max_left = 0
        self.left = max(0, min(new_left, max_left))
        self.update()
        self.idx = round(self.left / self._width)
        self.toggle_style_button(self.idx)

    def _on_drag_end(self, e):
        self.correct_position_size(self.idx)
        self.update()
        self._selection_callback()

    def switch_to_index(self, idx: int, no_call: bool = False):
        self.idx = idx
        self.toggle_style_button(self.idx)
        self.correct_position_size(self.idx)
        self.update()
        if not no_call:
            self._selection_callback()

    def _selection_callback(self):
        if self.on_selected:
            event = EventSelect(index=self.idx, label=self.buttons[self.idx].label)
            self.on_selected(event)

    def _container(self):
        self.liquid_con = ft.Container(
            height=self.__height,
            border=ft.border.only(top=ft.BorderSide(2, 'white,0.0')),
            animate=ft.Animation(duration=200, curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
            border_radius=self.__height,
            width=self._width,
            bgcolor='white,0.1',
            shadow=ft.BoxShadow(blur_style=ft.ShadowBlurStyle.OUTER, blur_radius=30, color='black,0')
        )
        return ft.Container(
            content=self.liquid_con,
            alignment=ft.alignment.center
        )
    def did_mount(self):
        self.switch_to_index(0, True)
        return super().did_mount()

class MenuSwitcher(ft.Stack):
    def __init__(
            self, 
            labels: list[str] = ["Menu", "App", "Settings", "Account"], 
            width: int = 400,
            on_selected: callable = None
            ):
        
        super().__init__()
        self.on_selected = on_selected
        self.labels = labels
        self._width = width
        self.width = width+10
        self.height = 50
        self.controls = self._controls()
    def _controls(self):
        self.liquid = LiquidContainer(self.width/len(self.labels), on_selected=self.on_selected)
        self.menu = _Menus(labels=self.labels, on_click=self.liquid.switch_to_index, width=self._width)
        self.liquid.buttons = self.menu.row.controls

        return [
            self.menu,
            self.liquid
        ]

if __name__ == "__main__":

    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        page.add(
            MenuSwitcher(

                on_selected=lambda e: print(f"Selected: {e.index} - {e.label}")
            )
        )


    ft.app(target=main)
