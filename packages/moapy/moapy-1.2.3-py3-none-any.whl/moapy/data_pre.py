from pydantic import Field
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import (
    enUnitThermalExpansion, enum_to_list, enDgnCode, enEccPu, enReportType,
    enUnitTemperature, enUnitLength, enUnitStress, enUnitForce, enUnitMoment, enUnitLoad, enUnitAngle, enUnitArea)

# ==== Base ====
class Angle(MBaseModel):
    """
    Angle class
    """
    value: float = Field(default=0.0, description="Angle value")
    unit: enUnitAngle = Field(default=enUnitAngle.Degree)

class Load(MBaseModel):
    """
    Load class
    """
    value: float = Field(default=0.0, description="Load value")
    unit: enUnitLoad = Field(default=enUnitLoad.kN_m2)

class Temperature(MBaseModel):
    """
    Thermal
    """
    value: float = Field(default=0.0, description="Temperature")
    unit: enUnitTemperature = Field(default=enUnitTemperature.Celsius)

class Length(MBaseModel):
    """
    Length
    """
    value: float = Field(default=0.0, description="Length")
    unit: enUnitLength = Field(default=enUnitLength.MM)

class Area(MBaseModel):
    """
    Area
    """
    value: float = Field(default=0.0, description="Area")
    unit: enUnitArea = Field(default=enUnitArea.MM2)

class Force(MBaseModel):
    """
    Force
    """
    value: float = Field(default=0.0, description="Force")
    unit: enUnitForce = Field(default=enUnitForce.kN)

class Moment(MBaseModel):
    """
    Moment
    """
    value: float = Field(default=0.0, description="Moment")
    unit: enUnitMoment = Field(default=enUnitMoment.kNm)

class Stress(MBaseModel):
    """
    Stress
    """
    value: float = Field(default=0.0, description="Stress")
    unit: enUnitStress = Field(default=enUnitStress.MPa)

class ThermalExpansionCoeff(MBaseModel):
    """
    Thermal Expansion Coefficient
    """
    value: float = Field(default=1.0, description="Thermal Expansion Coefficient")
    unit: enUnitThermalExpansion = Field(default=enUnitThermalExpansion.PER_CELSIUS)

# ==== Length ====
class EffectiveLength(MBaseModel):
    """
    Effective Length class
    """
    kx: float = Field(default=1.0, title="Kx", description="Effect buckling length factor(x direction)")
    ky: float = Field(default=1.0, title="Ky", description="Effect buckling length factor(y direction)")

    class Config(MBaseModel.Config):
        title = "Effective Length"
        description = "The Effective Length Factor is an important parameter used to evaluate the ability of a column or member in a structure to resist buckling. This factor adjusts the actual length of the member to help analyze buckling based on the anchorage conditions of the column. The effective buckling length factor defines the relationship between the buckling length and the column's anchorage conditions."

# ==== Forces ====
class UnitLoads(MBaseModel):
    """
    Unit Loads class
    """
    construction: Load = Field(default_factory=Load, title="Construction load", description="Input construction load")
    live: Load = Field(default_factory=Load, title="Live load", description="Input live load")
    finish: Load = Field(default_factory=Load, title="Finish load", description="Input finishing load")

    class Config(MBaseModel.Config):
        title = "Unit Loads"
        description = "You need to define the different loads that need to be considered in architectural and structural design. By providing specific information about each type of load, engineers can evaluate and design the safety and performance of structures."

class SectionForce(MBaseModel):
    """Force class

    Args:
        Fz (float): Axial force
        Mx (float): Moment about x-axis
        My (float): Moment about y-axis
        Vx (float): Shear about x-axis
        Vy (float): Shear about y-axis
    """
    Fz: Force = Field(default_factory=Force, title="Fz", description="Axial force")
    Mx: Moment = Field(default_factory=Moment, title="Mx", description="Moment about x-axis")
    My: Moment = Field(default_factory=Moment, title="My", description="Moment about y-axis")
    Vx: Force = Field(default_factory=Force, title="Vx", description="Shear about x-axis")
    Vy: Force = Field(default_factory=Force, title="Vy", description="Shear about y-axis")

    class Config(MBaseModel.Config):
        title = "Member Force"
        description = "Enter the member forces for the design load combination."

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: Force = Field(default_factory=Force, title="Nx", description="Axial Force")

    class Config:
        title = "Axial Force Option"

class DesignCode(MBaseModel):
    """Design Code class

    Args:
        design_code (str): Design code
        sub_code (str): Sub code
    """    
    design_code: str = Field(default="ACI 318-19", max_length=30)
    sub_code: str = Field(default="SI")

    class Config(MBaseModel.Config):
        title = "Design Code"

class DgnCode(MBaseModel):
    """
    DgnCode
    """
    name: str = Field(default="", description="DgnCode")

    class Config:
        title = "DgnCode"

