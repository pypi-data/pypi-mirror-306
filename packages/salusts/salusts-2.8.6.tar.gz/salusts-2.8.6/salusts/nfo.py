_ChipZoneEdges_cache = None

def ChipZoneEdges():
    global _ChipZoneEdges_cache
    if _ChipZoneEdges_cache is not None:
        return _ChipZoneEdges_cache

    ChipZoneEdges = {}
    #print('[i]initializing ChipZoneEdges')
    for IDy in ('1','2',''):
        if IDy=='':
            xTuple = map(chr, range(65,69))  # Solo
            yRange = (-21223,21223)  # 42446 +1
        elif IDy=='1':
            xTuple = map(chr, range(65,70))  # DualUpper
            yRange = (-17693,22562)  # 40255 +1
        elif IDy=='2':
            xTuple = map(chr, range(65,70))  # DualLower
            yRange = (-22562,17693)  # 40255 +1
        for IDx in xTuple:
            ZoneID = IDx + IDy
            match IDx:
                case 'A' if IDy != '':
                    xRange = (-111188,-67362)  # Dual
                case 'B' if IDy != '':
                    xRange = (-66551,-22725)
                case 'C' if IDy != '':
                    xRange = (-21913,21913)
                case 'D' if IDy != '':
                    xRange = (22725,66551)
                case 'E' if IDy != '':
                    xRange = (67362,111188)  # 43826 +1
                case 'A' if IDy == '':
                    xRange = (-110783,-57217)  # Solo
                case 'B' if IDy == '':
                    xRange = (-54783,-1217)
                case 'C' if IDy == '':
                    xRange = (1217,54783)
                case 'D' if IDy == '':
                    xRange = (57217,110783)  # 53566 +1
                case _:
                    raise ValueError("[x]It can only be memory error ...")
            ChipZoneEdges[ZoneID] = xRange + yRange
    _ChipZoneEdges_cache = ChipZoneEdges
    return _ChipZoneEdges_cache
