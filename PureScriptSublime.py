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
    current = pathlib.Path(__file__).parent.resolve()
    print("current = %s" % current)

    cmd = ["purty", 
           "format", 
           fname] 
    print("cmd = %s" % " ".join(cmd))
    stdout, stderr = subprocess.Popen(
      [" ".join(cmd)],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,      
      shell=True).communicate()

    #if stderr.strip():
    #  print("GROOVY FORMAT ERROR: %s" % stderr.strip().decode())
    #  print(stdout.decode('UTF-8'))
    #else:

    sublime.status_message("Build finished")

    try:
      r = stdout.decode('UTF-8')

      self.view.replace(edit, region, r)
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

      
  def on_post_save(self, view):
    if check_is_enabled_file(view.file_name()):
      view.run_command('pure_format')


    
