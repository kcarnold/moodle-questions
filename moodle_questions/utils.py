def cdata_str(text):
    if text == None:
        return ""
    return f"<![CDATA[{text}]]>"

def estr(text):
    if text == None:
        return ""
    else:
        return str(text)

def truefalse(x: bool):
    return 'true' if x else 'false'
