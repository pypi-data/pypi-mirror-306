from moapy.designers_guide.content_function.func_general import execute_calc_content, DG_Result_Reports

def execute_calc(G4_NODE_1: str) -> DG_Result_Reports:
    target_symbols = ['densityconcrete', 'paveroad', 'paverail', 'infill', 'strutwithballasted', 'strutwithoutballasted']
    inputs = {"G4_NODE_1": G4_NODE_1}
    return execute_calc_content(target_symbols, inputs)
