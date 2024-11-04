import moapy.designers_guide.content_calculator as calc_logic
import moapy.designers_guide.resource.content_node as content_node
from moapy.auto_convert import MBaseModel
from pydantic import Field as dataclass_field

class DG_Result_Reports(MBaseModel):
    res_report: dict = dataclass_field(default_factory=dict)

def execute_calc_content(target_symbols: list, req_input: dict) -> DG_Result_Reports:
    symbol_mappings = calc_logic.create_symbol_mappings(content_node.node_list)

    content_trees = calc_logic.get_function_tree_by_symbols(target_symbols, content_node.node_list, content_node.data_table, symbol_mappings)

    symbol_to_value = []
    for id, val in req_input.items():
        sym = calc_logic.find_by_id(content_node.node_list, id).get("latex_symbol", "")
        symbol_to_value.append({"symbol": sym, "value": val})

    report_bundles = []
    for content_tree in content_trees:
        report_bundles.append(calc_logic.get_report(content_tree, content_node.node_list, content_node.data_table, symbol_mappings, symbol_to_value))

    report_json = calc_logic.make_report_json(report_bundles)

    return DG_Result_Reports(res_report=report_json)