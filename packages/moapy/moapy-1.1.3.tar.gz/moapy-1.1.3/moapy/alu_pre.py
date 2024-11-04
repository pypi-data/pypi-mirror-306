from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
from moapy.steel_pre import SteelMomentModificationFactor
from moapy.enum_pre import enum_to_list, enAluminumMaterial_AA

class AluMaterial(MBaseModel):
    """
    Alu DB Material
    """
    code: str = dataclass_field(default='AA(A)', description="The term AA(A) typically refers to a specific designation within the Aluminum Association (AA) standards used in North America to classify aluminum alloys", readOnly=True)
    matl: str = dataclass_field(default='2014-T6', description="Please select an aluminum material", title="Material", enum=enum_to_list(enAluminumMaterial_AA))
    product: str = dataclass_field(default='Extrusions', description="Extrusions in aluminum product types refer to a manufacturing process that involves shaping aluminum into specific profiles by forcing it through a die.", readOnly=True)

    class Config(MBaseModel.Config):
        title = "Aluminum DB Material"
        description = "It provides structured information about the aluminum material, with the main fields being the code for the aluminum alloy, the aluminum material that the user can select (2014-T6), and the product type (extruded)."

class AluMomentModificationFactor(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    cb: float = dataclass_field(default=1.0, title="Cb", description="Coefficient that accounts for moment gradient along a beam’s length")
    m: float = dataclass_field(default=1.0, description="Constant determined from Table 4.8.1-1")

    class Config(MBaseModel.Config):
        title = "Aluminum Moment Modification Factor"
        description = "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements."