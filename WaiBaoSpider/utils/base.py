# -*- coding:utf-8 -*-
def unicode_body(response):
    if isinstance(response.body, unicode):
        return response.body
    try:
        return response.body_as_unicode()
    except:
        try:
            return response.body.decode(response.encoding)
        except:
            raise Exception("Cannot convert response body to unicode!")


def deal_ntr(text):
    content = text.strip().replace(u"\n", u"").replace(u"\t", u"").replace(u"\r", u"").replace(u" ", u"").replace(u"&nbsp", u"")
    return content
