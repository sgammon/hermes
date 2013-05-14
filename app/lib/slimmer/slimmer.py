#!/usr/bin/python

__version__='0.1.30'
__all__=['acceptableSyntax','guessSyntax','slimmer','css_slimmer',
         'html_slimmer','xhtml_slimmer','js_slimmer',
         '__version__']

import re, os, sys, getopt
import urllib2
try:
    from js_function_slimmer import slim as js_function_slimmer
except ImportError:
    js_function_slimmer = None

## Options
#
# If you're slimming HTML docs and really want to
# convert border="0" to border=0, be aware that this
# can take 5 times longer than without but compresses
# the document at least twice as good.
UNQUOTE_HTML_ATTRIBUTES = 0


# Define the syntax options we accept
HTML = 'html'
XHTML = 'xhtml'
CSS = 'css'
JS = 'js'

OK_SYNTAX = (HTML, XHTML, CSS, JS)

def acceptableSyntax(syntax):
    """ return the syntax as we recognize it or None """
    syntax = str(syntax).lower().strip().replace(' ','').replace('-','')
    syntax = syntax.replace('stylesheet','css') # allow for alias
    syntax = syntax.replace('javascript','js') # allow for alias
    if syntax in OK_SYNTAX:
        return syntax
    else:
        return None

some_javascript_code_regex = re.compile(
    'function\(\)\s*{|var \w|return false;|return true;|'\
    'function \w{2,15}\(|}\s*else if\s*\(')
some_css_code_regex = re.compile('^#\w+\s*{|body\s*{|font-family:|margin:0|display:'\
                                 '|height:\s*\d|border:1px')
_html_doctypes = ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01',)
_xhtml_doctypes = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional',
                   '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict')
some_xhtml_code_regex = re.compile('|'.join([re.escape(x) for x in _xhtml_doctypes])+\
                                   '|<html>|<title>|\s/>|<input|<a\s+', re.I)
some_html_code_regex = re.compile('|'.join([re.escape(x) for x in _html_doctypes])+\
                                  '|<table|background=\"|<script|border=0|<!--', re.I)
def guessSyntax(code):
    code = code.strip()
    if some_html_code_regex.findall(code):
        return HTML
    elif some_xhtml_code_regex.findall(code):
        return XHTML
    elif some_javascript_code_regex.findall(code):
        return JS
    elif some_css_code_regex.findall(code):
        return CSS
    else:
        # getting desperate but we shall prevail!
        if '</' in code:
            if '/>' in code or '/ >' in code:
                return XHTML
            return HTML

    return None

def slimmer(code, syntax=XHTML, hardcore=False):
    """ wrap all function we have """
    if syntax == XHTML:
        return _xhtml_slimmer(code)
    elif syntax == HTML:
        return _html_slimmer(code)
    elif syntax == CSS:
        return _css_slimmer(code)
    elif syntax == JS:
        return _js_slimmer(code, slim_functions=bool(hardcore))

try:
    import itertools
    def anyTrue(pred, seq):
        return True in itertools.imap(pred,seq)
except ImportError:
    def anyTrue(pred, seq):
        for e in seq:
            if pred(e):
                return True
        return False



# CSS
css_comments = re.compile(r'/\*.*?\*/', re.MULTILINE|re.DOTALL)
hex_colour = re.compile(r'#\w{2}\w{2}\w{2}')

def _css_slimmer(css):
    """ remove repeating whitespace ( \t\n) """

    #css = css_comments.sub('', css) # remove comments
    remove_next_comment = 1
    for css_comment in css_comments.findall(css):
        if css_comment[-3:]=='\*/':
            remove_next_comment=0
            continue
        if remove_next_comment:
            css = css.replace(css_comment, '')
        else:
            remove_next_comment = 1

    css = re.sub(r'\s\s+', ' ', css) # >= 2 whitespace becomes one whitespace
    css = re.sub(r'\s+\n', '', css) # no whitespace before end of line
    # Remove space before and after certain chars
    for char in ('{', '}', ':', ';', ','):
        css = re.sub(char+r'\s', char, css)
        css = re.sub(r'\s'+char, char, css)
    css = re.sub(r'\s+</',r'</', css) # no extraspace before </style>
    css = re.sub(r'}\s(#|\w)', r'}\1', css)
    css = re.sub(r';}', r'}', css) # no need for the ; before end of attributes
    css = re.sub(r'}//-->', r'}\n//-->', css)
    css = simplifyHexColours(css)

    # voice-family hack. The declation: '''voice-family: "\"}\""''' requires
    # that extra space between the ':' and the first '"' which _css_slimmer()
    # removed. Put it back (http://real.issuetrackerproduct.com/0168)
    css = re.sub(r'voice-family:"\\"}\\""', r'voice-family: "\\"}\\""', css)

    return css.strip()


# HTML
f_IMD = re.I|re.MULTILINE|re.DOTALL
f_MD = re.MULTILINE|re.DOTALL
f_M = re.MULTILINE

# the comment has to start with a space or a charater
# otherwise me might remove a SSI include which can look like this:
#  <!--#include virtual="/include/myinclude.asp"-->
html_comments_oneline = re.compile(r'<!--[\w\s].*?-->', re.I)

html_inline_css = re.compile(r'<style.*?>.*?</style>', f_IMD)
html_inline_js = re.compile(r'<script.*?>.*?</script>', f_IMD)

any_tag = re.compile(r"<\w.*?>", f_IMD)
excess_whitespace = re.compile(r' \s+|\s +', f_M)
excess_whitespace1 = re.compile(r'\w\s+\w', f_M)
excess_whitespace2 = re.compile(r'"\s+>', f_M)
excess_whitespace3 = re.compile(r"'\s+>", f_M)
excess_whitespace4 = re.compile('"\s\s+\w+="|\'\s\s+\w+=\'|"\s\s+\w+=|\'\s\s+\w+=', f_M)
excess_whitespace6 = re.compile(r"\d\s+>", f_M)

quotes_in_tag = re.compile('([a-zA-Z]+)="([a-zA-Z0-9-_\.]+)"')

def _html_slimmer(html, xml=0):
    """ Optimize like XHTML but go one step further """
    # 1. optimize inline CSS
    for styletag in html_inline_css.findall(html):
        html = html.replace(styletag, css_slimmer(styletag))

    # 2. optimize inline Javascript
    for scripttag in html_inline_js.findall(html):
        html = html.replace(scripttag, js_slimmer(scripttag))

    # 2. Remove excessive whitespace between tags
    html = re.sub(r'>\s+<','><', html)

    # 3. Remove oneline comments
    html = html_comments_oneline.sub('', html)

    # 4. In every tag, remove quotes on numerical attributes and all
    # excessive whitespace

    ew1 = excess_whitespace1 # shortcut
    ew6 = excess_whitespace6 # shortcut
    ew4 = excess_whitespace4 # shortcut

    for tag in uniqify(any_tag.findall(html)):
        # 4a. observe exceptions
        if tag.startswith('<!') or tag.find('</')>-1:
            continue
        original = tag

        # 4b. remove excess whitespace inside the tag
        tag= excess_whitespace2.sub('">', tag)
        tag= excess_whitespace3.sub("'>", tag)

        for each in ew1.findall(tag)+ew6.findall(tag):
            tag = tag.replace(each, excess_whitespace.sub(' ',each))
        for each in ew4.findall(tag):
            tag = tag.replace(each, each[0]+' '+each[1:].lstrip())

        # 4c. remove quotes
        if not xml and UNQUOTE_HTML_ATTRIBUTES:
            tag= quotes_in_tag.sub(r'\1=\2', tag)

        # has the tag been improved?
        if original != tag:
            html = html.replace(original, tag)

    return html.strip()



def _xhtml_slimmer(xhtml):
    # currently not difference
    return _html_slimmer(xhtml, xml=1)


excess_whitespace_js = re.compile('^\s+(\S)',re.MULTILINE)
excess_whitespace_js2 = re.compile('(\S+);\s+(\S+)', re.MULTILINE)
whitespaced_func_def = re.compile('(function)\s+(\S+\(.*?\))\s*{\s*(\S+)', f_IMD)
whitespaced_func_def2 = re.compile('function\s*\(\)\s*{\s*(\S+)', f_IMD)
js_comments_singlelines = re.compile('^//.*?$|\s+//.*?$', re.DOTALL|re.MULTILINE|re.I)
js_comments_singlelines2 = re.compile('((^|;|\s)//.*?$)', re.DOTALL|re.MULTILINE|re.I)
js_comment_end = re.compile('-->')
js_comment_start = re.compile('(<!--(.*?))$\s(\w+)', re.MULTILINE)
#js_comment_start2 = re.compile('(\<\!--(.*?)(\n+|[\r\n]+)\s*(\w+))', re.DOTALL|re.MULTILINE)
whitespaced_controls = re.compile('(for|else if|if|catch|while)\s*\((.*?)\)\s*{\s*(\S+)', f_IMD)
single_whitespaced_controls = re.compile('(try|else)\s*{\s*(\S+)', f_IMD)
sloppy_conditionals = re.compile('\(\s*(\S+)\s*(==|!=)\s*(\S+)\)')
sloppy_parameters = re.compile('\(([(\w+)\s,]+)\)')
sloppy_ifs = re.compile('\s*(if|else if|else)\s*({|\()')
sloppy_declarations = re.compile('var\s+(\w+)\s*=\s*(\d+|\w+|\"[\w+ ]\"|\[[\'\w \.,\"]+\])')
sloppy_simple_declarations = re.compile('(\w+)\s*=\s*(\d+|\w+|\"[\w+ ]\")')
sloppy_increments = re.compile('(\w+)\s*(\+=|-=)\s*(\d*|\"\w+\")')
js_multiline_comments = re.compile(r'/\*.*?\*/', re.MULTILINE|re.DOTALL)
closing_curly_brackets = re.compile(r'\s*}', re.MULTILINE)
opening_curly_brackets = re.compile(r'{\s*', re.MULTILINE)

