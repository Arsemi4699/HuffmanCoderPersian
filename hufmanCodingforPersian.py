uniCodeTable = [0x621, 0x623, 0x626, 0x624, 0x627, 0x628, 0x67E, 0x62A, 0x62B, 0x62C, 0x686, 0x62D, 0x62E, 0x62F, 0x630, 0x631, 0x632,
                0x698, 0x633, 0x634, 0x635, 0x636, 0x637, 0x638, 0x639, 0x63A, 0x641, 0x642, 0x6A9, 0x6AF, 0x644, 0x645, 0x646, 0x648,
                0x647, 0x6CC, 0x20, 0x2e, 0x21, 0x61f, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 37, 40, 41, 45, 43, 61, 47, 1548, 1614,
                1615, 1616, 39, 34, 58, 1563]
faFreq = [0] * len(uniCodeTable)
CharCodedList = []


class Node:
    def __init__(self, freq, code):
        self.CharFreq = freq
        self.UniCodefa = code
        self.leftChild = None
        self.rightChild = None
        self.hufCode = ""


def insertion_Sort(li):
    for i in range(1, len(li)):
        tmp = li[i]
        idx = i
        while tmp.CharFreq < li[idx-1].CharFreq and idx > 0:
            li[idx] = li[idx-1]
            idx -= 1
        li[idx] = tmp


def makeHufCode(root, hufCode):
    if root.leftChild != None:
        makeHufCode(root.leftChild, hufCode + "0")
    if root.rightChild != None:
        makeHufCode(root.rightChild, hufCode + "1")
    if root.leftChild == None and root.rightChild == None:
        root.hufCode = hufCode
        CharCodedList.append(root)


def darwTree(root, q):
    print(f"{root.UniCodefa}({root.CharFreq})")
    if root.leftChild != None:
        for i in range(q):
            print("      ", end="")
        if root.rightChild == None:
            print("└──", end="")
        else:
            print("├──", end="")
        print("0", end="")
        print("──", end="")
        darwTree(root.leftChild, q+1)
    if root.rightChild != None:
        for i in range(q):
            print("      ", end="")
        print("└──", end="")
        print("1", end="")
        print("──", end="")
        darwTree(root.rightChild, q+1)


def codeIt(faInText):

    for c in faInText:
        for i in range(len(uniCodeTable)):
            if ord(c) == uniCodeTable[i]:
                faFreq[i] += 1

    itemList = []
    for i in range(len(uniCodeTable)):
        if faFreq[i]:
            itemList.append(Node(faFreq[i], chr(uniCodeTable[i])))

    insertion_Sort(itemList)

    root = Node(0, 0)
    if debug:
        print("generating tree bottom to up: ")
    while (len(itemList) > 1):
        if debug:
            print("left child: ", itemList[0].CharFreq, itemList[0].UniCodefa)
        temp = Node(itemList[0].CharFreq, itemList[0].UniCodefa)
        temp.leftChild = itemList.pop(0)
        if debug:
            print("right child", itemList[0].CharFreq, itemList[0].UniCodefa)
        temp.CharFreq += itemList[0].CharFreq
        temp.UniCodefa += itemList[0].UniCodefa
        temp.rightChild = itemList.pop(0)
        if debug:
            print("Root: ", temp.CharFreq, temp.UniCodefa, end="\n\n")
        itemList.append(temp)
        insertion_Sort(itemList)
        root = temp

    makeHufCode(root, "")

    if debug:
        darwTree(root, 0)

    print("\nhuffman coding table: ")
    for i in CharCodedList:
        print(f"{i.UniCodefa} , {i.CharFreq} , code: {i.hufCode}")

    hufCodeOut = ""
    for i in faInText:
        for c in CharCodedList:
            if c.UniCodefa == i:
                hufCodeOut += f"{c.hufCode}"
    return hufCodeOut


def decodeIt(hufmanCoded):
    temp = ""
    decodeText = ""
    for i in hufmanCoded:
        temp += i
        for c in CharCodedList:
            if temp == c.hufCode:
                decodeText += c.UniCodefa
                temp = ""
                break
    return decodeText


faInText = input("enter a persian text(it's only consider persian chars): ")
debug = int(input("if you don't want to see generating tree process enter 0: "))
ansCode = codeIt(faInText)
print('\nHufman Code: ')
print(ansCode)
print('\nHufman Decode: ')
ansDecode = decodeIt(ansCode)
print(ansDecode)
