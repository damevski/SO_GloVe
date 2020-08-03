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
    return text


def write_post(posttext, out_fp):
    out_fp.write(posttext)
    out_fp.write("\n")


# Efficient parsing of large XML files from
# http://stackoverflow.com/a/9814580/987185
def parse_chats(chatfile, out_fp):
    chat = dict()

    tree = etree.parse(chatfile)

    # for node in tree.findall('message'):
    #     conv_id = node.get('conversation_id')
    #     if conv_id not in convs:
    #         convs.append(conv_id)

    # for conv in convs:
    for node in tree.findall('message'):
        # processing goes here
        conv_id = node.attrib['conversation_id']
        text = node.find('text').text
        assert conv_id is not None, "The conv_id is empty"
        if text is not None:
            if conv_id in chat:
                chat[conv_id] = chat[conv_id] + " " + str(text)
            else:
                chat[conv_id] = str(text)


    for key, value in chat.items():
        text = process_post(value)
        write_post(text, out_fp)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--chatfiles', nargs='+', help='Chats in E&C format', required=True)
    parser.add_argument('-o', '--outfile', nargs=1, help='Output file in GloVe input format', required=True)
    args = parser.parse_args()

    with open(args.outfile[0],'w') as out_fp:
        for chatfile in args.chatfiles:
           parse_chats(chatfile, out_fp)
