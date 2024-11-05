# Author: Pravallika Govada

# Contact: pravallika2606g@gmail.com

import os
import pandas as pd
import copy
from copy import deepcopy
import itertools
import csv
from pathlib import Path
import time

import importlib.resources as ExRes

def GSEA_CS_path():
    GSEA_CS_file_path = ExRes.files('QuantPlasia.data') / 'Cell Signatures' / 'GSEA_output.tsv'
    return str(GSEA_CS_file_path)

def GSEA_LEA_path():
    GSEA_LEA_file_path = ExRes.files('QuantPlasia.data') / 'Extent of Differentiation' /'GSEA_LEA_Output.xlsx'
    GSEA_LEA_COAD_file_path = ExRes.files('QuantPlasia.data') / 'Extent of Differentiation' /'GSEA_LEA_Output_COAD.xlsx'
    Collapsed_Probes_path = ExRes.files('QuantPlasia.data') / 'Extent of Differentiation' /'Collapsed_Probes.tsv'
    return str(GSEA_LEA_file_path), str(GSEA_LEA_COAD_file_path), str(Collapsed_Probes_path)

def DiGeSt_GeneSet_path():
    DiGeSt_path = ExRes.files('QuantPlasia.data') / 'Extent of Differentiation' /'DiGeSt.txt'
    return str(DiGeSt_path)

def Signatures_Of_Interest(Input_File_CS, FDR_value, Signatures):
    '''Returns the number of cell signatures or any other variables based on user-defined list for a given FDR q-value
       Args:
           Input_File_CS: File containing the results of GSEA output of any MSigDB module
           FDR_value: User-defined False Discovery Rate q-value as defined by GSEA
           Signatures: List of Signatures as they appear in GSEA output
        Returns:
           Cell Signatures and the number of times they appear in the GSEA output
    '''
    start_time = time.time()
    if '.tsv' not in os.path.basename(Input_File_CS):
        raise AssertionError("Expected File type is .tsv from GSEA Output")
    CSFile = pd.read_csv(Input_File_CS, sep='\t')
    CSFile_SelCS_Copy = pd.DataFrame(columns=CSFile.columns)
    CSFile_Sel=CSFile.loc[CSFile['FDR q-val'] <= FDR_value]
    All_List=[]
    for User_Signature in Signatures:
        User_Signature=User_Signature.upper()
        CSFile_SelCS=CSFile_Sel[CSFile_Sel["NAME"].str.contains(User_Signature, regex=False)]
        X=list(CSFile_SelCS["NAME"])
        print(f"\nNumber of cell signatures associated with the key word {User_Signature} are {len(X)}")
        CSFile_SelCS_Copy=CSFile_SelCS_Copy._append(CSFile_SelCS,ignore_index=True)
    CSFile_SelCS_Copy=CSFile_SelCS_Copy.loc[:,CSFile_SelCS_Copy.columns.isin(['NAME','ES','NES','FDR q-val'])]
    elapsed_time = time.time() - start_time
    print(f"\nQuantPlasia estimated the signatures in {elapsed_time:.2f} seconds")
    return

