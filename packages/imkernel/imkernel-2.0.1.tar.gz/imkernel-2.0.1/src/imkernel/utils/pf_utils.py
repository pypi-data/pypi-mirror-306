import warnings

import pandas as pd
import treelib

from imkernel.utils import id_generator
# import id_generator


def _level_list(names, lvl):
    """
    规范输入列表层数
    :param names: 需要规范的输入
    :param lvl: 最终列表的嵌套层数: 1, 2, 3
    :return: names 规范好的输入列表
    """
    if names and (lvl == 1 or lvl == 2 or lvl == 3) and not isinstance(names, list):
        names = [names]
    if names and (lvl == 2 or lvl == 3) and not isinstance(names[0], list):
        names = [names]
    if names and (lvl == 3) and not isinstance(names[0][0], list):
        names = [names]
    return names


def _tree_sub_node(n_tree, n_id, n_tag, data):
    """
    在树tree中n_id节点的子节点查找是否存在名为n_tag的节点
    :param n_tree: 原树
    :param n_id: 节点的id
    :param n_tag: 需要查找的子节点的tag
    """
    c_nodes = n_tree.children(n_id)  # 子节点b
    # 若已存在直接返回节点
    for c_node in c_nodes:
        if c_node.tag == n_tag:
            return c_node
    # 不存在则新建节点并返回
    else:
        return n_tree.create_node(tag=n_tag, identifier=id_generator.idgen.next_id(),
                                  parent=n_id, data=data)


def find_node_by_tag(tree, tag: str):
    """
    通过节点的tag在树中查找
    :param tree: 寻找的tree
    :param tag: 需要寻找的节点tag名称
    """
    for node in tree.all_nodes():
        if node.tag == tag:
            return node
    else:
        print(f'未找到 {tag} 节点。')
        return None


def tree_sys(tree, supsys=None, sys=None, subsys=None) -> treelib.Tree:
    """
    创建系统树
    :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
    :param supsys: 总系统列表（一级节点）
    :param sys: 系统列表（二级节点）
    :param subsys: 子系统列表（三级节点）
    :return: tree(系统树)
    """
    # 没有树则新建
    if isinstance(tree, str):
        tree_name = tree
        tree = treelib.Tree()
        tree.create_node(tree_name, id_generator.idgen.next_id(), data='root')  # 创建根节点
    if isinstance(tree, treelib.Tree):
        # 遍历三个名称列表进行节点添加
        if supsys:
            names1 = _level_list(supsys, 1)  # 规范列表层数
            for i, name1 in enumerate(names1):
                node1 = _tree_sub_node(tree, tree.root, name1, "supermodel")
                if sys:
                    names2 = _level_list(sys, 2)  # 规范列表层数
                    if i >= len(names2):  # 如果子名称长度小于上一级名称则跳过
                        continue
                    for j, name2 in enumerate(names2[i]):
                        node2 = _tree_sub_node(tree, node1.identifier, name2, "model")
                        if subsys:
                            names3 = _level_list(subsys, 3)  # 规范列表层数
                            if j >= len(names3):  # 如果子名称长度小于上一级名称则跳过
                                continue
                            for k, name3 in enumerate(names3[i][j]):
                                _tree_sub_node(tree, node2.identifier, name3, "subsystem")
    else:
        print(f'tree的类型错误，创建失败：{type(tree)}')
        return None
    return tree


# def tree_ele(tree, dimension: str, ele: str, eleid: str, eleprop: str,
#              elevar=None) -> treelib.Tree:
#     """
#     创建单元树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param dimension: person(人员), machine(机器), product(产品)
#     :param ele: 单元名（一级节点）
#     :param eleid: 单元的名称（二级节点）
#     :param eleprop: 单元的特性（二级节点）
#     :param elevar: 单元的特性变量（三级节点）
#     :return: tree（单元树）
#     """
#     # 没有树则新建
#     if isinstance(tree, str):
#         tree_name = f'{tree}_{dimension}'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data=dimension)  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         ele_node = _tree_sub_node(tree, tree.root, ele, f'{dimension}_name')  # ele（一级节点）
#         id_node = _tree_sub_node(tree, ele_node.identifier, eleid, f'{dimension}_id')  # 创建单元的名称（二级节点）
#         pr_node = _tree_sub_node(tree, ele_node.identifier, eleprop, f'{dimension}_prop')  # 创建单元的特性（二级节点）
#         elevar = _level_list(elevar, 1)  # 规范列表层数
#         for var in elevar:
#             var_node = _tree_sub_node(tree, pr_node.identifier, var, f'{dimension}_var')  # 特性的值名称（三级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


