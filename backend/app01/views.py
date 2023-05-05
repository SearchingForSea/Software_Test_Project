import json
import re

from django.shortcuts import render
from django.http import HttpResponse
from .models import test
from django.core import serializers


# Create your views here.
def get_info(request):
    return HttpResponse("no")


def basic_info(request):
    if request.method == 'GET':
        # try:
        es_data = test.objects.all()
        return_es_data = serializers.serialize('json', es_data, ensure_ascii=False)
        print(return_es_data)
        return HttpResponse(return_es_data)
        # except:
        #     return HttpResponse('no')


node_name = ['data-node-04', 'data-node-05', 'data-node-06', 'master-data-01', 'master-data-02', 'master-data-03', 'data-node-07']
def distribute_node(request):
    if request.method == 'GET':
        final_list = []
        move_list = []
        list1 = list(test.objects.all())
        list2 = list(json.loads(serializers.serialize('json', list1, ensure_ascii=False)))
        list3 = []
        for i in list2:
            list3.append(i["fields"])

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
        if not redistribute_node_dfs(remain_list, redistribution_list, shard_length, 0, len(redistribution_list), final_list, move_list):
            return HttpResponse("无法分配")

        # for i in move_list:
        #     print(i)

        json_dict = json.dumps(move_list)
        return HttpResponse(json_dict)


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


def redistribute_node_dfs(remain_list, redistribution_list, shard_length,index_i, n, final_list, move_list):
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

            recorde_index(redistribution_list[i].get('index'), redistribution_list[i].get('shard'),redistribution_list[i].get('prirep'), redistribution_list[i].get('node'), j, move_list)
            if redistribute_node_dfs(remain_list,redistribution_list, shard_length, index_i + 1, n, final_list, move_list):
                return True
            remain_list[j].pop()
            move_list.pop()
    return False


def judge_common_index(list1, index):
    for item in list1:
        if item.get('index') == index:
            return True
    return False


def recorde_index(index, shard, prirep, source_node,dest_node, move_list):
    dest_node = node_name[dest_node]
    d = {'index': index, 'shard': shard, 'prirep':prirep, 'source_node':source_node, 'dest_node':dest_node}
    move_list.append(d)
