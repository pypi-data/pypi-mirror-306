class TextSplitter:
    def __init__(self, max_length: int = 2000, overlap: int = 100):
        """
        初始化TextSplitter

        Args:
            max_length (int): 每个文本块的最大长度
            overlap (int): 相邻块之间的重叠字符数,用于保持上下文连贯性
        """
        self.max_length = max_length
        self.overlap = overlap

    def split_text(self, text: str) -> list[str]:
        """
        将文本切分成多个块

        Args:
            text (str): 待切分的文本

        Returns:
            list[str]: 切分后的文本块列表
        """
        if len(text) <= self.max_length:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            # 确定当前块的结束位置
            end = start + self.max_length

            if end >= len(text):
                # 如果是最后一块,直接添加剩余文本
                chunks.append(text[start:])
                break

            # 从end位置向前查找最近的分隔符
            split_pos = self._find_split_position(text, end)

            # 添加当前块
            chunks.append(text[start:split_pos])

            # 更新下一块的起始位置,考虑重叠
            start = split_pos - self.overlap

        return chunks

    def _find_split_position(self, text: str, pos: int) -> int:
        """
        在指定位置附近寻找合适的分割点
        优先级: 段落 > 句号 > 逗号 > 空格 > 强制分割

        Args:
            text (str): 文本内容
            pos (int): 建议的分割位置

        Returns:
            int: 实际的分割位置
        """
        # 向前查找段落分隔符
        for i in range(pos, max(pos - 200, 0), -1):
            if text[i] == '\n' and i > 0 and text[i-1] == '\n':
                return i

        # 向前查找句号
        for i in range(pos, max(pos - 100, 0), -1):
            if text[i] in ['。', '.', '!', '?', '！', '？']:
                return i + 1

        # 向前查找逗号
        for i in range(pos, max(pos - 50, 0), -1):
            if text[i] in ['，', ',', '、']:
                return i + 1

        # 向前查找空格
        for i in range(pos, max(pos - 20, 0), -1):
            if text[i].isspace():
                return i

        # 如果找不到合适的分割点,则强制分割
        return pos