import random
import json
import time

listOfFrozensets = []
my_permutations = []
SIG = []
jSim = []
SigSim = []
distJSim = []
distSigSim = []
myNeighborsDictJsim = []
myNeighborsDictSigSim = []
lstAvgJSim = []
lstAvgSigSim = []
AvgJsim = 0
AvgSigSim = 0
numbOfDocumets = 0
load = 0
numPermutations = 3
candidatesLSH = {}     
neighborsLSH = {}
lstAvgLSH = []         
AvgLSH = 0     
HASH_SPACE = 5000



#my_permutations.append({5: 0, 3: 1, 1: 2, 4: 3, 2: 4, 0: 5})#gia Testing.txt
#my_permutations.append({0: 0, 5: 1, 1: 2, 2: 3, 3: 4, 4: 5})
#my_permutations.append({3: 0, 2: 1, 1: 2, 0: 3, 5: 4, 4: 5})

my_permutations.append({1: 0, 2: 1, 6: 2, 5: 3, 0: 4, 4: 5 , 3:6})#gia paradeigma diafaneias 39 , diafaneies.txt
my_permutations.append({3: 0, 1: 1, 0: 2, 2: 3, 5: 4, 6: 5 , 4:6})
my_permutations.append({2: 0, 3: 1, 6: 2, 1: 3, 5: 4, 0: 5 , 4:6})


#STORE LIST OF DIXTIONARIES (IN JSON-FORMAT) TO FILE
json_to_file = open("./my_data.json", "w")
json.dump(my_permutations, json_to_file, indent=1)
json_to_file.close()

#print("\n=============================================================")
#print("This is the list of permutations, as is read from the input file:")
#for i in range(numPermutations):
#    print( "Permutation number", i ,"is :", permutations_from_file[i] )
#print("=============================================================\n")

def UpgradeGlobalVariable(lstOfFrozensets,numDocuments):
    global listOfFrozensets
    global numbOfDocumets

    listOfFrozensets = lstOfFrozensets
    numbOfDocumets = numDocuments

'''def UpgradeGlobalVariableLoad(l):
    global load
    load = l'''

def UpgradeGlobalVariablePermutations(per):
    global numPermutations
    numPermutations = per

def MyReadDataRoutine(nameDoc, numDocuments):
    f = open(nameDoc, "r");
    f1 = open(nameDoc, "r");
    lines = len(f1.readlines())
    f1.close()
    frozensetList = []
    lstWordIds = []

    x = f.readline()
    field = x.split()
    field = list(map(int,field))
    maxDocId = field[0]
    f.readline()
    f.readline()

    line = f.readline()
    fields = line.split()
    fields.pop()
    fields = list(map(int,fields))

    currentDocId = fields[0];
    lstWordIds.append(fields[1])

    if(numDocuments != maxDocId):
        while(True):
            line = f.readline()

            fields = line.split()
            fields.pop()
            fields = list(map(int,fields))

            if(currentDocId == fields[0]):
                lstWordIds.append(fields[1])
            else:
                currentDocId = fields[0]

                if (currentDocId > numDocuments):
                    break

                frozensetList.append(frozenset(lstWordIds))
                lstWordIds.clear()
                lstWordIds.append(fields[1])

        if(lstWordIds):
            frozensetList.append(frozenset(lstWordIds))
            lstWordIds.clear()
    else:
        for i in range(lines-4):
            line = f.readline()
            fields = line.split()
            fields.pop()
            fields = list(map(int, fields))

            if (currentDocId == fields[0]):
                lstWordIds.append(fields[1])
            else:
                currentDocId = fields[0]

                frozensetList.append(frozenset(lstWordIds))
                lstWordIds.clear()
                lstWordIds.append(fields[1])
        if (lstWordIds):
            frozensetList.append(frozenset(lstWordIds))
            lstWordIds.clear()
    return frozensetList

def MyJacSimWithSets(docID1,docID2):
    global listOfFrozensets
    global numbOfDocumets

    if ((1 <= docID1) and (docID1 <= numbOfDocumets) and (1 <= docID2) and (docID2 <= numbOfDocumets)):

        intersectionCounter = 0;

        for x in listOfFrozensets[docID1-1]:
            for y in listOfFrozensets[docID2-1]:
                if (x == y):
                    intersectionCounter += 1

        A = len(listOfFrozensets[docID1-1])
        B = len(listOfFrozensets[docID2-1])
        JacSim = intersectionCounter/(A+B-intersectionCounter)
    else:
        print("Invalid DocId1 and DocId2")
    return JacSim

