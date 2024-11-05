[![License](https://img.shields.io/badge/License-BSD\%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

# QuantPlasia

Well-coordinated events of epithelial differentiation are essential for the homeostasis and repair of the adult gastrointestinal tract epithelium. However, persistent GI tract repair, primarily due to prolonged inflammation causing factors such as GERD, and allergens in the esophagus, Helicobacter pylori infection in the stomach, inflammatory bowel disease, Crohn’s disease, and ulcerative colitis in the intestines, leads to aberrant epithelial homeostasis.

The resultant impaired epithelial differentiation eventually leads to 'Metaplasia'; a pre-cancerous condition. In the esophagus, it results in Barrett's metaplasia (often called either gastric or intestinal metaplasia depending on the cell types observed), where esophageal cells are replaced by gastric and/or intestinal cells. In the stomach, this often results in intestinal metaplasia and pseudopyloric or pyloric metaplasia, which may progress to spasmolytic polypeptide-expressing metaplasia (SPEM). Similarly, pyloric cell metaplasia has been observed in the small intestine and colon, while Paneth cell metaplasia occurs in the colon and rectum, and squamous cell metaplasia in the rectum.

Based on gene-expression dependent enrichment profiles obtained using GSEA, *QuantPlasia* identifies the existence of such metaplastic events and utilises the metric 'Degree of Differentiation' (here, 'Extent of Differentiation') to quantify the same [1, 2].

### Signatures of Interest

**Input File Pre-requisites**
* For cell signature identification, the file should be the GSEA output file in .tsv format

**Available Parameters**
* Input_File_CS : [string] path to the input file
* FDR_value : [float] FDR q-value threshold.
* Signatures : [list] keywords to identify the presence of associated signatures as they appear in GSEA output file

**Output**
* Reports the signatures associated with the keywords and the number of distinct signatures identified.

### Extent of Differentiation

**Input File Pre-requisites**
* The file must be the GSEA-leading edge analysis output saved in .xlsx format. 
* Before or after leading edge analysis, the 'Collapse Dataset' option should be used to obtain the mapping of Ensembl IDs or any other probe set used to obtain the respective gene names as GSEA output .tsv file.
* DiGeSt dataset is provided within the software, however for latest updates please refer to the GitHub page to ensure latest files are installed.

**Available Parameters**
* User_File : [string] path to the input file
* List_of_Signatures_of_Interest : [list] keywords associated with the signatures as they appear in GSEA output file

**Optional Parameters**
* Condition [string] : Default=None; Otherwise 'Inverse' to calculate the potential extent of differentiation from the perspective of signatures other than the previous user-defined list 
* Signatures_to_Omit [list] : Default=None; Otherwise additional list of signatures (usually signatures associated with tissue-resident cells) that the user may wish to omit while calculating the extent of differentiation when the Condition* is 'Inverse'.
* Tissue_Resident [string] : Default=None; Otherwise 'Yes' to calculate the extent of differentiation using the genes that are associated with the term 'Differentiation' as identified from 'GeneCards'. *Note: Applicable only to identify extent of differentiation from the perspective of tissue resident cell signatures.*
* Collapsed_Probe [string] : Default=None; Otherwise, user-input file path when *Tissue_Resident* is 'Yes'; contains collapsed probes from GSEA


**Output**
* Reports the extent of metaplasia associated differentiation as per user-defined conditions

**Installation**
```
pip install QuantPlasia
```

**Use Case 1**
```
#=============================Example Signature Extraction==========================#
from QuantPlasia import GSEA_CS_path, Signatures_Of_Interest

#This example is based on GSEA results on Stage II Esophageal Cancer

cell_signatures_file = GSEA_CS_path                                                                   #Input Path to Example File
Signatures = ['esophagus', 'esophageal', 'stomach', 'gastric', 'duodenum', 'duodenal', 'intestine']   #Keywords that appear in cell signatures module of GSEA

#Signatures_Of_Interest(Input_File_CS, FDR_value, Signatures)
Signatures_Of_Interest(cell_signatures_file, 0.05, Signatures) #FDR_value = 0.25 (minimum) or FDR_value = 0.05 (ideal)

```
**Use Case 2**
```
#=============================Example Extent of Differentiation for Tissue Non-Resident Cell Signatures==========================#
from QuantPlasia import GSEA_LEA_path, Extent_of_Differentiation

#This example is based on GSEA results on Stage II Esophageal Cancer

leading_edge_file,_,_ = GSEA_LEA_path()                                     #Input Path to Example File
Signatures = ['stomach', 'gastric', 'duodenum', 'duodenal', 'intestine']    #Keywords that appear in cell signatures module of GSEA

#Extent_of_Differentiation(User_File, List_of_Signatures_of_Interest)
Extent_of_Differentiation(leading_edge_file, Signatures)
```
**Use Case 3**
```
#==============Example Extent of Differentiation for Tissue Non-Resident Cell Signatures Other than Signatures of Interest ================#
from QuantPlasia import GSEA_LEA_path, Extent_of_Differentiation

#This example is based on GSEA results on Stage II Esophageal Cancer

leading_edge_file,_,_ = GSEA_LEA_path()                                                      #Input Path to Example File
Signatures = ['stomach', 'gastric', 'duodenum', 'duodenal', 'intestine', 'intestinal']     #Keywords that appear in cell signatures module of GSEA
Omitted_Signatures = ['esophagus', 'esophageal']

#Extent_of_Differentiation(User_File, List_of_Signatures_of_Interest, Condition, Signatures_to_Omit)
Extent_of_Differentiation(leading_edge_file, Signatures, Condition='Inverse', Signatures_to_Omit=Omitted_Signatures)
```
**Use Case 4**
```
#=============================Example Extent of Differentiation for Tissue Resident Cell Signatures==========================#
from QuantPlasia import GSEA_LEA_path, DiGeSt_GeneSet_path, Extent_of_Differentiation

#This example is based on GSEA results on Stage III Colon Cancer

_, leading_edge_file, Probe_file = GSEA_LEA_path()   #Input Path to Example File and Probe File
Signatures = ['intestine', 'intestinal']             #Keywords that appear in cell signatures module of GSEA
DIGEST_file = DiGeSt_GeneSet_path()                  #Input Path to DiGeSt Dataset

#Extent_of_Differentiation(User_File, List_of_Signatures_of_Interest, Tissue_Resident, Collapsed_Probe)
Extent_of_Differentiation(leading_edge_file, Signatures, Tissue_Resident='Yes', Collapsed_Probe=Probe_file)
```

**Expected Output**
* Use Case 2: The Extent of Differentiation for given conditions is 6.000
* Use Case 3: The Extent of Differentiation for given conditions is 4.978
* Use Case 4: The Extent of Differentiation for given conditions is 3.727

**References**  
[1] Subramanian A, Tamayo P, Mootha VK, Mukherjee S, Ebert BL, Gillette MA, et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proc Natl Acad Sci.2005;102(43):15545–50  
[2] Pravallika G, Rajasekaran R. Stage II oesophageal carcinoma: peril in disguise associated with cellular reprogramming and oncogenesis regulated by pseudogenes. BMC Genomics. 2024 Feb 2;25(1):135  

COPYRIGHT

Copyright (c) 2024, Pravallika Govada All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

CONTACT INFORMATION

Please address any queries or bug reports to Pravallika Govada at pravallika.govada2018@vitstudent.ac.in or pravallika2606g@gmail.com
