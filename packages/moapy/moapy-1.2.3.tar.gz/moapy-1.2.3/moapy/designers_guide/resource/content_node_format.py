node_format = [
    {
        'id': 'G{N}_NODE_{i}', # N: 예제 번호, i: 모듈 번호
        'standard': '{standard_number}', # standard_number: 설계기준 ex) EN1991-1-5
        'title': '{title}', # title: content node 이름
        'reference': '{reference}', # reference: 기호 및 수식이 포함되는 section
        'latex_symbol': r'{symbol}', # symbol: content node의 대표 기호 (필수 입력. 공백 허용 X)
        'latex_equation': r'{equation}', # equation: node의 결과 값을 도출 할 수 있는 수식 (필요 시에만 입력. LaTex 형식)
        'unit': '{unit}', # unit: content node 결과 값의 단위 (불필요 시 '' 입력)
        'description': r'{description}', # description: node에 대한 설명. 결과 Report에 표시되는 내용
        'type': '{result_type}', # result_type: 결과 값의 최종 형태 (number, string, table, graph, ...)
        # 'type': 'table' - Report의 결과 값이 table 형태로 출력
        # 'type': 'graph' - Report의 결과 값은 table이지만, UI에서 그래프로 출력
        'default': '{default_value}', # default_value: node의 기본 값 (필요 시에만 입력. const True)
        'required': ['{required_1}', '{required_2}', ...], # required_list: equation 및 table에 필요한 node의 symbol
        # TODO : 다른 standard의 symbol을 참조할 때 규칙 필요
        'enum': ['{enum_1}', '{enum_2}', ...], # enum_list: dropdown 형식으로 입력 받을 수 있는 값
        'table': '{table_data_type}', # table_data_type: table에 입력되는 데이터 형식 (dropdown, formula, result)
        # 'table': 'dropdown' - 사용자에게 combo box 형태로 입력 받음
        # 'table': 'formula' - 특정 조건에 따라 다른 formula를 적용
        # 'table': 'result' - Report에 표시할 결과 값에 대한 정보를 담은 table
        'const': '{const_boolean}', # const_boolean: node의 값이 상수인지 아닌지 여부 (True, False)
    },
]

data_table_format = [
    # 'table': 'dropdown'
    {
        "id": "{node_id}", # node_id: table을 사용할 node의 id
            "data": [
                {
                    'condition': r'{fomula_condition}', # fomula_condition: 적용 조건
                    'value': r'{result}', # result: 조건 만족 시 적용할 값 (node의 symbol result. 공백 허용 X)
                },
            ],
    },
    # 'table': 'fomula'
    {
        "id": "{node_id}", # node_id: table을 사용할 node의 id
            "data": [
                {
                    'condition': r'{fomula_condition}', # fomula_condition: 적용 조건
                    'value': r'{formula}', # formula: 조건 만족 시 적용되는 수식 (node의 latex_equation 대체)
                },
            ],
    },
    # 'table': 'result'
    {
        "id": "{node_id}", # node_id: table을 사용할 node의 id
            "data": [
                { # row 1
                    '{colum_1}': r'{colum_value_1}', # colum_value_1: 표시할 값
                    '{colum_2}': r'{colum_value_1}', # colum_value_2: 표시할 값 (수식이 들어갈 수 있음)
                },
                { # row 2
                    '{colum_1}': r'{colum_value_1}', # colum_value_1: 표시할 값
                    '{colum_2}': r'{colum_value_1}', # colum_value_2: 표시할 값 (수식이 들어갈 수 있음)
                },
            ],
    },
]