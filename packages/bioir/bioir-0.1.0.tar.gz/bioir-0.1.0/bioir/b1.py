print("""with open(fasta_file) as file:
    lines = file.readlines()
    print(lines)

sequence = ''

with open(fasta_file) as file:
    lines = file.readlines()
    sequence = ''.join(line.strip() for line in lines[1:]).upper()


a_count = sequence.count('A')
t_count = sequence.count('T')

total_count = len(sequence)

at_percent = ((a_count + t_count) * 100) / total_count 

g_count = sequence.count('G')
c_count = sequence.count('C')

gc_percent = ((g_count + c_count)*100)/total_count

at_percent / gc_percent

start_codon = 'ATG'
# stop_codon = 'TAA'
stop_codons = ['TAA', 'TAG', 'TGA']

start_index = sequence.find(start_codon)

coding_region = []

while start_index != -1:

    for stop_codon in stop_codons:
        stop_index = sequence.find(stop_codon,start_index+3)

        if stop_index != -1 and (stop_index - start_index) % 3 == 0:
            coding_seq = sequence[start_index:stop_index+3]
            coding_region.append(coding_seq)
            break

    start_index = sequence.find(start_codon,start_index+1)


motif = 'TATAA'

start_index = sequence.find(motif)

while start_index != -1:

    print(f"Motif '{motif}' found at positions {start_index}")

    start_index = sequence.find(motif,start_index+1)""")