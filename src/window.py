# window.py
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

from confy.widget_factory import WidgetFactory

@Gtk.Template(resource_path='/win/ohmyiris/Confy/window.ui')
class ConfyWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ConfyWindow'

    collection_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.widget_factory = WidgetFactory()

        self.build_collection_list()
        self.collection_list.connect("row_activated", self.collection_activated)
        self.collection_list.unselect_all()

    def build_collection_list(self):
        for collection in self.get_application().collections:
            widget = self.widget_factory.create_collection_list_item(collection['name'])
            self.collection_list.append(widget)

    def collection_activated(self, lisbox, row):
        item = row.get_child()
        collection_id = item.collection_id
