import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
        description = ("A FastA and FastQ parser that converts it to a CSV file with names and sequences. "
                        "Optional '-p' input after file also provides new columns with DNA info including "
                        "length, GC%%, Tm in celcius, and MW in g/mol."
                        ),
        epilog = "Outputs a CSV file with two columns: 'Name' and 'Sequence'"
                                )

parser.add_argument("file", metavar = "-file", help = "A FastA or FastQ file. \n"
                                                        "Accepts common extensions including '.fa', '.fq'"
                    )

parser.add_argument("-p", "--properties", action = "store_true",
                    help = "optional argument placed after the file that adds 4 columns with: lenght, GC%%, Tm, and MW (g/mol)"
                    )

args = parser.parse_args()

def fasta_to_csv(fasta_input):
    fasta_dict = fastA_to_pd(fasta_input)
    df1 = pd.DataFrame(fasta_dict.items(), columns = ["Name", "Sequence"])
    df1.to_csv("FastA_Sequences.csv", encoding = "utf-8", index = False)
    print("Successfully converted the FastA file to CSV")

def fasta_to_pd(fasta_input):
    fasta_dict = fastA_to_pd(fasta_input)
    df1 = pd.DataFrame(fasta_dict.items(), columns = ["Name", "Sequence"])
    df1["Length"] = df1["Sequence"].apply(seq_length)
    df1["GC(%)"], df1["Melting Temp"], df1["MW (g/mol)"] = zip(*df1["Sequence"].apply(seq_info))
    df1.to_csv("FastA_Sequences.csv", encoding = "utf-8", index = False)
    print("Successfully converted the FastA file to CSV")

def fastq_to_csv(fastq_input):
    fastq_dict = fastQ_to_pd(fastq_input)
    df2 = pd.DataFrame(fastq_dict.items(), columns = ["Name", "Sequence"])
    df2.to_csv("FastQ_Sequences.csv", encoding = "utf-8", index = False)
    print("Successfully converted the FastQ file to CSV")

def fastq_to_pd(fastq_input):
    fastq_dict = fastQ_to_pd(fastq_input)
    df2 = pd.DataFrame(fastq_dict.items(), columns = ["Name", "Sequence"])
    df2["Length"] = df2["Sequence"].apply(seq_length)
    df2["GC(%)"], df2["Melting Temp"], df2["MW (g/mol)"] = zip(*df2["Sequence"].apply(seq_info))
    df2.to_csv("FastQ_Sequences.csv", encoding = "utf-8", index = False)
    print("Successfully converted the FastQ file to CSV")
    
def fastA_to_pd(file_input):
    #create empty dictionary
    parsed_dict = {}
    
    try:
        with open(file_input, "r") as file:
            #Initialize seq_id and seq_sequence
            seq_id = None
            seq_cont = []
        
            for line in file:
                #Take first line and strip it
                line = line.strip()
            
                #Checks if the FastA line starts with '.'
                if line.startswith(">"):
                    if seq_id is not None:
                        parsed_dict[seq_id] = "".join(seq_cont)
                
                    seq_id = line[1:]
                    seq_cont = []
                
                    continue
            
                seq_cont.append(line)
        
            parsed_dict[seq_id] = "".join(seq_cont)
        
        return parsed_dict
    except:
        return "Not a valid FastA file"

def fastQ_to_pd(file_input_2):
    #Start empty dict
    parsed_fastq = {}
    
    try:
        with open(file_input_2, "r") as file3:
            #Makes sures to keep on looping until there are no more '@' lines
            while True:
                #First line should the the header
                header = file3.readline().strip()
                if not header:
                    break
                #Second line should be sequence
                sequence = file3.readline().strip()
                #Third line is '+' and fourth line is seq quality to ignore
                _ = file3.readline().strip()
                _ = file3.readline().strip()
                
                #Add sequence name and sequence to dictionary
                parsed_fastq[header[1:]] = sequence
            
            return parsed_fastq 
    except:
        return "Not a compatible FastQ file"

def seq_length(sequence):
    #Returns the DNA sequence length
    return len(sequence)

def seq_info(sequence):
    #Calculates the properties of the DNA sequence. 
    num_a = 0
    num_t = 0
    num_c = 0
    num_g = 0
    num_n = 0
    
    sequence = sequence.strip()
    sequence = list(str(sequence.upper()))
    #Each nucleotide is counted. Except for N which is then added to the list but not used.
    for nuc in sequence:
        if nuc == "A":
            num_a += 1
        elif nuc == "T":
            num_t += 1
        elif nuc == "C":
            num_c += 1
        elif nuc == "G":
            num_g += 1
        else:
            num_n += 1
    
    #Calculates the DNA GC content.
    try:
        seq_gc = 100 * ((num_g + num_c) / (num_g + num_c + num_a + num_t + num_n))
    
    except ZeroDivisionError:
        seq_gc = int(0)
    
    #Calculate the molecular weight
    mol_weight = ((num_a * 313.2) + (num_t * 304.2) + (num_g * 329.2) + (num_c * 289.2) + (num_n * 303.7) - 61.96)
    
    #Special case if length is less than 14
    if len(sequence) < 14:
        temp_melt = round((num_a + num_t)*2 + (num_g + num_c)*4, 2)
    #Results for all others ased on published data
    else:
        temp_melt = round(64.9 + 41*((num_g + num_c - 16.4)/(num_a + num_t + num_c + num_g)), 1)
    
    return round(seq_gc,1), temp_melt, mol_weight 
        
if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            #Checks if there are more than 2 command line iputs
            if len(sys.argv) == 2:
                if sys.argv[1].endswith((".fasta", ".fastA", ".FastA", ".FASTA", ".fa", ".FA", ".fas", ".FAS", ".fna", ".FNA", ".faa", ".FAA")):
                    df = fasta_to_csv(sys.argv[1])
                elif sys.argv[1].endswith((".fastQ", ".FASTQ", ".fastq", ".FastQ")):
                    df = fastq_to_csv(sys.argv[1])
                else:
                    raise FileNotFoundError
            #Checks if there are 3 command line inputs and if one of them is the 'properties' option
            elif len(sys.argv) == 3 and sys.argv[2] == "-p":
                if sys.argv[1].endswith((".fasta", ".fastA", ".FastA", ".FASTA", ".fa", ".FA", ".fas", ".FAS", ".fna", ".FNA", ".faa", ".FAA")):
                   df = fasta_to_pd(sys.argv[1])
                elif sys.argv[1].endswith((".fastQ", ".FASTQ", ".fastq", ".FastQ", ".fq", ".FQ")):
                    df = fastq_to_pd(sys.argv[1])
                else:
                    raise FileNotFoundError
            else:
                raise FileNotFoundError
        else:
            raise IOError
                
    except (FileNotFoundError, IOError):
        sys.exit("The file does not exists or it is not an acceptable input file, incorrect arguments, or too many inputs. Check file extension")