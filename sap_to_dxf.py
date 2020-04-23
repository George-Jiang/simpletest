import pandas as pd
import ezdxf
import os


def get_frames(filename):
    frames = pd.read_excel(filename, 'Connectivity - Frame', index_col= 0, skiprows= 1)
    frames = frames[1:]
    frame_sections = pd.read_excel(filename, 'Frame Section Assignments', index_col= 0, skiprows= 1)
    frame_sections = frame_sections[1:]
    frames = pd.merge(frames, frame_sections, on = 'Frame')
    coordinates = pd.read_excel(filename, 'Joint Coordinates', index_col= 0, skiprows= 1)
    coordinates = coordinates[1:]
    coordinates['Coor'] = coordinates.apply(lambda x: (x.GlobalX, x.GlobalY, x.GlobalZ), axis=1)
    frames.JointI = frames.JointI.apply(lambda x: coordinates.Coor[x])
    frames.JointJ = frames.JointJ.apply(lambda x: coordinates.Coor[x])
    frames = frames[['JointI','JointJ',"AnalSect"]]
    return(frames)


def to_dxf(filename):
    def create_layers_fonts(section_name_list,dwg):
        dwg.styles.new('custom', dxfattribs={'font': 'times.ttf', 'width': 0.8})
        for i, each in enumerate(section_name_list):
            dwg.layers.new(name = each, dxfattribs={'color': i + 1})
    frames = get_frames(filename)
    dwg = ezdxf.new('AC1024')
    msp = dwg.modelspace()
    create_layers_fonts(frames.AnalSect.unique(), dwg)
    for each in frames.index:
        row = frames.loc[each]
        msp.add_line(row.JointI, row.JointJ, dxfattribs= {'layer': row.AnalSect})
    filename = filename.replace('.xlsx','.dxf')
    dwg.saveas(filename)