# ==== Lcoms ====
class Lcom(MBaseModel):
    """
    Lcom class

    Args:
        name (str): load combination name
        f (Force): load combination force
    """
    name: str = Field(default="lcom", description="load combination name")
    f: SectionForce = Field(default_factory=SectionForce, title="force", description="load combination force")

    class Config(MBaseModel.Config):
        title = "Lcom Result"

class Lcoms(MBaseModel):
    """
    Lcoms class

    Args:
        lcoms (list[Lcom]): load combination result
    """
    lcoms: list[Lcom] = Field(default=[Lcom(name="uls1", f=SectionForce(Fz=Force(value=100.0, unit=enUnitForce.kN),
                                                                                 Mx=Moment(value=10.0, unit=enUnitMoment.kNm),
                                                                                 My=Moment(value=50.0, unit=enUnitMoment.kNm)))], description="load combination result")

    class Config(MBaseModel.Config):
        title = "Strength Result"

class AngleOpt(MBaseModel):
    """
    Angle Option
    """
    theta: Angle = Field(default_factory=Angle, title="angle", description="theta")

    class Config:
        title = "Theta Option"

class ElasticModulusOpt(MBaseModel):
    """
    Elastic Modulus Option
    """
    E: Stress = Field(default=Stress(value=200.0, unit=enUnitStress.MPa), title="E", description="Elastic Modulus")

    class Config:
        title = "Elastic Modulus Option"

class Unit(MBaseModel):
    """
    GSD global unit class
    
    Args:
        force (str): Force unit
        length (str): Length unit
        section_dimension (str): Section dimension unit
        pressure (str): Pressure unit
        strain (str): Strain unit
    """
    force: str = Field(
        default="kN", description="Force unit")
    length: str = Field(
        default="m", description="Length unit")
    section_dimension: str = Field(
        default="mm", description="Section dimension unit")
    pressure: str = Field(
        default="MPa", description="Pressure unit")
    strain: str = Field(
        default="%", description="Strain unit")

    class Config(MBaseModel.Config):
        title = "Unit"

# ==== Stress Strain Curve ====
class Stress_Strain_Component(MBaseModel):
    """Stress Strain Component class

    Args:
        stress (float): Stress
        strain (float): Strain
    """
    stress: float = Field(default=0.0, description="Stress")
    strain: float = Field(default=0.0, description="Strain")

    class Config(MBaseModel.Config):
        title = "Stress Strain Component"

# ==== Materials ====
class MaterialCurve(MBaseModel):
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

# ==== Geometry ====
class Point(MBaseModel):
    """
    Point class

    Args:
        x (float): x-coordinate
        y (float): y-coordinate
    """
    x: Length
    y: Length

    class Config(MBaseModel.Config):
        title = "Point"

class Points(MBaseModel):
    """
    GSD Points class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Points")

    class Config(MBaseModel.Config):
        title = "Points"

class OuterPolygon(MBaseModel):
    """
    GSD Outer Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Outer Polygon")

    class Config(MBaseModel.Config):
        title = "Outer Polygon"

class InnerPolygon(MBaseModel):
    """
    GSD Inner Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), 
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), 
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)), 
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Inner Polygon")

    class Config(MBaseModel.Config):
        title = "Inner Polygon"

class Lcb(MBaseModel):
    """
    GSD load combination class

    Args:
        uls (Lcoms): uls load combination
    """
    uls: Lcoms = Field(default=Lcoms(), description="uls load combination")

    class Config(MBaseModel.Config):
        title = "Load Combination"

# ==== options ====
class PMOptions(MBaseModel):
    """
    GSD options class
    
    Args:
        dgncode (str): Design code
        by_ecc_pu (str): ecc
    """
    dgncode: str = Field(default=enDgnCode.Eurocode2_04, description="Design code", enum=enum_to_list(enDgnCode))
    by_ecc_pu: str = Field(default="ecc", description="ecc or P-U", enum=enum_to_list(enEccPu))

    class Config(MBaseModel.Config):
        title = "Options"

class ReportType(MBaseModel):
    """
    Report Type class
    
    Args:
        report_type (str): Report type
    """
    type: str = Field(default="markdown", description="Report type", enum=enum_to_list(enReportType))

    class Config(MBaseModel.Config):
        title = "Report Type"

# ==== Section ====
class SectionRectangle(MBaseModel):
    """
    Section Rectangle class

    Args:
        b (float): Width
        h (float): Height
    """
    b: Length = Field(default=Length(value=400.0, unit=enUnitLength.MM), title="b", description="Width")
    h: Length = Field(default=Length(value=600.0, unit=enUnitLength.MM), title="h", description="Height")

    class Config(MBaseModel.Config):
        title = "Section Rectangle"
