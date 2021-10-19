class CommonHelper(object):
    @staticmethod
    def read_qss(style):
        with open(style, 'r', encoding='utf-8') as f:
            return f.read()
