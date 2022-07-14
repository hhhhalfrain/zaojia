import os

from whoosh import qparser
from whoosh.index import create_in, open_dir
from whoosh.fields import *

# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

import json
import xlrd
import xlwt

schema = Schema(title=TEXT(analyzer=ChineseAnalyzer(), stored=True),
                args=TEXT(analyzer=ChineseAnalyzer(), stored=True),
                id=TEXT(analyzer=ChineseAnalyzer(), stored=True)

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
    db = getAllDataAsDict('static/基础数据 2021-3-13-1.xls', n=0)
    # 存储schema信息至indexdir目录
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    texts = []
    for i in db:
        title_key = i['子目名称'].split()[0]
        print(title_key)
        args_key = ' '.join(i['子目名称'].split()[1:])
        print(args_key)
        id_key = i['子目编号']
        print(id_key)
        texts.append((title_key, args_key, id_key))
    # 按照schema定义信息，增加需要建立索引的文档
    writer = ix.writer()
    for title, args, id in texts:
        writer.add_document(title=title, args=args, id=id)
    writer.commit()


def query(label):
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
        build_schema()
    ix = open_dir(indexdir)
    searcher = ix.searcher()
    parser = QueryParser("title", schema=ix.schema,
                         group=qparser.OrGroup)
    query = parser.parse(label)
    results = searcher.search(query)
    print('查询到{}条结果'.format(len(results)))
    D = [{'title': i.highlights('title'), 'args': i['args'], 'id': i['id']} for i in results]
    return json.dumps(D, ensure_ascii=False)


if __name__ == '__main__':
    # build_schema()
    r = query('饮酒后驾驶机动车')
    r = json.JSONEncoder().encode(r)
    print(r)
