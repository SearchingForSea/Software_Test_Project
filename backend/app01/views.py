import json
import re
import pandas as pd
import os

from django.shortcuts import render
from django.http import HttpResponse
from .models import test
from django.core import serializers

# 第一题返回函数
def basic_info(request):
    if request.method == 'GET':
        return_es_data = json.dumps(get_input())
        return HttpResponse(return_es_data)


# 第二问
node_name = ['data-node-04', 'data-node-05', 'data-node-06', 'master-data-01', 'master-data-02', 'master-data-03',
             'data-node-07']
def distribute_node(request):
    if request.method == 'GET':
        final_list = []
        move_list = []
        # list1 = list(test.objects.all())
        # list2 = list(json.loads(serializers.serialize('json', list1, ensure_ascii=False)))
        # list3 = []
        # for i in list2:
        #     list3.append(i["fields"])
        list3 = get_input()
        # 格式化store字段中的信息
        transfer_data_format(list3)

        # 按照节点名称排序
        list4 = sorted(list3, key=lambda keys: keys.get('node'), reverse=False)

        # 计算每个节点的分片数量
        shard_length = len(list4)
        if shard_length % 7 != 0:
            shard_length = shard_length // 7 + 1
        else:
            shard_length = shard_length // 7

        # 将分片分裂成二维数组，每一维的节点名称相同
        list5 = split_list(list4)

        # 获取需要重新分配和剩下的分片
        [remain_list, redistribution_list] = scan_redistributive_node(list5, shard_length)
        remain_list.append([])

        # 重新分配
        if not redistribute_node_dfs(remain_list, redistribution_list, shard_length, 0, len(redistribution_list),
                                     final_list, move_list):
            return HttpResponse("无法分配")

        json_dict = json.dumps(move_list)
        return HttpResponse(json_dict)

def get_input():
    file_path = os.path.abspath(os.path.dirname(__file__)) + str("\cluster.xlsx")
    vm_data = pd.read_excel(io=file_path, names=None)
    vm_data = vm_data.values.tolist()
    move_list = []
    for i in vm_data:
        recorde_index_1(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], move_list)
    return move_list


def split_list(list1):
    rt = []
    n = 0
    for i in range(len(list1) - 1):
        if list1[i].get('node') != list1[i + 1].get('node'):
            rt.append(list1[n: i + 1])
            n = i + 1
    rt.append(list1[n:])
    return rt


def scan_redistributive_node(list1, shard_length):
    redistribution_list = []
    remain_list = []
    for item in list1:
        # 每一维度的数组，安照store排序
        list2 = sorted(item, key=lambda i: int(re.match(r'(\d+)', i.get('store')).group()), reverse=False)

        # 接收剩下的不需要重新排序的分片列表
        remain_list.append(scan_index(list2, redistribution_list, shard_length))
    return [remain_list, redistribution_list]


# 数据格式转化，将gb数据转化成mb
def transfer_data_format(list1):
    for item in list1:
        str1 = item.get('store')[-2:-1]
        if str1 == 'g':
            num = float(item.get('store')[0:-2]) * 1024
            str2 = str(num) + 'mb'
            item['store'] = str2


def scan_index(list1, redistribution_list, shard_length):
    remain_list = []
    for i in range(len(list1)):
        bo = False
        for j in range(i + 1, len(list1)):
            if list1[i].get('index') == list1[j].get('index'):
                redistribution_list.append(list1[i])
                bo = True
                break
        if not bo:
            if len(remain_list) < shard_length:
                remain_list.append(list1[i])
            else:
                redistribution_list.append(list1[i])
    return remain_list