def MyJacSimWithOrderedLists(docID1,docID2):
    global listOfFrozensets
    global numbOfDocumets

    if ((1 <= docID1) and (docID1 <= numbOfDocumets) and (1 <= docID2) and (docID2 <= numbOfDocumets)):
        wordIDs1 = sorted(listOfFrozensets[docID1-1])
        wordIDs2 = sorted(listOfFrozensets[docID2-1])

        intersectionCounter = 0;
        pos1 = 0
        pos2 = 0
        A = len(wordIDs1)
        B = len(wordIDs2)

        while (pos1<A) and (pos2<B):
            if (wordIDs1[pos1] == wordIDs2[pos2]):
                intersectionCounter +=1
                pos1 += 1
                pos2 += 1
            else :
                if (wordIDs1[pos1] < wordIDs2[pos2]):
                    pos1 += 1
                else :
                    pos2 += 1

        JacSim = intersectionCounter/(A+B-intersectionCounter)

    return JacSim

def create_random_hash_function(p=2**33-355, m=2**32-1):
    a = random.randint(1,p-1)
    b = random.randint(0, p-1)
    return lambda x: 1 + (((a * x + b) % p) % m)

def create_random_hash_dictionary(maxNum):
        h = create_random_hash_function()

        randomHash = { x:h(x) for x in range(maxNum) }
        myHashKeysOrderedByValues = sorted(randomHash, key=randomHash.get)
        myHash = { myHashKeysOrderedByValues[x]:x for x in range(maxNum) }

        return myHash

def MyMinHash(listOfFrozensets,k):
    M = []      # docs x words
    wordList = []
    h = []
    global load

    #1. Βρες max wordID
    helpList = sorted(listOfFrozensets[0])
    maxNum = helpList[-1]
    for docIds in listOfFrozensets:
        wordIdsList = sorted(docIds) # sortarismenh lista me ta wordID gia kathe docID
        m = wordIdsList[-1]
        if (maxNum<m):
            maxNum = m

    # 2. Φτιάξε M: κάθε doc → binary vector μεγέθους maxNum
    for docIds in listOfFrozensets:
        lst = [0] * maxNum
        for wordIds in docIds:
            lst[wordIds-1] = 1
        M.append(lst)

    # 3. Φτιάξε wordList: κάθε word → σε ποια docs εμφανίζεται
    for i in range(maxNum): 
        listed = [0]*len(M)
        l = 0
        for lst in M:
            listed[l]=lst[i]
            l +=1
        wordList.append(listed)

    # 4. Δημιούργησε k τυχαία hash functions
    if (load == 0):

        for i in range(k):
            h.append(create_random_hash_dictionary(maxNum))

        # SIG: k x numDocs
        SIG_temp = [[-1 for i in range(len(listOfFrozensets))] for j in range(k)]

        # 5. MinHash υπογραφέ
        for row in range(len(wordList)): # για κάθε wordID
            for col in range(len(wordList[row])): # για κάθε doc
                if (wordList[row][col] == 1):
                    for i in range(len(h)): # για κάθε hash function
                        if (SIG_temp[i][col] == -1):
                            SIG_temp[i][col] = h[i][row]
                        elif (SIG_temp[i][col] > h[i][row]):
                            SIG_temp[i][col] = h[i][row]
    # 6. Μετατροπή σε per-document υπογραφές: N x k
    signatures = []
    numDocs = len(listOfFrozensets)
    for doc in range(numDocs):
        sig_doc = [SIG_temp[i][doc] for i in range(k)]
        signatures.append(sig_doc)

    return signatures

def MySigSim(docID1,docID2,numPermutations):
    global SIG
    sig1 = SIG[docID1-1][:numPermutations]
    sig2 = SIG[docID2-1][:numPermutations]

    matches = 0
    for i in range(numPermutations):
        if sig1[i] == sig2[i]:
            matches += 1
    return matches / numPermutations

