import sublime
import sublime_plugin

import re

try:
  from Expression import expression
  from Statement import statement
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "JoinStatement plugin for installation instructions; to disable this " +
   "message remove this plugin")

class Base(sublime_plugin.TextCommand):
  def _get_info(self, sel, as_arguments):
    nesting = expression.get_nesting(self.view, sel.b)

    if sel.size() > 0:
      container = [sel.begin(), sel.end()]
    else:
      container = (nesting or statement.get_statement(self.view, sel.b))

    if container == None:
      return None

    if as_arguments:
      tokens = statement.get_arguments(self.view, sel.b, container)
    else:
      raw_tokens = statement.get_tokens(self.view, sel.b, container)
      if len(raw_tokens) == 0:
        tokens = raw_tokens
      else:
        tokens = self._get_logical_tokens(raw_tokens)

    if len(tokens) == 0:
      return None

    if not as_arguments and nesting == None:
      start = max(container[0], tokens[0][0])
      end = min(container[1], tokens[len(tokens) - 1][1])
      container = [start, end]

    new_lines = as_arguments or nesting != None
    return container, tokens, new_lines

  def _get_logical_tokens(self, raw_tokens):
    tokens = []
    last = raw_tokens[0]
    for index, token in enumerate(raw_tokens[: -1]):
      next_token = raw_tokens[index + 1]
      region = sublime.Region(token[1], next_token[0])
      delimeter = self.view.substr(region)
      delimeter_start = len(delimeter) - len(delimeter.lstrip())
      scope = self.view.scope_name(token[1] + delimeter_start)

      if 'operator.logical' in scope:
        new_token = [last[0], token[1]]
        tokens.append(new_token)
        last = next_token

    if len(tokens) == 0 or last[1] != tokens[-1][1]:
      tokens.append([last[0], raw_tokens[-1][1]])

    return tokens

class JoinStatement(Base):
  def run(self, edit, as_arguments = True):
    selections = []
    for sel in self.view.sel():
      self._join(edit, sel, as_arguments)

  def _join(self, edit, sel, as_arguments):
    info = self._get_info(sel, as_arguments)
    if info == None:
      return

    container, tokens, new_lines = info

    end = container[1]
    for index, token in enumerate(reversed(tokens)):
      if new_lines or index > 0:
        self._remove_new_lines(edit, token[1], end, index == 0)

      end = token[0]

    if new_lines:
      self._remove_new_lines(edit, container[0] - 1, end, False, True)

  def _remove_new_lines(self, edit, start, end, first = False, last = False):
    region = sublime.Region(start, end)
    delimeter = self.view.substr(region)
    if "\n" not in delimeter:
      return

    delimeter = delimeter.replace("\n", '')
    delimeter = re.sub(r'(\s)\s*', '\\1', delimeter)

    if first:
      delimeter = re.sub(r'^\s*', '', delimeter)

    if last:
      delimeter = re.sub(r'\s*$', '', delimeter)

    self.view.replace(edit, region, delimeter.replace("\n", ''))

class UnjoinStatement(Base):
  def run(self, edit, as_arguments = True):
    selections = []
    for sel in self.view.sel():
      self._unjoin(edit, sel, as_arguments)

  def _unjoin(self, edit, sel, as_arguments):
    info = self._get_info(sel, as_arguments)
    if info == None:
      return

    container, tokens, new_lines = info
    start_line = self.view.substr(self.view.line(container[0]))
    indentation = re.search(r'^\s*', start_line).group(0)

    end = container[1]
    for index, token in enumerate(reversed(tokens)):
      if new_lines or index > 0:
        self._add_new_lines(edit, indentation, token[1], end, index == 0)

      end = token[0]

    if new_lines:
      self._add_new_lines(edit, indentation, container[0] - 1, end, False, True)

  def _add_new_lines(self, edit, indentation, start, end, first = False,
    last = False):
    if first == False:
      is_tab = self.view.settings().get('translate_tabs_to_spaces')
      if is_tab == True:
        indentation += "\t"
      else:
        indentation += ' ' * self.view.settings().get('tab_size')

    region = sublime.Region(start, end)
    delimeter = self.view.substr(region)
    delimeter = re.sub(r'\s*$', "\n" + indentation, delimeter)
    if region.empty():
      self.view.insert(edit, region.b, delimeter)
    else:
      if self.view.substr(region) == delimeter:
        return
      self.view.replace(edit, region, delimeter)