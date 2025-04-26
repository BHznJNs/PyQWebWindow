from dataclasses import dataclass
from typing import Callable
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QMenu

class QContextMenu:
    @dataclass
    class _MenuAction:
        action_text: str
        action_callback: Callable
    
    @dataclass
    class _MenuSection:
        section_text: str

    class _MenuSeparator: pass

    def __init__(self):
        self._menu_items: list[ContextMenuItem] = []
    
    def _factory(self, parent: QWidget) -> QMenu:
        menu = QMenu(parent)
        for menu_item in self._menu_items:
            match menu_item:
                case QContextMenu():
                    menu.addMenu(menu_item._factory(menu))
                case QContextMenu._MenuAction(action_text, action_callback):
                    action = menu.addAction(action_text)
                    action.triggered.connect(action_callback)
                case QContextMenu._MenuSection(section_text):
                    menu.addSection(section_text)
                case QContextMenu._MenuSeparator():
                    menu.addSeparator()
        return menu

    def _show(self, parent: QWidget, pos: QPoint):
        menu = self._factory(parent)
        menu.exec_(menu.mapToGlobal(pos))

    def add_action(self, action_text: str, action_callback: Callable):
        self._menu_items.append(QContextMenu._MenuAction(action_text, action_callback))

    def add_actions(self, actions: list[tuple[str, Callable]]):
        self._menu_items.extend([
            QContextMenu._MenuAction(action_text, action_callback)
            for action_text, action_callback in actions
        ])

    def add_submenu(self, submenu: "QContextMenu"):
        self._menu_items.append(submenu)
    
    def add_section(self, section_text: str):
        self._menu_items.append(QContextMenu._MenuSection(section_text))
    
    def add_separator(self):
        self._menu_items.append(QContextMenu._MenuSeparator())

ContextMenuItem = QContextMenu\
    | QContextMenu._MenuAction\
    | QContextMenu._MenuSection\
    | QContextMenu._MenuSeparator
