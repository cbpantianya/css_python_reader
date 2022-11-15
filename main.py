import os
import re
import string
import shutil

import requests


# TODO: Need fix
def download_file(url, filename):
    # download file from remote
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)


# read csv from csvfile
def read_css(filename):
    with open(filename, 'r') as f:
        return f.read()


# parse css from css string
def parse_css(css: string):
    # a dict to store css
    css_font_family = []

    # use regex to parse css font-face block
    font_face = re.findall(r'@font-face\s*{[^}]*}', css)
    for i in font_face:
        # use regex to parse css font-family src unicode-range from font-face block
        font_family = re.findall(r'font-family:\s*([^;]*);', i)
        font_style = re.findall(r'font-style:\s*([^;]*);', i)
        font_weight = re.findall(r'font-weight:\s*([^;]*);', i)
        font_display = re.findall(r'font-display:\s*([^;]*);', i)
        src_url = re.findall(r'src:\s*url\(([^)]*)\)', i)
        unicode_range = re.findall(r'unicode-range:\s*([^;]*);', i)

        # add font-family to dict
        css_font_family.append({
            'font-family': font_family[0],
            'font-style': font_style[0],
            'font-weight': font_weight[0],
            'font-display': font_display[0],
            'src-url': src_url[0],
            'unicode-range': unicode_range[0]
        })

    os.makedirs('output', exist_ok=True)
    with open('output/' + 'fonts' + '.css', 'w+') as f:
        for i in css_font_family:
            file_name = re.findall(r'([^/]*\.[^/]*)$', i['src-url'])[0]
            # download font file
            download_file(i['src-url'], 'output/' + file_name)
            # write font-family to css
            f.write('@font-face {\n')
            f.write('  font-family: ' + i['font-family'] + ';\n')
            f.write('  font-style: ' + i['font-style'] + ';\n')
            f.write('  font-weight: ' + i['font-weight'] + ';\n')
            f.write('  font-display: ' + i['font-display'] + ';\n')
            f.write('  src: url(' + "'./" + file_name + "'" + ') format(\'woff2\');\n')
            f.write('  unicode-range: ' + i['unicode-range'] + ';\n')
            f.write('}\n')


if __name__ == '__main__':
    # clean file in output
    shutil.rmtree('output')
    css_str = read_css('fonts.css')
    parse_css(css_str)
