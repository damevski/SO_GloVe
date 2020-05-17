import argparse
import re
import preprocess_text as pp
from lxml import etree, html

#
#
def process_post(post):
    try:
        tree = html.fromstring(bytes(post, encoding='utf-8'))
    except etree.ParserError as e:
        if str(e) == "Document is empty":
            return ""
        raise
    for code in tree.xpath("//code"):
        if code.text is None:
            continue
        if '\n' in code.text:
            code.getparent().remove(code)
    text = pp.tokenize(tree.text_content())
    print(text)
    return text


def write_post(posttext, out_fp):
    out_fp.write(posttext)
    out_fp.write("\n")

# Efficient parsing of large XML files from
# http://stackoverflow.com/a/9814580/987185
def parse_posts(sofile, out_fp):
    context = etree.iterparse(sofile, events=('end',))
    for action, elem in context:
        if elem.tag=='row':
            # processing goes here
            if 'Title' in elem.attrib and 'Body' in elem.attrib:
                text = process_post(elem.attrib['Title'] + ' ' + elem.attrib['Body'])
                write_post(text, out_fp)
            assert elem.text is None, "The row wasn't empty"

        # cleanup
        # first empty children from current element
            # This is not absolutely necessary if you are also deleting
            # siblings, but it will allow you to free memory earlier.
        elem.clear()
        # second, delete previous siblings (records)
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        # make sure you have no references to Element objects outside the loop


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sofile', nargs=1, help='Stack Overflow Posts.xml file', required=True)
    parser.add_argument('-o', '--outfile', nargs=1, help='Output file in GloVe input format', required=True)
    args = parser.parse_args()

    with open(args.outfile[0],'w') as out_fp:
        parse_posts(args.sofile[0], out_fp)
