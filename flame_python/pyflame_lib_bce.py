"""
Script Name: PyFlame Library
Version: 4.0.0
Written by: Michael Vaglienty
Creation Date: 10.31.20
Update Date: 01.05.25

This file contains a library various custom UI widgets that can be used to build QT windows similar to the look of Flame along with some other useful functions.

This file should be placed in same folder as main script.

To avoid conflicts with having multiple copies within /opt/Autodesk/shared/python, file should be renamed to: pyflame_lib_<script name>.py

Custom QT Widgets:

    PyFlameButton - Custom QT Flame Button
    PyFlameButtonGroup - Allows for groupings of PyFlameButton types(PyFlameButton, PyFlamePushButton...).
    PyFlameEntry - Custom QT Flame Entry Field Widget. Replaces PyFlameLineEdit.
    PyFlameLabel - Custom QT Flame Label Widget.
    PyFlameLineEditFileBrowser - Custom QT Line Edit Widget. Opens Flame File Browser when clicked.
    PyFlameListWidget - Custom QT Flame List Widget.
    PyFlamePushButton - Custom QT Flame Push Button.
    PyFlamePushButtonMenu - Custom QT Flame Push Button Widget with Menu.
    PyFlameColorPushButtonMenu - Custom QT Flame Push Button with Color Menu.
    PyFlameSlider - Custom QT Flame Numerical Slider.
    PyFlameTextEdit - Custom QT Flame Text Edit Widget.
    PyFlameTokenPushButtonMenu - Custom QT Flame Push Button with Token Menu.
    PyFlameTreeWidget - Custom QT Flame Tree Widget.

Custom QT Layouts:

    PyFlameGridLayout - Custom QT Grid Layout.
    PyFlameHBoxLayout - Custom QT Horizontal Box Layout.
    PyFlameVBoxLayout - Custom QT Vertical Box Layout.

Custom QT Windows:

    PyFlamePresetManager - Preset Manager for scripts.
    PyFlameMessageWindow - Flame Message Window
    PyFlamePasswordWindow - Flame Password Window
    PyFlameProgressWindow - Flame Progress Window
    PyFlameDialogWindow - Flame QT Dialog Window
    PyFlameWindow - Flame QT Window

Utility Classes:

    PyFlameConfig - Class for creating, loading, and saving config files.

Utility Functions:

    pyflame.copy_to_clipboard - Copy text to clipboard using QT.
    pyflame.create_file_system_folders - Create a folder in the file system based on the provided folder structure.
    pyflame.create_media_panel_folders - Create a folder in the media panel based on the provided folder structure.
    pyflame.create_media_panel_libraries - Create libraries with folders in the media panel based on the provided folder structure.
    pyflame.convert_export_preset_name_to_path - Convert export preset name to path.
    pyflame.file_browser - Flame file browser or QT file browser window.
    pyflame.find_by_tag - Search through a Flame object's contained objects by tags.
    pyflame.font_resize - Resize font size for all PyFlame widgets for different screen resolutions. - Not intended to be used outside of this file.
    pyflame.generate_unique_node_names - Generate unique node names based on a list of existing node names.
    pyflame.get_export_preset_names - Get export preset names from Shared and Project paths. User paths are not checked.
    pyflame.get_export_preset_version - Get export preset version.
    pyflame.get_flame_python_packages_path - Get path to Flame python packages folder.
    pyflame.get_flame_version - Get version of Flame.
    pyflame.gui_resize - Resize PyFlame widgets for different screen resolutions. - Not intended to be used outside of this file.
    pyflame.iterate_name - Iterate through a list of names and return a unique name based on the list.
    pyflame.move_to_shot_folder - Move a clip to a shot folder in the Media Panel.
    pyflame.open_in_finder - Open path in System Finder.
    pyflame.print - Print a message to the terminal and Flame message area.
    pyflame.print_dict - Cleanly print nested dictionaries with indentation to the terminal.
    pyflame.print_json - Cleanly print JSON data to terminal with proper indentation for easy readability.
    pyflame.print_list - Print a list of items to the terminal and Flame message area.
    pyflame.refresh_hooks - Refresh Flame python hooks.
    pyflame.resolve_shot_name - Resolve shot name from string.
    pyflame.resolve_tokens - Resolve strings containing tokens.
    pyflame.set_shot_tagging - Tag Flame objects with shot name tag (ShotName: <shot_name>).
    pyflmae.shot_name_from_clip - Get shot name from clip.
    pyflame.untar - Untar a tar file.
    pyflame.update_export_preset - Update export preset version.
    pyflame.verify_script_install - Verify that script is installed in the correct location with any additional files that are required.

Usage:

    To incorporate the functionality of the file into a script, include the following line at the beginning:

        from pyflame_lib_<script name> import *

    This imports all components from the specified library, enabling direct access to its contents within your script.

    To utilize PyFlameFunctions, access them using pyflame.FUNCTION_NAME:
        pyflame.print
        pyflame.get_flame_version
        ...

    For widget usage, refer to them by their names:
        PyFlamePushButtonMenu
        PyFlamePushButton
        ...

Updates:

    v4.0.0 01.05.25

        Fixed type hinting for copy_to_clipboard function. This was causing scripts not to work with Flame 2024.

        Added new pyflame functions:
            create_media_panel_library - Create a library with folders in the media panel based on the provided folder structure.
            create_media_panel_folder - Create a single folder in the media panel based on the provided folder structure.
            create_media_panel_folders - Create folders in the media panel from a list of folder names and a folder structure.
            create_file_system_folder - Create a single folder in the file system based on the provided folder structure.
            create_file_system_folders - Create folders from a list of folder names and a folder structure.
            print - Print a message to the terminal and Flame message area. Replaces message_print function which has been deprecated.
            print_dict - Cleanly print nested dictionaries with indentation to the terminal.
            print_json - Cleanly print JSON data to terminal with proper indentation for easy readability.
            set_shot_tagging - Tag Flame objects with shot name tag (ShotName: <shot_name>).
            verify_script_install - Verify that script is installed in the correct location with any additional files that are required.
            find_by_tag - Search through a Flame object's contained objects by tags.
            shot_name_from_clip - Get shot name from clip.
            move_to_shot_folder - Move a clip to a shot folder in the Media Panel.
            get_export_preset_names - Get export preset names from Shared and Project paths. User paths are not checked.
            convert_export_preset_name_to_path - Convert export preset name to path.

        pyflame.generate_unique_node_names:
            Fixed: Would not properly generate a new name if the first character of the new name was a number.

        pyflame.resolve_tokens:
            Batch groups are now checked for a ShotName tag(ShotName:<shot_name>). If found, it is used to resolve the shot name token.

        Added new widget:
            PyFlameEntry - Replaces PyFlameLineEdit which has been deprecated.
                Added new argument:
                    align - Align entry text to left, right, or center. Default is left.

        PyFlameTextEdit:
            read-only background color now matches read-only background color of PyFlameEntry for consistency.

        PyFlameTreeWidget:
            Added new arguments:
                top_level_editable - Allow editing of name of top level items in the tree. Default is False.
                tree_list - List of items to populate the tree. Useful when dealing with batch group schematic reels shelf reels and desktop reels.
                tree_list_no_root - List of items to populate the tree excluding the root item. Useful when dealing with batch group schematic reels shelf reels and desktop reels.
                update_callback - Function to call when an item is edited, inserted, or deleted.

            Added new attributes:
                selected_item - Return the text of the currently selected item.
                item_path - Return the recursive path of the currently selected item.
                item_paths - Return the recursive paths of the currently selected items.
                all_item_paths - Return the recursive paths of all items in the PyFlameTreeWidget.

        PyFlameGridLayout:
            Added the ability to set the number of columns and rows in the grid to make it easier to place widgets especially where space is desired between widgets.
            By default the unit size of the grid is 150px wide and 28px high. The size of a normal button. The width and height of each grid unit along with the
            number of columns and rows can be adjusted using setGridSize method.

            Added new arguments:
                columns - Set number of columns in the grid. Default is 0.
                rows - Set number of rows in the grid. Default is 0.
                column_width - Set width of each column in the grid. Default is 150.
                row_height - Set height of each row in the grid. Default is 28.
                adjust_column_widths - Set width of specific columns in the grid. Default is {}.
                adjust_row_heights - Set height of specific rows in the grid. Default is {}.

            Removed the following arguments:
                setMinimumColumnWidth - No longer needed.
                setMinimumRowHeight - No longer needed.

            Added new method:
                setGridSize - Configure the grid layout dimensions and cell sizes. This method allows you to:
                    - Set the number of columns and rows in the grid
                    - Define the width of each column (in pixels)
                    - Define the height of each row (in pixels)
                    - Automatically adjust spacing between grid cells

                    This makes it easier to create precise layouts, especially when you need consistent spacing
                    between widgets or want to reserve empty cells in your grid.

        PyFlameWindow/PyFlameDialogWindow
            Simplified window creation by adding PyFlameGridLayout to the window by default with optional
            arguments to set the number of columns and rows along with column and row widths. This can
            be overridden by passing grid_layout=False.

            Added new arguments:
                tab_width - Set the width of tab name label
                tab_height - Set the height of the tab name label
                grid_layout - Set to True to use the default grid layout. Default is True.
                grid_layout_columns - Set the number of columns in the grid layout. Default is 4.
                grid_layout_rows - Set the number of rows in the grid layout. Default is 3.
                grid_layout_column_width - Set the width of each column in the grid layout. Default is 150.
                grid_layout_row_height - Set the height of each row in the grid layout. Default is 28.
                grid_layout_adjust_column_widths - Set the width of specific columns in the grid layout. Default is {}.
                grid_layout_adjust_row_heights - Set the height of specific rows in the grid layout. Default is {}.

        PyFlameMessageWindow:
            Updated message printing to terminal to be more clear.
            Message text no longer uses html tags such as <b> or <br>. Text is now printed as plain text.

        PyFlameProgressWindow:
            Updated message printing to terminal to be more clear.

        Deprecated pyflame functions:
            message_print - Use pyflame.print instead.
            resolve_path_tokens - Use pyflame.resolve_tokens instead.

        Deprecated widgets:
            PyFlameLineEdit - Use PyFlameEntry instead.
            PyFlameLabel.Style.BACKGROUND - Use PyFlameEntry with read_only=True instead.

        Miscellaneous:
            max_width argument is now set to True by default for all widgets. width and height are
            now bypassed. This means the widgets will now expand to fill the available space. The
            size of the widgets is now determined by the layout(PyFlameGridLayout, PyFlameHBoxLayout,
            PyFlameVBoxLayout). To override this behavior, set max_width to False and set width and height
            arguments to set the size of the widget.

            max_height argument is now set to True by default on the following widgets. The above behavior for
            max_width applies to max_height.
                PyFlameListWidget
                PyFlameTreeWidget
                PyFlameTextEdit


    v3.2.0 09.09.24

        Added new pyflame functions:
            json_print - Cleanly print JSON data to terminal with proper indentation for easy readability.

    v3.1.0 09.01.24

        PyFlameMessageWindow - Added scrollbars to message window for long messages.

        Added new pyflame functions:
            print_list - Print a list of items to the terminal and Flame message area.
            print - Print a message to the terminal and Flame message area.

    v3.0.0 08.16.24

        Added new PyFlameFunction:
            copy_to_clipboard - Copy text to clipboard using QT.

        Added new Utility Class:
            _WindowResolution - Utility class to determine the main window resolution based on the Qt version.
            Fixes conflicts with Shotgrid Toolkit and Flame 2025. Thanks to Ari Brown for this fix.

        PyFlameConfig:
            Config file is now saved as a JSON file. Values no longer need to be converted to strings before saving as before. Values are saved as their original data types.

        Message/Password/Progress Windows:
            Message text is now set to plain text format. HTML tags are no longer supported. Text appears as typed.
            Added line wrap to message window text. Text will wrap to next line if it exceeds the window width.

        PyFlameTreeWidget:
            Fixed font size issue in linux.
            When sorting is enabled, sorting is done in ascending order of items in column 0.

        PyFlameProgressBar Window:
            Done button is now enabled once progress is complete. No need to manually set it to enabled.

    v2.5.0 06.22.24

        Improvements to docstrings to enhance hover over tooltips in IDEs.

        Updated PyFlameTreeWidget:
            Added new attributes:
                tree_list - Get a list of all item names in the tree. (Converted this to an attribute from a method)
                tree_dict - Get a dictionary of all items in the tree.

    v2.4.0 06.12.24

        Updated PyFlameTreeWidget:
            Added new methods:
                fill_tree: Fill the tree widget with the provided dictionary.
                add_item: Add a new item as a child of the currently selected item in the tree,
                delete_item: Delete the selected item in the tree.
                sort_items: Sort all items in the tree while maintaining the structure and keeping the tree expanded.
                tree_list: Get a list of all item names in the tree.

        Added new pyflame function:
            iterate_name - Iterate through a list of names and return a unique name based on the list.

    v2.3.0 05.07.24

        Added new class:
            PyFlameButtonGroup - Allows for grouping of PyFlameButtons, PyFlamePushButtons, PyFlamePushButtonMenus, and PyFlameColorPushButtonMenus.
                                 By default set_exclusive is set to True. This means only one button in the group can be selected at a time.

        Added new pyflame function:
            generate_unique_node_names - Generate unique node names based on a list of existing node names.

    v2.2.0 05.05.24

        Added new class:
            PyFlamePresetManager - This class allows for saving/editing/deleting of presets for scritps. Presets can be assigned to specific projects or be global.

        Added constants for script name(SCRIPT_NAME), script path(SCRIPT_PATH). These are used as default values for script_name and script_path arguments in all classes and functions.
        Both constants are derived from the pyflame_lib file path and file name.

        Updated all classes and functions that have parameters for script_name and script_path. They now use SCRIPT_NAME constant for script name and SCRIPT_PATH
        constant for script path as default values if not passed as arguments.

    v2.1.16 04.29.24

        Added BatchGroupName token to resolve_path_tokens function. A PyBatch object must be passed as the flame_pyobject argument.

        PyFlameDialogWindow - Updated window layout to fix alignment issues with lines.

    v2.1.15 04.23.24

        PyFlameLineEdit: Added argument for setting tooltip text.

    v2.1.14 04.16.24

        PyFlameConfig: Added new method: get_config_values. This method returns the values of a config file at the supplied path as a dictionary.

    v2.1.13 04.01.24

        PyFlameConfig: Config file is now saved if it doesn't exist when loading the default config values.

    v2.1.12 03.08.24

        PyFlamePushButtonMenu: Added new argument: enabled - enabled or disable button state. Default is True.

        PyFlamePushButton: Added new argument: enabled - enabled or disable button state. Default is True.

    v2.1.11 03.03.24

        PyFlameTokenPushButtonMenu: Fixed menu sizing to be consistent with other menus.

        PyFlamePushButtonMenu: Menu text is now left aligned.

    v2.1.10 02.29.24

        Added new layout classes:
            PyFlameGridLayout
            PyFlameHBoxLayout
            PyFlameVBoxLayout

            These classes adjust values for margins, spacing, and minimum size for the layout using pyflame.gui_resize method
            so the layout looks consistent across different screen resolutions. Removes need to use pyflame.gui_resize inside
            of main script.

        Added new class:
            PyFlameColorPushButtonMenu - Push Button Menu with color options. Returns selected color as a tuple of normalized RGB values.

        Added arguments to turn off/on menu indicators for PyFlamePushButtonMenu and PyFlameColorPushButtonMenu. Default is off.

        Improved argument validations for all widgets.

    v2.1.9 02.17.24

        Fixed all widget tooltip text color. Color is now set to white instead of red.

        Fixed all widget tooltip border. Is now set to 1px solid black.

    v2.1.8 02.11.24

        Improvements to UI/code for PyFlameMessage, PyFlameProgress, and PyFlamePassword windows.

    v2.1.7 02.09.24

        Fixed: Config values not printing in terminal when loading config file.

        Added parameter to pyflame.get_flame_python_packages_path to enable/disable printing path to terminal.
        Default is True.

    v2.1.6 01.31.24

        Fixed PySide6 errors/font in slider calculator.

        Added new class: PyFlameLineEditFileBrowser - Line Edit widget that opens a flame file browser when clicked.

        PyFlameLineEdit: Added read_only parameter. This will make the line edit read only and unselectable with dark background. Default is False.

        PyFlameSlider: Added rate parameter. This controls the sensitivity of the slider. The value should be between 1 and 10.
        1 is the most sensitive and 10 is the least sensitive. Default is 10.

    v2.1.5 01.25.24

        Updated PyFlameTokenPushButton:
            Added default argument values:
                text='Add Token'
                token_dict={}
                token_dest=None
            Added new method:
                add_menu_options(new_options): Add new menu options to the existing token menu and clear old options.

    v2.1.4 01.21.24

        Updated PySide.
        Improved UI scaling for different screen resolutions.
        Fixed issue with PyFlameConfig not properly returning boolean values.

    v2.1.3 11.21.23

        Updated pyflame.get_export_preset_version() to check default jpeg export preset for preset version.
        This function no longer needs to be updated manually.

    v2.1.2 11.17.23

        Updated Token Push Button Menu widget. Added ability to clean destination(line edit widget) before adding the token.

    v2.1.1 11.06.23

        Added pyflame functions for dealing with export preset versions:
            pyflame.get_export_preset_version()
            pyflame.update_export_preset()

    v2.1.0 08.14.23

        All widgets have been updated to be more consistent.

        All widgets have been changed from Flame to PyFlame.
        For example: FlamePushButtonMenu -> PyFlamePushButtonMenu
        Widgets should be left in this file and not moved individually
        to other files. This will cause problems since some widgets rely
        on other widgets/functions in this file.

        Widget documentation has been improved.
"""

#---------------------------------------------
# [Imports]
#---------------------------------------------

import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from enum import Enum
from functools import partial
from subprocess import PIPE, Popen
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import flame

#--------------------------------------------
# [PySide Imports]
#--------------------------------------------

# Try to import PySide6, otherwise import PySide2

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtGui import QAction
    using_pyside6 = True
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
    QAction = QtWidgets.QAction
    using_pyside6 = False

#---------------------------------------------
# [Constants]
#---------------------------------------------

# Get script name from file name. Removes 'pyflame_lib_' and '.py' from file name.
SCRIPT_PATH = os.path.abspath(__file__).rsplit('/', 1)[0]
SCRIPT_NAME = os.path.basename(__file__)[12:-3].replace('_', ' ').title()

PYFLAME_FONT = 'Discreet' # Font used in all PyFlame UI elements
PYFLAME_FONT_SIZE = 13 # Default font size used in all PyFlame UI elements

SHARED_FILE_SEQUENCE_PATH = '/opt/Autodesk/shared/export/presets/file_sequence'
SHARED_MOVIE_EXPORT_PATH = '/opt/Autodesk/shared/export/presets/movie_file'
PROJECT_FILE_SEQUENCE_PATH = ''
PROJECT_MOVIE_EXPORT_PATH = ''

#---------------------------------------------
# [PyFlame Enums]
#---------------------------------------------
# For internal script use only.
# Not meant to be used outside of this file.
#---------------------------------------------

class Color(Enum):
    """
    Color
    ======

    Enum for storing color values used in the PyFlame UI elements. This class helps in maintaining a consistent
    color scheme throughout the application, making it easy to change colors in a centralized manner.

    Each color is represented as an RGB value string, which can be used to style different elements
    in the application, such as text, buttons, borders, and backgrounds.

    Examples
    --------
        To set a button background color:
        ```
        button.setStyleSheet(f'background-color: {Color.GRAY.value};')
        ```

        To set a text color for a label:
        ```
        label.setStyleSheet(f'color: {Color.TEXT.value};')
        ```
    """

    BLUE = 'rgb(0, 110, 175)'
    RED = 'rgb(200, 29, 29)'
    GRAY = 'rgb(58, 58, 58)'
    BLACK = 'rgb(0, 0, 0)'
    WHITE = 'rgb(255, 255, 255)'

    TEXT = 'rgb(154, 154, 154)'
    TEXT_BRIGHT = 'rgb(185, 185, 185)'
    TEXT_SELECTED = 'rgb(210, 210, 210)'
    TEXT_DISABLED = 'rgb(116, 116, 116)'
    TEXT_UNDERLINE = 'rgb(40, 40, 40)'
    TEXT_BORDER = 'rgb(64, 64, 64)'
    TEXT_READ_ONLY_BACKGROUND = 'rgb(30, 30, 30)'

    BUTTON_TEXT = 'rgb(165, 165, 165)'
    SELECTED_GRAY = 'rgb(71, 71, 71)'

    BORDER = 'rgb(90, 90, 90)'
    BORDER_BRIGHTER = 'rgb(120, 120, 120)'

    UNDERLINE = 'rgb(40, 40, 40, 1)'

    ENTRY_GRAY = 'rgb(54, 54, 54)'

    DISABLED_GRAY = 'rgb(54, 54, 54)'

    # List and Tree Widget Colors
    ITEM_BACKGROUND_COLOR = 'rgb(30, 30, 30)'
    ITEM_ALT_BACKGROUND_COLOR = 'rgb(36, 36, 36)'

    # Push Button Colors
    PUSHBUTTON_BLUE = 'rgb(44, 54, 68)'
    PUSHBUTTON_BLUE_CHECKED = 'rgb(50, 101, 173)'
    PUSHBUTTON_BLUE_DISABLED = 'rgb(50, 50, 50)'

    TAB_PANE = 'rgb(49, 49, 49)'

    SCROLLBAR_HANDLE = 'rgb(49, 49, 49)'

class TextColor(Enum):
    """
    TextColor
    =========

    Color options for text being printed to the terminal.

    Attributes:
    -----------
        GREEN (str):
            Green text.

        YELLOW (str):
            Yellow text.

        RED (str):
            Red text.

        WHITE (str):
            White text.

        BLUE (str):
            Blue text.

        RESET (str):
            Reset text color to default.
    """

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BLUE = '\033[38;2;0;120;215m'
    RESET = '\033[0m'

    def format(self, text: str) -> str:
        """
        Formats the given text with the Enum's color.

        Args:
            text (str): The text to format.

        Returns:
            str: The formatted text with ANSI color codes.
        """
        return f"{self.value}{text}{TextColor.RESET.value}"

class Style(Enum):
    """
    Style
    =====

    Enum for PyFlameLabel style options.

    Attributes:
    -----------
        NORMAL (str):
            Standard label without any additional styling. Text is left aligned by default.

        UNDERLINE (str):
            Text is underlined. Text is centered by default.

        BACKGROUND (str):
            Adds a darker background to the label. Text is left aligned by default.

        BORDER (str):
            Adds a white border around the label with a dark background. Text is centered by default.
    """

    NORMAL = 'normal'
    UNDERLINE = 'underline'
    BACKGROUND = 'background'
    BORDER = 'border'

class Align(Enum):
    """
    Align
    =====

    Enum for text alignment.

    Attributes:
    -----------
        LEFT (str):
            Align text to the left.

        RIGHT (str):
            Align text to the right.

        CENTER (str):
            Align text to the center.
    """

    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'

class MessageType(Enum):
    """
    MessageType
    ===========

    Enum for PyFlameMessageWindows types.

    Attributes:
    -----------
        INFO (str):
            Information message type.

        OPERATION_COMPLETE (str):
            Operation complete message type.

        CONFIRM (str):
            Confirmation message type.

        ERROR (str):
            Error message type.

        WARNING (str):
            Warning message type.
    """

    INFO = 'Info'
    OPERATION_COMPLETE = 'Operation Complete'
    CONFIRM = 'Confirm'
    ERROR = 'Error'
    WARNING = 'Warning'

class PrintType(Enum):
    """
    MessageType
    ===========

    Enum for pyflame.print types.

    Attributes:
    -----------
        INFO (str):
            Information type.

        ERROR (str):
            Error type.

        WARNING (str):
            Warning type.
    """

    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'

class LineColor(Enum):
    """
    LineColor
    =========

    Enum for PyFlameWindow side bar color options.

    Attributes:
    -----------
        GRAY (str):
            Gray line.

        GRAY_TRANS (str):
            Gray line with 25% transparency.

        BLUE (str):
            Blue line.

        BLUE_TRANS (str):
            Blue line with 25% transparency.

        RED (str):
            Red line.

        RED_TRANS (str):
            Red line with 25% transparency.

        GREEN (str):
            Green line.

        GREEN_TRANS (str):
            Green line with 25% transparency.
    """

    # Gray
    GRAY = QtGui.QColor(71, 71, 71)  # Gray (fully opaque)
    GRAY_TRANS = QtGui.QColor(71, 71, 71, 64)  # Gray with 25% transparency (alpha=64)

    # Blue
    BLUE = QtGui.QColor(0, 110, 175)  # Blue (fully opaque)
    BLUE_TRANS = QtGui.QColor(0, 110, 176, 64)  # Blue with 25% transparency (alpha=64)

    # Yellow
    YELLOW = QtGui.QColor(251, 181, 73)  # Yellow (fully opaque)
    YELLOW_TRANS = QtGui.QColor(251, 181, 73, 64)  # Yellow with 25% transparency (alpha=64)

    # Red
    RED = QtGui.QColor(200, 29, 29)  # Red (fully opaque)
    RED_TRANS = QtGui.QColor(200, 29, 29, 64)  # Red with 25% transparency (alpha=64)

    # Green
    GREEN = QtGui.QColor(0, 180, 13) # Green (fully opaque)
    GREEN_TRANS = QtGui.QColor(0, 180, 13, 64) # Green with 25% transparency (alpha=64)

    # Teal
    TEAL = QtGui.QColor(14, 110, 106) # Teal (fully opaque)
    TEAL_TRANS = QtGui.QColor(14, 110, 106, 64) # Teal with 25% transparency (alpha=64)

class BrowserType(Enum):
    """
    BrowserType
    ===========

    Enum for PyFlameLineEditFileBrowser browser type options.

    Attributes:
    -----------
        FILE (str):
            File browser.

        DIRECTORY (str):
            Directory browser.
    """

    FILE = 'file'
    DIRECTORY = 'directory'

#-------------------------------------
# [Utility Classes]
#-------------------------------------

class _WindowResolution():
    """
    Window Resolution
    =================

    Utility class to determine the main window resolution based on the Qt version.
    It checks the major version of the QtCore module and uses the appropriate method
    to obtain the main window resolution. Fixes issues when using QT with Shotgrid
    in Flame 2025. Thanks to Ari Brown for this fix.
    """

    @staticmethod
    def main_window():
        """
        Get the main window resolution based on the Qt version.

        Returns:

            main_window_res : QDesktopWidget or QScreen
                The main window resolution object. The type depends on the Qt version:
                    - QtWidgets.QDesktopWidget for Qt versions less than 6
                    - QtGui.QGuiApplication.primaryScreen for Qt versions 6 and above
        """

        if QtCore.__version_info__[0] < 6:
            main_window_res = QtWidgets.QDesktopWidget()
        else:
            main_window_res = QtGui.QGuiApplication.primaryScreen()
        return main_window_res

pyflamewin = _WindowResolution()

#-------------------------------------
# [PyFlame Functions]
#-------------------------------------

class _PyFlameFunctions():
    """
    PyFlameFunctions
    ================

    A class containing various useful functions.

    Methods that can be accessed using:
        ```
        pyflame.method_name
        ```

    Example
    -------
        To print a message using the `print` method:
        ```
        pyflame.print(
            text='Config not found.',
            type=PrintType.ERROR
            )
        ```
    """

    @staticmethod
    def verify_script_install(additional_files: list=None) -> bool:
        """
        Verify Script Install
        =====================

        Verify that script is installed in the correct location.

        Scripts should always be installed in a folder with the same name as the script file.

        Checks to make sure the script folder is named the same as the main script file, that the
        script folder is writable, and that the script folder contains the required additional
        files if any are specified.

        Args:
        -----
            `additional_files` (list):
                List of additional files to check for in the script folder. These are other files
                that are required for the script to work. This should only be a list of file names,
                not full paths. If file is in a subfolder of the script folder, it should include
                the subfolder name. For example, if the script folder is named 'srt_to_xml' and the
                file 'xml_template.xml' is in the 'templates' subfolder, the file name should be
                'templates/xml_template.xml'.

        Returns:
        --------
            bool: True if script is installed in correct location and not missing any additional files, False if not.

        Raises:
        -------
            TypeError:
                If `additional_files` is not a list.

        Example:
        --------
            To check if script is installed in proper location along with additional files:
            ```
            verify_install = pyflame.verify_script_install(
                additional_files=[
                    'xml_template.xml',
                    'xml_title_template.xml',
                    'text_node_template.ttg',
                    ]
                )

            print(verify_install)
            ```
        """

        # Validate arguments
        if additional_files and not isinstance(additional_files, list):
            raise TypeError(f"pyflame.verify_script_install: Expected 'additional_files' to be a list, got {type(additional_files).__name__} instead.")

        pyflame.print('Verifying Script Install', new_line=False)
        print('------------------------\n')

        # Get script path info
        script_path = os.path.abspath(os.path.dirname(__file__))
        root_path = os.path.dirname(script_path)
        script_folder_name = script_path.rsplit('/', 1)[1]
        script_file_name = os.path.basename(__file__)[12:-3]

        print('Script Path:', script_path)
        print('Root Path:', root_path)
        print('Script Folder Name:', script_folder_name)
        print('Script File Name:', script_file_name + '.py\n')

        # Check if script folder name matches script file name
        if not script_folder_name == script_file_name:
            PyFlameMessageWindow(
                message=(
                    f'Script install path is incorrect: \n\n'
                    f'    {script_path} \n\n'
                    f'The name of the script folder should match the name of the main script file. \n\n'
                    f'Script install path should be:\n\n'
                    f'    {os.path.join(root_path, script_file_name)}'
                    ),
                type=MessageType.ERROR
                )
            return False

        # Check script folder for write permissions
        if not os.access(script_path, os.W_OK):
            PyFlameMessageWindow(
                message=(
                    'Script folder is not writable. \n\n'
                    'Please check permissions and try again.'
                    ),
                type=MessageType.ERROR
                )
            return False

        # Check for additional files needed for script to work
        if additional_files:
            pyflame.print('Checking For Additional Files:')
            for file in additional_files:
                if not os.path.isfile(os.path.join(script_path, file)):
                    PyFlameMessageWindow(
                        message=(
                            f'File not found: \n\n'
                            f'    {file}\n\n'
                            f'Please check that the file is in the correct location and try again.'
                            ),
                        type=MessageType.ERROR
                        )
                    return False
                else:
                    pyflame.print(f'{file} -> Found', text_color=TextColor.GREEN, new_line=False)
            print('\n', end='')

        print('------------------------\n')

        pyflame.print('Script Install Verified', text_color=TextColor.GREEN)
        return True

    @staticmethod
    def create_media_panel_libraries(library_structure: dict[str, Any]) -> None:
        """
        Create Media Panel Library
        ==========================

        Create libraries/folders in the media panel based on the provided library/folder structure.

        Tokens can be used in library/folder names.

        Args:
        -----
            `library_structure` (dict):
                A dictionary representing the library/folder structure to be created.
                'Workspace' should always be the top level key.

        Raises:
        -------
            TypeError:
                If `library_structure` is not a dictionary.
            ValueError:
                If 'Workspace' is not the only top-level key in `library_structure`.

        Example:
        --------
            To create a library with folders in the media panel:
            ```
            library_structure = {
                'Workspace': {
                    'Library1': {
                        'Folder1': {
                            'SubFolder1': {},
                            'SubFolder2': {}
                            },
                        'Folder2': {}
                        },
                    'Library2': {
                        'Folder1': {
                            'SubFolder1': {},
                            'SubFolder2': {}
                            },
                        'Folder2': {}
                        }
                    }
                }

            pyflame.create_media_panel_libraries(library_structure)
            ```
        """

        # Validate argument type
        if not isinstance(library_structure, dict):
            raise TypeError(f"pyflame.create_media_panel_libraries: Expected 'library_structure' to be a dict, got {type(library_structure).__name__} instead.")
        # Validate that 'Workspace' is the only top-level key
        if set(library_structure.keys()) != {'Workspace'}:
            raise ValueError("pyflame.create_media_panel_libraries: 'library_structure' must have 'Workspace' as its only top-level key.")

        pyflame.print('Creating Media Panel Libraries and Folders...')
        pyflame.print('Library Structure:', underline=True, print_to_flame=False)
        pyflame.print_dict(library_structure)

        # Create new libraries and folders
        def create_folders(folder_structure, folder_dest):

            for key, value in folder_structure.items():
                key = pyflame.resolve_tokens(key) # Resolve tokens in folder name
                folder = folder_dest.create_folder(key)
                create_folders(value, folder)

        for key, value in library_structure.items():
            for library, folder_structure in value.items():
                new_library_name = pyflame.resolve_tokens(library) # Resolve tokens in library name
                new_library = flame.project.current_project.current_workspace.create_library(new_library_name)
                create_folders(folder_structure, new_library)

        pyflame.print('Media Panel Libraries and Folders Created', arrow=True)

    @staticmethod
    def create_media_panel_folder(folder_name: str, folder_structure: dict[str, Any], dest: Union[flame.PyFolder, flame.PyLibrary], shot_name_tag: str=None) -> None:
        """
        Create Media Panel Folder
        =========================

        Create a folder in the media panel based on the provided folder structure. Tokens can be used in folder names.

        By default folders are tagged with the shot name token.

        Args:
        -----
            `folder_name` (str):
                Name of the main folder to create in the media panel.

            `folder_structure` (dict):
                A dictionary representing the folder structure to be created.

            `dest` (Folder):
                The destination folder/library in the Media Panel where the main folder will be created.

            `shot_name_tag` (str):
                Use to add ShotName tag to folder with matching name. If shot_name_tag is PYT_0010 any folder named PYT_0010 will be tagged with 'ShotName: PYT_0010'.
                (Default: `None`)

        Raises:
        -------
            TypeError:
                If `folder_name` is not a string.
                If `folder_structure` is not a dictionary.
                If `dest` is not a flame.PyFolder or flame.PyLibrary.
                If `shot_name_tag` is not a string.

        Example:
        --------
            To create media panel folders:
            ```
            folder_structure = {
                'Folder1': {
                    'SubFolder1': {},
                    'SubFolder2': {
                        'SubSubFolder1': {}
                    }
                },
                'Folder2': {}
            }

            pyflame.create_media_panel_folder(
                folder_name='Shot001',
                folder_structure=folder_structure,
                dest=flame.project.current_project.current_workspace,
                shot_name_tag='Shot0010',
                )
            ```
        """

        # Validate arguments
        if not isinstance(folder_name, str):
            raise TypeError(f"pyflame.create_media_panel_folder: Expected 'folder_name' to be a str, got {type(folder_name).__name__} instead.")
        if not isinstance(folder_structure, dict):
            raise TypeError(f"pyflame.create_media_panel_folder: Expected 'folder_structure' to be a dict, got {type(folder_structure).__name__} instead.")
        if not isinstance(dest, (flame.PyFolder, flame.PyLibrary)):
            raise TypeError(f"pyflame.create_media_panel_folder: Expected 'dest' to be a flame.PyFolder or flame.PyLibrary, got {type(dest).__name__} instead.")
        if shot_name_tag != None and not isinstance(shot_name_tag, str):
            raise TypeError(f"pyflame.create_media_panel_folder: Expected 'shot_name_tag' to be None or a str, got {type(shot_name_tag).__name__} instead.")

        def create_sub_folders(folders, parent_folder):
            """
            Create Sub-Folders
            ==================

            Recursively create sub-folders based on the provided folder structure.

            Args:
            -----
                `folder_structure` (dict):
                    A dictionary representing the folder structure to be created.

                `parent_folder` (Folder):
                    The parent folder where the sub-folders will be created.
            """

            for key, value in folders.items():
                key = pyflame.resolve_tokens(key) # Resolve tokens in folder name
                new_folder = parent_folder.create_folder(key)
                if shot_name_tag and new_folder.name == shot_name_tag:
                    new_folder.tags=[f'ShotName: {shot_name_tag}']
                create_sub_folders(value, new_folder)

        pyflame.print('Creating Media Panel Folder...')
        pyflame.print('Folder Structure:', underline=True, print_to_flame=False)
        pyflame.print_dict(folder_structure)

        # Create the main shot folder
        folder_name = pyflame.resolve_tokens(folder_name) # Resolve tokens in folder name
        root_folder = dest.create_folder(folder_name)

        # Tag root folder with shot name if shot_name_tag is provided and folder_name matches shot_name_tag
        if shot_name_tag and folder_name == shot_name_tag:
            root_folder.tags=[f'ShotName: {shot_name_tag}']

        # Create sub-folders under the shot folder based on the settings
        for folders in folder_structure.values():
            create_sub_folders(folders, root_folder)

        pyflame.print(f'Media Panel Folder Created: {folder_name}', arrow=True)

    @staticmethod
    def create_media_panel_folders(folder_list: list[str], folder_structure: dict[str, Any], dest: Union[flame.PyFolder, flame.PyLibrary]) -> None:
        """
        Create Media Panel Folders
        ==========================

        Create folders in the Media Panel from a list of folder names. Tokens can be used in folder names.

        Args:
        -----
            `folder_list` (list[str]):
                List of folder names to create.

            `folder_structure` (dict):
                Dictionary representing the folder structure to create.

            `dest` (Folder):
                The destination folder/library in the Media Panel where the folders will be created.

        Raises:
        -------
            TypeError:
                If `folder_list` is not a list.
                If `folder_structure` is not a dictionary.
                If `dest` is not a flame.PyFolder or flame.PyLibrary.

        Notes:
        ------
            Tokens can be used in folder names.

            Uses _PyFlameFunctions.create_media_panel_folder() to create each folder in list.

        Example:
        --------
            To create media panel folders:
            ```
            folder_list = [
                'PYT_0010',
                'PYT_0020',
                'PYT_0030',
                'PYT_0040',
                ]

            folder_structure = {
                'Folder1': {
                    'SubFolder1': {},
                    'SubFolder2': {}
                },
                'Folder2': {}
            }

            pyflame.create_media_panel_folders(
                folder_list=folder_list,
                folder_structure=folder_structure,
                dest=flame.project.current_project.current_workspace,
                )
            ```
        """

        # Validate arguments
        if not isinstance(folder_list, list):
            raise TypeError(f"pyflame.create_media_panel_folders: Expected 'folder_list' to be a list, got {type(folder_list).__name__} instead.")
        if not isinstance(folder_structure, dict):
            raise TypeError(f"pyflame.create_media_panel_folders: Expected 'folder_structure' to be a dict, got {type(folder_structure).__name__} instead.")
        if not isinstance(dest, (flame.PyFolder, flame.PyLibrary)):
            raise TypeError(f"pyflame.create_media_panel_folders: Expected 'dest' to be a flame.PyFolder or flame.PyLibrary, got {type(dest).__name__} instead.")

        pyflame.print('Creating Media Panel Folders...')
        pyflame.print('Folder Structure:', underline=True, print_to_flame=False, text_color=TextColor.BLUE)
        pyflame.print_dict(folder_structure)

        for folder_name in folder_list:
            _PyFlameFunctions.create_media_panel_folder(folder_name, folder_structure, dest, folder_name)

    @staticmethod
    def create_file_system_folder(folder_name: str, folder_structure: dict[str, Any], dest_path: str, skip_existing: bool=False) -> None:
        """
        Create File System Folder
        =========================

        Create a folder in the file system based on the provided folder structure. Tokens can be used in folder names.

        Args:
        -----
            `folder_name` (str):
                Name of the main folder to create.

            `folder_structure` (dict):
                Dictionary representing the folder structure to create.

            `dest_path` (str):
                Path where folders will be created.

            `skip_existing` (bool):
                Skip creating folders if they already exist.

        Raises:
        -------
            TypeError:
                If `folder_name` is not a string.
                If `folder_structure` is not a dictionary.
                If `dest_path` is not a string.
                If `skip_existing` is not a boolean.

        Example:
        --------
            To create a file system folder:
            ```
            folder_structure = {
                'Folder1': {
                    'SubFolder1': {},
                    'SubFolder2': {
                        'SubSubFolder1': {}
                    }
                },
                'Folder2': {}
            }

            pyflame.create_file_system_folder(
                folder_name='Shot001',
                folder_structure=folder_structure,
                dest_path='/path/to/dest/folder',
                skip_existing=False
                )
            ```

            The above example will create the following folder structure:
            ```
            /path/to/dest/folder/Shot001/Folder1/SubFolder1
            /path/to/dest/folder/Shot001/Folder1/SubFolder2/SubSubFolder1
            /path/to/dest/folder/Shot001/Folder2
            ```
        """

        def create_sub_folders(value: dict, parent_folder: str) -> None:
            """
            Create Sub-Folders
            ==================

            Recursively create sub-folders based on the provided folder structure.

            Args:
            -----
                `value` (dict):
                    Nested dictionary representing folder structure.

                `parent_folder` (str):
                    The parent folder where the sub-folders will be created.
            """

            for key, value in value.items():
                key = pyflame.resolve_tokens(key) # Resolve tokens in folder name
                folder = os.path.join(parent_folder, key)
                try:
                    os.makedirs(folder, exist_ok=True)
                except OSError as e:
                    print(f"Error creating directory {folder}: {e}")
                create_sub_folders(value, folder)

        #Validate arguments
        if not isinstance(folder_name, str):
            raise TypeError(f"pyflame.create_file_system_folder: Expected 'folder_name' to be a str, got {type(folder_name).__name__} instead.")
        if not isinstance(folder_structure, dict):
            raise TypeError(f"pyflame.create_file_system_folder: Expected 'folder_structure' to be a dict, got {type(folder_structure).__name__} instead.")
        if not isinstance(dest_path, str):
            raise TypeError(f"pyflame.create_file_system_folder: Expected 'dest_path' to be a str, got {type(dest_path).__name__} instead.")
        if not isinstance(skip_existing, bool):
            raise TypeError(f"pyflame.create_file_system_folder: Expected 'skip_existing' to be a bool, got {type(skip_existing).__name__} instead.")

        # Create folders
        for key, value in folder_structure.items():
            folder_name = pyflame.resolve_tokens(folder_name) # Resolve tokens in folder name
            parent_folder = os.path.join(dest_path, folder_name)
            if not os.path.isdir(parent_folder) or not skip_existing:
                try:
                    os.makedirs(parent_folder, exist_ok=True)
                    pyflame.print(
                        text=f'Creating File System Folders For: {folder_name}',
                        new_line=False,
                        text_color=TextColor.GREEN,
                        )
                except OSError as e:
                    print(f"Error creating directory {parent_folder}: {e}")
                create_sub_folders(value, parent_folder)
            else:
                pyflame.print(
                    text=f'File system folder: {folder_name} already exists, skipping.',
                    new_line=False,
                    )

        # Refresh Media Panel
        flame.execute_shortcut("Refresh the MediaHub's Folders and Files")

    @staticmethod
    def create_file_system_folders(folder_list: list[str], folder_structure: dict[str, Any], dest_path: str) -> None:
        """
        Create File System Folders
        ==========================

        Create file system folders for a list of folders. Tokens can be used in folder names.

        Args:
        -----
            `folder_list` (list[str]):
                List of folder names to create.

            `folder_structure` (dict):
                Dictionary representing the folder structure to create.

            `dest_path` (str):
                Path where folders will be created.

        Raises:
        -------
            TypeError:
                If `folder_list` is not a list.
                If `folder_structure` is not a dictionary.
                If `dest_path` is not a string.

        Notes:
        ------
            Tokens can be used in folder names.

            Uses _PyFlameFunctions.create_file_system_folder() to create each folder in list.

        Example:
        --------
            To create file system folders:
            ```
            folder_structure = {
                'Folder1': {
                    'SubFolder1': {},
                    'SubFolder2': {
                        'SubSubFolder1': {}
                    }
                },
                'Folder2': {}
            }

            folder_list = [
                'PYT_0010',
                'PYT_0020',
                'PYT_0030',
                'PYT_0040',
                ]

            pyflame.create_file_system_folders(
                folder_list=folder_list,
                folder_structure=folder_structure,
                dest_path='/path/to/dest/folder',
                )
            ```

            The above example will create the following folder structure:
            ```
            /dest/folder/path/PYT_0010/Folder1/SubFolder1
            /dest/folder/path/PYT_0010/Folder1/SubFolder2/SubSubFolder1
            /dest/folder/path/PYT_0010/Folder2
            /dest/folder/path/PYT_0020/Folder1/SubFolder1
            /dest/folder/path/PYT_0020/Folder1/SubFolder2/SubSubFolder1
            /dest/folder/path/PYT_0020/Folder2
            /dest/folder/path/PYT_0030/Folder1/SubFolder1
            /dest/folder/path/PYT_0030/Folder1/SubFolder2/SubSubFolder1
            /dest/folder/path/PYT_0030/Folder2
            /dest/folder/path/PYT_0040/Folder1/SubFolder1
            /dest/folder/path/PYT_0040/Folder1/SubFolder2/SubSubFolder1
            /dest/folder/path/PYT_0040/Folder2
            ```
        """

        # Validate arguments
        if not isinstance(folder_list, list):
            raise TypeError(f"pyflame.create_file_system_folders: Expected 'folder_list' to be a list, got {type(folder_list).__name__} instead.")
        if not isinstance(folder_structure, dict):
            raise TypeError(f"pyflame.create_file_system_folders: Expected 'folder_structure' to be a dict, got {type(folder_structure).__name__} instead.")
        if not isinstance(dest_path, str):
            raise TypeError(f"pyflame.create_file_system_folders: Expected 'dest_path' to be a str, got {type(dest_path).__name__} instead.")

        pyflame.print('Creating File System Folders', text_color=TextColor.GREEN)
        pyflame.print('Folder Structure:', underline=True, print_to_flame=False, text_color=TextColor.BLUE)
        pyflame.print_dict(folder_structure)

        for folder_name in folder_list:
            _PyFlameFunctions.create_file_system_folder(folder_name, folder_structure, dest_path)

    @staticmethod
    def copy_to_clipboard(value: Union[str, int]) -> None:
        """
        Copy to Clipboard
        =================

        Copy string(text) to clipboard using QT.

        Args:
        -----
            `value` (str | int):
                Text or integer to copy to clipboard.

        Raises:
        -------
            TypeError:
                If `value` is not a string or integer.

        Example:
        --------
            To copy text to clipboard:
            ```
            pyflame.copy_to_clipboard('Text to copy to clipboard.')
            ```
            To copy an integer to clipboard:
            ```
            pyflame.copy_to_clipboard(12345)
            ```
        """

        # Validate argument type
        if not isinstance(value, str | int):
            raise TypeError(f"pyflame.copy_to_clipboard: Expected 'value' to be a string or int, got {type(value).__name__} instead.")

        # Convert value to string if it is an integer
        if isinstance(value, int):
            value = str(value)

        # Copy path to clipboard
        qt_app_instance = QtWidgets.QApplication.instance()
        qt_app_instance.clipboard().setText(value)

        pyflame.print(f'Value copied to clipboard: {value}')

    @staticmethod
    def print(text: str, indent: int=0, print_type=PrintType.INFO, new_line: bool=True, arrow: bool=False, underline: bool=False, double_underline: bool=False, text_color: TextColor=None, time: int=3, print_to_flame: bool=True, script_name: str=SCRIPT_NAME) -> None:
        """
        Print
        =====

        Print text to the terminal and Flame message area.

        Args:
        -----
            `text` (str):
                Text to print.

            `indent` (int):
                Indent text in terminal by the specified amount of spaces.
                (Default: `0`)

            `print_type` (PrintType):
                See print types below.
                (Default: `PrintType.INFO`)

            `new_line` (bool):
                Print a new line after text.
                (Default: `True`)

            `arrow` (bool):
                Add an arrow `--> ` to the start of the text. Also sets text color to green.
                (Default: `False`)

            `underline` (bool):
                Add an underline to the text. A line of dashes will be printed below the text.
                (Default: `False`)

            `double_underline` (bool):
                Add a double underline to the text. Equals sign will be printed below the text.
                (Default: `False`)

            `text_color` (TextColor):
                Text color to print text in terminal. Overrides print_type color. See text colors below.
                (Default: `None`)

            `time` (int):
                Amount of time to display text in Flame for in seconds.
                (Default: `3`)

            `print_to_flame` (bool):
                Print message to Flame message area.
                (Default: `True`)

            `script_name` (str):
                Name of script. This is displayed in the Flame message area.
                (Default: `SCRIPT_NAME`)

        Print Types:
        --------------
        - `PrintType.INFO`: Prints text in default color.
        - `PrintType.ERROR`: Printed text will be yellow.
        - `PrintType.WARNING`: Printed text will be red.

        Text Color:
        ------------
        - `TextColor.GREEN`: Green text.
        - `TextColor.YELLOW`: Yellow text.
        - `TextColor.RED`: Red text.
        - `TextColor.WHITE`: White text.
        - `TextColor.BLUE`: Blue text.
        - `TextColor.RESET`: Reset text color to default.

        Raises:
        -------
        TypeError:
            If `text` is not a string.
            If `indent` is not an integer.
            If `new_line`, `arrow`, `underline`, or `double_underline` is not a boolean.
            If `time` is not an integer.
            If `script_name` is not a string.
            If `text_color` is not a TextColor.
        ValueError:
            If `type` is not a valid PrintType.

        Example:
        --------
            To print some text:
            ```
            pyflame.print('This is some text.')
            ```

            To print indented text:
            ```
            pyflame.print('This is some indented text.', indent=True)
            ```
        """

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f"pyflame.print: Expected 'text' to be a string, got {type(text).__name__} instead.")
        if not isinstance(indent, int):
            raise TypeError(f"pyflame.print: Expected 'indent' to be a int, got {type(indent).__name__} instead.")
        if not isinstance(new_line, bool):
            raise TypeError(f"pyflame.print: Expected 'new_line' to be a boolean, got {type(new_line).__name__} instead.")
        if not isinstance(arrow, bool):
            raise TypeError(f"pyflame.print: Expected 'arrow' to be a boolean, got {type(arrow).__name__} instead.")
        if not isinstance(underline, bool):
            raise TypeError(f"pyflame.print: Expected 'underline' to be a boolean, got {type(underline).__name__} instead.")
        if not isinstance(double_underline, bool):
            raise TypeError(f"pyflame.print: Expected 'double_underline' to be a boolean, got {type(double_underline).__name__} instead.")
        if not isinstance(time, int):
            raise TypeError(f"pyflame.print: Expected 'time' to be an integer, got {type(time).__name__} instead.")
        if not isinstance(script_name, str):
            raise TypeError(f"pyflame.print: Expected 'script_name' to be a string, got {type(script_name).__name__} instead.")
        valid_message_types = (PrintType.INFO, PrintType.ERROR, PrintType.WARNING)
        if print_type not in valid_message_types:
            raise ValueError(f"pyflame.print:  Expected 'print_type' to be one of: PrintType.INFO, PrintType.ERROR, PrintType.WARNING. Got: {type(print_type).__name__} instead.")
        if text_color and not isinstance(text_color, TextColor):
            raise TypeError(f"pyflame.print: Expected 'text_color' to be a TextColor(TextColor.GREEN, TextColor.YELLOW, TextColor.RED, TextColor.WHITE, TextColor.BLUE, TextColor.RESET.), got {type(text_color).__name__} instead.")

        original_text = text
        text_length = len(text)

        # Add arrow to text if specified
        if arrow:
            text = f'--> {text}'
            text_color = TextColor.GREEN

        # Add indentation to text if specified
        if indent:
            text = f'{" " * indent}{text}'

        # Add text color to text if specified
        if text_color:
            text = text_color.format(text) # Print message with specified text_color and indentation
            color = text_color.value
        elif print_type == PrintType.INFO:
            text = text # Print message text normally
            color = ''
        elif print_type == PrintType.ERROR:
            text = f'{TextColor.YELLOW.value}{text}{TextColor.RESET.value}' # Print message text in yellow
            color = TextColor.YELLOW.value
        elif print_type == PrintType.WARNING:
            text = f'{TextColor.RED.value}{text}{TextColor.RESET.value}' # Print message text in red
            color = TextColor.RED.value

        print(text) # Print message text to terminal with specified color

        if underline:
            print(f'{color}{"-" * text_length}{TextColor.RESET.value}') # Print underline
        if double_underline:
            print(f'{color}{"=" * text_length}{TextColor.RESET.value}') # Print double underline
        if new_line:
            print('\n', end='')

        # Print to Flame Message Window - Flame 2023.1 and later
        # Warning and error intentionally swapped to match color of message window
        if print_to_flame:
            try:
                if print_type == PrintType.INFO:
                    flame.messages.show_in_console(f'{script_name}: {original_text}', 'info', time)
                elif print_type == PrintType.ERROR:
                    flame.messages.show_in_console(f'{script_name}: {original_text}', 'warning', time)
                elif print_type == PrintType.WARNING:
                    flame.messages.show_in_console(f'{script_name}: {original_text}', 'error', time)
            except:
                pass

    @staticmethod
    def print_dict(dict_data: dict[str, Any], indent: int=0) -> None:
        """
        Print Dict
        ==========

        Cleanly prints nested dictionaries with indentation to the terminal.

        Args:
        -----
            `dict_data` (dict):
                Dictionary to print.

            `indent` (int):
                Indentation level.
                (Default: `0`)

        Raises:
        -------
            TypeError:
                If `dict_data` is not a dictionary.
                If `indent` is not an integer.

        Example:
        --------
            To print a nested dictionary:
            ```
            dictionary = {
                'Key1': {
                    'SubKey1': 'Value1',
                    'SubKey2': 'Value2'
                    },
                'Key2': {
                    'SubKey1': 'Value1',
                    'SubKey2': 'Value2'
                    }
                }

            pyflame.print_dict(
                data_dict=dictionary,
                indent=0,
                )
            ```

            Output:
            ```
            Key1
                SubKey1: Value1
                SubKey2: Value2
            Key2
                SubKey1: Value1
                SubKey2: Value2
            ```
        """

        # Validate argument type
        if not isinstance(dict_data, dict):
            raise TypeError(f"pyflame.print_dict: Expected 'dict_data' to be a dict, got {type(dict_data).__name__} instead.")
        if not isinstance(indent, int):
            raise TypeError(f"pyflame.print_dict: Expected 'indent' to be an int, got {type(indent).__name__} instead.")

        def print_to_terminal(dict_data: dict[str, Any], indent: int) -> None:

            # Print dictionary data
            for key, value in dict_data.items():
                print('  ' * indent + str(key))
                if isinstance(value, dict) and value:
                    print_to_terminal(
                        dict_data=value,
                        indent=indent+1,
                        )

        print_to_terminal(dict_data, indent)

        print('\n', end='')

    @staticmethod
    def print_json(json_data, indent=0) -> None:
        """
        Print JSON
        ==========

        Cleanly print JSON data to terminal with proper indentation.

        Args:
        -----
            `json_data` (dict | list | str | int | bool):
                JSON data to print.

            `indent` (int):
                Indentation level.
                (Default: `0`)

        Raises:
        -------
            TypeError:
                If `indent` is not an integer.

        Example:
        --------
            ```
            pyflame.print_json(
                json_data=config.json,
                )
            ```
        """

        def print_to_terminal(json_data, indent):

            spacing = ' ' * indent

            # Check if the current data is a dictionary
            if isinstance(json_data, dict):
                # If "script_name" is present, print it first
                if "script_name" in json_data and indent == 0:
                    print(f"{spacing}script_name: {json_data['script_name']}")

                # Now print the rest of the dictionary except "script_name"
                for key, value in json_data.items():
                    if key == "script_name":
                        continue  # Skip "script_name" as it has already been printed

                    if isinstance(value, dict) and not value:
                        print(f"{spacing}{key}")  # Print the key without a colon if the value is an empty dict
                    else:
                        print(f"{spacing}{key}: ", end="")
                        if isinstance(value, (dict, list)):
                            print()  # Add a new line for nested structures
                            print_to_terminal(value, indent + original_indent)  # Recursive call
                        else:
                            print(value)  # Print the value immediately without an extra new line


            # If it's a list, iterate through the list items
            elif isinstance(json_data, list):
                for item in json_data:
                    print_to_terminal(item, indent + original_indent)  # Recursive call

            # Handle boolean values
            elif isinstance(json_data, bool):
                print(f"{'true' if json_data else 'false'}")

            # Handle any other data type (e.g., strings, numbers)
            else:
                print(f"{spacing}{json_data}")

        # Validate argument type
        if not isinstance(indent, int):
            raise TypeError(f"pyflame.print_json: Expected 'indent' to be an int, got {type(indent).__name__} instead.")

        original_indent = indent  # Store the original indent level

        print_to_terminal(json_data, indent)

        print()  # Ensure a single new line after all the data is printed

    @staticmethod
    def print_list(list_name: str, list_items: list, indent=0, time: int=3, script_name: str=SCRIPT_NAME) -> None:
        """
        Print List
        ===========

        Print a list of items to the terminal and Flame message area.

        Args:
        -----
            `list_name` (str):
                Name of the list.

            `list_items` (list):
                List of items to print.

            `indent` (int, optional):
                Indent message in terminal by specified amount of spaces.
                (Default: `0`)

            `time` (int, optional):
                Amount of time to display message in Flame for in seconds.
                (Default: `3`)

            `script_name` (str, optional):
                Name of script. This is displayed in the Flame message area.
                (Default: `SCRIPT_NAME`)

        Raises:
        -------
            TypeError:
                If `list_name` is not a string.
                If `list_items` is not a list.
                If any item in `list_items` is not a string.
                If `indent` is not an integer.
                If `time` is not an integer.
                If `script_name` is not a string.

            ValueError:
                If `list_items` is not a list of strings.

        Example:
        --------
            To print a list of items:
            ```
            pyflame.print_list(
                list_name='List of Items',
                list_items=[
                    'Item1',
                    'Item2',
                    'Item3'
                    ]
                )
            ```
        """

        # Validate argument types
        if not isinstance(list_name, str):
            raise TypeError(f"pyflame.print_list: Expected 'text' to be a string, got {type(list_name).__name__} instead.")
        if not isinstance(list_items, list):
            raise TypeError(f"pyflame.print_list: Expected 'list_items' to be a list, got {type(list_items).__name__} instead.")
        if not all(isinstance(item, str) for item in list_items):
            raise ValueError(f"pyflame.print_list: Expected all items in 'list_items' to be strings.")
        if not isinstance(indent, int):
            raise TypeError(f"pyflame.print_list: Expected 'indent' to be a integer, got {type(indent).__name__} instead.")
        if not isinstance(time, int):
            raise TypeError(f"pyflame.print_list: Expected 'time' to be an integer, got {type(time).__name__} instead.")
        if not isinstance(script_name, str):
            raise TypeError(f"pyflame.print_list: Expected 'script_name' to be a string, got {type(script_name).__name__} instead.")

        # Print list name to terminal
        print(f'{list_name}:')
        print('-' * (len(list_name)+1))
        print('\n', end='')

        # Print list name to Flame message area
        flame.messages.show_in_console(f'{script_name}: {list_name}:', 'info', 3)

        # Print list to terminal, indenting each item by 4 spaces if indent is True
        for item in list_items:
            print(f'{" " * indent}{item}')
        print('\n', end='')
        print('-' * (len(list_name)+1)) # Print a line of dashes after the list
        print('\n', end='')

        # Print list items to Flame message area. List items are not indented in the Flame message area.
        for item in list_items:
            flame.messages.show_in_console(f'{script_name}: {item}', 'info', 3)

    @staticmethod
    def message_print(message: str, type=MessageType.INFO, script_name: str=SCRIPT_NAME, time: int=3, ) -> None:
        """
        Message Print
        =============

        **Deprecated** Use `pyflame.print` instead.

        Prints messages to terminal and Flame message area(2023.1+).

        Args:
        -----
            message (str):
                Message to print.

            type (MessageType):
                Type of message. See message types below.
                (Default: `MessageType.INFO`)

            script_name (str):
                Name of script. This is displayed in the Flame message area.
                (Default: `SCRIPT_NAME`)

            time (int):
                Amount of time to display message for in seconds.
                (Default: `3`)

        Message Types:
        --------------
        - `MessageType.INFO`: Standard message.
        - `MessageType.ERROR`: Error message. Text in terminal will be yellow.
        - `MessageType.WARNING`: Warning message. Text in terminal will be red.

        Example:
        --------
            To print an error message:
            ```
            pyflame.message_print(
                message='Config not found.',
                type=MessageType.ERROR,
                )
            ```
        """

        script_name = script_name.upper()

        # Validate arguments
        if not isinstance(message, str):
            raise TypeError(f'PyFlame message_print: Invalid message type: {message}. message must be of type str.')
        if not isinstance(script_name, str):
            raise TypeError(f'Pyflame message_print: Invalid script_name type: {script_name}. script_name must be of type str.')
        valid_message_types = {MessageType.INFO, MessageType.ERROR, MessageType.WARNING}
        if type not in valid_message_types:
            raise ValueError(f'PyFlame message_print: Invalid message type: {type}. Accepted types: MessageType.INFO, MessageType.ERROR, MessageType.WARNING.')
        if not isinstance(time, int):
            raise TypeError(f'Pyflame message_print: Invalid time type. time must be of type int.')

        print(f'\033[91m--> DeprecationWarning: pyflame.message_print: Use pyflame.print instead.\033[0m\n') # Print message text in red

        # Print to terminal/shell
        if type == MessageType.INFO:
            print(f'--> {message}\n') # Print message text normally
        elif type == MessageType.ERROR:
            print(f'\033[93m--> {message}\033[0m\n') # Print message text in yellow
        elif type == MessageType.WARNING:
            print(f'\033[91m--> {message}\033[0m\n') # Print message text in red

        script_name = script_name.upper()

        # Print to Flame Message Window - Flame 2023.1 and later
        # Warning and error intentionally swapped to match color of message window
        try:
            if type == MessageType.INFO:
                flame.messages.show_in_console(f'{script_name}: {message}', 'info', time)
            elif type == MessageType.ERROR:
                flame.messages.show_in_console(f'{script_name}: {message}', 'warning', time)
            elif type == MessageType.WARNING:
                flame.messages.show_in_console(f'{script_name}: {message}', 'error', time)
        except:
            pass

    @staticmethod
    def generate_unique_node_names(node_names: list[str], existing_node_names: list[str]) -> list[str]:
        """
        Generate Unique Node Names
        ==========================

        Generate unique node names based on the provided list of node names, ensuring that each new node
        name does not conflict with names in a given list of existing node names. If a conflict is found,
        the function appends an incrementing number to the original name until a unique name is created.

        Args:
        -----
            `node_names` (list[str]):
                List of node names that need to be checked and possibly modified to ensure uniqueness.

            `existing_node_names` (list[str]):
                List of already existing node names against which the new node names will be checked for uniqueness.

        Returns:
        --------
            list[str]:
                A list of new unique node names. Each name in this list is guaranteed to be unique against the provided list of existing node names.

        Raises:
        -------
            TypeError:
                If `node_names` is not a list.
                If `existing_node_names` is not a list.
            ValueError:
                If any element in `node_names` is not a string.
                If any element in `existing_node_names` is not a string.

        Example:
        --------
            To generate unique node names for a list of nodes:
            ```
            generate_unique_node_names(
                node_names=[
                    'Node1',
                    'Node2',
                    'Node3'
                    ],
                existing_node_names=[
                    'Node7',
                    'Node2',
                    'Node4',
                    ]
                )
            ```
        """

        # Validate arguments types
        if not isinstance(node_names, list):
            raise TypeError(f"pyflame.generate_unique_node_names: Expected 'node_names' to be a list, got {type(node_names).__name__} instead.")
        if not all(isinstance(name, str) for name in node_names):
            raise ValueError(f'pyflame.generate_unique_node_names: All elements in node_names list must be strings.')
        if not isinstance(existing_node_names, list):
            raise TypeError(f"pyflame.generate_unique_node_names: Expected 'existing_node_names' to be a list, got {type(existing_node_names).__name__} instead.")
        if not all(isinstance(name, str) for name in existing_node_names):
            raise ValueError(f'pyflame.generate_unique_node_names: All elements in existing_node_names list must be strings.')

        # Check node names for uniqueness
        new_node_names = []
        for name in node_names:
            # If name starts with a number, add a '_' to the name
            if name[0].isdigit():
                name = f'_{name}'
            original_name = name
            i = 1
            # Keep appending a number to the name until it's unique
            while name in existing_node_names:
                name = f"{original_name}{i}"
                i += 1

            # Add the unique name to the list
            new_node_names.append(name)
            existing_node_names.append(name)

        return new_node_names

    @staticmethod
    def get_flame_version() -> float:
        """
        Get Flame Version
        =================

        Gets version of flame and returns float value.

        Returns:
        --------
            `flame_version` (float): 2022.0
                2022 -> 2022.0
                2022.1.1 -> 2022.1
                2022.1.pr145 -> 2022.1

        Example:
        --------
            To get the version of Flame:
            ```
            flame_version = pyflame.get_flame_version()
            ```
        """

        flame_version = flame.get_version()

        if 'pr' in flame_version:
            flame_version = flame_version.rsplit('.pr', 1)[0]
        if len(flame_version) > 6:
            flame_version = flame_version[:6]
        flame_version = float(flame_version)

        print('Flame Version:', flame_version, '\n')

        return flame_version

    @staticmethod
    def get_flame_python_packages_path(print_path: bool=True) -> str:
        """
        Get Flame Python Packages Path
        ===============================

        Get path to Flame's python packages folder.

        Args:
        -----
            `print_path` (bool):
                Print path to terminal.
                (Default: `True`)

        Returns:
        --------
            `python_packages_path` (str):
                Path to Flame's python packages folder.

        Raises:
        -------
            FileNotFoundError:
                If no python3.* folder is found in the python lib path.

        Example:
        --------
            To get the path to Flame's python packages folder:
            ```
            python_packages_path = pyflame.pyflame_get_flame_python_packages_path()
            ```
        """

        # Validate argument types
        if not isinstance(print_path, bool):
            raise TypeError(f"pyflame.get_flame_python_packages_path: Expected 'print_path' to be a bool, got {type(print_path).__name__} instead.")

        flame_version = flame.get_version() # Get flame version

        python_lib_path = f'/opt/Autodesk/python/{flame_version}/lib' # Path to Flame's python lib folder

        # Find the folder in the python lib path that starts with 'python3.'
        for folder in os.listdir(python_lib_path):
            if folder.startswith('python3.'):
                python_package_folder = os.path.join(python_lib_path, folder, 'site-packages')
                if print_path:
                    print('Flame Python Packages Folder:', python_package_folder, '\n')
                return python_package_folder

        raise FileNotFoundError('No python3.* folder found in the python lib path.')

    @staticmethod
    def file_browser(path: str='/opt/Autodesk', title: Optional[str]=None, extension: Optional[List[str]]=None, select_directory: bool=False, multi_selection: bool=False, include_resolution: bool=False, use_flame_browser: bool=True, window_to_hide: Optional[List[QtWidgets.QWidget]]=None) -> Optional[Union[str, list]]:
        """
        File Browser
        ============

        Opens Flame's file browser(Flame 2023.1+) or QT file browser window(Flame 2022 - Flame 2023).

        Args:
        -----
            `path` (str):
                Open file browser to this path.
                (Default: `'/opt/Autodesk'`)

            `title` (str):
                File browser window title.
                (Default: `None`)

            `extension` (list):
                File extension filter. None to list directories.
                (Default: `None`)

            `select_directory` (bool):
                Ability to select directories.
                (Default: `False`)

            `multi_selection` (bool):
                Ability to select multiple files/folders.
                (Default: `False`)

            `include_resolution` (bool):
                Enable resolution controls in flame browser.
                (Default: `False`)

            `use_flame_browser` (bool):
                Use Flame's file browser if using Flame 2023.1 or later.
                (Default: `True`)

            `window_to_hide` (list[QtWidgets.QWidget]):
                Hide Qt window while Flame file browser window is open. Window is restored when browser is closed.
                (Default: `None`)

        Returns:
        --------
            `path` (str, list):
                Path to selected file or directory. When `multi_selection` is enabled, the file browser will return a list. Otherwise it will return a string.

        Example:
        --------
            To open a file browser:
            ```
            path = pyflame_file_browser(
                path=self.undistort_map_path,
                title='Load Undistort ST Map(EXR)',
                extension=['exr'],
                )
            ```
        """

        # Check argument values
        if not isinstance(path, str):
            raise TypeError(f'Pyflame file_browser: Invalid path type: {path}. path must be of type str.')
        if title is not None and not isinstance(title, str):
            raise TypeError(f'Pyflame file_browser: Invalid title type: {title}. title must be of type str or None.')
        if extension is not None and not isinstance(extension, list):
            raise TypeError(f'Pyflame file_browser: Invalid extension type: {extension}. extension must be of type list or None.')
        if not isinstance(select_directory, bool):
            raise TypeError(f'Pyflame file_browser: Invalid select_directory type: {select_directory}. select_directory must be of type bool.')
        if not isinstance(multi_selection, bool):
            raise TypeError(f'Pyflame file_browser: Invalid multi_selection type: {multi_selection}. multi_selection must be of type bool.')
        if not isinstance(include_resolution, bool):
            raise TypeError(f'Pyflame file_browser: Invalid include_resolution type: {include_resolution}. include_resolution must be of type bool.')
        if not isinstance(use_flame_browser, bool):
            raise TypeError(f'Pyflame file_browser: Invalid use_flame_browser type: {use_flame_browser}. use_flame_browser must be of type bool.')
        if window_to_hide is not None and not isinstance(window_to_hide, list):
            raise TypeError(f'Pyflame file_browser: Invalid window_to_hide type: {window_to_hide}. window_to_hide must be of type list or None.')

        if not title and not extension:
            title = 'Select Directory'
        elif not title and extension:
            title = 'Select File'

        # Clean up path
        while os.path.isdir(path) is not True:
            path = path.rsplit('/', 1)[0]
            if '/' not in path and not os.path.isdir(path):
                path = '/opt/Autodesk'
            print('Browser path:', path, '\n')

        # Open file browser
        if pyflame.get_flame_version() >= 2023.1 and use_flame_browser:

            # Hide Qt window while browser is open
            if window_to_hide:
                for window in window_to_hide:
                    window.hide()

            # Open Flame file browser
            flame.browser.show(
                title=title,
                extension=extension,
                default_path=path,
                select_directory=select_directory,
                multi_selection=multi_selection,
                include_resolution=include_resolution
                )

            # Restore Qt windows
            if window_to_hide:
                for window in window_to_hide:
                    window.show()

            # Return file path(s) from Flame file browser
            if flame.browser.selection:
                if multi_selection:
                    return flame.browser.selection
                return flame.browser.selection[0]
        else:
            browser = QtWidgets.QFileDialog()
            browser.setDirectory(path)

            if select_directory or not extension:
                browser.setFileMode(QtWidgets.QFileDialog.Directory)
            else:
                browser.setFileMode(QtWidgets.QFileDialog.ExistingFile)
                filter_str = ';;'.join(f'*.{ext}' for ext in extension)
                browser.setNameFilter(filter_str)

                browser.selectNameFilter(filter_str)

            if browser.exec_():
                return str(browser.selectedFiles()[0])

            print('\n--> Import cancelled \n')
            return

    @staticmethod
    def open_in_finder(path: str) -> None:
        """
        Open in Finder
        ==============

        Open path in System Finder.

        Args:
        -----
            `path` (str):
                Path to open in Finder.
        """

        # Validate argument types
        if not isinstance(path, str):
            raise TypeError(f"pyflame.open_in_finder: Expected 'open_in_finder' to be a string, got {type(open_in_finder).__name__} instead.")

        if not os.path.exists(path):
            pyflame.print(
                text=f'Path does not exist: {path}',
                type=MessageType.ERROR,
            )
            return

        # Open path in Finder or File Explorer
        if platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

        pyflame.print(f'Opening path in Finder: {path}')

    @staticmethod
    def refresh_hooks(script_name: str=SCRIPT_NAME) -> None:
        """
        Refresh Hooks
        =============

        Refresh python hooks and print message to terminal and Flame message window.

        Args:
        -----
            `script_name` (str):
                Name of script. This is displayed in the Flame message area.
                (Default: `SCRIPT_NAME`)

        Raises:
        -------
            TypeError:
                If `script_name` is not a string.

        Example:
        --------
            To refresh python hooks:
            ```
            pyflame.refresh_hooks()
            ```
        """

        # Validate argument type
        if not isinstance(script_name, str):
            raise TypeError(f"pyflame.refresh_hooks: Expected 'script_name' to be a string, got {type(script_name).__name__} instead.")

        flame.execute_shortcut('Rescan Python Hooks') # Refresh python hooks

        print('=' * 80)
        pyflame.print('Python Hooks Refreshed', new_line=False)
        print('=' * 80 + '\n')

    @staticmethod
    def resolve_path_tokens(tokenized_path: str, flame_pyobject=None, date=None) -> str:
        """
        Resolve Path Tokens
        ===================

        Resolves paths with tokens.

        **Deprecated** Use `pyflame.resolve_tokens` instead.
        """

        print('\033[91m--> DeprecationWarning - pyflame.resolve_path_tokens - use pyflame.resolve_tokens instead.\033[0m\n')

        return pyflame.resolve_tokens(tokenized_path, flame_pyobject, date) # Resolve path tokens

    @staticmethod
    def resolve_tokens(tokenized_string: str, flame_pyobject=None, date=None) -> str:
        """
        Resolve Path Tokens
        ===================

        Resolves strings containing tokens.

        Args:
        -----
            `tokenized_string` (str):
                String with tokens to be translated.

            `flame_pyobject` (flame.PyClip, optional):
                Flame PyClip/PySegment/PyBatch Object.
                (Default: `None`)

            `date` (datetime, optional):
                Date/time to use for token translation. If None is passed datetime value will be gotten each time function is run.
                (Default: `None`)

        Supported tokens:
        -----------------
            <ProjectName>, <ProjectNickName>, <UserName>, <UserNickName>, <YYYY>, <YY>, <MM>, <DD>, <Hour>, <Minute>, <AMPM>, <ampm>

            Additional tokens available when Flame PyObjects as passed in the flame_pyobject argument:
                PyClip and PySegment:
                    <ShotName>, <SeqName>, <SEQNAME>, <ClipName>, <Resolution>, <ClipHeight>, <ClipWidth>, <TapeName>
                PyBatch:
                    <BatchGroupName>, <ShotName>, <SeqName>, <SEQNAME>

        Returns:
        --------
            `resolved_string` (str):
                String with resolved tokens.

        Raises:
        -------
            TypeError:
                If `tokenized_string` is not a string.

        Example:
        --------
            To resolve path tokens:
            ```
            export_path = pyflame.translate_path_tokens(
                tokenized_string=custom_export_path,
                flame_pyobject=clip,
                date=date
                )
            ```
        """

        # Validate argument types
        if not isinstance(tokenized_string, str):
            raise TypeError(f"pyflame.resolve_tokens: Expected 'tokenized_string' to be a string, got {type(tokenized_string).__name__} instead.")

        def get_seq_name(name):
            """
            Get sequence name abreviation from shot name
            """

            seq_name = re.split('[^a-zA-Z]', name)[0]
            return seq_name

        pyflame.print('Resolving Tokens', new_line=False)
        print('----------------')


        print('Checking for tokens in string:', tokenized_string)

        # Check if string has tokens
        if not re.search(r'<.*?>', tokenized_string):
            pyflame.print(f'No tokens found in string: {tokenized_string}')
            return tokenized_string
        else:
            pyflame.print(f'Tokens found in string, resolving...')

        # Get time values for token conversion
        if not date:
            date = datetime.datetime.now()

        yyyy = date.strftime('%Y')
        yy = date.strftime('%y')
        mm = date.strftime('%m')
        dd = date.strftime('%d')
        hour = date.strftime('%I')
        if hour.startswith('0'):
            hour = hour[1:]
        minute = date.strftime('%M')
        ampm_caps = date.strftime('%p')
        ampm = str(date.strftime('%p')).lower()

        # Replace tokens in path
        resolved_path = re.sub('<ProjectName>', flame.project.current_project.name, tokenized_string)
        resolved_path = re.sub('<ProjectNickName>', flame.project.current_project.nickname, resolved_path)
        resolved_path = re.sub('<UserName>', flame.users.current_user.name, resolved_path)
        resolved_path = re.sub('<UserNickName>', flame.users.current_user.nickname, resolved_path)
        resolved_path = re.sub('<YYYY>', yyyy, resolved_path)
        resolved_path = re.sub('<YY>', yy, resolved_path)
        resolved_path = re.sub('<MM>', mm, resolved_path)
        resolved_path = re.sub('<DD>', dd, resolved_path)
        resolved_path = re.sub('<Hour>', hour, resolved_path)
        resolved_path = re.sub('<Minute>', minute, resolved_path)
        resolved_path = re.sub('<AMPM>', ampm_caps, resolved_path)
        resolved_path = re.sub('<ampm>', ampm, resolved_path)

        # Get Batch Group Name - Only works when a PyBatch object is passed as the flame_pyobject argument.
        if '<BatchGroupName>' in tokenized_string and isinstance(flame_pyobject, flame.PyBatch):
            resolved_path = re.sub('<BatchGroupName>', str(flame_pyobject.name)[1:-1], resolved_path)

        # Resolve tokens for flame pyobjects
        if flame_pyobject:
            if isinstance(flame_pyobject, flame.PyClip):

                def resolve_clip_tokens(clip, resolved_path: str) -> str:
                    """
                    Resolve Clip Tokens
                    ===================
                    """

                    clip_name = str(clip.name)[1:-1] # Get clip name

                    # Get shot name from clip
                    try:
                        if clip.versions[0].tracks[0].segments[0].shot_name != '':
                            shot_name = str(clip.versions[0].tracks[0].segments[0].shot_name)[1:-1]
                        else:
                            shot_name = pyflame.resolve_shot_name(clip_name)
                    except:
                        shot_name = ''

                    # Get tape name from clip
                    try:
                        tape_name = str(clip.versions[0].tracks[0].segments[0].tape_name) # Get tape name
                    except:
                        tape_name = ''

                    seq_name = get_seq_name(shot_name) # Get Seq Name from shot name

                    # Replace clip tokens in path
                    resolved_path = re.sub('<ShotName>', shot_name, resolved_path)
                    resolved_path = re.sub('<SeqName>', seq_name, resolved_path)
                    resolved_path = re.sub('<SEQNAME>', seq_name.upper(), resolved_path)
                    resolved_path = re.sub('<ClipName>', str(clip.name)[1:-1], resolved_path)
                    resolved_path = re.sub('<Resolution>', str(clip.width) + 'x' + str(clip.height), resolved_path)
                    resolved_path = re.sub('<ClipHeight>', str(clip.height), resolved_path)
                    resolved_path = re.sub('<ClipWidth>', str(clip.width), resolved_path)
                    resolved_path = re.sub('<TapeName>', tape_name, resolved_path)

                    return resolved_path

                resolved_path = resolve_clip_tokens(flame_pyobject, resolved_path)

            elif isinstance(flame_pyobject, flame.PySegment):

                def resolve_segment_tokens(segment, resolved_path: str) -> str:
                    """
                    Resolve Segment Tokens
                    ======================

                    Args:
                    -----
                        `segment` (flame.PySegment):
                            Flame PySegment object.

                        `resolved_path` (str):
                            Resolved path with tokens.

                    Returns:
                    --------
                        `resolved_path` (str):
                            Resolved path with tokens.
                    """

                    segment_name = str(segment.name)[1:-1]

                    # Get shot name from clip
                    try:
                        if segment.shot_name != '':
                            shot_name = str(segment.shot_name)[1:-1]
                        else:
                            shot_name = pyflame.resolve_shot_name(segment_name)
                    except:
                        shot_name = ''

                    # Get tape name from segment
                    try:
                        tape_name = str(segment.tape_name)
                    except:
                        tape_name = ''

                    seq_name = get_seq_name(shot_name) # Get Seq Name from shot name

                    # Replace segment tokens in path
                    resolved_path = re.sub('<ShotName>', shot_name, resolved_path)
                    resolved_path = re.sub('<SeqName>', seq_name, resolved_path)
                    resolved_path = re.sub('<SEQNAME>', seq_name.upper(), resolved_path)
                    resolved_path = re.sub('<ClipName>', segment_name, resolved_path)
                    resolved_path = re.sub('<Resolution>', 'Unable to Resolve', resolved_path)
                    resolved_path = re.sub('<ClipHeight>', 'Unable to Resolve', resolved_path)
                    resolved_path = re.sub('<ClipWidth>', 'Unable to Resolve', resolved_path)
                    resolved_path = re.sub('<TapeName>', tape_name, resolved_path)

                    return resolved_path

                resolved_path = resolve_segment_tokens(flame_pyobject, resolved_path)

            elif isinstance(flame_pyobject, flame.PyBatch):

                def resolve_batch_tokens(batch, resolved_path: str) -> str:
                    """
                    Resolve Batch Tokens
                    ====================

                    Batch is checked for a ShotName tag(ShotName:<shot_name>). If found, it is used to resolve the shot name token.
                    Otherwise, any Render nodes in the batch are checked for a shot name. If a shot name is found, it is used to resolve the shot name token.
                    If no shot name is found, the batch name is used to resolve the shot name token.

                    Args:
                    -----
                        `batch` (flame.PyBatch):
                            Flame PyBatch object.

                        `resolved_path` (str):
                            Resolved path with tokens.

                    Returns:
                    --------
                        `resolved_path` (str):
                            Resolved path with tokens.
                    """

                    def get_shot_name_tag(batch) -> str:
                        """
                        Get Shot Name Tag
                        """

                        # Check for ShotName tag
                        if batch.tags.get_value() != []:
                            print('Batch Tags:', batch.tags.get_value())
                            for tag in batch.tags.get_value():
                                if tag.startswith('ShotName:'):
                                    shot_name = tag.split(': ')[1]
                                    print(f'Batch Shot Name Tag Found: {shot_name}')
                                    return shot_name
                        else:
                            print('No Batch Shot Name Tags Found')
                            return None

                    def get_shot_name_from_render_nodes(batch) -> str:
                        """
                        Get Shot Name from Render Nodes
                        """

                        render_node_types = ['Render', 'Write File']
                        render_nodes = [node for node in batch.nodes if node.type in render_node_types]

                        if render_nodes:
                            shot_name = str(render_nodes[0].shot_name)[1:-1]
                            if shot_name:
                                print(f'Render Node Shot Name Found: {shot_name}')
                                return shot_name
                            else:
                                print('Render Node Shot Name Not Found')
                                return None
                        else:
                            print('No Render Nodes Found')
                            return None

                    shot_name = get_shot_name_tag(batch)
                    if not shot_name:
                        shot_name = get_shot_name_from_render_nodes(batch)
                    if not shot_name:
                        shot_name = pyflame.resolve_shot_name(str(batch.name)[1:-1])
                        print(f'Shot Name from Batch Name: {shot_name}')

                    print('\n', end='')

                    seq_name = get_seq_name(shot_name) # Get Seq Name from shot name

                    # Replace tokens in path
                    resolved_path = re.sub('<ShotName>', shot_name, resolved_path)
                    resolved_path = re.sub('<SeqName>', seq_name, resolved_path)
                    resolved_path = re.sub('<SEQNAME>', seq_name.upper(), resolved_path)

                    return resolved_path

                resolved_path = resolve_batch_tokens(flame_pyobject, resolved_path)

        pyflame.print(f'Resolved Tokenized String: {resolved_path}', text_color=TextColor.GREEN, new_line=False)
        print('----------------\n')

        return resolved_path

    @staticmethod
    def resolve_shot_name(name: str) -> str:
        """
        Resolve Shot Name
        =================

        Resolves a shot name from a provided string. This function is intended to handle
        two formats: a camera source name like 'A010C0012' or a standard name where the
        shot name precedes other identifiers (e.g. 'pyt_0010_comp').

        Args:
        -----
            `name` (str):
                The name to be resolved into a shot name.

        Returns:
        --------
            str: The resolved shot name.

        Raises:
        -------
            TypeError:
                If `name` is not a string.

        Examples:
        ---------
            Using a camera source name:
            ```
            shot_name = pyflame.resolve_shot_name('A010C0012')
            print(shot_name)  # Outputs: A010C001
            ```

            Using a standard name:
            ```
            shot_name = pyflame.resolve_shot_name('pyt_0010_comp')
            print(shot_name)  # Outputs: pyt_0010
            ```
        """

        # Validate argument types
        if not isinstance(name, str):
            raise TypeError(f"pyflame.resolve_shot_name: Expected 'name' to be a string, got {type(name).__name__} instead.")

        # Check if the name follows the format of a camera source (e.g. A010C0012).
        # If so, take the first 8 characters as the shot name.
        # The regex ^A\d{3}C\d{3} matches strings that start with 'A', followed by
        # three digits, followed by 'C', followed by three more digits.
        if re.match(r'^A\d{3}C\d{3}', name):
            shot_name = name[:8]
        else:
            # If the name is not a camera source, we assume it's in a different format
            # that requires splitting to find the shot name.
            # We split the name using digit sequences as delimiters.
            shot_name_split = re.split(r'(\d+)', name)

            # After splitting, we need to reassemble the shot name.
            # If there is at least one split, we check if the second element in the
            # split is alphanumeric. If it is, we concatenate the first two elements.
            # If it's not alphanumeric, we concatenate the first three elements.
            if len(shot_name_split) > 1:
                if shot_name_split[1].isalnum():
                    shot_name = shot_name_split[0] + shot_name_split[1]
                else:
                    shot_name = shot_name_split[0] + shot_name_split[1] + shot_name_split[2]
            else:
                # If the name wasn't split (no digits found), we keep the original name.
                shot_name = name

        return shot_name

    @staticmethod
    def untar(tar_file_path: str, untar_path: str, sudo_password: Optional[str]=None) -> bool:
        """
        Untar
        =====

        Untar a tar file.

        Args:
        -----
            `tar_file_path` (str):
                Path to tar file to untar including filename.tgz/tar.

            `untar_path` (str):
                Untar destination path.

            `sudo_password` (bool, optional):
                Password for sudo.
                (Default: `None`)

        Returns:
        --------
            bool: True if untar successful, False if not.

        Example:
        --------
            To untar a file:
            ```
            pyflame.unzip('/home/user/file.tar', '/home/user/untarred')
            ```
        """

        # Validate arguments
        if not isinstance(tar_file_path, str):
            raise TypeError(f"pyflame.untar: Expected 'tar_file_path' to be a string, got {type(tar_file_path).__name__} instead.")
        if not isinstance(untar_path, str):
            raise TypeError(f"pyflame.untar: Expected 'untar_path' to be a string, got {type(untar_path).__name__} instead.")
        if sudo_password is not None and not isinstance(sudo_password, str):
            raise TypeError(f"pyflame.untar: Expected 'sudo_password' to be a string, got {type(sudo_password).__name__} instead.")

        # Untar
        untar_command = f'tar -xvf {tar_file_path} -C {untar_path}'
        untar_command = untar_command.split()

        if sudo_password:
            process = Popen(['sudo', '-S'] + untar_command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
            stdout, stderr = process.communicate(sudo_password + '\n')
            if stderr:
                print(stderr)
        else:
            process = Popen(untar_command, stdin=PIPE, stderr=PIPE, universal_newlines=True)

        # Check if files exist in untar_path
        files_exist = False
        if os.path.isdir(untar_path):
            files = os.listdir(untar_path)
            if files:
                files_exist = True

        if files_exist:
            print('--> Untar successful.\n')
            return True
        else:
            print('--> Untar failed.\n')
            return False

    @staticmethod
    def gui_resize(value: int) -> int:
        """
        GUI Resize
        ==========

        Provides scaling for Qt UI elements based on the current screen's height
        relative to a standard height of 3190 pixels(HighDPI(Retina) resolution of
        Mac Studio Display).

        Args:
        -----
            `value` (int):
                Value to be scaled.

        Returns:
        --------
            int:
                The value scaled for the current screen resolution.

        Example:
        --------
            To resize a window:
            ```
            self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
            ```
        """

        # Validate argument type
        if not isinstance(value, int):
            raise TypeError(f"pyflame.gui_resize: Expected 'value' to be an int, got {type(value).__name__} instead.")

        # Baseline resolution from mac studio display
        base_screen_height = 3190

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        screen_resolution = main_window_res.screenGeometry()

        # Check if high DPI scaling is enabled. If so, double the screen height.
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            screen_height = screen_resolution.height() * 2
        else:
            screen_height = screen_resolution.height()

        # Calculate screen ratio
        screen_ratio = round(screen_height / base_screen_height, 1)

        if screen_ratio >= 1.0:
            screen_ratio = screen_ratio * .9

        # Scale value based on screen ratio
        scaled_value = int(float(value) * screen_ratio * 1.1)

        return scaled_value

    @staticmethod
    def font_resize(value: int) -> int:
        """
        Font Resize
        ===========

        Provides scaling for fonts to be used in Qt UI elements.
        Fonts are first scaled with the gui_resize method. Then if the
        current display is a High DPI display(Retina Displays) the
        result is returned. If the current display is not a High DPI
        display the the value is scaled further by 0.8 so fonts don't
        appear to big.

        Args:
        -----
            `value` (int):
                Value to be scaled.

        Returns:
        --------
            int:
                The font size value scaled for the current screen resolution.

        Example:
        --------
            To resize a font:
            ```
            font.setPointSize(pyflame.font_resize(13)
            ```
        """

        # Validate argument types
        if not isinstance(value, int):
            raise TypeError(f"pyflame.font_resize: Expected 'value' to be an int, got {type(value).__name__} instead.")

        # Scale font size through gui_resize method
        scaled_size = pyflame.gui_resize(value)

        # If screen is High DPI return scaled value, if not return scaled value * .8 to scale smaller.
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling')  and platform.system() == 'Darwin':
            return scaled_size
        else:
            #return int(scaled_size * 0.8)
            return value

    @staticmethod
    def get_export_preset_version(preset_path: str) -> Tuple[str, str]:
        """
        Get Export Preset Version
        ==========================

        Get current export preset version and current Flame preset export version.
        This should be updated with each new version of Flame.

        Args:
        -----
            `preset_path` (str):
                Path of preset to check/update.

        Returns:
        --------
            `current_export_version` (str):
                Version of current preset export.

            `export_version` (str):
                Export preset version for currernt version of Flame.

        Example:
        --------
            To get the export preset version:
            ```
            current_export_version, export_version = pyflame.get_export_preset_version(preset_path)
            ```

        Note:
        -----
            Scripts that use this:
                Create Export Menus
                SynthEyes Export
                Create Shot
        """

        # Validate argument types
        if not isinstance(preset_path, str):
            raise TypeError(f"pyflame.get_export_preset_version: Expected 'preset_path' to be a str, got {type(preset_path).__name__} instead.")

        print('Checking export preset version...')

        print('    Export preset path:', preset_path)

        def get_current_export_version(preset_path) -> str:
            """
            Get export version for current export preset XML.
            """

            # Open export preset XML
            export_preset_xml_tree = ET.parse(preset_path)
            root = export_preset_xml_tree.getroot()

            # Get version export preset is currently set to
            for setting in root.iter('preset'):
                current_export_version = setting.get('version')
                print(f'    Current export preset version: {current_export_version}')

            return current_export_version

        def get_export_version() -> str:
            """
            Get export version for current version of Flame from the default
            Jpeg export preset XML.
            """

            # Open Flame default Jpeg export preset XML
            preset_dir = flame.PyExporter.get_presets_dir(
                flame.PyExporter.PresetVisibility.Autodesk, flame.PyExporter.PresetType.Image_Sequence
            )
            preset_path = os.path.join(
                preset_dir, "Jpeg", "Jpeg (8-bit).xml"
            )
            preset_xml_tree = ET.parse(preset_path)
            root = preset_xml_tree.getroot()

            # Get version default export preset is currently set to
            for setting in root.iter('preset'):
                default_export_version = setting.get('version')
                print(f'    Flame default export preset version: {default_export_version}')
                print('\n', end='')

            return default_export_version

        current_export_version = get_current_export_version(preset_path)
        export_version = get_export_version()

        return current_export_version, export_version

    @staticmethod
    def update_export_preset(preset_path: str) -> None:
        """
        Update Export Preset
        ====================

        Update export preset file version to match current version of flame being used.

        Args:
        -----
            `preset_path` (str):
                Path of preset to check/update.

        Example:
        --------
            To update the export preset:
            ```
            pyflame.update_export_preset(preset_path)
            ```
        """

        # Validate argument types
        if not isinstance(preset_path, str):
            raise TypeError(f"pyflame.update_export_preset: Expected 'preset_path' to be a str, got {type(preset_path).__name__} instead.")

        current_export_version, export_version = pyflame.get_export_preset_version(
            preset_path=preset_path,
            )

        # If preset version if different than current export version then update preset xml
        if current_export_version != export_version:
            export_preset_xml_tree = ET.parse(preset_path) # Open preset XML file
            root = export_preset_xml_tree.getroot()

            # Update preset version in preset XML
            for element in root.iter('preset'):
                element.set('version', export_version)

            # Write out updated preset XML file
            export_preset_xml_tree.write(preset_path)

            print(f'Export preset updated to: {export_version}\n')
        print('Export preset current, nothing to update.\n')

    @staticmethod
    def iterate_name(existing_names: List[str], new_name: str) -> str:
        """
        Iterate Name
        ============

        Generates a unique name by appending a counter to the new_name until it no longer appears in the existing_names list.

        Args:
        -----
            `existing_names` (list of str):
                A list of existing names.

            `new_name` (str):
                The base name to be made unique.

        Returns:
        --------
            str:
                A unique name not present in the existing_names list.

        Example:
        --------
            To generate a unique name:
            ```
            unique_name = pyflame.iterate_name(existing_names, new_name)
            ```
        """

        # Validate argument types
        if not isinstance(existing_names, list):
            raise TypeError(f"pyflame.iterate_name: Expected 'existing_names' to be a list, got {type(iterate_name).__name__} instead.")
        if not all(isinstance(name, str) for name in existing_names):
            raise TypeError("pyflame.iterate_name: All elements in existing_names must be a string.")
        if not isinstance(new_name, str):
            raise TypeError(f"pyflame.iterate_name: Expected 'new_name' to be a string, got {type(new_name).__name__} instead.")

        # Initialize a counter
        counter = 1

        # Initialize the potential new name
        potential_name = new_name

        # Loop until we find a unique name
        while potential_name in existing_names:
            # Increment the name with the counter
            potential_name = f"{new_name} {counter}"
            # Increment the counter
            counter += 1

        return potential_name

    @staticmethod
    def get_export_preset_names() -> List[str]:
        """
        Get Export Preset Names
        =======================

        Get Export Preset Names from Shared and Project paths. User paths are not checked.

        The following are added to the beginning of each preset name:
            Shared: File Sequence:
            Shared: Movie:
            Project: File Sequence:
            Project: Movie:

        Returns:
        --------
            list[str]:
                A list of export preset names.
        """

        print('Getting Export Presets:\n')

        # Get Shared File Sequence Export Presets
        if os.path.isdir(SHARED_FILE_SEQUENCE_PATH):
            shared_file_sequence_export_presets = [f'Shared: File Sequence: {p[:-4]}' for p in os.listdir(SHARED_FILE_SEQUENCE_PATH) if p.endswith('.xml')]
        else:
            shared_file_sequence_export_presets = []
            print('Shared File Sequence Export Presets path does not exist:', SHARED_FILE_SEQUENCE_PATH, '\n')

        # Get Shared Movie Export Presets
        if os.path.isdir(SHARED_MOVIE_EXPORT_PATH):
            shared_movie_export_presets = [f'Shared: Movie: {p[:-4]}' for p in os.listdir(SHARED_MOVIE_EXPORT_PATH) if p.endswith('.xml')]
        else:
            shared_movie_export_presets = []
            print('Shared Movie Export Presets path does not exist:', SHARED_MOVIE_EXPORT_PATH, '\n')

        # Get Project File Sequence Export Presets
        if os.path.isdir(PROJECT_FILE_SEQUENCE_PATH):
            project_file_sequence_export_presets = [f'Project: File Sequence: {p[:-4]}' for p in os.listdir(PROJECT_FILE_SEQUENCE_PATH) if p.endswith('.xml')]
        else:
            project_file_sequence_export_presets = []
            print('Project File Sequence Export Presets path does not exist:', PROJECT_FILE_SEQUENCE_PATH, '\n')

        # Get Project Movie Export Presets
        if os.path.isdir(PROJECT_MOVIE_EXPORT_PATH):
            project_movie_export_presets = [f'Project: Movie: {p[:-4]}' for p in os.listdir(PROJECT_MOVIE_EXPORT_PATH) if p.endswith('.xml')]
        else:
            project_movie_export_presets = []
            print('Project Movie Export Presets path does not exist:', PROJECT_MOVIE_EXPORT_PATH, '\n')

        # Combine all export presets
        export_presets = shared_file_sequence_export_presets + shared_movie_export_presets + project_file_sequence_export_presets + project_movie_export_presets
        pyflame.print_list(
            list_name='Export Presets',
            list_items=export_presets,
            )

        print('Export Preset Check Complete.\n')

        return export_presets

    @staticmethod
    def convert_export_preset_name_to_path(export_preset_name: str) -> str:
        """
        Convert Export Preset Name to Path
        ==================================

        Convert Export Preset Name from Preset Menus(PyFlamePushButtonMenu) to Path.

        Preset Menu names should be in the following format:
            Shared: File Sequence: Jpeg (8-bit)
            Project: File Sequence: Jpeg (8-bit)
            Shared: Movie: Quicktime 4444
            Project: Movie: Quicktime 4444

        Shared:, Project:, File Sequence:, and Movie: are fixed strings and will be used to determine the path.

        Args:
        -----
            export_preset_name (str):
                Export preset name to convert to path.
                Example: 'Shared: File Sequence: Jpeg (8-bit)'

        Returns:
        --------
            str:
                Path to export preset.

        Raises:
        -------
            TypeError:
                If 'export_preset_name' is not a string.

        Example:
        --------
            To convert an export preset name to a path:
            ```
            export_preset_name = 'Shared: File Sequence: Jpeg (8-bit)'
            export_preset_path = pyflame.convert_export_preset_name_to_path(export_preset_name)
            ```

            export_preset_path will be:
            ```
            /opt/Autodesk/shared/presets/file_sequence/Jpeg (8-bit).xml
            ```
        """

        # Validate argument types
        if not isinstance(export_preset_name, str):
            raise TypeError(f"pyflame.convert_export_preset_name_to_path: Expected 'export_preset_name' to be a string, got {type(export_preset_name).__name__} instead.")

        # Convert export preset name to path
        if export_preset_name == '':
            return ''
        elif 'Shared: File Sequence:' in export_preset_name:
            print('Shared: File Sequence:',os.path.join(SHARED_FILE_SEQUENCE_PATH, f'{export_preset_name.split(": ")[2]}.xml'))
            return os.path.join(SHARED_FILE_SEQUENCE_PATH, f'{export_preset_name.split(": ")[2]}.xml')
        elif 'Shared: Movie:' in export_preset_name:
            print('Shared: Movie:', os.path.join(SHARED_MOVIE_EXPORT_PATH, f'{export_preset_name.split(": ")[2]}.xml'))
            return os.path.join(SHARED_MOVIE_EXPORT_PATH, f'{export_preset_name.split(": ")[2]}.xml')
        elif 'Project: File Sequence:' in export_preset_name:
            print('Project: File Sequence:', os.path.join(PROJECT_FILE_SEQUENCE_PATH, f'{export_preset_name.split(": ")[2]}.xml'))
            return os.path.join(PROJECT_FILE_SEQUENCE_PATH, f'{export_preset_name.split(": ")[2]}.xml')
        elif 'Project: Movie:' in export_preset_name:
            print('Project: Movie:', os.path.join(PROJECT_MOVIE_EXPORT_PATH, f'{export_preset_name.split(": ")[2]}.xml'))
            return os.path.join(PROJECT_MOVIE_EXPORT_PATH, f'{export_preset_name.split(":")[2]}.xml')
        else:
            return ''

    @staticmethod
    def set_shot_tagging(pyobject: Union[flame.PyLibrary, flame.PyFolder, flame.PyDesktop, flame.PyBatch, flame.PyClip], shot_name: str, append: bool=False) -> None:
        """
        Set Shot Tagging
        ================

        Set shot tagging for Flame object.

        Tags can be appended to existing tags or set directly. Default is to set tag directly.

        Args:
        -----
            pyobject (flame.PyObject):
                Flame object to set tagging for. Can be PyLibrary, PyFolder, PyDesktop, PyBatch, or PyClip.

            shot_name (str):
                Shot name to set as tag.

            append (bool, optional):
                Append shot name tag to existing tags.
                (Default: False)

        Raises:
        -------
            TypeError:
                If 'pyobject' is not a PyLibrary, PyFolder, PyDesktop, PyBatch, or PyClip.
                If 'shot_name' is not a string.
                If 'append' is not a boolean.

        Notes:
        ------
            - If appending tags, existing tags starting with ShotName: are removed before new tag is added.
        """

        # Validate arguments
        if not isinstance(pyobject, (flame.PyLibrary, flame.PyFolder, flame.PyDesktop, flame.PyBatch, flame.PyClip)):
            raise TypeError(f"pyflame.set_shot_tagging: Expected 'pyobject' to be a PyLibrary, PyFolder, PyDesktop, PyBatch, or PyClip, got {type(pyobject).__name__} instead.")
        if not isinstance(shot_name, str):
            raise TypeError(f"pyflame.set_shot_tagging: Expected 'shot_name' to be a string, got {type(shot_name).__name__} instead.")
        if not isinstance(append, bool):
            raise TypeError(f"pyflame.set_shot_tagging: Expected 'append' to be a boolean, got {type(append).__name__} instead.")

        # If appending tag, get all existing object tags and add new tag otherwise set tag directly
        if append:
            # Get all existing object tags
            all_tags = pyobject.tags.get_value()

            # If tag starting with ShotName: already exists, remove it
            if any(tag.startswith('ShotName:') for tag in all_tags):
                all_tags = [tag for tag in all_tags if not tag.startswith('ShotName:')]

            # Add new ShotName tag
            all_tags.append(f'ShotName: {shot_name}')

            pyobject.tags = all_tags
        else:
            pyobject.tags = [f'ShotName: {shot_name}'] # Set tag directly

    @staticmethod
    def find_by_tag(pyobject: Union[flame.PyLibrary, flame.PyDesktop, flame.PyFolder], target_tag: str, sorted: bool=True):
        """
        Find By Tag
        ===========

        Perform binary or linear search on PyObject's contained objects by tags.

        For example, search through a Library for a folder with a specific tag. It will not recursively search through subfolders.

        If `sorted` is True, uses binary search to efficiently find a Flame object that contains the target tag in its tag list.
        The search assumes PyObjects contained within the given PyObject are sorted by the tag being searched for.
        For instance, if searching a folder, the folder's immediate contained objects (subfolders and clips) must
        be sorted by the tag being searched for.

        If `sorted` is False, performs a linear search through the PyObjects contained within the given PyObject. This can be slower
        for large lists of PyObjects.

        Args:
        -----
            pyobject (flame.PyLibrary, flame.PyDesktop, or flame.PyFolder):
                Flame PyObject (Library, Desktop, or Folder) that will be searched for item with target tag.

            target_tag (str):
                Tag to search for. If contains ':', will match against tag_type:value format.

            sorted (bool):
                If True, assumes PyObjects contained within `pyobject` are sorted by tag.
                When True, performs a binary search. If False, performs a linear search.
                (Default: True)

        Returns:
        --------
            The matching Flame PyObject if found, None otherwise.

        Examples:
        --------
            Find a shot folder by tag where PyObjects are sorted by tag:
            ```
            find_by_tag(
                pyobject=<PyLibraryObject>,
                target_tag='ShotName: PYT_0010',
                )
            ```

            Find a clip by tag where PyObjects are not sorted by tag:
            ```
            find_by_tag(
                pyobject=<PyLibraryObject>,
                target_tag='ShotName: PYT_0010',
                sorted=False
                )
            ```
        """

        # If sorted is True, perform binary search other wise perform a linear search
        if sorted:
            print('Performing Binary Tag Search')
            # Split target tag at ': ' to get tag_type if ':' is present
            if ':' in target_tag:
                tag_type = target_tag.split(': ', 1)[0]
            else:
                tag_type = target_tag

            # Perform binary search
            start, end = 0, len(pyobject) - 1

            while start <= end:
                mid = (start + end) // 2
                pyobject_tags = pyobject[mid].tags.get_value()
                # Loop through folder_tags to fing tag starting with tag_type
                for tag in pyobject_tags:
                    if tag.startswith(tag_type):
                        pyobject_tag = tag
                        break

                # Perform a direct comparison
                if pyobject_tag == target_tag:
                    print(f'Found Tagged PyObject: {pyobject[mid].name}\n')
                    return pyobject[mid]  # Return the PyObject object if found
                elif pyobject_tag < target_tag:
                    start = mid + 1
                else:
                    end = mid - 1
        else:
            # Perform linear search
            print('Performing Linear Tag Search')
            for pyobject_item in pyobject:
                if target_tag in pyobject_item.tags.get_value():
                    print(f'Found Tagged PyObject: {pyobject_item.name}\n')
                    return pyobject_item

        print(f'Tagged PyObject: {target_tag} Not Found\n')

        return None

    @staticmethod
    def shot_name_from_clip(clip: flame.PyClip) -> str:
        """
        Shot Name From Clip
        ===================

        Get shot name from clip.

        Args:
        -----
            clip (flame.PyClip):
                Clip to get shot name from

        Returns:
        --------
            shot_name (str):
                Shot name

        Notes:
        -----
            - Check if clip has assigned Shot Name.
            - Check if clip is tagged with ShotName (ShotName: PYT_0010)
            - If no Shot Name is assigned or tagged, extract shot name from clip name.
        """

        pyflame.print('Getting Shot Name From Clip', new_line=False)

        # Check if shot name is assigned to clip
        assigned_shot_name = str(clip.versions[0].tracks[0].segments[0].shot_name)[1:-1]
        if assigned_shot_name != '':
            shot_name = assigned_shot_name
            pyflame.print(f'Shot Name Found: {shot_name}', text_color=TextColor.GREEN)
            return shot_name

        # Check if clip is tagged with ShotName
        clip_tags = clip.tags.get_value()
        shot_name_tag = [tag for tag in clip_tags if tag.startswith('ShotName:')]
        if shot_name_tag:
            shot_name = shot_name_tag[0].split(': ')[1]
            pyflame.print(f'Shot Name Tag Found: {shot_name}', text_color=TextColor.GREEN)
            return shot_name

        # Get shot name from clip name
        clip_name = str(clip.name)[1:-1]
        print('Clip Name:', clip_name)

        # Split clip name into list by numbers in clip name
        shot_name_split = re.split(r'(\d+)', clip_name)
        shot_name_split = [s for s in shot_name_split if s != '']
        #print('shot_name_split:', shot_name_split)

        # If second part of split name contains only alphanumeric chars,
        # combine first two parts (e.g. "Shot" + "01" -> "Shot01")
        # Otherwise combine first three parts to handle separators
        # (e.g. "Shot" + "_" + "01" -> "Shot_01")
        if shot_name_split[1].isalnum():
            shot_name = shot_name_split[0] + shot_name_split[1]
        else:
            shot_name = shot_name_split[0] + shot_name_split[1] + shot_name_split[2]

        # Tag clip with shot name
        pyflame.set_shot_tagging(clip, shot_name)

        pyflame.print(f'Shot Name from Clip Name: {shot_name}', text_color=TextColor.GREEN)

        return shot_name

    @staticmethod
    def move_to_shot_folder(shot_name: str, pyobject: Union[flame.PyClip, flame.PyBatch, flame.PyDesktop], search_location: Union[flame.PyLibrary, flame.PyFolder], dest_folder_path: str) -> None:
        """
        Move to Shot Folder
        ===================

        Move PyClip, PyBatch, or PyDesktop to a Media Panel shot folder in search_location(flame.PyLibrary or flame.PyFolder)

        Folders in search location must be tagged with 'ShotName: <shot_name>', i.e. 'ShotName: PYT_0010'

        Args:
        -----
            shot_name (str):
                Name of shot

            pyobject (Union[flame.PyClip, flame.PyBatch, flame.PyDesktop]):
                PyClip, PyBatch, or PyDesktop to move to shot folder.

            search_location (Union[flame.PyLibrary, flame.PyFolder]):
                Media Panel Library or Folder to search through for shot folder.

            dest_folder_path (str):
                Destination folder path in Shot Folder.
                Example: 'Shot_Folder/Plates'
        """

        def get_folder_from_path(folder: flame.PyFolder, media_panel_folder_path: str) -> flame.PyFolder:
            """
            Get Folder from Path
            ====================

            Recursively find Media Panel folder from path

            Args:
            -----
                folder (flame.PyFolder):
                    Media Panel Folder to search through for destination folder.

                media_panel_folder_path (str):
                    Media Panel destination folder path.
                    Example: 'Shot_Folder/Plates'

            Returns:
            --------
                dest_folder (flame.PyFolder):
                    Destination folder.
            """


            def find_next_folder(folder: flame.PyFolder, folder_list: list) -> flame.PyFolder:
                """
                Find Next Folder
                ===============

                Recursively find next folder in folder list.
                """

                for sub_folder in folder.folders:
                    if sub_folder.name == folder_list[0]:
                        return find_next_folder(sub_folder, folder_list[1:])
                return folder

            # Convert media_panel_folder_path to list and remove first element (root folder)
            folder_list = media_panel_folder_path.split('/', 1)[1].split('/')

            # Find destination folder
            dest_folder = find_next_folder(shot_folder, folder_list)

            return dest_folder

        # Create target tag for shot folder search
        target_tag = f'ShotName: {shot_name}'

        # Search through search_location(flame.PyLibrary or flame.PyFolder) for shot folder with matching target tag
        shot_folder = pyflame.find_by_tag(search_location.folders, target_tag)

        dest_folder = get_folder_from_path(shot_folder, dest_folder_path)
        flame.media_panel.move(pyobject, dest_folder)

pyflame = _PyFlameFunctions()

#-------------------------------------
# [PyFlame Config]
#-------------------------------------

class PyFlameConfig:
    """
    PyFlameConfig
    =============

    A class to manage configuration settings for the PyFlame script.

    This class handles loading and saving configuration settings from and to a JSON file.
    It updates instance attributes based on the configuration values.

    Values can be provided as their original data types. Values no longer need to be converted to strings.

    Args:
    -----
        `config_values` (Dict[str, Any]):
            A dictionary to store configuration key-value pairs.

        `config_path` (str):
            The file path to the configuration JSON file.

        `script_name` (str):
            The name of the script. This is used to identify the script in the configuration file. This does not need to be set in most cases.
            (Default: `SCRIPT_NAME`)

    Methods:
    --------
        `load_config(config_values: Dict[str, Any])`:
            Loads configuration values from a JSON file and updates instance attributes.

        `save_config(config_values: Dict[str, Any])`:
            Saves the current configuration values to a JSON file.

        `get_config_values()` -> Dict[str, Any]:
            Returns the current configuration values.

    Raises:
    -------
        TypeError:
            If `config_values` is not a dictionary.
            If `config_path` is not a string.
        ValueError:
            If `config_values` is empty.

    Examples:
    ---------
        To Load/Create settings:
        ```
        settings = PyFlameConfig(
                config_values={
                'camera_path': '/opt/Autodesk',
                'scene_scale': 100,
                'import_type': 'Action Objects',
                'st_map_setup': False,
                }
            )
        ```

        To save settings:
        ```
        settings.save_config(
            config_values={
                'camera_path': self.path_entry.text(),
                'scene_scale': self.scene_scale_slider.get_value(),
                'import_type': self.import_type.text(),
                'st_map_setup': self.st_map_setup.isChecked(),
                }
            )
        ```

        To get setting values:
        ```
        print(settings.camera_path)
        >'/opt/Autodesk'
        ```
    """

    def __init__(self,
                 config_values: Dict[str, Any],
                 config_path: str=os.path.join(SCRIPT_PATH, 'config/config.json'),
                 script_name: str=SCRIPT_NAME
                 ):

        # Argument type validation
        if not isinstance(config_values, dict):
            raise TypeError(f"PyFlameConfig: Expected 'config_values' to be a dictionary, got {type(config_values).__name__} instead.")
        if not config_values:
            raise ValueError("PyFlameConfig: config_values dictionary cannot be empty.")
        if not isinstance(config_path, str):
            raise TypeError(f"PyFlameConfig: Expected 'config_path' to be a string, got {type(config_path).__name__} instead.")

        # Initialize instance attributes
        self.config_values: Dict[str, Any] = config_values
        self.config_path = config_path
        self.script_name = script_name

        # Load the configuration
        self.load_config()

    def load_config(self) -> None:
        """
        Load Config
        ===========

        Loads the configuration from the JSON file and updates instance attributes.

        This method reads the configuration file specified by `config_path`. If the file exists,
        it updates the instance's configuration values and attributes with those read from the file.
        If the file does not exist, it saves the default configuration values to the file.
        """

        #print('Loading script configuration...\n')

        pyflame.print('Loading Script Configuration', underline=True, )

        # Load the configuration from the JSON file
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                loaded_config: Dict[str, Any] = json.load(f)
                # Update the default values with the loaded ones
                self.config_values.update(loaded_config)
        else:
            # Ensure the config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            # Save the default configuration values if the file does not exist
            self.save_config(self.config_values)

        # Set the attributes from config values
        for key, value in self.config_values.items():
            setattr(self, key, value)

        # Print values to terminal
        pyflame.print_json(
            json_data=self.config_values,
            indent=2,
            )

        print('-' * 28, '\n')

        pyflame.print('Script Configuration Loaded', arrow=True)

    def save_config(self, config_values: Optional[Dict[str, Any]]=None, config_path: Optional[str]=None) -> None:
        """
        Save Config
        ===========

        Saves the current configuration values to the JSON file.

        This method updates the configuration values with any provided values and writes them to
        the configuration file specified by `config_path`. It ensures that existing values are
        preserved unless explicitly overwritten.

        Args:
        -----
            `config_values` (Dict[str, Any]):
                A dictionary of configuration values to update.
                (Default: None)

            `config_path` (str):
                The file path to save the configuration JSON file. This does not need to be set in most cases.
                (Default: None)

        Raises:
        -------
            TypeError:
                If `config_values` is not a dictionary.

        Example:
        --------
            To save the current configuration values:
            ```
            settings.save_config(
                config_values={
                    'camera_path': self.path_entry.text(),
                    'scene_scale': self.scene_scale_slider.get_value(),
                    'import_type': self.import_type.text(),
                    'st_map_setup': self.st_map_setup.isChecked(),
                    }
                )
            ```
        """

        # Validate argument types
        if config_values is not None and not isinstance(config_values, dict):
            raise TypeError(f"PyFlameConfig.save_config: Expected 'config_values' to be a dictionary or None, got {type(config_values).__name__} instead.")
        if config_path is not None and not isinstance(config_path, str):
            raise TypeError(f"PyFlameConfig.save_config: Expected 'config_path' to be a string or None, got {type(config_path).__name__} instead.")

        pyflame.print('Saving Script Configuration', underline=True, )

        if config_path is None:
            config_path = self.config_path

        if config_values:
            self.config_values.update(config_values)

        # Ensure the script name is in the config
        self.config_values['script_name'] = self.script_name

        # script_name should be the first key in the config
        self.config_values = {key: self.config_values[key] for key in ['script_name'] + list(self.config_values.keys())}

        # Read existing config to keep unaltered values
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                existing_config: Dict[str, Any] = json.load(f)
        else:
            existing_config = {}

        # Update only provided values
        existing_config.update(self.config_values)

        with open(config_path, 'w') as f:
            json.dump(existing_config, f, indent=4)

        # Update the instance attributes with new config values
        for key, value in self.config_values.items():
            setattr(self, key, value)

        # Print values to terminal
        pyflame.print_json(
            json_data=self.config_values,
            indent=2,
            )

        print('-' * 27, '\n')

        pyflame.print('Script Configuration Saved', arrow=True)

    def get_config_values(config_path: str) -> Dict[str, Any]:
        """
        Get Config Values
        =================

        Returns the current configuration values.

        This method provides access to the current state of configuration values stored in the instance.

        Args:
        -----
            `config_path` (str):
                The file path to the configuration JSON file.

        Returns:
        --------
            Dict[str, Any]: The current configuration values.
        """

        # Validate argument type
        if not isinstance(config_path, str):
            raise TypeError(f"PyFlameConfig.get_config_values: Expected 'config_path' to be a string, got {type(config_path).__name__} instead.")

        # Load the configuration from the JSON file
        with open(config_path, 'r') as f:
            return json.load(f)

#-------------------------------------
# [PyFlame QT Widget Classes]
#-------------------------------------

class PyFlameButton(QtWidgets.QPushButton):
    """
    PyFlameButton
    =============

    Custom QT Flame Button Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlameButton text.

        `connect` (callable):
            Function to call when PyFlameButton is clicked.

        `width` (int, optional):
            PyFlameButton width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameButton height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameButton to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `color` (Color, optional):
            PyFlameButton color. See Color Options below.
            (Default: `Color.GRAY`)

        `font` (str, optional):
            Font family to be used for the text on the button.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text on the button.
            (Default: `PYFLAME_FONT_SIZE`)

        `tooltip` (str, optional):
            PyFlameButton tooltip text.
            (Default: `None`)

    Color Options:
    --------------
        - `Color.GRAY`: Standard gray button.
        - `Color.BLUE`: Blue button.
        - `Color.RED`: Red button.

    Methods:
    --------
        `set_button_color(color)`:
            Set the color of the button after its creation using Color Options.

    Examples:
    ---------
        Create a blue PyFlameButton:
        ```
        button = PyFlameButton(
            text='Button Name',
            connect=some_function,
            color=Color.BLUE
            )
        ```

        To change the button color after creation:
        ```
        button.set_button_color(Color.BLUE)
        ```

        Enable or disable the button:
        ```
        button.setEnabled(True)
        button.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlameButton',
                 text: str,
                 connect: Callable[..., None],
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 color: Color=Color.GRAY,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 tooltip: Optional[str]=None,
                 ) -> None:
        super().__init__()

        # Validate arguments
        if not isinstance(text, str):
            raise TypeError(f"PyFlameButton: Expected 'text' to be a string, got {type(text).__name__} instead.")
        if not callable(connect):
            raise TypeError(f"PyFlameButton: Expected 'connect' to be a callable function, got {type(connect).__name__} instead.")
        if not isinstance(width, int):
            raise TypeError(f"PyFlameButton: Expected 'width' to be an int, got {type(width).__name__} instead.")
        if not isinstance(height, int):
            raise TypeError(f"PyFlameButton: Expected 'height' to be an int, got {type(height).__name__} instead.")
        if not isinstance(max_width, bool):
            raise TypeError(f"PyFlameButton: Expected 'max_width' to be a bool, got {type(max_width).__name__} instead.")
        if not isinstance(color, Color):
            raise TypeError(f"PyFlameButton: Expected 'color' to be a Color Enum, got {type(color).__name__} instead.")
        if not isinstance(font, str):
            raise TypeError(f"PyFlameButton: Expected 'font' to be a string, got {type(font).__name__} instead.")
        if not isinstance(font_size, int):
            raise TypeError(f"PyFlameButton: Expected 'font_size' to be an int, got {type(font_size).__name__} instead.")
        if tooltip is not None and not isinstance(tooltip, str):
            raise TypeError(f"PyFlameButton: Expected 'tooltip' to be a string or None, got {type(tooltip).__name__} instead.")

        # Set button font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build button
        self.setText(text)
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(connect)
        if tooltip is not None:
            self.setToolTip(tooltip)

        self._set_stylesheet(color)

    def set_button_color(self, color: Color) -> None:
        """
        Set Button Color
        ================

        Set the color of the button after its creation.

        This public method updates the button's appearance by changing its color.

        Args:
        -----
            `color` (Color):
                The color to set for the button: `Color.GRAY`, `Color.Blue`, `Color.RED`

        Raises:
        -------
            ValueError:
                If the provided `color` is not a supported color option.

        Example:
        --------
            Change the button color to red:

            ```
            button.set_button_color(Color.RED)
            ```
        """

        if color not in {Color.GRAY, Color.BLUE, Color.RED}:
            raise ValueError(f'_set_stylesheet: Unsupported color: {color}. Supported colors are: GRAY, BLUE, RED.')

        self._set_stylesheet(color)
        self.update()  # Refresh the button's appearance

    def _set_stylesheet(self, color: Color) -> None:
        """
        Set Style Sheet
        ===============

        This private method sets the widget stylesheet.

        The stylesheet has three color options for the button: GRAY, BLUE, and RED.

        Args:
        -----
            `color` (Color):
                The color to set for the button: `Color.GRAY`, `Color.Blue`, `Color.RED`

        Raises:
        -------
            ValueError:
                If the provided `color` is not a supported color option.
        """

        # Validate argument
        if color not in {Color.GRAY, Color.BLUE, Color.RED}:
            raise ValueError(f'PyFlameButton._set_stylesheet: Unsupported color: {color}. Supported colors are: GRAY, BLUE, RED.')

        # Set button color based on color enum
        if color == Color.GRAY:
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {Color.BUTTON_TEXT.value}; /* Button text color */
                    background-color: {Color.GRAY.value}; /* Button color */
                    border: none; /* Button border */
                    }}
                QPushButton:hover{{
                    border: 1px solid {Color.BORDER.value}; /* Hover button border */
                    }}
                QPushButton:pressed{{
                    color: {Color.TEXT_SELECTED.value}; /* Pressed text color */
                    background-color: {Color.SELECTED_GRAY.value}; /* Pressed button color */
                    border: 1px solid {Color.BORDER.value}; /* Pressed button border */
                    }}
                QPushButton:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    background-color: {Color.GRAY.value}; /* Disabled button color */
                    border: none; /* Disabled button border */
                    }}
                QToolTip{{
                    color: {Color.WHITE.value}; /* Tooltip text color */
                    background-color: {Color.SELECTED_GRAY.value}; /* Tooltip background color */
                    border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                    }}
                """)

        elif color == Color.BLUE:
            self.setStyleSheet(f"""
                QPushButton{{
                    color: {Color.TEXT_BRIGHT.value}; /* Button text color */
                    background-color: {Color.BLUE.value}; /* Button color */
                    border: none; /* Button border */
                    }}
                QPushButton:hover{{
                    border: 1px solid {Color.BORDER_BRIGHTER.value}; /* Hover button border */
                    }}
                QPushButton:pressed{{
                    color: {Color.TEXT_SELECTED.value}; /* Pressed text color */
                    border: 1px solid {Color.BORDER_BRIGHTER.value}; /* Pressed button border */
                    }}
                QPushButton:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    background-color: {Color.GRAY.value}; /* Disabled button color */
                    border: none; /* Disabled button border */
                    }}
                QToolTip{{
                    color: {Color.WHITE.value}; /* Tooltip text color */
                    background-color: {Color.SELECTED_GRAY.value}; /* Tooltip background color */
                    border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                    }}
                """)

        elif color == Color.RED:
            self.setStyleSheet(f"""
                QPushButton{{
                    color: {Color.TEXT_BRIGHT.value}; /* Button text color */
                    background-color: {Color.RED.value}; /* Button color */
                    border: none; /* Button border */
                    }}
                QPushButton:hover{{
                    border: 1px solid {Color.BORDER.value}; /* Hover button border */
                    }}
                QPushButton:pressed{{
                    color: {Color.TEXT_SELECTED.value}; /* Pressed text color */
                    border: 1px solid {Color.BORDER.value}; /* Pressed button border */
                    }}
                QPushButton:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    background-color: {Color.GRAY.value}; /* Disabled button color */
                    border: none; /* Disabled button border */
                    }}
                QToolTip{{
                    color: {Color.WHITE.value}; /* Tooltip text color */
                    background-color: {Color.SELECTED_GRAY.value}; /* Tooltip background color */
                    border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                    }}
                """)

class PyFlameButtonGroup(QtWidgets.QButtonGroup):
    """
    PyFlameButtonGroup
    ==================

    Custom QT Flame Button Group Widget Subclass

    This class allows for grouping multiple buttons to control their checked state collectively.
    It supports setting the buttons to exclusive or non-exclusive behavior, meaning that either
    only one button can be checked at a time or multiple buttons can be checked simultaneously.

    Args:
    -----
        `buttons` (list):
            List of buttons to be part of group.

        `set_exclusive` (bool, optional):
            If True, only one button can be checked at a time.
            (Default: `True`)

    Example:
    --------
        To create a button group:
        ```
        button_group = PyFlameButtonGroup(
            buttons=[
                self.action_node_only_push_button,
                self.st_map_setup_button,
                self.patch_setup_button,
                ],
            )
        ```
    """

    def __init__(self: 'PyFlameButtonGroup',
                    buttons: list,
                    set_exclusive: bool=True,
                    ) -> None:
        super().__init__()

        # Validate arguments
        if not isinstance(buttons, list):
            raise TypeError(f"PyFlameButtonGroup: Expected 'buttons' to be a list, got {type(buttons).__name__} instead.")
        if not all(isinstance(button, QtWidgets.QPushButton) for button in buttons):
            raise TypeError(f"PyFlameButtonGroup: All elements in 'buttons' must be instances of QPushButton.")
        if not isinstance(set_exclusive, bool):
            raise TypeError(f"PyFlameButtonGroup: Expected 'set_exclusive' to be a bool, got {type(set_exclusive).__name__} instead.")

        # Set exclusive
        self.setExclusive(set_exclusive)

        # Add buttons to group
        for button in buttons:
            self.addButton(button)

class PyFlameEntry(QtWidgets.QLineEdit):
    """
    PyFlameEntry
    ============

    Custom QT Flame LineEdit Widget Subclass

    Replaces PyFlameLineEdit.

    Args:
    -----
        `text` (str):
            Initial text to be displayed in the entry field.

        `align` (Align, optional):
            Align text to left, right, or center.
            See Align Options below.
            (Default: `Align.LEFT`)

        `width` (int, optional):
            Width of the entry field in pixels.
            (Default: `50`)

        `height` (int, optional):
            Height of the entry field in pixels.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameEntry to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `text_changed` (callable, optional):
            Function to be called whenever the text in the entry field changes. This is typically used to perform live updates based on user input.
            (Default: `None`)

        `placeholder_text` (str, optional):
            Temporary text to display when PyFlameEntry is empty.
            (Default: `None`)

        `read_only` (bool, optional):
            Sets the entry to be read-only if True, disabling user input and applying a distinct visual style to indicate this state. Text is not selectable.
            (Default: `False`)

        `font` (str, optional):
            Font family to be used for the text in the entry field.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text in the entry field.
            (Default: `PYFLAME_FONT_SIZE`)

    Align Options:
    --------------
        - `Align.LEFT`: Aligns text to the left side of the label.
        - `Align.RIGHT`: Aligns text to the right side of the label.
        - `Align.CENTER`: Centers text within the label.

    Examples:
    ---------
        To create a PyFlameEntry:
        ```
        entry = PyFlameEntry(
            value='Something here'
            )
        ```

        To get text from PyFlameEntry:
        ```
        entry.text()
        ```

        To set PyFlameEntry text:
        ```
        entry.setText('Some text here')
        ```

        To enable/disable PyFlameEntry:
        ```
        entry.setEnabled(True)
        entry.setEnabled(False)
        ```

        To set PyFlameEntry as focus (cursor will be in PyFlameEntry):
        ```
        entry.setFocus()
        ```
    """

    def __init__(self: 'PyFlameEntry',
                 text: str,
                 align: Align=Align.LEFT,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 text_changed: Optional[Callable]=None,
                 placeholder_text: Optional[str]=None,
                 tooltip: Optional[str]=None,
                 read_only: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate arguments
        if not isinstance(text, str):
            raise TypeError(f"PyFlameEntry: Expected 'text' to be a str, got {type(text).__name__} instead.")
        if not isinstance(align, Align):
            raise TypeError(f"PyFlameEntry: Expected 'align' to be an Align enum, got {type(align).__name__} instead.")
        if width is not None and not isinstance(width, int):
            raise TypeError(f"PyFlameEntry: Expected 'width' to be None or an int, got {type(width).__name__} instead.")
        if not isinstance(height, int):
            raise TypeError(f"PyFlameEntry: Expected 'height' to be an int, got {type(height).__name__} instead.")
        if not isinstance(max_width, bool):
            raise TypeError(f"PyFlameEntry: Expected 'max_width' to be a bool, got {type(max_width).__name__} instead.")
        if text_changed is not None and not callable(text_changed):
            raise TypeError(f"PyFlameEntry: Expected 'text_changed' to be a callable function or None, got {type(text_changed).__name__} instead.")
        if placeholder_text is not None and not isinstance(placeholder_text, str):
            raise TypeError(f"PyFlameEntry: Expected 'placeholder_text' to be a string or None, got {type(placeholder_text).__name__} instead.")
        if not isinstance(read_only, bool):
            raise TypeError(f"PyFlameEntry: Expected 'read_only' to be a boolean, got {type(read_only).__name__} instead.")
        if not isinstance(font, str):
            raise TypeError(f"PyFlameEntry: Expected 'font' to be a string, got {type(font).__name__} instead.")
        if not isinstance(font_size, int):
            raise TypeError(f"PyFlameEntry: Expected 'font_size' to be an int, got {type(font_size).__name__} instead.")

        self.read_only = read_only

        self.setToolTip(tooltip)

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build Entry
        self.setText(str(text))

        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        if text_changed is not None:
            self.textChanged.connect(text_changed)
        if placeholder_text is not None:
            self.setPlaceholderText(placeholder_text)

        if read_only:
            self.setReadOnly(True)

        # Set text alignment
        if align == Align.LEFT:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        elif align == Align.RIGHT:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        elif align == Align.CENTER:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

        # Set stylesheet
        self._set_stylesheet(self.read_only)

    def _set_stylesheet(self, read_only) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the widget stylesheet.

        The stylesheet has two states: read-only and editable.

        If read-only, the background color is darker and the text color is gray.
        Otherwise, the default Flame line edit stylesheet is applied.

        Args:
        -----
            `read_only` (bool):
                Indicates whether the PyFlameLineEdit is read-only.

        Raises:
        -------
            TypeError:
                If `read_only` is not a boolean.

        Example:
        --------
            Set PyFlameEntry stylesheet to `read_only`:
            ```
            self._set_stylesheet(read_only)
            ```
        """

        # Validate argument type
        if not isinstance(read_only, bool):
            raise TypeError(f'_set_stylesheet: Invalid read_only argument: {read_only}. Must be a boolean.')

        # Set line edit stylesheet based on read-only state
        if read_only:
            self.setStyleSheet(f"""
                QLineEdit{{
                    color: {Color.TEXT.value};
                    background-color: {Color.TEXT_READ_ONLY_BACKGROUND.value};
                    border: 1px solid {Color.TEXT_READ_ONLY_BACKGROUND.value};
                    padding-left: 1px;
                    }}
                QLineEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    padding-left: 1px;
                    }}
                QLineEdit:disabled{{
                    color: {Color.TEXT_DISABLED.value};
                    background-color: {Color.DISABLED_GRAY.value};
                    border: 1px solid {Color.DISABLED_GRAY.value};
                    padding-left: 1px;
                    }}
                QToolTip{{
                    color: {Color.WHITE.value}; /* Tooltip text color */
                    background-color: {Color.SELECTED_GRAY.value};
                    border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                    }}
                """)
        # Set line edit stylesheet based on editable state
        else:
            self.setStyleSheet(f"""
                QLineEdit{{
                    color: {Color.TEXT.value};
                    background-color: rgb(55, 65, 75);
                    border: 1px solid rgb(55, 65, 75);
                    selection-color: rgb(38, 38, 38);
                    selection-background-color: rgb(184, 177, 167);
                    padding-left: 1px;
                    }}
                QLineEdit:focus{{
                    background-color: rgb(73, 86, 99);
                    padding-left: 1px;
                    }}
                QLineEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    padding-left: 1px;
                    }}
                QLineEdit:disabled{{
                    color: {Color.TEXT_DISABLED.value};
                    background-color: {Color.DISABLED_GRAY.value};
                    border: 1px solid {Color.DISABLED_GRAY.value};
                    padding-left: 1px;
                    }}
                QToolTip{{
                    color: {Color.WHITE.value}; /* Tooltip text color */
                    background-color: {Color.SELECTED_GRAY.value};
                    border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                    }}
                """)

    def mousePressEvent(self, event):
        if self.read_only:
            self.clearFocus()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.read_only:
            event.ignore()
        else:
            super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if not self.read_only:  # This allows typing when not read-only.
            super().keyPressEvent(event)
        else:
            pass

    def mouseDoubleClickEvent(self, event):
        if self.read_only:
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

class PyFlameLabel(QtWidgets.QLabel):
    """
    PyFlameLabel
    ============

    Custom QT Flame Label Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlameLabel text.

        `style` (Style, optional):
            Select from different styles. See Style Options below.
            (Default: `Style.NORMAL`)

        `align` (Align, optional):
            Align text to left, right, or center. Overrides LabelStyle alignment. If set to None, Style alignment will be used.
            See Align Options below.
            (Default: `None`)

        `width` (int, optional):
            PyFlameLabel width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameLabel height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameLabel to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `max_height` (bool, optional):
            Set PyFlameLabel to maximum height. Use if height is being set by layout. Overrides `height` if set to True.
            (Default: `False`)

        `underline_color` (Color, optional):
            Color of text underline when using `Style.UNDERLINE`.
            Tuple must contain 4 values rgba(Red, Green, Blue, Alpha).
            The fourth value (alpha) is a float number between 0 and 1.
            (Default: `Color.TEXT_UNDERLINE.value`)

        `font` (str, optional):
            PyFlameLabel font.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            PyFlameLabel font size.
            (Default: `PYFLAME_FONT_SIZE`)

        `font` (str, optional):
            Font family to be used for the label text.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the label text.
            (Default: `PYFLAME_FONT_SIZE`)

    Style Options:
    --------------
        - `Style.NORMAL`: Standard label without any additional styling. Text is left aligned.
        - `Style.UNDERLINE`: Underlines label text. Text is centered.
        - `Style.BACKGROUND`: Adds a darker background to the label. Text is left aligned.
        - `Style.BORDER`: Adds a white border around the label with a dark background. Text is centered.

    Align Options:
    --------------
        - `None`: Uses the alignment defined by the style.
        - `Align.LEFT`: Aligns text to the left side of the label.
        - `Align.RIGHT`: Aligns text to the right side of the label.
        - `Align.CENTER`: Centers text within the label.

    Examples:
    ---------
        To create a label:
        ```
        label = PyFlameLabel(
            text='This is a label',
            style=Style.UNDERLINE,
            align=Align.LEFT,
            )
        ```

        To set label text:
        ```
        label.setText('New Text')
        ```

        To enable/disable label:
        ```
        label.setEnabled(True)
        label.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlameLabel',
                 text: str,
                 style: Style=Style.NORMAL,
                 align: Optional[Align]=None,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 max_height: bool=False,
                 underline_color: Color=Color.TEXT_UNDERLINE.value,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate arguments
        if not isinstance(text, str):
            raise TypeError(f"PyFlameLabel: Expected 'text' to be a string, got {type(text).__name__} instead.")
        if not isinstance(style, Style):
            raise TypeError(f"PyFlameLabel: Expected 'style' to be a Style Enum, got {type(style).__name__} instead.")
        if align is not None and not isinstance(align, Align):
            raise TypeError(f"PyFlameLabel: Expected 'align' to be an Align Enum or None, got {type(align).__name__} instead.")
        if not isinstance(width, int):
            raise TypeError(f"PyFlameLabel: Expected 'width' to be an int, got {type(width).__name__} instead.")
        if not isinstance(height, int):
            raise TypeError(f"PyFlameLabel: Expected 'height' to be an int, got {type(height).__name__} instead.")
        if not isinstance(max_width, bool):
            raise TypeError(f"PyFlameLabel: Expected 'max_width' to be a bool, got {type(max_width).__name__} instead.")
        if not isinstance(max_height, bool):
            raise TypeError(f"PyFlameLabel: Expected 'max_height' to be a bool, got {type(max_height).__name__} instead.")
        if not isinstance(underline_color, str):
            raise TypeError(f"PyFlameLabel: Expected 'underline_color' to be a str, got {type(underline_color).__name__} instead.")
        if not isinstance(font, str):
            raise TypeError(f"PyFlameLabel: Expected 'font' to be a string, got {type(font).__name__} instead.")
        if not isinstance(font_size, int):
            raise TypeError(f"PyFlameLabel: Expected 'font_size' to be an int, got {type(font_size).__name__} instead.")

        self.underline_color = underline_color

        # Set label font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build label
        self.setText(text)

        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on style
        if align == Align.LEFT:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        elif align == Align.RIGHT:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        elif align == Align.CENTER:
            self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        else:  # If align is None
            if style == Style.NORMAL or style == Style.BACKGROUND:
                self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            else:  # UNDERLINE or BORDER
                self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)

        self._set_stylesheet(style)

    def _set_stylesheet(self, style: Style) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the widget stylesheet.

        The stylesheet has four predefined style options: NORMAL, UNDERLINE, and BORDER.

        Args:
        -----
            `style` (Style):
                The style to set for the label. This should be an instance of the `Style` enum,
                which defines the available styles.

        Raises:
        -------
            ValueError:
                If the provided `style` is not a supported style option.

        Example:
        --------
            Set the label stylesheet:
            ```
            self._set_stylesheet(style)
            ```
        """

        # Validate argument type
        if style not in {Style.NORMAL, Style.UNDERLINE, Style.BACKGROUND, Style.BORDER}:
            raise ValueError(f'_set_stylesheet: Unsupported style: {style}. Supported styles are: NORMAL, UNDERLINE, BACKGROUND, BORDER.')

        # Set label style based on style enum
        if style == Style.NORMAL:
            self.setStyleSheet(f"""
                QLabel{{
                    color: {Color.TEXT.value}; /* Label text color */
                    }}
                QLabel:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    }}
                """)
        elif style == Style.UNDERLINE:
            self.setStyleSheet(f"""
                QLabel{{
                    color: {Color.TEXT.value}; /* Label text color */
                    border-bottom: 1px inset {self.underline_color}; /* Underline color */
                    }}
                QLabel:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    }}
                """)
        elif style == Style.BACKGROUND:
            pyflame.print('***Deprecated PyFlameLabel Style.BACKGROUND. Use PyFlameEntry read-only instead.***', text_color=TextColor.RED)
            self.setStyleSheet(f"""
                QLabel{{
                    color: {Color.TEXT.value};
                    background-color: rgb(30, 30, 30);
                    padding-left: 5px;
                    }}
                QLabel:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    }}
                """)
        elif style == Style.BORDER:
            self.setStyleSheet(f"""
                QLabel{{
                    color: {Color.TEXT.value}; /* Label text color */
                    border: 1px solid rgb{Color.TEXT_BORDER.value}; /* Label border */
                    }}
                QLabel:disabled{{
                    color: {Color.TEXT_DISABLED.value}; /* Disabled text color */
                    }}
                """)

class PyFlameLineEdit(PyFlameEntry):
    """
    PyFlameLineEdit
    ===============

    **DEPRECATED**

    Custom QT Flame LineEdit Widget Subclass. This class is deprecated and will be removed in future versions.
    Please use `PyFlameEntry` instead.
    """

    def __init__(self: 'PyFlameLineEdit',
                 text: str,
                 width: int = 150,
                 height: int = 28,
                 max_width: bool = False,
                 text_changed: Optional[Callable] = None,
                 placeholder_text: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 read_only: bool = False,
                 font: str = PYFLAME_FONT,
                 font_size: int = PYFLAME_FONT_SIZE,
                 ) -> None:

        # Issue a deprecation warning to the user
        pyflame.print('***Deprecated PyFlameLineEdit. Use PyFlameEntry instead.***', text_color=TextColor.RED)

        # Call the parent class (PyFlameEntry) __init__ method
        super().__init__(
            text=text,
            width=width,
            height=height,
            max_width=max_width,
            text_changed=text_changed,
            placeholder_text=placeholder_text,
            tooltip=tooltip,
            read_only=read_only,
            font=font,
            font_size=font_size,
        )

class PyFlameLineEditFileBrowser(QtWidgets.QLineEdit):
    """
    PyFlameLineEditFileBrowser
    ==========================

    Custom QT Flame Line Edit File Browser Widget Subclass

    Opens a Flame file browser when clicked on.

    Args:
    -----
        `text` (str):
            PyFlameLineEditFileBrowser text.

        `width` (int, optional):
            PyFlameLineEditFileBrowser width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameLineEditFileBrowser height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameLineEditFileBrowser to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `placeholder_text` (str, optional):
            Temporary text to display when PyFlameLineEditFileBrowser is empty.
            (Default: `None`)

        `browser_type` (BrowserType):
            Type of browser to open. Select from BrowserType.FILE or BrowserType.DIRECTORY.
            (Default: `BrowserType.FILE`)

        `browser_ext` (list, optional):
            List of file extensions to filter by when browser_type is BrowserType.FILE. Ignore if browser_type is BrowserType.DIRECTORY.
            (Default: `[]`)

        `browser_title` (str):
            Title of browser window.
            (Default: `Select File`)

        `browser_window_to_hide` (QtWidgets.QWidget, optional):
            Window to hide when browser is open.
            (Default: `None`)

        `connect` (callable, optional):
            Function to call when text is changed.
            (Default: `None`)

        `font` (str, optional):
            Line edit font.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Line edit font size.
            (Default: `PYFLAME_FONT_SIZE`)

        `font` (str, optional):
            Font family to be used for the text in the entry field.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text in the entry field.
            (Default: `PYFLAME_FONT_SIZE`)

    Attributes:
    -----------
        `path` (str):
            The selected file or directory path.

    Examples:
    ---------
        To create a PyFlameLineEditFileBrowser:
        ```
        path_entry = PyFlameLineEditFileBrowser(
            text=some_path,
            browser_type=BrowserType.FILE,
            browser_ext=[
                'exr',
                ],
            browser_title='Select Image',
            browser_window_to_hide=[self.window],
            )
        ```

        To get path from PyFlameLineEditFileBrowser:
        ```
        path_entry.path
        ```

        To get path from PyFlameLineEditFileBrowser:
        ```
        path_entry.text()
        ```

        To set path in PyFlameLineEditFileBrowser:
        ```
        path_entry.setText('Some text here')
        ```

        To enable/disable PyFlameLineEditFileBrowser:
        ```
        path_entry.setEnabled(True)
        path_entry.setEnabled(False)
        ```

        To set PyFlameLineEditFileBrowser as focus (cursor will be in PyFlameLineEditFileBrowser):
        ```
        path_entry.setFocus()
        ```
    """

    clicked = QtCore.Signal()

    def __init__(self,
                 text: str,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 placeholder_text: Optional[str]=None,
                 browser_type: BrowserType=BrowserType.FILE,
                 browser_ext: List[str]=[],
                 browser_title: str='Select File',
                 browser_window_to_hide: Optional[QtWidgets.QWidget]=None,
                 connect: Optional[Callable[..., None]] = None,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ):
        super().__init__()

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(width, int):
            raise ValueError(f'PyFlameLineEditFileBrowser: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise ValueError(f'PyFlameLineEditFileBrowser: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise ValueError(f'PyFlameLineEditFileBrowser: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif placeholder_text is not None and not isinstance(placeholder_text, str):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid placeholder_text argument: {placeholder_text}. Must be of type str or None.')
        elif not isinstance(browser_type, BrowserType):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid browser_type argument: {browser_type}. Must be an instance of BrowserType Enum. '
                            'Options are: BrowserType.FILE or BrowserType.DIRECTORY.')
        elif not isinstance(browser_ext, list):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid browser_ext argument: {browser_ext}. Must be of type list.')
        elif not isinstance(browser_title, str):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid browser_title argument: {browser_title}. Must be of type str.')
        elif browser_window_to_hide is not None and not isinstance(browser_window_to_hide, list):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid browser_window_to_hide argument: {browser_window_to_hide}. Must be None or of type list.')
        elif not callable(connect):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid connect argument: {connect}. Must be a callable function or method, or None.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlameLineEditFileBrowser: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise ValueError(f'PyFlameLineEditFileBrowser: Invalid font_size argument: {font_size}. Must be of type int.')

        self.path = self.text()

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build line edit
        self.setText(text)
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setReadOnly(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set placeholder text if specified
        if placeholder_text is not None:
            self.setPlaceholderText(placeholder_text)

        # If browser title is not specified, set it based on browser type
        if browser_title == '':
            if browser_type == BrowserType.FILE:
                browser_title = 'Select File'
            elif browser_type == BrowserType.DIRECTORY:
                browser_title = 'Select Directory'

        # Set browser select directory based on browser type
        if browser_type == BrowserType.FILE:
            browser_select_directory = False
        elif browser_type == BrowserType.DIRECTORY:
            browser_select_directory = True

        def open_file_browser():
            """
            Open File Browser
            =================

            Open flame file browser to select file or directory.
            """

            new_path = pyflame.file_browser(
                path=self.text(),
                title=browser_title,
                extension=browser_ext,
                select_directory=browser_select_directory,
                window_to_hide=browser_window_to_hide,
            )

            if new_path:
                self.setText(new_path)
                self.path = new_path

        self.clicked.connect(open_file_browser)

        # Connect to function if one is specified
        if connect:
            self.clicked.connect(connect)

        self._set_stylesheet()

    def _set_stylesheet(self) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the widget stylesheet.

        Example:
        --------
            Set the lineedit stylesheet:
            ```
            self._set_stylesheet()
            ```
        """

        self.setStyleSheet(f"""
            QLineEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(55, 65, 75);
                selection-color: rgb(38, 38, 38);
                selection-background-color: rgb(184, 177, 167);
                border: 1px solid rgb(55, 65, 75);
                padding-left: 5px;
            }}
            QLineEdit:focus{{
                background-color: rgb(73, 86, 99);
            }}
            QLineEdit:hover{{
                border: 1px solid {Color.BORDER.value};
            }}
            QLineEdit:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: {Color.DISABLED_GRAY.value};
                border: 1px solid {Color.DISABLED_GRAY.value};
            }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
        """)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
            return
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Right):
            super().keyPressEvent(event)
        else:
            pass

class PyFlameListWidget(QtWidgets.QListWidget):
    """
    PyFlameListWidget
    =================

    Custom QT Flame List Widget Subclass

    Args:
    -----
        `width` (int, optional):
            PyFlameListWidget width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameListWidget height.
            (Default: `50`)

        `max_width` (bool, optional):
            Set PyFlameListWidget to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `max_height` (bool, optional):
            Set PyFlameListWidget to maximum height. Use if height is being set by layout. Overrides `height` if set to True.
            (Default: `True`)

        `font` (str, optional):
            Font family to be used for the text in the list.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text in the list.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `add_items(items: List[str])`:
            Add a list of strings to the list widget.

    Examples:
    ---------
        To create PyFlameListWidget:
        ```
        list_widget = PyFlameListWidget()
        ```

        To add items to PyFlameListWidget:
        ```
        list_widget.add_items([item1, item2, item3])
        ```

        To enable/disable PyFlameListWidget:
        ```
        list_widget.setEnabled(True)
        list_widget.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlameListWidget',
                 width: int=50,
                 height: int=50,
                 max_width: bool=True,
                 max_height: bool=True,
                 tooltip: Optional[str]=None,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(width, int):
            raise TypeError(f'PyFlameListWidget: Invalid width argument: {width}. Must be of type int.')
        if not isinstance(height, int):
            raise TypeError(f'PyFlameListWidget: Invalid height argument: {height}. Must be of type int.')
        if not isinstance(max_width, bool):
            raise TypeError(f'PyFlameListWidget: Invalid max_width argument: {max_width}. Must be of type bool.')
        if not isinstance(max_height, bool):
            raise TypeError(f'PyFlameListWidget: Invalid max_height argument: {max_height}. Must be of type bool.')
        if tooltip is not None and not isinstance(tooltip, str):
            raise TypeError(f'PyFlameListWidget: Invalid tooltip argument: {tooltip}. Must be of type str or None.')
        if not isinstance(font, str):
            raise TypeError(f'PyFlameListWidget: Invalid font argument: {font}. Must be of type str.')
        if not isinstance(font_size, int):
            raise TypeError(f'PyFlameListWidget: Invalid font_size argument: {font_size}. Must be of type int.')

        # Set label font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build list widget
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        if max_height:
            self.setMaximumHeight(pyflame.gui_resize(3000))
        self.spacing()
        self.setUniformItemSizes(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAlternatingRowColors(True)

        # Set tooltip if specified
        if tooltip is not None:
            self.setToolTip(tooltip)

        # Set stylesheet
        self._set_stylesheet()

    def add_items(self, items: List[str]) -> None:
            """
            Add Items
            =========

            Add a list of strings to PyFlameListWidget.

            Args:
            -----
                `items` (List[str]):
                    The list of strings to be added.

            Raises:
            -------
                TypeError:
                    If `items` is not a list.
                    If `items` is not a list of strings.
            """

            if not isinstance(items, list):
                raise TypeError('PyFlameListWidget: items must be a list of strings.')
            if not all(isinstance(item, str) for item in items):
                raise TypeError('PyFlameListWidget: All items must be strings.')

            self.addItems(items)

    def _set_stylesheet(self) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the PyFlameListWidget stylesheet.

        Example:
        --------
            ```
            self._set_stylesheet()
            ```
        """

        self.setStyleSheet(f"""
            QListWidget{{
                color: {Color.TEXT.value};
                background-color: {Color.ITEM_BACKGROUND_COLOR.value};
                alternate-background-color: {Color.ITEM_ALT_BACKGROUND_COLOR.value};
                outline: 3px {Color.BLACK.value};
                border: 1px solid rgba(0, 0, 0, .2);
                }}
            QListWidget::item{{
                padding-top: {pyflame.gui_resize(5)}px;  /* Increase top padding */
                padding-bottom: {pyflame.gui_resize(5)}px;  /* Increase bottom padding */
                }}
            QListWidget::item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.SELECTED_GRAY.value};
                }}
            QScrollBar::handle{{
                background: {Color.GRAY.value};  /* Scrollbar handle color */
                }}
            QScrollBar:vertical{{
                width: {pyflame.gui_resize(8)}px;  /* Adjust the width of the vertical scrollbar */
                }}
            QScrollBar:horizontal{{
                height: {pyflame.gui_resize(8)}px;  /* Adjust the height of the horizontal scrollbar */
                }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
            """)

class PyFlamePushButton(QtWidgets.QPushButton):
    """
    PyFlamePushButton
    =================

    Custom QT Flame Push Button Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlamePushButton text.

        `button_checked` (bool, optional):
            Set PyFlamePushButton to be checked or unchecked. True for checked, False for unchecked.
            (Default: `False`)

        `connect` (callable, optional):
            Function to be called when PyFlamePushButton is pressed.
            (Default: `None`)

        `width` (int, optional):
            PyFlamePushButton width.
            (Default: `50`)

        `height` (int, optional):
            PyFlamePushButton height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlamePushButton to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `enabled` (bool, optional):
            Set PyFlamePushButton to be enabled or disbaled. True for enabled, False for disabled.
            (Default: `True`)

        `tooltip` (str, optional):
            PyFlamePushButton tooltip text.
            (Default: `None`)

        `font` (str, optional):
            Font family to be used for the text on the button.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text on the button.
            (Default: `PYFLAME_FONT_SIZE`)

    Examples:
    ---------
        To create a PyFlamePushButton:
        ```
        pushbutton = PyFlamePushButton(
            text='Button Name',
            button_checked=False,
            )
        ```

        To get PyFlamePushButton checked state:
        ```
        pushbutton.isChecked()
        ```

        To set PyFlamePushButton checked state:
        ```
        pushbutton.setChecked(True)
        ```

        To enable/disable PyFlamePushButton:
        ```
        pushbutton.setEnabled(True)
        pushbutton.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlamePushButton',
                 text: str,
                 button_checked: bool=False,
                 connect: Optional[Callable[..., None]]=None,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 enabled: bool=True,
                 tooltip: Optional[str]=None,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlamePushButton: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(button_checked, bool):
            raise TypeError(f'PyFlamePushButton: Invalid button_checked argument: {button_checked}. Must be of type bool.')
        elif connect is not None and not callable(connect):
            raise TypeError(f'PyFlamePushButton: Invalid connect argument: {connect}. Must be a callable function or method, or None.')
        elif not isinstance(width, int):
            raise ValueError(f'PyFlamePushButton: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise ValueError(f'PyFlamePushButton: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise ValueError(f'PyFlamePushButton: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif not isinstance(enabled, bool):
            raise TypeError(f'PyFlamePushButton: Invalid enabled argument: {enabled}. Must be of type bool.')
        elif tooltip is not None and not isinstance(tooltip, str):
            raise TypeError(f'PyFlamePushButton: Invalid tooltip argument: {tooltip}. Must be of type str or None.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlamePushButton: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise ValueError(f'PyFlamePushButton: Invalid font_size argument: {font_size}. Must be of type int.')

        # Set button font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build push button
        self.setText(text)
        self.setCheckable(True)
        self.setChecked(button_checked)
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(connect)
        if tooltip is not None:
            self.setToolTip(tooltip)

        # Set button to be enabled or disabled
        self.setEnabled(enabled)

        self._set_stylesheet()

    def _set_stylesheet(self) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the widget stylesheet.

        Example:
        --------
            ```
            self._set_stylesheet()
            ```
        """

        self.setStyleSheet(f"""
            QPushButton{{
                color: {Color.TEXT.value};
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE.value});
                text-align: left;
                border-top: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE.value});
                border-bottom: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE.value});
                border-left: 1px solid {Color.GRAY.value};
                border-right: 1px solid {Color.PUSHBUTTON_BLUE.value};
                padding-left: {pyflame.gui_resize(5)}px;
                }}
            QPushButton:checked{{
                color: {Color.TEXT_SELECTED.value};
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.SELECTED_GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE_CHECKED.value});
                text-align: {Align.LEFT.value};
                border-top: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.SELECTED_GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE_CHECKED.value});
                border-bottom: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.SELECTED_GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE_CHECKED.value});
                border-left: 1px solid {Color.SELECTED_GRAY.value};
                border-right: 1px solid {Color.PUSHBUTTON_BLUE_CHECKED.value};
                padding-left: {pyflame.gui_resize(5)}px;
                font: italic;
                }}
            QPushButton:hover{{
                border: 1px solid {Color.BORDER.value};
                }}
            QPushButton:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: .93 {Color.GRAY.value}, stop: .94 {Color.PUSHBUTTON_BLUE_DISABLED.value});
                font: light;
                border: none;
                }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
            """)

class PyFlamePushButtonMenu(QtWidgets.QPushButton):
    """
    PyFlamePushButtonMenu
    =====================

    Custom QT Flame Menu Push Button Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlamePushButtonMenu text.

        `menu_options` (list):
            Options shown in menu when the PyFlamePushButtonMenu is pressed.

        `width` (int, optional):
            PyFlamePushButtonMenu width.
            (Default: `50`)

        `height` (int, optional):
            PyFlamePushButtonMenu height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlamePushButtonMenu to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `connect` (callable, optional):
            Function to be called when PyFlamePushButtonMenu is changed.
            (Default: `None`)

        `menu_indicator` (bool, optional):
            Show menu indicator arrow.
            (Default: `False`)

        `font` (str, optional):
            Font family to be used for the text on the button.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text on the button.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `update_menu(text, menu_options, connect)`:
            Use to update an existing button menu.

    Examples:
    ---------
        To create a PyFlamePushButtonMenu:
        ```
        menu_push_button = PyFlamePushButtonMenu(
            text='push_button_name',
            menu_options=[
                'Item 1',
                'Item 2',
                'Item 3',
                'Item 4'
                ],
            align=Align.LEFT,
            )
        ```

        To get current PyFlamePushButtonMenu selection:
        ```
        menu_push_button.text()
        ```

        To update an existing PyFlamePushButtonMenu:
        ```
        menu_push_button.update_menu(
            text='Current Menu Selection',
            menu_options=[
                'Item 5',
                'Item 6',
                'Item 7',
                'Item 8'
                ],
            )
        ```
    """

    def __init__(self: 'PyFlamePushButtonMenu',
                 text: str,
                 menu_options: List[str],
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 connect: Optional[Callable[..., None]]=None,
                 enabled: bool=True,
                 menu_indicator: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(menu_options, list):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid menu_options argument: {menu_options}. Must be of type list.')
        elif not isinstance(width, int):
            raise ValueError(f'PyFlamePushButtonMenu: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise ValueError(f'PyFlamePushButtonMenu: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise ValueError(f'PyFlamePushButtonMenu: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif connect is not None and not callable(connect):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid connect argument: {connect}. Must be a callable function or method, or None.')
        elif not isinstance(enabled, bool):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid enabled argument: {enabled}. Must be of type bool.')
        elif not isinstance(menu_indicator, bool):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid menu_indicator argument: {menu_indicator}. Must be of type bool.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise ValueError(f'PyFlamePushButtonMenu: Invalid font_size argument: {font_size}. Must be of type int.')

        # Set button font
        self.font_size = pyflame.font_resize(font_size)
        font = QtGui.QFont(font)
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.font = font

        # Build push button menu
        self.setText(' ' + text) # Add space to text to create padding. Space is removed when text is returned.
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create menus
        self.pushbutton_menu = QtWidgets.QMenu(self)
        self.pushbutton_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushbutton_menu.aboutToShow.connect(self._match_push_button_width) # Match menu width to button width
        self.pushbutton_menu.setMinimumWidth(pyflame.gui_resize(width))

        # Menu stylesheet
        self._set_menu_stylesheet()

        # Add menu options
        for menu in menu_options:
            self.pushbutton_menu.addAction(menu, partial(self._create_menu, menu, connect))

        self.setMenu(self.pushbutton_menu)

        # Set button to be enabled or disabled
        self.setEnabled(enabled)

        self._set_button_stylesheet(menu_indicator)

    def _set_button_stylesheet(self, menu_indicator) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the widget stylesheet, optionally including a menu indicator.

        This private method updates the button's appearance by applying a stylesheet
        that includes styles for various states such as normal, disabled, and hover.
        It also optionally includes a menu indicator based on the `menu_indicator` parameter.

        Args:
        -----
            `menu_indicator (bool)`:
                If True, includes a menu indicator in the PyFlamePushButtonMenu stylesheet. False, hides the menu indicator.

        Raises:
        -------
            TypeError:
                If `menu_indicator` is not a bool.

        Example:
        --------
            ```
            button._set_button_stylesheet(menu_indicator)
            ```
        """

        # Validate argument types
        if not isinstance(menu_indicator, bool):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid menu_indicator argument: {menu_indicator}. Must be of type bool.')


        #### ADD PADDING TO STYLESHEET AND REMOVE SPACE FROM TEXT BEING ADDED TO BUTTON ####
        #### CHERCK ALL METHODS FOR SPACES BEING ADDED TO TEXT ####
        #### REMOVE SPACES ####


        # Set menu indicator to show or hide
        if menu_indicator:
            menu_indicator_style = f"""
            QPushButton::menu-indicator{{
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: {pyflame.gui_resize(15)}px;
                height: {pyflame.gui_resize(15)}px;
                right: {pyflame.gui_resize(10)}px;
            }}
            """
        else:
            menu_indicator_style = f"""
            QPushButton::menu-indicator{{
                image: none;
            }}"""

        self.setStyleSheet(f"""
            QPushButton{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                border: none;
                text-align: left;
                padding-left: {pyflame.gui_resize(2)}px;
                }}
            QPushButton:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: rgb(45, 55, 68);
                border: none;
                }}
            QPushButton:hover{{
                border: 1px solid {Color.BORDER.value};
                padding-left: {pyflame.gui_resize(1)}px;
                }}
            QToolTip{{
                color: {Color.WHITE.value};
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value};
                }}
                {menu_indicator_style} # Insert menu indicator style
            """)

    def _set_menu_stylesheet(self) -> None:
        """
        Set Stylesheet
        ==============

        This private method sets the PyFlamePushButtonMenu stylesheet.

        Example:
        --------
            ```
            self._set_menu_stylesheet()
            ```
        """

        self.pushbutton_menu.setStyleSheet(f"""
            QMenu{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                border: none;
                font: {self.font_size}px "Discreet";
                }}
            QMenu::item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: rgb(58, 69, 81);
                }}
            """)

    def _match_push_button_width(self):

        self.pushbutton_menu.setMinimumWidth(self.size().width())

    def _create_menu(self, menu, connect):

        self.setText(' ' + menu) # Add space to text to create padding. Space is removed when text is returned.

        # Add connect to menu
        if connect:
            connect()

    def update_menu(self, text: str, menu_options: List[str], connect=None):
        """
        Update Menu
        ===========

        This method is used to update an existing PyFlamePushButtonMenu menu.

        Args:
        -----
            `text` (str):
                Set PyFlamePushButtonMenu text.

            `menu_options` (List[str]):
                The list of menu options to be added to the PyFlamePushButtonMenu menu.

            `connect` (callable, optional):
                Function to be called when PyFlamePushButtonMenu is changed.
                (Default: `None`)

        Example:
        --------
        ```
        menu_push_button.update_menu(
            text='Current Menu Selection',
            menu_options=[
                new_option1,
                new_option2,
                new_option3
                ],
            )
        ```

        Raises:
        -------
            TypeError:
                If `text` is not a string.
                If `menu_options` is not a list.
                If `menu_options` is not a list of strings
                If `connect` is not None or a callable function or method.
        """

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(menu_options, list):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid menu_options argument: {menu_options}. Must be of type list.')
        elif not all(isinstance(menu, str) for menu in menu_options):
            raise TypeError(f'PyFlamePushButtonMenu: All menu_options must be strings.')
        elif connect is not None and not callable(connect):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid connect argument: {connect}. Must be a callable function or method, or None.')

        # Set button text
        self.set_text(' ' + text) # Add space to text to create padding. Space is removed when text is returned.

        # Clear existing menu options
        self.pushbutton_menu.clear()

        # Add new menu options
        for menu in menu_options:
            self.pushbutton_menu.addAction(menu, partial(self._create_menu, menu, connect))

    def setText(self, text: str) -> None:
        """
        Set Text
        ========

        Public method that sets the button's text with a space added to the beginning to create padding.

        Note:
        -----
        This method is retained for backwards compatibility. The new method to use is `set_text`.

        Args:
        -----
            `text` (str):
                Set PyFlamePushButtonMenu text.

        Raises:
        -------
            TypeError:
                If `text` is not a string.

        Example:
        --------
        ```
        push_button.setText('Button Name')
        ```
        """

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid text argument: {text}. Must be of type str.')

        # Strip leading and trailing whitespace
        text = text.strip()

        # Set button text
        super().setText(' ' + text)

    def set_text(self, text: str) -> None:
        """
        Set Text
        ========

        Public method that sets the button's text with a space added to the beginning to create padding.

        This method is an alias for setText. Alias is used to maintain consistency with other PyFlame widgets.

        Args:
        -----
            `text` (str):
                Set PyFlamePushButtonMenu text.

        Raises:
        -------
            TypeError:
                If `text` is not a string.

        Example:
        --------
        ```
        push_button.set_text('Button Name')
        ```
        """

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid text argument: {text}. Must be of type str.')

        # Set text using setText
        self.setText(text)

    def text(self) -> str:
        """
        Text
        ====

        Publid method that returns the PyFlamePushButtonMenu's text with the first character (space that is added to button text) removed.

        Returns:
            str: The PyFlamePushButtonMenu text without the first character.
        """

        current_text = super().text()
        return current_text[1:] if current_text else ''

class PyFlameColorPushButtonMenu(QtWidgets.QPushButton):
    """
    PyFlameColorPushButtonMenu
    ==========================

    Custom QT Flame Color Push Button Menu Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlameColorPushButtonMenu text.

        `menu_options` (list):
            Options shown in menu when PyFlameColorPushButtonMenu is pressed.

        `width` (int, optional):
            PyFlameColorPushButtonMenu width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameColorPushButtonMenu height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameColorPushButtonMenu to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `color_options` (dict, optional):
            Color options and their normalized RGB values. Values must be in the range of 0.0 to 1.0.
            When None is passed, the default color options are used.
            (Default: `None`)

        `menu_indicator` (bool, optional):
            Show menu indicator arrow.
            (Default: `False`)

        `font` (str, optional):
            Font family to be used for the text on the button.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text on the button.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `color_value()`:
            Return normalized RGB color value of selected color.

    Examples:
    ---------
        To create a PyFlameColorPushButtonMenu:
        ```
        color_pushbutton = PyFlameColorPushButtonMenu(
            text='Red',
            )
        ```

        To get selected color value:
        ```
        color_pushbutton.color_value()
        ```

        To get current PyFlameColorPushButtonMenu text:
        ```
        color_pushbutton.text()
        ```
    """

    def __init__(self,
                 text: str,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 color_options: Optional[Dict[str, Tuple[float, float, float]]]=None,
                 menu_indicator: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        if color_options is None:  # Initialize with default if None
            color_options = {
                'Red': (0.310, 0.078, 0.078),
                'Green': (0.125, 0.224, 0.165),
                'Bright Green': (0.118, 0.396, 0.196),
                'Blue': (0.176, 0.227, 0.322),
                'Light Blue': (0.227, 0.325, 0.396),
                'Purple': (0.318, 0.263, 0.424),
                'Orange': (0.467, 0.290, 0.161),
                'Gold': (0.380, 0.380, 0.235),
                'Yellow': (0.592, 0.592, 0.180),
                'Grey': (0.537, 0.537, 0.537),
                'Black': (0.0, 0.0, 0.0),
                }

        # Validate argument types
        if text not in color_options:
            raise ValueError(f'PyFlameColorPushButtonMenu: Invalid text argument: {text}. Must be one of the following: {", ".join(color_options.keys())}')
        elif not isinstance(width, int):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif color_options is None and not isinstance(color_options, dict):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid color_options argument: {color_options}. Must be of type dict.')
        elif not isinstance(menu_indicator, bool):
            raise TypeError(f'PyFlamePushButtonMenu: Invalid menu_indicator argument: {menu_indicator}. Must be of type bool.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise TypeError(f'PyFlameColorPushButtonMenu: Invalid font_size argument: {font_size}. Must be of type int.')
        for color, rgb_values in color_options.items():
            if not isinstance(rgb_values, tuple) or len(rgb_values) != 3:
                raise ValueError(f"Color '{color}' does not have a valid RGB value tuple of length 3.")
            if not all(isinstance(value, (float, int)) and 0.0 <= value <= 1.0 for value in rgb_values):
                raise ValueError(f"RGB values for '{color}' must be floats or ints between 0.0 and 1.0. Got: {rgb_values}")

        # Color options and their RGB values
        self.color_options = color_options

        # Set button font
        self.font_size = pyflame.font_resize(font_size)
        font = QtGui.QFont(font)
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.font = font

        # Generate and set the initial color icon based on the provided text
        initial_color_value = self.color_options[text]
        self.setIcon(self._generate_color_icon(initial_color_value))
        self.setIconSize(QtCore.QSize(self.font_size, self.font_size))  # Adjust size as needed

        # Build push button menu
        self.setText(text)
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create push button menu
        self.pushbutton_menu = QtWidgets.QMenu(self)
        self.pushbutton_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushbutton_menu.setMinimumWidth(width)

        # Add color menu options
        for color_name, color_value in self.color_options.items():
            icon = self._generate_color_icon(color_value)
            action = QAction(icon, color_name, self)
            action.triggered.connect(partial(self._create_menu, color_name))
            self.pushbutton_menu.addAction(action)

        self.setMenu(self.pushbutton_menu)

        # Set widget stylesheet
        self._set_button_stylesheet(menu_indicator)

        # Menu stylesheet
        self._set_menu_stylesheet()

    def color_value(self) -> Tuple[float, float, float]:
        """
        Color Value
        ===========

        This method retrieves the RGB color value corresponding to the current text
        of the button. The color value is returned as a tuple of three floats.

        Returns:
        --------
            Tuple[float, float, float]:
                The RGB color value as a tuple.

        Raises:
        -------
            ValueError:
                If the current text of the button does not correspond to any color option.

        Example:
        --------
            Get the RGB color value of the PyFlameColorPushButtonMenu's currently selected color:
            ```
            rgb_value = button.color_value()
            ```
        """

        current_text = self.text()
        if current_text in self.color_options:
            return self.color_options[current_text]
        else:
            # Handle the error case where the button's text does not match any color option
            raise ValueError(f'"{current_text}" is not a valid color option.')

    def _generate_color_icon(self, color_value: Tuple[float, float, float]) -> QtGui.QIcon:
        """
        Generate Color Icon
        ===================

        This private method generates a color icon based on the given color value.
        The size of the icon is based on the widget font size.

        Args:
        -----
            `color_value` (Tuple[float, float, float]):
                The RGB color value, where each float is between 0 and 1.

        Returns:
        --------
            QtGui.QIcon:
                The generated color icon.

        Raises:
        -------
            TypeError:
                If `color_value` is not a tuple.
            ValueError:
                If `color_value` does not contain exactly three float values between 0 and 1.

        Example:
        --------
            Generate an icon for the color red:
            ```
            red_icon = widget._generate_color_icon((1.0, 0.0, 0.0))
            ```
        """

        # Validate argument types
        if not isinstance(color_value, tuple):
            raise TypeError(f'_generate_color_icon: Invalid type for color_value: {type(color_value)}. Must be a tuple.')
        if len(color_value) != 3 or not all(isinstance(c, float) and 0 <= c <= 1 for c in color_value):
            raise ValueError(f'_generate_color_icon: Invalid value for color_value: {color_value}. Must be a tuple of three floats between 0 and 1.')

        # Create the pixmap and fill with the given color
        pixmap = QtGui.QPixmap(self.font_size, self.font_size)  # Size of the color square
        pixmap.fill(QtGui.QColor(*[int(c * 255) for c in color_value]))  # Convert color values to 0-255 range
        return QtGui.QIcon(pixmap)

    def _create_menu(self, color_name) -> None:
        """
        Create Menu
        ===========

        This private method updates the button's text and icon to reflect the selected color.

        Args:
        -----
            `color_name (str)`:
                The name of the color to set for the button.

        Raises:
        -------
            TypeError:
                If `color_name` is not a string.
            ValueError:
                If `color_name` does not correspond to any available color option.

        Example:
        --------
            Update the button to reflect the color 'red':
            ```
            button._create_menu('red')
            ```
        """

        # Validate argument types
        if not isinstance(color_name, str):
            raise TypeError(f'_create_menu: Invalid type for color_name: {type(color_name)}. Must be a string.')
        if color_name not in self.color_options:
            raise ValueError(f'_create_menu: Invalid color_name: "{color_name}". Must be one of the available color options.')

        # Update the button's text and icon
        self.setText(color_name)
        icon = self._generate_color_icon(self.color_options[color_name])
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(self.font_size, self.font_size))


    def _set_button_stylesheet(self, menu_indicator) -> None:
        """
        Set Button Stylesheet
        =====================

        This private method sets the PyFlameColorPushButtonMenu stylesheet.
        """

        # Set menu indicator style
        if menu_indicator:
            menu_indicator_style =f"""
            QPushButton::menu-indicator{{
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: {pyflame.gui_resize(15)}px;
                height: {pyflame.gui_resize(15)}px;
                right: {pyflame.gui_resize(10)}px;
            }}
            """
        else:
            # Hide the menu indicator by setting its image to none
            menu_indicator_style = """
            QPushButton::menu-indicator{
                image: none;
                }"""

        self.setStyleSheet(f"""
            QPushButton{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                border: none;
                text-align: left;
                left: {pyflame.gui_resize(10)}px;
                }}
            QPushButton:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: rgb(45, 55, 68);
                border: none;
                }}
            QPushButton:hover{{
                border: 1px solid {Color.BORDER.value};
                }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
            {menu_indicator_style} # Insert menu indicator style
            """)

    def _set_menu_stylesheet(self) -> None:
        """
        Set Menu Stylesheet
        ===================

        This private method sets the PyFlameColorPushButtonMenu menu stylesheet.
        """

        self.pushbutton_menu.setStyleSheet(f"""
            QMenu{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                text-align: center;
                border: none;
                font: {self.font_size}px "Discreet";
                }}
            QMenu::item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: rgb(58, 69, 81);
                }}
            """)

class PyFlameSlider(QtWidgets.QLineEdit):
    """
    PyFlameSlider
    =============

    Custom QT Line Edit Widget Subclass

    Args:
    -----
        `start_value` (int or float):
            Initial value.

        `min_value` (int or float):
            Minimum value.

        `max_value` (int or float):
            Maximum value.

        `value_is_float` (bool, optional):
            If True, the value is float.
            (Default: `False`)

        `rate` (int or float, optional):
            Slider sensitivity. The value should be between 1 and 10. Lower values are more sensitive.
            (Default: `10`)

        `width` (int, optional):
            PyFlameSlider width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameSlider height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set PyFlameSlider to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `connect` (callable, optional):
            Function to call when value is changed.
            (Default: `None`)

        `font` (str, optional):
            Font family to be used for the text in the slider.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text in the slider.
            (Default: `PYFLAME_FONT_SIZE`)

        `tooltip` (str, optional):
            PyFlameSlider tooltip text.
            (Default: `None`)

    Methods:
    --------
        `get_value()`:
            Return the PyFlameSlider value as an integer or float.

    Examples:
    ---------
        To create a PyFlameSlider:
        ```
        slider = PyFlameSlider(
            start_value=0,
            min_value=-20,
            max_value=20,
            )
        ```

        To return the PyFlameSlider value as an integer or float:
        ```
        slider.get_value()
        ```

        To return the PyFlameSlider value as a string:
        ```
        slider.text()
        ```

        To enable/disable PyFlameSlider:
        ```
        slider.setEnabled(True)
        slider.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlameSlider',
                 start_value: int,
                 min_value: int,
                 max_value: int,
                 value_is_float: bool=False,
                 rate: Union[int, float]=10,
                 width: int=50,
                 height: int=28,
                 max_width: bool=True,
                 connect=None,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 tooltip: Optional[str]=None,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(start_value, (int, float)):
            raise TypeError(f'PyFlameSlider: Invalid start_value argument: {start_value}. Must be of type int or float.')
        elif not isinstance(min_value, (int, float)):
            raise TypeError(f'PyFlameSlider: Invalid min_value argument: {min_value}. Must be of type int or float.')
        elif not isinstance(max_value, (int, float)):
            raise TypeError(f'PyFlameSlider: Invalid max_value argument: {max_value}. Must be of type int or float.')
        elif not isinstance(value_is_float, bool):
            raise TypeError(f'PyFlameSlider: Invalid value_is_float argument: {value_is_float}. Must be of type bool.')
        elif not isinstance(rate, (int, float)) or rate < 1 or rate > 10:
            raise TypeError(f'PyFlameSlider: Invalid rate argument: {rate}. Must be of type int or float between 1 and 10.')
        elif not isinstance(width, int):
            raise TypeError(f'PyFlameSlider: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise TypeError(f"PyFlameSlider: Expected 'max_width' to be a bool, got {type(max_width).__name__} instead.")
        elif not isinstance(height, int):
            raise TypeError(f'PyFlameSlider: Invalid height argument: {height}. Must be of type int.')
        elif connect is not None and not callable(connect):
            raise TypeError(f'PyFlameSlider: Invalid connect argument: {connect}. Must be a callable function or method, or None.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlameSlider: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise TypeError(f'PyFlameSlider: Invalid font_size argument: {font_size}. Must be of type int.')
        elif tooltip is not None and not isinstance(tooltip, str):
            raise TypeError(f'PyFlameSlider: Invalid tooltip argument: {tooltip}. Must be of type str or None.')

        # Set slider font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size + 1))
        self.font = font
        self.setFont(self.font)

        # Scale button size for screen resolution
        self.width = pyflame.gui_resize(width)
        self.height = pyflame.gui_resize(height)

        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        else:
            self.setMinimumWidth(self.width)
            self.setMaximumWidth(self.width)

        # Build slider
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumHeight(self.height)

        if tooltip is not None:
            self.setToolTip(tooltip)

        if value_is_float:
            self.spinbox_type = 'Float'
        else:
            self.spinbox_type = 'Integer'

        self.rate = rate *.1
        self.min = min_value
        self.max = max_value
        self.steps = 1
        self.value_at_press = None
        self.pos_at_press = None
        self.setValue(start_value)
        self.setReadOnly(True)
        self.textChanged.connect(self.value_changed)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._set_stylesheet()

        self.clearFocus()

        class Slider(QtWidgets.QSlider):

            def __init__(self, start_value, min_value, max_value, width):
                super(Slider, self).__init__()

                self.setMaximumHeight(pyflame.gui_resize(4))
                #self.setMinimumWidth(width)
                #self.setMaximumWidth(width)
                self.setMinimum(min_value)
                self.setMaximum(max_value)
                self.setValue(start_value)
                self.setOrientation(QtCore.Qt.Horizontal)

                # Slider stylesheet

                self.setStyleSheet(f"""
                    QSlider{{
                        color: rgb(55, 65, 75);
                        background-color: rgb(39, 45, 53);
                        }}
                    QSlider::groove{{
                        color: rgb(39, 45, 53);
                        background-color: rgb(39, 45, 53);
                        }}
                    QSlider::handle:horizontal{{
                        background-color: rgb(102, 102, 102);
                        width: {pyflame.gui_resize(3)}px;
                        }}
                    QSlider::disabled{{
                        color: {Color.TEXT_DISABLED.value};
                        background-color: rgb(55, 65, 75);
                        }}
                    """)

                self.setDisabled(True)
                self.raise_()

        def set_slider():
            slider666.setValue(float(self.text()))
            slider666.setFont(self.font)

        slider666 = Slider(start_value, min_value, max_value, pyflame.gui_resize(width))
        self.textChanged.connect(set_slider)

        self.textChanged.connect(connect) # Connect to function when slider value is changed

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(slider666)
        self.vbox.setContentsMargins(0, pyflame.gui_resize(24), 0, 0)

    def _set_stylesheet(self) -> None:

        # Slider stylesheet
        self.setStyleSheet(f"""
            QLineEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(55, 65, 75);
                selection-color: rgb(38, 38, 38);
                selection-background-color: rgb(184, 177, 167);
                border: none;
                padding-left: 5px;
                }}
            QLineEdit:hover{{
                border: 1px solid {Color.BORDER.value};
                }}
            QLineEdit:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: rgb(55, 65, 75);
                }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
            """)

    def get_value(self):
        """
        Returns the slider's current value as an int or float.

        If the slider's value is of type 'Integer', this method will return the value as an int.
        Otherwise, the value will be returned as a float.

        Returns:
            Union[int, float]:
                The current slider value.
        """
        if self.spinbox_type == 'Integer':
            return int(self.text())
        else:
            return float(self.text())

    def _calculator(self):

        def clear():
            calc_lineedit.setText('')

        def button_press(key):

            if self.clean_line == True:
                calc_lineedit.setText('')

            calc_lineedit.insert(key)

            self.clean_line = False

        def plus_minus():

            if calc_lineedit.text():
                calc_lineedit.setText(str(float(calc_lineedit.text()) * -1))

        def add_sub(key):

            if calc_lineedit.text() == '':
                calc_lineedit.setText('0')

            if '**' not in calc_lineedit.text():
                try:
                    calc_num = eval(calc_lineedit.text().lstrip('0'))

                    calc_lineedit.setText(str(calc_num))

                    calc_num = float(calc_lineedit.text())

                    if calc_num == 0:
                        calc_num = 1
                    if key == 'add':
                        self.setValue(float(self.text()) + float(calc_num))
                    else:
                        self.setValue(float(self.text()) - float(calc_num))

                    self.clean_line = True
                except:
                    pass

        def enter():

            if self.clean_line == True:
                return calc_window.close()

            if calc_lineedit.text():
                try:

                    # If only single number set slider value to that number

                    self.setValue(float(calc_lineedit.text()))
                except:

                    # Do math

                    new_value = calculate_entry()
                    self.setValue(float(new_value))

            close_calc()

        def equals():

            if calc_lineedit.text() == '':
                calc_lineedit.setText('0')

            if calc_lineedit.text() != '0':

                calc_line = calc_lineedit.text().lstrip('0')
            else:
                calc_line = calc_lineedit.text()

            if '**' not in calc_lineedit.text():
                try:
                    calc = eval(calc_line)
                except:
                    calc = 0

                calc_lineedit.setText(str(calc))
            else:
                calc_lineedit.setText('1')

        def calculate_entry():

            calc_line = calc_lineedit.text().lstrip('0')

            if '**' not in calc_lineedit.text():
                try:
                    if calc_line.startswith('+'):
                        calc = float(self.text()) + eval(calc_line[-1:])
                    elif calc_line.startswith('-'):
                        calc = float(self.text()) - eval(calc_line[-1:])
                    elif calc_line.startswith('*'):
                        calc = float(self.text()) * eval(calc_line[-1:])
                    elif calc_line.startswith('/'):
                        calc = float(self.text()) / eval(calc_line[-1:])
                    else:
                        calc = eval(calc_line)
                except:
                    calc = 0
            else:
                calc = 1

            calc_lineedit.setText(str(float(calc)))

            return calc

        def close_calc():

            calc_window.close()

            self.setStyleSheet(f"""
                QLineEdit{{
                    color: {Color.TEXT.value};
                    background-color: rgb(55, 65, 75);
                    selection-color: {Color.TEXT.value};
                    selection-background-color: rgb(55, 65, 75);
                    border: none;
                    padding-left: 5px;
                    }}
                QLineEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    }}
                """)

        def revert_color():

            self.setStyleSheet(f"""
                QLineEdit{{
                    color: {Color.TEXT.value};
                    background-color: rgb(55, 65, 75);
                    selection-color: {Color.TEXT.value};
                    selection-background-color: rgb(55, 65, 75);
                    border: none;
                    padding-left: 5px;
                    }}
                QLineEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    }}
                """)

        self.clean_line = False

        calc_window = QtWidgets.QWidget()
        calc_window.setMinimumSize(QtCore.QSize(210, 280))
        calc_window.setMaximumSize(QtCore.QSize(210, 280))
        calc_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        calc_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        calc_window.destroyed.connect(revert_color)
        calc_window.move(QtGui.QCursor.pos().x() - 110, QtGui.QCursor.pos().y() - 290)
        calc_window.setStyleSheet(f"""
            background-color: rgb(36, 36, 36)
        """)

        # Label
        calc_label = QtWidgets.QLabel('Calculator', calc_window)
        calc_label.setAlignment(QtCore.Qt.AlignCenter)
        calc_label.setMinimumHeight(28)
        font = QtGui.QFont(PYFLAME_FONT)
        font.setPointSize(pyflame.font_resize(PYFLAME_FONT_SIZE))
        calc_label.setFont(font)
        calc_label.setStyleSheet(f"""
            color: {Color.TEXT.value};
            background-color: rgb(57, 57, 57);
        """)

        #  LineEdit
        calc_lineedit = QtWidgets.QLineEdit('', calc_window)
        calc_lineedit.setMinimumHeight(28)
        calc_lineedit.setFocus()
        calc_lineedit.returnPressed.connect(enter)
        calc_lineedit.setFont(font)
        calc_lineedit.setStyleSheet(f"""
            QLineEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(55, 65, 75);
                selection-color: rgb(38, 38, 38);
                selection-background-color: rgb(184, 177, 167);
                border: none;
                padding-left: 5px;
                }}
            """)

        # Limit input to numbers and math symbols
        try:
            from PySide6.QtCore import QRegularExpression
            from PySide6.QtGui import QRegularExpressionValidator as QValidator
        except ImportError:
            from PySide2.QtCore import QRegExp as QRegularExpression
            from PySide2.QtGui import QRegExpValidator as QValidator

        regex = QRegularExpression('[0-9_,=,/,*,+,\-,.]+')
        validator = QValidator(regex)
        calc_lineedit.setValidator(validator)

        # Buttons
        def calc_null():
            # For blank button - this does nothing
            pass

        class FlameButton(QtWidgets.QPushButton):

            def __init__(self, text, size_x, size_y, connect, parent, *args, **kwargs):
                super(FlameButton, self).__init__(*args, **kwargs)

                self.setText(text)
                self.setParent(parent)
                self.setMinimumSize(size_x, size_y)
                self.setMaximumSize(size_x, size_y)
                self.setFocusPolicy(QtCore.Qt.NoFocus)
                self.clicked.connect(connect)

                # Set button font
                font = QtGui.QFont(PYFLAME_FONT)
                font.setPointSize(pyflame.font_resize(PYFLAME_FONT_SIZE))
                self.setFont(font)

                self.setStyleSheet(f"""
                    QPushButton{{
                        color: {Color.TEXT.value};
                        background-color: {Color.GRAY.value};
                        border: none;
                        }}
                    QPushButton:hover{{
                        border: 1px solid {Color.BORDER.value};
                        }}
                    QPushButton:pressed{{
                        color: rgb(159, 159, 159);
                        background-color: rgb(66, 66, 66);
                        border: none;
                        }}
                    QPushButton:disabled{{
                        color: {Color.TEXT_DISABLED.value};
                        background-color: {Color.GRAY.value};
                        border: none;
                        }}
                    """)

        blank_button = FlameButton('', 40, 28, calc_null, calc_window)
        blank_button.setDisabled(True)
        plus_minus_button = FlameButton('+/-', 40, 28, plus_minus, calc_window)
        plus_minus_button.setStyleSheet(f"""
            color: {Color.TEXT.value};
            background-color: rgb(45, 55, 68);
        """)

        add_button = FlameButton('Add', 40, 28, (partial(add_sub, 'add')), calc_window)
        sub_button = FlameButton('Sub', 40, 28, (partial(add_sub, 'sub')), calc_window)

        #  --------------------------------------- #

        clear_button = FlameButton('C', 40, 28, clear, calc_window)
        equal_button = FlameButton('=', 40, 28, equals, calc_window)
        div_button = FlameButton('/', 40, 28, (partial(button_press, '/')), calc_window)
        mult_button = FlameButton('/', 40, 28, (partial(button_press, '*')), calc_window)

        #  --------------------------------------- #

        _7_button = FlameButton('7', 40, 28, (partial(button_press, '7')), calc_window)
        _8_button = FlameButton('8', 40, 28, (partial(button_press, '8')), calc_window)
        _9_button = FlameButton('9', 40, 28, (partial(button_press, '9')), calc_window)
        minus_button = FlameButton('-', 40, 28, (partial(button_press, '-')), calc_window)

        #  --------------------------------------- #

        _4_button = FlameButton('4', 40, 28, (partial(button_press, '4')), calc_window)
        _5_button = FlameButton('5', 40, 28, (partial(button_press, '5')), calc_window)
        _6_button = FlameButton('6', 40, 28, (partial(button_press, '6')), calc_window)
        plus_button = FlameButton('+', 40, 28, (partial(button_press, '+')), calc_window)

        #  --------------------------------------- #

        _1_button = FlameButton('1', 40, 28, (partial(button_press, '1')), calc_window)
        _2_button = FlameButton('2', 40, 28, (partial(button_press, '2')), calc_window)
        _3_button = FlameButton('3', 40, 28, (partial(button_press, '3')), calc_window)
        enter_button = FlameButton('Enter', 40, 61, enter, calc_window)

        #  --------------------------------------- #

        _0_button = FlameButton('0', 89, 28, (partial(button_press, '0')), calc_window)
        point_button = FlameButton('.', 40, 28, (partial(button_press, '.')), calc_window)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setVerticalSpacing(5)
        grid_layout.setHorizontalSpacing(5)

        grid_layout.addWidget(calc_label, 0, 0, 1, 4)

        grid_layout.addWidget(calc_lineedit, 1, 0, 1, 4)

        grid_layout.addWidget(blank_button, 2, 0)
        grid_layout.addWidget(plus_minus_button, 2, 1)
        grid_layout.addWidget(add_button, 2, 2)
        grid_layout.addWidget(sub_button, 2, 3)

        grid_layout.addWidget(clear_button, 3, 0)
        grid_layout.addWidget(equal_button, 3, 1)
        grid_layout.addWidget(div_button, 3, 2)
        grid_layout.addWidget(mult_button, 3, 3)

        grid_layout.addWidget(_7_button, 4, 0)
        grid_layout.addWidget(_8_button, 4, 1)
        grid_layout.addWidget(_9_button, 4, 2)
        grid_layout.addWidget(minus_button, 4, 3)

        grid_layout.addWidget(_4_button, 5, 0)
        grid_layout.addWidget(_5_button, 5, 1)
        grid_layout.addWidget(_6_button, 5, 2)
        grid_layout.addWidget(plus_button, 5, 3)

        grid_layout.addWidget(_1_button, 6, 0)
        grid_layout.addWidget(_2_button, 6, 1)
        grid_layout.addWidget(_3_button, 6, 2)
        grid_layout.addWidget(enter_button, 6, 3, 2, 1)

        grid_layout.addWidget(_0_button, 7, 0, 1, 2)
        grid_layout.addWidget(point_button, 7, 2)

        calc_window.setLayout(grid_layout)

        calc_window.show()

    def value_changed(self):

        # If value is greater or less than min/max values set values to min/max

        if int(self.value()) < self.min:
            self.setText(str(self.min))
        if int(self.value()) > self.max:
            self.setText(str(self.max))

    def mousePressEvent(self, event):

        if event.buttons() == QtCore.Qt.LeftButton:
            self.value_at_press = self.value()
            self.pos_at_press = event.pos()
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
            self.setFont(self.font)
            self.setStyleSheet(f"""
                QLineEdit{{
                    color: {Color.TEXT_SELECTED.value};
                    background-color: rgb(73, 86, 99);
                    selection-color: {Color.TEXT.value};
                    selection-background-color: rgb(73, 86, 99);
                    border: none; padding-left: 5px;
                    }}
                QLineEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    }}
                """)

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            # Open calculator if button is released within 10 pixels of button click

            if event.pos().x() in range((self.pos_at_press.x() - 10), (self.pos_at_press.x() + 10)) and event.pos().y() in range((self.pos_at_press.y() - 10), (self.pos_at_press.y() + 10)):
                self._calculator()
            else:
                self.setStyleSheet(f"""
                    QLineEdit{{
                        color: {Color.TEXT.value};
                        background-color: rgb(55, 65, 75);
                        selection-color: {Color.TEXT.value};
                        selection-background-color: rgb(55, 65, 75);
                        border: none;
                        padding-left: 5px;
                        }}
                    QLineEdit:hover{{
                        border: 1px solid {Color.BORDER.value};
                        }}
                    """)

            self.value_at_press = None
            self.pos_at_press = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            return

        super(PyFlameSlider, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):

        if event.buttons() != QtCore.Qt.LeftButton:
            return

        if self.pos_at_press is None:
            return

        steps_mult = self.getStepsMultiplier(event)
        delta = event.pos().x() - self.pos_at_press.x()

        if self.spinbox_type == 'Integer':
            delta /= 10 * self.rate # Make movement less sensiteve.
        else:
            delta /= 100 * self.rate
        delta *= self.steps * steps_mult

        value = self.value_at_press + delta
        self.setValue(value)

        super(PyFlameSlider, self).mouseMoveEvent(event)

    def getStepsMultiplier(self, event):

        steps_mult = 1

        if event.modifiers() == QtCore.Qt.CTRL:
            steps_mult = 10
        elif event.modifiers() == QtCore.Qt.SHIFT:
            steps_mult = 0.10

        return steps_mult

    def setMinimum(self, value):

        self.min = value

    def setMaximum(self, value):

        self.max = value

    def setSteps(self, steps):

        if self.spinbox_type == 'Integer':
            self.steps = max(steps, 1)
        else:
            self.steps = steps

    def value(self):

        if self.spinbox_type == 'Integer':
            return int(self.text())
        else:
            return float(self.text())

    def setValue(self, value):

        if self.min is not None:
            value = max(value, self.min)

        if self.max is not None:
            value = min(value, self.max)

        if self.spinbox_type == 'Integer':
            self.setText(str(int(value)))
        else:
            # Keep float values to two decimal places

            self.setText('%.2f' % float(value))

class PyFlameTextEdit(QtWidgets.QTextEdit):
    """
    PyFlameTextEdit
    ===============

    Custom QT Flame Text Edit Widget Subclass

    Args:
    -----
        `text` (str):
            PyFlameTextEdit text.

        `width` (int, optional):
            PyFlameTextEdit width.
            (Default: `50`)

        `height` (int, optional):
            PyFlameTextEdit height.
            (Default: `50`)

        `max_width` (bool, optional):
            Set PyFlameTextEdit to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `max_height` (bool, optional):
            Set PyFlameTextEdit to maximum height. Use if height is being set by layout. Overrides `height` if set to True.
            (Default: `True`)

        `read_only` (bool, optional):
            Text in PyFlameTextEdit is read only.
            (Default: `False`)

        `font` (str, optional):
            Font family to be used for the text.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `text()`:
            Returns PyFlameTextEdit text.

        `setText(text)`:
            Sets the text in the PyFlameTextEdit.

    Examples:
    ---------
        To create a PyFlameTextEdit:
        ```
        text_edit = PyFlameTextEdit(
            text='Some text here',
            read_only=True,
            )
        ```

        To get text from PyFlameTextEdit:
        ```
        text_edit.text()
        ```

        To set text in PyFlameTextEdit:
        ```
        text_edit.setText('Some text here')
        ```

        To enable/disable PyFlameTextEdit:
        ```
        text_edit.setEnabled(True)
        text_edit.setEnabled(False)
        ```
    """

    def __init__(self: 'PyFlameTextEdit',
                 text: str,
                 width: int=50,
                 height: int=50,
                 max_width: Optional[bool]=True,
                 max_height: Optional[bool]=True,
                 read_only: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(text, str):
            raise TypeError(f'PyFlameTextEdit: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(width, int):
            raise TypeError(f'PyFlameTextEdit: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise TypeError(f'PyFlameTextEdit: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise TypeError(f'PyFlameTextEdit: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif not isinstance(max_height, bool):
            raise TypeError(f'PyFlameTextEdit: Invalid max_height argument: {max_height}. Must be of type bool.')
        elif not isinstance(read_only, bool):
            raise TypeError(f'PyFlameTextEdit: Invalid read_only argument: {read_only}. Must be of type bool.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlameTextEdit: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise TypeError(f'PyFlameTextEdit: Invalid font_size argument: {font_size}. Must be of type int.')

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Build text edit
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        if max_height:
            self.setMaximumHeight(pyflame.gui_resize(3000))
        self.setText(text)
        self.setReadOnly(read_only)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._set_text_edit_style(read_only)

    def _set_text_edit_style(self, read_only: bool):
        """
        Set Text Edit Stylesheet
        ========================

        This private method sets the PyFlameTextEdit stylesheet.
        """

        if read_only:
            self.setStyleSheet(f"""
                QTextEdit{{
                    color: {Color.TEXT.value};
                    background-color: {Color.TEXT_READ_ONLY_BACKGROUND.value};
                    selection-color: rgb(38, 38, 38);
                    selection-background-color: rgb(184, 177, 167);
                    border: none;
                    padding-left: 1px;
                    }}
                QTextEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    padding-left: 1px;
                    }}
                QScrollBar::handle{{
                    background: {Color.SCROLLBAR_HANDLE.value};
                    }}
                QScrollBar:vertical{{
                    width: {pyflame.gui_resize(8)}px;  /* Adjust the width of the vertical scrollbar */
                    }}
                QScrollBar:horizontal{{
                    height: {pyflame.gui_resize(8)}px;  /* Adjust the height of the horizontal scrollbar */
                    }}
                """)
        else:
            self.setStyleSheet(f"""
                QTextEdit{{
                    color: {Color.TEXT.value};
                    background-color: rgb(55, 65, 75);
                    selection-color: rgb(38, 38, 38);
                    selection-background-color: rgb(184, 177, 167);
                    border: none;
                    padding-left: 1px;
                    }}
                QTextEdit:hover{{
                    border: 1px solid {Color.BORDER.value};
                    padding-left: 1px;
                    }}
                QTextEdit:focus{{
                    background-color: rgb(73, 86, 99);
                    }}
                QScrollBar::handle{{
                    background: {Color.SCROLLBAR_HANDLE.value};
                    }}
                QScrollBar:vertical{{
                    width: {pyflame.gui_resize(8)}px;  /* Adjust the width of the vertical scrollbar */
                    }}
                QScrollBar:horizontal{{
                    height: {pyflame.gui_resize(8)}px;  /* Adjust the height of the horizontal scrollbar */
                    }}
                """)

    def text(self) -> str:
        """
        Text
        ====

        Get text from PyFlameTextEdit.

        Returns:
        --------
            str: PyFlameTextEdit text.

        Example:
        --------
            To get text from PyFlameTextEdit:
            ```
            text = text_edit.text()
            ```
        """

        return self.toPlainText()

    def setText(self, text: str) -> None:
        """
        Set Text
        ========

        Sets the text in the text edit.

        Args:
        -----
            `text (str)`:
                Text to be added to TextEdit.

        Raises:
        -------
            TypeError:
                If `text` argument is not of type str.

        Example:
        --------
            To set text in PyFlameTextEdit:
            ```
            text_edit.setText('Some text here')
            ```
        """

        # Validate argument type
        if not isinstance(text, str):
            raise TypeError(f'PyFlameTextEdit: Invalid text argument: {text}. Must be of type str.')

        self.setPlainText(text)

class PyFlameTokenPushButton(QtWidgets.QPushButton):
    """
    PyFlameTokenPushButton
    ======================

    Custom QT Flame Token Push Button Widget Subclass

    When a token is chosen from the menu, it is inserted into the PyFlameEntry widget specified by token_dest.

    Args:
    -----
        `text` (str, optional):
            PyFlameTokenPushButton text.
            (Default: `Add Token`)

        `token_dict` (dict, optional):
            Dictionary defining tokens. {'Token Name': '<Token>'}.
            (Default: `{}`)

        `token_dest` (PyFlameEntry, optional):
            PyFlameEntry that token value will be applied to.
            (Default: `None`)

        `clear_dest` (bool, optional):
            Clear destination QLineEdit before inserting token.
            (Default: `False`)

        `width` (int, optional):
            Button width.
            (Default: `50`)

        `height` (int, optional):
            Button height.
            (Default: `28`)

        `max_width` (bool, optional):
            Set to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `font` (str, optional):
            Font family to be used for the text on the button.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text on the button.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `add_menu_options(new_options)`:
            Clears existing menu and adds new menu options PyFlameTokenPushButton menu.

    Examples:
    ---------
        To create a PyFlameTokenPushButton:
        ```
        token_push_button = PyFlameTokenPushButton(
            token_dict={
                'Token 1': '<Token1>',
                'Token2': '<Token2>',
                },
            token_dest=PyFlameEntry,
            clear_dest=True,
            )
        ```

        To enable/disable PyFlameTokenPushButton:
        ```
        token_push_button.setEnabled(True)
        token_push_button.setEnabled(False)
        ```

        To add new menu options to the existing token menu:
        ```
        token_push_button.add_menu_options(
            new_options={
                'New Token Name': '<New Token>',
                }
            )
        ```
    """

    def __init__(self: 'PyFlameTokenPushButton',
                 text: str='Add Token',
                 token_dict: Dict[str, str]={},
                 token_dest: Optional[PyFlameEntry]=None,
                 clear_dest: bool=False,
                 width: int=50,
                 height: int=28,
                 max_width: Optional[bool]=True,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate arguments types
        if not isinstance(text, str):
            raise TypeError(f'PyFlameTokenPushButton: Invalid text argument: {text}. Must be of type str.')
        elif not isinstance(token_dict, dict):
            raise TypeError(f'PyFlameTokenPushButton: Invalid token_dict argument: {token_dict}. Must be of type dict.')
        elif not isinstance(token_dest, QtWidgets.QLineEdit):
            raise TypeError(f'PyFlameTokenPushButton: Invalid token_dest argument: {token_dest}. Must be of type QtWidgets.QLineEdit.')
        elif not isinstance(clear_dest, bool):
            raise TypeError(f'PyFlameTokenPushButton: Invalid clear_dest argument: {clear_dest}. Must be of type bool.')
        elif not isinstance(width, int):
            raise TypeError(f'PyFlameTokenPushButton: Invalid width argument: {width}. Must be of type int.')
        elif not isinstance(height, int):
            raise TypeError(f'PyFlameTokenPushButton: Invalid height argument: {height}. Must be of type int.')
        elif not isinstance(max_width, bool):
            raise TypeError(f'PyFlameTokenPushButton: Invalid max_width argument: {max_width}. Must be of type bool.')
        elif not isinstance(font, str):
            raise TypeError(f'PyFlameTokenPushButton: Invalid font argument: {font}. Must be of type str.')
        elif not isinstance(font_size, int):
            raise TypeError(f'PyFlameTokenPushButton: Invalid font_size argument: {font_size}. Must be of type int.')

        # Set button font
        self.font_size = pyflame.font_resize(font_size)
        font = QtGui.QFont(font)
        font.setPointSize(self.font_size)
        self.setFont(font)

        # Build token push button
        self.setText(text)
        self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create the token menu
        self.token_menu = QtWidgets.QMenu(self)
        self.token_menu.setFocusPolicy(QtCore.Qt.NoFocus)

        def token_action_menu():

            def insert_token(token):
                if clear_dest:
                    token_dest.setText('')
                for key, value in token_dict.items():
                    if key == token:
                        token_name = value
                        token_dest.insert(token_name)

            for key, value in token_dict.items():
                self.token_menu.addAction(key, partial(insert_token, key))

        token_action_menu()
        self.setMenu(self.token_menu)

        self._set_stylesheet()
        self._set_menu_style_sheet()

        self.token_dict = token_dict
        self.token_dest = token_dest
        self.clear_dest = clear_dest

    def _set_stylesheet(self):
        """
        Set Stylesheet
        ==============

        This private method sets the PyFlameTokenPushButton stylesheet.
        """

        self.setStyleSheet(f"""
            QPushButton{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                border: none;
                font: {self.font_size}px "Discreet";
                }}
            QPushButton:hover{{
                border: 1px solid {Color.BORDER.value};
                }}
            QPushButton:disabled{{
                color: {Color.TEXT_DISABLED.value};
                background-color: rgb(45, 55, 68);
                border: none;
                }}
            QPushButton::menu-indicator{{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: {pyflame.gui_resize(15)}px;
                height: {pyflame.gui_resize(15)}px;
                right: {pyflame.gui_resize(10)}px;
                }}
            QToolTip{{
                color: {Color.WHITE.value}; /* Tooltip text color */
                background-color: {Color.SELECTED_GRAY.value};
                border: 1px solid {Color.BLACK.value}; /* Tooltip border color */
                }}
            """)

    def _set_menu_style_sheet(self):
        """
        Set Menu Stylesheet
        ===================

        This private method sets the PyFlameTokenPushButton menu stylesheet.
        """

        self.menu().setStyleSheet(f"""
            QMenu{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 55, 68);
                border: none;
                font: {self.font_size}px "Discreet";
                }}
            QMenu::item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: rgb(58, 69, 81);
                }}
            """)

    def add_menu_options(self, new_options: Dict[str, str]):
            """
            Add Menu Options
            ================

            Clears existing PyFlameTokenPushButton menu and creats new menu from `add_menu_options`.

            Args:
            -----
                `new_options` (dict):
                    Dictionary of new token options to add. The key is the name of the token to display in the menu, and the
                    value is the token to insert into the destination PyFlameLineEdit.

            Raises:
            -------
                TypeError:
                    If `new_options` is not a dictionary
                    If the dictionary does not contain strings as keys and values.

            Example:
            --------
                Add new options to PyFlameTokenPushButton menu:
                ```
                token_push_button.add_menu_options(
                    new_options={
                        'New Token Name': '<New Token>'
                        },
                    )
                ```
            """

            # Validate the argument type
            if not isinstance(new_options, dict):
                raise TypeError('add_menu_options: new_options must be a dictionary.')

            # Validate the contents of the dictionary
            for key, value in new_options.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise TypeError('add_menu_options: All keys and values in new_options must be strings.')

            def insert_new_token(token):
                """
                Insert New Token
                ================

                Insert the new token into the destination PyFlameEntry.

                Args:
                -----
                   `token` (str):
                        The token to insert into the destination PyFlameEntry.
                """

                if self.clear_dest:
                    self.token_dest.setText('')
                for key, value in self.token_dict.items():
                    if key == token:
                        token_name = value
                        self.token_dest.insert(token_name)

            # Clear existing token menu and dictionary
            self.token_menu.clear()
            self.token_dict.clear()

            # Add new menu options
            for key, value in new_options.items():
                self.token_dict[key] = value
                self.token_menu.addAction(key, partial(insert_new_token, key))

class PyFlameTreeWidget(QtWidgets.QTreeWidget):
    """
    PyFlameTreeWidget
    =================

    Custom QT Flame Tree Widget Subclass

    Args:
    -----
        `column_names` (list[str]):
            List of names to be used for column names in tree.

        `connect` (callable, optional):
            Function to call when item in tree is clicked on.
            (Default: `None`)

        `width` (int, optional):
            Width of tree widget.
            (Default: `50`)

        `height` (int, optional):
            Height of tree widget.
            (Default: `50`)

        `max_width` (bool, optional):
            Set to maximum width. Use if width is being set by layout. Overrides `width` if set to True.
            (Default: `True`)

        `max_height` (bool, optional):
            Set to maximum height. Use if height is being set by layout. No need to set height if this is used.
            (Default: `True`)

        `tree_dict` (Dict[str, Dict[str, str]], optional):
            Dictionary of items to populate the tree widget. Useful when dealing with folder trees.
            (Default: `{}`)

        `tree_list` (List[str], optional):
            List of items to populate the tree widget. Useful when dealing with batch group schematic reels shelf reels and desktop reels.
            (Default: `[]`)

        `allow_children` (bool, optional):
            Whether to allow children in the tree.
            (Default: `True`)

        `sorting` (bool, optional):
            Whether to enable sorting in the tree widget.
            (Default: `False`)

        `min_items` (int, optional):
            Minimum number of items that must remain in the tree.
            (Default: `1`)

        `update_callback` (callable, optional):
            Function to call when an item is edited, inserted, or deleted.
            (Default: `None`)

        `font` (str, optional):
            Font family to be used for the text in the tree.
            (Default: `PYFLAME_FONT`)

        `font_size` (int, optional):
            Size of the font to be used for the text in the tree.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `fill_tree_dict(tree_dict: Dict[str, Dict[str, str]], editable: bool=False)`:
            Fill the PyFlameTreeWidget with the provided dictionary.

        `fill_tree_list(tree_list: List[str])`:
            Fill the PyFlameTreeWidget with the provided list.

        `add_item(item_name: str)`:
            Add a new item as a child of the currently selected item in the tree, or as a child of the top-level item if no item is selected.

        `delete_item()`:
            Delete the selected item in the PyFlameTreeWidget.
            Does not delete if the item is the top-level item or if the total number of items under the top-level item would drop below
            the minimum required that is set by the min_items argument.

        `sort_items()`:
            Sort all items in the tree while maintaining the structure and keeping the tree expanded.

    Attributes:
    -----------
        `all_item_paths`:
            Returns:
                List[str]:
                    The recursive paths of all items in the PyFlameTreeWidget.

        `all_item_paths_no_root`:
            Returns:
                List[str]:
                    The recursive paths of all items in the PyFlameTreeWidget excluding the root item.

        `item_path`:
            Returns:
                str:
                    The recursive path of the currently selected item.

        `item_paths`:
            Returns:
                List[str]:
                    The recursive paths of all selected items.

        `selected_item`:
            Returns:
                str:
                    The text of the currently selected item.
        `tree_dict`: A nested dictionary representing the tree structure. Useful when dealing with folder trees.
            Returns:
                Dict[str, Dict]:
                    A nested dictionary representing the tree structure.

        `tree_list`: A list of all item names in the tree. Useful when dealing with batch group schematic reels shelf reels and desktop reels.
            Returns:
                List[str]:
                    A list of all item names.

        `tree_list_no_root`: A list of all item names in the tree excluding the root item. Useful when dealing with batch group schematic reels shelf reels and desktop reels.
            Returns:
                List[str]:
                    A list of all item names excluding the root item.

    Inherited Methods:
    ------------------
        `setEnabled(bool)`:
            Enable or disable the PyFlameTreeWidget. True to enable, False to disable.

        `setSortingEnabled(bool)`:
            Enable or disable sorting in the PyFlameTreeWidget. True to enable sorting, False to disable.

        `clear()`:
            Clear all items from the PyFlameTreeWidget.

    Examples:
    ---------
        To create a PyFlameTreeWidget with a dictionary:
        ```
        tree_widget = PyFlameTreeWidget(
            column_names=[
                'Column 1',
                'Column 2',
                'Column 3',
                'Column 4',
                ],
            tree_dict={
                'Shot Folder': {
                    'Elements': {},
                    'Plates': {},
                    'Ref': {},
                    'Renders': {},
                    }
                },
            sorting=True,
            allow_children=False
            )
        ```

        To create a PyFlameTreeWidget with a list:
        ```
        tree_widget = PyFlameTreeWidget(
            column_names=[
                'Schematic Reel Template',
                ],
            tree_list=[
                'Schematic Reel 1',
                'Schematic Reel 2',
                'Schematic Reel 3',
                'Schematic Reel 4',
                ],
            top_level_item='Schematic Reels',
            sorting=True,
            allow_children=False
            )
        ```

        Add a new item to the tree:
        ```
        tree_widget.add_item(item_name='New Item')
        ```

        Delete the selected item in the tree:
        ```
        tree_widget.delete_item()
        ```

        Sort all items in the tree:
        ```
        tree_widget.sort_items()
        ```

        Get the text of the currently selected item:
        ```
        tree_widget.selected_item
        ```

        Get the recursive path of the currently selected item:
        ```
        tree_widget.item_path
        ```

        Get the recursive paths of all selected items:
        ```
        tree_widget.item_paths
        ```

        Get the recursive paths of all items in the PyFlameTreeWidget:
        ```
        tree_widget.all_item_paths
        ```
    """

    def __init__(self: 'PyFlameTreeWidget',
                 column_names: List[str],
                 connect: Optional[Callable[..., None]] = None,
                 width: int = 50,
                 height: int = 50,
                 max_width: Optional[bool] = True,
                 max_height: Optional[bool] = True,
                 tree_dict: Dict[str, Dict[str, str]] = {},
                 tree_list: List[str] = [],
                 top_level_item: Optional[str] = None,
                 top_level_editable: bool = False,
                 allow_children: bool = True,
                 sorting: bool = False,
                 min_items: int = 1,
                 update_callback: Optional[Callable[..., None]] = None,
                 font_family: str = PYFLAME_FONT,
                 font_size: int = PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(column_names, list):
            raise TypeError(f"PyFlameTreeWidget: Expected 'column_names' to be a list, got {type(column_names).__name__} instead.")
        if connect is not None and not callable(connect):
            raise TypeError(f"PyFlameTreeWidget: Expected 'connect' to be a callable function or method, or None, got {type(connect).__name__} instead.")
        if not isinstance(width, int):
            raise TypeError(f"PyFlameTreeWidget: Expected 'width' to be an integer, got {type(width).__name__} instead.")
        if not isinstance(height, int):
            raise TypeError(f"PyFlameTreeWidget: Expected 'height' to be an integer, got {type(height).__name__} instead.")
        if not isinstance(max_width, bool):
            raise TypeError(f"PyFlameTreeWidget: Expected 'max_width' to be a boolean, got {type(max_width).__name__} instead.")
        if not isinstance(max_height, bool):
            raise TypeError(f"PyFlameTreeWidget: Expected 'max_height' to be a boolean, got {type(max_height).__name__} instead.")
        if not isinstance(tree_dict, dict):
            raise TypeError(f"PyFlameTreeWidget: Expected 'tree_dict' to be a dictionary, got {type(tree_dict).__name__} instead.")
        if not isinstance(tree_list, list):
            raise TypeError(f"PyFlameTreeWidget: Expected 'tree_list' to be a list, got {type(tree_list).__name__} instead.")
        if top_level_item is not None and not isinstance(top_level_item, str):
            raise TypeError(f"PyFlameTreeWidget: Expected 'top_level_item' to be a string, got {type(top_level_item).__name__} instead.")
        if tree_list and not top_level_item:
            raise ValueError("PyFlameTreeWidget: 'top_level_item' must be provided when 'tree_list' is used.")
        if not isinstance(top_level_editable, bool):
            raise TypeError(f"PyFlameTreeWidget: Expected 'top_level_editable' to be a boolean, got {type(top_level_editable).__name__} instead.")
        if not isinstance(allow_children, bool):
            raise TypeError(f"PyFlameTreeWidget: Expected 'allow_children' to be a boolean, got {type(allow_children).__name__} instead.")
        if not isinstance(sorting, bool):
            raise TypeError(f"PyFlameTreeWidget: Expected 'sorting' to be a boolean, got {type(sorting).__name__} instead.")
        if not isinstance(min_items, int) or min_items < 1:
            raise TypeError(f"PyFlameTreeWidget: Expected 'min_items' to be an integer greater than or equal to 1, got {type(min_items).__name__} instead.")
        if update_callback is not None and not callable(update_callback):
            raise TypeError(f"PyFlameTreeWidget: Expected 'update_callback' to be a callable function or method, or None, got {type(update_callback).__name__} instead.")
        if not isinstance(font_family, str):
            raise TypeError(f"PyFlameTreeWidget: Expected 'font_family' to be a string, got {type(font_family).__name__} instead.")
        if not isinstance(font_size, int):
            raise TypeError(f"PyFlameTreeWidget: Expected 'font_size' to be an integer, got {type(font_size).__name__} instead.")

        # Set attributes
        self.allow_children = allow_children
        self.min_items = min_items
        self.top_level_editable = top_level_editable
        self.update_callback = update_callback

        font_size = pyflame.font_resize(font_size)

        # Set font
        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(font_size)
        self.setFont(font)

        # Set header font
        header_font = QtGui.QFont()
        header_font.setFamily(font_family)
        header_font.setPointSize(font_size)
        self.header().setFont(header_font)

        # Build tree widget
        #self.setFixedSize(pyflame.gui_resize(width), pyflame.gui_resize(height))
        if max_width:
            self.setMaximumWidth(pyflame.gui_resize(3000))
        if max_height:
            self.setMaximumHeight(pyflame.gui_resize(3000))
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(connect)
        self.setHeaderLabels(column_names)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.itemCollapsed.connect(self._on_item_collapsed)  # Prevent top-level item from collapsing

        self._set_stylesheet()

        # Set sorting based on the argument
        self.setSortingEnabled(sorting)
        if sorting:
            self.sortItems(0, QtCore.Qt.AscendingOrder)

        # Fill tree with dictionary if provided, otherwise use list
        if tree_dict:
            self.fill_tree_dict(tree_dict)
        elif tree_list:
            # Convert list to dict using top_level_item as the key. Each item in the list should be a string value of the key not a list.
            tree_dict = {top_level_item: {str(item): {} for item in tree_list}}


            self.fill_tree_dict(tree_dict)

        # Set the first top-level item as the current item
        self.setCurrentItem(self.topLevelItem(0))

        # Set the top-level item as uneditable if top_level_editable is False
        if not top_level_editable:
            self._set_top_level_uneditable()

        # Trigger the callback function if it is set when an item is changed
        self.itemChanged.connect(self._trigger_callback)

    # ============ Private Methods ============ #

    def _trigger_callback(self) -> None:
        """
        Trigger Callback
        ================

        Trigger the callback function if it is set.

        Note:
        -----
            This method is intended for internal use only and should not be called directly.
        """

        if self.update_callback:
            self.update_callback()

    def _set_top_level_uneditable(self) -> None:
        """
        Set Top Level Uneditable
        ========================

        Set the top-level item in the PyFlameTreeWidget as uneditable and all child items as editable.

        Note:
        -----
            This method is intended for internal use only and should not be called directly.
        """

        # Access the top item using the tree object
        top_item = self.topLevelItem(0)  # Index 0 gets the first top-level item

        # Check if the top item exists. If it does, set the flags to make it uneditable and all child items editable
        if top_item:
            # Make the top_item non-editable
            top_item.setFlags(top_item.flags() & ~QtCore.Qt.ItemIsEditable)
            # Ensure all child items remain editable
            for i in range(top_item.childCount()):
                child_item = top_item.child(i)
                child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsEditable)

    def _on_item_collapsed(self, item):
        """
        On Item Collapsed
        =================

        Prevent the top-level item from collapsing.

        Note:
        -----
            This method is intended for internal use only and should not be called directly.

        Args:
        -----
            `item` (PyFlameTreeWidget.QTreeWidgetItem):
                The item that was collapsed.
        """

        # Check if the item is a top-level item
        if self.indexOfTopLevelItem(item) != -1:
            self.expandItem(item)  # Re-expand the top-level item

    # ============ Methods ============ #

    def fill_tree_dict(self, tree_dict: Dict[str, str], editable: bool=False) -> None:
        """
        Fill Tree Dict
        ==============

        Fill the PyFlameTreeWidget with items from the provided dictionary.

        Args:
        -----
            `tree_dict` (Dict[str, str]):
                Dictionary to populate the PyFlameTreeWidget.
                The keys and values should be strings representing item names and
                nested dictionaries in string format respectively.

            `editable` (bool, optional):
                Whether the items in the tree should be editable.
                (Default: False)

        Raises:
        -------
            TypeError:
                If `tree_dict` is not a dictionary.
                If `editable` is not a boolean.

            ValueError:
                If any key or value in `tree_dict` is not a string.
                If any value cannot be evaluated as a dictionary.

        Example:
        --------
            Populate the PyFlameTreeWidget with items from a dictionary:
            ```
            tree_data =
            tree_widget.fill_tree(
                tree_dict={
                    'Shot_Folder': {
                        'Elements': {},
                        'Plates': {},
                        'Ref': {},
                        'Renders': {}
                        }
                    },
                editable=True,
                )
            ```
        """

        # Validate arguments
        if not isinstance(tree_dict, dict):
            raise TypeError('fill_tree: tree_dict must be a dictionary.')
        if not isinstance(editable, bool):
            raise TypeError('fill_tree: editable must be a boolean.')
        for key, value in tree_dict.items():
            if not isinstance(key, (str, dict)):
                raise ValueError(f'fill_tree: All keys in tree_dict must be strings. Invalid key: {key}')
            if not isinstance(value, (str, dict)):
                raise ValueError(f'fill_tree: All values in tree_dict must be strings. Invalid value for key "{key}": {value}')

        # ============ Fill Tree ============ #

        # Disable sorting before filling the tree
        self.setSortingEnabled(False)

        # Set the default and editable flags for the items
        default_flags = (
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsUserCheckable |
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsEditable
            )
        editable_flags = default_flags | QtCore.Qt.ItemIsEditable

        def fill_item(parent: QtWidgets.QTreeWidgetItem, value: Dict) -> None:
            """
            Fill Item
            =========

            Recursively fill the PyFlameTreeWidget with items from the dictionary.
            """

            for key, val in value.items():
                child = QtWidgets.QTreeWidgetItem([key])
                parent.addChild(child)
                if isinstance(val, dict):
                    fill_item(child, val)

                # Set item flags
                if editable:
                    child.setFlags(editable_flags)
                else:
                    child.setFlags(default_flags)

                # Set the item as expanded initially if it has children
                if isinstance(val, dict) and val:
                    child.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                    child.setExpanded(True)

        self.clear()
        fill_item(self.invisibleRootItem(), tree_dict)

        # Restore sorting state based on the initial setting
        self.setSortingEnabled(self.isSortingEnabled())

    def fill_tree_list(self, tree_list: List[str]) -> None:
        """
        Fill Tree List
        ==============
        """

        self.clear()
        for item in tree_list:
            self.addTopLevelItem(QtWidgets.QTreeWidgetItem([item]))

    def add_item(self, item_name: str) -> None:
        """
        Add Item
        ========

        Add a new item as a child of the currently selected item in the PyFlameTreeWidget,
        or as a child of the top-level item if no item is selected.

        The new item will have the following flags:
        - Selectable
        - User checkable
        - Enabled
        - Editable

        Args:
            `item_name` (str):
                The name of new item to add.

        Raises:
            TypeError:
                If `item_name` is not a string.

        Example:
        --------
            Add a new item to the PyFlameTreeWidget:
            ```
            tree_widget.add_item(item_name='New Item')
            ```
        """

        # Validate the argument type
        if not isinstance(item_name, str):
            raise TypeError(f'add_item: item_name must be a string. Invalid item_name: {item_name}')

        # Disable sorting before adding the item
        self.setSortingEnabled(False)

        # Iterate the item name if it already exists in the tree
        existing_item_names = self.tree_list
        item_name = pyflame.iterate_name(existing_item_names, item_name)

        # Get the currently selected items
        selected_items = self.selectedItems()

        if not selected_items:
            # No item is selected, add the new item under the top-level item
            parent = self.topLevelItem(0)  # Always add under the first top-level item
            index = parent.childCount()
        else:
            selected_item = selected_items[0]
            if self.allow_children:
                parent = selected_item
                index = parent.childCount()
            else:
                parent = selected_item.parent()
                if not parent:
                    # Selected item is a top-level item, add under it
                    parent = selected_item
                    index = parent.childCount()
                else:
                    # Selected item is not a top-level item
                    index = parent.indexOfChild(selected_item) + 1

        # Create a new tree widget item with the specified name
        new_item = QtWidgets.QTreeWidgetItem([item_name])

        # Set the desired flags for the new item
        new_item.setFlags(
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsUserCheckable |
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsEditable
        )

        # Insert the new item at the determined position under the parent
        parent.insertChild(index, new_item)

        # Ensure the parent item is expanded to show the new child
        if parent != self.invisibleRootItem():
            parent.setExpanded(True)

        # Set the newly added item as the currently selected item
        self.setCurrentItem(new_item)

        # Restore sorting state based on the initial setting
        self.setSortingEnabled(self.isSortingEnabled())

        # Trigger the callback function if it is set
        self._trigger_callback()

        pyflame.print(f'Added item: {item_name}', text_color=TextColor.GREEN)

    def delete_item(self) -> None:
        """
        Delete Item
        ===========

        Deletes the selected item in the PyFlameTreeWidget.
        Will not delete if the item is the top-level item or if the total number of items under the top-level item would drop below the minimum required.

        Example:
        --------
            Delete the selected item in the PyFlameTreeWidget:
            ```
            tree_widget.delete_item()
            ```
        """

        # Get the currently selected items
        selected_items = self.selectedItems()

        if not selected_items:
            return  # No item is selected, do nothing

        selected_item = selected_items[0]

        # Get the parent of the selected item
        parent = selected_item.parent()

        # Check if the selected item is a top-level item
        if parent is None:
            pyflame.print('Cannot delete root folder from tree.', text_color=TextColor.RED)
            return  # Do not delete the top-level item

        # Count the total number of items under the top-level item
        def count_items(item: QtWidgets.QTreeWidgetItem) -> int:
            count = item.childCount()
            for i in range(item.childCount()):
                count += count_items(item.child(i))
            return count

        top_level_item = self.topLevelItem(0)
        total_items_under_top = count_items(top_level_item)

        # Check if the total number of items under the top-level item is less than or equal to the minimum items
        if total_items_under_top <= self.min_items:
            return  # Do not delete items if it would drop below the minimum number of items

        # If the item can be deleted, proceed with the deletion
        index = parent.indexOfChild(selected_item)
        parent.takeChild(index)

        # Restore sorting state based on the initial setting
        self.setSortingEnabled(self.isSortingEnabled())

        # Trigger the callback function if it is set
        self._trigger_callback()

        pyflame.print(f'Deleted item: {selected_item.text(0)}', text_color=TextColor.RED)

    def sort_items(self) -> None:
        """
        Sort Items
        ==========

        Sorts all items in the PyFlameTreeWidget while maintaining the structure and keeping the tree expanded.
        """

        def save_expansion_state(item: QtWidgets.QTreeWidgetItem, state: Dict[str, bool]) -> None:
            """
            Recursively save the expansion state of the items.
            """

            state[item.text(0)] = item.isExpanded()
            for i in range(item.childCount()):
                save_expansion_state(item.child(i), state)

        def restore_expansion_state(item: QtWidgets.QTreeWidgetItem, state: Dict[str, bool]) -> None:
            """
            Recursively restore the expansion state of the items.
            """

            item.setExpanded(state.get(item.text(0), False))
            for i in range(item.childCount()):
                restore_expansion_state(item.child(i), state)

        def sort_items_recursively(item: QtWidgets.QTreeWidgetItem) -> None:
            """
            Recursively sort the children of the item.
            """

            children = [item.child(i) for i in range(item.childCount())]
            children.sort(key=lambda x: x.text(0))

            for i, child in enumerate(children):
                item.takeChild(item.indexOfChild(child))
                item.insertChild(i, child)
                sort_items_recursively(child)

        # Save the expansion state
        expansion_state = {}
        top_level_items = [self.topLevelItem(i) for i in range(self.topLevelItemCount())]
        for top_level_item in top_level_items:
            save_expansion_state(top_level_item, expansion_state)

        # Disable sorting before manually sorting the items
        self.setSortingEnabled(False)

        # Sort the top-level items
        top_level_items.sort(key=lambda x: x.text(0))
        for i, top_level_item in enumerate(top_level_items):
            self.takeTopLevelItem(self.indexOfTopLevelItem(top_level_item))
            self.insertTopLevelItem(i, top_level_item)
            sort_items_recursively(top_level_item)

        # Restore the expansion state
        for top_level_item in top_level_items:
            restore_expansion_state(top_level_item, expansion_state)

        # Restore sorting state based on the initial setting
        self.setSortingEnabled(self.isSortingEnabled())

        # Trigger the callback function if it is set
        self._trigger_callback()

        pyflame.print('Tree items sorted.', text_color=TextColor.GREEN)

    # ============ Attributes ============ #

    @property
    def all_item_paths(self) -> list:
        """
        All Item Paths
        ==============

        Generate a list of paths to all items in the tree.

        Returns:
        --------
            list:
                A list of strings, where each string is the recursive path to an item in the tree.
        """

        def get_paths(item, current_path):
            # Recursive helper function to build paths for each item and its children
            path = current_path + [item.text(0)]
            paths.append("/".join(path))
            for i in range(item.childCount()):
                get_paths(item.child(i), path)

        paths = []
        root_count = self.topLevelItemCount()
        for i in range(root_count):
            root_item = self.topLevelItem(i)
            get_paths(root_item, [])

        return paths

    @property
    def all_item_paths_no_root(self) -> list:
        """
        All Item Paths No Root
        ======================

        Generate a list of paths to all items in the tree excluding the root.

        Returns:
        --------
            list:
                A list of strings, where each string is the recursive path to an item in the tree excluding the root.
        """

        # Remove root item from paths
        clean_paths = []
        for path in self.all_item_paths:
            # Split the path by '/', exclude the root element, and rejoin the rest
            path_parts = path.split('/')
            if len(path_parts) > 1:  # Make sure there's more than just the root
                clean_paths.append("/".join(path_parts[1:]))

        return clean_paths

    @property
    def item_path(self) -> str:
        """
        Item Path
        =========

        Return the recursive path of the currently selected item.

        Returns:
        --------
            str:
                The recursive path of the currently selected item.

        Example:
        --------
            Get the recursive path of the currently selected item:
            ```
            tree_widget.item_path
            ```

        """

        item = self.currentItem()

        path = []
        while item is not None:
            path.insert(0, item.text(0))  # Insert at the beginning to build from root to leaf
            item = item.parent()  # Move up to the parent item

        return "/".join(path)  # Combine path elements with "/"

    @property
    def item_paths(self) -> List[str]:
        """
        Item Paths
        ==========

        Return the recursive paths of the currently selected items.

        Returns:
        --------
            List[str]:
                The recursive paths of the currently selected items.

        Example:
        --------
            Get the recursive paths of the currently selected items:
            ```
            tree_widget.item_paths
            ```
        """

        def get_item_path():

            item = self.currentItem()

            path = []
            while item is not None:
                path.insert(0, item.text(0))  # Insert at the beginning to build from root to leaf
                item = item.parent()  # Move up to the parent item

            return "/".join(path)  # Combine path elements with "/"

        return [get_item_path(item) for item in self.selectedItems()]

    @property
    def selected_item(self) -> str:
        """
        Selected Item
        =============

        Return the text of the currently selected item.

        Returns:
        --------
            str:
                The text of the currently selected item.

        Example:
        --------
            Get the text of the currently selected item:
            ```
            tree_widget.selected_item
            ```
        """

        return self.currentItem().text(0)

    @property
    def tree_dict(self) -> Dict[str, Dict]:
        """
        Tree Dict
        =========

        Get the items in the tPyFlameTreeWidget as a nested dictionary.

        This traverses the PyFlameTreeWidget, captures the hierarchical paths of each item,
        and converts these paths into a nested dictionary structure. Each item's path is
        represented as keys in the dictionary.

        Returns:
        --------
            Dict[str, Dict]:
                A nested dictionary representing the hierarchical structure of the PyFlameTreeWidget.

        Example:
        --------
            Get a nested dictionary representing the hierarchical structure of the PyFlameTreeWidget:
            ```
            tree_widget.tree_dict
            ```
        """

        def get_tree_path(item):
            """
            Get Tree Path
            =============

            Get the path of a tree item as a string.

            Args:
            -----
                `item` (QTreeWidgetItem):
                    The tree item to get the path for.

            Returns:
            --------
                str: The path of the item.
            """

            path = []
            while item:
                path.append(str(item.text(0)))
                item = item.parent()
            return '/'.join(reversed(path))

        def get_items_recursively():
            """
            Get Items Recursively
            ======================

            Recursively traverse the PyFlameTreeWidget and collect paths of all items.

            Args:
            -----
                `item` (QTreeWidgetItem, optional):
                    The tree item to start traversal from. Defaults to None.

            Returns:
            --------
                list: A list of paths of all tree items.
            """

            path_list = []

            def search_child_item(item):
                for m in range(item.childCount()):
                    child_item = item.child(m)
                    path_list.append(get_tree_path(child_item))
                    search_child_item(child_item)

            for i in range(self.topLevelItemCount()):
                top_item = self.topLevelItem(i)
                path_list.append(get_tree_path(top_item))
                search_child_item(top_item)

            return path_list

        # Get all paths from tree
        path_list = get_items_recursively()

        # Convert path list to dictionary
        tree_dict = {}
        for path in path_list:
            p = tree_dict
            for x in path.split('/'):
                p = p.setdefault(x, {})

        return tree_dict

    @property
    def tree_list(self) -> List[str]:
        """
        Tree List
        =========

        Property to get a list of all item names in the PyFlameTreeWidget.

        This property traverses the tree widget and collects the names of all items in a list.

        Returns:
        --------
            List[str]:
                A list of all item names.

        Example:
        --------
            Get a list of all item names:
            ```
            tree_widget.tree_list
            ```
        """

        item_names = []

        def traverse_item(item: QtWidgets.QTreeWidgetItem) -> None:
            item_names.append(item.text(0))
            for i in range(item.childCount()):
                traverse_item(item.child(i))

        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            traverse_item(root.child(i))

        return item_names

    @property
    def tree_list_no_root(self) -> List[str]:
        """
        Tree List No Root
        =================

        Return the tree list excluding the root item.
        """

        return self.tree_list[1:]

    # ============ Stylesheet - Private Method ============ #

    def _set_stylesheet(self):
        """
        Set Stylesheet
        ==============

        This private method sets the PyFlameTreeWidget stylesheet.
        """

        self.setStyleSheet(f"""
            QTreeWidget{{
                color: {Color.TEXT.value};
                background-color: rgb(30, 30, 30);
                alternate-background-color: rgb(36, 36, 36);
                border: 1px solid rgba(0, 0, 0, .1);
                }}
            QTreeWidget::item{{
                padding-top: {pyflame.gui_resize(5)}px;  /* Increase top padding */
                padding-bottom: {pyflame.gui_resize(5)}px;  /* Increase bottom padding */
            }}
            QHeaderView::section{{
                color: {Color.TEXT.value};
                background-color: rgb(57, 57, 57);
                border: none;
                padding-left: {pyflame.gui_resize(10)}px;
                height: {pyflame.gui_resize(18)}px;
                }}
            QTreeWidget:item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: {Color.SELECTED_GRAY.value};
                selection-background-color: rgb(153, 153, 153);
                }}
            QTreeWidget:item:selected:active{{
                color: rgb(153, 153, 153);
                border: none;
                }}
            QTreeWidget:disabled{{
                color: rgb(101, 101, 101);
                background-color: rgb(34, 34, 34);
                }}
            QMenu{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 48, 61);
                }}
            QMenu::item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: rgb(58, 69, 81);
                }}
            QScrollBar::handle{{
                background: {Color.SCROLLBAR_HANDLE.value};
                }}
            QScrollBar:vertical{{
                width: {pyflame.gui_resize(8)}px;  /* Adjust the width of the vertical scrollbar */
                }}
            QScrollBar:horizontal{{
                height: {pyflame.gui_resize(8)}px;  /* Adjust the height of the horizontal scrollbar */
                }}
            QTreeWidget::branch:has-siblings:!adjoins-item{{
                border-image: none;
                background: transparent;
                }}
            QTreeWidget::branch:has-siblings:adjoins-item{{
                border-image: none;
                background: transparent;
                }}
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item{{
                border-image: none;
                background: transparent;
                }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings{{
                border-image: none;
                background: transparent;
                }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings{{
                border-image: none;
                background: transparent;
                }}
            QTreeWidget:item:selected{{
                color: {Color.TEXT_SELECTED.value};
                background-color: {Color.SELECTED_GRAY.value};
                }}
            QHeaderView::section:disabled{{
                color: {Color.TEXT_DISABLED.value};
                }}
            QTreeWidget::item:disabled:selected {{
                color: {Color.TEXT_DISABLED.value};
                background-color: {Color.SELECTED_GRAY.value};
                }}
            """)

#-------------------------------------
# [PyFlame Layout Classes]
#-------------------------------------

class PyFlameGridLayout(QtWidgets.QGridLayout):
    """
    PyFlameGridLayout
    =================

    Custom QT QGridLayout Subclass.

    Configure the grid size of the layout by setting the number of columns, rows,
    and their respective sizes. Optionally adjust the width of specific columns
    and the height of specific rows.

    Args:
    -----
        `columns` (int):
            Number of columns in the grid.
            Columns start counting at 0.
            (Default: `0`)

        `rows` (int):
            Number of rows in the grid.
            Rows start counting at 0.
            (Default: `0`)

        `column_width` (int):
            Default width of each column in pixels.
            (Default: `150`)

        `row_height` (int):
            Default height of each row in pixels.
            (Default: `28`)

        `adjust_column_widths` (dict[int, int], optional):
            A dictionary to adjust the width of specific columns.
            Keys are column indices (0-based), and values are widths in pixels.
            (Default: `{}`)

        `adjust_row_heights` (dict[int, int], optional):
            A dictionary to adjust the height of specific rows.
            Keys are row indices (0-based), and values are heights in pixels.
            (Default: `{}`)

    Raises:
    -------
        TypeError:
            If any argument is not of the expected type.

        ValueError:
            If any argument is invalid (e.g., negative or out-of-range values).

    Example:
    --------
        Create a PyFlameGridLayout with 4 columns and 5 rows:
        ```
        grid_layout = PyFlameGridLayout(
            columns=4,
            rows=5,
            )
        ```

        Create a PyFlameGridLayout with 4 columns and 5 rows, with specific column widths:
        ```
        grid_layout = PyFlameGridLayout(
            columns=4,
            rows=5,
            adjust_column_widths={0: 200, 1: 150, 2: 100, 3: 50},
            )
        ```
    """

    def __init__(
        self: 'PyFlameGridLayout',
        columns: int = 0,
        rows: int = 0,
        column_width: int = 150,
        row_height: int = 28,
        adjust_column_widths: dict[int, int] = {},
        adjust_row_heights: dict[int, int] = {}
        ) -> None:
        super().__init__()

        # Validate all arguments
        self._validate_arguments(
            columns=columns,
            rows=rows,
            column_width=column_width,
            row_height=row_height,
            adjust_column_widths=adjust_column_widths,
            adjust_row_heights=adjust_row_heights
            )

        # Create and add widgets to the grid
        for row in range(rows):
            for col in range(columns):
                # If adjust_column_widths is None or empty, default to column_width
                if adjust_column_widths and col in adjust_column_widths:
                    width = adjust_column_widths[col]
                else:
                    width = column_width

                # If adjust_row_heights is None or empty, default to row_height
                if adjust_row_heights and row in adjust_row_heights:
                    height = adjust_row_heights[row]
                else:
                    height = row_height

                # Create the label with the specified dimensions
                empty_label = PyFlameLabel(
                    text='',
                    width=width,
                    height=height
                )
                self.addWidget(empty_label, row, col)

    @staticmethod
    def _validate_arguments(
        columns: int,
        rows: int,
        column_width: int,
        row_height: int,
        adjust_column_widths: dict[int, int],
        adjust_row_heights: dict[int, int]
        ) -> None:
        """
        Validate all arguments passed to the constructor.

        Args:
        -----
            `columns` (int):
                Number of columns.

            `rows` (int):
                Number of rows.

            `column_width` (int):
                Default column width.

            `row_height` (int):
                Default row height.

            `adjust_column_widths` (dict[int, int]):
                Column-specific width adjustments.

            `adjust_row_heights` (dict[int, int]):
                Row-specific height adjustments.

        Raises:
        -------
            TypeError:
                If any argument is of an incorrect type.

            ValueError:
                If any argument has invalid values.
        """

        # Validate core dimensions
        if not all(isinstance(arg, int) for arg in (columns, rows, column_width, row_height)):
            raise TypeError("Columns, rows, column_width, and row_height must all be integers.")
        if any(arg < 0 for arg in (columns, rows, column_width, row_height)):
            raise ValueError("Columns, rows, column_width, and row_height must be 0 or greater.")

        # Validate adjustment dictionaries
        for adjustments, limit, name in [
            (adjust_column_widths, columns, "column"),
            (adjust_row_heights, rows, "row")
            ]:
            if not isinstance(adjustments, dict):
                raise TypeError(f"adjust_{name}_widths must be a dictionary with integer keys and values.")
            for idx, value in adjustments.items():
                if not isinstance(idx, int) or not isinstance(value, int):
                    raise TypeError(f"adjust_{name}_widths keys and values must be integers.")
                if idx < 0 or idx >= limit:
                    raise ValueError(f"{name.capitalize()} index {idx} is out of range (0 to {limit - 1}).")
                if value <= 0:
                    raise ValueError(f"{name.capitalize()} size for {name} {idx} must be greater than 0.")

class PyFlameHBoxLayout(QtWidgets.QHBoxLayout):
    """
    PyFlameHBoxLayout
    =================

    Custom QT QHBoxLayout Subclass.

    Values are adjusted for display scale using `pyflame.gui_resize()`.

    Methods:
    --------
        `setSpacing(spacing)`:
            Apply spacing between widgets in PyFlameHBoxLayout adjusted for display scale using `pyflame.gui_resize()`.

        `setContentsMargins(left, top, right, bottom)`:
            Apply margins to PyFlameHBoxLayout adjusted for display scale using `pyflame.gui_resize()`.

    Example:
    --------
        To create a PyFlameHBoxLayout with a couple of widgets added to it:
        ```
        hbox_layout = PyFlameHBoxLayout()
        hbox_layout.setSpacing(10)
        hbox_layout.setContentsMargins(10, 10, 10, 10)
        hbox_layout.addWidget(self.label_01)
        hbox_layout.addWidget(self.pushbutton_01)
        ```
    """

    def __init__(self: 'PyFlameHBoxLayout') -> None:
        super().__init__()

    def setSpacing(self, spacing: int) -> None:
        """
        Set Spacing
        ===========

        Add fixed amount of space between widgets in the PyFlameHBoxLayout.

        Spacing is adjusted for display scale using `pyflame.gui_resize()`.

        The spacing affects all widgets added to the PyFlameHBoxLayout after the `setSpacing` call. It does not
        alter the PyFlameHBoxLayout's margins—use `setContentsMargins` for margin adjustments. The spacing is
        applied between the widgets themselves, not between widgets and the PyFlameHBoxLayout's border or between
        widgets and any layout containers (e.g., windows) they may be in.

        Args:
        -----
            `spacing` (int):
                Spacing in pixels.

        Raises:
        -------
            TypeError:
                If `spacing` is not an integer.

        Example:
        --------
            To set the spacing between widgets in the PyFlameHBoxLayout to 10 pixels:
            ```
            hbox_layout.setSpacing(10)
            ```
        """

        # Validate argument type
        if not isinstance(spacing, int):
            raise TypeError(f"PyFlameHBoxLayout.setSpacing: Expected 'spacing' to be an int, got {type(spacing).__name__} instead.")

        # Set Spacing
        super().setSpacing(pyflame.gui_resize(spacing))

    def addSpacing(self, spacing: int) -> None:
        """
        Add Spacing
        ===========

        Insert fixed amount of non-stretchable space between widgets in the PyFlameHBoxLayout.

        Spacing is adjusted for display scale using `pyflame.gui_resize()`.

        This method adds a spacer item of a specified size to the PyFlameHBoxLayout, effectively increasing
        the distance between the widget that precedes the spacer and the widget that follows it.
        The space is a one-time, non-adjustable gap that does not grow or shrink with the PyFlameHBoxLayout's
        resizing, providing precise control over the spacing in the PyFlameHBoxLayout.

        Args:
        -----
            `spacing` (int):
                Spacing in pixels.

        Raises:
        -------
            TypeError:
                If `spacing` is not an integer.

        Example:
        --------
            To add a 10-pixel space between two widgets in the PyFlameHBoxLayout:
            ```
            hbox_layout.addSpacing(10)
            ```
        """

        # Validate argument types
        if not isinstance(spacing, int):
            raise TypeError(f"PyFlameHBoxLayout.addSpacing: Expected 'spacing' to be an int, got {type(spacing).__name__} instead.")

        # Add Spacing
        super().addSpacing(pyflame.gui_resize(spacing))

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        """
        Set Contents Margins
        ====================

        Set margins around the contents of the PyFlameHBoxLayout.

        Values are adjusted for display scale using `pyflame.gui_resize()`.

        This method specifies the size of the margins on each side of the PyFlameHBoxLayout container.
        Margins are defined as the space between the outermost widgets in the PyFlameHBoxLayout and the
        edges of the PyFlameHBoxLayout's container (e.g., a window).

        Args:
        -----
            `left` (int):
                Left margin in pixels.

            `top` (int):
                Top margin in pixels.

            `right` (int):
                Right margin in pixels.

            `bottom` (int):
                Bottom margin in pixels.

        Raises:
        -------
            TypeError:
                If `left` is not an integer.
                If `top` is not an integer.
                If `right` is not an integer.
                If `bottom` is not an integer.

        Example:
        --------
            To set margins around the contents of the PyFlameHBoxLayout to 10 pixels:
            ```
            hbox_layout.setContentsMargins(10, 10, 10, 10)
            ```
        """

        # Validate argument type
        if not isinstance(left, int):
            raise TypeError(f"PyFlameHBoxLayout.setContentsMargins: Expected 'left' to be an int, got {type(left).__name__} instead.")
        if not isinstance(top, int):
            raise TypeError(f"PyFlameHBoxLayout.setContentsMargins: Expected 'top' to be an int, got {type(top).__name__} instead.")
        if not isinstance(right, int):
            raise TypeError(f"PyFlameHBoxLayout.setContentsMargins: Expected 'right' to be an int, got {type(right).__name__} instead.")
        if not isinstance(bottom, int):
            raise TypeError(f"PyFlameHBoxLayout.setContentsMargins: Expected 'bottom' to be an int, got {type(bottom).__name__} instead.")

        # Set Margins
        super().setContentsMargins(
            pyflame.gui_resize(left),
            pyflame.gui_resize(top),
            pyflame.gui_resize(right),
            pyflame.gui_resize(bottom)
            )

class PyFlameVBoxLayout(QtWidgets.QVBoxLayout):
    """
    PyFlameVBoxLayout
    =================

    Custom QT QVBoxLayout Subclass.

    Values are adjusted for display scale using `pyflame.gui_resize()`.

    Methods:
    --------
        `setSpacing(spacing)`:
            Apply spacing between widgets in the PyFlameVBoxLayout adjusted for display scale using `pyflame.gui_resize()`.

        `setContentsMargins(left, top, right, bottom)`:
            Apply margins to the PyFlameVBoxLayout adjusted for display scale using `pyflame.gui_resize()`.

    Example:
    --------
        To create a PyFlameVBoxLayout with a couple of widgets added to it:
        ```
        vbox_layout = PyFlameVBoxLayout()
        vbox_layout.setSpacing(10)
        vbox_layout.setContentsMargins(10, 10, 10, 10)
        vbox_layout.addWidget(self.label_01)
        vbox_layout.addWidget(self.pushbutton_01)
        ```
    """

    def __init__(self: 'PyFlameVBoxLayout') -> None:
        super().__init__()

    def setSpacing(self, spacing: int) -> None:
        """
        Set Spacing
        ===========

        Add fixed amount of space between widgets in the PyFlameVBoxLayout.

        Spacing is adjusted for display scale using `pyflame.gui_resize()`.

        The spacing affects all widgets added to the PyFlameVBoxLayout after the `setSpacing` call. It does not
        alter the PyFlameVBoxLayout's margins—use `setContentsMargins` for margin adjustments. The spacing is
        applied between the widgets themselves, not between widgets and the PyFlameVBoxLayout's border or between
        widgets and any PyFlameVBoxLayout containers (e.g., windows) they may be in.

        Args:
        -----
            `spacing` (int):
                Spacing in pixels.

        Raises:
        -------
            TypeError:
                If `spacing` is not an integer.

        Example:
        --------
            To set the spacing between widgets in the PyFlameVBoxLayout to 10 pixels:
            ```
            vbox_layout.setSpacing(10)
            ```
        """

        # Validate argument type
        if not isinstance(spacing, int):
            raise TypeError(f"PyFlameVBoxLayout.setSpacing: Expected 'spacing' to be an int, got {type(spacing).__name__} instead.")

        # Set Spacing
        super().setSpacing(pyflame.gui_resize(spacing))

    def addSpacing(self, spacing: int) -> None:
        """
        Add Spacing
        ===========

        Insert fixed amount of non-stretchable space between widgets in the PyFlameVBoxLayout.

        Spacing is adjusted for display scale using `pyflame.gui_resize()`.

        This method adds a spacer item of a specified size to the PyFlameVBoxLayout, effectively increasing
        the distance between the widget that precedes the spacer and the widget that follows it.
        The space is a one-time, non-adjustable gap that does not grow or shrink with the PyFlameVBoxLayout's
        resizing, providing precise control over the spacing in the PyFlameVBoxLayout.

        Args:
        -----
            `spacing` (int):
                Spacing in pixels.

        Raises:
        -------
            TypeError:
                If `spacing` is not an integer.

        Example:
        --------
            To add a 10-pixel space between two widgets in the PyFlameVBoxLayout:
            ```
            vbox_layout.addSpacing(10)
            ```
        """

        # Validate argument type
        if not isinstance(spacing, int):
            raise TypeError(f"PyFlameVBoxLayout.addSpacing: Expected 'spacing' to be an int, got {type(spacing).__name__} instead.")

        # Add Spacing
        super().addSpacing(pyflame.gui_resize(spacing))

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        """
        Set Contents Margins
        ====================

        Sets the margins around the contents of the PyFlameVBoxLayout.

        Values are adjusted for display scale using `pyflame.gui_resize()`.

        This method specifies the size of the margins on each side of the PyFlameVBoxLayout container.
        Margins are defined as the space between the outermost widgets in the PyFlameVBoxLayout and the
        edges of the PyFlameVBoxLayout's container (e.g., a window).

        Args:
        -----
            `left` (int):
                Left margin in pixels.
            `top` (int):
                Top margin in pixels.
            `right` (int):
                Right margin in pixels.
            `bottom` (int):
                Bottom margin in pixels.

        Raises:
        -------
            TypeError:
                If `left` is not an integer.
                If `top` is not an integer.
                If `right` is not an integer.
                If `bottom` is not an integer.

        Example:
        --------
            To set margins around the contents of the PyFlameVBoxLayout to 10 pixels:
            ```
            vbox_layout.setContentsMargins(10, 10, 10, 10)
            ```
        """

        # Validate argument type
        if not isinstance(left, int):
            raise TypeError(f"PyFlameVBoxLayout.setContentsMargins: Expected 'left' to be an int, got {type(left).__name__} instead.")
        if not isinstance(top, int):
            raise TypeError(f"PyFlameVBoxLayout.setContentsMargins: Expected 'top' to be an int, got {type(top).__name__} instead.")
        if not isinstance(right, int):
            raise TypeError(f"PyFlameVBoxLayout.setContentsMargins: Expected 'right' to be an int, got {type(right).__name__} instead.")
        if not isinstance(bottom, int):
            raise TypeError(f"PyFlameVBoxLayout.setContentsMargins: Expected 'bottom' to be an int, got {type(bottom).__name__} instead.")

        # Set Margins
        super().setContentsMargins(
            pyflame.gui_resize(left),
            pyflame.gui_resize(top),
            pyflame.gui_resize(right),
            pyflame.gui_resize(bottom)
            )

#-------------------------------------
# [PyFlame Window Classes]
#-------------------------------------

class PyFlamePresetManager():
    """
    PyFlamePresetManager
    ====================

    Handles management of presets for Flame python scripts.

    Actions
    -------

        New
        ---
            Creates a new preset using default values that can be edited.

        Edit
        ----
            Edit an existing preset from the preset list.

        Duplicate
        ---------
            Create a duplicate of the selected preset.

        Delete
        ------
            Delete the selected preset.
            If the selected preset is the default preset, the default preset will be set to the first preset in the preset list.
            If the selected preset is a project preset, all project presets using the preset will be set to the default preset.
            If the selected preset is both the default and project preset, the default preset will be set to the first preset in
            the preset list and all project presets using the preset will be set to the default preset.

        Set Default Preset
        ------------------
            Set the selected preset as the default preset.
            The default preset will be used for all Flame projects unless a project preset is set.

        Set Project Preset
        ------------------
            Set the selected preset as the project preset for the current project.
            This will bypass the default preset.

        Remove Project Preset
        ---------------------
            Remove the preset assigned to the current project.
            This will cause the current project to use the default preset.

    Args
    ----
        `script_version` (str):
            Version of the script.

        `setup_script` (callable):
            Setup window class/function.

        `script_name` (str):
            Name of the script.
            (Default: `SCRIPT_NAME`)

        `script_path` (str): Path to the script.
            (Default: `SCRIPT_PATH`)

    Raises
    ------
        TypeError:
            If `script_name` is not a string.
            if `script_version` is not a string.
            If `script_path` is not a string.
            If `setup_script` is not callable function.

    Example
    -------
        Initialize PyFlamePresetManager:
        ```
        PyFlamePresetManager(
            script_version=SCRIPT_VERSION,
            setup_script=ScriptSetup,
            )
        ```

    Public Methods
    --------------
        load_preset() -> PyFlameConfig:
            Loads preset assigned to current project(Project or Default Preset) and returns preset settings as attributes.
            ```
            self.settings = PyFlamePresetManager(
                script_version=SCRIPT_VERSION,
                setup_script=None,
                ).load_preset()
            ```
    """

    def __init__(
            self,
            script_version: str,
            setup_script: Callable[..., Any] = None,
            script_name: str=SCRIPT_NAME,
            script_path: str=SCRIPT_PATH,
        ):

        # Validate argument types
        if not isinstance(script_version, str):
            raise TypeError(f'PyFlamePresetManager: script_version must be a string.')
        elif setup_script is not None and not callable(setup_script):
            raise TypeError('PyFlamePresetManager: setup_script must be a callable function or None.')
        elif not isinstance(script_name, str):
            raise TypeError('PyFlamePresetManager: script_name must be a string.')
        elif not isinstance(script_path, str):
            raise TypeError(f'PyFlamePresetManager: script_path must a string.')

        print('\n')
        print(f'[========= {script_name} Preset Manager {script_version} =========]\n')

        # Initialize variables
        self.default_preset_extension = ' (Default)'
        self.project_preset_extension = ' (Project)'
        self.script_name = script_name
        self.script_version = script_version
        self.script_path = script_path
        self.setup_script = setup_script
        self.flame_prj_name = flame.project.current_project.project_name
        self.preset_settings_name = self.script_name.lower().replace(' ', '_') + '_preset_settings'

        # Initialize paths
        self.preset_config_json = os.path.join(self.script_path, 'config', 'preset_manager_config.json') # Preset Manager config file
        self.preset_path = os.path.join(self.script_path, 'config', 'presets')
        self.project_config_path = os.path.join(self.script_path, 'config', 'project_presets')

        # Create preset folders if they do not exist
        self.create_preset_folders()

        # Check script path
        if not self.check_script_path():
            return

        # Load/Create Preset Manager config file
        self.settings = self.load_config()

        if setup_script:
            # Open preset window
            self.preset_window()

    def check_script_path(self) -> bool:
        """
        Check Script Path
        =================

        Check if script is installed in the correct location.

        Returns:
        --------
            bool: True if script is installed in correct location, False if not.
        """

        if os.path.dirname(os.path.abspath(__file__)) != SCRIPT_PATH:
            PyFlameMessageWindow(
                message=f'Script path is incorrect. Please reinstall script.\n\nScript path should be:\n\n{self.script_path}',
                type=MessageType.ERROR,
                )
            return False
        return True

    def load_config(self) -> PyFlameConfig:
        """
        Load Config
        ===========

        Create/Load Preset Manager config values from config file.

        Returns:
        --------
            settings (PyFlameConfig): PyFlameConfig instance with loaded config values.
        """

        settings = PyFlameConfig(
            config_values={
                'default_preset': '',
                },
            config_path=self.preset_config_json,
            script_name=self.script_name,
            )

        return settings

    def save_config(self) -> None:
        """
        Save Config
        ===========

        Save Preset Manager config values to config file.
        """

        self.settings.save_config(
            config_values={
                'default_preset': self.settings.default_preset,
                },
            config_path=self.preset_config_json,
            )

    def message_print(self, message: str) -> None:
        """
        Message Print
        =============

        Print message to Flame message window and terminal/shell.

        Args:
        -----
            `message (str)`:
                Message to print.
        """

        pyflame.print(
            text=message,
            script_name=self.script_name,
            )

    def info_message(self, message: str) -> None:
        """
        Info Message
        ============

        Open info message window using PyFlameMessageWindow.

        Args:
        -----
            `message (str)`:
                The message to display.
        """

        PyFlameMessageWindow(
            message=message,
            script_name=self.script_name,
            )

    def error_message(self, message: str) -> None:
        """
        Error Message
        =============

        Open error message window using PyFlameMessageWindow.

        Args:
        -----
            `message (str)`:
                The message to display.
        """

        PyFlameMessageWindow(
            message=message,
            script_name=self.script_name,
            type=MessageType.ERROR,
            )

    def warning_message(self, message:str) -> bool:
        """
        Warning Message
        ===============

        Open warning message window using PyFlameMessageWindow.

        Args:
        -----
            `message (str)`:
                The message to display.

        Returns:
        --------
            confirm (bool): User confirmation to proceed.
        """

        confirm = PyFlameMessageWindow(
            message=message,
            script_name=self.script_name,
            type=MessageType.WARNING,
            )

        return confirm

    def confirm_message(self, message: str) -> bool:
        """
        Confirm Message
        ===============

        Open confirm message window using PyFlameMessageWindow.

        Args:
        -----
            `message (str)`:
                The message to display.

        Returns:
        --------
            confirm (bool): User confirmation to proceed.
        """

        confirm = PyFlameMessageWindow(
            message=message,
            script_name=self.script_name,
            type=MessageType.CONFIRM,
            )

        return confirm

    def create_preset_folders(self) -> None:
        """
        Create Preset Folders
        ======================

        Check for preset folders and create if they do not exist.
        """

        if not os.path.isdir(self.preset_path):
            os.makedirs(self.preset_path)

        if not os.path.isdir(self.project_config_path):
            os.makedirs(self.project_config_path)

    # ----------------------------------------------------------------------------------------------------------------------

    def preset_window(self) -> None:
        """
        Preset Window
        =============

        Build Preset Manager window.
        """

        def close_window() -> None:
            """
            Close Window
            ============

            Close preset window
            """

            self.preset_window.close()

            self.message_print('Done.')

        # Build window
        self.preset_window = PyFlameWindow(
            title=f'{self.script_name} Preset Manager <small>{self.script_version}',
            return_pressed=close_window,
            grid_layout_columns=7,
            grid_layout_rows=7,
            grid_layout_adjust_column_widths={4: 50},
            )

        # Labels
        self.current_project_preset_label = PyFlameLabel(
            text='Current Project Preset',
            )
        self.presets_label = PyFlameLabel(
            text='Presets',
            )

        # Entry Fields
        self.current_project_preset_field = PyFlameEntry(
            text='',
            placeholder_text='No presets available. Create a new preset.',
            read_only=True,
            )

        # Push Button Menu
        self.current_preset_menu_pushbutton = PyFlamePushButtonMenu(
            text='',
            menu_options=[],
            )

        #  Buttons
        self.new_button = PyFlameButton(
            text='New',
            connect=self.new_preset,
            tooltip='Create new preset.',
            )
        self.set_as_default_button = PyFlameButton(
            text='Set Default Preset',
            connect=self.set_as_default_preset,
            tooltip='Set selected preset as default preset. The default preset will be used for all Flame projects unless a different preset is set for the current project.',
            )
        self.edit_button = PyFlameButton(
            text='Edit',
            connect=self.edit_preset,
            tooltip='Edit selected preset.',
            )
        self.set_project_preset_button = PyFlameButton(
            text='Set Project Preset',
            connect=self.set_preset_to_current_project,
            tooltip='Set current preset as current project preset. This will bypass the default preset.',
            )
        self.remove_from_project_button = PyFlameButton(
            text='Remove Project Preset',
            connect=self.remove_preset_from_project,
            tooltip='Remove preset assigned to current project.',
            )
        self.delete_button = PyFlameButton(
            text='Delete',
            connect=self.delete_preset,
            tooltip='Delete selected preset.',
            )
        self.duplicate_button = PyFlameButton(
            text='Duplicate',
            connect=self.duplicate_preset,
            tooltip='Duplicate selected preset.',
            )

        self.done_btn = PyFlameButton(
            text='Done',
            connect=close_window,
            color=Color.BLUE,
            )

        # Get current project preset to display in current project preset field
        self.update_ui()

        #-------------------------------------
        # [Widget Layout]
        #-------------------------------------

        self.preset_window.grid_layout.addWidget(self.current_project_preset_label, 0, 0)
        self.preset_window.grid_layout.addWidget(self.current_project_preset_field, 0, 1, 1, 3)
        self.preset_window.grid_layout.addWidget(self.presets_label, 1, 0)
        self.preset_window.grid_layout.addWidget(self.current_preset_menu_pushbutton, 1, 1, 1, 3)

        self.preset_window.grid_layout.addWidget(self.new_button, 1, 5)
        self.preset_window.grid_layout.addWidget(self.edit_button, 1, 6)

        self.preset_window.grid_layout.addWidget(self.duplicate_button, 2, 5)
        self.preset_window.grid_layout.addWidget(self.delete_button, 2, 6)

        self.preset_window.grid_layout.addWidget(self.set_as_default_button, 3, 5)

        self.preset_window.grid_layout.addWidget(self.set_project_preset_button, 4, 5)
        self.preset_window.grid_layout.addWidget(self.remove_from_project_button, 4, 6)

        self.preset_window.grid_layout.addWidget(self.done_btn, 6, 6)

        # self.preset_window.add_layout(grid_layout)
        # self.preset_window.show()

    # ---------------------------------------- #
    # Button Functions
    # ---------------------------------------- #

    def new_preset(self) -> None:
        """
        New Preset
        ==========

        Create a new preset by opening the setup window with default settings.
        """

        self.message_print('Creating new preset...')

        new_preset_name = self.create_or_edit_preset()

        if new_preset_name:
            self.message_print(f'New preset created: {new_preset_name}')
        else:
            self.message_print('New preset creation cancelled.')

    def edit_preset(self) -> None:
        """
        Edit Preset
        ===========

        Edit the currently selected preset by loading the setup window with the preset settings.
        """

        self.message_print('Editing selected preset...')

        # Get config settings from selected preset
        preset = self.get_current_preset_button_name()
        preset_path = os.path.join(self.preset_path, preset + '.json')
        #print('Preset Path:', preset_path, '\n')

        settings = PyFlameConfig.get_config_values(config_path=preset_path)
        #print('Settings Dict:', settings, '\n')

        preset_config = PyFlameConfig(
            config_values=settings,
            config_path=preset_path,
            script_name=self.script_name,
            )

        # Load Setup window passing preset_config to load preset values.
        preset_name = self.create_or_edit_preset(preset_path=preset_path, preset_config=preset_config)

        if preset_name:
            self.message_print(f'Edited preset: {preset_name}')
        else:
            self.message_print('Edit cancelled.')

    def set_as_default_preset(self) -> None:
        """
        Set as Default Preset
        ======================

        Set currently selected preset as the default preset.
        Default preset will have ' (Default)' added to the end of the name.

        Updates current Current Project Preset field, Preset button, Preset list, and config file.
        """

        self.message_print('Updating default preset...')

        if self.current_preset_menu_pushbutton.text():
            self.update_default_preset(self.current_preset_menu_pushbutton.text())# Set default preset in preset config JSON
            self.update_ui() # Update UI with new default preset
            self.message_print(f'Default preset set to: {self.current_preset_menu_pushbutton.text()}')
        else:
            self.message_print('No preset selected to set as Default Preset.')

    def set_preset_to_current_project(self) -> None:
        """
        Set Preset to Current Project
        ==============================

        Assigns the current preset to the current project.

        Set the currently selected preset as the project preset for the current project.
        If a project preset already exists for the current project, it will be deleted and replaced with the new preset.

        If there is no preset currently selected, the function prints a message indicating that no preset was selected to set as the project preset.
        """

        self.message_print('Assigning preset to current project...')

        if self.current_preset_menu_pushbutton.text():
            preset_name_text = self.get_current_preset_button_name() # Get current preset button name
            #print('Preset Name Text:', preset_name_text, '\n')

            # Path for new preset file
            preset_path = os.path.join(self.project_config_path, self.flame_prj_name + '.json')

            # If project preset already exists, delete it before creating new one.
            if os.path.isfile(preset_path):
                os.remove(preset_path)

            # Create project preset
            self.create_project_preset_json(preset_name_text, preset_path)

            # Update ui with new project preset name
            self.update_ui() # Update UI with new preset

            self.message_print(f'Preset set for this project: {preset_name_text}')
        else:
            self.message_print('No preset selected to set as Project Preset.')

    def remove_preset_from_project(self) -> None:
        """
        Remove Preset from Project
        ==========================

        Remove the preset from the current project.

        Unassign the preset from the current project. If the preset is not set as the default preset,
        it will no longer be associated with this project. The preset file itself will not be deleted, only its
        association with the current project is removed.

        Note:
        - If the preset is also set as the default preset, it will remain associated with the project.
        - This function updates the UI after removing the preset.
        """

        preset_name = self.get_current_preset_button_name() # Get current preset from push button

        self.message_print(f'Removing preset from project: {preset_name}')

        # Delete project preset JSON file
        project_preset_path = os.path.join(self.project_config_path, self.flame_prj_name + '.json')
        if os.path.isfile(project_preset_path):
            os.remove(project_preset_path)
            self.message_print(f'Preset removed from project: {preset_name}')
        else:
            self.message_print(f'No project preset found for current project.')

        # Update UI
        self.update_ui()

    def duplicate_preset(self) -> None:
        """
        Duplicate Preset
        ================

        Create a duplicate of the currently selected preset.

        Duplicate the currently selected preset by creating a copy of its JSON file with 'copy' appended to the end of its name.
        If there are existing presets with the same name in the preset directory, 'copy' is incrementally appended until a unique name is found.

        If there is no preset currently selected, the function prints a message indicating that no preset was selected for duplication.

        Note:
        - The duplicated preset maintains the same settings as the original.
        - The duplicated preset is immediately added to the preset menu and displayed in the UI.
        """

        print('Duplicating preset...\n')

        if self.current_preset_menu_pushbutton.text():
            # Get list of existing saved presets
            existing_presets = [f[:-5] for f in os.listdir(self.preset_path)]

            # Get current preset name from push button
            current_preset_name = self.get_current_preset_button_name()

            # Set new preset name to current preset name
            new_preset_name = current_preset_name

            # If preset name already exists, add ' copy' to the end of the name until a unique name is found
            while new_preset_name in existing_presets:
                new_preset_name = new_preset_name  + ' copy'

            # Duplicate preset JSON file with new preset name
            source_file = os.path.join(self.preset_path, current_preset_name + '.json')
            dest_file = os.path.join(self.preset_path, new_preset_name + '.json')
            shutil.copyfile(source_file, dest_file)

            # Update preset name in new preset JSON file
            self.preset_json_save_preset_name(
                preset_path=dest_file,
                preset_name=new_preset_name,
                )

            # Update UI
            self.update_ui()
            self.current_preset_menu_pushbutton.setText(new_preset_name)

            self.message_print(f'Duplicate preset created: {new_preset_name}')
        else:
            print('No preset selected to duplicate.\n')

    def delete_preset(self) -> None:
        """
        Delete Preset
        =============

        Deletes the currently selected preset.

        This function ensures that the preset being deleted is not in use by any project preset or set as the default preset.
        If the preset is the default preset, the preset at the top of the list will be set as the default preset until one is set.
        If the preset is being used by other projects, the user will be prompted to confirm deletion. All project presets using the preset
        being deleted will be set to the default preset.
        """

        def check_project_files():
            """
            Check all project config files for the current preset before deletion.
            """

            preset_names = []
            preset_paths = []

            if os.listdir(self.project_config_path):
                for config_file in os.listdir(self.project_config_path):
                    preset_path = os.path.join(self.project_config_path, config_file)
                    saved_preset_name = self.get_project_preset_name_json(preset_path)
                    preset_names.append(saved_preset_name)
                    preset_paths.append(preset_path)

            if preset_names:
                if preset_name.split(' (Project)')[0] in preset_names:
                    return preset_paths # User confirmed deletion.
                else:
                    return True # Preset not used by other projects, can be deleted.
            else:
                return True # No project presets, can be deleted.

        print('Deleting preset...\n')

        if self.current_preset_menu_pushbutton.text():
            preset_name = self.current_preset_menu_pushbutton.text() # Get current preset from push button
            preset_path = os.path.join(self.preset_path, preset_name + '.json') # Get path to preset JSON file

            project_files = check_project_files()

            # If selected preset is not the default preset, confirm deletion, check to see if other projects are using preset, then delete preset, otherwise return.
            if not preset_name.endswith(self.default_preset_extension) and not preset_name.endswith(self.project_preset_extension):
                if self.warning_message(message=f'Delete preset: {preset_name}'):
                    # Check all project config files for current preset before deleting.
                    if project_files:
                        os.remove(preset_path)
                        self.update_ui() # Update UI with new default preset
                        self.message_print(f'Preset deleted: {preset_name}')
                        self.save_config()
                    else:
                        return
                else:
                    return

            # If selected preset is the default preset, confirm that the user wants to delete it.
            elif preset_name.endswith(self.default_preset_extension):
                confirm_delete = self.warning_message(message=f'Selected preset is currently the default preset.\n\nDeleting this preset will set the default preset to the first saved preset in the preset list.\n\nAre you sure you want to delete this preset?')
                if not confirm_delete:
                    return

            # If selected preset it the project preset, confirm that the user wants to delete it.
            elif preset_name.endswith(self.project_preset_extension):
                confirm_delete = self.warning_message(message=f'Selected preset is currently the project preset for one or more projects.\n\nDeleting this preset will set all those projects to the default preset.\n\nAre you sure you want to delete this preset?')
                if not confirm_delete:
                    return

            # If user confirmed deletion, check all project config files for current preset before deleting.
            if confirm_delete:
                if project_files:
                    # If confirmed, delete preset
                    preset_path = os.path.join(self.preset_path, preset_name + '.json')
                    os.remove(os.path.join(self.preset_path, self.get_current_preset_button_name() + '.json'))

                    # Set new default preset to first preset in preset list if it exists, otherwise set to empty string
                    if os.listdir(self.preset_path):
                        new_preset = self.get_preset_list()[0]
                    else:
                        new_preset = ''

                    # Delete all project presets using preset being deleted
                    if isinstance(project_files, list):
                        for path in project_files:
                            os.remove(path)

                    # Update UI and config file with new default preset
                    self.update_default_preset(new_preset) # Update preset name
                    self.update_ui() # Update UI with new default preset
                    self.message_print(f'Preset deleted: {preset_name}')
                    return
        else:
            print('No preset selected to delete.\n')

    # ---------------------------------------- #
    # Button Helper Functions
    # ---------------------------------------- #

    def create_or_edit_preset(self, preset_path: str=None, preset_config: PyFlameConfig=None) -> None:
        """
        Create or Edit Preset
        =====================

        Creates a new preset or edits an existing one.

        Create a new preset or the modification of an existing one.
        Hides the preset window during the modification process, then loads the setup window
        to allow users to modify preset settings. After the modification is complete, it updates
        the UI and returns the name of the modified or newly created preset.

        Args:
        -----
            `preset_path` (str, optional):
                The path to the existing preset JSON file. If provided, the function will edit the preset located at this path. Defaults to None.

            `preset_config` (PyFlameConfig, optional): An instance of PyFlameConfig representing the existing preset
                configuration.
                (Default: `None`)

        Returns:
        --------
            str or None: The name of the modified or newly created preset, if successful. Returns None if the
            preset modification or creation process is canceled.

        Raises:
        -------
            TypeError:
                If `new_preset.settings` is not a dictionary.

        Example:
        --------
            Creating a new preset:
            ```
            new_preset_name = self.create_or_edit_preset()
            ```

            Editing an existing preset:
            ```
            edited_preset_name = self.create_or_edit_preset(preset_path='/path/to/preset.json', preset_config=preset_config)
            ```
        """

        # Hide preset window while creating new preset
        self.preset_window.hide()

        # Load Setup window passing preset_config to load preset values.
        new_preset = self.setup_script(settings=preset_config)

        # Restore preset window after creating new preset
        self.preset_window.show()

        # If preset name is changed during edit, update all project presets using preset with new preset name
        if new_preset.settings:
            # Check to make sure new_preset.settings is returning a dictionary
            if not isinstance(new_preset.settings, dict):
                raise TypeError(f"PyFlamePresetManager: Expected 'new_preset.settings' to be a dictionary, got {type(new_preset.settings).__name__} instead.")

            # Remove old preset file if replacing preset
            if preset_path:
                os.remove(preset_path)

            # Get preset_name value from new_preset.settings dictionary
            new_preset_name = new_preset.settings['preset_name']

            new_default_preset_name = ''

            # If preset list is empty, set new preset as default preset
            if not self.get_preset_list() or new_preset_name == self.settings.default_preset:
                self.update_default_preset(new_preset_name)
                new_default_preset_name += self.default_preset_extension

            # Save new preset to file
            PyFlameConfig(
                config_values=new_preset.settings,
                config_path=os.path.join(os.path.join(self.script_path, 'config', 'presets'), new_preset_name + '.json'),
                script_name=self.script_name,
                )

            # Update UI with new preset name
            self.update_ui()

            if new_default_preset_name:
                self.current_preset_menu_pushbutton.setText(new_preset_name + new_default_preset_name)
            else:
                self.current_preset_menu_pushbutton.setText(new_preset_name)

            return new_preset_name

        else:
            return None

    def create_project_preset_json(self, preset_name: str, preset_path: str) -> None:
        """
        Create Project Preset JSON
        ==========================

        Creates a new project preset JSON file with the specified preset name.

        Args:
        -----
            `preset_name (str)`:
                The name of the preset.

            `preset_path (str)`:
                The path to the project preset JSON file.
        """

        # Create project preset as a dictionary
        preset_json = {
                "preset_name": preset_name
            }

        # Create or overwrite the preset file with JSON content
        with open(preset_path, 'w') as json_file:
            json.dump(preset_json, json_file, indent=4)
            print(f"Preset file created at {preset_path}")

        # Update and save new preset file with current preset name
        self.preset_json_save_preset_name(preset_path, preset_name)

    def update_project_presets(self, old_preset_name: str, new_preset_name: str):
        """
        Update Project Presets
        ======================

        This function iterates through all project presets in the project config path. If it finds a project preset with the old preset name,
        it updates the project preset to use the new preset name.

        Args:
        -----
            `old_preset_name (str)`:
                The name of the preset to be replaced.

            `new_preset_name (str)`:
                The new name of the preset.
        """

        self.message_print(f'Updating project presets to new preset name: {new_preset_name}')

        for project_preset_json in os.listdir(self.project_config_path):
            project_preset_json_path = os.path.join(self.project_config_path, project_preset_json)
            project_preset_name = self.get_project_preset_name_json(project_preset_json_path)
            if project_preset_name == old_preset_name:
                self.preset_json_save_preset_name(project_preset_json_path, new_preset_name)

        self.message_print(f'Updated project presets to new preset name: {new_preset_name}')

    def get_project_preset_name_json(self, project_preset_path: str) -> str:
        """
        Get Project Preset Name JSON
        ============================

        Get name of preset from project preset JSON file.

        Args:
        -----
            `project_preset_path (str)`:
                Path to project preset JSON file.
        """

        # Load the JSON file
        with open(project_preset_path, 'r') as json_file:
            data = json.load(json_file)

        # Extract the preset name
        preset_name = data.get("preset_name", None)

        return preset_name

    def get_preset_list(self) -> List[str]:
        """
        Get Preset List
        ===============

        Builds list of presets from preset folder.
        Adds (Default) to the end of the default preset name.
        Sorts list alphabetically.

        Returns:
        --------
            `preset_list (List[str])`:
                List of preset names.
        """

        try:
            presets = [file[:-5] for file in os.listdir(self.preset_path)]
            if self.settings.default_preset in presets:
                default_index = presets.index(self.settings.default_preset)
                presets[default_index] += self.default_preset_extension
        except Exception as e:
            print(f"Error listing presets: {e}")
            return []
        else:
            presets.sort()
            return presets

    def update_ui(self) -> None:
        """
        Update UI
        =========

        Updates Preset Manager UI based on the current preset settings.

        This function updates UI elements such as the Current Project Preset field, Current Preset button, and Preset list
        based on the current preset settings. It checks if a project preset exists for the current project. If a project preset
        exists, it uses that preset. If no project preset exists, it uses the default preset. If no default preset exists, it
        uses the first preset in the list of available presets. If no presets exist, the Current Project Preset field will
        display 'No saved presets found.'
        """

        def get_project_preset_name() -> str:
            """
            Checks for an existing project preset and returns its name.

            Returns:
                str: The name of the project preset if found, else None.
            """

            print('PROJECT NAME:', self.flame_prj_name)

            print('list dir:', os.listdir(self.project_config_path))

            # Check for existing project preset in project preset folder
            try:
                project_preset = [f[:-5] for f in os.listdir(self.project_config_path) if f[:-5] == self.flame_prj_name][0]
            except:
                project_preset = False

            # If project preset is found, get preset name from project preset file. Else return None.
            if project_preset:
                project_preset_path = os.path.join(self.project_config_path, project_preset + '.json')
                preset_name = self.get_project_preset_name_json(project_preset_path) # Get preset name from project preset JSON file
                preset_path = os.path.join(self.preset_path, preset_name + '.json')

                # If preset exists, return preset name adding (Default) if preset is default preset.
                # Else preset does not exist, delete project preset JSON and return None.
                if os.path.isfile(preset_path):
                    # If preset name is the default preset, add (Default) to the end of the name
                    if preset_name == self.settings.default_preset:
                        preset_name = preset_name + self.default_preset_extension
                    return preset_name
                else:
                    os.remove(project_preset_path) # Delete project preset JSON file
                    return None
            else:
                return None

        def update_buttons() -> None:
            """
            Update which buttons are enabled or disabled based on current preset field.
            """

            # Get text from current project preset field
            current_preset = self.current_project_preset_field.text()

            # If 'No saved presets found.' is in current preset field, disable buttons
            if current_preset == 'No saved presets found.':
                self.set_as_default_button.setEnabled(False)
                self.edit_button.setEnabled(False)
                self.set_project_preset_button.setEnabled(False)
                self.remove_from_project_button.setEnabled(False)
                self.delete_button.setEnabled(False)
                self.duplicate_button.setEnabled(False)
            else:
                self.set_as_default_button.setEnabled(True)
                self.edit_button.setEnabled(True)
                self.set_project_preset_button.setEnabled(True)
                self.delete_button.setEnabled(True)
                self.duplicate_button.setEnabled(True)

            # If ' (Project)' is not in current preset field, disable remove project preset button
            if not current_preset.endswith(self.project_preset_extension):
                self.remove_from_project_button.setEnabled(False)
            else:
                self.remove_from_project_button.setEnabled(True)

        self.message_print('Updating Preset Manager UI...')

        # Get list of existing presets
        existing_presets = self.get_preset_list()
        #print('EXISTING PRESETS:', existing_presets, '\n')

        # Check for to see if a project preset is set for current project
        preset = get_project_preset_name()
        if preset:
            new_preset_name = preset + self.project_preset_extension
            #print('NEW PRESET NAME:', new_preset_name, '\n')
            if new_preset_name.endswith(' (Default) (Project)'):
                new_preset_name = new_preset_name.replace(' (Default) (Project)', ' (Project)')
            # Add project preset extension to preset name in existing presets list
            if preset in existing_presets:
                existing_presets[existing_presets.index(preset)] = new_preset_name
            # Add project preset extension to preset name
            preset = new_preset_name
            #print('Project Preset:', preset, '\n')

        # If no project preset exists, try using the default preset, else set to first preset in list, if it exists, else set to 'No saved presets found.'
        else:
            preset = self.settings.default_preset
            if os.path.isfile(os.path.join(self.preset_path, preset + '.json')):
                preset = preset + self.default_preset_extension
            else:
                presets = existing_presets
                if presets:
                    preset = presets[0]
                    self.update_default_preset(preset)
                else:
                    preset = 'No saved presets found.'
        #print('Current Project Preset:', preset, '\n')

        # Update current preset push button and current project preset field
        self.current_preset_menu_pushbutton.setText(preset)
        self.current_project_preset_field.setText(preset)
        self.current_preset_menu_pushbutton.update_menu(preset, existing_presets)

        # Update which buttons are enabled or disabled based on current preset field
        update_buttons()

        self.message_print('Preset Manager UI Updated.')

    def get_current_preset_button_name(self) -> str:
        """
        Get Current Preset Button Name
        ===============================

        Get current preset button text. Remove ' (Default)' or '( Project)' if it exists in name.

        Returns:
        --------
            current_preset (str): Current preset name.
        """

        # Get current preset name from push button
        current_preset = self.current_preset_menu_pushbutton.text()

        # Remove ' (Default)' or '( Project)' from preset name if it exists
        if current_preset.endswith(self.default_preset_extension):
            current_preset = current_preset[:-10]
        elif current_preset.endswith(self.project_preset_extension):
            current_preset = current_preset[:-9]
        current_preset = current_preset.strip()

        return current_preset

    def update_default_preset(self, new_default_preset: str) -> None:
        """
        Update Default Preset
        =====================

        Update default preset setting and write to config file.

        Args:
        -----
            `new_default_preset (str)`:
                New default preset name.
        """

        # Remove ' (Default)' from preset name if it exists
        if new_default_preset.endswith(self.default_preset_extension):
            new_default_preset = new_default_preset[:-10]
        #print('new_default_preset:', new_default_preset, '\n')

        # Update default preset setting
        self.settings.default_preset = new_default_preset

        # Update config file with new default preset
        self.save_config()

        print(f'--> Updated default preset to: {new_default_preset}')

    def preset_json_save_preset_name(self, preset_path: str, preset_name: str) -> None:
        """
        Preset JSON Save Preset Name
        ============================

        Add preset name to project preset JSON file.

        Args:
        -----
            `preset_path (str)`:
                Path to project preset JSON file.

            `preset_name (str)`:
                Name of preset.
        """

        # Read the JSON file
        with open(preset_path, 'r') as file:
            data = json.load(file)

        # Update the preset_name field
        data['preset_name'] = preset_name

        # Write the updated data back to the JSON file
        with open(preset_path, 'w') as file:
            json.dump(data, file, indent=4)

    # ---------------------------------------- #
    # Public Methods
    # ---------------------------------------- #

    def load_preset(self) -> PyFlameConfig:
        """
        Load Preset
        ===========

        Load preset from preset JSON file and return settings.

        Returns:
        --------
            settings: With preset values as attributes.
        """

        def get_project_preset() -> str:
            """
            Check for project preset. If found, return project preset path.

            Returns:
            --------
                project_preset (str):
                    Path to project preset JSON file.
            """

            print('Checking for project preset...')

            try:
                project_preset_list = [f[:-5] for f in os.listdir(self.project_config_path)]
            except:
                project_preset_list = []
            print('Project Preset List:', project_preset_list, '\n')

            if self.flame_prj_name in project_preset_list:
                # Get project preset name from project preset JSON file
                project_preset = os.path.join(self.project_config_path, self.flame_prj_name + '.json')
                project_preset_name = self.get_project_preset_name_json(project_preset)
                # Get path to preset set as project preset
                project_preset = os.path.join(self.preset_path, project_preset_name + '.json')
                print('Project Preset found:', project_preset)
            else:
                project_preset = None
                print('No Project Preset found.')

            return project_preset

        def get_default_preset() -> str:
            """
            Check for default preset. If found, return preset path.

            Returns:
            --------
                default_preset (str):
                    Path to default preset JSON file.
            """

            print('Checking for default preset...')

            # Get list of existing presets
            existing_presets = self.get_preset_list()

            if self.settings.default_preset:
                default_preset = os.path.join(self.preset_path, self.settings.default_preset + '.json')
                print('Default Preset found:', default_preset, '\n')
            elif existing_presets:
                default_preset = os.path.join(self.preset_path, existing_presets[0] + '.json')
                print('Default Preset not set, using first preset found:', default_preset, '\n')
            else:
                print('No Default Preset found.\n')
                default_preset = None

            return default_preset

        print('Loading preset...')

        # Check for project preset JSON file
        preset_path = get_project_preset()

        # if no project preset is found, use default preset
        if not preset_path:
            preset_path = get_default_preset()

        # if no default preset is found, give message to create new preset in script setup.
        if not preset_path:
            #print('No presets found. Open setup window to create new preset.\n')
            self.info_message('No presets found.\n\nGo to script setup to create new preset.\n\nFlame Main Menu -> Logik -> Logik Portal Script Setup -> Uber Save Setup')
            return

        settings = PyFlameConfig(
            config_values=PyFlameConfig.get_config_values(config_path=preset_path),
            config_path=preset_path,
            script_name=self.script_name,
            )

        return settings

class PyFlameMessageWindow(QtWidgets.QDialog):
    """
    PyFlameMessageWindow
    ====================

    Custom QT Flame Message Window.

    Messsage window to display various types of messages.

    Args:
    -----
        `message` (str):
            Text displayed in the body of the window.

        `type` (MessageType):
            Type of message window to be shown.
            (Default: `MessageType.INFO`)

        `title` (str, optional):
            Use to override default title for message type.
            (Default: `None`)

        `script_name` (str, optional):
            Name of script. Used to set window title.
            (Default: `SCRIPT_NAME`)

        `time` (int):
            Time in seconds to display message in flame message area.
            (Default: `3`)

        `font` (str):
            Message font.
            (Default: `PYFLAME_FONT`)

        `font_size` (int):
            Message font size.
            (Default: `PYFLAME_FONT_SIZE`)

        `parent` (QtWidget, optional):
            Parent window.
            (Default: `None`)

    Message Types:
    --------------
        - `MessageType.INFO`:
            - Title: SCRIPT_NAME
            - Title with no script_name: Python Hook
            - Window lines: Blue
            - Buttons: Ok
        - `MessageType.OPERATION_COMPLETE`:
            - Title: SCRIPT_NAME: Operation Complete
            - Title with no script_name: Python Hook: Operation Complete
            - Window lines: Blue
            - Buttons: Ok
        - `MessageType.CONFIRM`:
            - Title: SCRIPT_NAME: Confirm Operation
            - Title with no script_name: Python Hook: Confirm Operation
            - Window lines: Grey
            - Buttons: Confirm, Cancel
            - Returns bool value.
        - `MessageType.ERROR`:
            - Title: SCRIPT_NAME: Error
            - Title with no script_name: Python Hook: Error
            - Window lines: Yellow
            - Buttons: Ok
        - `MessageType.WARNING`:
            - Title: SCRIPT_NAME: Warning
            - Title with no script_name: Python Hook: Warning
            - Window lines: Red
            - Buttons: Confirm, Cancel
            - Returns bool value.

    Returns:
    --------
        bool: True if confirm button is pressed, False if cancel button is pressed.
              A bool value is only returned for `MessageType.CONFIRM` and `MessageType.WARNING`.

    Examples:
    ---------
        Example for an error message:
        ```
        PyFlameMessageWindow(
            message=(
                'File not found.'
                ),
            type=MessageType.ERROR,
            )
        ```

        Example for a confirmation message, returns a bool:
        ```
        proceed = PyFlameMessageWindow(
            message='Do you want to do this?',
            type=MessageType.CONFIRM,
            )
        ```
    """

    def __init__(self: 'PyFlameMessageWindow',
                 message: str,
                 type: MessageType=MessageType.INFO,
                 title: Optional[str]=None,
                 script_name: str=SCRIPT_NAME,
                 time: int=5,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 parent=None
                 ):
        super().__init__()

        # Validate argument types
        if not isinstance(message, str):
            raise TypeError('PyFlameMessageWindow: message must be a string.')
        elif script_name is not None and not isinstance(script_name, str):
            raise TypeError('PyFlameMessageWindow: script_name must be a string or None.')
        elif not isinstance(type, MessageType):
            raise ValueError('PyFlameMessageWindow: type must be an instance of Type Enum: '
                            'MessageType.INFO, MessageType.OPERATION_COMPLETE, MessageType.CONFIRM, MessageType.ERROR, '
                            'MessageType.WARNING.')
        elif title is not None and not isinstance(title, str):
            raise TypeError('PyFlameMessageWindow: title must be a string or None.')
        elif not isinstance(time, int):
            raise TypeError('PyFlameMessageWindow: time must be an integer.')
        elif not isinstance(font, str):
            raise TypeError('PyFlameMessageWindow: font must be a string.')
        elif not isinstance(font_size, int) or font_size <= 0:
            raise TypeError('PyFlameMessageWindow: font_size must be a positive integer.')

        self.type = type
        self.confirmed = False

        # Set common button
        self.button = PyFlameButton(
            text='Ok',
            connect=self.confirm,
            width=110,
            color=Color.BLUE,
        )

        self.confirm_button = PyFlameButton(
            text='Confirm',
            connect=self.confirm,
            width=110,
            color=Color.BLUE,
        )

        # Set message window type options
        if type == MessageType.INFO:
            if not title:
                title = script_name

        elif type == MessageType.OPERATION_COMPLETE:
            if not title:
                title = f'{script_name}: Operation Complete'

        elif type == MessageType.ERROR:
            if not title:
                title = f'{script_name}: Error'

        elif type == MessageType.CONFIRM:
            if not title:
                title = f'{script_name}: Confirm Operation'
            self.button.setText = 'Confirm'

        elif type == MessageType.WARNING:
            if not title:
                title = f'{script_name}: Warning'
            self.confirm_button.set_button_color(Color.RED)

        message_font = font

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Set Window size for screen
        self.width = pyflame.gui_resize(500)
        self.height = pyflame.gui_resize(330)

        # Create message window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(QtCore.QSize(self.width, self.height))
        self.setStyleSheet(f"""
            background-color: rgb(36, 36, 36);
        """)

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        resolution = main_window_res.screenGeometry()

        # Center window on screen
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.setParent(parent)

        self.grid = QtWidgets.QGridLayout()

        self.title_label = PyFlameLabel(
            text=title,
            width=500,
            font_size=24,
            )

        self.message_text = QtWidgets.QTextEdit()
        self.message_text.setPlainText(message)
        self.message_text.setReadOnly(True)
        self.message_text.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.message_text.setFont(font)
        self.message_text.setStyleSheet(f"""
            QTextEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                selection-color: rgb(190, 190, 190);
                selection-background-color: rgb(36, 36, 36);
                border: none;
                padding-left: 1px;
                }}
            QScrollBar::handle{{
                background: {Color.SCROLLBAR_HANDLE.value};
                }}
            QScrollBar:vertical{{
                width: {pyflame.gui_resize(8)}px;  /* Adjust the width of the vertical scrollbar */
                }}
            QScrollBar:horizontal{{
                height: {pyflame.gui_resize(8)}px;  /* Adjust the height of the horizontal scrollbar */
                }}
            """)

        # Set layout for message window
        row_height = pyflame.gui_resize(pyflame.gui_resize(30))

        if type == MessageType.CONFIRM or type == MessageType.WARNING:
            self.cancel_button = PyFlameButton(
                text='Cancel',
                connect=self.cancel,
                width=110,
                )
            self.grid.addWidget(self.title_label, 0, 0)
            self.grid.setRowMinimumHeight(1, row_height)
            self.grid.addWidget(self.message_text, 2, 0, 4, 8)
            self.grid.setRowMinimumHeight(9, row_height)
            self.grid.addWidget(self.cancel_button, 10, 5)
            self.grid.addWidget(self.confirm_button, 10, 6)
        else:
            self.grid.addWidget(self.title_label, 0, 0)
            self.grid.setRowMinimumHeight(1, row_height)
            self.grid.addWidget(self.message_text, 2, 0, 4, 8)
            self.grid.setRowMinimumHeight(9, row_height)
            self.grid.addWidget(self.button, 10, 6)

        self.setLayout(self.grid)

        self._print(message, title, time) # Print message to terminal and Flame's console area

        self.exec()

    def __bool__(self):
        return self.confirmed

    def _print(self, message: str, title: str, time: int):
        """
        Print
        ======

        Private method to print to the terminal/shell and Flame's console area.

        Notes:
        ------
            This method is intended for internal use only and should not be called directly.
        """

        def print_message(color_code: str, message_type: str, message: str):
            print(
                f'{color_code}' + # Set text color
                '=' * 80 + '\n' +
                f'{message_type}: {SCRIPT_NAME.upper()}' + '\n' +
                '=' * 80 + '\n\n' +
                f'{message}\n\n' +
                '-' * 80 + '\n'
                f'{TextColor.RESET.value}'  # Reset text color
                )

        # Print to terminal/shell
        if self.type == MessageType.INFO or self.type == MessageType.OPERATION_COMPLETE or self.type == MessageType.CONFIRM:
            print_message(TextColor.BLUE.value, 'Info', message)
        elif self.type == MessageType.WARNING:
            print_message(TextColor.RED.value, 'Warning', message)
        elif self.type == MessageType.ERROR:
            print_message(TextColor.YELLOW.value, 'Error', message)

        # Print message to the Flame message area - only works in Flame 2023.1 and later
        # Warning and error intentionally swapped to match color of message window
        title = title.upper()

        try:
            if self.type == MessageType.INFO or self.type == MessageType.OPERATION_COMPLETE or self.type == MessageType.CONFIRM:
                flame.messages.show_in_console(f'{title}: {message}', 'info', time)
            elif self.type == MessageType.ERROR:
                flame.messages.show_in_console(f'{title}: {message}', 'warning', time)
            elif self.type == MessageType.WARNING:
                flame.messages.show_in_console(f'{title}: {message}', 'error', time)
        except:
            pass

    def cancel(self):
        self.close()
        self.confirmed = False
        #print('--> Cancelled\n')
        pyflame.print('Operation Cancelled', text_color=TextColor.RED)

    def confirm(self):
        self.close()
        self.confirmed = True
        if self.type == MessageType.CONFIRM or self.type == MessageType.WARNING:
            pyflame.print('Operation Confirmed', text_color=TextColor.GREEN)

    def paintEvent(self, event):
        """
        Draw vertical line on left side of window and a horizontal line across
        the top of the window under the title text.
        """

        # Initialize painter
        painter = QtGui.QPainter(self)

        if self.type == MessageType.CONFIRM:
            line_color = LineColor.GRAY.value
            horizontal_line_color = LineColor.GRAY_TRANS.value
        elif self.type == MessageType.INFO or self.type == MessageType.OPERATION_COMPLETE:
            line_color = LineColor.BLUE.value
            horizontal_line_color = LineColor.BLUE_TRANS.value
        elif self.type == MessageType.ERROR:
            line_color = LineColor.YELLOW.value
            horizontal_line_color = LineColor.YELLOW_TRANS.value
        elif self.type == MessageType.WARNING:
            line_color = LineColor.RED.value
            horizontal_line_color = LineColor.RED_TRANS.value

        # Draw 50% transparent horizontal line
        scaled_vertical_pos = pyflame.gui_resize(50)
        painter.setPen(QtGui.QPen(horizontal_line_color, .5, QtCore.Qt.SolidLine))
        painter.drawLine(0, scaled_vertical_pos, self.width, scaled_vertical_pos)

        # Draw fully opaque vertical line on left side
        scaled_bar_width = pyflame.gui_resize(4)
        painter.setPen(QtGui.QPen(line_color, scaled_bar_width, QtCore.Qt.SolidLine))
        painter.drawLine(0, 0, 0, self.height)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.confirm()

class PyFlamePasswordWindow(QtWidgets.QDialog):
    """
    PyFlamePasswordWindow
    =====================

    Custom Qt Flame Password Window.

    This class provides a custom dialog window for entering a password or a username and password.

    Args:
    -----
        `message` (str):
            The message to be displayed in the window.

        `title` (str, optional):
            The title text shown in the top left of the window. If set to None, the default title of either
            'Enter Password' or 'Enter Username and Password' will be used based on `user_name_prompt` argument.
            (Default: `None`)

        `user_name_prompt` (bool):
            If set to True, the window will prompt for both username and password.
            (Default: `False`)

        `font` (str):
            The font to be used in the window.
            (Default: `PYFLAME_FONT`)

        `font_size` (int):
            The font size to be used in the window.
            (Default: `PYFLAME_FONT_SIZE`)

        `parent` (QtWidgets.QWidget, optional):
            The parent window of this dialog.
            (Default: `None`)

    Methods:
    --------
        `password()` -> Optional[Union[str, bool]]:
            Returns the entered password as a string or None if no password was entered.

        `username_password()` -> Tuple[Optional[str], Optional[str]]:
            Returns the entered username and password as a tuple or (None, None) if no username or password was entered.

    Notes:
    ------
        For messages with multiple lines, use triple quotes for message text.

    Examples:
    ---------
        For a password prompt:
        ```
        password_window = PyFlamePasswordWindow(
            message=f'System password needed to install {SCRIPT_NAME}.',
            )

        password = password_window.password()
        ```

        For a username and password prompt:
        ```
        password_window = PyFlamePasswordWindow(
            message='Enter username and password.',
            user_name_prompt=True,
            )

        username, password = password_window.username_password()
        ```
    """

    def __init__(self: 'PyFlamePasswordWindow',
                 message: str,
                 title: Optional[str]=None,
                 user_name_prompt: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 parent: Optional[QtWidgets.QWidget]=None
                 ):
        super().__init__()

        # Validate argument types
        if not isinstance(message, str):
            raise TypeError('PyFlamePasswordWindow: message must be a string')
        elif title is not None and not isinstance(title, str):
            raise TypeError('PyFlamePasswordWindow: title must be a string or None')
        elif not isinstance(user_name_prompt, bool):
            raise TypeError('PyFlamePasswordWindow: user_name_prompt must be a boolean')
        elif not isinstance(font, str):
            raise TypeError('PyFlamePasswordWindow: font must be a string')
        elif not isinstance(font_size, int) or font_size <= 0:
            raise TypeError('PyFlamePasswordWindow: font_size must be a positive integer')

        # Set window title if set to None
        if not title and user_name_prompt:
            title = 'Enter Username and Password'
        elif not title and not user_name_prompt:
            title = 'Enter Password'
        else:
            title = title

        self.user_name_prompt = user_name_prompt
        self.username_value = ''
        self.password_value = ''

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Set Window size for screen
        self.width = pyflame.gui_resize(500)
        self.height = pyflame.gui_resize(300)

        # Build password window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet(f"""
            background-color: rgb(36, 36, 36);
        """)

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        resolution = main_window_res.screenGeometry()

        # Center window on screen
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.setParent(parent)

        # Title Label
        self.title_label = PyFlameLabel(
            text=title,
            width=self.width,
            font_size=24,
            )

        # Message Text
        self.message_text = QtWidgets.QTextEdit()
        self.message_text.setPlainText(message)
        self.message_text.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.message_text.setDisabled(True)
        self.message_text.setFont(font)
        self.message_text.setStyleSheet(f"""
            QTextEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                selection-color: rgb(190, 190, 190);
                selection-background-color: rgb(36, 36, 36);
                border: none;
                padding-left: {pyflame.gui_resize(10)}px;
                padding-right: {pyflame.gui_resize(10)}px;
                }}
            """)

        self.password_label = PyFlameLabel(
            text='Password',
            width=80,
            )
        self.password_entry = PyFlameEntry(
            text='',
            )
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_entry.returnPressed.connect(self._set_password)

        if user_name_prompt:
            self.username_label = PyFlameLabel(
                text='Username',
                width=80,
                )
            self.username_entry = PyFlameEntry(
                text='',
                )
            self.username_entry.returnPressed.connect(self._set_username_password)
            self.confirm_button = PyFlameButton(
                text='Confirm',
                connect=self._set_username_password,
                width=110,
                color=Color.BLUE,
                )
        else:
            self.confirm_button = PyFlameButton(
                text='Confirm',
                connect=self._set_password,
                width=110,
                color=Color.BLUE,
                )

        self.cancel_button = PyFlameButton(
            text='Cancel',
            connect=self._cancel,
            width=110,
            )

        # UI Widget Layout
        self.grid = QtWidgets.QGridLayout()
        self.grid.setColumnMinimumWidth(1, pyflame.gui_resize(150))
        self.grid.setColumnMinimumWidth(2, pyflame.gui_resize(150))
        self.grid.setColumnMinimumWidth(3, pyflame.gui_resize(150))

        self.grid.addWidget(self.title_label, 0, 0)
        self.grid.setRowMinimumHeight(1, pyflame.gui_resize(10))
        self.grid.addWidget(self.message_text, 2, 0, 1, 4)

        if user_name_prompt:
            self.grid.addWidget(self.username_label, 4, 0)
            self.grid.addWidget(self.username_entry, 4, 1, 1, 3)
            self.grid.addWidget(self.password_label, 5, 0)
            self.grid.addWidget(self.password_entry, 5, 1, 1, 3)
            self.grid.setRowMinimumHeight(6, pyflame.gui_resize(45))
        else:
            self.grid.addWidget(self.password_label, 4, 0)
            self.grid.addWidget(self.password_entry, 4, 1, 1, 3)
            self.grid.setRowMinimumHeight(5, pyflame.gui_resize(45))

        self.grid.setRowMinimumHeight(7, pyflame.gui_resize(20))
        self.grid.addWidget(self.cancel_button, 8, 2)
        self.grid.addWidget(self.confirm_button, 8, 3)

        self.password_value = ''
        self.username_value = ''

        print(f'\n--> {title}: {message}\n')

        self.setLayout(self.grid)
        self.show()

        # Set entry focus
        if user_name_prompt:
            self.username_entry.setFocus()
        else:
            self.password_entry.setFocus()

        self.exec_()

    def _cancel(self):
        """
        Close window and return False when cancel button is pressed.
        """

        self.close()
        print('--> Cancelled.\n')
        return False

    def _set_username_password(self):

        if self.password_entry.text() and self.username_entry.text():
            self.close()
            self.username_value = self.username_entry.text()
            self.password_value = self.password_entry.text()
            return

    def _set_password(self):

        password = self.password_entry.text()

        if password:
            command = ['sudo', '-S', 'echo', 'Testing sudo password']
            try:
                # Run the command with sudo and pass the password through stdin
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, error = process.communicate(input=password+'\n')

                if process.returncode == 0:
                    print('Sudo password is correct.\n')
                    self.password_value = self.password_entry.text()
                    self.close()
                    return
                else:
                    print('Sudo password is incorrect.')
                    self.message_text.setText('Password incorrect, try again.')
            except Exception as e:
                print('Error occurred while testing sudo password:', str(e))

    def password(self) -> Optional[str]:
        """
        Password
        ========

        Returns the entered password as a string or None if no password was entered.

        Returns:
        --------
            password (str): The entered password as a string.

        Examples:
        ---------
            To get the entered password:
            ```
            password = password_window.password()
            ```
        """

        if self.password_value:
            return self.password_value
        return None

    def username_password(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Username Password
        =================

        Returns the entered username and password as a tuple or (None, None) if no username or password was entered.

        Returns:
        --------
            Tuple[Optional[str], Optional[str]]: Username and password as a tuple.

        Examples:
        ---------
            To get the entered username and password:
            ```
            username, password = password_window.username_password()
            ```
        """

        if self.username_value and self.password_value:
            return self.username_value, self.password_value
        return None, None

    def paintEvent(self, event):
        """
        Draw vertical red line on left side of window and a horizontal line across
        the top of the window under the title text.
        """

        # Initialize painter
        painter = QtGui.QPainter(self)

        # Draw 50% transparent horizontal line
        scaled_vertical_pos = pyflame.gui_resize(50)
        painter.setPen(QtGui.QPen(LineColor.RED_TRANS.value, .5, QtCore.Qt.SolidLine))
        painter.drawLine(0, scaled_vertical_pos, self.width, scaled_vertical_pos)

        # Draw fully opaque vertical line on left side
        scaled_line_width = pyflame.gui_resize(4)
        painter.setPen(QtGui.QPen(LineColor.RED.value, scaled_line_width, QtCore.Qt.SolidLine))
        painter.drawLine(0, 0, 0, self.height)

    def mousePressEvent(self, event):

        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):

        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

class PyFlameProgressWindow(QtWidgets.QDialog):
    """
    PyFlameProgressWindow
    =====================

    Custom QT Flame Progress Window

    Args:
    -----
        `num_to_do` (int):
            Total number of operations to do.

        `title` (str, optional):
            text shown in top left of window ie. Rendering...
            (Default: `None`)

        `text` (str, optional): message to show in window.
            (Default: `None`)

        `line_color` (WindowBarColor):
            Color of bar on left side of window.
            (Default: `LineColor.BLUE`)

        `enable_done_button` (bool):
            Enable/Disable done button,
            (Default: `False`)

        `font` (str): Font to be used in window.
            (Default: `PYFLAME_FONT`)

        `font_size` (int): Size of font.
            (Default: `PYFLAME_FONT_SIZE`)

    LineColor Options:
    ------------------
    - `LineColor.GRAY`: For gray line.
    - `LineColor.BLUE`: For blue line.
    - `LineColor.RED`: For red line.
    - `LineColor.GREEN`: For green line.
    - `LineColor.YELLOW`: For yellow line.
    - `LineColor.TEAL`: For teal line.

    Methods:
    --------
        `set_progress_value(int)`:
            Set progress bar value.

        `enable_done_button(bool)`:
            Enable or disable done button.

        `set_text(str)`:
            Set text in window.

    Notes:
    ------
        For text with multiple lines, use triple quotes.

    Examples:
    ---------
        To create progress bar window:
        ```
        self.progress_window = PyFlameProgressWindow(
            num_to_do=10,
            title='Rendering...',
            text='Rendering: Batch 1 of 5',
            enable_done_button=True,
            )
        ```

        To update progress bar progress value:
        ```
        self.progress_window.set_progress_value(5)
        ```

        To update text in window:
        ```
        self.progress_window.set_text('Rendering: Batch 2 of 5')
        ```

        To enable or disable done button - True or False:
        ```
        self.progress_window.enable_done_button(True)
        ```
    """

    def __init__(self: 'PyFlameProgressWindow',
                 num_to_do: int,
                 title: Optional[str]=None,
                 text: Optional[str]=None,
                 line_color: LineColor=LineColor.BLUE,
                 enable_done_button: bool=False,
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 parent=None
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(num_to_do, int):
            raise TypeError('PyFlameProgressWindow: num_to_do must be an integer')
        if title is not None and not isinstance(title, str):
            raise TypeError('PyFlameProgressWindow: title must be a string or None')
        elif text is not None and not isinstance(text, str):
            raise TypeError('PyFlameProgressWindow: text must be a string or None')
        elif not isinstance(line_color, LineColor):
            raise ValueError('PyFlameProgressWindow: color must be an instance of LineColor Enum. '
                             'Options are: LineColor.GRAY, LineColor.BLUE, LineColor.RED, '
                             'LineColor.GREEN, LineColor.YELLOW, LineColor.TEAL.')
        elif not isinstance(enable_done_button, bool):
            raise TypeError('PyFlameProgressWindow: enable_done_button must be True or False')
        elif not isinstance(font, str):
            raise TypeError('PyFlameProgressWindow: font must be a string')
        elif not isinstance(font_size, int):
            raise TypeError('PyFlameProgressWindow: font_size must be an integer')

        self.line_color = line_color
        self.num_to_do = num_to_do

        if not title:
            title = 'Task Progress'

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Set Window size for screen
        self.window_width = pyflame.gui_resize(500)
        self.window_height = pyflame.gui_resize(330)

        # Build window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(QtCore.QSize(self.window_width, self.window_height))
        self.setMaximumSize(QtCore.QSize(self.window_width, self.window_height))
        self.setStyleSheet(f"""
            background-color: rgb(36, 36, 36)
            """)

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        resolution = main_window_res.screenGeometry()

        # Center window on screen
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.setParent(parent)

        self.grid = QtWidgets.QGridLayout()

        self.title_label = PyFlameLabel(
            text=title,
            font_size=24,
            )

        self.message_text = QtWidgets.QTextEdit()
        self.message_text.setDisabled(True)
        self.message_text.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.message_text.setDisabled(True)
        self.message_text.setFont(font)
        self.message_text.setStyleSheet(f"""
            QTextEdit{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                selection-color: rgb(190, 190, 190);
                selection-background-color: rgb(36, 36, 36);
                border: none;
                padding-left: {pyflame.gui_resize(10)}px;
                padding-right: {pyflame.gui_resize(10)}px;
                }}
            """)
        self.message_text.setPlainText(text)

        # Progress bar
        bar_max_height = pyflame.gui_resize(5)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximum(num_to_do)
        self.progress_bar.setMaximumHeight(bar_max_height)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar{{
                color: {Color.TEXT.value};
                background-color: rgb(45, 45, 45);
                border: none;
                }}
            QProgressBar:chunk{{
                background-color: {Color.BLUE.value};
                }}
            """)

        self.done_button = PyFlameButton(
            text='Done',
            connect=self.close,
            width=110,
            color=Color.BLUE,
            )
        self.done_button.setEnabled(enable_done_button)

        # Layout
        row_height = pyflame.gui_resize(30)

        self.grid.addWidget(self.title_label, 0, 0)
        self.grid.setRowMinimumHeight(1, row_height)
        self.grid.addWidget(self.message_text, 2, 0, 1, 4)
        self.grid.addWidget(self.progress_bar, 8, 0, 1, 7)
        self.grid.setRowMinimumHeight(9, row_height)
        self.grid.addWidget(self.done_button, 10, 6)
        self.grid.setRowMinimumHeight(11, row_height)

        print(
            f'{TextColor.GREEN.value}' + # Set text color
            '=' * 80 + '\n' +
            f'{title}' + '\n' +
            '=' * 80 + '\n' +
            f'{TextColor.RESET.value}'  # Reset text color
            )

        self.setLayout(self.grid)
        self.show()

    def set_text(self, text) -> None:
        """
        Set Text
        ========

        Use to set the text of the message text edit widget to the specified text.

        Args:
        -----
            `text` (str):
                The text to set in the message text edit widget.

        Raises:
        -------
            TypeError:
                If `text` is not a string.

        Example:
        ---------
            To set the text in the progress window:
            ```
            self.progress_window.set_text('Rendering: Batch 2 of 5')
            ```
        """

        # Validate argument type
        if not isinstance(text, str):
            raise TypeError('PyFlameProgressWindow: set_text must be a string')

        # Set progress window text
        self.message_text.setText(text)

    def set_progress_value(self, value) -> None:
        """
        Set Progress Value
        ==================

        Use to set the progress value of the progress bar.

        Args:
        -----
            `value` (int):
                The value to set the progress bar to.

        Raises:
        -------
            TypeError:
                If `value` is not an integer.

        Examples:
        ---------
            To set the progress bar to 5:
            ```
            self.progress_window.set_progress_value(5)
            ```
        """

        # Validate argument type
        if not isinstance(value, int):
            raise TypeError('PyFlameProgressWindow: set_progress_value must be an integer')

        # Set progress bar value
        self.progress_bar.setValue(value)
        QtWidgets.QApplication.processEvents()

        # Enable Done button if progress bar value equals num_to_do(completed)
        if value == self.num_to_do:
            self.done_button.setEnabled(True)

    def enable_done_button(self, value) -> None:
        """
        Enable Done Button
        ==================

        Use to enable or disable the done button.

        Args:
        -----
            `value` (bool):
                True to enable done button, False to disable done button.

        Raises:
        -------
            TypeError:
                If `value` is not a boolean.

        Examples:
        ---------
            To enable done button:
            ```
            self.progress_window.enable_done_button(True)
            ```
        """

        # Validate argument type
        if not isinstance(value, bool):
            raise TypeError('PyFlameProgressWindow: enable_done_button must be True or False')

        # Enable or disable done button
        if value:
            self.done_button.setEnabled(True)
        else:
            self.done_button.setEnabled(False)

    def showEvent(self, event):
        """
        If the window has a parent, center the window on the screen.
        """

        parent = self.parent()
        if parent:
            # Center the window on the screen
            screen_geometry =  QtWidgets.QDesktopWidget().screenGeometry()
            x = (screen_geometry.width() - self.width()) / 2
            y = (screen_geometry.height() - self.height()) / 2
            x = x/2
            y = y/2

            self.move(x, y)

            super().showEvent(event)

    def paintEvent(self, event):

        # Set line color
        if self.line_color == LineColor.GRAY:
            line_color = LineColor.GRAY.value
            horizontal_line_color = LineColor.GRAY_TRANS.value
        elif self.line_color == LineColor.BLUE:
            line_color = LineColor.BLUE.value
            horizontal_line_color = LineColor.BLUE_TRANS.value
        elif self.line_color == LineColor.RED:
            line_color = LineColor.RED.value
            horizontal_line_color = LineColor.RED_TRANS.value
        elif self.line_color == LineColor.GREEN:
            line_color = LineColor.GREEN.value
            horizontal_line_color = LineColor.GREEN_TRANS.value
        elif self.line_color == LineColor.YELLOW:
            line_color = LineColor.YELLOW.value
            horizontal_line_color = LineColor.YELLOW_TRANS.value
        elif self.line_color == LineColor.TEAL:
            line_color = LineColor.TEAL.value
            horizontal_line_color = LineColor.TEAL_TRANS.value

        # Initialize painter
        painter = QtGui.QPainter(self)

        # Draw 50% transparent horizontal line below text
        scaled_line_height = pyflame.gui_resize(50)
        painter.setPen(QtGui.QPen(horizontal_line_color, .5, QtCore.Qt.SolidLine))
        painter.drawLine(0, scaled_line_height, self.window_width, scaled_line_height)

        # Draw fully opaque vertical line on left side
        scaled_line_width = pyflame.gui_resize(4)
        painter.setPen(QtGui.QPen(line_color, scaled_line_width, QtCore.Qt.SolidLine))
        painter.drawLine(0, 0, 0, self.window_height)

    def mousePressEvent(self, event):

        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):

        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.close()

class _OverlayWidget(QtWidgets.QWidget):
    """
    Overlay Widget
    ==============

    This is a private class, should not be used outside this module.

    This class is used to help add the vertical and horizontal colored lines to the
    PyFlameDialogWindow and PyFlameMessageWindow windows. It draws a blue vertical line
    along the left edge of the parent widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPalette(QtGui.QPalette(QtCore.Qt.transparent))
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 110, 175), pyflame.gui_resize(2)))
        painter.drawLine(0, 0, 0, 1000)

class PyFlameDialogWindow(QtWidgets.QDialog):
    """
    PyFlameDialogWindow
    ===================

    Custom QT Flame Dialog Window Widget

    Args:
    -----
        `title` (str):
            Text displayed in top left corner of window.
            (Default: `Python Script`)

        `width` (int, optional):
            Set minimum width of window.
            (Default: `150`)

        `height` (int, optional):
            Set minimum height of window.
            (Default: `30`)

        `line_color` (LineColor): Color of bar on left side of window.
            (Default: `LineColor.BLUE`)

        `return_pressed` (callable, optional):
            Function to be called when return key is pressed.
            (Default: `None`)

        `tab_width` (int):
            Set width of window tab labels.

        `tab_height` (int):
            Set height of of window tab labels.

        `grid_layout` (bool):
            Add grid layout to window.
            (Default: `True`)

        `grid_columns` (int):
            Number of columns in grid layout. Only used if `grid_layout` is `True`.
            (Default: `4`)

        `grid_rows` (int):
            Number of rows in grid layout. Only used if `grid_layout` is `True`.
            (Default: `3`)

        `font` (str): Font to be used in window.
            (Default: `PYFLAME_FONT`)

        `font_size` (int): Size of font.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `add_layout(layout)`:
            Add layout to window.

    Notes:
    ------

    LineColor Options:
    `LineColor.GRAY`: For gray line.
    `LineColor.BLUE`: For blue line.
    `LineColor.RED`: For red line.
    `LineColor.GREEN`: For green line.
    `LineColor.YELLOW`: For yellow line.
    `LineColor.TEAL`: For teal line.

    Example:
    --------
        To create a window:
        ```
        window = PyFlameDialogWindow(
            title=f'{SCRIPT_NAME} <small>{SCRIPT_VERSION},
            return_pressed=confirm,
            )
        ```

        To add a layout to the window:
        ```
        window.add_layout(layout)
        ```
    """

    def __init__(self: 'PyFlameDialogWindow',
                 title: str='Python Script',
                 width: Optional[int]=None,
                 height: Optional[int]=None,
                 line_color: LineColor=LineColor.BLUE,
                 return_pressed: Optional[Callable]=None,
                 tab_width: int=150,
                 tab_height: int=24,
                 grid_layout: bool=True,
                 grid_layout_columns: int=4,
                 grid_layout_rows: int=3,
                 grid_layout_column_width: int=150,
                 grid_layout_row_height: int=28,
                 grid_layout_adjust_column_widths: Optional[dict[int, int]]={},
                 grid_layout_adjust_row_heights: Optional[dict[int, int]]={},
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(title, str):
            raise TypeError(f"PyFlameDialogWindow: Expected 'title' to be a string, got {type(title).__name__} instead.")
        if width is not None and not isinstance(width, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'width' to be None or an int, got {type(width).__name__} instead.")
        if height is not None and not isinstance(height, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'height' to be None or an int, got {type(height).__name__} instead.")
        if not isinstance(line_color, LineColor):
            raise TypeError(f"PyFlameDialogWindow: Expected 'line_color' to be a LineColor Enum, got {type(line_color).__name__} instead. "
                             "LineColor options are: LineColor.GRAY, LineColor.BLUE, LineColor.RED, LineColor.GREEN, "
                             "LineColor.YELLOW, LineColor.TEAL.")
        if return_pressed is not None and not callable(return_pressed):
            raise TypeError(f"PyFlameDialogWindow: Expected 'return_pressed' to be a callable function, got {type(return_pressed).__name__} instead.")
        if not isinstance(tab_width, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'tab_width' to be an int, got {type(tab_width).__name__} instead.")
        if not isinstance(tab_height, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'tab_height' to be an int, got {type(tab_height).__name__} instead.")
        if not isinstance(grid_layout, bool):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout' to be a bool, got {type(grid_layout).__name__} instead.")
        if not isinstance(grid_layout_columns, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_columns' to be an int, got {type(grid_layout_columns).__name__} instead.")
        if not isinstance(grid_layout_rows, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_rows' to be an int, got {type(grid_layout_rows).__name__} instead.")
        if not isinstance(grid_layout_column_width, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_column_width' to be an int, got {type(grid_layout_column_width).__name__} instead.")
        if not isinstance(grid_layout_row_height, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_row_height' to be an int, got {type(grid_layout_row_height).__name__} instead.")
        if not isinstance(grid_layout_adjust_column_widths, dict):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_adjust_column_widths' to be a dict, got {type(grid_layout_adjust_column_widths).__name__} instead.")
        if not isinstance(grid_layout_adjust_row_heights, dict):
            raise TypeError(f"PyFlameDialogWindow: Expected 'grid_layout_adjust_row_heights' to be a dict, got {type(grid_layout_adjust_row_heights).__name__} instead.")
        if not isinstance(font, str):
            raise TypeError(f"PyFlameDialogWindow: Expected 'font' to be a string, got {type(font).__name__} instead.")
        if not isinstance(font_size, int):
            raise TypeError(f"PyFlameDialogWindow: Expected 'font_size' to be an int, got {type(font_size).__name__} instead.")

        self.line_color = line_color
        self.return_pressed = return_pressed
        self.font_size = pyflame.font_resize(font_size)
        self.tab_width = pyflame.gui_resize(tab_width)
        self.tab_height = pyflame.gui_resize(tab_height)

        # Set window size
        # self.width = pyflame.gui_resize(width)
        # self.height = pyflame.gui_resize(height)
        # self.setMinimumSize(QtCore.QSize(self.width, self.height))

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        resolution = main_window_res.screenGeometry()

        # Center window on screen
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        # Set font
        font = QtGui.QFont(font)
        font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(font)

        # Window title label
        title_label = PyFlameLabel(
            text='<span style="white-space: pre;">  ' + title, # Add space to title using CSS code. This pushes the title to the right one space.
            style=Style.UNDERLINE,
            align=Align.LEFT,
            max_width=True,
            underline_color='rgba(0, 43, 66, 0.5)',
            height=40,
            font_size=24,
            )

        # Window layout
        # -------------
        title_text_hbox = PyFlameHBoxLayout()
        title_text_hbox.addWidget(title_label)
        title_text_hbox.setContentsMargins(0, 0, 0, 0)  # Remove margins around the title label

        # Center layout - where main UI is added
        self.center_layout = PyFlameGridLayout()
        # Create widget to hold the center layout
        center_widget = QtWidgets.QWidget()
        center_widget.setLayout(self.center_layout)

        # Add the center layout to the main layout
        main_vbox2 = PyFlameVBoxLayout()
        main_vbox2.addWidget(center_widget, alignment=QtCore.Qt.AlignCenter)
        main_vbox2.addStretch()
        main_vbox2.setContentsMargins(15, 15, 15, 15) # Add margin around main UI

        main_vbox3 = PyFlameVBoxLayout()
        main_vbox3.addLayout(title_text_hbox)
        main_vbox3.addLayout(main_vbox2)
        main_vbox3.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.setLayout(main_vbox3)

        self._set_stylesheet(font)

        # Initialize and set up the overlay for blue line on left edge of window
        self.overlay = _OverlayWidget(self)

        # Create default grid layout if grid_layout is True
        if grid_layout:
            self.grid_layout = PyFlameGridLayout(
                columns=grid_layout_columns,
                rows=grid_layout_rows,
                column_width=grid_layout_column_width,
                row_height=grid_layout_row_height,
                adjust_column_widths=grid_layout_adjust_column_widths,
                adjust_row_heights=grid_layout_adjust_row_heights,
                )

            self.add_layout(self.grid_layout)
            self.show()

    def add_layout(self, layout):
        """
        Add Layout
        ==========

        Add widget layout to the main window.

        Args:
        -----
            layout (PyFlameLayout):
                Main widget layout to add to Main Window.
        """

        self.center_layout.addLayout(layout, 0, 0)

    def _set_stylesheet(self, font):

        # Window stylesheet
        self.setStyleSheet(f"""
            QWidget{{
                background-color: rgb(36, 36, 36);
                }}
            QTabWidget{{
                background-color: rgb(36, 36, 36);
                border: none;
                }}
            QTabWidget::tab-bar{{
                alignment: center;
                }}
            QTabBar::tab{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                width: {self.tab_width}px;
                height: {self.tab_height}px;
                padding: {pyflame.gui_resize(5)}px;
                }}
            QTabBar::tab:selected{{
                color: rgb(200, 200, 200);
                background-color: rgb(31, 31, 31);
                border: 1px solid rgb(31, 31, 31);
                border-bottom: 1px solid {Color.BLUE.value};
                }}
            QTabBar::tab:!selected{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                border: none;
                }}
            QTabWidget::pane{{
                border-top: 1px solid {Color.TAB_PANE.value};
                }}
            """)

    def mousePressEvent(self, event):

        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):

        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and self.return_pressed is not None:
            self.return_pressed()

    def resizeEvent(self, event):

        # Ensure the left blue line overlay covers the whole window when resizing
        self.overlay.setGeometry(0, 0, 100, 3000)
        super().resizeEvent(event)

class PyFlameWindow(QtWidgets.QWidget):
    """
    PyFlameWindow
    =============

    Custom QT Flame Window Widget

    Creates a custom QT window with a colored bar on the left side of the window.

    By default, the window will have a grid layout with 4 columns and 2 rows.
    This can be overridden by setting the `grid_columns` and `grid_rows` arguments.
    If `grid_layout` is set to `False`, the window will not have a grid layout and a layout
    will need to be added in the main script.

    Args:
    -----
        `title (str)`:
            Text displayed in top left corner of window.
            (Default: `Python Script`)

        `width (int)`: Set minimum width of window.
            (Default: `150`)

        `height (int)`: Set minimum height of window.
            (Default: `30`)

        `line_color (LineColor)`: Color of bar on left side of window.
            (Default: `LineColor.BLUE`)

        LineColor Options:
        - `LineColor.GRAY`: For gray line.
        - `LineColor.BLUE`: For blue line.
        - `LineColor.RED`: For red line.
        - `LineColor.GREEN`: For green line.
        - `LineColor.YELLOW`: For yellow line.
        - `LineColor.TEAL`: For teal line.

        `return_pressed (callable, optional)`: Function to be called when return key is pressed.
            (Default: `None`)

        `tab_width` (int):
            Set width of window tab labels.

        `tab_height` (int):
            Set height of of window tab labels.

        `grid_layout` (bool):
            Add grid layout to window.
            (Default: `True`)

        `grid_columns` (int):
            Number of columns in grid layout. Only used if `grid_layout` is `True`.
            (Default: `4`)

        `grid_rows` (int):
            Number of rows in grid layout. Only used if `grid_layout` is `True`.
            (Default: `3`)

        `font (str)`: Font to be used in window.
            (Default: `PYFLAME_FONT`)

        `font_size (int)`: Size of font.
            (Default: `PYFLAME_FONT_SIZE`)

    Methods:
    --------
        `add_layout(layout)`:
            Add layout to window.

    Notes:
    ------
        - For proper sizing of widgets and placement of widgets in the window,
        be sure to set the correct number of columns and rows in the grid layout
        when using the default grid layout.

    Example:
    --------
        To create a window using the default grid layout:
        ```
        window = PyFlameWindow(
            title=f'{SCRIPT_NAME} <small>{SCRIPT_VERSION},
            return_pressed=confirm,
            grid_columns=6,
            grid_rows=5,
            )

        window.addWidget(some_widget1, row=0, column=0, row_span=1, column_span=1)
        window.addWidget(some_widget2, row=0, column=0, row_span=1, column_span=1)
        window.addWidget(some_widget3, row=0, column=0, row_span=1, column_span=1)
        ```

        To create a window not using the default grid layout:
        ```
        window = PyFlameWindow(
            title=f'{SCRIPT_NAME} <small>{SCRIPT_VERSION},
            return_pressed=confirm,
            grid_layout=False,
            )

        create some widgets here...

        layout = PyFlameVBoxLayout()

        layout.addWidget(some_widget1, row=0, column=0, row_span=1, column_span=1)
        layout.addWidget(some_widget2, row=0, column=0, row_span=1, column_span=1)
        layout.addWidget(some_widget3, row=0, column=0, row_span=1, column_span=1)

        window.add_layout(layout)

        window.show()
        ```
    """

    def __init__(self: 'PyFlameWindow',
                 title: str='Python Script',
                 width: int=150,
                 height: int=30,
                 line_color: LineColor=LineColor.BLUE,
                 return_pressed: Optional[Callable]=None,
                 tab_width: int=150,
                 tab_height: int=24,
                 grid_layout: bool=True,
                 grid_layout_columns: int=4,
                 grid_layout_rows: int=3,
                 grid_layout_column_width: int=150,
                 grid_layout_row_height: int=28,
                 grid_layout_adjust_column_widths: Optional[dict[int, int]]={},
                 grid_layout_adjust_row_heights: Optional[dict[int, int]]={},
                 font: str=PYFLAME_FONT,
                 font_size: int=PYFLAME_FONT_SIZE,
                 ) -> None:
        super().__init__()

        # Validate argument types
        if not isinstance(title, str):
            raise TypeError(f'PyFlameWindow: Invalid text argument: {title}. Must be of type str.')
        if not isinstance(width, int):
            raise TypeError(f'PyFlameWindow: Invalid width argument: {width}. Must be of type int.')
        if not isinstance(height, int):
            raise TypeError(f'PyFlameWindow: Invalid height argument: {height}. Must be of type int.')
        # If width is set, height must also be set
        if width and not height:
            raise ValueError('PyFlameWindow: height must be set if width is set.')
        # If height is set, width must also be set
        if height and not width:
            raise ValueError('PyFlameWindow: width must be set if height is set.')
        if not isinstance(line_color, LineColor):
            raise ValueError(f'PyFlameWindow: Invalid text argument: {line_color}. Must be of type LineColor Enum. '
                             'Options are: LineColor.GRAY, LineColor.BLUE, LineColor.RED, LineColor.GREEN, '
                             'LineColor.YELLOW, LineColor.TEAL.')
        if return_pressed is not None and not callable(return_pressed):
            raise TypeError(f'PyFlameWindow: Invalid text argument: {return_pressed}. Must be a callable function or None.')
        if not isinstance(tab_width, int):
            raise TypeError(f"PyFlameWindow: Expected 'tab_width' to be an int, got {type(tab_width).__name__} instead.")
        if not isinstance(tab_height, int):
            raise TypeError(f"PyFlameWindow: Expected 'tab_height' to be an int, got {type(tab_height).__name__} instead.")
        if not isinstance(grid_layout, bool):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout' to be a bool, got {type(grid_layout).__name__} instead.")
        if not isinstance(grid_layout_columns, int):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_columns' to be an int, got {type(grid_layout_columns).__name__} instead.")
        if not isinstance(grid_layout_rows, int):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_rows' to be an int, got {type(grid_layout_rows).__name__} instead.")
        if not isinstance(grid_layout_column_width, int):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_column_width' to be an int, got {type(grid_layout_column_width).__name__} instead.")
        if not isinstance(grid_layout_row_height, int):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_row_height' to be an int, got {type(grid_layout_row_height).__name__} instead.")
        if not isinstance(grid_layout_adjust_column_widths, dict):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_adjust_column_widths' to be a dict, got {type(grid_layout_adjust_column_widths).__name__} instead.")
        if not isinstance(grid_layout_adjust_row_heights, dict):
            raise TypeError(f"PyFlameWindow: Expected 'grid_layout_adjust_row_heights' to be a dict, got {type(grid_layout_adjust_row_heights).__name__} instead.")
        if not isinstance(font, str):
            raise TypeError(f'PyFlameWindow: Invalid text argument: {font}. Must be of type str.')
        if not isinstance(font_size, int):
            raise TypeError(f'PyFlameWindow: Invalid text argument: {font_size}. Must be of type int.')

        self.line_color = line_color
        self.return_pressed = return_pressed
        self.font_size = pyflame.font_resize(font_size)
        self.tab_width = pyflame.gui_resize(tab_width)
        self.tab_height = pyflame.gui_resize(tab_height)

        # Set window size
        # self.width = pyflame.gui_resize(width)
        # self.height = pyflame.gui_resize(height)
        # self.setMinimumSize(QtCore.QSize(self.width, self.height))

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Get current screen resolution
        main_window_res = pyflamewin.main_window()
        resolution = main_window_res.screenGeometry()

        # Center window on screen
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        # Set font
        window_font = QtGui.QFont(font)
        window_font.setPointSize(pyflame.font_resize(font_size))
        self.setFont(window_font)

        # Window title label
        title_label = PyFlameLabel(
            text='<span style="white-space: pre;">  ' + title, # Add space to title using CSS code. This pushes the title to the right one space.
            style=Style.UNDERLINE,
            align=Align.LEFT,
            max_width=True,
            underline_color='rgba(0, 43, 66, 0.5)',
            height=40,
            font_size=24,
            )

        # Window layout
        # -------------
        title_text_hbox = PyFlameHBoxLayout()
        title_text_hbox.addWidget(title_label)
        title_text_hbox.setContentsMargins(0, 0, 0, 0)  # Remove margins around the title label

        # Center layout - where main UI is added
        self.center_layout = PyFlameGridLayout()
        # Create widget to hold the center layout
        center_widget = QtWidgets.QWidget()
        center_widget.setLayout(self.center_layout)

        # Add the center layout to the main layout
        main_vbox2 = PyFlameVBoxLayout()
        main_vbox2.addWidget(center_widget, alignment=QtCore.Qt.AlignCenter)
        main_vbox2.addStretch()
        main_vbox2.setContentsMargins(15, 15, 15, 15) # Add margin around main UI

        main_vbox3 = PyFlameVBoxLayout()
        main_vbox3.addLayout(title_text_hbox)
        main_vbox3.addLayout(main_vbox2)
        main_vbox3.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.setLayout(main_vbox3)

        self._set_stylesheet(font)

        # Initialize and set up the overlay for blue line on left edge of window
        self.overlay = _OverlayWidget(self)

        # Create default grid layout if grid_layout is True
        if grid_layout:
            self.grid_layout = PyFlameGridLayout(
                columns=grid_layout_columns,
                rows=grid_layout_rows,
                column_width=grid_layout_column_width,
                row_height=grid_layout_row_height,
                adjust_column_widths=grid_layout_adjust_column_widths,
                adjust_row_heights=grid_layout_adjust_row_heights,
                )

            self.add_layout(self.grid_layout)
            self.show()

    def add_layout(self, layout):
        """
        Add Layout
        ==========

        Add widget layout to the main window.

        Args:
        -----
            layout (PyFlameLayout):
                Main widget layout to add to Main Window.
        """

        self.center_layout.addLayout(layout, 0, 0)

    def _set_stylesheet(self, font):

        # Window stylesheet
        self.setStyleSheet(f"""
            QWidget{{
                background-color: rgb(36, 36, 36);
                }}
            QTabWidget{{
                background-color: rgb(36, 36, 36);
                border: none;
                }}
            QTabWidget::tab-bar{{
                alignment: center;
                }}
            QTabBar::tab{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                width: {self.tab_width}px;
                height: {self.tab_height}px;
                padding: {pyflame.gui_resize(5)}px;
                font-family: {font};
                font-size: {self.font_size}px;
                }}
            QTabBar::tab:selected{{
                color: rgb(200, 200, 200);
                background-color: rgb(31, 31, 31);
                border: 1px solid rgb(31, 31, 31);
                border-bottom: 1px solid {Color.BLUE.value};
                }}
            QTabBar::tab:!selected{{
                color: {Color.TEXT.value};
                background-color: rgb(36, 36, 36);
                border: none;
                }}
            QTabWidget::pane{{
                border-top: 1px solid {Color.TAB_PANE.value};
                }}
            """)

    def mousePressEvent(self, event):

        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):

        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()
        except:
            pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and self.return_pressed is not None:
            self.return_pressed()

    def resizeEvent(self, event):

        # Ensure the left blue line overlay covers the whole window when resizing
        self.overlay.setGeometry(0, 0, 100, 3000)
        super().resizeEvent(event)
