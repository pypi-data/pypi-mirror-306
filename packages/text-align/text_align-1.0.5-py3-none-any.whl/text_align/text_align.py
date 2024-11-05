def justify(text: str, width: int) -> str:
    # разделяем строку по пробелам на слова
    splitted_text = text.split(' ')
    # делаем начальный список для рядов со словами
    rows_list = [[splitted_text[0]]]

    for i in range(1, len(splitted_text)):
        # кол-во одиночных пробелов между словами
        default_row_spaces = len(rows_list[-1]) - 1

        # суммируем длину слов и одиночных пробелов между ними
        last_row_len = sum(map(lambda word: len(word), rows_list[-1])) + default_row_spaces

        # если длина последнего ряда со следующим словом больше запрашиваемой (с 1 пробелом между всеми словами ряда)
        if (last_row_len + len(splitted_text[i]) + 1) > width:
            # кол-во дополнительных пробелов для набора заданной длины ряда
            row_extra_spaces = width - last_row_len
            # кол-во всех пробелов для набора заданной длины ряда
            row_all_spaces = default_row_spaces + row_extra_spaces
            # кол-во пробелов для добавления к каждому слову (кроме последнего)
            add_each = row_all_spaces // default_row_spaces if default_row_spaces > 0 else 0
            # кол-во пробелов, оставшихся для добавления, после добавления к каждому слову
            add_left = row_all_spaces % default_row_spaces if default_row_spaces > 0 else 0

            for j in range(default_row_spaces):
                # если к слову нужно добавить дополнительный пробел, кроме тех, что для каждого слова
                if j < add_left:
                    rows_list[-1][j] += ' ' * (add_each + 1)
                else:
                    rows_list[-1][j] += ' ' * add_each

            # добавляем в список рядов новый ряд с текущим словом
            rows_list.append([splitted_text[i]])
        else:
            rows_list[-1].append(splitted_text[i])
    # добавляем пробелы между словами в последнем ряду
    for i in range(len(rows_list[-1]) - 1):
        rows_list[-1][i] += ' '

    justify_str = '\n'.join([''.join(row) for row in rows_list])
    return justify_str


def left(text: str, width: int) -> str:
    # разделяем строку по пробелам на слова
    splitted_text = text.split(' ')
    # делаем начальный список для рядов со словами
    rows_list = [[splitted_text[0]]]

    for i in range(1, len(splitted_text)):
        # суммируем длину слов и одиночных пробелов между ними
        last_row_len = sum(map(lambda word: len(word), rows_list[-1]))

        # если длина последнего ряда со следующим словом больше запрашиваемой (с 1 пробелом между всеми словами ряда)
        if (last_row_len + len(splitted_text[i]) + 1) > width:
            # кол-во дополнительных пробелов для набора заданной длины ряда
            row_extra_spaces = width - last_row_len
            # добавляем недостающие пробелы в конец строки
            rows_list[-1].append(' ' * row_extra_spaces)

            # добавляем в список рядов новый ряд с текущим словом
            rows_list.append([splitted_text[i]])
        else:
            rows_list[-1].append(' ' + splitted_text[i])

    justify_str = '\n'.join([''.join(row) for row in rows_list])
    return justify_str


def right(text: str, width: int) -> str:
    # разделяем строку по пробелам на слова
    splitted_text = text.split(' ')
    # делаем начальный список для рядов со словами
    rows_list = [[splitted_text[0]]]

    for i in range(1, len(splitted_text)):
        # суммируем длину слов и одиночных пробелов между ними
        last_row_len = sum(map(lambda word: len(word), rows_list[-1]))

        # если длина последнего ряда со следующим словом больше запрашиваемой (с 1 пробелом между всеми словами ряда)
        if (last_row_len + len(splitted_text[i]) + 1) > width:
            # кол-во дополнительных пробелов для набора заданной длины ряда
            row_extra_spaces = width - last_row_len
            # добавляем недостающие пробелы в начало строки
            rows_list[-1].insert(0, ' ' * row_extra_spaces)

            # добавляем в список рядов новый ряд с текущим словом
            rows_list.append([splitted_text[i]])
        else:
            rows_list[-1].append(' ' + splitted_text[i])

    # суммируем длину слов и одиночных пробелов между ними последнего ряда
    last_row_len = sum(map(lambda word: len(word), rows_list[-1]))
    # добавляем недостающие пробелы в начало строки в последнем ряду
    rows_list[-1].insert(0, ' ' * (width - last_row_len))

    justify_str = '\n'.join([''.join(row) for row in rows_list])
    return justify_str


def center(text: str, width: int) -> str:
    # разделяем строку по пробелам на слова
    splitted_text = text.split(' ')
    # делаем начальный список для рядов со словами
    rows_list = [[splitted_text[0]]]

    for i in range(1, len(splitted_text)):
        # суммируем длину слов и одиночных пробелов между ними
        last_row_len = sum(map(lambda word: len(word), rows_list[-1]))

        # если длина последнего ряда со следующим словом больше запрашиваемой (с 1 пробелом между всеми словами ряда)
        if (last_row_len + len(splitted_text[i]) + 1) > width:
            # кол-во дополнительных пробелов для набора заданной длины ряда
            row_extra_spaces = width - last_row_len

            add_to_start = row_extra_spaces // 2
            add_to_end = row_extra_spaces - add_to_start
            # добавляем недостающие пробелы в начало и конец строки
            rows_list[-1].insert(0, ' ' * add_to_start)
            rows_list[-1].append(' ' * add_to_end)

            # добавляем в список рядов новый ряд с текущим словом
            rows_list.append([splitted_text[i]])
        else:
            rows_list[-1].append(' ' + splitted_text[i])

    # суммируем длину слов и одиночных пробелов между ними последнего ряда
    last_row_len = sum(map(lambda word: len(word), rows_list[-1]))
    # кол-во дополнительных пробелов для набора заданной длины ряда
    row_extra_spaces = width - last_row_len

    add_to_start = row_extra_spaces // 2
    add_to_end = row_extra_spaces - add_to_start
    # добавляем недостающие пробелы в начало и конец строки
    rows_list[-1].insert(0, ' ' * add_to_start)
    rows_list[-1].append(' ' * add_to_end)

    justify_str = '\n'.join([''.join(row) for row in rows_list])
    return justify_str


if __name__ == '__main__':
    str_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sagittis dolor mauris, at elementum ligula tempor eget. In quis rhoncus nunc, at aliquet orci. Fusce at dolor sit amet felis suscipit tristique. Nam a imperdiet tellus. Nulla eu vestibulum urna. Vivamus tincidunt suscipit enim, nec ultrices nisi volutpat ac. Maecenas sit amet lacinia arcu, non dictum justo. Donec sed quam vel risus faucibus euismod. Suspendisse rhoncus rhoncus felis at fermentum. Donec lorem magna, ultricies a nunc sit amet, blandit fringilla nunc. In vestibulum velit ac felis rhoncus pellentesque. Mauris at tellus enim. Aliquam eleifend tempus dapibus. Pellentesque commodo, nisi sit amet hendrerit fringilla, ante odio porta lacus, ut elementum justo nulla et dolor."
    res = justify(text=str_text, width=55)

    print()
    print(res)
