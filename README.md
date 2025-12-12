# Nearest Neighbor Search on Large Document Collections
## Jaccard Similarity, MinHash & Locality Sensitive Hashing (LSH)

This repository contains an implementation and experimental evaluation of
**nearest neighbor search techniques for large-scale document collections**.
The project was developed in the context of the course  
**Algorithms for Big Data / Algorithms for Large-Scale Data**.

The goal is to study the **accuracy, efficiency and scalability** of different
approaches for document similarity search, including:

- Exact **Jaccard similarity** (brute-force baseline)
- **MinHash signatures** as a fast approximation of Jaccard similarity
- **Locality Sensitive Hashing (LSH)** for scalable nearest-neighbor retrieval

---

## 1. Problem Description

Each document is represented in **bag-of-words** form.
The input files follow the standard `docword` format:

```text
D          # number of documents
W          # number of distinct terms
NNZ        # number of non-zero entries
docID wordID wordCount
docID wordID wordCount
...
```

In this project, word frequencies are ignored and each document is modeled as
**a set of word identifiers**.

For two documents \(X\) and \(Y\), the **Jaccard similarity** is defined as:

```text
JacSim(X, Y) = |X ∩ Y| / |X ∪ Y|
```

The task is to identify, for each document, its **nearest neighbors** and to
compare exact and approximate similarity search methods in terms of:

- runtime performance,
- scalability,
- average similarity accuracy.

---

## 2. Implemented Algorithms

### PT1 – Data Reading and Preprocessing

`MyReadDataRoutine(filename, numDocuments)`

- Reads a `docword` input file.
- Loads only the first `numDocuments` documents.
- Represents each document as a `frozenset` of word IDs.
- Stores the document collection in global memory for reuse.

### PT2 – Exact Jaccard Similarity

Two exact Jaccard similarity implementations are provided:

1. `MyJacSimWithSets(docID1, docID2)`
   - Uses Python set operations.
   - Simple but slower for large documents.

2. `MyJacSimWithOrderedLists(docID1, docID2)`
   - Converts sets to sorted lists.
   - Uses a two-pointer merge technique.
   - More efficient and used in brute-force experiments.

### PT3 – MinHash Signature Construction

`MyMinHash(listOfFrozensets, K)`

- Constructs `K` random MinHash permutations.
- Computes a **K-dimensional signature** for each document.
- Returns a signature matrix with the following structure:

```text
SIG[docID][hashIndex]
```

This representation allows efficient approximation of Jaccard similarity.

### PT4 – Signature-Based Similarity (SigSim)

`MySigSim(docID1, docID2, numPermutations)`

- Compares the MinHash signatures of two documents.
- Returns the fraction of matching signature components.
- Provides a fast approximation of Jaccard similarity.

### PT5 – Brute-Force Nearest Neighbor Search

`BruteForce(numDocuments, numNeighbors, numPermutations)`

- Computes all pairwise similarities among the first `numDocuments` documents.
- Uses:
  - exact Jaccard similarity,
  - MinHash-based signature similarity.
- For each document:
  - identifies the `numNeighbors` nearest neighbors,
  - computes average similarity.
- Reports:
  - per-document average similarity,
  - global average similarity,
  - execution time.

Brute-force Jaccard similarity has quadratic time complexity
and becomes impractical for large document collections.

### PT6 – Locality Sensitive Hashing (LSH)

`MyLSH(SIG, bands, rowsPerBand, numNeighbors)`

- Applies **LSH on MinHash signatures**.
- Splits each signature into bands and hashes them into buckets.
- Documents falling into the same bucket are treated as **candidate neighbors**.
- Exact similarity is computed **only for candidate pairs**.
- Nearest neighbors and average similarities are computed similarly to brute force.
- Achieves significant runtime improvements for large datasets.

---

## 3. Project Structure

```text
.
├── Lab1_with_LSH.py        # Core implementation (PT1–PT6)
├── FrontEndLab_with_LSH.py # Menu-driven interface
├── Lab1_part1.py           # Basic data loading test
├── my_data.json            # (Optional) stored hash permutations
└── README.md
```

---

## 4. How to Run

### Requirements

- Python **3.9 or later**
- No external dependencies

### Execution

Run the interactive menu:

```bash
python FrontEndLab_with_LSH.py
```

The menu allows the user to:

- select the dataset,
- choose the number of documents,
- compute Jaccard similarity,
- build MinHash signatures,
- run brute-force nearest neighbor search,
- run LSH-based approximate nearest neighbor search,
- inspect intermediate and final results.

### Datasets

This repository **includes only** the file:

- `DATA_1-docword.enron.txt`

Other `docword` files mentioned in the code or interface (for example
`DATA_2-docword.nips.txt`) are **not provided** and are optional. If desired,
they can be added later in the same directory and used directly from the
frontend menu.

---

## 5. Performance Observations

- Brute-force Jaccard similarity becomes extremely slow for large datasets
  (e.g., ~13 minutes for 5000 documents).
- MinHash signatures drastically reduce similarity computation time.
- LSH further improves scalability by limiting comparisons to candidate pairs.

These results clearly demonstrate the advantages of approximate methods
for similarity search in large-scale document collections.

---

## 6. Notes

- The implementation closely follows the algorithms presented in the lab handout.
- The focus is on clarity and educational value rather than production optimization.
- The project highlights why brute-force similarity search does not scale
  and how MinHash and LSH provide practical solutions.
