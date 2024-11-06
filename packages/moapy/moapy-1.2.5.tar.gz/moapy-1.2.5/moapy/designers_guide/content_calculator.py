# from version import moapy_version
import moapy.designers_guide.resource.content_node as content_node
import moapy.designers_guide.resource.report_form as report_form
import moapy.designers_guide.resource.contents as contents

import re
import sympy
import json
from sympy import Symbol
from sympy.parsing.latex import parse_latex

# Func Desc. Insert spaces around operators in LaTeX
def insert_spaces(latex_expr):
    # List of operators
    binary_operators = [r'\\pm', r'\\cdot', r'\\times', r'\\div', r'\\mod', r'\\land', r'\\lor', r'\\cup', r'\\cap', r'\\oplus']
    relation_operators = [r'=', r'\\neq', r'\\leq', r'\\geq', r'<', r'>', r'\\approx', r'\\sim', r'\\equiv', r'\\subset', r'\\supset']
    function_operators = [r'\\sin', r'\\cos', r'\\log', r'\\ln' r'\\lim', r'\\int', r'\\sum', r'\\left', r'\\right']
    operators = binary_operators + relation_operators + function_operators

    for op in operators:
        latex_expr = re.sub(f'({op})([^ ])', r'\1 \2', latex_expr)
        latex_expr = re.sub(f'([^ ])({op})', r'\1 \2', latex_expr)
    return re.sub(r'\s+', ' ', latex_expr).strip()

def is_latex_equation(expr):
    # List of operators
    binary_operators = [r'\\pm', r'\\cdot', r'\\times', r'\\div', r'\\mod', r'\\land', r'\\lor', r'\\cup', r'\\cap', r'\\oplus']
    relation_operators = [r'=', r'\\neq', r'\\leq', r'\\geq', r'<', r'>', r'\\approx', r'\\sim', r'\\equiv', r'\\subset', r'\\supset']
    function_operators = [r'\\sin', r'\\cos', r'\\log', r'\\ln' r'\\lim', r'\\int', r'\\sum', r'\\left', r'\\right']
    operators = binary_operators + relation_operators + function_operators

    for op in operators:
        if re.search(op, expr):
            return True
    return False

# Func Desc. Replace LaTeX symbols with simple symbols and map them
def create_symbol_mappings(node_list):
    symbol_mappings = {item['latex_symbol']: f'S_{{{i + 1}}}' for i, item in enumerate(node_list)}
    symbol_mappings = dict(sorted(symbol_mappings.items(), key=lambda item: len(item[0]), reverse=True))
    content_node.node_list = replace_symbols_in_equations(content_node.node_list, symbol_mappings)
    return symbol_mappings

def replace_latex_to_simple(latex_str, symbol_mappings, required_symbols = None):
    lhs = latex_str.split('=')[0].strip()
    simple_str = latex_str
    for latex_symbol, simple_symbol in symbol_mappings.items():
        if latex_symbol != lhs and required_symbols is not None and latex_symbol not in required_symbols:
            continue
        simple_str = re.sub(rf'(?<!\w){re.escape(latex_symbol)}(?!\w)', simple_symbol, simple_str)
    return simple_str

# Func Desc. Replace LaTeX symbols with simple symbols in node list
def replace_symbols_in_equations(node_list, symbol_mappings):
    # TODO : symbol 이 중복되는 상황이 발생할 수 있음. 추가 식별자 도입 필요
    for node in (m for m in node_list if "latex_equation" in m):
        required_symbols = node['required'] if 'required' in node else None
        preprocessed_eq = node['latex_equation']
        preprocessed_eq = replace_latex_to_simple(preprocessed_eq, symbol_mappings, required_symbols)
        node['preprocessed_equation'] = preprocessed_eq
        node['sympy_expr'] = parse_latex(preprocessed_eq)
    return node_list

class TreeNode:
    def __init__(self, symbol, operation=None, children=None):
        self.symbol = symbol  # 노드의 심볼 (변수 또는 함수명)
        self.operation = operation  # 노드의 연산자 또는 함수 정의
        self.children = children if children is not None else []  # 자식 노드 리스트

    def add_child(self, child_node):
        self.children.append(child_node)

