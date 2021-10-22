from PyQt5.QtWidgets import QComboBox


class ComboBox(QComboBox):

    def __init__(self, select):
        super(ComboBox, self).__init__()
        # 绑定text_changed事件,将改变的值写入传入的list中
        self.save_select = select
        self.currentIndexChanged.connect(self.select_changed)

    def select_changed(self):
        self.save_select.clear()
        self.save_select.append(self.currentIndex())
        print(self.save_select)