def BruteForce(numDocuments, numNeighbors, numPermutations):
    global jSim, SigSim, distJSim, distSigSim
    global myNeighborsDictJsim, myNeighborsDictSigSim
    global lstAvgJSim, lstAvgSigSim
    global AvgJsim, AvgSigSim
    global SIG, listOfFrozensets

    jSim = []
    SigSim = []
    distJSim = []
    distSigSim = []
    myNeighborsDictJsim = []
    myNeighborsDictSigSim = []
    lstAvgJSim = []
    lstAvgSigSim = []
    AvgJsim = 0
    AvgSigSim = 0

    # 1) Υπολόγισε υπογραφές μία φορά
    SIG = MyMinHash(listOfFrozensets, numPermutations)
    
    # ---------------------- JACCARD + SIGSIM ΓΙΑ ΟΛΑ ΤΑ ΖΕΥΓΗ ----------------------
    start_time = time.perf_counter ()

    for i in range(numDocuments-1):
        lst_j = []
        lst_sig = []
        for j in range(i,numDocuments-1):
            d1 = i + 1
            d2 = j + 2

            lst_j.append(MyJacSimWithOrderedLists(d1, d2))
            lst_sig.append(MySigSim(d1, d2, numPermutations))

        jSim.append(lst_j)
        SigSim.append(lst_sig)

    # ---------------------- ΑΠΟΣΤΑΣΕΙΣ & ΓΕΙΤΟΝΕΣ ΜΕ JACCARD ----------------------
    # Αποστάσεις και γειτονές με Jaccard
    for i in range(len(jSim)):
        counter = 1
        jSimDict = {}
        for j in range(len(jSim[i])):
            counter += 1
            jSimDict[i+counter] = 1 - jSim[i][j]
        distJSim.append(jSimDict)

    # Ταξινόμηση dicts κατά απόσταση
    pos = -1
    for elements in distJSim:
        pos += 1
        sortedDict = {k: v for k, v in sorted(elements.items(), key=lambda  item: item[1])}
        distJSim[pos] = sortedDict

    # Υπολογισμός κοντινότερων γειτόνων (Jaccard)
    for dicts in distJSim:
        myDict = {}
        if (len(dicts) < numNeighbors-1):
            for elements in dicts.keys():
                myDict[elements] = 1 - dicts[elements]
            myNeighborsDictJsim.append(myDict)
        counter = -1
        myDict = {}
        for elements in dicts.keys():
            counter += 1
            myDict[elements] = 1 - dicts[elements]
            if (counter == numNeighbors-1):
                break
        myNeighborsDictJsim.append(myDict)

    end_time = time.perf_counter ()
    print("ExecTime JSsim : ",end_time - start_time, "seconds")

    # Μέσος όρος ομοιότητας για κάθε doc (Jaccard)
    for lists in myNeighborsDictJsim:
        avgPerDocId = 0
        for elements in lists.keys():
            avgPerDocId += lists[elements]
        lstAvgJSim.append(avgPerDocId/numNeighbors)

    for elements in lstAvgJSim:
        AvgJsim += elements

    AvgJsim = AvgJsim/numDocuments
    
    # ---------------------- ΑΠΟΣΤΑΣΕΙΣ & ΓΕΙΤΟΝΕΣ ΜΕ SIGSIM ----------------------
    start_time = time.perf_counter ()
    
    for i in range(len(SigSim)):
        counter = 1
        SigDict = {}
        for j in range(len(SigSim[i])):
            counter += 1
            SigDict[i+counter] = 1 - SigSim[i][j]
        distSigSim.append(SigDict)

    # Ταξινόμηση
    pos = -1
    for elements in distSigSim:
        pos += 1
        sortedDict = {k: v for k, v in sorted(elements.items(), key=lambda  item: item[1])}
        distSigSim[pos] = sortedDict

    # Υπολογισμός κοντινότερων γειτόνων (SigSim)
    for dicts in distSigSim:
        myDict = {}
        if (len(dicts) < numNeighbors-1):
            for elements in dicts.keys():
                myDict[elements] = 1 - dicts[elements]
            myNeighborsDictSigSim.append(myDict)
        counter = -1
        myDict = {}
        for elements in dicts.keys():
            counter += 1
            myDict[elements] = 1 - dicts[elements]
            if (counter == numNeighbors-1):
                break
        myNeighborsDictSigSim.append(myDict)

    end_time = time.perf_counter ()
    print("ExecTime SigSsim : ",end_time - start_time, "seconds")

    # Μέσος όρος ομοιότητας για κάθε doc (SigSim)
    for lists in myNeighborsDictSigSim:
        avgPerDocId = 0
        for elements in lists.keys():
            avgPerDocId += lists[elements]
        lstAvgSigSim.append(avgPerDocId/numNeighbors)

    for elements in lstAvgSigSim:
        AvgSigSim += elements

    AvgSigSim = AvgSigSim/numDocuments

