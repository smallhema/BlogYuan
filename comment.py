#!/usr/bin/dev python
# -*- coding:utf-8 -*-
# __author__ = "guoxing"
# Date:2017/9/16
def comment_tree(coment_list):
    comment_str="<div class='comment'>"
    for row in coment_list:
        tpl="<div class='content'>%s</div>"%(row["content"])
        comment_str+=tpl
        if row["child"]:
            child_str=comment_tree(row["child"])
            comment_str+=child_str
    comment_str+="</div>"
    return comment_str