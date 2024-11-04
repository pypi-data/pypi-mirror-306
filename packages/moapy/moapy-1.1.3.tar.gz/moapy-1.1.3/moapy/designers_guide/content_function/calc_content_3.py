from moapy.designers_guide.content_function.func_general import execute_calc_content, DG_Result_Reports

def execute_calc(G1_NODE_1: str, G1_NODE_2: float, G1_NODE_3: float, G1_NODE_5: float, G1_NODE_6: float) -> DG_Result_Reports:
    target_symbols = ['\\Delta T_{N,exp}', '\\Delta T_{N,con}']
    inputs = {"G1_NODE_1": G1_NODE_1, "G1_NODE_2": G1_NODE_2, "G1_NODE_3": G1_NODE_3, "G1_NODE_5": G1_NODE_5, "G1_NODE_6": G1_NODE_6}
    return execute_calc_content(target_symbols, inputs)
