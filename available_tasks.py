import sublime, sublime_plugin
import re
import time

# Function for displaying a list of available tasks. Selecting a task from the list highlights it in the docuemtn.


class AvailableTasksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        today_date = time.strftime('%Y-%m-%d')
        self.available_marker = []
        self.markers = []
        self.view.find_all(r'(^\n*(\s*)(.+)(@start|@due|@started)\((20[1-9][0-9]\-[0-1][0-9]\-[0-3][0-9])\))', 0, "$0,$5", self.markers)
        for marker in self.markers:
        
            if time.strptime(marker.split(',')[1], '%Y-%m-%d') <= time.strptime(today_date, '%Y-%m-%d'):
                self.available_marker.append(marker.split(',')[0])

        self.view.window().show_quick_panel(self.available_marker, self.goto_task, sublime.MONOSPACE_FONT)

    def goto_task(self, choice):
        if choice == -1:
            return
        else:
            findmarker = self.available_marker[choice]
            self.view.sel().clear()

            # re.escape escapes a single quote. That breaks the Sublime find function.
            # Need to substitute escaped single quote with just single quote
            findmarker = findmarker.replace("{", "\{").replace("}", "\}").replace("[", "\[").replace("]", "\]").replace("(", "\(").replace(")", "\)").replace("+", "\+")

            pt = self.view.find(findmarker, 0)
            self.view.sel().add(pt)
            self.view.show(pt)