# def tree_method(tree, method_name: str,
#                 in_param=None, out_param=None,
#                 in_sub_param=None, out_sub_param=None) -> treelib.Tree:
#     """
#     创建方法树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param method_name: 方法名称（一级节点）
#     :param in_param: 方法输入参数（二级节点）
#     :param in_sub_param: 方法输入子参数（三级节点）
#     :param out_param: 方法输出参数（二级节点）
#     :param out_sub_param: 方法输出子参数（三级节点）
#     :return: tree（方法树）
#     """
#     # 没有树则新建
#     if isinstance(tree, str):
#         tree_name = f'{tree}_method'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data='method')  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         m_node = _tree_sub_node(tree, tree.root, method_name, 'method_name')  # 方法节点（一级节点）
#         # s_node = tree.create_node('状态操作', f'method_state_operate {m_num}', m_node.identifier)
#         # tree.create_node('状态', f'method_state {m_num}', s_node.identifier)
#         # tree.create_node('操作', f'method_operate {m_num}', s_node.identifier)
#         # 输入
#         i_node = _tree_sub_node(tree, m_node.identifier, "输入", 'method_in_param')  # 输入节点（二级节点）
#         in_param = _level_list(in_param, 1)  # 规范列表层数
#         for i, p1 in enumerate(in_param):
#             p1_node = _tree_sub_node(tree, i_node.identifier, p1, data='method_in_sub_param')  # 输入分类节点（三级节点）
#             if in_sub_param:
#                 in_params = _level_list(in_sub_param, 2)  # 规范列表层数
#                 if i >= len(in_params):
#                     continue
#                 for j, p2 in enumerate(in_params[i]):
#                     _tree_sub_node(tree, p1_node.identifier, p2, data='method_in_param_var')  # 输入值节点（四级节点）
#         # 输出
#         o_node = _tree_sub_node(tree, m_node.identifier, "输出", 'method_out_param')  # 输出节点（二级节点）
#         out_param = _level_list(out_param, 1)  # 规范列表层数
#         for i, p1 in enumerate(out_param):
#             p1_node = _tree_sub_node(tree, o_node.identifier, p1, data='method_out_sub_param')  # 输出分类节点（三级节点）
#             if out_sub_param:
#                 out_params = _level_list(out_sub_param, 2)  # 规范列表层数
#                 if i >= len(out_params):
#                     continue
#                 for j, p2 in enumerate(out_params[i]):
#                     _tree_sub_node(tree, p1_node.identifier, p2, data='method_out_param_var')  # 输出值节点（四级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


# def tree_procedure(tree, name: str, subname:str,
#                    prop=None, variable=None) -> treelib.Tree:
#     """
#     创建流程树
#     :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
#     :param name: 流程名称（一级节点）
#     :param subname: 子名称（二级节点）
#     :param prop: 特征名称 list（三级节点）
#     :param variable: 特征值 list（四级节点）
#     :return: tree（流程树）
#     """
#     if isinstance(tree, str):
#         tree_name = f'{tree}_procedure'
#         tree = treelib.Tree()
#         tree.create_node(tree_name, id_generator.idgen.next_id(), data='procedure')  # 创建根节点
#     if isinstance(tree, treelib.Tree):
#         # 创建节点，已有则不新建，没有则新建
#         p_node = _tree_sub_node(tree, tree.root, name, "procedure_name")  # 流程名称（一级节点）
#         s_node = _tree_sub_node(tree, p_node.identifier, subname, "procedure_sub")  # 流程子名称（二级节点）
#         props = _level_list(prop, 1)  # 规范列表层数
#         for i, prop in enumerate(props):
#             prop_node = _tree_sub_node(tree, s_node.identifier, prop, data='procedure_sub_param')  # 特性节点（三级节点）
#             if variable:
#                 variables = _level_list(variable, 2)  # 规范列表层数
#                 if i >= len(variables):
#                     continue
#                 for j, var in enumerate(variables[i]):
#                     _tree_sub_node(tree, prop_node.identifier, var, data='procedure_sub_var')  # 变量节点（四级节点）
#     else:
#         print(f'tree的类型错误，创建失败：{type(tree)}')
#         return None
#     return tree


