import os
import sys
import FPTree
'''
class FPGrowth:
    def __init__(self, minsup=2):
        self.fp = []
        self.minsup = minsup
    
    def growth(self, tree, postNodes):
        if tree.isUniquePath():
            nodeCombinations = []
            tree.getCombinationFromPath(nodeCombinations)
            for combination in nodeCombinations:
                support = self._getMinSupport(combination)
                if support is None or support < self.minsup:
                    continue
                #gen pattern
                pattern = ([],support)
                for node in combination:
                    pattern[0].append(node["name"])
                for node in postNodes:
                    pattern[0].append(node)
                if len(pattern[0]) > 1:
                    self.fp.append(pattern)
                    #self._print((Pattern(pattern)
        else:
            for item in tree.itemTable:
                #gen pattern
                pattern = ([],tree.itemTable[item][0])
                pattern[0].append(item)
                for node in postNodes:
                    pattern[0].append(node)
                if len(pattern[0]) > 1 and pattern[1] > self.minsup: 
                    self.fp.append(pattern)  
                    #self._print((Pattern(pattern)
                #construct conditional pattern base
                baseSet = []
                tree.getConditionalPatternBase(item,baseSet)  
                tmpTree = FPTree.FPTree(baseSet, minsup=self.minsup) 
                tmpTree.build()
                if not tmpTree.isEmpty():
                    self.growth(tmpTree, pattern[0])       
            
    def _getMinSupport(self, nodes):
        if len(nodes) == 0:
            return None
        support = nodes[0]["support"]
        for node in nodes:
            if node["support"] < support:
                support = node["support"]
        return support
    
def test(dataset):
    #testcase = [[["i2","i1","i5"],1],[["i2","i4"],1],[["i2","i3"],1],[["i2","i1","i4"],1],[["i1","i3"],1],[["i2","i3"],1],[["i1","i3"],1],[["i2","i1","i3","i5"],1],[["i2","i1","i3"],1]]
    #testcase = [[["a","b"],1],[["b","c","d"],1],[["a","c","d","e"],1],[["a","d","e"],1],[["a","b","c"],1],[["a","b","c","d"],1],[["a"],1],[["a","b","c"],1],[["a","b","d"],1],[["b","c","e"],1]]
    #testcase = [(["i1","i2"],1),(["i3"],1)]
    #dataset = [line.split() for line in open('mushroom.dat').readlines()]
    #dataset= [[1, 2, 3, 4,6], [2, 3, 4, 5,6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6]]
    testcase = []
    for a in dataset:
        testcase.append([a,1])
    tree = FPTree.FPTree(testcase,minsup=4)      
    tree.build()
    algorithm = FPGrowth(minsup=4)
    algorithm.growth(tree,[])
    res = sorted(algorithm.fp, key=lambda d:d[1], reverse = True )
    for rule in res:
        print(rule)
    print('the second freq_set_numbers is '+str(len(res)))
    
'''
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        # needs to be updated
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        """inc(对count变量增加给定值)
        """
        self.count += numOccur

def loadSimpDat(dataset):
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
            #    ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    #return [[1, 2, 3, 4,6], [2, 3, 4, 5,6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6]]
    return dataset


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if not frozenset(trans) in retDict:
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict


