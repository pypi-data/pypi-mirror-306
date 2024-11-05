import treelib
from loguru import logger
from treelib import Tree
from imkernel.utils.id_generator import idgen
from imkernel.core.treelib_utils import get_node_by_tag_and_data

LAYER_1 = "layer_1"
MODEL_NAME = "model_name"
LAYER_2 = "layer_2"
OBJECT_NAME = "object_name"
LAYER_3 = "layer_3"
PROP_NAME = "prop_name"
PROP_VARIABLE = "prop_variable"


def tree_to_list(tree):
    # 深度与类型的映射字典
    depth_type_map = {
        1: 'layer_1',
        2: 'model_name',
        3: 'layer_2',
        4: 'object_name',
        5: 'layer_3',
        6: 'prop_name',
        7: 'prop_variable'
    }

    result = []
    # 用于存储原始id到新id的映射
    id_mapping = {}

    def traverse(node_id, tree_id):
        node = tree.get_node(node_id)
        depth = tree.depth(node)

        # 为当前节点生成新id
        new_id = idgen.next_id()
        id_mapping[node.identifier] = new_id

        # 获取父节点的新id
        parent_node = tree.parent(node.identifier)
        new_parent_id = id_mapping.get(parent_node.identifier, 0) if parent_node else 0

        # 创建节点字典
        node_dict = {
            'id': new_id,
            'parentId': new_parent_id,
            'name': node.tag,
            'treeId': node.identifier,  # 使用原始treelib node的id
            'nodeType': depth_type_map.get(depth + 1, 'None')
        }
        result.append(node_dict)

        # 递归遍历子节点
        for child in tree.children(node_id):
            traverse(child.identifier, tree_id)

    # 从根节点开始遍历
    traverse(tree.root, 1)

    return result


