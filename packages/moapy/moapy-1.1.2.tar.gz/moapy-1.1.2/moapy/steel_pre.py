from pydantic import Field as dataclass_field
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enConnectionType, enUnitLength, en_H_EN10365, enSteelMaterial_EN10025, en_H_AISC05_US, enBoltName, enBoltMaterialEC
from moapy.data_pre import Length

# ==== Steel DB ====
class SteelLength(MBaseModel):
    """
    Steel DB Length
    """
    l_x: Length = dataclass_field(default=Length(value=3000.0, unit=enUnitLength.MM), title="Lx", description="Unbraced length(x-direction)")
    l_y: Length = dataclass_field(default=Length(value=3000.0, unit=enUnitLength.MM), title="Ly", description="Unbraced length(y-direction)")
    l_b: Length = dataclass_field(default=Length(value=3000.0, unit=enUnitLength.MM), title="Lb", description="Lateral unbraced length")

    class Config(MBaseModel.Config):
        title = "Member Length"
        description = "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."

class SteelLength_EC(SteelLength):
    """
    Steel DB Length
    """
    l_t: Length = dataclass_field(default=Length(value=3000.0, unit=enUnitLength.MM), title="Lt", description="Torsional Buckling Length")

    class Config(MBaseModel.Config):
        title = "Member Length"
        description = "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."

