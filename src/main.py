# main.py
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

import os
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import ConfyWindow

import yaml


class ConfyApplication(Adw.Application):
    """The main application singleton class."""

    collections = []

    def __init__(self):
        super().__init__(application_id='win.ohmyiris.Confy',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/win/ohmyiris/Confy')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self.search_collections()

    def search_collections(self):
        collections_folder = Gio.File.new_for_path("/app/share/collections")
        cancellable = Gio.Cancellable()
        collections_files = collections_folder.enumerate_children("standard::name,standard::content-type", Gio.FileQueryInfoFlags.NONE, cancellable)

        file_info = collections_files.next_file()
        while file_info:
            content_type = file_info.get_content_type()
            if content_type == "application/yaml" or content_type == ".yaml" or content_type == ".yml": # extensions are for windows
                name = file_info.get_name()
                file = collections_folder.get_child(name)
                input_stream = file.read(cancellable)

                bytes = input_stream.read_bytes(4096, cancellable)
                yaml_data = bytes.get_data().decode()

                data = yaml.safe_load(yaml_data)
                self.collections.extend(data)

            # Cycle to the next file
            file_info = collections_files.next_file()


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = ConfyWindow(application=self)
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='confy',
                                application_icon='win.ohmyiris.Confy',
                                developer_name='masak',
                                version='0.1.0',
                                developers=['masak'],
                                copyright='© 2025 masak')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = ConfyApplication()
    return app.run(sys.argv)