if __name__ == '__main__':
    model_tree = Tree()
    model_tree.create_node('model', 'model')
    model_tree.create_node('DTIS_511', 'modelname 1', 'model')
    model_tree.create_node('insoftube', 'modelname 2', 'model')
    model_tree.create_node('insofaiam', 'modelname 3', 'model')
    print(model_tree)
    person_tree = Tree()
    person_tree.create_node('person', 'person')
    person_tree.create_node('机构', 'personname 1', 'person')
    person_tree.create_node('编号', 'personid 1', 'personname 1')
    person_tree.create_node('特性', 'personprop 1', 'personname 1')
    person_tree.create_node('属性', 'personpropname 1.1', 'personprop 1')
    person_tree.create_node('类型', 'personpropvar 1.1.1', 'personpropname 1.1')
    person_tree.create_node('级别', 'personpropvar 1.1.2', 'personpropname 1.1')
    person_tree.create_node('编码', 'personpropvar 1.1.3', 'personpropname 1.1')
    person_tree.create_node('排序', 'personpropvar 1.1.4', 'personpropname 1.1')
    person_tree.create_node('状态', 'personpropvar 1.1.5', 'personpropname 1.1')
    person_tree.create_node('职位', 'personname 2', 'person')
    person_tree.create_node('编号', 'personid 2', 'personname 2')
    person_tree.create_node('特性', 'personprop 2', 'personname 2')
    person_tree.create_node('个人', 'personname 3', 'person')
    person_tree.create_node('编号', 'personid 3', 'personname 3')
    person_tree.create_node('特性', 'personprop 3', 'personname 3')
    person_tree.create_node('属性', 'personpropname 3.1', 'personprop 3')
    person_tree.create_node('编号', 'personpropvar 3.1.1', 'personpropname 3.1')
    person_tree.create_node('资质', 'personpropvar 3.1.2', 'personpropname 3.1')
    person_tree.create_node('性别', 'personpropvar 3.1.3', 'personpropname 3.1')
    person_tree.create_node('年龄', 'personpropvar 3.1.4', 'personpropname 3.1')
    person_tree.create_node('地址', 'personpropvar 3.1.5', 'personpropname 3.1')
    person_tree.create_node('手机', 'personpropvar 3.1.6', 'personpropname 3.1')
    person_tree.create_node('昵称', 'personpropvar 3.1.7', 'personpropname 3.1')
    person_tree.create_node('头像', 'personpropvar 3.1.8', 'personpropname 3.1')
    person_tree.create_node('签名', 'personpropvar 3.1.9', 'personpropname 3.1')
    person_tree.create_node('角色', 'personname 4', 'person')
    person_tree.create_node('编号', 'personid 4', 'personname 4')
    person_tree.create_node('特性', 'personprop 4', 'personname 4')
    person_tree.create_node('账号', 'personname 5', 'person')
    person_tree.create_node('编号', 'personid 5', 'personname 5')
    person_tree.create_node('特性', 'personprop 5', 'personname 5')
    model_tree.paste('modelname 1', person_tree, deep=False)
    product_tree = Tree()
    product_tree.create_node('product', 'product')
    product_tree.create_node('试件', 'productname 1', 'product')
    product_tree.create_node('编号', 'productid 1', 'productname 1')
    product_tree.create_node('特性', 'productprop 1', 'productname 1')
    product_tree.create_node('属性', 'productpropname 1.1', 'productprop 1')
    product_tree.create_node('型号', 'productpropvar 1.1.1', 'productpropname 1.1')
    product_tree.create_node('平台', 'productpropvar 1.1.2', 'productpropname 1.1')
    product_tree.create_node('级别', 'productpropvar 1.1.3', 'productpropname 1.1')
    product_tree.create_node('研制阶段', 'productpropvar 1.1.4', 'productpropname 1.1')
    product_tree.create_node('测点', 'productname 2', 'product')
    product_tree.create_node('编号', 'productid 2', 'productname 2')
    product_tree.create_node('特性', 'productprop 2', 'productname 2')
    product_tree.create_node('属性', 'productpropname 2.1', 'productprop 2')
    product_tree.create_node('部件', 'productpropvar 2.1.1', 'productpropname 2.1')
    product_tree.create_node('通道号', 'productpropvar 2.1.2', 'productpropname 2.1')

    model_tree.paste('modelname 1', product_tree, deep=False)
    method_tree = Tree()
    method_tree.create_node('method', 'method')
    method_tree.create_node('型面生成', 'methodname 1', 'method')
    method_tree.create_node('方法体', 'method_body 1', 'methodname 1')
    method_tree.create_node('输入', 'input 1', 'methodname 1')
    method_tree.create_node('型线十一参数', 'inputname 1.1', 'input 1')
    method_tree.create_node('Chord_Length', 'inputvar 1.1.1', 'inputname 1.1')
    method_tree.create_node('Upper_Max_Width', 'inputvar 1.1.2', 'inputname 1.1')
    method_tree.create_node('Upper_Max_Width_Loc', 'inputvar 1.1.3', 'inputname 1.1')
    method_tree.create_node('Upper_Angle', 'inputvar 1.1.4', 'inputname 1.1')
    method_tree.create_node('Upper_tip_coeff', 'inputvar 1.1.5', 'inputname 1.1')
    method_tree.create_node('Upper_aft_part_shape', 'inputvar 1.1.6', 'inputname 1.1')
    method_tree.create_node('型面参数', 'inputname 1.2', 'input 1')
    method_tree.create_node('型线数量', 'inputvar 1.2.1', 'inputname 1.2')
    method_tree.create_node('型线间距', 'inputvar 1.2.2', 'inputname 1.2')
    method_tree.create_node('输出', 'output 1', 'methodname 1')
    method_tree.create_node('型线坐标', 'outputname 1.1', 'output 1')
    method_tree.create_node('工艺设计', 'methodname 2', 'method')
    method_tree.create_node('方法体', 'method_body 2', 'methodname 2')
    method_tree.create_node('输入', 'input 2', 'methodname 2')
    method_tree.create_node('输出', 'output 2', 'methodname 2')
    # print (method_tree)
    model_tree.paste('modelname 1', method_tree, deep=False)
    print(model_tree)
    procedure_tree = Tree()
    procedure_tree.create_node('procedure', 'procedure')
    #
    procedure_tree.create_node('试验任务定义', 'procedurename 1', 'procedure')
    procedure_tree.create_node('编号', 'procedureid 1', 'procedurename 1')
    procedure_tree.create_node('状态', 'procedurestate 1', 'procedurename 1')
    procedure_tree.create_node('状态', 'procedurestatevar 1.1', 'procedurestate 1')
    procedure_tree.create_node('起止时间', 'procedurestatevar 1.2', 'procedurestate 1')
    procedure_tree.create_node('特性', 'procedureprop 1', 'procedurename 1')
    procedure_tree.create_node('产品信息', 'procedurepropname 1.1', 'procedureprop 1')
    procedure_tree.create_node('型号', 'procedurepropvar 1.1.1', 'procedurepropname 1.1')
    procedure_tree.create_node('平台', 'procedurepropvar 1.1.2', 'procedurepropname 1.1')
    procedure_tree.create_node('级别', 'procedurepropvar 1.1.3', 'procedurepropname 1.1')
    procedure_tree.create_node('阶段', 'procedurepropvar 1.1.4', 'procedurepropname 1.1')
    procedure_tree.create_node('试验方向', 'procedurepropvar 1.1.5', 'procedurepropname 1.1')
    procedure_tree.create_node('机器信息', 'procedurepropname 1.2', 'procedureprop 1')
    procedure_tree.create_node('场地', 'procedurepropvar 1.2.1', 'procedurepropname 1.2')
    procedure_tree.create_node('设备', 'procedurepropvar 1.2.2', 'procedurepropname 1.2')
    procedure_tree.create_node('工装', 'procedurepropvar 1.2.3', 'procedurepropname 1.2')
    procedure_tree.create_node('人员信息', 'procedurepropname 1.3', 'procedureprop 1')
    procedure_tree.create_node('试验甲方', 'procedurepropvar 1.3.1', 'procedurepropname 1.3')
    procedure_tree.create_node('部负责人', 'procedurepropvar 1.3.2', 'procedurepropname 1.3')
    procedure_tree.create_node('室负责人', 'procedurepropvar 1.3.3', 'procedurepropname 1.3')
    procedure_tree.create_node('产保工程师', 'procedurepropvar 1.3.4', 'procedurepropname 1.3')
    #
    procedure_tree.create_node('试验人员组织', 'procedurename 2', 'procedure')
    procedure_tree.create_node('编号', 'procedureid 2', 'procedurename 2')
    procedure_tree.create_node('状态', 'procedurestate 2', 'procedurename 2')
    procedure_tree.create_node('状态', 'procedurestatevar 2.1', 'procedurestate 2')
    procedure_tree.create_node('起止时间', 'procedurestatevar 2.2', 'procedurestate 2')
    procedure_tree.create_node('特性', 'procedureprop 2', 'procedurename 2')
    procedure_tree.create_node('试验管理团队', 'procedurepropname 2.1', 'procedureprop 2')
    procedure_tree.create_node('技术指挥', 'procedurepropvar 2.1.1', 'procedurepropname 2.1')
    procedure_tree.create_node('技术副指挥', 'procedurepropvar 2.1.2', 'procedurepropname 2.1')
    procedure_tree.create_node('振动负责人', 'procedurepropvar 2.1.3', 'procedurepropname 2.1')
    procedure_tree.create_node('测量负责人', 'procedurepropvar 2.1.4', 'procedurepropname 2.1')
    procedure_tree.create_node('综合管理岗', 'procedurepropvar 2.1.5', 'procedurepropname 2.1')
    procedure_tree.create_node('试验操作团队一岗', 'procedurepropname 2.2', 'procedureprop 2')
    procedure_tree.create_node('应变系统', 'procedurepropvar 2.2.1', 'procedurepropname 2.2')
    procedure_tree.create_node('控制系统', 'procedurepropvar 2.2.2', 'procedurepropname 2.2')
    procedure_tree.create_node('混响室本体', 'procedurepropvar 2.2.3', 'procedurepropname 2.2')
    procedure_tree.create_node('功放系统', 'procedurepropvar 2.2.4', 'procedurepropname 2.2')
    procedure_tree.create_node('台体系统', 'procedurepropvar 2.2.5', 'procedurepropname 2.2')
    procedure_tree.create_node('测量系统', 'procedurepropvar 2.2.6', 'procedurepropname 2.2')
    procedure_tree.create_node('气源系统', 'procedurepropvar 2.2.7', 'procedurepropname 2.2')
    procedure_tree.create_node('力测量', 'procedurepropvar 2.2.8', 'procedurepropname 2.2')
    procedure_tree.create_node('试验操作团队二岗', 'procedurepropname 2.3', 'procedureprop 2')
    procedure_tree.create_node('应变系统', 'procedurepropvar 2.3.1', 'procedurepropname 2.3')
    procedure_tree.create_node('控制系统', 'procedurepropvar 2.3.2', 'procedurepropname 2.3')
    procedure_tree.create_node('混响室本体', 'procedurepropvar 2.3.3', 'procedurepropname 2.3')
    procedure_tree.create_node('功放系统', 'procedurepropvar 2.3.4', 'procedurepropname 2.3')
    procedure_tree.create_node('台体系统', 'procedurepropvar 2.3.5', 'procedurepropname 2.3')
    procedure_tree.create_node('测量系统', 'procedurepropvar 2.3.6', 'procedurepropname 2.3')
    procedure_tree.create_node('气源系统', 'procedurepropvar 2.3.7', 'procedurepropname 2.3')
    procedure_tree.create_node('力测量', 'procedurepropvar 2.3.8', 'procedurepropname 2.3')
    procedure_tree.create_node('试件交接', 'procedurename 3', 'procedure')
    procedure_tree.create_node('试验前总检', 'procedurename 4', 'procedure')
    procedure_tree.create_node('试验参数设置', 'procedurename 5', 'procedure')
    procedure_tree.create_node('试验', 'procedurename 6', 'procedure')
    procedure_tree.create_node('试验结果评价', 'procedurename 7', 'procedure')
    procedure_tree.create_node('试验报告生成', 'procedurename 8', 'procedure')
    # print (procedure_tree)
    model_tree.paste('modelname 1', procedure_tree, deep=False)
    print(model_tree)
    #
    dict_list = tree_to_list(model_tree)
    for item in dict_list:
        print(item)
