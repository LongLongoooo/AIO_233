import streamlit as st
import numpy as np

def load_vocab ( file_path ) :
    with open ( file_path , "r") as f :
        lines = f.readlines ()
    words = sorted (set ([ line . strip () . lower () for line in lines ]) )
    return words
# build vocabulary
vocabs = load_vocab ( file_path =r"C:\Users\long0\PycharmProjects\Module_Exercises_4\source\source\data\vocab.txt")

def delete_cost(source: str):
  return 1
def insert_cost(target: str):
  return 1
def sub_cost(source: str, target: str):
  if source == target:
    return 0
  return 1

def Levenshtein_distance(source: str, target: str):
  newsource = "#" + source
  newtarget = "#" + target
  M = len(newsource)
  N = len(newtarget)

  matrix = np.zeros((M,N))
  for i in range(M):
    for j in range(N):
      if min(i, j) == 0:
        matrix[i, j] = max(i, j)
      else:
        value1 = matrix[(i-1), j] + delete_cost(newsource[i]) # Use newsource for indexing
        value2 = matrix[i, (j-1)] + insert_cost(newtarget[j]) # Use newtarget for indexing
        value3 = matrix[(i-1), (j-1)] + sub_cost(newsource[i], newtarget[j]) # Use newsource and newtarget

        matrix[i, j] = min(value1, value2, value3)

  return matrix[M-1, N-1]

def main():
    st.title("Word Correction")
    word = st.text_input("Enter word: ")

    if st.button("Analyse"):

        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = Levenshtein_distance(word, vocab)


        sorted_distances = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        corrected_word = list(sorted_distances.keys())[0]

        st.write("Correct word: ", corrected_word)

        col1, col2 = st.columns(2)
        col1.write("Vocabulary")

        col2.write("Distances: ")
        col2.write(sorted_distances)
if __name__ == "__main__":
    main()