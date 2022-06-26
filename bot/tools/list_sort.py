def list_sort(dsr_list, exe_list):
    exe_list_indices = [i[0] for i in sorted(
        enumerate(exe_list), key=lambda x:x[1])]
    exe_list_indices_indices = [i[0] for i in sorted(
        enumerate(exe_list_indices), key=lambda x:x[1])]
    sorted_list = [x for _, x in sorted(
        zip(exe_list_indices_indices, dsr_list))]
    return sorted_list
