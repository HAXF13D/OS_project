from pprint import pprint


class File:
    def __init__(self, name, file_size=0, mode='r'):
        """
        :param name: Имя файла
        :param file_size: Размер файла в байтах
        :param mode: Режим файла(чтение(r), запись(w))
        """
        self.__set_filename(name)
        self.__set_file_size(file_size)
        self.__set_mode(mode)
        self.__set_start_block()
        self.__blocks = [self.__start_block]

    def get_filename(self):
        return self.__filename

    def blocks(self):
        return self.__blocks

    def get_start_block(self):
        return self.__start_block

    def info(self):
        print(f"Название файла: {self.__filename}")
        print(f"Размер файла: {self.__file_size}")
        print(f"Режим файла: {self.__file_mode}")
        print(f"Начальный блок: {self.__start_block}")
        print(f"Конечный блок: {self.__last_block}")
        print(f"Блоки: {self.__blocks}")
        #pprint(File_System.get_info())

    def __set_last_block(self, block):
        self.__last_block = block

    def __set_filename(self, name):
        self.__filename = name

    def __set_file_size(self, file_size):
        self.__file_size = file_size

    def __set_mode(self, mode):
        self.__file_mode = mode

    def __set_start_block(self):
        self.__start_block = File_System.find_free_block()
        self.__last_block = self.__start_block

    def remove(self):
        block = self.__start_block
        self.__blocks = []
        while int(block) != self.__last_block:
            temp = File_System.get_next_block(block)
            File_System.change_next_block_info(block, "000")
            File_System.change_content(block, 253*"~")
            block = temp
        else:
            File_System.change_next_block_info(block, "000")
            File_System.change_content(block, 253 * "~")

    def rewrite(self):
        import sys
        if self.__file_mode == 'w':
            text = input("Введите текст:\n")
            block = self.__start_block
            s_b = block
            while int(block) != self.__last_block:
                temp = File_System.get_next_block(block)
                File_System.change_next_block_info(block, "000")
                File_System.change_content(block, 253 * "~")
                block = temp
            else:
                File_System.change_next_block_info(block, "000")
                File_System.change_content(block, 253 * "~")
            amount = len(text) // 253
            last = len(text) % 253

            self.__set_file_size(len(text))

            content = []
            for i in range(amount):
                content.append(text[i*253:i*253+253])

            if last != 0:
                content.append(text[amount*253:amount*253+last] + "^" + (253-1-last)*"~")
            self.__blocks = []
            for line in content:
                block = s_b
                self.__blocks.append(block)
                File_System.change_content(block, line)
                s_b = File_System.find_free_block()
                File_System.change_next_block_info(block, str(s_b))
            self.__set_last_block(block)
        else:
            print("Файл недоступен для записи", file=sys.stderr)

    def write(self):
        import sys
        if self.__file_mode == 'w':
            text = input("Введите текст:\n")
            self.__set_file_size(self.__file_size + len(text))
            block = self.__last_block
            s_b = block
            data = File_System.get_info()[block].get('content')
            position = data.find('^')
            if position == -1:
                s_b = File_System.find_free_block()
                File_System.change_next_block_info(block, str(s_b))
            block = s_b
            data = File_System.get_info()[block].get('content')
            position_1 = data.find('^')
            position_2 = data.find('~')
            if position_1 == -1:
                position = position_2
            else:
                position = position_1
            temp = data[position::]
            insert = text[0:len(temp)]
            to_del = len(insert)
            if len(insert) < len(temp):
                insert = insert + '^' + (len(temp) - len(insert) - 1) * '~'
            final = data[:position] + insert
            File_System.change_content(block, final)
            text = text[to_del::]
            amount = len(text) // 253
            last = len(text) % 253
            content = []
            for i in range(amount):
                content.append(text[i * 253:i * 253 + 253])
            if last != 0:
                content.append(text[amount * 253:amount * 253 + last] + "^" + (253 - 1 - last) * "~")
            if len(content) != 0:
                s_b = File_System.find_free_block()
                self.__blocks.append(s_b)
                File_System.change_next_block_info(block, str(s_b))
            for line in content:
                block = s_b
                self.__blocks.append(block)
                File_System.change_content(block, line)
                s_b = File_System.find_free_block()
                File_System.change_next_block_info(block, str(s_b))
            self.__set_last_block(block)
        else:
            print("Файл недоступен для записи", file=sys.stderr)

    def read(self):
        import sys
        if self.__file_mode == "r":
            block = self.__start_block
            text = ""
            map_file_content = File_System.get_info()
            while int(block) != self.__last_block:
                text += map_file_content[int(block)]['content']
                block = map_file_content[int(block)]['next_block']
            else:
                text += map_file_content[int(block)]['content']
            text = text.replace("~", "")
            text = text.replace("^", "\n")
            print(text)
        else:
            print("Файл недоступен для чтения", file=sys.stderr)

    def set_mode(self, mode):
        import sys
        if mode == "r":
            self.__set_mode(mode)
        elif mode == "w":
            self.__set_mode(mode)
        else:
            print(f"Неверный режим", file=sys.stderr)

    @staticmethod
    def concat(first, second):
        import sys
        if isinstance(first, File) and isinstance(second, File):
            if first.__file_mode == "w" and second.__file_mode == "r":
                block = second.__start_block
                text = ""
                map_file_content = File_System.get_info()
                while int(block) != second.__last_block:
                    text += map_file_content[int(block)]['content']
                    block = map_file_content[int(block)]['next_block']
                else:
                    text += map_file_content[int(block)]['content']
                text = text.replace("~", "")
                text = text.replace("^", "\n")

                first.__set_file_size(first.__file_size + len(text))
                block = first.__last_block
                s_b = block
                data = File_System.get_info()[block].get('content')
                position = data.find('^')
                if position == -1:
                    s_b = File_System.find_free_block()
                    File_System.change_next_block_info(block, str(s_b))
                block = s_b
                data = File_System.get_info()[block].get('content')
                position_1 = data.find('^')
                position_2 = data.find('~')
                if position_1 == -1:
                    position = position_2
                else:
                    position = position_1
                temp = data[position::]
                insert = text[0:len(temp)]
                to_del = len(insert)
                if len(insert) < len(temp):
                    insert = insert + '^' + (len(temp) - len(insert) - 1) * '~'
                final = data[:position] + insert
                File_System.change_content(block, final)
                text = text[to_del::]
                amount = len(text) // 253
                last = len(text) % 253
                content = []
                for i in range(amount):
                    content.append(text[i * 253:i * 253 + 253])
                if last != 0:
                    content.append(text[amount * 253:amount * 253 + last] + "^" + (253 - 1 - last) * "~")
                if len(content) != 0:
                    s_b = File_System.find_free_block()
                    File_System.change_next_block_info(block, str(s_b))
                for line in content:
                    block = s_b
                    File_System.change_content(block, line)
                    s_b = File_System.find_free_block()
                    File_System.change_next_block_info(block, str(s_b))
                first.__set_last_block(block)
            else:
                print("Невозможно выполнить слияние!", file=sys.stderr)
                print("Проверьте режимы файлов", file=sys.stderr)


