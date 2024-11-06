import ctypes
import json
import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import UnitLoads, SectionRectangle, SectionForce
from moapy.rc_pre import SlabMember_EC, GirderLength, BeamRebarPattern
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes

def report_ec2_beam(sect: SectionRectangle, rebar: BeamRebarPattern, force: SectionForce) -> ResultBytes:
    dll = load_dll()
    json_data_list = [rebar.json(), rebar.json(), rebar.json()]
    file_path = call_func(dll, 'Report_EC2_Beam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_beam(sect: SectionRectangle, rebar: BeamRebarPattern, force: SectionForce) -> dict:
    dll = load_dll()
    json_data_list = [rebar.json(), rebar.json(), rebar.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Beam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    res = report_ec2_beam(SectionRectangle(), BeamRebarPattern(), SectionForce())
    print(res)