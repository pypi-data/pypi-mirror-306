from moapy.designers_guide.content_function.func_general import execute_calc_content, DG_Result_Reports

def execute_calc(G2_NODE_4: float, G2_NODE_6: str, G2_NODE_9: float) -> DG_Result_Reports:
    target_symbols = ['\\theta_{i}', 'e_{i}', 'H_{i}']
    inputs = {"G2_NODE_4": G2_NODE_4, "G2_NODE_6": G2_NODE_6, "G2_NODE_9": G2_NODE_9}
    return execute_calc_content(target_symbols, inputs)
