import re
from sys import exit


def del_nums(st: str) -> str:
    res = ''
    for i in st:
        if not i.isdigit():
            res += i
    return res


def del_alph(st: str) -> str:
    res = ''
    for i in st:
        if i.isdigit():
            res += i
    return res


def nums_to_inds(nums: list[str]) -> dict[str:int]:
    resus = {}
    for n in range(len(nums)):
        resus[nums[n]] = n
    return resus


def check_str_for_dict(string: str) -> bool:
    formatik = [r'^first_name\d*$', r'^second_name\d*$', r'^last_name\d*$', r'^phone\d*$', r'^email\d*$']
    return any(bool(re.match(re.compile(i), string)) for i in formatik)


def check_email(email: str) -> bool:
    return bool(re.match(r'[a-zA-Z0-9_\-]+@[a-zA-Z0-9]+\.[a-zA-Z]', email))


def correct_name(norfors: str) -> str:
    return norfors.strip().capitalize()


def check_phone_number(phone: str) -> bool:
    nje = re.compile(r'^[0-9]{10}$')
    return bool(re.match(nje, phone))


def check_ascii(string: str) -> bool:
    checking = string  # мы должны опустошить данную нам строку
    # чтобы убедиться, что в ней нет ничего, кроме цифр и #
    for i in '0123456789#':
        checking = checking.replace(i, '')
    return (not checking) and string  # мы проверяем, пуста ли конечная строка и не пуста ли изначальная строка


def ascii_to_human(string: str) -> str or None:  # два в одном: преобразование в человеческий вид
    # и проверка на то, что пользователь ввел коды "нормальных" символов
    lst = string.split('#')
    hum = ''
    for i in lst:
        if int(i) in range(32, 127):
            hum += chr(int(i))
        else:
            print('You should use only printable characters.')
            return None
    return hum


def user_dummy(their_string: str) -> list[str] or None:
    result = None
    their_string = their_string.strip(' ').strip(',')
    if ',' not in their_string:
        print("You should use , in your input.")
        return result
    else:
        result = their_string.split(',')
        ch_res = len(list(filter(lambda x: x.count('=') == 1, result))) == len(result)
        if not ch_res:
            print("You have incorrectly used = in your input.")
            return None
        else:
            return result


def inputik(puttt: list[str]) -> dict[str: str] or None:
    res = {}
    for i in puttt:
        key, arg = i.strip(' ').split('=')
        key = key.strip(' ')
        arg = arg.strip(' ')
        if not check_str_for_dict(key):
            print('You have entered incorrect key.')
            return None
        if key not in res.keys():
            res[key] = arg
        else:
            print('You have entered two values for one argument.')
            return None
    return res


def dict_to_listdict(du: dict[str: str]) -> list[dict[str: str]] or None:
    keys = du.keys()
    if (len(keys) / 5) != (len(keys) // 5):
        return None
    else:
        resik = [{} for _ in range(len(keys) // 5)]
        nums = list(set([del_alph(i) for i in keys]))
        if len(nums) != (len(keys) // 5):
            return None
        change_num_to_ind = nums_to_inds(nums)
        for k in keys:
            index = change_num_to_ind[del_alph(k)]
            resik[index][del_nums(k)] = du[k]
        return resik


def check_dict(dd: dict[str: str]) -> dict[str: str] or None:
    usl = check_phone_number(dd['phone']) and check_email(dd['email'])
    dd['first_name'] = correct_name(dd['first_name'])
    dd['second_name'] = correct_name(dd['second_name'])
    dd['last_name'] = correct_name(dd['last_name'])
    if usl:
        return dd
    else:
        print('You have entered incorrect phone number or email.')
        return None


def listdict_to_str(du: list[dict[str:str]]) -> list[str]:
    res = []
    for i in range(len(du)):
        res.append(
            ' '.join([du[i]['last_name'], du[i]['first_name'], du[i]['second_name'], du[i]['email'], du[i]['phone']]))
    return res


def searching(user_string: str, data: list[str]) -> list[str]:
    out = []
    for item in data:
        if user_string.lower() in item.lower():
            out.append(item)
    return out


def cleaning(s: str) -> str:
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s


if __name__ == "__main__":
    first_string = input()
    while not check_ascii(first_string):
        first_string = input()
    while not ascii_to_human(first_string):
        first_string = input()
    while not user_dummy(ascii_to_human(first_string)):
        first_string = input()
    while not inputik(user_dummy(ascii_to_human(first_string))):
        first_string = input()
    perv_dict = inputik(user_dummy(ascii_to_human(first_string)))
    lst_dct = dict_to_listdict(perv_dict)
    checked_lst_dict = [check_dict(i) for i in lst_dct]
    if not all(checked_lst_dict):
        exit()
    searching_data = listdict_to_str(checked_lst_dict)
    users_string = cleaning(input())
    print(*searching(users_string, searching_data), sep='\n')