class SteelMomentModificationFactor(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_mx: float = dataclass_field(default=1.0, title="Cmx", description="Cmx Modification Factor")
    c_my: float = dataclass_field(default=1.0, title="Cmy", description="Cmy Modification Factor")

    class Config(MBaseModel.Config):
        title = "Steel Moment Modification Factor"
        description = "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."

class SteelMomentModificationFactor_EC(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    c1: float = dataclass_field(default=1.0, title="C1", description="ratio between the critical bending moment and the critical constant bending moment for a member with hinged supports")
    c_mlt: float = dataclass_field(default=1.0, title="Cmlt", description="equivalent uniform moment factor for LTB")

    class Config(MBaseModel.Config):
        title = "Steel Moment Modification Factor"
        description = "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."

class SteelSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = dataclass_field(default='H', description="Shape of member section", readOnly=True)
    name: str = dataclass_field(default='H 400x200x8/13', description="Section Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Section"
        description = "Steel DB Section"

class SteelSection_AISC05_US(SteelSection):
    """
    Steel DB Section
    """
    shape: str = dataclass_field(default='H', description="Shape of member section", readOnly=True)
    name: str = dataclass_field(default='W40X362', description="Please select a section.", enum=enum_to_list(en_H_AISC05_US))

    class Config(MBaseModel.Config):
        title = "Steel DB Section"
        description = "Currently, only H-sections are supported."

class SteelSection_EN10365(SteelSection):
    """
    Steel DB Section wit
    """
    shape: str = dataclass_field(default='H', description="Shape of member section", readOnly=True)
    name: str = dataclass_field(default='HD 260x54.1', description="Use DB stored in EN10365", enum=enum_to_list(en_H_EN10365))

    class Config(MBaseModel.Config):
        title = "Steel DB Section"
        description = "EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."

class SteelMaterial(MBaseModel):
    """
    Steel DB Material
    """
    code: str = dataclass_field(default='KS18(S)', description="Material Code", readOnly=True)
    name: str = dataclass_field(default='SS275', description="Material Name")

    class Config(MBaseModel.Config):
        title = "Steel DB Material"
        description = "Steel DB Material"

class SteelMaterial_EC(SteelMaterial):
    """
    Steel DB Material
    """
    code: str = dataclass_field(default='EN10025', description="Material code", readOnly=True)
    name: str = dataclass_field(default='S275', description="Material of steel member", enum=enum_to_list(enSteelMaterial_EN10025))

    class Config(MBaseModel.Config):
        title = "Steel DB Material"
        description = "EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."

class BoltMaterial(MBaseModel):
    """
    Bolt Material
    """
    name: str = dataclass_field(default='F10T', description="Bolt Material Name")

    class Config(MBaseModel.Config):
        title = "Bolt Material"
        description = "Bolt Material"

class BoltMaterial_EC(BoltMaterial):
    """
    Bolt Material
    """
    name: str = dataclass_field(default='4.8', description="Bolt Material Name", enum=enum_to_list(enBoltMaterialEC))

    class Config(MBaseModel.Config):
        title = "Bolt Material"
        description = "Bolt Material"

class SteelMember(MBaseModel):
    """
    Steel Member
    """
    sect: SteelSection = dataclass_field(default=SteelSection(), description="Section")
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")

    class Config(MBaseModel.Config):
        title = "Steel Member"
        description = "Steel sections and material inputs are fundamental elements of structural design, each requiring proper selection based on their characteristics and requirements. This maximizes the strength, stability, and durability of the structure and contributes to designing a safe and efficient structure."

class SteelMember_EC(SteelMember):
    """
    Steel Member
    """
    sect: SteelSection_EN10365 = dataclass_field(default=SteelSection_EN10365(), title="Section", description="Shape of section")
    matl: SteelMaterial_EC = dataclass_field(default=SteelMaterial_EC(), title="Material", description="Material of steel member")

    class Config(MBaseModel.Config):
        title = "Steel Member"
        description = "Steel sections and material inputs are fundamental elements of structural design, each requiring proper selection based on their characteristics and requirements. This maximizes the strength, stability, and durability of the structure and contributes to designing a safe and efficient structure."

class SteelConnectMember(MBaseModel):
    """
    Steel Connect Member
    """
    supporting: SteelMember = dataclass_field(default=SteelMember(), description="Supporting Member")
    supported: SteelMember = dataclass_field(default=SteelMember(), description="Supported Member")

    class Config(MBaseModel.Config):
        title = "Steel Connect Member"
        description = "Supporting and supported sections play complementary roles in bolted connections and make important contributions to the load bearing and transfer of the structure. The correct design and analysis of these two sections is essential to ensure the stability and durability of the structure."

class SteelConnectMember_EC(SteelConnectMember):
    """
    Steel Connect Member
    """
    supporting: SteelMember_EC = dataclass_field(default=SteelMember_EC(), title="Supporting member", description="Supporting Member")
    supported: SteelMember_EC = dataclass_field(default=SteelMember_EC(), title="Supported member", description="Supported Member")

    class Config(MBaseModel.Config):
        title = "Steel Connect Member"
        description = "Supporting and supported sections play complementary roles in bolted connections and make important contributions to the load bearing and transfer of the structure. The correct design and analysis of these two sections is essential to ensure the stability and durability of the structure."

class SteelBoltConnectionForce(MBaseModel):
    """
    Steel Bolt Connection Force
    """
    percent: float = dataclass_field(default=30.0, title="Strength design(%)", description="Generally section of steel beam is determined by bending moment, typically shear is set 30% as default because there is no problem even if shear is assumed to about 30 % of member strength. If it is required to consider 100% of member strength, change the entered value.")

    class Config(MBaseModel.Config):
        title = "Steel Bolt Connection Force"
        description = "Steel Bolt Connection Force"

class SteelBolt(MBaseModel):
    """
    Steel Bolt
    """
    name: str = dataclass_field(default='M16', title="bolt name", description="bolt size", enum=enum_to_list(enBoltName))
    matl: BoltMaterial = dataclass_field(default=BoltMaterial(), title="bolt material", description="Material of bolt")

    class Config(MBaseModel.Config):
        title = "Steel Bolt"
        description = "Steel Bolt"

class SteelBolt_EC(MBaseModel):
    """
    Steel Bolt
    """
    name: str = dataclass_field(default='M20', title="Bolt name", description="Bolt size", enum=enum_to_list(enBoltName))
    matl: BoltMaterial_EC = dataclass_field(default=BoltMaterial_EC(), title="Bolt material", description="Material of bolt")

    class Config(MBaseModel.Config):
        title = "Steel Bolt"
        description = """A bolt is a mechanical element that connects members of a structure and is used to transfer loads.\n
            Diameter: The outer diameter of a bolt, usually expressed in a metric system such as M6, M8, M10, etc.\n
            Length: The overall length of the bolt, determined by the thickness of the connecting members.\n
            Class: The strength rating, expressed as a class, for example 8.8, 10.9, etc., where higher numbers increase strength.
            """

class ShearConnector(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt = dataclass_field(default=SteelBolt(), description="stud bolt")
    num: int = dataclass_field(default=1, description="stud column")
    space: Length = dataclass_field(default=Length(value=300.0, unit=enUnitLength.MM), description="stud spacing")
    length: Length = dataclass_field(default=Length(value=100.0, unit=enUnitLength.MM), description="stud length")

    class Config(MBaseModel.Config):
        title = "Shear Connector"
        description = "Shear Connector"

class ShearConnector_EC(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt_EC = dataclass_field(default=SteelBolt_EC(name="M19"), title="Bolt specifications", description="Stud bolt")
    num: int = dataclass_field(default=1, title="Number", description="Stud column")
    space: Length = dataclass_field(default=Length(value=300.0, unit=enUnitLength.MM), title="Stud Spacing", description="Stud spacing")
    length: Length = dataclass_field(default=Length(value=100.0, unit=enUnitLength.MM), title="Stud Length", description="Stud length")

    class Config(MBaseModel.Config):
        title = "Shear Connector"
        description = "Shear connections play an important role in ensuring the strength and stability of a structure, and they come in a variety of shapes and materials to meet different structural requirements. When used properly and in accordance with design criteria, shear connections can contribute to the safety and durability of a structure."

class Welding(MBaseModel):
    """
    Welding
    """
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")
    length: Length = dataclass_field(default=Length(value=6.0, unit=enUnitLength.MM), description="Leg of Length")

    class Config(MBaseModel.Config):
        title = "Welding"
        description = "Welding"

class Welding_EC(Welding):
    """
    Welding
    """
    matl: SteelMaterial_EC = dataclass_field(default=SteelMaterial_EC(), description="Material")
    length: Length = dataclass_field(default=Length(value=6.0, unit=enUnitLength.MM), description="Leg of Length")

    class Config(MBaseModel.Config):
        title = "Welding"
        description = "Information for reviewing welds on supporting members."

class SteelPlateMember(MBaseModel):
    """
    Steel Plate Member
    """
    matl: SteelMaterial = dataclass_field(default=SteelMaterial(), description="Material")
    bolt_num: int = dataclass_field(default=4, description="Number of Bolts")
    thk: Length = dataclass_field(default=Length(value=6.0, unit=enUnitLength.MM), description="Thickness")

    class Config(MBaseModel.Config):
        title = "Steel Plate Member"
        description = "Steel Plate Member"

class SteelPlateMember_EC(SteelPlateMember):
    """
    Steel Plate Member
    """
    matl: SteelMaterial_EC = dataclass_field(default=SteelMaterial_EC(), title="Plate material", description="Material")
    bolt_num: int = dataclass_field(default=4, title="Number of bolt", description="Number of Bolts")
    thk: Length = dataclass_field(default=Length(value=6.0, unit=enUnitLength.MM), title="Thickness", description="Thickness of plate")

    class Config(MBaseModel.Config):
        title = "Steel Plate Member"
        description = "Steel Plate Member"

class ConnectType(MBaseModel):
    """
    Connect Type class

    Args:
        type (str): Connection type
    """
    type: str = dataclass_field(default="Fin Plate - Beam to Beam", title="Connect type", description="Connect type", enum=enum_to_list(enConnectionType))

    class Config(MBaseModel.Config):
        title = "Connection Type"
        description = """
            The four types of bolted connections mentioned are described below:
            \n
            1. Fin Plate - Beam to Beam (Fin_B_B) \n
            This is the use of a fin plate to connect two beams, where a fin plate is attached to the end of each beam to connect them together.
            \n\n
            2. Fin Plate - Beam to Column (Fin_B_C)\n
            A method of connecting beams to columns, where fin plates are attached to the sides of the columns and the ends of the beams to create a solid connection.
            \n\n
            3. End Plate - Beam to Beam (End_B_B)\n
            A method of connecting two beams using end plates at the ends. An end plate is attached to the end of each beam and connected via bolts.
            \n\n
            4. End Plate - Beam to Column (End_B_C)\n
            This method of connecting beams to columns uses end plates attached to the sides of the columns to connect with the ends of the beams. Bolts are secured to the column through the end plate.
            """
