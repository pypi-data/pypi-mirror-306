# Author: Pravallika Govada

# Contact: pravallika2606g@gmail.com

import os
import pandas as pd
import copy
import itertools
import csv
from pathlib import Path
import time

import importlib.resources as ExRes

def load_example_data_path():
    # This will return the path to the example CSV file
    example_file_path = ExRes.files('POpCan.data') / 'Example.csv'
    return str(example_file_path)  # Convert to string for easier use

def get_output_path():
    home_dir = Path.home()
    downloads_path = home_dir / 'Downloads'

    if downloads_path.exists() and downloads_path.is_dir():
        return downloads_path
    else:
        raise FileNotFoundError("Downloads folder not found.")

def Find_Overlap(GeneSet_Multiple, Condition, Output_Path):
    '''Returns a file of comma separated values indicating the extent of overlap between multiple user-defined conditions
        having sub-categories and the respective entries that are overlapping
       Args:
           GeneSet_Multiple: A file containing the genes or any other variables that are to be compared between two or more
                               cancer types / disease conditions having multiple sub-categories                    
           Condition: Either 'Between' or 'within'; Between will find overlap only between sub-categories of two main
                       cancer types / conditions, while within will compare the overlap between the sub-categories
                       of same cancer type / disease condition
        Returns:
            Percentage overlap and assoiciated gene list (can be other variables too)
    '''
    start_time = time.time()
    GeneSet_Multiple = pd.read_csv(GeneSet_Multiple)
    Output_Path = Path(Output_Path)
    Header_List = list(GeneSet_Multiple.columns.values)
    HL = len(Header_List)
    GeneListDict = {}
    for i in Header_List:
        GeneListDict[i] = []
        ith_Column = GeneSet_Multiple[i].tolist()
        filtered_ith_Column = [x for x in ith_Column if str(x) != 'nan']
        GeneListDict[i].extend(filtered_ith_Column)

    LCT, LS, TD=[], [], []
    
    def type_stage_dys():
        '''Returns three different lists to calculate the number of conditions to perform and identify extent of overlap
           Args: 
               User File
           Returns: 
               Three different lists for cancer type (or disease type), first sub-category (such as stage) and
                       second sub-category (such as expression type)
        '''
        for j in Header_List:
            k, k1, k2=j.split("_")[0],j.split("_")[1],j.split("_")[2]
            if k not in LCT:
                if len(k)==4:
                    LCT.append(k)
                else:
                    raise KeyError("Please refer to documentation to appropriately name column headers")
            if k1 not in LS:
                LS.append(k1)
            if k2 not in TD:
                TD.append(k2)
        return LCT,LS,TD
    
    CanTypeList={}
    def mk_multiCanDict():
        '''Reads and returns a list of conditions provided by the user
           Args: 
               LCT list generated from previous function
           Returns: 
               A list of cancer types / disease types and their 4-letter coded acronyms
        '''
        for l in LCT:            
            CanTypeList[l]=[]
            for L in Header_List:
                if L[:4]==l:
                    CanTypeList[l].append(L)
                else:
                    pass
        return CanTypeList

    Dysregulation_repititions, CSDCombValList, TotalCombs=[], [], []

    def combination_number_between():
        '''Generates the number of combinations needed to perform and identify overlap if the user specified condition
            is 'Between'
            Args: 
                LCT, LS and TD lists generated from previous function
            Returns: 
                The number of combinations needed to calculate percentage overlap
        '''
        for CanType in CanTypeList.keys():
            for ToD in TD: 
                ToD_number=sum(ToD in CanSD_Combo for CanSD_Combo in list(CanTypeList[CanType]))
                Dysregulation_repititions.append(ToD_number)
            
        List_of_AllCanDys=list(itertools.zip_longest(*[iter(Dysregulation_repititions)]*(len(TD))))
        CanSD_Values = {LCT[CancerType]: List_of_AllCanDys[CancerType] for CancerType in range(len(LCT))}

        CanSD_Values_copy=copy.deepcopy(CanSD_Values)
        LCT_Copy=copy.deepcopy(LCT)
        
        for ChosenCanType in CanSD_Values.keys():
            if len(CanSD_Values_copy) > 1:
                print(f"Calculating Combinations for {ChosenCanType}...\n")
                if ChosenCanType in LCT_Copy:
                    CombValList=[]
                    Current_List=CanSD_Values_copy[ChosenCanType]
                    Index_val=LCT_Copy.index(ChosenCanType)
                    del LCT_Copy[Index_val]
                    del CanSD_Values_copy[ChosenCanType]
                    for CanSD_val in Current_List:
                        for Giv_CancerType in CanSD_Values_copy.keys():
                            for Next_CanSD_val in CanSD_Values_copy[Giv_CancerType]:
                                CombVal=CanSD_val*Next_CanSD_val
                                CombValList.append(CombVal)
                CSDCombValList.append(sum(CombValList))
                Current_TotalCombs=sum(CSDCombValList)
            elif len(CanSD_Values_copy) == 1:
                print(f"No need to calculate further for {ChosenCanType}\n")
                TotalCombs.append(sum(CSDCombValList))
                print(f"Total possible combinations is {TotalCombs}\n")
        return TotalCombs

    Percentage_Values, KEYCANLIST=[], []

    def overlapping_percentage_between():
        '''Generates a file of comma separated values depicting the percentage overlap
            Args: 
                Combination number and multiple lists from previous function to generate copies for further processing
            Returns: 
                Percentage overlap of variables between user-defined condition
        '''
        Percentage_Overlapping = pd.DataFrame(data = None)
        Column_Header=['SetA','SetB','Overlapping_Percentage','Number_of_Genes','Gene_List']
        Percentage_Overlapping = pd.concat([Percentage_Overlapping, pd.DataFrame([Column_Header])], ignore_index=True)
        GLD_New=copy.deepcopy(GeneListDict)
        CanTypeList_New=copy.deepcopy(CanTypeList)
        
        all_values=0

        for n in GeneListDict.keys():
            if all_values < TotalCombs[0]:
                if n[:4] in CanTypeList_New.keys():
                    SetA=set(GeneListDict[n])
                    KEYCANLIST=list(CanTypeList_New[n[:4]])
                    for N in KEYCANLIST:
                        if N in GLD_New:
                            del GLD_New[N]
                        else:
                            pass
                    for o in GLD_New:
                        SetB=set(GLD_New[o])
                        intersection_of_entries = SetA.intersection(SetB)
                        IOEntries=(list(intersection_of_entries))
                        overlap = len(IOEntries)
                        List1 = len(SetA)
                        List2 = len(SetB)
                        perc = (overlap/((List1+List2)-overlap))*100
                        Percentage_Values.append(perc)
                        IOEntries_List=[]
                        IOEntries_List.append(n)
                        IOEntries_List.append(o)
                        IOEntries_List.append(perc)
                        IOEntries_List.append(len(IOEntries))
                        IOEntries_List.append(IOEntries)
                        Percentage_Overlapping = pd.concat([Percentage_Overlapping, pd.DataFrame([IOEntries_List])], ignore_index=True)
                    KEYCANLIST.remove(n)
                    CanTypeList_New[n[:4]]=KEYCANLIST
                    if len(CanTypeList_New[n[:4]])==0:
                        del CanTypeList_New[n[:4]]
                    else:
                        pass
                else:
                    GLD_New=GLD_New
                    for O in GLD_New:
                        SetB1=set(GLD_New[O])
                        intersection_of_entries = SetA.intersection(SetB1)
                        IOEntries1=(list(intersection_of_entries))
                        overlap = len(IOEntries1)
                        List1 = len(SetA)
                        List2 = len(SetB1)
                        perc = (overlap/((List1+List2)-overlap))*100
                        Percentage_Values.append(perc)
                        IOEntries1_List=[]
                        IOEntries1_List.append(n)
                        IOEntries1_List.append(O)
                        IOEntries1_List.append(perc)
                        IOEntries1_List.append(len(IOEntries1))
                        IOEntries1_List.append(IOEntries1)
                        Percentage_Overlapping = pd.concat([Percentage_Overlapping, pd.DataFrame([IOEntries1_List])], ignore_index=True)
                        
                        all_values=len(Percentage_Values)
            
            #Save Analysis File
            output_file_path = Output_Path / "POpCan_Between.csv"
            Percentage_Overlapping.to_csv(output_file_path, index=False)


        print(f"Percentage Overlap has been calculated between disease type including their subcategories.\n")
        elapsed_time = time.time() - start_time
        print(f"POpCan completed in {elapsed_time:.2f} seconds")              
        return Percentage_Values

    CancerType_for_within, CancerStageType_for_within=[], []
  
    def combination_number_within():
        '''Generates the number of combinations needed to perform and identify overlap if the user specified condition is 'Within'
            Args: 
                LCT, LS and TD lists generated from previous function
            Returns: 
                The number of combinations needed to calculate percentage overlap
        '''
        for CanType in CanTypeList.keys():
            for ToD in TD: 
                ToD_number=sum(ToD in CanSD_Combo for CanSD_Combo in list(CanTypeList[CanType]))
                Dysregulation_repititions.append(ToD_number)
            
        for CanTypeW in LCT:
            for ToDW in TD:
                NewType=str(CanTypeW)+'_'+str(ToDW)
                CancerType_for_within.append(NewType)
            
        CanSD_Values = {CancerType_for_within[CancerType]: Dysregulation_repititions[CancerType] for CancerType in range(len(CancerType_for_within))}
            
        CanSD_Values_copy=copy.deepcopy(CanSD_Values)
        CancerType_for_within_Copy=copy.deepcopy(CancerType_for_within)

        for ChosenCanType in CanSD_Values.keys():
            if len(CanSD_Values_copy) > 1:
                print("Calculating Combinations for",ChosenCanType,"...", '\n')
                if ChosenCanType in CancerType_for_within_Copy:
                    CombValList=[]
                    CurrentVal=CanSD_Values_copy[ChosenCanType]
                    if CurrentVal > 0:
                        SumWithinDys=0
                        for WithinDys in range(0,CurrentVal):
                            SumWithinDys+=WithinDys
                        CombValList.append(SumWithinDys)
                    elif CurrentVal == 0:
                        CombValList.append(CurrentVal)
                    Index_val=CancerType_for_within_Copy.index(ChosenCanType)
                    del CancerType_for_within_Copy[Index_val]
                    del CanSD_Values_copy[ChosenCanType]
                    for Giv_CancerType in CanSD_Values_copy.keys():
                        NextVal=CanSD_Values_copy[Giv_CancerType]
                        CombVal=(CurrentVal*NextVal)
                        CombValList.append(CombVal)
                CSDCombValList.append(sum(CombValList))
                Current_TotalCombs=sum(CSDCombValList)
            elif len(CanSD_Values_copy) == 1:
                print("Calculating Combinations for",ChosenCanType,"...", '\n')
                if ChosenCanType in CancerType_for_within_Copy:
                    CombValList=[]
                    CurrentVal=CanSD_Values_copy[ChosenCanType]
                    if CurrentVal > 0:
                        SumWithinDys=0
                        for WithinDys in range(0,CurrentVal):
                            SumWithinDys+=WithinDys
                        CombValList.append(SumWithinDys)
                    elif CurrentVal == 0:
                        CombValList.append(CurrentVal)
                CSDCombValList.append(sum(CombValList))
                Current_TotalCombs=sum(CSDCombValList)
                TotalCombs.append(sum(CSDCombValList))
                print(f"Total possible combinations is {TotalCombs}\n")
        return TotalCombs

    Percentage_Values, KEYCANLIST=[], []        
        
    def overlapping_percentage_within():
        '''Generates a file of comma separated values depicting the percentage overlap
            Args: 
                Combination number and multiple lists from previous function to generate copies for further processing
            Returns: 
                Percentage overlap of variables between user-defined condition
        '''
        Percentage_Overlapping = pd.DataFrame(data = None)
        Column_Header=['SetA','SetB','Overlapping_Percentage','Number_of_Genes','Gene_List']
        Percentage_Overlapping = pd.concat([Percentage_Overlapping, pd.DataFrame([Column_Header])], ignore_index=True)
        GLD_New=copy.deepcopy(GeneListDict)
        CanTypeList_New=copy.deepcopy(CanTypeList)

        all_values=0
                    
        CancerStageType_for_within_Copy=copy.deepcopy(Header_List)
                
        for n in GeneListDict.keys():
            if all_values < TotalCombs[0]:
                if n in CancerStageType_for_within_Copy:
                    SetA=set(GeneListDict[n])
                    del GLD_New[n]
                    NewCanSDType_val=CancerStageType_for_within_Copy.index(n)
                    del CancerStageType_for_within_Copy[NewCanSDType_val]                        
                    for o in GLD_New:
                        SetB=set(GLD_New[o])
                        intersection_of_entries = SetA.intersection(SetB)
                        IOEntries=(list(intersection_of_entries))
                        overlap = len(IOEntries)
                        List1 = len(SetA)
                        List2 = len(SetB)
                        perc = (overlap/((List1+List2)-overlap))*100
                        Percentage_Values.append(perc)
                        IOEntries_List=[]
                        IOEntries_List.append(n)
                        IOEntries_List.append(o)
                        IOEntries_List.append(perc)
                        IOEntries_List.append(len(IOEntries))
                        IOEntries_List.append(IOEntries)
                        Percentage_Overlapping = pd.concat([Percentage_Overlapping, pd.DataFrame([IOEntries_List])], ignore_index=True)
                           
                        all_values=len(Percentage_Values)
            
                #Save Analysis File
            output_file_path = Output_Path / "POpCan_Within.csv"
            Percentage_Overlapping.to_csv(output_file_path, index=False)
            
        print(f"Percentage Overlap has been calculated between and within disease type and their subcategories.\n")
        elapsed_time = time.time() - start_time
        print(f"POpCan completed in {elapsed_time:.2f} seconds")               
        return Percentage_Values

    if Condition=='Between':
        type_stage_dys()
        mk_multiCanDict()
        combination_number_between()
        overlapping_percentage_between()

    elif Condition=='Within':
        type_stage_dys()
        mk_multiCanDict()
        combination_number_within()
        overlapping_percentage_within()

    return