def search_content_by_lhs_latex(node_list, lhs_latex_symbol):
    for node in node_list:
        if lhs_latex_symbol == str(node['latex_symbol']):
            return node
    return None

def search_equation_by_lhs_latex(node_list, lhs_latex_symbol):
    for node in node_list:
        if lhs_latex_symbol == str(node['latex_symbol']):
            return node
    return None

def get_latex_symbol_by_simple_symbol(simple_symbol, symbol_mappings):
    for latex_symbol, simple in symbol_mappings.items():
        if simple == simple_symbol:
            return latex_symbol
    return None

def get_table_data_by_symbol(node, data_table):
    if 'table' in node:
        return next(dt['data'] for dt in data_table if dt['id'] == node['id'])
    return None

def find_by_id(node_list, node_id):
    # id를 기준으로 데이터를 찾음
    for item in node_list:
        if item['id'] == node_id:
            return item
    return None

def find_by_latex_symbol(node_list, target_latex_symbol):
    # latex_symbol을 기준으로 데이터를 찾음
    for item in node_list:
        if item['latex_symbol'] == target_latex_symbol:
            return item
    return None

def replace_log_to_ln(equation):
    stack = []
    replaced_equation = []

    i = 0
    while i < len(equation):
        if equation[i:i+4] == "log(":
            stack.append(len(replaced_equation))
            replaced_equation.append("ln(")
            i += 4
        elif len(stack) > 0 and equation[i:i+4] == ", E)":
            replaced_equation.append(")")
            stack.pop()
            i += 4
        else:
            replaced_equation.append(equation[i])
            i += 1

    return ''.join(replaced_equation)

def get_child_symbols_by_expr(node):
    if 'sympy_expr' in node:
        return node['sympy_expr'].rhs.free_symbols
    return []

def get_child_symbols_by_required(node):
    if 'required' in node:
        return node['required']
    return []

def get_child_symbols_by_data_table(node, data_table, symbol_mappings):
    children = []
    if 'table' in node:
        table_data = get_table_data_by_symbol(node, data_table)
        for td in table_data:
            simple_condition = replace_latex_to_simple(td['condition'], symbol_mappings)
            for latex_symbol, simple in symbol_mappings.items():
                if simple in simple_condition:
                    children.append(simple)
    children = set(children)
    return children

def get_calc_tree(target_symbol, node_list, data_table, symbol_mappings):
    current_node = search_equation_by_lhs_latex(node_list, target_symbol)
    if current_node is None:
        return None
    
    node = TreeNode(target_symbol, current_node)
    
    child_symbols = set(get_child_symbols_by_required(current_node))
    expr_symbols = get_child_symbols_by_expr(current_node)
    for sym in expr_symbols:
        latex_symbol = get_latex_symbol_by_simple_symbol(str(sym), symbol_mappings)
        if latex_symbol is None:
            print('No symbol found for ' + str(child))
            continue
        child_symbols.add(latex_symbol)

    for child in child_symbols:
        child_node = get_calc_tree(child, node_list, data_table, symbol_mappings)
        if child_node is not None:
            node.add_child(child_node)
        else:
            node.add_child(TreeNode(latex_symbol))
        
    return node  

def get_leaf_nodes(node):
    leaf_nodes = []
    if node.children: # 자식이 있는 경우, 재귀적으로 자식들을 탐색
        for child in node.children:
            leaf_nodes.extend(get_leaf_nodes(child))
    else: # 만약 자식이 없는 노드면 (리프 노드)
        leaf_nodes.append(node)
    
    return leaf_nodes

