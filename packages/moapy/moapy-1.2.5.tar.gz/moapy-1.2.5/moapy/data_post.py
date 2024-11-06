from pydantic import Field
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Force, Lcom

class ResultMD(MBaseModel):
    """
    Result Markdown
    """
    md: str = Field(default="", description="Markdown")

    class Config(MBaseModel.Config):
        title = "Markdown"

class ResultBytes(MBaseModel):
    """
    Result Bytes
    """
    type: str = Field(default="xlsx", description="Type")
    result: str = Field(default="", description="have to base64 to binary data")

    class Config(MBaseModel.Config):
        title = "Bytes"

class Mesh3DPM(MBaseModel):
    """
    3D P-M onion mesh result class

    Args:
        mesh3dpm (list[Force]): onion mesh result
    """
    mesh3dpm : list[Force] = Field(default=[], description="onion mesh result")

    class Config(MBaseModel.Config):
        title = "3DPM onion mesh result"

class Result3DPM(MBaseModel):
    """
    GSD 3DPM result class
    
    Args:
        meshes (Mesh3DPM): 3DPM onion result
        lcbs (list[Lcom]): Load combination
        strength (list[Lcom]): Strength result
    """
    meshes: Mesh3DPM = Field(default=Mesh3DPM(), description="3DPM onion result")
    lcbs: list[Lcom] = Field(default=[], description="Load combination")
    strength: list[Lcom] = Field(default=[], description="Strength result")

    class Config(MBaseModel.Config):
        title = "3DPM Result"

class SectionProperty(MBaseModel):
    """
    Section Property
    """
    Area: float = Field(default=0.0, description="Area")
    Asy: float = Field(default=0.0, description="Asy")
    Asz: float = Field(default=0.0, description="Asz")
    Ixx: float = Field(default=0.0, description="Ixx")
    Iyy: float = Field(default=0.0, description="Iyy")
    Izz: float = Field(default=0.0, description="Izz")
    Cy: float = Field(default=0.0, description="Cy")
    Cz: float = Field(default=0.0, description="Cz")
    Syp: float = Field(default=0.0, description="Syp")
    Sym: float = Field(default=0.0, description="Sym")
    Szp: float = Field(default=0.0, description="Szp")
    Szm: float = Field(default=0.0, description="Szm")
    Ipyy: float = Field(default=0.0, description="Ipyy")
    Ipzz: float = Field(default=0.0, description="Ipzz")
    Zy: float = Field(default=0.0, description="Zy")
    Zz: float = Field(default=0.0, description="Zz")
    ry: float = Field(default=0.0, description="ry")
    rz: float = Field(default=0.0, description="rz")

    class Config:
        title = "Section Property"