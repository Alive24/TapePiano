__calibrateTable = [1.00] * 88

# Make Calibration Here. Index = noteId - 1

__calibrateTable[0] = 0.85
__calibrateTable[1] = 0.85
__calibrateTable[2] = 0.85
__calibrateTable[3] = 0.85
__calibrateTable[4] = 0.85
__calibrateTable[5] = 0.85
__calibrateTable[6] = 0.85
__calibrateTable[7] = 0.85
__calibrateTable[8] = 0.85
__calibrateTable[9] = 0.85
__calibrateTable[10] = 0.85
__calibrateTable[11] = 0.85
__calibrateTable[12] = 0.92
__calibrateTable[13] = 0.92
__calibrateTable[14] = 0.92
__calibrateTable[15] = 0.92
__calibrateTable[16] = 0.92
__calibrateTable[17] = 0.92
__calibrateTable[18] = 0.92
__calibrateTable[19] = 0.92
__calibrateTable[20] = 0.92
__calibrateTable[21] = 0.92
__calibrateTable[22] = 0.92
__calibrateTable[23] = 0.92
__calibrateTable[24] = 0.97
__calibrateTable[25] = 0.97
__calibrateTable[26] = 0.97
__calibrateTable[27] = 0.97
__calibrateTable[28] = 0.97
__calibrateTable[29] = 0.97
__calibrateTable[30] = 0.97
__calibrateTable[31] = 0.97
__calibrateTable[32] = 0.97
__calibrateTable[33] = 0.97
__calibrateTable[34] = 0.97
__calibrateTable[35] = 0.97
__calibrateTable[44] = 0.85
__calibrateTable[45] = 0.85
__calibrateTable[46] = 0.85
__calibrateTable[47] = 0.85
__calibrateTable[48] = 0.85
__calibrateTable[49] = 0.85
__calibrateTable[50] = 0.85
__calibrateTable[51] = 0.85
__calibrateTable[52] = 0.85
__calibrateTable[53] = 0.85
__calibrateTable[54] = 0.85
__calibrateTable[55] = 0.85
__calibrateTable[56] = 0.92
__calibrateTable[57] = 0.92
__calibrateTable[58] = 0.92
__calibrateTable[59] = 0.92
__calibrateTable[60] = 0.92
__calibrateTable[61] = 0.92
__calibrateTable[62] = 0.92
__calibrateTable[63] = 0.92
__calibrateTable[64] = 0.92
__calibrateTable[65] = 0.92
__calibrateTable[66] = 0.92
__calibrateTable[67] = 0.92
__calibrateTable[68] = 0.97
__calibrateTable[69] = 0.97
__calibrateTable[70] = 0.97
__calibrateTable[71] = 0.97
__calibrateTable[72] = 0.97
__calibrateTable[73] = 0.97
__calibrateTable[74] = 0.97
__calibrateTable[75] = 0.97
__calibrateTable[76] = 0.97
__calibrateTable[77] = 0.97
__calibrateTable[78] = 0.97
__calibrateTable[79] = 0.97




def getCalibrateRatio(noteId: int) -> float:
    try:
        return __calibrateTable[noteId-1]
    except:
        print("Index out of range.")

