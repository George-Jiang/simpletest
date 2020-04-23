import ezdxf

def process(filename,top_number, bottom_number):
    dwg = ezdxf.readfile(filename)
    msp = dwg.modelspace()
    
    def process(layer, number, msp = msp):
        bar_text = msp.query('TEXT[layer == "{}"]'.format(layer))
        for each in bar_text:
            if float(each.dxf.text) < float(number):
                msp.delete_entity(each)
            else:
                each.dxf.color = 1
    process('12', bottom_number)
    process('13', top_number)
    dwg.save()