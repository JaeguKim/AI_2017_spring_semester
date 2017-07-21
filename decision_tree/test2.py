class Node:
    data = ''
    child_dic = {}
    attr_name_list = []
    def __init__(self, attr_name = None, attr_list = None):
        if attr_name is None:
            return
        self.data = attr_name
        if attr_list is None:
            return

        for temp in attr_list:
            self.child_dic[temp] = Node()
            self.attr_name_list.append(temp)

    def print_child_dic(self):
        print(self.child_dic)

    def get_child_dic(self):
        return self.child_dic

    def print_nodes(self):
        if self.data == 'empty':
            print('empty terminal node')
            return
        print(self.data)
        if self.data is 'e' or self.data is 'p': #terminal node이면 return
            return


test_node = Node('abcd')
test_node = Node()
print(test_node.data)