def generate_json_schema(node):
    schema = {
        "title": node.get("title", ""),
        "type": node.get("type", "string"),
        "description": node.get("description", ""),
        "symbol": node.get("latex_symbol", ""),
        "unit": node.get("unit", ""),
    }

    if "default" in node:
        schema["default"] = node["default"]

    if "enum" in node:
        schema["enum"] = node["enum"]
    
    if is_const(node):
        schema["readOnly"] = True

    # if "formula" in node:
    #     schema["formula"] = node["formula"]

    # return {
    #     node['id']: {
    #         "standard": node['standard'],
    #         "reference": node['reference'],
    #         "latex_symbol": node['latex_symbol'],
    #         "unit": node['unit'],
    #         "schema": schema
    #     }
    # }
    
    # return {node['id'] : schema}
    return {node["id"] : schema}

def is_const(node):
    return node.get("const", False) == True

def extract_node_id(key):
    match = re.search(r'NODE_(\d+)', key)
    return int(match.group(1)) if match else float('inf')

def get_function_tree_by_symbols(target_symbols, node_list, data_table, symbol_mappings):
    params_tree = []
    for target_symbol in target_symbols:
        content_tree = get_calc_tree(target_symbol, node_list, data_table, symbol_mappings)
        if content_tree is not None:
            params_tree.append(content_tree)
    return params_tree

def get_function_tree(target_content, node_list, data_table, symbol_mappings):
    target_symbols = target_content.get("target_symbols", [])
    return get_function_tree_by_symbols(target_symbols, node_list, data_table, symbol_mappings)

def get_function_tree_schema(target_content, node_list, data_table, symbol_mappings):
    params_tree = []
    req_properties = {}
    required = set()
    res_properties = {}

    params_tree = get_function_tree(target_content, node_list, data_table, symbol_mappings)
    for content_tree in params_tree:
        params = []
        leafs = get_leaf_nodes(content_tree)
        for leaf in leafs:
            param = find_by_latex_symbol(node_list, leaf.symbol)
            params.append(param)

        for param in params:
            req_properties.update(generate_json_schema(param))
            if is_const(param) == False:
                required.add(param['id'])

        node = find_by_id(node_list, content_tree.operation['id'])
        res_properties.update(generate_json_schema(node))
    
    req_properties = dict(sorted(req_properties.items(), key=lambda item: extract_node_id(item[0])))
    req_required = sorted(list(required), key=lambda item: extract_node_id(item))

    # target_symbols = target_content.get("target_symbols", [])
    # req_properties.update({"target_symbols" : {
    #     "type": "array",
    #     "default": target_symbols
    # }})
    # req_required.append("target_symbols")
    
    # TODO : Response OpenAPI 규칙에 맞게 재정의 필요
    res_properties = dict(sorted(res_properties.items(), key=lambda item: extract_node_id(item[0])))

    post = {
        "summary" : target_content.get('title', "None Title"),
        "description" : target_content.get('description', "None Description"),
        "requestBody" : {
            "content": {
                "application/json": {
                    "schema" : {
                        "type": "object",
                        "properties": req_properties,
                        "required" : req_required
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": res_properties
                        }
                    }
                }
            }
        }
    }

    path = f"/execute?functionId=moapy-designers_guide-content_function-{get_auto_func_file_name(target_content)}-{get_auto_func_name()}"
    schema = {
        # "$ref": f"#/paths/{path.replace("/", "~1")}/post/requestBody/content/application~1json/schema", # NOTE : rjsf 테스트 시 주석 해제
        "openapi": "3.1.0",
        "info": {
            "title": "moapy",
            "description": "Schema for moapy",
            "version": "0.9.8" # moapy_version # TODO : import version 오류 해결 후 버전 정보 추가
        },
        "servers": [
            {
            "url": "https://moa.rpm.kr-dv-midasit.com/backend/python-executor/"
            },
            {
            "url": "https://moa.rpm.kr-st-midasit.com/backend/function-executor/python-execute/"
            }
        ],
        "paths": {
            path: {
                "post": post
            }
        }
    }

    return [params_tree, schema, req_required]

def get_auto_func_file_name(target_content):
    return f"calc_content_{target_content['id']}"

def get_auto_func_name():
    return f"execute_calc"

