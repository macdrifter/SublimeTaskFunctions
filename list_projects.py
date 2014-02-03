import sublime, sublime_plugin
import re

class ListProjectsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.markers = []
        self.view.find_all(r'^\s*(\w+.+:\s*(\@[^\s]+(\(.*?\))?\s*)*$\n?)|^\s*---.{3,5}---+$', 0, "$1", self.markers)
        self.view.window().show_quick_panel(self.markers, self.goto_project, sublime.MONOSPACE_FONT)

    def goto_project(self, choice):
        if choice == -1:
            return
        else:
            findmarker = self.markers[choice]
            self.view.sel().clear()

            # re.escape escapes a single quote. That breaks the Sublime find function.
            # Need to substitute escaped single quote with just single quote
            findmarker = findmarker.replace("{", "\{").replace("}", "\}").replace("[", "\[").replace("]", "\]").replace("(", "\(").replace(")", "\)").replace("+", "\+")

            pt = self.view.find(findmarker, 0)
            self.view.sel().add(pt)
            self.view.show(pt)