def redistribute_node_dfs(remain_list, redistribution_list, shard_length, index_i, n, final_list, move_list):
    if index_i == n:
        final_list = remain_list
        return True
    for i in range(index_i, len(redistribution_list)):
        for j in range(len(remain_list) - 1, -1, -1):
            if len(remain_list[j]) >= shard_length:
                continue
            # 判断每一个节点中是否有相同的索引
            bo = judge_common_index(remain_list[j], redistribution_list[i].get('index'))
            if bo:
                continue
            remain_list[j].append(redistribution_list[i])

            recorde_index(redistribution_list[i].get('index'), redistribution_list[i].get('shard'),
                          redistribution_list[i].get('prirep'), redistribution_list[i].get('node'), j, move_list)
            if redistribute_node_dfs(remain_list, redistribution_list, shard_length, index_i + 1, n, final_list,
                                     move_list):
                return True
            remain_list[j].pop()
            move_list.pop()
    return False


def judge_common_index(list1, index):
    for item in list1:
        if item.get('index') == index:
            return True
    return False





# 第三问，分配虚拟机
def calculate_weight_1(vm, BM_using):
    a, b, c = 1,1,1
    if vm[7] > vm[8]:
        a += 1
    else:
        b += 1

    if vm[7] > vm[9]:
        a += 1
    else:
        c += 1

    if vm[8] > vm[9]:
        b += 1
    else:
        c += 1

    a, b, c = a / 6, b / 6, c / 6

    for item in BM_using:
        weight = item[4] * a + item[5] * b + item[6] * c
        if weight == float(0):
            item[8] = 0.0
        else:
            item[8] = weight

def calculate_weight_2(vm, bm_using):
    for bm in bm_using:
        bm[8] = vm[7] * bm[4] + vm[8] * bm[5] + vm[9] * bm[6] / (bm[4] + bm[5] + bm[6])