def get_auto_function(target_content, required, node_list):
    func_name = get_auto_func_name()
    target_symbols = target_content.get("target_symbols", [])

    func_params = ""
    func_input = "inputs = {"
    for req in required:
        func_input += f'"{req}": {req}'
        curr_node = find_by_id(node_list, req)
        if curr_node is None:
            continue
        datatype = curr_node.get("type", "number")
        func_params += f"{req}: "
        if datatype == "number":
            func_params += "float"
        elif datatype == "string":
            func_params += "str"
        elif datatype == "array":
            func_params += "list"
        if(req != required[-1]):
            func_params += ", "
            func_input += ", "
    func_input += "}"

    func_code = f"""from moapy.designers_guide.content_function.func_general import execute_calc_content, DG_Result_Reports

def {func_name}({func_params}) -> DG_Result_Reports:
    target_symbols = {target_symbols}
    {func_input}
    return execute_calc_content(target_symbols, inputs)
"""
    return func_code

def is_calcuated_symbol(stack_reports, symbol):
    return any(report.symbol == symbol for report in stack_reports)

def get_unique_report(stack_reports, sub_reports): # Extract a non-overlapping report with an accumulated list
    symbols_stack = {report.symbol for report in stack_reports}
    symbols_sub = {report.symbol for report in sub_reports}
    duplicates = symbols_stack & symbols_sub
    unique_sub_reports = [report for report in sub_reports if report.symbol not in duplicates]
    return unique_sub_reports

def sympy_post_processing(expr): # 단순 계산이 안되는 연산식 처리
    expr_rhs_str = str(expr.rhs)
    res_value = sympy.parse_expr(expr_rhs_str)
    expr = sympy.Eq(expr.lhs, res_value)
    # rhs_value = 0
    # min_match = re.search(r'min\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # max_match = re.search(r'max\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # if min_match:
    #     rhs_value = sympy.Min(*map(float, min_match.groups()))
    # elif max_match:
    #     rhs_value = sympy.Max(*map(float, max_match.groups()))
    # else:
    #     return None
    # expr_rhs_str = expr_rhs_str.replace(min_match.group(), str(rhs_value))
    # expr_rhs_simbol = sympy.parse_expr(expr_rhs_str)
    # expr = sympy.Eq(expr.lhs, expr_rhs_simbol)
    # recursion_expr = sympy_post_processing(expr)
    # if recursion_expr is not None:
    #     expr = recursion_expr
    return expr

