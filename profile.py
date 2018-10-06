class Profile:

    experience = ""
    technology = []
    projects = {}

    def __init__(self, name, iam, ii, trends, python, cpp, java, js, iot, ml, vr, ar, cc, eh, proficiency, github):
      self.name = name
      self.iam = iam
      self.ii = ii
      self.trends = trends
      self.python = python
      self.cpp = cpp
      self.java = java
      self.js = js
      self.iot = iot
      self.ml = ml
      self.vr = vr
      self.ar = ar
      self.cc = cc
      self.eh = eh
      self.proficiency = proficiency
      self.github = github

    def disp_name(self):
      print(self.name)

    def disp_name(self):
      for tech in technology:
        print(self.technology, " ")

    #def disp_name(self):
    # for key, value in projects
    #  print(self.name)    