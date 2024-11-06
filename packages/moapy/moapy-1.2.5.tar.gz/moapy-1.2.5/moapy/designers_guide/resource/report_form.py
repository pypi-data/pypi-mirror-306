from dataclasses import dataclass

@dataclass
class ReportForm:
    standard: str = 'Standard',
    reference: str = '',
    title: str = 'Title',
    description: str = 'Description',
    symbol: str = 'Symbol',
    formula: list = [],
    result: float = 0.0,
    result_table: list = [],
    unit: str = 'Unit'

    def to_dict(self):
        return {
            'standard': self.standard,
            'reference': self.reference,
            'title': self.title,
            'description': self.description,
            'symbol': self.symbol,
            'formula': self.formula if isinstance(self.formula, list) else [self.formula],
            'result': str(self.result),
            'result_table': self.result_table if isinstance(self.result_table, list) else [self.result_table],
            'unit': self.unit
        }
    
    def __repr__(self) -> str:
        full_formula = ""
        full_formula += f"{self.symbol}"
        for curr_formula in self.formula if self.formula else []:
            full_formula += " = " + f"{curr_formula}"
        full_formula += " = " + f"{self.result}" + f" {self.unit}"
                
        return (
            f"[{self.standard} {self.reference}] "
            f"{self.title}\n"
            f"{self.description}\n"
            f"{full_formula}"
        )