def get_report(node, node_list, table_list, symbol_mappings, symbol_to_value):
    params_report = []
    symbol_result = []
    for chlid in node.children:
        if is_calcuated_symbol(params_report, chlid.symbol):
            continue
        sub_reports = get_report(chlid, node_list, table_list, symbol_mappings, symbol_to_value)
        if sub_reports is None:
            continue
        for sub_report in sub_reports:
            symbol_result.append(tuple([symbol_mappings[f"{sub_report.symbol}"], sub_report.symbol, sub_report.result]))
        unique_sub_reports = get_unique_report(params_report, sub_reports)
        params_report.extend(unique_sub_reports)

    for sym_val in symbol_to_value:
        exist = next((item for item in symbol_result if item[1] == sym_val['symbol']), None)
        if exist:
            continue
        symbol_result.append(tuple([symbol_mappings[f"{sym_val['symbol']}"], sym_val['symbol'], sym_val['value']]))
    symbol_result = set(symbol_result)

    current_content = find_by_latex_symbol(node_list, node.symbol)
        
    current_report = report_form.ReportForm()
    current_report.standard = current_content['standard']
    current_report.title = current_content['title']
    current_report.unit = current_content['unit']
    current_report.reference = current_content['reference']
    current_report.description = current_content['description']
    current_report.symbol = current_content['latex_symbol']
    current_report.formula = []
    current_report.result_table = []
    if 'default' in current_content:
        current_report.result = current_content['default']

    required_symbols = current_content['required'] if 'required' in current_content else None

    table_data = get_table_data_by_symbol(current_content, table_list)
    input_value = next((item for item in symbol_to_value if item['symbol'] == node.symbol), None)
    if table_data and current_content['table'] == 'dropdown': # 'table' : 'dropdown'
        for td in table_data if table_data else []:
            if td['condition'] == input_value['value']:
                current_report.result = td['value']
    elif table_data and current_content['table'] == 'result': # 'table' : 'result'
        data_check = table_data
        for i, td in enumerate(table_data) if table_data else []:
            if i == 0:
                header_list = []
                for key, value in td.items():
                    header_list.append(key)
                current_report.result_table.append(tuple(header_list))
            row_list = []
            for key, value in td.items():
                res_value = ""
                if is_latex_equation(str(value)):
                    calc_expr = insert_spaces(value)
                    expr_parts = re.split(r'\\text\{([^}]*)\}', str(calc_expr))
                    for i, part in enumerate(expr_parts):
                        if i % 2 == 0:
                            part_expr = parse_latex(replace_latex_to_simple(part, symbol_mappings, required_symbols))
                            for sym, disp_sym, res in symbol_result:
                                x = sympy.symbols(f"{sym}")
                                if part_expr.has(x):
                                    part_expr = part_expr.subs(x, res)
                            res_value += f"{str(part_expr.evalf())} "
                        else:
                            res_value += f"{part} "
                else:
                    res_value = str(value)
                row_list.append(res_value)
            current_report.result_table.append(row_list)
    elif input_value:
            current_report.result = input_value['value']
    elif 'sympy_expr' in node.operation: # fomula
        if table_data and current_content['table'] == 'formula': # 'table' : 'formula'
            for td in table_data if table_data else []:
                cd_expr = re.sub(r'(?<![<>!])=(?![=<>])', '==', td['condition'])
                cd_expr = replace_latex_to_simple(cd_expr, symbol_mappings, required_symbols)
                for sym, disp_sym, res in symbol_result:
                    cd_expr = cd_expr.replace(sym, str(res))
                if sympy.sympify(cd_expr) == True:
                    node.operation['sympy_expr'] = parse_latex(replace_latex_to_simple(td['value'], symbol_mappings, required_symbols))

        expr = node.operation['sympy_expr']
        org_formula = replace_log_to_ln(f"{expr.rhs}")
        mid_formula = org_formula

        for sym, disp_sym, res in symbol_result:
            x = sympy.symbols(f"{sym}")
            if expr.has(x):
                expr = expr.subs(x, res)
            org_formula = org_formula.replace(sym, disp_sym)
            mid_formula = mid_formula.replace(sym, str(res))
        
        current_report.formula.append(org_formula)
        current_report.formula.append(mid_formula)
        current_report.result = expr.evalf().rhs

        if 'min' in str(expr) or 'max' in str(expr):
            post_formula = f"{expr.rhs}"
            current_report.formula.append(post_formula)
            expr = sympy_post_processing(expr)
            current_report.result = expr.evalf().rhs

    params_report.append(current_report)
    
    return params_report

def make_report_json(report_bundles):
    report_bundle_json = []
    for report_bundle in report_bundles:
        report_json = []
        for report in report_bundle:
            report_json.append(report.to_dict())
        report_bundle_json.append(report_json)
    return {"result": report_bundle_json}

