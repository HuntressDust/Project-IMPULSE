from __future__ import annotations


class Description:
    def __init__(self, line1: str="", line2:str="", line3:str=""):
        self.line1=line1
        self.line2=line2
        self.line3=line3
        self.text_lines=list([line1,line2,line3])

default_description = Description("placeholder1",
                                  "placeholder2",
                                  "placeholder3")




