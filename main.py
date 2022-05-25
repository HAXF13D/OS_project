from file_system import File_System, File
import sys


def choose() -> int:
    print("Выбирите действие:")
    print("1 - Список файлов")
    print("2 - Добавить файл")
    print("3 - Действия с файлами")
    print("4 - Выход")
    n = int(input())
    if 1 <= n <= 4:
        return n
    else:
        print("Попробуйте еще раз:")
        print()
        return choose()


def select_file(size) -> int:
    n = int(input("Введите номер файла: "))
    if 1 <= n <= size + 1:
        return n
    else:
        print("Некоркетный номер файла, попробуйте еще раз")
        print()
        return select_file(size)


def choose_action() -> int:
    print("1 - Удалить файл")
    print("2 - Перезапись файла")
    print("3 - Дописать в конец файла")
    print("4 - Чтение из файла")
    print("5 - Смена режима")
    print("6 - Слияние файлов")
    print("7 - Выйти из режима работы с файлом")
    n = int(input("Выберите действие: "))
    if 1 <= n <= 7:
        return n
    else:
        print("Попробуйте еще раз:")
        print()
        return choose_action()


def main():
    FS = File_System()
    files = []
    while True:
        dis = choose()
        if dis == 1:
            if len(files) != 0:
                fs = []
                for i in range(128):
                    fs.append('Null')
                for file in files:
                    file.info()
                    for block in file.blocks():
                        fs[int(block)] = file.get_filename()
                for i, name in enumerate(fs):
                    print(f"{'0'*(3-len(str(i))) + str(i)}: {name}")
            else:
                print("Файловая система пуста")
        elif dis == 2:
            name = input(
                "Введите имя файла: "
            )
            check = True
            for file in files:
                if file.get_filename() == name:
                    check = False
            if check:
                files.append(File(name=name))
                s_b = files[-1].get_start_block()
                FS.change_content(s_b, "^" + 252*'~')
            else:
                print("Файл с таким именем уже существует", file=sys.stderr)
        elif dis == 3:
            if len(files) != 0:
                for i, file in enumerate(files):
                    print(f"№{i + 1} {file.get_filename()}")
                n = select_file(len(files))
                n -= 1
                print(f"Выбран файл {files[n].get_filename()}")
                while True:
                    action = choose_action()
                    if action == 1:
                        files[n].remove()
                        temp = []
                        for i, file in enumerate(files):
                            if i != n:
                                temp.append(file)
                        files = temp
                        break
                    elif action == 2:
                        files[n].rewrite()
                    elif action == 3:
                        files[n].write()
                    elif action == 4:
                        files[n].read()
                    elif action == 5:
                        mode = input(
                            "Выбрать режим\n"
                            "r - чтение\n"
                            "w - запись\n"
                            "Режим: "
                        )
                        files[n].set_mode(mode)
                    elif action == 6:
                        print("Выбрать второй файл для склейки")
                        for i, file in enumerate(files):
                            if i != n:
                                print(f"№{i + 1} {file.get_filename()}")
                        n2 = select_file(len(files))
                        n2 -= 1
                        print(f"Выбран файл {files[n2].get_filename()}")
                        File.concat(
                            files[n],
                            files[n2]
                        )
                    elif action == 7:
                        break
            else:
                print("Файловая система пуста")
        elif dis == 4:
            exit(0)


if __name__ == "__main__":
    main()
