from typing import Optional
from pydantic import Field
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Point, Stress_Strain_Component, Length, enUnitLength, Stress, enUnitStress, MaterialCurve, Area, enUnitArea, SectionRectangle
from moapy.enum_pre import enum_to_list, enUnitArea, enUnitLength, enUnitStress, enUnitThermalExpansion, enUnitAngle, enUnitTemperature, enDgnCode, enBoltName, enUnitMoment, enRebar_UNI
# ==== Concrete Material ====
class ConcreteGrade(MBaseModel):
    """
    GSD concrete class

    Args:
        design_code (str): Design code
        grade (str): Grade of the concrete
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="C12", description="Grade of the concrete")

    class Config(MBaseModel.Config):
        title = "Concrete Grade"

class Concrete_General_Properties(MBaseModel):
    """
    GSD concrete general properties for calculation
    
    Args:
        strength (int): Grade of the concrete
        elastic_modulus (float): Elastic modulus of the concrete
        density (float): Density of the concrete
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the concrete
        poisson_ratio (float): Poisson ratio of the concrete
    """
    strength: int = Field(
        gt=0, default=12, description="Grade of the concrete")
    elastic_modulus: float = Field(
        gt=0, default=30000, description="Elastic modulus of the concrete")
    density: float = Field(
        gt=0, default=2400, description="Density of the concrete")
    thermal_expansion_coefficient: float = Field(
        gt=0, default=0.00001, description="Thermal expansion coefficient of the concrete")
    poisson_ratio: float = Field(
        gt=0, default=0.2, description="Poisson ratio of the concrete")

    class Config(MBaseModel.Config):
        title = "Concrete General Properties"

class Concrete_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        factor_b1 (float): Plastic strain limit for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    factor_b1: float = Field(
        default=0.85, description="Plastic strain limit for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "Concrete Stress Options for ULS"

class Concrete_Stress_ULS_Options_Eurocode(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        partial_factor_case (float): Partial factor case for ULS
        partial_factor (float): Partial factor for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    partial_factor_case: float = Field(
        default=1.0, description="Partial factor case for ULS")
    partial_factor: float = Field(
        default=1.5, description="Partial factor for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "Concrete Stress Options for ULS"

class Concrete_SLS_Options(MBaseModel):
    """
    GSD concrete stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        plastic_strain_limit (float): Plastic strain limit for SLS
        failure_compression_limit (float): Failure compression limit for SLS
        material_model_tension (str): Material model for SLS tension
        failure_tension_limit (float): Failure tension limit for SLS
    """
    material_model: str = Field(
        default="Linear", description="Material model for SLS")
    plastic_strain_limit: float = Field(
        default=0.002, description="Plastic strain limit for SLS")
    failure_compression_limit: float = Field(
        default=0.003, description="Failure compression limit for SLS")
    material_model_tension: str = Field(
        default="interpolated", description="Material model for SLS tension")
    failure_tension_limit: float = Field(
        default=0.003, description="Failure tension limit for SLS")

    class Config(MBaseModel.Config):
        title = "Concrete Stress Options for SLS"

# ==== Rebar & Tendon Materials ====
class RebarGrade(MBaseModel):
    """
    GSD rebar grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the rebar
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="Grade 420", description="Grade of the rebar")

    class Config(MBaseModel.Config):
        title = "Rebar Grade"

class TendonGrade(MBaseModel):
    """
    GSD Tendon grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the tendon
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(default="Grade 420", description="Grade of the tendon")

    class Config(MBaseModel.Config):
        title = "Tendon Grade"

class RebarProp(MBaseModel):
    """
    GSD rebar prop

    Args:
        area (float): Area of the rebar
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the rebar")

    class Config(MBaseModel.Config):
        title = "Rebar Properties"