def manage_resource(request):
    if request.method == 'GET':

        # 获取虚拟机数据
        file_path = os.path.abspath(os.path.dirname(__file__)) + str("\BM和VM机器信息明细表.xlsx")
        vm_data = pd.read_excel(io=file_path, names=None, sheet_name='虚拟机VM')
        vm_data = vm_data.values.tolist()
        vm_data = sorted(vm_data, key=lambda x: x[10], reverse=True)

        # 获取物理机数据
        file_path = os.path.abspath(os.path.dirname(__file__)) + str("\BM和VM机器信息明细表.xlsx")
        bm_data = pd.read_excel(io=file_path, names=None, sheet_name='物理机BM')
        bm_data = bm_data.values.tolist()
        for bm in bm_data:
            bm[3] = bm[3] * 1024
            bm.append([])

        vm_sum_store = vm_data[0][4]
        vm_sum_cpu = vm_data[0][5]
        vm_sum_memory = vm_data[0][6]
        bm_sum_store = 0
        bm_sum_cpu = 0
        bm_sum_memory = 0
        first_time_bm_num = 0
        for i in range(len(bm_data)):
            bm_sum_store += bm_data[i][1]
            bm_sum_cpu += bm_data[i][2]
            bm_sum_memory += bm_data[i][3]
            if bm_sum_store >= vm_sum_store and bm_sum_cpu >= vm_sum_cpu and bm_sum_memory >= vm_sum_memory:
                first_time_bm_num = i + 1
                break

        bm_using = []
        for vm in vm_data:
            have_move = False
            max_index = max(enumerate(vm[7:10]), key=lambda x: x[1])[0] + 1

            if len(bm_using) == 0:
                for i in range(first_time_bm_num):
                    bm_using.append(bm_data[i])
                bm_data = bm_data[first_time_bm_num:]

                bm_using[0][1] -= vm[1]
                bm_using[0][2] -= vm[2]
                bm_using[0][3] -= vm[3]
                bm_using[0][4] = bm_using[0][1] / 12516
                bm_using[0][5] = bm_using[0][2] / 120
                bm_using[0][6] = bm_using[0][3] / (512 * 1024)
                bm_using[0][7] = (bm_using[0][4] + bm_using[0][5] + bm_using[0][6]) / 3
                bm_using[0][9].append(vm[0])
            else:
                # 一种算法
                # calculate_weight_2(vm, bm_using)
                # 最合理算法
                calculate_weight_1(vm, bm_using)

                bm_using = sorted(bm_using, key=lambda x: x[8], reverse=True)

                # 其余算法
                # calculate_weight_1(vm, bm_using)
                # bm_using = sorted(bm_using, key=lambda x: x[8], reverse=True)
                # weight = [1, 1, 1]
                # coefficient = weight[max_index-1]
                # bm_using = sorted(bm_using, key=lambda x: (x[max_index + 3]*coefficient / (x[4] + x[5] + x[6])))
                # bm_using = sorted(bm_using, key=lambda x: (x[max_index+3]), reverse=True)

                is_add = False
                for bm in bm_using:
                    if vm[1] <= bm[1] and vm[2] <= bm[2] and vm[3] <= bm[3]:
                        bm[1] -= vm[1]
                        bm[2] -= vm[2]
                        bm[3] -= vm[3]
                        bm[4] = bm[1] / 12516
                        bm[5] = bm[2] / 120
                        bm[6] = bm[3] / (512 * 1024)
                        bm[7] = (bm[4] + bm[5] + bm[6]) / 3
                        bm[9].append(vm[0])
                        have_move = True
                        break
                if not have_move:
                    if len(bm_data) == 0:
                        return HttpResponse("物理机不足，分配失败")
                    else:
                        is_add = True
                        bm_using.append(bm_data[0])
                        bm_data = bm_data[1:]
                        bm_using[len(bm_using) - 1][1] -= vm[1]
                        bm_using[len(bm_using) - 1][2] -= vm[2]
                        bm_using[len(bm_using) - 1][3] -= vm[3]
                        bm_using[len(bm_using) - 1][4] = bm_using[len(bm_using) - 1][1] / 12516
                        bm_using[len(bm_using) - 1][5] = bm_using[len(bm_using) - 1][2] / 120
                        bm_using[len(bm_using) - 1][6] = bm_using[len(bm_using) - 1][3] / (512 * 1024)
                        bm_using[len(bm_using) - 1][7] = (bm_using[len(bm_using) - 1][4] + bm_using[len(bm_using) - 1][5] + bm_using[len(bm_using) - 1][6]) / 3
                        bm_using[len(bm_using) - 1][9].append(vm[0])

        return_bm_data = []
        avg_rate = 0
        bm_using = sorted(bm_using, key=lambda x: x[7])
        op_len = 0
        if is_add:
            op_len = len(bm_using) - 1
        else:
            op_len = len(bm_using)

        for i in range(op_len):
            avg_rate += (1 - bm_using[i][7])
        avg_rate = avg_rate / op_len

        if len(bm_data) != 0:
            for i in range(len(bm_data)):
                bm_using.append(bm_data[i])
        for bm in bm_using:
            transform_bm_data(bm[0], bm[1], bm[2], bm[3], bm[4], bm[5], bm[6], bm[7], bm[9], return_bm_data)
        return_data = {
            'avg_rate': avg_rate,
            'return_bm_data': return_bm_data
        }
        return_data = json.dumps(return_data)
        return HttpResponse(return_data)

# 阶段信息
def recorde_index(index, shard, prirep, source_node, dest_node, move_list):
    dest_node = node_name[dest_node]
    d = {'index': index, 'shard': shard, 'prirep': prirep, 'source_node': source_node, 'dest_node': dest_node}
    move_list.append(d)

# 物理机数据格式转换：二维数组转字典
def transform_bm_data(name, store, cpu_num, memory, store_rate, cpu_rate, memory_rate, avg_rate, stored_vm, target_data):
    d = {'name': name, 'store': store, 'cpu_num': cpu_num, 'memory': memory, 'store_rate': store_rate,
         'cpu_rate': cpu_rate, 'memory_rate': memory_rate, 'avg_rate': avg_rate, 'stored_vm': stored_vm}
    target_data.append(d)

# 将列表元素转化成字典
def recorde_index_1(index, shard, prirep, state, docs, store, ip, node, move_list):
    d = {'index': index, 'shard': shard, 'prirep': prirep,"state": state, "docs":docs, "store":store, "ip":ip, "node":node }
    move_list.append(d)