def Extent_of_Differentiation(User_File, List_of_Signatures_of_Interest, **kwargs):
    '''Returns Degree of Differentiation as described previously in # PMID: 38308202
       Args:
           User_File: User File created by using Leading Edge Analysis by GSEA of all signatures under the desired FDR q-value.
           List_of_Signatures_of_Interest: User-defined list of signatures
           **kwargs: Additional optional keyword arguments.
               - Condition (str, optional): If 'Inverse', calculates the degree of differentiation from the perspective of signatures other than that of the user-defined list 
               - Signatures_to_Omit (list, optional): Additional list of signatures that the user can omit while calculating the extent of differentiation for the 
                                                      condition 'Inverse'
               - Tissue_Resident (str, optional): If 'Yes', calculates the extent / degree of differentiation only for the genes that are associated with the term 
                                                  'Differentiation' as identified from 'GeneCards'
               - Collapsed_Probe (str, optional): User-input file path when the Tissue_Resident Differentiation is 'Yes'; contains collapsed probes from GSEA
       Returns:
           Degree of Differentiation as numerical value depending on the user-condition
    '''
    start_time = time.time()
    User_File=pd.read_excel(User_File)
    column_names=list(User_File.iloc[1])
    User_File.columns=column_names
    User_File=User_File.drop(User_File.index[:2])
    User_File = User_File.drop('Description', axis=1).reset_index(drop=True)
    CSignDF=deepcopy(User_File)
    Non_CSignDF=deepcopy(User_File)

    Tissue_Resident = kwargs.get('Tissue_Resident', None)
    Collapsed_Probe = kwargs.get('Collapsed_Probe', None)
    if Tissue_Resident==None:
        pass
    elif Tissue_Resident==None and Collapsed_Probe!=None:
        raise AssertionError("Please remove collapsed probe file and try again")
    elif Tissue_Resident=='Yes' and Collapsed_Probe==None:
        raise AssertionError("Please ensure both input files for collapsed probes and DiGeSt are provided")
    elif Tissue_Resident=='Yes' and Collapsed_Probe!=None:
        Differentiation_assoiated_File=DiGeSt_GeneSet_path()
        Collapsed_Probe_File=Collapsed_Probe
    
    Desired_List = [x.upper() for x in List_of_Signatures_of_Interest]

    Signatures_to_Omit = kwargs.get('Signatures_to_Omit', None)

    if Signatures_to_Omit!=None:
        Signatures_to_Omit = [y.upper() for y in Signatures_to_Omit]
        for droppings in Desired_List:
            Non_CSignDF = Non_CSignDF[Non_CSignDF["Name"].str.contains(droppings) == False]
            Non_CSignDF.reset_index(inplace=True)
            Non_CSignDF=Non_CSignDF.drop('index',axis=1)
        for droppings_1 in Signatures_to_Omit:
            Non_CSignDF = Non_CSignDF[Non_CSignDF["Name"].str.contains(droppings_1) == False]
            Non_CSignDF.reset_index(inplace=True)
            Non_CSignDF=Non_CSignDF.drop('index',axis=1)
        UnDesiredList=list(Non_CSignDF["Name"])
        for droppings_2 in UnDesiredList:
            CSignDF = CSignDF[CSignDF["Name"].str.contains(droppings_2) == False]
            CSignDF.reset_index(inplace=True)
            CSignDF=CSignDF.drop('index',axis=1)
        for droppings_3 in Signatures_to_Omit:
            CSignDF = CSignDF[CSignDF["Name"].str.contains(droppings_3) == False]
            CSignDF.reset_index(inplace=True)
            CSignDF=CSignDF.drop('index',axis=1)
    elif Signatures_to_Omit==None:
        for droppings in Desired_List:
            Non_CSignDF = Non_CSignDF[Non_CSignDF["Name"].str.contains(droppings) == False]
            Non_CSignDF.reset_index(inplace=True)
            Non_CSignDF=Non_CSignDF.drop('index',axis=1)
        UnDesiredList=list(Non_CSignDF["Name"])
        for droppings_1 in UnDesiredList:
            CSignDF = CSignDF[CSignDF["Name"].str.contains(droppings_1) == False]
            CSignDF.reset_index(inplace=True)
            CSignDF=CSignDF.drop('index',axis=1)

    Condition = kwargs.get('Condition', None)
    if Condition==None and Tissue_Resident=='Yes':
        GeneSetColumn = CSignDF.columns[0]
        BNames=os.path.basename(Differentiation_assoiated_File)
        if BNames.endswith('.txt') or BNames.endswith('.tsv'):
            pass
        else:
            raise AssertionError("Please provide a valid input file")        
        Diff_Genes=pd.read_csv(Differentiation_assoiated_File, sep='\t')
        Collapsed_Probe_GSEA=pd.read_csv(Collapsed_Probe_File, sep='\t') 
        print(f"\nUnfiltered Collapsed Dataset has {Collapsed_Probe_GSEA.shape[0]} genes \n")
        filtered_DGeneProbes = pd.merge(Collapsed_Probe_GSEA, Diff_Genes, left_on='MATCHING PROBE SET(S)', right_on='Gene_ID', how='inner')
        print(f"\nFiltered Collapsed Dataset has {filtered_DGeneProbes.shape[0]} differentiation-associated genes \n")
        filtered_DGeneProbes = filtered_DGeneProbes.drop(columns=['Gene_ID'])
        filtered_DGeneProbes_Names = filtered_DGeneProbes['NAME'].tolist()
        filtered_DGeneProbes_Names = [col for col in filtered_DGeneProbes_Names if col in CSignDF.columns]
        Final_ColumnNames = [GeneSetColumn] + filtered_DGeneProbes_Names
        filtered_CSignDF = CSignDF[Final_ColumnNames]
        CellSign_Names=filtered_CSignDF["Name"]
        FileTra=filtered_CSignDF.T
        FileTra.columns=CellSign_Names
        FileTra=FileTra[1:]
        Compare_Col = [0]*len(FileTra[CellSign_Names[0]])
        FileTra.insert(0,"Compare_Col", Compare_Col,True)
        CellSign_Names_1_or_0=[]
        for i in CellSign_Names:
            New=i+str("_1_or_0")
            CellSign_Names_1_or_0.append(New)
            FileTra[New] = FileTra.apply(lambda row: 0 if row[i] == row["Compare_Col"] else 1 if row[i] != row["Compare_Col"] else -1, axis=1)
        FileTra_Copy=deepcopy(FileTra[CellSign_Names_1_or_0])
        FileTra_Copy["SUM"]=FileTra_Copy.sum(axis=1)
        Final_DF = deepcopy(FileTra_Copy[FileTra_Copy['SUM'] > 1])
        Final_DF.loc[len(Final_DF.index)]=Final_DF.sum(axis=0)
        FinColL=[]
        for j in Final_DF.columns:
            if Final_DF[j].sum()==0:
                FinColL=FinColL
            elif Final_DF[j].sum()!=0:
                FinColL.append(j)
        #print(f"\nNumber of Genes = {(len(Final_DF['SUM'])-1)} and Number of Cell Signatures = {(len(FinColL)-1)} \n")
    elif Condition==None and Tissue_Resident==None:
        CellSign_Names=CSignDF["Name"]
        FileTra=CSignDF.T
        FileTra.columns=CellSign_Names
        FileTra=FileTra[1:]
        Compare_Col = [0]*len(FileTra[CellSign_Names[0]])
        FileTra.insert(0,"Compare_Col", Compare_Col,True)
        CellSign_Names_1_or_0=[]
        for i in CellSign_Names:
            New=i+str("_1_or_0")
            CellSign_Names_1_or_0.append(New)
            FileTra[New] = FileTra.apply(lambda row: 0 if row[i] == row["Compare_Col"] else 1 if row[i] != row["Compare_Col"] else -1, axis=1)
        FileTra_Copy=deepcopy(FileTra[CellSign_Names_1_or_0])
        FileTra_Copy["SUM"]=FileTra_Copy.sum(axis=1)
        Final_DF = deepcopy(FileTra_Copy[FileTra_Copy['SUM'] > 1])
        Final_DF.loc[len(Final_DF.index)]=Final_DF.sum(axis=0)
        FinColL=[]
        for j in Final_DF.columns:
            if Final_DF[j].sum()==0:
                FinColL=FinColL
            elif Final_DF[j].sum()!=0:
                FinColL.append(j)
        #print(f"\nNumber of Genes = {(len(Final_DF['SUM'])-1)} and Number of Cell Signatures = {(len(FinColL)-1)}")
    elif Condition=='Inverse':
        CellSign_Names=Non_CSignDF["Name"]
        FileTra=Non_CSignDF.T
        FileTra.columns=CellSign_Names
        FileTra=FileTra[1:]
        Compare_Col = [0]*len(FileTra[CellSign_Names[0]])
        FileTra.insert(0,"Compare_Col", Compare_Col,True)
        CellSign_Names_1_or_0=[]
        for i in CellSign_Names:
            New=i+str("_1_or_0")
            CellSign_Names_1_or_0.append(New)
            FileTra[New] = FileTra.apply(lambda row: 0 if row[i] == row["Compare_Col"] else 1 if row[i] != row["Compare_Col"] else -1, axis=1)
        FileTra_Copy=deepcopy(FileTra[CellSign_Names_1_or_0])
        FileTra_Copy["SUM"]=FileTra_Copy.sum(axis=1)
        Final_DF = deepcopy(FileTra_Copy[FileTra_Copy['SUM'] > 1])
        Final_DF.loc[len(Final_DF.index)]=Final_DF.sum(axis=0)
        FinColL=[]
        for j in Final_DF.columns:
            if Final_DF[j].sum()==0:
                FinColL=FinColL
            elif Final_DF[j].sum()!=0:
                FinColL.append(j)
    print(f"\nNumber of Genes = {(len(Final_DF['SUM'])-1)} and Number of Cell Signatures = {(len(FinColL)-1)}")
    Reporting_DegODiff=(len(Final_DF['SUM'])-1)/(len(FinColL)-1)
    print(f"\nThe Extent of Differentiation for given conditions is {Reporting_DegODiff:.3f}.")
    elapsed_time = time.time() - start_time
    print(f"\nQuantPlasia completed estimating extent of differentiation in {elapsed_time:.2f} seconds")
    return