class TendonProp(MBaseModel):
    """
    GSD Tendon prop

    Args:
        area (float): Area of the tendon
        prestress (float): Prestress of the tendon
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the tendon")
    prestress: Stress = Field(default=Stress(value=0.0, unit=enUnitStress.MPa), description="Prestress of the tendon")

    class Config(MBaseModel.Config):
        title = "Tendon Properties"

class Rebar_General_Properties(MBaseModel):
    """
    GSD rebar general properties for calculation
    
    Args:
        strength (int): Grade of the rebar
        elastic_modulus (float): Elastic modulus of the rebar
        density (float): Density of the rebar
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the rebar
        poisson_ratio (float): Poisson ratio of the rebar
    """
    strength: int = Field(
        default=420, description="Grade of the rebar")
    elastic_modulus: float = Field(
        default=200000, description="Elastic modulus of the rebar")
    density: float = Field(
        default=7850, description="Density of the rebar")
    thermal_expansion_coefficient: float = Field(
        default=0.00001, description="Thermal expansion coefficient of the rebar")
    poisson_ratio: float = Field(
        default=0.3, description="Poisson ratio of the rebar")

    class Config(MBaseModel.Config):
        title = "Rebar General Properties"

class Rebar_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD rebar stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for ULS")
    failure_strain: float = Field(
        default=0.7, description="Failure strain limit for ULS")

    class Config(MBaseModel.Config):
        title = "Rebar Stress Options for ULS"

class Rebar_Stress_SLS_Options(MBaseModel):
    """
    GSD rebar stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        failure_strain (float): Failure strain limit for SLS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for SLS")
    failure_strain: float = Field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})

    class Config(MBaseModel.Config):
        title = "Rebar Stress Options for SLS"

class MaterialRebar(MaterialCurve):
    """
    GSD rebar class
    
    Args:
        grade (RebarGrade): Grade of the rebar
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "Material Rebar"

class MaterialTendon(MaterialCurve):
    """
    GSD tendon class
    
    Args:
        grade (TendonGrade): Grade of the tendon
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "Material Tendon"

