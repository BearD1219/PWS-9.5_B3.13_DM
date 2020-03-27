class HTML:
    ''' Не указывать атрибут "output" что-бы вывести результат на экран, иначе указать имя файла'''
    def __init__(self, output = "print"):
        self.output = output
        self.tag = "html"
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.output != "print":
            with open(self.output, "w") as fd:
                print("<%s>" %(self.tag), file = fd)
                for child in self.children:
                    print(child, file = fd)
                print("</%s>" %(self.tag), file = fd)
        else:
            print("<%s>" %(self.tag))
            for child in self.children:
                print(child)
            print("</%s>" %(self.tag))

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
    
    def __enter__(self):
        return(self)

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        if not self.children:
            return "<{tag}>\n</{tag}>".format(tag = self.tag)
        else:
            child_list = []
            for child in self.children:
                child_list.append(str(child))
            child_list = "\n".join(child_list)
            return "{space}<{tag}>\n{child}\n{space}</{tag}>".format(tag = self.tag, child = child_list, space = " " * 2)

class Tag:
    def __init__(self, tag, is_single = False):
        self.tag = tag
        self.text = ""
        self.is_single = is_single
        self.attributes = {}
        self.children = []
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_attr(self):
        attr = []
        for attribute, value in self.attributes.items():
            attr.append('%s = "%s"' %(attribute, value))
        attr = " ".join(attr)
        return attr

    def __str__(self):
        if self.children:
            child_list = []
            for child in self.children:
                attr = []
                for attribute, value in child.attributes.items():
                    attr.append('%s = "%s"' %(attribute, value))
                attr = " ".join(attr)
                if child.is_single:
                    child_list.append("{space}<{tag} {attr}/>".format(tag = child.tag, attr = attr, space = " " * 6))
                else:
                    child_list.append("{space}<{tag} {attr}>{text}</{tag}>".format(tag = child.tag, attr = attr, text = child.text, space = " " * 6))
            child_list = "\n".join(child_list)
            attr = self.get_attr()
            return "{space}<{tag} {attr}>{text}\n{child}\n{space}</{tag}>".format(tag = self.tag, attr = attr, text = self.text, child = child_list, space = " " * 4) 
        else:
            attr = self.get_attr()
            if self.is_single:
                return "{space}<{tag} {attr}/>".format(tag = self.tag, attr = attr, space = " " * 4)
            else:
                return "{space}<{tag} {attr}>{text}</{tag}>".format(tag = self.tag, attr = attr, text = self.text, space = " " * 4)


''' Пример разметки '''

with HTML() as html:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
        head.children.append(title)
    with TopLevelTag("body") as body:
        with Tag("h1") as h1:
            h1.attributes["class"] = "main-text"
            h1.text = "Test"
        with Tag("div") as div:
            div.attributes["class"] = "container container-fluid"
            div.attributes["id"] = "lead"
            with Tag("p") as p:
                p.text = "another test"
            with Tag("img", is_single=True) as img:
                img.attributes["src"] = "/icon.png"
                img.attributes["data-image"] = "responsive"
            div.children.append(p)
            div.children.append(img)
        body.children.append(h1)
        body.children.append(div)
    html.children.append(head)
    html.children.append(body)