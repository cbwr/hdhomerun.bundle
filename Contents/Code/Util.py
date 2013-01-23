
########################################
def XPathSelectOne(doc, query):
    Log( "Util.py XPathSelectOne ..." )
    nodes = doc.xpath(query)
    if len(nodes):
        node = nodes[0]
        try: text = node.text
        except AttributeError:
            text = str(node)
        return text
    else:
        return None