# this version does not use recursion
def updateHeader(nodeToTest, targetNode):
    """updateHeader(更新头指针，建立相同元素之间的关系，例如： 左边的r指向右边的r值，就是后出现的相同元素 指向 已经出现的元素)
    从头指针的nodeLink开始，一直沿着nodeLink直到到达链表末尾。这就是链表。
    性能：如果链表很长可能会遇到迭代调用的次数限制。
    Args:
        nodeToTest  满足minSup {所有的元素+(value, treeNode)}
        targetNode  Tree对象的子节点
    """
    # 建立相同元素之间的关系，例如： 左边的r指向右边的r值
    while (nodeToTest.nodeLink is not None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateTree(items, inTree, headerTable, count):
    """updateTree(更新FP-tree，第二次遍历)
    # 针对每一行的数据
    # 最大的key,  添加
    Args:
        items       满足minSup 排序后的元素key的数组（大到小的排序）
        inTree      空的Tree对象
        headerTable 满足minSup {所有的元素+(value, treeNode)}
        count       原数据集中每一组Kay出现的次数
    """
    # 取出 元素 出现次数最高的
    # 如果该元素在 inTree.children 这个字典中，就进行累加
    # 如果该元素不存在 就 inTree.children 字典中新增key，value为初始化的 treeNode 对象
    if items[0] in inTree.children:
        # 更新 最大元素，对应的 treeNode 对象的count进行叠加
        inTree.children[items[0]].inc(count)
    else:
        # 如果不存在子节点，我们为该inTree添加子节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 如果满足minSup的dist字典的value值第二位为null， 我们就设置该元素为 本节点对应的tree节点
        # 如果元素第二位不为null，我们就更新header节点
        if headerTable[items[0]][1] is None:
            # headerTable只记录第一次节点出现的位置
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            # 本质上是修改headerTable的key对应的Tree，的nodeLink值
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        # 递归的调用，在items[0]的基础上，添加item0[1]做子节点， count只要循环的进行累计加和而已，统计出节点的最后的统计值。
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def createTree(dataSet, minSup=1):
    """createTree(生成FP-tree)
    Args:
        dataSet  dist{行：出现次数}的样本数据
        minSup   最小的支持度
    Returns:
        retTree  FP-tree
        headerTable 满足minSup {所有的元素+(value, treeNode)}
    """
    # 支持度>=minSup的dist{所有元素：出现的次数}
    headerTable = {}
    # 循环 dist{行：出现次数}的样本数据
    for trans in dataSet:
        # 对所有的行进行循环，得到行里面的所有元素
        # 统计每一行中，每个元素出现的总次数
        for item in trans:
            # 例如： {'ababa': 3}  count(a)=3+3+3=9   count(b)=3+3=6
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 删除 headerTable中，元素次数<最小支持度的元素
    headertable={}
    for k in headerTable.keys():
        if headerTable[k] >= minSup:
            headertable[k]=headerTable[k]
    headerTable=headertable
    # 满足minSup: set(各元素集合)
    freqItemSet = set(headerTable.keys())
    # 如果不存在，直接返回None
    if len(freqItemSet) == 0:
        return None, None
    headertable={}
    for k in headerTable:
        # 格式化： dist{元素key: [元素次数, None]}
        headertable[k] = [headerTable[k], None]

    headerTable=headertable 
    # create tree
    retTree = treeNode('Null Set', 1, None)
    # 循环 dist{行：出现次数}的样本数据
    for tranSet, count in dataSet.items():
        # localD = dist{元素key: 元素总出现次数}
        localD = {}
        for item in tranSet:
            # 判断是否在满足minSup的集合中
            if item in freqItemSet:
                # print(( 'headerTable[item][0]=', headerTable[item][0], headerTable[item]
                localD[item] = headerTable[item][0]
        # print(( 'localD=', localD
        if len(localD) > 0:
            # p=key,value; 所以是通过value值的大小，进行从大到小进行排序
            # orderedItems 表示取出元组的key值，也就是字母本身，但是字母本身是大到小的顺序
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            # print( 'orderedItems=', orderedItems, 'headerTable', headerTable, '\n\n\n'
            # 填充树，通过有序的orderedItems的第一位，进行顺序填充 第一层的子节点。
            updateTree(orderedItems, retTree, headerTable, count)

    return retTree, headerTable


def ascendTree(leafNode, prefixPath):
    """ascendTree(如果存在父节点，就记录当前节点的name值)
    Args:
        leafNode   查询的节点对于的nodeTree
        prefixPath 要查询的节点值
    """
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    """findPrefixPath 基础数据集
    Args:
        basePat  要查询的节点值
        treeNode 查询的节点所在的当前nodeTree
    Returns:
        condPats 对非basePat的倒叙值作为key,赋值为count数
    """
    condPats = {}
    # 对 treeNode的link进行循环
    while treeNode is not None:
        prefixPath = []
        # 寻找改节点的父节点，相当于找到了该节点的频繁项集
        ascendTree(treeNode, prefixPath)
        # 避免 单独`Z`一个元素，添加了空节点
        if len(prefixPath) > 1:
            # 对非basePat的倒叙值作为key,赋值为count数
            # prefixPath[1:] 变frozenset后，字母就变无序了
            # condPats[frozenset(prefixPath)] = treeNode.count
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        # 递归，寻找改节点的下一个 相同值的链接节点
        treeNode = treeNode.nodeLink
        # print( treeNode
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    """mineTree(创建条件FP树)
    Args:
        inTree       myFPtree
        headerTable  满足minSup {所有的元素+(value, treeNode)}
        minSup       最小支持项集
        preFix       preFix为newFreqSet上一次的存储记录，一旦没有myHead，就不会更新
        freqItemList 用来存储频繁子项的列表
    """
    # 通过value进行从小到大的排序， 得到频繁项集的key
    # 最小支持项集的key的list集合
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    #print( '-----', sorted(headerTable.items(), key=lambda p: p[1][0]))
    #print('bigL=', bigL)
    # 循环遍历 最频繁项集的key，从小到大的递归寻找对应的频繁项集
    for basePat in bigL:
        # preFix为newFreqSet上一次的存储记录，一旦没有myHead，就不会更新
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print('newFreqSet=', newFreqSet, preFix)

        freqItemList.append(newFreqSet)
        #print('freqItemList=', freqItemList)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print( 'condPattBases=', basePat, condPattBases)

        # 构建FP-tree
        myCondTree, myHead = createTree(condPattBases, minSup)
        #print( 'myHead=', myHead)
        # 挖掘条件 FP-tree, 如果myHead不为空，表示满足minSup {所有的元素+(value, treeNode)}
        if myHead is not None:
            # 递归 myHead 找出频繁项集
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

#if __name__ == "__main__":
def test(dataset,minSup):
    simpDat = loadSimpDat(dataset)
    initSet = createInitSet(simpDat)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    # 创建条件模式基
    freqItemList = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItemList)
    print(freqItemList)
    print('\n\nthe second freq_set_numbers is '+str(len(freqItemList)))
