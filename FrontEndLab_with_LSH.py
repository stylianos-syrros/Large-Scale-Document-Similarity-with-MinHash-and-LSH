from Lab1_with_LSH import *

print("-----------------------------------------------------------")
print(" DATASET SELECTION ")
print("-----------------------------------------------------------")
print("1) Enron dataset        (DATA_1-docword.enron.txt)")
print("2) Nips dataset        (DATA_2-docword.nips.txt)")
print("3) Exit")
print("-----------------------------------------------------------")

choice = input("Select dataset (1–3): ")

if choice == "1":
    filename = "DATA_1-docword.enron.txt"
elif choice == "2":
    filename = "DATA_2-docword.nips.txt"
elif choice == "3":
    exit()
else:
    print("Invalid selection")
    exit()

numDocuments = int(input("Give me the number of documents to read: "))
documents = MyReadDataRoutine(filename, numDocuments)

while(True):
    print("----------------------------------------------------------------------------")
    print("1)MyReadDataRoutine")
    print("2)MyJacSimWithSets")
    print("3)MyJacSimWithOrderedLists")
    print("4)create_random_hash_dictionary")
    print("5)MyMinHash")
    print("6)MySigSim")
    print("7)BruteForce")
    print("8)MyLSH")
    print("9)Change txt file")
    print("10)change number of documents")
    print("11)Exit")

    selection = str(input("Select 1-11:"))
    print("----------------------------------------------------------------------------")

    if(selection == "11"):
        break

    elif(selection == "1"):
        listOfFrozensets = MyReadDataRoutine(filename,numDocuments)
        UpgradeGlobalVariable(listOfFrozensets,numDocuments)
        #x = str(input("Do you want to print the list of frozensets (y/n)?"))
        #if(x == "y"):
        print(listOfFrozensets)

    elif(selection == "2"):
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets,numDocuments)
        print(f"Give two document IDs between 1 and {numDocuments}, separated by space (e.g. '2 5'):")
        DocId1, DocId2 = map(int, input().split())
        if not (1 <= DocId1 <= numDocuments and 1 <= DocId2 <= numDocuments):
            print("Doc IDs must be between 1 and", numDocuments)
        else:
            jSimWithSets = MyJacSimWithSets(DocId1, DocId2)
            print("Jaccard Similarity (with sets) =", jSimWithSets)


    elif(selection == "3"):
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)

        print(f"Give two document IDs between 1 and {numDocuments}, separated by space (e.g. '2 5'):")
        DocId1, DocId2 = map(int, input().split())

        if not (1 <= DocId1 <= numDocuments and 1 <= DocId2 <= numDocuments):
            print("Doc IDs must be between 1 and", numDocuments)
        else:
            jSimWithOrderedLists = MyJacSimWithOrderedLists(DocId1, DocId2)
            print("Jaccard Similarity (with ordered lists) =", jSimWithOrderedLists)

    elif(selection == "4"):
        x = int(input("Give the maximum value for hashing (creates a permutation of 0..max-1):"))
        hash = create_random_hash_dictionary(x)
        print("Your ordered hash function is:",hash)

    elif(selection == "5"):
        #load = int(input("Do you want to load your hash function (load = 0) or do you want to create random hash functions (load = 1)? Type 0 or 1: "))
        #if(load == 0):
        
        permutations = int(input("How much permutations do you want for MinHash? "))
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        
        UpgradeGlobalVariable(listOfFrozensets,numDocuments)
        #UpgradeGlobalVariableLoad(0)
        
        SIG = MyMinHash(listOfFrozensets,permutations)

        print("Your signatures are: ",SIG)

    elif(selection == "6"):
        #load = int(input("Do you want to load your hash function(load = 0) or do you want to creat random hash functions(load = 1)?Type 0 or 1: "))
        #if (load == 0):
            
        permutations = int(input("How many permutations do you want for SigSim? "))
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)
        #UpgradeGlobalVariableLoad(0)

        print(f"Give two document IDs between 1 and {numDocuments}, separated by space (e.g. '2 5'):")
        DocId1, DocId2 = map(int, input().split())
        if not (1 <= DocId1 <= numDocuments and 1 <= DocId2 <= numDocuments):
            print("Doc IDs must be between 1 and", numDocuments)
        else:
            SigSim = MySigSim(DocId1, DocId2, permutations)
            print("Sig Similarity:", SigSim)

    elif(selection == "7"):
        #load = int(input("Do you want to load your hash function(load = 0) or do you want to creat random hash functions(load = 1)? Type 0 or 1: "))
        #if (load == 0):
        
        permutations = int(input("How much permutations do you want? "))
        neighbors = int(input("Give me the number of neighbors:"))

        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)
        #UpgradeGlobalVariableLoad(0)
        UpgradeGlobalVariablePermutations(permutations)

        BruteForce(numDocuments,neighbors,permutations)

        while(True):
            print("----------------------------------------------------------------------------")
            print("1)Jaccard Similarities")
            print("2)Signature Similarities")
            print("3)Distances JSim")
            print("4)Distances SigSim")
            print("5)Closest Neighbors based on Jsim")
            print("6)Closest Neighbors based on SigSim")
            print("7)Average Jsim (for all documents)")
            print("8)Average SigSim (for all documents)")
            print("9)Total Average Jsim (of all documents)")
            print("10)Total Average SigSim (of all documents)")
            print("11)Exit")

            sel = str(input("Select 1-11:"))
            print("----------------------------------------------------------------------------")

            if(sel == "11"):
                break
            elif(sel == "1"):
                printJSim()
            elif(sel == "2"):
                printSigSim()
            elif(sel == "3"):
                printDistJSim()
            elif(sel == "4"):
                printDistSigSim()
            elif(sel == "5"):
                printMyNeighborsDictJsim()
            elif(sel == "6"):
                printMyNeighborsDictSigSim()
            elif(sel == "7"):
                printLstAvgJSim()
            elif(sel == "8"):
                printLstAvgSigSim()
            elif (sel == "9"):
                printAvgJsim()
            elif (sel == "10"):
                printAvgSigSim()

    elif(selection == "8"):
        try:
            SIG  
        except NameError:
            print("You must run MyMinHash first (option 5) to create the signature matrix SIG.")
        else:
            print(f"You used {len(SIG[0])} permutations in MyMinHash, so bands * rows_per_band must equal {len(SIG[0])}.")
            bands = int(input("Give number of bands: "))
            rows = int(input("Give number of rows per band: "))
            k = int(input("Give number of neighbors (K): "))

            MyLSH(SIG, bands, rows, k)

            while(True):
                print("----------------------------------------------------------------------------")
                print("1) Candidate Neighbors (LSH buckets)")
                print("2) Final LSH Neighbors (K-NN)")
                print("3) AvgSim per Document (LSH)")
                print("4) Total AvgSim (LSH)")
                print("5) Exit")
                print("----------------------------------------------------------------------------")

                x1 = str(input("Give me your selection: "))

                if(x1 == "1"):
                    printCandidatesLSH()
                elif(x1 == "2"):
                    printNeighborsLSH()
                elif x1 == "3":
                    printLstAvgLSH()
                elif x1 == "4":
                    printAvgLSH()
                elif(x1 == "5"):
                    print("Exiting LSH menu...")
                    break
                else:
                    print("Wrong Selection")

    elif(selection == "9"):
        filename = str(input("Give me new txt name:"))
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)
        x = str(input("Do you want to print the list of frozensets(y/n)?"))
        if (x == "y"):
            print(listOfFrozensets)

    elif(selection == "10"):
        numDocuments = int(input("Give me the new number of documents to read: "))
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)
        listOfFrozensets = MyReadDataRoutine(filename, numDocuments)
        UpgradeGlobalVariable(listOfFrozensets, numDocuments)
