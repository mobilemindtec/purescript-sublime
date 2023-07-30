import sublime, sublime_plugin
import subprocess
import os
import json
import pathlib

class PureFormatCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    region = sublime.Region(0, self.view.size())
    content = self.view.substr(region)
    fname = self.view.file_name()
    #current = pathlib.Path(__file__).parent.resolve()

    tmp_file = "/tmp/code.purs"
    with open(tmp_file, 'w') as f:
        f.write(content)

    cmd = ["purty",
           "format",
           tmp_file] 
    print("cmd = %s" % " ".join(cmd))

    sublime.status_message("Pure format starting..")

    stdout, stderr = subprocess.Popen(
      [" ".join(cmd)],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      shell=True).communicate()

    if stderr.strip():
      print("PureScriptFormat ERROR: %s" % stderr.strip().decode())

      r = stderr.decode('UTF-8')
      if 'Error formatting' in r:

        description = r.split("\n")
        if len(description) > 0:
          description = description[1].strip()
        else:
          description = r

        sublime.error_message("Pure format error: %s" % description)

    else:


      try:
        r = stdout.decode('UTF-8')
        self.view.replace(edit, region, r)
        sublime.status_message("Pure format finished")
      except Exception as e:
        print("PureScriptFormat fail: %s" % e)
        print("PureScriptFormat ERROR: %s" % stderr.strip().decode())
        print("PureScriptFormat RESULT: %s" % stdout.decode('UTF-8'))

def check_is_enabled_file(file_name):
  types = ['.purs']

  for t in types:
    if file_name.lower().endswith(t):
      return True
  return False

class PureEventDump(sublime_plugin.EventListener):


  def on_pre_save(self, view):
    if check_is_enabled_file(view.file_name()):
      view.run_command('pure_format')