class MaterialConcrete(MaterialCurve):
    """
    GSD material for Concrete class
    
    Args:
        grade (ConcreteGrade): Grade of the concrete
        curve_uls (list[Stress_Strain_Component]): Stress strain curve concrete ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

    class Config(MBaseModel.Config):
        title = "Material Concrete"

class Material(MBaseModel):
    """
    GSD concrete class

    Args:
        concrete (MaterialConcrete): Concrete properties
        rebar (MaterialRebar): Rebar properties
        tendon (MaterialTendon): Tendon properties
    """
    concrete: MaterialConcrete = Field(default=MaterialConcrete(), description="Concrete properties")
    rebar: Optional[MaterialRebar] = Field(default=MaterialRebar(), description="Rebar properties")
    tendon: Optional[MaterialTendon] = Field(default=MaterialTendon(), description="Tendon properties")

    def __post_init__(self):
        if self.rebar is None and self.tendon is None:
            raise ValueError("Either rebar or tendon must be provided.")

    class Config(MBaseModel.Config):
        title = "Material"

class ConcreteGeometry(MBaseModel):
    """
    GSD concrete geometry class
    
    Args:
        outerPolygon (list[Point]): Outer polygon of the concrete
        innerPolygon (list[Point]): Inner polygon of the concrete
    """
    outerPolygon: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), 
                                               Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)), Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Outer polygon of the concrete")
    innerPolygon: list[Point] = Field(default=[Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)), Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)),
                                               Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM)), Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM))], description="Inner polygon of the concrete")

    class Config(MBaseModel.Config):
        title = "Concrete Geometry"

class RebarGeometry(MBaseModel):
    """
    GSD rebar geometry class

    Args:
        prop (RebarProp): properties of the rebar
        points (list[Point]): Rebar Points
    """
    prop: RebarProp = Field(default=RebarProp(), description="properties of the rebar")
    points: list[Point] = Field(default=[Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)), Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM)), Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM))], description="Rebar Points")

    class Config(MBaseModel.Config):
        title = "Rebar Geometry"

class TendonGeometry(MBaseModel):
    """
    GSD tendon geometry class
    
    Args:
        prop (TendonProp): properties of the tendon
        points (list[Point]): Tendon Points
    """
    prop: TendonProp = Field(default=TendonProp(), description="properties of the tendon")
    points: list[Point] = Field(default=[], description="Tendon Points")

    class Config(MBaseModel.Config):
        title = "Tendon Geometry"

class Geometry(MBaseModel):
    """
    GSD geometry class

    Args:
        concrete (ConcreteGeometry): Concrete geometry
        rebar (RebarGeometry): Rebar geometry
        tendon (TendonGeometry): Tendon geometry
    """
    concrete: ConcreteGeometry = Field(default=ConcreteGeometry(), description="Concrete geometry")
    rebar: Optional[list[RebarGeometry]] = Field(default=[RebarGeometry()], description="Rebar geometry")
    tendon: Optional[list[TendonGeometry]] = Field(default=[TendonGeometry()], description="Tendon geometry")

    class Config(MBaseModel.Config):
        title = "Geometry"

class SlabMember_EC(MBaseModel):
    """
    Slab Member
    """
    fck: Stress = Field(default=Stress(value=24.0, unit=enUnitStress.MPa), title="fck", description="Concrete strength")
    thickness: Length = Field(default=Length(value=150.0, unit=enUnitLength.MM), title="Slab thick", description="Slab thickness")

    class Config(MBaseModel.Config):
        title = "Slab Member"
        description = "Slab Member with concrete strength and thickness"

class GirderLength(MBaseModel):
    """
    Girder Length
    """
    span: Length = Field(default=Length(value=10.0, unit=enUnitLength.M), title="Span length", description="Span Length")
    spacing: Length = Field(default=Length(value=3.0, unit=enUnitLength.M), title="Spacing", description="Spacing")

    class Config(MBaseModel.Config):
        title = "Girder Length"
        description = "Provides the information needed to define the lengths and spacing of lattice beams in a structure. This information is essential to ensure that spans and spacing are properly accounted for in the structural design to ensure load distribution and safety. "

class NeutralAxisDepth(MBaseModel):
    """
    Neutral Axis Depth
    """
    depth: Length = Field(default=Length(value=0.0, unit=enUnitLength.MM), title="Neutral Axis Depth", description="Neutral Axis Depth")

    class Config(MBaseModel.Config):
        title = "Neutral Axis Depth"
        description = "Neutral Axis Depth"

class RebarNumberNameCover(MBaseModel):
    """
    Rebar Number
    """
    number: int = Field(default=2, title="Number", description="Number of Rebar")
    name: str = Field(default="P26", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))
    cover: Length = Field(default=Length(value=20.0, unit=enUnitLength.MM), title="Cover", description="Distance from centroid of reinforcement to the nearest surface of the concrete")

    class Config(MBaseModel.Config):
        title = "Rebar Number"
        description = "Rebar Number"

class RebarNumberNameSpace(MBaseModel):
    """
    Rebar Number Name Space
    """
    number: int = Field(default=2, title="Number", description="Number of legs")
    name: str = Field(default="P10", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))
    space: Length = Field(default=Length(value=100.0, unit=enUnitLength.MM), title="Space", description="Distance between rebars")

    class Config(MBaseModel.Config):
        title = "Rebar Number"
        description = "Rebar Number"

class BeamRebarPattern(MBaseModel):
    top: list[RebarNumberNameCover] = Field(default=[RebarNumberNameCover()], title="Top", description="Top Rebar")
    bot: list[RebarNumberNameCover] = Field(default=[RebarNumberNameCover()], title="Bot", description="Bottom Rebar")
    stirrup: RebarNumberNameSpace = Field(default=RebarNumberNameSpace(), title="Stirrup", description="Stirrup Rebar")

    class Config(MBaseModel.Config):
        title = "Beam Rebar Pattern"
        description = "Beam Rebar Pattern"