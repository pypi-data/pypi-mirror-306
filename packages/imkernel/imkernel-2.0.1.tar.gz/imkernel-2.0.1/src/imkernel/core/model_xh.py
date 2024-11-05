import os
import time
from venv import logger

import numpy as np
import pandas as pd
from treelib import Tree

from imkernel.core import get_algorithm_by_path
from imkernel.core.utils import remove_empty_members


def build_tree(supname, name, subname=None, sub_subname=None):
    """
    根据给定的树状数据结构，构建一棵树。

    参数:
    - supname: 根节点的名称
    - name: 二级节点的列表（每个子列表是一级节点的直接子节点）
    - subname: 三级节点的列表（可选）
    - sub_subname: 四级节点的列表（可选）

    返回:
    - tree: 构建完成的树
    """
    # 创建树并添加根节点，id和tag相同
    tree = Tree()
    tree.create_node(tag=supname, identifier=supname)

    # 遍历 name 列表并添加节点
    for idx, second_level_list in enumerate(name):
        # 创建二级节点，id为"根节点tag+二级节点tag"
        second_level_tag = second_level_list[0]
        second_level_id = f"{supname}@{second_level_tag}"
        tree.create_node(tag=second_level_tag, identifier=second_level_id, parent=supname)

        # 如果 subname 存在，则创建三级节点
        if subname:
            for third_level in subname[idx]:
                # 三级节点，id为"二级节点tag+三级节点tag"
                third_level_id = f"{second_level_tag}@{third_level}"
                tree.create_node(tag=third_level, identifier=third_level_id, parent=second_level_id)

                # 如果 sub_subname 存在，则创建四级节点
                if sub_subname:
                    for fourth_level in sub_subname[idx][subname[idx].index(third_level)]:
                        # 四级节点，id为"三级节点tag+四级节点tag"
                        fourth_level_id = f"{third_level}@{fourth_level}"
                        tree.create_node(tag=fourth_level, identifier=fourth_level_id, parent=third_level_id)

    return tree


# 方法：根据索引名称和列名添加值
def add_value(df, index_name, column_name, value):
    """
    根据索引名称和列名，为多级索引的 DataFrame 添加值。

    参数:
    df: pandas DataFrame，具有多级索引
    index_name: 要匹配的索引名称（针对 level_4）
    column_name: 要修改的列名
    value: 要添加的值
    """
    # 找到符合 index_name 的行，并在指定列中添加值
    df.loc[pd.IndexSlice[:, :, :, index_name], column_name] = value


# 将 MultiIndex DataFrame 转换为树的方法
def df_to_tree(df):
    # 创建根节点
    supname = "root"
    tree = Tree()
    tree.create_node(tag=supname, identifier=supname)

    # 遍历 DataFrame 的 MultiIndex
    for index, row in df.iterrows():
        current_parent = supname  # 从根节点开始
        for level, level_name in enumerate(index):
            # 跳过 None 或 NaN 的值
            if level_name is None or (isinstance(level_name, float) and np.isnan(level_name)):
                continue

            # 定义节点的 id 和 tag
            current_id = f"{current_parent}@{level_name}"
            if not tree.contains(current_id):
                tree.create_node(tag=level_name, identifier=current_id, parent=current_parent)
            current_parent = current_id  # 将当前节点设为下一级的父节点

        # 将行的所有值作为叶子节点添加
        for col, value in row.items():
            leaf_id = f"{current_parent}@{col}"
            if not tree.contains(leaf_id):
                tree.create_node(tag=f"{col}: {value}", identifier=leaf_id, parent=current_parent)

    return tree


def assign_results(element_df, element_idx, format_result):
    if not isinstance(format_result, (list, tuple)):
        format_result = [format_result]

    existing_output_cols = [col for col in element_df.columns if col.startswith('output')]
    existing_output_cols.sort()

    if not existing_output_cols:
        logger.error("DataFrame中没有output列")
        return element_df

    # 调整结果长度
    if len(format_result) > len(existing_output_cols):
        logger.warning(f"结果数量({len(format_result)})超过DataFrame的output列数({len(existing_output_cols)})，将截断多余的结果")
        format_result = format_result[:len(existing_output_cols)]
    elif len(format_result) < len(existing_output_cols):
        logger.warning(f"结果数量({len(format_result)})少于DataFrame的output列数({len(existing_output_cols)})，将用None补充")
        format_result = format_result + [None] * (len(existing_output_cols) - len(format_result))

    try:
        # 获取实际的索引位置
        index_position = element_df[element_idx].index[0]

        # 为每个列单独赋值
        for col, value in zip(existing_output_cols, format_result):
            element_df.at[index_position, col] = value

    except Exception as e:
        logger.error(f"赋值失败: {str(e)}")
        logger.error(f"DataFrame形状: {element_df.shape}")
        logger.error(f"选中的行数: {element_idx.sum()}")
        logger.error(f"现有output列: {existing_output_cols}")

    return element_df


def run(method_df, element_df, method_name):
    # 在第4级索引中查找方法名
    method_idx = method_df.index.get_level_values(3) == method_name
    method_row = method_df[method_idx]
    # 检查行数
    if len(method_row) == 0:
        raise ValueError(f"未找到方法: {method_name}")
    elif len(method_row) > 1:
        raise ValueError(f"找到多个匹配的方法 {method_name}，共 {len(method_row)} 条记录")
    element_idx = element_df.index.get_level_values(3) == method_name
    element_row = element_df[element_idx]
    # 检查行数
    if len(method_row) == 0:
        raise ValueError(f"未找到方法: {method_name}")
    elif len(method_row) > 1:
        raise ValueError(f"找到多个匹配的方法 {method_name}，共 {len(method_row)} 条记录")
    # 字典
    method_row_dict = method_row.to_dict('records')[0]
    element_row_dict = element_row.to_dict('records')[0]
    function = method_row_dict['function']
    input_1 = method_row_dict['input1']
    input_2 = method_row_dict['input2']
    output_1 = method_row_dict['output1']
    output_2 = method_row_dict['output2']
    input_1_data = element_row_dict['input1']
    input_2_data = element_row_dict['input2']
    output_1_data = element_row_dict['output1']
    output_2_data = element_row_dict['output2']
    input_data_list = [input_1_data, input_2_data]
    # 分割py路径，函数名称
    method_body, method_name = os.path.split(function)
    if not method_body or not method_name:
        raise Exception("方法体/方法获取失败")

    print(f"方法体：{method_body}，方法：{method_name}")
    print(f"参数：{input_1}{input_2}")
    print(f"参数值：{input_data_list}")

    print(f"尝试导入方法体")
    # 获取算法
    function = get_algorithm_by_path(method_body, method_name)
    if not function:
        raise Exception(f"未能导入{method_name}")
    print(f"成功导入算法: {method_name}")
    format_input = remove_empty_members(input_data_list)
    print(f"输入：{format_input}")
    # 开始计时
    start_time = time.time()
    format_result = function(*format_input)

    # 结束计时
    end_time = time.time()

    element_df = assign_results(element_df, element_idx, format_result)
    # 计算耗时
    execution_time = end_time - start_time
    print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
    # element_df.loc[element_idx, ['output1', 'output2']] = [output_1_data, output_2_data]
