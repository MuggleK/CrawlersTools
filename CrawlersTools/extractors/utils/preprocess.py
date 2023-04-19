from lxml.html import etree

from CrawlersTools.extractors.schemas.element import Element
from CrawlersTools.extractors.utils.element import children, remove_element, remove_children

# fmt:off
CONTENT_EXTRACTOR_USELESS_TAGS = ['audio', 'colgroup', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'iframe',
                                  'input', 'link', 'option', 'path', 'script', 'select', 'source', 'style', 'svg',
                                  'symbol', 'video']

CONTENT_EXTRACTOR_STRIP_TAGS = ['b', 'blockquote', 'br', 'font',  'p', 'section', 'span', 'spanlang', 'spanstyle',
                                'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'th', 'tr', 'u'] # 'img'

KEYWORD_FEATURES = 'and not (contains(@class,"main")) and not (contains(@class,"content"))and not (contains(@class,"con"))and not (contains(@class,"container")) and not (contains(@class,"list")) and not (contains(@class,"box")) and not (contains(@class,"right"))and not (contains(@class,"body")) and not (contains(@class,"lanmu")) '
CONTENT_EXTRACTOR_NOISE_XPATH = [
    # '//div[contains(@class, "comment")]',
    '//div[contains(@class, "advertisement")]',
    '//div[contains(@class, "advert")]',
    '//a[contains(@style, "display: none")]',
    '//a[contains(@style, "display:none")]',  # TODO css不展示数据是否要去除，可能会影响正文重复
    f'//div[contains(@class, "foot") {KEYWORD_FEATURES}]',
    f'//div[contains(@class, "footer") {KEYWORD_FEATURES}]',
    # f'//div[contains(@class, "location") {KEYWORD_FEATURES}]',
    f'//div[contains(@class, "navigation") {KEYWORD_FEATURES}]',
    f'//div[contains(@class, "barrier") {KEYWORD_FEATURES}]',
    '//div[contains(@id, "foot")]',
    # '//div[contains(@class, "head")]',    # 误删
    # '//div[contains(@id, "head")]',
    # '//div[contains(@class, "nav")]', # 误删
    '//div[contains(@id, "nav")]',
    '//div[contains(@class, "siderbar")]',
    '//div[contains(@class, "breadcrumb")]',
    '//div[contains(@id, "siderbar")]',
    '//div[contains(@id, "页脚")]',
    '//div[contains(@class, "页脚")]',
    '//div[contains(@id, "页眉")]',
    '//div[contains(@id, "页头")]',
    '//div[contains(@class, "页眉")]',
    '//div[contains(@class, "页头")]',
    '//*[contains(@class, "hidden")]',
]


def preprocess4content_extractor(element: Element, is_content: bool = True):
    """
    preprocess element for content extraction
    :param element:
    :param is_content:  save content without tag
    :return:
    """
    remove_children(element, CONTENT_EXTRACTOR_NOISE_XPATH)

    # remove tag and its content
    etree.strip_elements(element, *CONTENT_EXTRACTOR_USELESS_TAGS)

    if not is_content: return
    # only move tag pair
    etree.strip_tags(element, *CONTENT_EXTRACTOR_STRIP_TAGS)

    for child in children(element):

        # merge text in span or strong to parent p tag
        if child.tag.lower() == 'p' or child.tag.lower() == 'table':
            etree.strip_tags(child, 'span')
            etree.strip_tags(child, 'strong')
            etree.strip_tags(child, 'tr')
            etree.strip_tags(child, 'td')

            if not (child.text and child.text.strip()):
                remove_element(child)

        # if a div tag does not contain any sub node, it could be converted to p node.
        if child.tag.lower() == 'div' and not child.getchildren():
            child.tag = 'p'


LIST_EXTRACTOR_USELESS_TAGS = CONTENT_EXTRACTOR_USELESS_TAGS
LIST_EXTRACTOR_STRIP_TAGS = CONTENT_EXTRACTOR_STRIP_TAGS
LIST_EXTRACTOR_NOISE_XPATH = CONTENT_EXTRACTOR_NOISE_XPATH


def preprocess4list_extractor(element: Element):
    """
    preprocess element for list extraction
    :param element:
    :return:
    """
    # remove tag and its content
    etree.strip_elements(element, *CONTENT_EXTRACTOR_USELESS_TAGS)
    # only move tag pair
    etree.strip_tags(element, *CONTENT_EXTRACTOR_STRIP_TAGS)

    remove_children(element, CONTENT_EXTRACTOR_NOISE_XPATH)

    for child in children(element):

        # merge text in span or strong to parent p tag
        if child.tag.lower() == 'p':
            etree.strip_tags(child, 'span')
            etree.strip_tags(child, 'strong')

            if not (child.text and child.text.strip()):
                remove_element(child)

        # if a div tag does not contain any sub node, it could be converted to p node.
        if child.tag.lower() == 'div' and not child.getchildren():
            child.tag = 'p'


LIST_CLASSIFIER_USELESS_TAGS = ['style', 'script', 'link', 'video', 'audio', 'iframe', 'source', 'svg', 'path',
                                'symbol', 'footer', 'header']
LIST_CLASSIFIER_STRIP_TAGS = ['span', 'blockquote']
LIST_CLASSIFIER_NOISE_XPATHS = [
    '//div[contains(@class, "comment")]',
    '//div[contains(@class, "advertisement")]',
    '//div[contains(@class, "advert")]',
    '//div[contains(@style, "display: none")]',
]


def preprocess4list_classifier(element: Element):
    """
    preprocess element for list classifier
    :param element:
    :return:
    """
    # remove tag and its content
    etree.strip_elements(element, *LIST_CLASSIFIER_USELESS_TAGS)
    # only move tag pair
    etree.strip_tags(element, *LIST_CLASSIFIER_STRIP_TAGS)

    remove_children(element, LIST_CLASSIFIER_NOISE_XPATHS)

    for child in children(element):

        # merge text in span or strong to parent p tag
        if child.tag.lower() == 'p':
            etree.strip_tags(child, 'span')
            etree.strip_tags(child, 'strong')

            if not (child.text and child.text.strip()):
                remove_element(child)

        # if a div tag does not contain any sub node, it could be converted to p node.
        if child.tag.lower() == 'div' and not child.getchildren():
            child.tag = 'p'
