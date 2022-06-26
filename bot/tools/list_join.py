def list_join(exe_list, max_len=0):
    if len(exe_list) == 1:
        out = exe_list[0]
    elif len(exe_list) > 1:
        exe_str = ', '.join(map(str, exe_list))
        exe_len = len(exe_str) + 1
        if max_len and exe_len > max_len:
            prc_list = exe_list
            prc_len = exe_len
            for _ in range(1, exe_len + 1):
                if prc_len > max_len:
                    prc_list = prc_list[:-1]
                    prc_str = ', '.join(map(str, prc_list))
                    prc_len = len(prc_str) + 1
            exc_len = len(exe_list) - len(prc_list)
            exc_qnt = exc_len if exc_len > 1 else 2
            exe_str = ', '.join(map(str, exe_list[:-exc_qnt]))
            out = exe_str + f' и {exc_qnt} других'
        else:
            k = exe_str.rfind(',')
            if k > 0:
                out = exe_str[:k] + ' и' + exe_str[k + 1:]
            else:
                out = exe_str
    else:
        out = exe_list
    return out
