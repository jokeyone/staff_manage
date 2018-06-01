#!/usr/bin/env python
# encoding: utf-8
from tabulate import tabulate

DB_FILE = "staff.db"
COLUMNS = ['id', 'name', 'age', 'phone', 'dept', 'enrolled_date']


# 加载员工信息表，并转成指定的格式
def load_db(db_file):
    """
    加载员工信息表，并转成指定的格式
    :param db_file:
    :return:
    """
    data = {}
    for i in COLUMNS:
        data[i] = []
    f = open(db_file, "r")
    for line in f:
        staff_id, name, age, phone, dept, enrolled_date = line.split(',')
        data['id'].append(staff_id)
        data['name'].append(name)
        data['age'].append(age)
        data['phone'].append(phone)
        data['dept'].append(dept)
        data['enrolled_date'].append(enrolled_date)
    return data


def save_db():
    """把内存数据存入硬盘"""
    f = open("%s.new" % DB_FILE, "w", encoding="utf-8")
    for index, staff_id in enumerate(STAFF_DATA['id']):
        row = []
        for col in COLUMNS:
            row.append(STAFF_DATA[col][index])
        f.write(",".join(row))
    f.close()


# 执行加载员工信息
STAFF_DATA = load_db(DB_FILE)  # 程序一启动就执行


# 打印日志用,正常打印，错误红色打印
def print_log(msg, log_type="info"):
    if log_type == 'info':
        print("\033[32;1m %s \033[0m" % msg)
    elif log_type == 'error':
        print("\033[31;1m %s \033[0m" % msg)


def syntax_where(clause):
    '''
    解析where条件，并过滤数据
    :param clause: eg. age>22
    :return:
    '''

    # 大于
    def op_gt(column, condition_val):
        '''
        :param column: eg.age
        :param condition_val: eg.22
        :return:
        '''
        match_records = []
        # print(STAFF_DATA[column])
        for index, val in enumerate(STAFF_DATA[column]):  # "age":[22,44,55]

            if float(val) > float(condition_val):
                # print("match",val)# 匹配上
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                match_records.append(record)

        # print(match_records)
        return match_records

        # else:
        #     print("没", val, condition_val)

    # 小于
    def op_lt(column, condition_val):
        match_records = []
        # print(STAFF_DATA[column])
        for index, val in enumerate(STAFF_DATA[column]):  # "age":[22,44,55]

            if float(val) < float(condition_val):
                # print("match",val)# 匹配上
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                match_records.append(record)

        # print(match_records)
        return match_records

        # else:
        #     print("没", val, condition_val)

    # 等于
    def op_eq(column, condition_val):
        match_records = []
        # print(STAFF_DATA[column])
        for index, val in enumerate(STAFF_DATA[column]):  # "age":[22,44,55]

            if val == condition_val:
                # print("match",val)# 匹配上
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                match_records.append(record)

        # print(match_records)
        return match_records

    # 类似
    def op_like(column, condition_val):
        match_records = []
        # print(STAFF_DATA[column])
        for index, val in enumerate(STAFF_DATA[column]):  # "age":[22,44,55]

            if condition_val in val:
                # print("match",val)# 匹配上
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                match_records.append(record)

        # print(match_records)
        return match_records

    operators = {
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        'like': op_like,
    }
    for op_key, op_func in operators.items():

        # print("adfalskdjfla;sjkdf",op_key,op_func)
        if op_key in clause:
            # print("clause", clause)
            column, val = clause.split(op_key)
            matched_data = op_func(column.strip(), val.strip())
            # print(column.strip(),val.strip())
            # print(matched_data)
            # print_log(matched_data)
            return matched_data
            break
    else:
        print_log("语法错误:where条件只能支持[>,<,=,like]", "error")


def syntax_find(data_set, query_clause):
    '''
    解析查询语句，并从data_set中打印指定的列
    :param data_set:[['2', 'Jack Wang', '28', '13451024608', 'HR', '2015-01-07\n'], ['4', 'Mack Qiao', '44', '15653354208', 'Sales', '2016-02-01\n'], ['5', 'Rachel Chen', '23', '13351024606', 'IT', '2013-03-16\n'], ['10', 'Shanshan Du', '26', '13698424612', 'Operation', '2017-07-02']]
    :param query_clause: eg. find name,age from staff_table
    :return:
    '''

    filter_cols_tmp = query_clause.split("from")[0][4:].split(',')
    # print_log(filter_cols_tmp)
    filter_cols = [i.strip() for i in filter_cols_tmp]
    if '*' in filter_cols[0]:
        print(tabulate(data_set, headers=COLUMNS, tablefmt="grid"))
    else:
        # print(filter_cols)
        reformat_data_set = []
        for row in data_set:
            filtered_vals = []  # 把要打印的字段放入
            for col in filter_cols:
                col_index = COLUMNS.index(col)
                filtered_vals.append((row[col_index]))  # 拿到列的索引，依次取出纪录对应的索引的值
            # print(filtered_vals)
            reformat_data_set.append(filtered_vals)
        print("一共处理 %s 行，数据如下:" % len(reformat_data_set))
        # for r in reformat_data_set:
        #     print(r)
        print(tabulate(reformat_data_set, headers=filter_cols, tablefmt="grid"))