def _js_slimmer(js, slim_functions=False):

    # 1. remove all whitespace starting every line
    js = excess_whitespace_js.sub(r'\1',js)

    # 2. Remove all /* multiline comments  */
    js = js_multiline_comments.sub('',js)

    # 3. // style comments
    def _reject_slashslash_comment(match):

        if match.group().find('-->')==-1:
            return ''
        else:
            return match.group()
    js = js_comments_singlelines.sub(_reject_slashslash_comment, js)
    _="""
    for comment, start in js_comments_singlelines2.findall(js):
        # ...except those that contain -->
        replacewith = ''
        if start == ';':
            replacewith = ';'
        if not js_comment_end.findall(comment):
            js = js.replace(comment, replacewith)
    """

    js = js_comment_start.sub(r'<!--\n\3', js)

    # 3. excessive whitespace after semicolons
    js = excess_whitespace_js2.sub(r'\1;\2', js)

    # 4. functions defined with lots of whitespace
    js = whitespaced_func_def.sub(r'\1 \2{\3', js)
    js = whitespaced_func_def2.sub(r'function(){\1', js)

    # 5. control statements with lots of whitespace
    js = whitespaced_controls.sub(r'\1(\2){\3', js)

    # 6. control statements without params with lots of whitespace
    js = single_whitespaced_controls.sub(r'\1{\2', js)

    # 7. convert '(page == "foo")' to '(page=="foo")'
    js = sloppy_conditionals.sub(r'(\1\2\3)', js)

    # 8. convert '} else if {' to '}else if{'
    js = sloppy_ifs.sub(r'\1\2', js)

    # 9. convert 'var x = foo' to 'var x=foo'
    js = sloppy_declarations.sub(r'var \1=\2',js)
    js = sloppy_simple_declarations.sub(r'\1=\2', js)

    # 10. whitespace around closing } curly brackets
    js = opening_curly_brackets.sub('{', js)
    js = closing_curly_brackets.sub('}', js)

    # 11. Neater parameter lists

    #js = sloppy_parameters.sub(lambda m:m.group().replace(' ',''), js)
    def param_list_fixer(m):
        whole = m.group()
        params = m.groups()[0]
        return whole.replace(params,
                 ','.join([x.strip() for x in params.split(',')]))
    js = sloppy_parameters.sub(param_list_fixer, js)

    # 12. sloppy increments
    js = sloppy_increments.sub(r'\1\2\3', js)

    if slim_functions and js_function_slimmer:
        js = js_function_slimmer(js)

    return js.strip()


## ----- Some fancier names
##

def css_slimmer(css, hardcore=False):
    return _css_slimmer(css)

def xhtml_slimmer(xhtml, hardcore=False):
    return _xhtml_slimmer(xhtml)

def html_slimmer(html, hardcore=False):
    return _html_slimmer(html)

def js_slimmer(js, hardcore=False):
    return _js_slimmer(js, slim_functions=bool(hardcore))


## ----- Methods related to simplifying HEX colour codes

def uniqify(all):
    """ borrowed from Tim Peters' algorithm on ASPN Cookbook """
    # REMEMBER! This will shuffle the order of the list
    u = {}
    for each in all:
        u[each]=1
    return u.keys()

def simplifyHexColours(text):
    """ Replace all colour declarations where pairs repeat.
    I.e. #FFFFFF => #FFF; #CCEEFF => #CEF
    and #EFEFEF, #EFCDI9 avoided """
    colour_replacements = {}
    all_hex_encodings = hex_colour.findall(text)

    for e in uniqify(all_hex_encodings):
        if e[1]==e[2] and e[3]==e[4] and e[5]==e[6]:
            colour_replacements[e] = '#'+e[1]+e[3]+e[5]
    for k, v in colour_replacements.items():
        text = text.replace(k, v)
    return text


def __grr():
    print "Usage: python slimmer.py /path/to/input.html [xhtml|html|css|js] /path/to/output.html"

