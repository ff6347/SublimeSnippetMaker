import sublime
import sublime_plugin
import os

template = """<snippet>
  <!-- Example: Hello, ${1:this} is a ${2:snippet}. -->
  <!--
    taken from here: http://sublimetext.info/docs/en/extensibility/snippets.html
    $SELECTION   The text that was selected when the snippet was triggered.
    $TM_CURRENT_LINE    Content of the line the cursor was in when the snippet was triggered.
    $TM_CURRENT_WORD    Current word under the cursor when the snippet was triggered.
    $TM_FILENAME    File name of the file being edited including extension.
    $TM_FILEPATH    File path to the file being edited.
    $TM_FULLNAME    User’s user name.
    $TM_LINE_INDEX  Column the snippet is being inserted at, 0 based.
    $TM_LINE_NUMBER Row the snippet is being inserted at, 1 based.
    $TM_SELECTED_TEXT   An alias for $SELECTION.
    $TM_SOFT_TABS   YES if translate_tabs_to_spaces is true, otherwise NO.
    $TM_TAB_SIZE    Spaces per-tab (controlled by the tab_size option).
  -->
  <content><![CDATA[
%s
]]></content>
  <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
  <tabTrigger>%s</tabTrigger>
  <description>%s</description>
  <!-- Optional: Set a scope to limit where the snippet will trigger -->
  <!-- <scope>%s</scope> -->
</snippet>"""


class MakeSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.scope = self.view.scope_name(self.view.sel()[0].begin()).split(' ')[0]
        self.snippet_text = "\n".join([self.view.substr(i) for i in self.view.sel()])
        self.view.window().show_input_panel('Trigger', '', self.set_trigger, None, None)

    def set_trigger(self, trigger):
        self.trigger = trigger
        self.view.window().show_input_panel('Description', '', self.set_description, None, None)

    def set_description(self, description):
        self.description = description
        self.view.window().show_input_panel('File Name', 'Default.sublime-snippet', self.make_snippet, None, None)

    def make_snippet(self, file_name):
        print self.trigger, self.description
        if len(file_name) > 0:
            file_path = os.path.join(sublime.packages_path(), 'User', file_name)

            if os.path.exists(file_path):
                if sublime.ok_cancel_dialog('Override %s?' % file_name) is False:
                    return

            file = open(file_path, "wb")
            snippet_xml = template % (self.snippet_text, self.trigger, self.description, self.scope)
            file.write(snippet_xml)
            file.close()

            self.view.window().open_file(file_path)

        else:
            sublime.error_message('Please specify the snippet name!!')
