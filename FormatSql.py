import sublime, sublime_plugin

import os
import sys
import imp
sys.path.append(os.path.dirname(__file__))
import sqlparse

class FormatSqlCommand(sublime_plugin.TextCommand):
    def format(self, raw_sql):
        try:
            return sqlparse.format(raw_sql, 
                keyword_case = "upper",
                identifier_case = None,
                strip_comments = False,
                indent_tabs = False,
                indent_width = 4,
                reindent = True,
                comma_first = False,
                strip_whitespace = True
                # truncate_strings = <int>
                # reindent_aligned = True/False 
                # wrap_after = <int>
                # right_margin = <int>
                # Docs: https://github.com/andialbrecht/sqlparse/blob/master/sqlparse/formatter.py
            )
        except Exception as e:
            print(e)
            return None

    def replace_region_with_formatted_sql(self, edit, region):
        selected_text = self.view.substr(region)
        foramtted_text = self.format(selected_text)
        self.view.replace(edit, region, foramtted_text)

    def reloadMods(self):
        reload_mods = []
        for mod in sys.modules:
            if (mod.startswith('sqlparse')) and sys.modules[mod] != None:
                reload_mods.append(mod)
        moduleLoadOrder = [
            'sqlparse.exceptions',
            'sqlparse.tokens',
            'sqlparse.compat',
            'sqlparse.cli',
            'sqlparse.utils',
            'sqlparse.sql',
            'sqlparse.keywords',
            'sqlparse.lexer',
            'sqlparse.formatter',
            'sqlparse',
            'sqlparse.filters.right_margin',
            'sqlparse.filters.aligned_indent',
            'sqlparse.filters.reindent',
            'sqlparse.filters.others',
            'sqlparse.filters.tokens',
            'sqlparse.filters',
            'sqlparse.engine.grouping',
            'sqlparse.engine.filter_stack',
            'sqlparse.engine.statement_splitter',
            'sqlparse.filters.output',
            'sqlparse.engine',
        ]
        for mod in moduleLoadOrder:
            imp.reload(sys.modules[mod])

    def run(self, edit):
        self.reloadMods()
        window = self.view.window()
        view = window.active_view()

        for region in self.view.sel():
            if region.empty():
                selection = sublime.Region(0, self.view.size())
                self.replace_region_with_formatted_sql(edit, selection)
                self.view.set_syntax_file("Packages/SQL/SQL.tmLanguage")
            else:
                self.replace_region_with_formatted_sql(edit, region)