class File_System:
    """
    Структура файла file.map
        Первые 3 символа - указатель на следующий блок
        Остальные 253 символа - контент файла
    """

    def __init__(self):
        """
        Иициализируем файловую систему
        Создаем файл file.map
        записываем 128 строк по 256 символов
        1 символ - 1 байт
        """
        from config import ROOT_DIR
        my_file = open(f'{ROOT_DIR}/file.map', "w+")
        for i in range(0, 128):
            my_file.write("000" + 253 * "~")
        my_file.close()

    @staticmethod
    def get_info():
        """
        Получаем информацию о файловой системе
        :return: Словарь для каждых 256 байт файла
        """
        from config import ROOT_DIR
        my_file = open(f'{ROOT_DIR}/file.map', "r")
        file_contents = my_file.read()
        i = 0
        block, content = 0, ""
        d = {}

        for sym in range(0, len(file_contents), 256):
            d[sym//256] = {
                'next_block': file_contents[sym:sym + 3],
                'content': file_contents[sym + 3:sym + 256]
            }

        my_file.close()
        return d

    @staticmethod
    def find_free_block():
        import sys
        map_file_content = File_System.get_info()
        for key in map_file_content:
            if map_file_content[key].get('next_block') == '000' \
                    and map_file_content[key].get('content')[0] == '~':
                return key
        print(f"Свободного места нет", file=sys.stderr)

    @staticmethod
    def get_next_block(key):
        key = int(key)
        map_file_content = File_System.get_info()
        next_block = None
        try:
            next_block = map_file_content[key].get("next_block")
        except Exception as e:
            print(e)
        return next_block

    @staticmethod
    def change_next_block_info(key, new_block):
        key = int(key)
        map_file_content = File_System.get_info()
        map_file_content[key]['next_block'] = (3 - len(str(new_block))) * '0' + str(new_block)
        from config import ROOT_DIR
        my_file = open(f'{ROOT_DIR}/file.map', "w+")
        for key in map_file_content:
            temp = map_file_content[key]['next_block']
            temp += map_file_content[key]['content']
            my_file.write(temp)
        my_file.close()

    @staticmethod
    def change_content(key, new_content):
        key = int(key)
        map_file_content = File_System.get_info()
        map_file_content[key]['content'] = new_content
        from config import ROOT_DIR
        my_file = open(f'{ROOT_DIR}/file.map', "w+")
        for key in map_file_content:
            temp = map_file_content[key]['next_block']
            temp += map_file_content[key]['content']
            my_file.write(temp)
        my_file.close()