def tree_dimension(tree, dimension: str, name: str, item=None, prop=None, variable=None) -> treelib.Tree:
    """
    创建维度子树
    :param tree: 传入tree表示向其中添加分支，传入str表示新建tree（根节点）
    :param dimension: 维度：person(人员), machine(机器), product(产品), method(方法), procedure(流程)
    :param name: 名称（一级节点）
    :param item: 子名称 list（二级节点）
    :param prop: 特性名称 list（三级节点）
    :param variable: 特性变量名称 list（四级节点）
    :return: tree（维度子树）
    """
    if isinstance(tree, str):
        tree_name = f"{tree}_{dimension}"
        tree = treelib.Tree()
        tree.create_node(tree_name, id_generator.idgen.next_id(), data=f"{dimension}")  # 创建根节点
    if isinstance(tree, treelib.Tree):
        # 创建固定需求节点
        name_node = _tree_sub_node(tree, tree.root, name, f"{dimension}_name")  # 名称（一级节点）
        if dimension != "method":
            id_node = _tree_sub_node(tree, name_node.identifier, "编号", data=f"{dimension}_item")  # item 编号，即id
        elif dimension == "method":
            mt_node = _tree_sub_node(tree, name_node.identifier, "方法体", data=f"{dimension}_item")  # item 方法：方法体
        if dimension == "procedure":
            st_node = _tree_sub_node(tree, name_node.identifier, "状态", data=f"{dimension}_item")  # item 流程：状态
            _tree_sub_node(tree, st_node.identifier, "状态", data=f"{dimension}_item")  # prop 状态：状态
            _tree_sub_node(tree, st_node.identifier, "起止时间", data=f"{dimension}_item")  # prop 状态：起止时间
        # 遍历三个名称列表进行节点添加
        if item:
            items = _level_list(item, 1)  # 规范列表层数
            for i, it in enumerate(items):
                item_node = _tree_sub_node(tree, name_node.identifier, it, data=f"{dimension}_item")  # 子名称（二级节点）
                if prop:
                    props = _level_list(prop, 2)  # 规范列表层数
                    if i >= len(props):  # 如果子名称长度小于上一级名称则跳过
                        continue
                    for j, pr in enumerate(props[i]):
                        prop_node = _tree_sub_node(tree, item_node.identifier, pr, data=f"{dimension}_property")  # 特性节点（三级节点）
                        if variable:
                            variables = _level_list(variable, 3)  # 规范列表层数
                            if j >= len(variables):  # 如果子名称长度小于上一级名称则跳过
                                continue
                            for k, var in enumerate(variables[j][i]):
                                _tree_sub_node(tree, prop_node.identifier, var, data=f"{dimension}_variable")  # 特性变量节点（四级节点）
    else:
        print(f'tree的类型错误，创建失败：{type(tree)}')
        return None
    return tree


def combine_sys_dimension(system_tree, root_ele: str, sub_trees) -> None:
    """
    将子树合并到系统树下的root_ele对应节点
    :param system_tree: 需要合并的系统树
    :param root_ele: 系统树下的指定节点tag
    :param sub_trees: 子树列表
    :return: None
    """
    def find_node(tree, tag):
        """通过节点的tag在树中查找"""
        for tag_n in tree.all_nodes():
            if tag_n.tag == tag:
                return tag_n
        else:
            return None
    if not isinstance(sub_trees, list):
        sub_trees = [sub_trees]
    # 查找子树需要合并到系统树的指定节点
    node = find_node(system_tree, root_ele)
    if node:
        from treelib.exceptions import NodeIDAbsentError
        for sub_tree in sub_trees:
            if sub_tree:
                try:
                    system_tree.remove_node(sub_tree.all_nodes()[0].identifier)
                except NodeIDAbsentError:
                    pass
                system_tree.paste(node.identifier, sub_tree, deep=False)
    else:
        print('合并失败，请查看树中是否存在' + root_ele + '这个节点。')


def tree_to_df(tree, columns_name: str, columns_num: int, index_levels=None) -> pd.DataFrame:
    """
    将树转换为dataframe，所有节点作为多级索引
    :param tree: 需要转换的树
    :param columns_name: 列名
    :param columns_num: 列数
    :param index_levels: 索引的名称
    :return: 返回转换的dataframe
    """
    idx_len = tree.depth()  # 树的深度
    idx_tuples = []  # 索引根据元组生成
    idx_names = index_levels if index_levels else [f'{i + 1}级' for i in range(idx_len + 1)]  # 索引的名称
    # 生成多级索引的元组
    for path in tree.paths_to_leaves():
        tags = []
        for nid in path:
            tags.append(tree.get_node(nid).tag)
        tags += ['None'] * (idx_len - len(path[:-1]))  # 补充缺少的索引名
        idx_tuples.append(tuple(tags))
    # 创建多级行索引
    index = pd.MultiIndex.from_tuples(
        tuples=idx_tuples,
        names=idx_names
    )
    df = pd.DataFrame(index=index)
    for n in range(columns_num):
        df[f'{columns_name} {n + 1}'] = None
    return df


