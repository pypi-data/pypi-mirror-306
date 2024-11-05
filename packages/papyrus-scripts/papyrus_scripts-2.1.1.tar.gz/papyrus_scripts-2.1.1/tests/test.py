from papyrus_scripts import PapyrusDataset, preprocess, reader

# data2 = (PapyrusDataset(is3d=False, version='latest', plusplus=False, chunksize=int(1e6))
#                                 .keep_organism('Mus musculus (Mouse)')
#                                 .keep_source('chembl')
#                                 .keep_protein_class({'l5': 'CC chemokine receptor'})
#                                 .not_isin('accession', ['P13500', 'P13501'])
#                                 .keep_activity_type(['ki', 'kd'])
#                                 .aggregate(progress=True))
#
# #print(data2.organism.value_counts())
# print(data2.source.value_counts())
# print(data2.Classification.value_counts())
# print(data2.accession.value_counts())
# print(data2[['type_IC50', 'type_EC50', 'type_KD', 'type_Ki', 'type_other']].value_counts())


fn_data = reader.read_papyrus(is3d=False, version='latest', plusplus=True, chunksize=int(1e6))
fn_protein_data = reader.read_protein_set(version='latest')
fn_filter1 = preprocess.keep_organism(fn_data, fn_protein_data, organism='Homo sapiens (Human)')
fn_filter2 = preprocess.keep_protein_class(fn_filter1, fn_protein_data, classes={'l5': 'Adenosine receptor'})
fn_filter3 = preprocess.keep_type(fn_filter2, activity_types='ic50')
fn_data_agg = preprocess.consume_chunks(fn_filter3, progress=True)
oop_data_agg = (PapyrusDataset(is3d=False, version='latest', plusplus=True, chunksize=int(1e6))
                .keep_organism('Homo sapiens (Human)')
                .keep_protein_class({'l5': 'Adenosine receptor'})
                .keep_activity_type('ic50')
                .aggregate(progress=True))

print(fn_data_agg)
print(oop_data_agg)
