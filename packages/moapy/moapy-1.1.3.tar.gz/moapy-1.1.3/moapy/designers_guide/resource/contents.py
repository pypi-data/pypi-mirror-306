contents = [
    {
        "id": "1",
        "standard": "EN1991-1-1",
        "standard_name": "Eurocode 1: Actions on structures — Part 1-1: General actions — Densities, self-weight, imposed loads for buildings",
        "title": "Nominal Density Guide for Construction Materials in Bridge Structures",
        "description": "This guide provides a comprehensive overview of the nominal density values for various construction materials commonly used in bridge structures. It is designed to assist engineers and designers in selecting appropriate materials based on their density characteristics, ensuring the structural integrity and longevity of bridge projects.",
        "target_symbols": [r'densityconcrete', r'paveroad', r'paverail', r'infill', r'strutwithballasted', r'strutwithoutballasted'],
        "test_input": [
            {'symbol': 'densitytype', 'value': 'Weight density (kN/m^3)'}, # densitytype = Weight density
            # {'symbol': 'densitytype', 'value': 'Mass density (kg/m^3)'}, # densitytype = Mass density
        ],
    },
    {
        "id": "2",
        "standard": "EN1991-1-4",
        "standard_name": "Eurocode 1: Actions on structures — Part 1-4: General actions — Wind actions",
        "title": "Guide to Calculating Peak Velocity Pressure at Height",
        "description": "This guide provides a detailed approach for calculating the peak velocity pressure at a specific height by accounting for both mean wind velocity and short-term fluctuations caused by turbulence. The calculation includes determining key parameters such as air density, mean wind velocity, and the exposure factor. The peak velocity pressure is influenced by the turbulence intensity and the exposure factor, which take into account the effects of terrain and height on wind speed. This guide explains how to determine these parameters using the appropriate methods and values, ensuring that engineers can accurately assess wind loads on structures at various elevations.",
        "target_symbols": [r'q_{p(z)}'],
        "test_input": [
            {'symbol': 'v_{b,0}', 'value': '36.5'},
            {'symbol': 'z_{e}', 'value': '3.24'},
            {'symbol': 'terrain', 'value': 'I'}, # terrain = I
            # {'symbol': 'terrain', 'value': 'II'}, # terrain = II
            # {'symbol': 'terrain', 'value': 'III'}, # terrain = III
            # {'symbol': 'terrain', 'value': 'IV'}, # terrain = IV
        ],
    },
    {
        "id": "3",
        "standard": "EN1991-1-5",
        "standard_name": "Eurocode 1: Actions on structures — Part 1-5: General actions — Thermal actions",
        "title": "Non-linear temperature differences for bridge decks",
        "description": "This guide explains how to calculate the non-linear temperature differences for bridge decks in accordance with EN1991-1-5, following Approach 2. It covers calculations for steel decks (type 1), composite decks (type 2), and concrete decks (type 3), taking into account factors such as section height and surfacing thickness. This guide provides temperature gradients and values by height, which are necessary for structural analysis considering temperature differences.",
        "target_symbols": [r'\Delta T_{N,exp}', r'\Delta T_{N,con}'],
        "test_input": [
            {'symbol': 'l', 'value': '27.5'},
            {'symbol': 'N', 'value': '815'},
            {'symbol': 'T_{min}', 'value': -15.555},
            {'symbol': 'T_{max}', 'value': 29.999},
            {'symbol': 'p_{years}', 'value': 30},
            {'symbol': 'Deck_types', 'value': 'steel box girder'}, # Deck_types = Type1
            # {'symbol': 'Deck_types', 'value': 'composite deck'}, # Deck_types = Type2
            # {'symbol': 'Deck_types', 'value': 'concrete box girder'}, # Deck_types = Type3
        ],
    },
    {
        "id": "4",
        "standard": "EN1992-1-1",
        "standard_name": "Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings",
        "title": "Guide for Calculating Geometrical Imperfection in Bridge Design",
        "description": "TGeometrical imperfections in bridge design account for deviations due to construction tolerances or fabrication errors. These imperfections are critical for components like girders, piers, and arches, affecting their stability and load-bearing capacity. In girders and piers, imperfections can lead to additional moments or instability, especially under axial compression, and must be included in the structural analysis to prevent buckling. For arch bridges, imperfections impact vertical and horizontal buckling behavior, requiring early consideration in design. Geometrical imperfections are primarily considered in ultimate limit state analysis, ensuring the structure can handle real-world loads while maintaining stability.",
        "target_symbols": [r'\theta_{i}', r'e_{i}', r'H_{i}'],
        "test_input": [
            {'symbol': 'l', 'value': '27.5'},
            {'symbol': 'N', 'value': '815'},
            {'symbol': 'buckmode', 'value': 'Pinned Ends'}, # buckmode = Pinned Ends
            # {'symbol': 'buckmode', 'value': 'Free - Fixed Ends'}, # buckmode = Free - Fixed Ends
            # {'symbol': 'buckmode', 'value': 'Pinned - Fixed Ends'}, # buckmode = Pinned - Fixed Ends
            # {'symbol': 'buckmode', 'value': 'Fixed Ends'}, # buckmode = Fixed Ends
            # {'symbol': 'buckmode', 'value': 'Guided - Fixed Ends'}, # buckmode = Guided - Fixed Ends
        ],
    },
]