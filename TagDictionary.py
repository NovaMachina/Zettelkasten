class TagDictionary:
    _tags = {}

    @staticmethod
    def addFile(tag, file_name):
        if tag not in TagDictionary._tags:
            TagDictionary._tags[tag] = [file_name]
        else:
            TagDictionary._tags[tag].append(file_name)

    @staticmethod
    def printDictioanry():
        print(TagDictionary._tags)