def _pingable(url):
    try:
        urllib2.urlopen(url)
        return 1
    except:
        return 0

def _is_openable_url(path_or_url):
    # looks like a URL?
    if path_or_url.lower().startswith('http'):
        return _pingable(path_or_url)
    else:
        return 0

def __guess_syntax(filepath):
    lines = []

    if os.path.isfile(filepath) or _is_openable_url(filepath):
        if filepath.lower().endswith('.css'):
            return 'css'
        elif filepath.lower().endswith('.js'):
            return 'js'

        if os.path.isfile(filepath):
            f=open(filepath)
        else:
            f=urllib2.urlopen(filepath)

        line = f.readline()
        c = 0
        while len(lines) < 50 and line is not None:
            if line.strip():
                lines.append(line)
            line = f.readline()
            c += 1
            if c>100:
                break # paranoid safety

        f.close()

        lines_list = lines
        lines = '\n'.join([x for x in lines_list if x.find('!DOCTYPE')>-1])
        if lines.find('HTML 4.0')>-1:
            return 'html'
        elif lines.find('XHTML 1.0')>-1:
            return 'xhtml'
        elif lines.find('<html>') > -1:
            return 'html'
        else:
            lines = '\n'.join(lines_list)
            if lines.lower().find('<html') > -1:
                return 'html'

        if filepath.lower().endswith('.html') or \
          filepath.lower().endswith('.htm'):
            return 'html'


    return None


def __showversion():
    print __version__

def __usage():
    print usage

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vt", 
                           ["help", "output=", "version", "test", "hardcore"])
        except getopt.error, msg:
            raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    outputfile = None
    speedtest = 0
    hardcore = False

    for o, a in opts:
        if o == "--version":
            __showversion()
            return 2
        elif o in ('-h', '--help'):
            __usage()
            return 3
        elif o in ('-o', '--output'):
            outputfile = a
        elif o in ("-t", "--test"):
            speedtest = 1
        elif o == '--hardcore':
            hardcore = True

    if not args:
        __usage()
        return 4

    syntax = None
    inputfile = None
    otherargs = []
    for arg in args:
        if arg in ('-t', '--test'):
            speedtest = 1
        elif arg.startswith('--output='):
            outputfile = arg[9:]
        elif acceptableSyntax(arg):
            syntax = acceptableSyntax(arg)
        elif os.path.isfile(arg) or _is_openable_url(arg):
            inputfile = arg
        else:
            otherargs.append(arg)

    if inputfile and syntax is None:
        syntax = __guess_syntax(inputfile)

    if inputfile is None:
        print >>sys.stderr, "No input file"
        print >>sys.stderr, "for help use --help"
        return 2

    if not acceptableSyntax(syntax):
        print >>sys.stderr, "Unrecognized syntax"
        print >>sys.stderr, "for help use --help"
        return 2

    if otherargs:
        print >>sys.stderr, "Unrecognized arguments %r"%otherargs
        print >>sys.stderr, "for help use --help"
        return 2



    run(inputfile, syntax, speedtest, outputfile, hardcore=hardcore)

    return 0


from time import time

def _gzipText(content):
    import cStringIO,gzip
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(None, 'wb', 9, zbuf)
    zfile.write(content)
    zfile.close()
    return zbuf.getvalue()

def run(inputfile, syntax, speedtest, outputfile, hardcore=False):
    if os.path.isfile(inputfile):
        contents = open(inputfile).read()
    else:
        contents = urllib2.urlopen(inputfile).read()
    t0=time()
    slimmed = slimmer(contents, syntax, hardcore=hardcore)
    t=time()-t0



    if speedtest:
        before = len(contents)
        after = len(slimmed)
        after_zlibbed = len(slimmed.encode('zlib'))
        after_gzip = len(_gzipText(slimmed))
        size_before = before
        if size_before > 100000:
            size_before = "%s (%sK)"%(size_before, size_before/1024)
        size_after = after
        if size_after > 100000:
            size_after = "%s (%sK)"%(size_after, size_after/1024)
        size_difference = before-after
        if size_difference > 10000:
            size_difference = "%s (%sK)"%(size_difference, size_difference/1024)
        print "Took %s seconds"%round(t, 3)
        print "Bytes before: %s"%size_before
        print "Bytes after:  %s"%size_after
        print "Bytes after zlib: %s"%after_zlibbed
        print "Bytes after gzip: %s"%after_gzip
        print "Bytes saved:  %s "%size_difference,
        print "(%s%% of original size)"%(100*round(after/float(before), 2))

    elif outputfile:
        open(outputfile, 'w').write(slimmed)

    else:
        print >>sys.stdout, slimmed


if __name__=='__main__':
    sys.exit(main())


