```
//////////////////////////////////////////////////////////////
//     ______           __     ___      ____________    __  //
//    / ____/___ ______/ /_   |__ \    / ____/ ___/ |  / /  //
//   / /_  / __ `/ ___/ __/   __/ /   / /    \__ \| | / /   //
//  / __/ / /_/ (__  ) /_    / __/   / /___ ___/ /| |/ /    //
// /_/____\__,_/____/\__/   /____/   \____//____/ |___/     //
//   / ____/___  ____ _   _____  _____/ /____  _____        //
//  / /   / __ \/ __ \ | / / _ \/ ___/ __/ _ \/ ___/        //
// / /___/ /_/ / / / / |/ /  __/ /  / /_/  __/ /            //
// \____/\____/_/ /_/|___/\___/_/   \__/\___/_/             //
//                                                          //
//////////////////////////////////////////////////////////////

```

## FastA or FastQ to CSV Converter

Let's face it: CSVs still rule our lives. Whether is finance, 'databases', and even DNA sequences, they are ubiquitious in our lives.
While scientists prefer to use common formats like FastA and FastQ to store DNA oligo or sequencing data, nonetheless you'll need a program like SnapGene, ApE, or Geneious.
Though most scientists have at least one of those programs, this script will parse through the FastA or FastQ program and convert it to an universal format like CSV.

This script takes in a FastA or FastQ file and output:
1. Name
2. Sequence

With the optional '-p' option, it will also output the fllowing informatio in the same file:

3. Length
4. GC content (%)
5. Melting Temperature (&deg;C)
6. Molecular Weight (g/mol)

## Requirements
### Required dependecies 
Dependencies for script:
```
python 3.2 or above
pandas 2.2.1 or above
```
The rest are standard Python libraries.

#### Running the script
```
python fast2csv.py filename.fasta [-p]
python fast2csv.py filename.fastq [-p]
```

### Examples
#### Input FastA file

\>DNA1<br>ATCGATCG

\>DNA2<br>TACGGCAG<br>GAACCTGA

#### Output CSV file without the '-p' option.
| Name      | Sequence           |
| :---      | :---               |
|DNA1       |  ATCGATCG          |
|DNA2       |  TACGGCAGGAACCTGA  |

#### Output CSV file with the '-p' option.

| Name      | Sequence           | Length  | GC (%)   | Melting Temp  | MW (g/mol)   |
| :---      | :---               | :---    | :---     | :---          | :---         |
|DNA1       |  ATCGATCG          | 8       | 50       | 24            | 2409.64      |
|DNA2       |  TACGGCAGGAACCTGA  | 16      | 56.2     | 45.9          | 4915.24      |

