from moapy.designers_guide.content_function.func_general import execute_calc_content, DG_Result_Reports

def execute_calc(G3_NODE_2: float, G1_NODE_3: float, G3_NODE_10: float, G3_NODE_16: float, G3_NODE_17: float) -> DG_Result_Reports:
    target_symbols = ['q_{p(z)}']
    inputs = {"G3_NODE_2": G3_NODE_2, "G1_NODE_3": G1_NODE_3, "G3_NODE_10": G3_NODE_10, "G3_NODE_16": G3_NODE_16, "G3_NODE_17": G3_NODE_17}
    return execute_calc_content(target_symbols, inputs)
