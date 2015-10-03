#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-09-17
# 

import re
import os
import sys
import codecs

prep = [u'и', u'в', u'не', u'на', u'я', u'он', u'с', u'а', u'что', u'по',
 u'к', u'но', u'мы', u'из', u'у', u'за', u'весь', u'от', u'о', u'ты', u'вы',
 u'или', u'еще', u'до', u'наш', u'мой', u'во', u'со', u'под', u'ну', u'их', 
 u'без', u'ни', u'для', u'об', u'для']
 
post= [u'ли', u'же', u'век', u'год', u'г\.', u'вв\.', u'века', u'бы']

def transform(content):
    content = content.replace(u'\n', u'\n\n')
    content = content.replace(u'...', u'\\dots')
    content = content.replace(u'…', u'\\dots')
    content = content.replace(u'\xa0', u' ')
    content = re.sub('( )+', ' ', content)
    content = content.replace(u'\xad', u'')
    
    for pr in prep:
        content = re.sub(u'(\n| |«|\()' + pr + u' ', u'\\1' + pr + u'~', content, flags = re.UNICODE)
        pr = pr.capitalize()
        content = re.sub(u'(\n| |«|\()' + pr + u' ', u'\\1' + pr + u'~', content, flags = re.UNICODE)
    for ps in post:
        content = re.sub(u' (' + ps + u')( |\n|[.,!?])', u'~\\1\\2', content, flags = re.UNICODE)
        
    content = re.sub(u'([А-ЯЁ])\.( )?([А-ЯЁ])', u'\\1.",\\3', content)
    content = re.sub(u'([А-ЯЁ])\.( )?([А-ЯЁ])', u'\\1.",\\3', content)
    content = re.sub(u'([А-ЯЁа-яё0-9])-([А-ЯЁа-яё])', u'\\1"=\\2', content)
    content = re.sub(u'(\d|[CMXVIL])(—|-|–)(\d|[CMXVIL])', u'\\1\\,--\\,\\3', content)
    content = re.sub(u'( )(—|-|–)( )', u'\\1"---\\3', content)
    content = re.sub(u'\n(\s+)?(—|-|–)', u'\n"--*', content)
    content = re.sub(u'(\d)( )?%', u'\\1~\%', content)
    return content
    

def main(argv):
    for fl in argv[1:]:
        f = codecs.open(fl, 'r', 'utf-8')
        content = f.read()
        f.close
        if fl.endswith('.txt'):
            fl = fl.replace('.txt', '.tex')
        else:
            fl = fl + '.tex'
        content = transform(content)
        fw = codecs.open(fl, 'w', 'utf-8')
        fw.write(content)
    
    return 0

if __name__ == '__main__':
    main(sys.argv)

