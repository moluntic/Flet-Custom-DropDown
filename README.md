# Flet Custom Controls

This repository contains custom UI controls built with [Flet](https://flet.dev/) for Python.  
Each control is implemented as a reusable component to simplify building modern, interactive desktop apps.

## Features

- Easy-to-use custom controls (e.g., DropDown)
- Clean, readable code (Maybe not LOL)
- Designed for extensibility (more controls coming soon)

## Usage

Each control can be imported and used in your Flet app.  
See the code comments and examples in each file for details.

## Controls

- `DropDownV2.py` — Custom drop-down menu with overlay selection

  **Parameters:**
  - `height` (float): Height of the DropDown (default: 40)
  - `width` (float): Width of the DropDown (default: 70)
  - `text_style` (ft.TextStyle): Style for the displayed text (default: `ft.TextStyle(size=15, color='white,0.8')`)
  - `default_value` (str): Initial displayed value (default: "None")
  - `options` (list[str]): List of selectable options (default: [])
  - `on_select` (callable): Callback function called when an option is selected (default: None)
  - `max_visible` (int): Maximum number of visible options in overlay (default: 3)
  - <img width="264" height="298" alt="image" src="https://github.com/user-attachments/assets/a7842d91-d3b5-4d09-823f-b356ca4f8545" />
  - <img width="300" height="328" alt="image" src="https://github.com/user-attachments/assets/d41f5086-5a6e-4a56-b2c0-79260783b9e1" />

  **Support Features:**
    - Light/Dark Theme. 



- `MenuSwitcher.py` - Custom Switcher AKA liquid glass 

  **Parameters**
  - `labels` (list[str]): Text values to show in menu
  - `width` (int): Width of the MenuSwitcher (default: 400)
  - `on_selected` (callable): Callback function that is called after a menu item is selected.

  **Support Features:**
    - returns enum with index and label of selected item. (`EventSelect(index=0, label='Menu')`)
  
  **Example Usage:**
    ```
    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        page.add(
            MenuSwitcher(
                labels=["Menu", "App", "Settings", "Account"],
                on_selected=lambda e: print(f"Selected: {e.index} - {e.label}")
            )
        )


    ft.app(target=main)
    ```


# Contributors:
- [Moluntic](https://github.com/moluntic) - Added theme support (Light / Dark) for DropDownV2

More controls will be added in the future.