def syntax_delete(data_set, query_clause):
    # print(data_set)
    need_del=[]
    # print(STAFF_DATA)
    for i in range(len(data_set)):
        need_del.append(int(data_set[i][0])-1)
    # print(need_del)
    for x in COLUMNS:
        for i in need_del:
            # del STAFF_DATA[x][int(i)]
            del STAFF_DATA[x][i]
    print(STAFF_DATA)
    # for i in range(len(COLUMNS)):
    #     del STAFF_DATA[COLUMNS[i]]

    # print(STAFF_DATA)
    #     for i in need_del:
    #         STAFF_DATA.pop([x][i])
    # print(STAFF_DATA)


def syntax_update(data_set, query_clause):
    '''

    :param data_set: [['2', 'Jack Wang', '28', '13451024608', 'HR', '2015-01-07\n'], ['4', 'Mack Qiao', '44', '15653354208', 'Sales', '2016-02-01\n'], ['5', 'Rachel Chen', '23', '13351024606', 'IT', '2013-03-16\n'], ['10', 'Shanshan Du', '26', '13698424612', 'Operation', '2017-07-02']]
    :param query_clause: eg. update staff_table set age = 25
    :return:
    '''
    formula_raw = query_clause.split('set')
    if len(formula_raw) > 1:
        col_name, new_val = formula_raw[1].strip().split('=')
        # print(col_name,new_val)
        col_index = COLUMNS.index(col_name)
        # 循环data_set,取到每条纪录的ID，拿着这个ID到staff_data['id']里找对应的ID的索引
        # 拿到之后，用索引去staff_data['age']表里改对应索引的值
        print("dataset", data_set)
        for matched_row in data_set:
            staff_id = matched_row[0]
            staff_id_index = STAFF_DATA['id'].index(staff_id)
            STAFF_DATA[col_name][staff_id_index] = new_val
        print(STAFF_DATA)

        save_db()
        print_log("成功修改了%s条数据" % len(data_set))

    else:
        print_log("语法错误：未检测到set关键字！", "error")


def syntax_add(data_set, query_clause):
    col_data = query_clause.split("staff_table")[1].strip()

    last_index = int(data_set[-1:][0][0]) - 1
    new_id = last_index + 2
    # print(new_id)
    # add_data=[]
    add_data = col_data.split(',')
    add_data.insert(0, new_id)
    print(add_data)
    # data_set.append(add_data)
    # print(data_set)

    # print(STAFF_DATA)
    for i in range(len(COLUMNS)):
        STAFF_DATA[COLUMNS[i]].append(add_data[i])

    print(STAFF_DATA)


# 分析语句，并将语句拆分开
def synatx_parser(cmd):
    '''
    解析语句，并执行
    :param cmd:
    :return:
    '''

    syntax_list = {
        'find': syntax_find,
        'del': syntax_delete,
        'update': syntax_update,
        'add': syntax_add
    }
    # print(cmd)
    if cmd.split()[0] in ('find', 'add', 'del', 'update'):
        # 通过where进行拆分
        if 'where' in cmd:
            query_clause, where_clause = cmd.split("where")
            # print(query_clause, where_clause)
            # 跳转对条件进行处理
            # syntax_where(where_clause)
            matched_record = syntax_where(where_clause)

        else:
            matched_record = []
            # print(STAFF_DATA)
            for index, staff_id in enumerate(STAFF_DATA['id']):
                # print(index,staff_id)
                record = []
                for col in COLUMNS:
                    record.append((STAFF_DATA[col][index]))
                # print(record)
                matched_record.append(record)
            query_clause = cmd
        cmd_action = cmd.split()[0]
        if cmd_action in syntax_list:
            # print(syntax_list[cmd_action][matched_record,query_clause])

            syntax_list[cmd_action](matched_record, query_clause)
    else:
        print_log("语法错误:", "error")
        print("[find\\add\del\\update] [column1,..] from [staff_table] [where] [column] [>,...][condtion]")


# 主进程，用户输入查询语句，并持续执行
def main():
    '''
    让用户输入语句并执行
    :return:
    '''

    while True:
        cmd = input("[staff_db]\n").strip()
        # print('cmd',cmd)
        # cmd = "find name,age from staff_table where age > 22 "
        if not cmd: continue

        synatx_parser(cmd)


main()
