# widget_factory.py
#
# Copyright 2025 masak
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

class WidgetFactory:
    def __init__(self):
        pass

    def create_collection_list_item(self, name: str):
        """Item for the collection list. A GtkLabel
        Has a .collection_id"""
        item = Gtk.Label.new(name) # will be display name instead
        item.collection_id = name
        return item