def dimension_data_value(df, name: str, item: str, prop: str, variable: list) -> None:
    """
    df数据输入
    :param df: 需要进行数据输入的df
    :param name: 名称（一级节点）
    :param item: 子名称 list（二级节点）
    :param prop: 特性名称 list（三级节点）
    :param variable: 特性变量名称 list（四级节点）
    :return: None
    """
    # 忽略多级索引可能导致的性能警告
    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
    # 系统名称
    sysname = df.index[0][0]
    # 列满需要添加新列之后进行插入，标记哪一列没有值
    tmp = len(df.columns) + 1  # 默认新一列
    indexes = [df.index.get_level_values(0)[0], name, item, prop]  # [sysname, name, item, prop]
    # 查找是否有没有值的列
    for i, col in enumerate(df.columns):
        if df.loc[tuple(indexes), col].isnull().all():
            tmp = i + 1  # i+1列没有值或需要进行覆盖操作
            break
    # 插值
    col_name = f'id/value {tmp}'
    for idx, var in zip(df.loc[tuple(indexes)].index, variable):
        df.loc[tuple(indexes + [idx]), col_name] = var


# def element_data_value(df, dimension: str, root_ele: str, ele: str, eleid: str, elevar: list) -> None:
#     """
#     向传入的单元df进行输入操作
#     :param df: 单元df对象
#     :param dimension: 维度 person(人员), machine(机器), product(产品),
#     :param root_ele: 树的根节点名称，系统树中的项目名称
#     :param ele: 单元树中的一级节点，df中的一级索引
#     :param eleid: 二级节点'名称'的值
#     :param elevar: 二级节点'特征'对应三级节点对应的值
#     :return: None
#     """
#     # 列满需要添加新列之后进行插入，标记哪一列没有值
#     tmp = len(df.columns) + 1  # 默认新一列
#     root_name = f'{root_ele}_{dimension}'
#     # 忽略多级索引可能导致的性能警告
#     warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
#     # 查找是否有没有值的列
#     for i, col in enumerate(df.columns):
#         if (df.loc[(root_name, ele, '名称'), col].isnull().all() or
#                 (df.loc[root_name, ele, '名称'][col] == eleid).all()):
#             tmp = i + 1  # i+1列没有值或需要进行覆盖操作
#             break
#     # 插值
#     col_name = f'{dimension} {tmp}'
#     df.loc[(root_name, ele, '名称'), col_name] = eleid
#     for idx, var in zip(df.loc[root_name, ele, '特性'].index, elevar):
#         df.loc[(root_name, ele, '特性', idx), col_name] = var
#
#
# def method_data_value(df, root_method: str, method_name: str, method_prop: str,
#                       sub_method_prop: str, method_vars: list) -> None:
#     """
#     向传入的方法df进行输入操作
#     :param df: 方法df
#     :param root_method: 方法所属
#     :param method_name: 方法名称
#     :param method_prop: 方法属性，输入输出
#     :param sub_method_prop: 方法子属性，第二级输入输出
#     :param method_vars: 属性的具体值
#     :return: None
#     """
#     # 列满需要添加新列之后进行插入，标记哪一列没有值
#     tmp = len(df.columns) + 1  # 默认新一列
#     root_name = f'{root_method}_method'
#     # 忽略多级索引可能导致的性能警告
#     warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
#     # indexes = [root_name, method_name, method_prop] if method_prop == '状态操作' else \
#     #     [root_name, method_name, method_prop, sub_method_prop]  # indexes
#     indexes = [root_name, method_name, method_prop, sub_method_prop]
#     # 查找是否有没有值的列
#     for i, col in enumerate(df.columns):
#         if df.loc[tuple(indexes), col].isnull().all():
#             tmp = i + 1  # i+1列没有值或需要进行覆盖操作
#             break
#     # 插值
#     col_name = f'method_value {tmp}'
#     # indexes = df.loc[tuple(indexes)].index
#     for idx, var in zip(df.loc[tuple(indexes)].index, method_vars):
#         # if method_prop == '状态操作':
#         #     idx = idx[0]
#         df.loc[tuple(indexes + [idx]), col_name] = var
#
#
# def procedure_data_value(df, name: str, subname: str, prop: str, prop_vars: list) -> None:
#     # 列满需要添加新列之后进行插入，标记哪一列没有值
#     tmp = len(df.columns) + 1  # 默认新一列
#     # 忽略多级索引可能导致的性能警告
#     warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
#     indexes = [df.index.get_level_values(0)[0], name, subname, prop]  # [sysname, name, subname, prop]
#     # 查找是否有没有值的列
#     for i, col in enumerate(df.columns):
#         if df.loc[tuple(indexes), col].isnull().all():
#             tmp = i + 1  # i+1列没有值或需要进行覆盖操作
#             break
#     # 插值
#     col_name = f'id/value {tmp}'
#     for idx, var in zip(df.loc[tuple(indexes)].index, prop_vars):
#         df.loc[tuple(indexes + [idx]), col_name] = var


