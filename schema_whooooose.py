# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json
import xlrd
import xlwt

schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                content=TEXT(stored=True, analyzer=ChineseAnalyzer())
                )
def getAllDataAsDict(name, n=0, end_colx=None, nrows=None):
    book = xlrd.open_workbook(name)
    table = book.sheets()[0]
    db = []
    header = table.row_values(n, start_colx=0, end_colx=end_colx)
    if nrows == None:
        nrows = table.nrows
    for i in range(2, nrows):
        db.append(dict(zip(header, table.row_values(i, start_colx=0, end_colx=None))))
    return db

def build_schema():
    print('build_schema')
    db=getAllDataAsDict('省级通用目录（子项）明细表 (2).xls',n=1)
    # 存储schema信息至indexdir目录
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    texts=[]
    for i in db:
        texts.append((i['子项名称'],i['主项名称']))
    # 按照schema定义信息，增加需要建立索引的文档
    writer = ix.writer()
    for title, content in texts:
        writer.add_document(title=title,content=content)
    writer.commit()

def query(label):
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = open_dir(indexdir)
    searcher = ix.searcher()
    result=searcher.search(label)
    return result