def MyLSH(SIG, bands, rows_per_band, numNeighbors):
    import time
    global listOfFrozensets   
    global neighborsLSH
    global candidatesLSH
    global lstAvgLSH
    global AvgLSH
    
    start = time.perf_counter()

    N = len(SIG)          # πλήθος εγγράφων
    k = len(SIG[0])       # πλήθος permutations (MinHash functions)
    assert k == bands * rows_per_band, "Error: k must equal bands * rows_per_band"

    candidatesLSH = {doc: set() for doc in range(N)}
    neighborsLSH = [{} for _ in range(N)]
    lstAvgLSH = []
    AvgLSH = 0

    # 1. Υποψήφια ζεύγη με βάση τα bands
    for b in range(bands):
        bucket_dict = {}

        band_start = b * rows_per_band
        band_end = band_start + rows_per_band

        for doc in range(N):
            band_tuple = tuple(SIG[doc][row] for row in range(band_start, band_end))
            h = hash(band_tuple) % HASH_SPACE
  
            bucket_dict.setdefault(h, []).append(doc)

        # Όσα docs πέφτουν στο ίδιο bucket είναι υποψήφιοι γείτονες
        for group in bucket_dict.values():
            if len(group) > 1:
                for d in group:
                    for other in group:
                        if d != other:
                            candidatesLSH[d].add(other)

    # 2. Υπολογισμός ομοιοτήτων ΜΟΝΟ για τα υποψήφια ζεύγη
    for d in range(N):
        sim_dict = {}

        # βρες similarity μόνο με τους candidate neighbors
        for other in candidatesLSH[d]:
            sim = MyJacSimWithOrderedLists(d + 1, other + 1)
            sim_dict[other + 1] = sim   # αποθηκεύουμε similarity (όχι distance)

        topK = sorted(sim_dict.items(), key=lambda x: x[1], reverse=True)[:numNeighbors]
        neighborsLSH[d] = dict(topK)

    # 3. Global AvgSim όπως στο brute force
    for doc in range(N):
        if len(neighborsLSH[doc]) == 0:
            lstAvgLSH.append(0)
        else:
            lstAvgLSH.append(sum(neighborsLSH[doc].values()) / len(neighborsLSH[doc]))

    # 4. Υπολογισμός overall AvgSim
    AvgLSH = sum(lstAvgLSH) / N
    end = time.perf_counter()
    print("ExecTime LSH:", end - start, "seconds")

def printJSim():
    global jSim

    x = -1
    for i in range(len(jSim)):
        x += 1
        for j in range(len(jSim[i])):
            print("JSim(",i+1,j+2+x,"):",jSim[i][j])

def printSigSim():
    global SigSim

    x = -1
    for i in range(len(SigSim)):
        x += 1
        for j in range(len(SigSim[i])):
            print("SigSim(", i+1, j+2+x, "):", SigSim[i][j])

def printDistJSim():
    global distJSim

    print("The distances are sorted")
    for i in range(len(distJSim)):
        for j in distJSim[i].keys():
            print("DistJSim(",i+1,j,"):",distJSim[i][j])

def printDistSigSim():
    global distSigSim

    print("The distances are sorted")
    for i in range(len(distSigSim)):
        for j in distSigSim[i].keys():
            print("DistSigSim(", i + 1, j, "):", distSigSim[i][j])

def printMyNeighborsDictJsim():
    global myNeighborsDictJsim

    for i in range(len(myNeighborsDictJsim)):
        for j in myNeighborsDictJsim[i].keys():
            print("NeighborJSim(", i + 1, j, "):", myNeighborsDictJsim[i][j])

def printMyNeighborsDictSigSim():
    global myNeighborsDictSigSim

    for i in range(len(myNeighborsDictSigSim)):
        for j in myNeighborsDictSigSim[i].keys():
            print("NeighborSigSim(", i + 1, j, "):", myNeighborsDictSigSim[i][j])

def printLstAvgJSim():
    global lstAvgJSim
    #print(lstAvgJSim)
    for i in range(len(lstAvgJSim)):
        print("The AvgJsim for DocId",i,"is:",lstAvgJSim[i])

def printLstAvgSigSim():
    global lstAvgSigSim
    #print(lstAvgSigSim)
    for i in range(len(lstAvgSigSim)):
        print("The AvgSigSim for DocId",i,"is:",lstAvgSigSim[i])

def printAvgJsim():
    global AvgJsim

    print("AvgJSim: ",AvgJsim)

def printAvgSigSim():
    global AvgSigSim

    print("AvgSigSim: ",AvgSigSim)

def printCandidatesLSH():
    global candidatesLSH
    for doc, cands in candidatesLSH.items():
        print(f"Doc {doc+1} candidates: {sorted(list(cands))}")

def printNeighborsLSH():
    global neighborsLSH
    for doc in range(len(neighborsLSH)):
        print(f"Doc {doc+1} neighbors: {neighborsLSH[doc]}")

def printLstAvgLSH():
    global lstAvgLSH
    for i, val in enumerate(lstAvgLSH):
        print(f"Doc {i+1} AvgSim(LSH) = {val}")

def printAvgLSH():
    global AvgLSH
    print("Overall AvgSim (LSH):", AvgLSH)