if __name__ == '__main__':
    pass
    # 系统树
    system_tree = tree_sys(tree='insofsys',
                           supsys=['insoftest', 'insofrobot', 'insofaiam'],
                           sys=['DTIS_511', 'NDT_SNOTC'],
                           subsys=[])
    print(system_tree)
    system_tree = tree_sys(tree=system_tree,
                           supsys='insofrobot',
                           sys=['insofbend', 'insoflaser', 'insoftube'], )
    print(system_tree)
    system_tree = tree_sys(tree=system_tree,
                           supsys='insofaiam',
                           sys='insofmining')
    print(system_tree)

    # 人员机器产品树
    person_tree = tree_dimension(tree='DTIS_511', dimension='person', name='个人',
                                 item='特性', prop='属性',
                                 variable=['地址', '头像', '年龄', '性别', '手机'])
    print(person_tree)
    person_tree = tree_dimension(tree=person_tree, dimension='person', name='机构',
                                 item='特性', prop='属性',
                                 variable=['排序', '地址', '类型'])
    print(person_tree)
    person_tree = tree_dimension(tree=person_tree, dimension='person', name='职位', item='特性')
    person_tree = tree_dimension(tree=person_tree, dimension='person', name='角色', item='特性')
    person_tree = tree_dimension(tree=person_tree, dimension='person', name='账号', item='特性')
    print(person_tree)

    # 方法树
    method_tree = tree_dimension(tree='DTIS_511', dimension='method', name='型面生成',
                                 item=['输入', '输出'], prop=[['型线十一参数', '型面参数'], ['型线坐标']],
                                 variable=[[['Chord_Length', 'Upper_Angle', 'Upper_Max'], ['型线数量', '型线间距']], [[]]])
    print(method_tree)
    method_tree = tree_dimension(tree=method_tree, dimension='method', name='工艺设计', item=['输入', '输出'])
    print(method_tree)

    # 流程树
    procedure_tree = tree_dimension(tree='DTIS_511', dimension='procedure', name='试验人员组织',
                                    item='特性', prop=['一岗', '二岗'],
                                    variable=[[['力测量', '功放系统', '台体系统', '应变系统', '控制系统']], [['力测量', '混响室本体']]])
    print(procedure_tree)
    procedure_tree = tree_dimension(tree=procedure_tree, dimension='procedure', name='试验人员组织',
                                    item='特性', prop=['一岗', '二岗'],
                                    variable=[[[]], [['力测量', '功放系统']]])
    print(procedure_tree)

    # 合并树
    combine_sys_dimension(system_tree, 'DTIS_511', [person_tree, method_tree, procedure_tree])
    print(system_tree)

    # 人员机器设备树转df
    person_df = tree_to_df(person_tree, 'id/value', 6,
                           index_levels=['sysname', 'name', 'item', 'property', 'variable'])
    print(person_df)

    # 方法树转df
    method_df = tree_to_df(method_tree, 'id/value', 6,
                           index_levels=['sysname', 'name', 'item', 'property', 'variable'])
    print(method_df)

    # 流程树转df
    procedure_df = tree_to_df(procedure_tree, 'id/value', 6,
                           index_levels=['sysname', 'name', 'item', 'property', 'variable'])
    print(procedure_df)

    # df数据添加
    dimension_data_value(df=procedure_df, name='试验人员组织', item='特性', prop='一岗', variable=[1, 2, 3, 4, 5])
    print(procedure_df)
