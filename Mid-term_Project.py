#Mid-term Project
#Madison Elliott
#Programming for data science
#Books used: Dracula, Frankenstein, Lair of the White Worm, The Jewel of Seven Stars, The Last Man, Mathilda
#Author: Mary Wollstonecraft Shelley - Frankenstein, The Last Man, Mathilda
#Author: Bram Stoker - Dracula, The Lair of the White Worm, The Jewel of Seven Stars

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
import re
import sys

#targets and markers
#target_words = ['as', 'but', 'from', 'can', 'what', 'the'] #update to AT LEAST 20 words. And put the target words in a different file to make less hard coded

def read_target_words(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Target words file '{file_path}' not found.")  # Fixed f-string placement
        sys.exit(1)

target_words = read_target_words("Target_Words.txt")

Markers = {
    "dracula": (
        "*** START OF THE PROJECT GUTENBERG EBOOK DRACULA ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK DRACULA ***"
    ),
    "frankenstein": (
        "*** START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN; OR, THE MODERN PROMETHEUS ***"
    ),
    "Lair of the White Worm": (
        "*** START OF THE PROJECT GUTENBERG EBOOK THE LAIR OF THE WHITE WORM ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE LAIR OF THE WHITE WORM ***"
    ),
    "The Jewel of Seven Stars": (
        "*** START OF THE PROJECT GUTENBERG EBOOK THE JEWEL OF SEVEN STARS ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE JEWEL OF SEVEN STARS ***"
    ),
    "The Last Man": (
        "*** START OF THE PROJECT GUTENBERG EBOOK THE LAST MAN ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE LAST MAN ***"
    ),
    "Mathilda": (
        "*** START OF THE PROJECT GUTENBERG EBOOK MATHILDA ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK MATHILDA ***"
    )
}

def process_text(file_path):
    markers_found = False
    for key in Markers:
        if key.lower() in file_path.lower():
            start_marker, end_marker = Markers[key]
            markers_found = True
            break
    if not markers_found:
        print(f"Markers not found for {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    if start_index == -1 or end_index == -1:
        print(f"Markers not found in {file_path}")
        sys.exit(1)

    content = text[start_index + len(start_marker):end_index].strip()
    words = re.findall(r'\b\w+\b', content.lower())  # Extract words, lowercased
    word_count = len(words)

    # Count and normalize target words
    word_frequencies = Counter(words)
    word_counts = {word: word_frequencies.get(word, 0) for word in target_words}
    normalized_counts = {word: (count / word_count if word_count > 0 else 0) for word, count in word_counts.items()}

    return normalized_counts
    
def calculate_total_difference(all_counts):
    total_difference = 0
    book_names = list(all_counts.keys())
    for i in range(len(book_names)):
        for j in range(i+1, len(book_names)):
            diff = sum(abs(all_counts[book_names[i]][word] - all_counts[book_names[j]][word]) for word in target_words)
            total_difference += diff
    return total_difference

def plot_results(all_counts, total_difference):
    plt.figure(figsize=(12, 8))

    for book_name, counts in all_counts.items():
        counts_list = [counts.get(word, 0) for word in target_words]
        plt.plot(target_words, counts_list, marker='o', label=book_name)
    
    plt.xlabel('Words')
    plt.ylabel('Normalized Count')
    plt.title('Power Spectrum of Word Usage Comparison')
    plt.legend()

    # Display total difference on the graph
    plt.text(0.5, 0.95, f"Total Difference Value: {total_difference:.4f}",
             ha='center', va='top', transform=plt.gca().transAxes, fontsize=12, color='red')

    plt.show()

def main():
    args = sys.argv[1:]
    if len(args) < 1 or len(args) > 6:
        print("Usage: python <script_name> <file1> <file2> [<file3> <file4> <file5> <file6>]")
        sys.exit(1)

    all_counts = {}
    for file_path in args:
        counts = process_text(file_path)
        all_counts[file_path] = counts
    
    total_difference = calculate_total_difference(all_counts)
    plot_results(all_counts, total_difference)

if __name__ == "__main__":
    main()