def get_markdown_text(report_bundles):
    markdown_text = ""

    markdown_text += "### Result\n"
    markdown_text += "View and analyze the calculated results based on your inputs and selected options.\n\n"
    markdown_text += "---\n\n"
    for i, report_bundle in enumerate(report_bundles):
        main_report = report_bundle[-1]
        markdown_text += "___" + f"{main_report.title}" + ",___\n"
        if main_report.result_table:
            for idx, row in enumerate(main_report.result_table):
                markdown_text += "|"
                for col in row:
                    markdown_text += f"{col}" + "|"
                markdown_text += "\n"
                if idx == 0:
                    for col in row:
                        markdown_text += "---" + "|"
                    markdown_text += "\n"
            markdown_text += "\n"
        else:
            markdown_text += "$$" + f"{main_report.symbol}\quad" + f"{main_report.result}"
            if main_report.unit != "":
                markdown_text += f"\,({main_report.unit})"
            markdown_text += "$$\n\n"
    markdown_text += "---\n\n"

    markdown_text += "### Details\n"
    markdown_text += "Explore the detailed steps and methodologies used in the calculation process.\n\n"
    markdown_text += "---\n\n"

    for report_bundle in report_bundles:
        for idx, report in enumerate(report_bundle):
            markdown_text += "__" + f"{idx + 1}. " + f"[{report.standard} {report.reference}]" + "__ " + f"{report.title}\n\n"
            markdown_text += f"{report.description}\n\n"

            if report.result_table:
                for idx, row in enumerate(report.result_table):
                    markdown_text += "|"
                    for col in row:
                        markdown_text += f"{col}" + "|"
                    markdown_text += "\n"
                    if idx == 0:
                        for col in row:
                            markdown_text += "---" + "|"
                        markdown_text += "\n"
                markdown_text += "\n"
            else:
                full_formula = ""
                full_formula += f"{report.symbol}"
                for curr_formula in report.formula if report.formula else []:
                    full_formula += " = " + f"{curr_formula}"
                full_formula += " = " + f"{report.result} "
                if report.unit != "":
                    full_formula += f"\,({report.unit})"
                
                markdown_text += "$$" + full_formula + "$$\n\n"

        if(report_bundle != report_bundles[-1]):
            markdown_text += "---\n\n"
    markdown_text += "---\n\n"

    return markdown_text

# 이 함수는 입력, 출력, 함수 테스트용
def main():
    # Step 1: 사전 작업
    # Step 1-1: Insert spaces in LaTeX equations
    for node in (m for m in content_node.node_list if "latex_equation" in m):
        node['latex_equation'] = insert_spaces(node['latex_equation'])

    # Step 1-2: Create symbol mappings and replace symbols in equations
    symbol_mappings = create_symbol_mappings(content_node.node_list)

    # Step 2 : Input the Target Content
    # NOTE : 자동 생성할 Content 선택. 
    # target_content = contents.contents[0] # [EN1991-1-1] Nominal Density Guide for Construction Materials in Bridge Structures
    # target_content = contents.contents[1] # [EN1991-1-4] Guide to Calculating Peak Velocity Pressure at Height
    target_content = contents.contents[2] # [EN1991-1-5] Non-linear temperature differences for bridge decks
    # target_content = contents.contents[3] # [EN1992-1-1] Guide for Calculating Geometrical Imperfection in Bridge Design

    # Step 3 : Create a content tree & OpenAPI Schema
    [content_trees, schema, required] = get_function_tree_schema(target_content, content_node.node_list, content_node.data_table, symbol_mappings)
    
    json_schema_text = json.dumps(schema, indent=2)
    schema_file_path = f"schemas/managed/moapy/designers_guide/calc_content_{target_content['id']}.json" 
    with open(schema_file_path, "w", encoding="utf-8") as schema_file:
        schema_file.write(json_schema_text)
    
    auto_function = get_auto_function(target_content, required, content_node.node_list)
    func_file_path = f"moapy/designers_guide/content_function/{get_auto_func_file_name(target_content)}.py"
    with open(func_file_path, "w", encoding="utf-8") as func_file:
        func_file.write(auto_function)

    # Step 4 : Get the input value from UI
    # NOTE : symbol_to_value은 Front의 UI에서 전달 받아야 함.
    symbol_to_value = target_content['test_input']

    # Step 5 : Print a result Report (markdown)
    report_bundles = []
    for content_tree in content_trees:
        report_bundles.append(get_report(content_tree, content_node.node_list, content_node.data_table, symbol_mappings, symbol_to_value))

    report_json = make_report_json(report_bundles)
    report_json_text = json.dumps(report_json, indent=4)
    with open("moapy/designers_guide/res_file/report.json", "w", encoding="utf-8") as report_json_file:
        report_json_file.write(report_json_text)

    markdown_text = get_markdown_text(report_bundles)
    with open("moapy/designers_guide/res_file/report.md", "w", encoding="utf-8") as markdown_file:
        markdown_file.write(markdown_text)

# main()