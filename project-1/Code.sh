#!/bin/bash

# Function to calculate average length
calculate_average_length() {
    local input_file="$1"
    awk '{ total += length($0) } END { print total / NR }' "$input_file"
}

# Step 1: Extract nucleotide sequences and store them in a new file
grep -o '[ATGC]*' ENCFF214BTG.txt > ENCFF214BTG_nucleotide_sequences.txt

# Calculate average length for the reference file
average_length=$(calculate_average_length "ENCFF214BTG_nucleotide_sequences.txt")

# Input file containing nucleotide sequences
input_file="ENCFF214BTG_nucleotide_sequences.txt"

# Output file to store cropped nucleotide sequences
cropped_file="ENCFF214BTG_cropped_sequences.txt"

# Discard sequences shorter than the average length and trim sequences longer than the average length
awk -v average_length="$average_length" '{ if (length($0) >= average_length) print substr($0, 1, average_length) }' "$input_file" > "$cropped_file"




# Sort the narrowpeak file
sort -k1,1 -k2,2n "ENCFF214BTG.bed" > sorted.bed


# Output file for negative regions
negative_regions_file="ENCFF214BTG_negative_regions.bed"


# Iterate through the sorted narrowpeak file
prev_end=0
while read -r chrom start end rest; do
    # Calculate middle region between consecutive accessible regions
    if [ "$prev_end" -ne 0 ]; then
        middle_start=$((prev_end + 1))
        middle_end=$((start - 1))
        # Output middle region if it exists
        if [ "$middle_end" -gt "$middle_start" ]; then
            echo "$chrom $middle_start $middle_end" >> "$negative_regions_file"
        fi
    fi
    prev_end="$end"
done < sorted.bed

# Remove temporary sorted file
rm sorted.bed



# Convert negative regions file to tab-separated format
awk '{$1=$1}1' OFS="\t" "$negative_regions_file" > "${negative_regions_file%.*}_tab.bed"

# Use bedtools to extract nucleotide sequences from negative regions
bedtools getfasta -fi /users/Yudhisha/reference/hg38.fa -bed "${negative_regions_file%.*}_tab.bed" -fo "${negative_regions_file%.*}.txt"

# Extract nucleotide sequences and store them in a new file
grep -o '[ATGC]*' "${negative_regions_file%.*}.txt" > "${negative_regions_file%.*}_nucleotide_sequences.txt"

# Input file containing nucleotide sequences
neg_input_file="${negative_regions_file%.*}_nucleotide_sequences.txt"

# Output file to store cropped nucleotide sequences
neg_cropped_file="${negative_regions_file%.*}_cropped_sequences.txt"

# Discard sequences shorter than the average length and trim sequences longer than the average length
awk -v neg_average_length="$average_length" '{ if (length($0) >= neg_average_length) print substr($0, 1, neg_average_length) }' "$neg_input_file" > "$neg_cropped_file"







