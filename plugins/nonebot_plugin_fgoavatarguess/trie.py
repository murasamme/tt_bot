import pygtrie
from . import _datac
from nonebot import logger


class Trie_:

    def __init__(self):
        self._all_name_list = None
        self._trie_ = pygtrie.CharTrie()
        self.update()

    def update(self):
        self._trie_.clear()
        for idx, names in _datac.CHARA_NAME.items():
            for n in names:
                if n not in self._trie_:
                    self._trie_[n] = idx
                else:
                    logger.warning(f'出现重名{n}于id{idx}与id{self._trie_[n]}')
        self._all_name_list = self._trie_.keys()

    def get_id(self, name):
        return self._trie_[name] if name in self._trie_ else 0