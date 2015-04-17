from variables import *

def output(t, x, qq, filename, adding=True):
    if adding:
        myfile = open(filename, 'a')
    else:
        myfile = open(filename, 'w')

    myfile.write("\n \n #Time = %.10f \n" %(t))
    
    for i in range(len(x)):
        myfile.write(str(x[i]) + "  ")
        for j in range(len(qq[:, i])):
            myfile.write(str(qq[j, i]) + "  ")
        myfile.write("\n")

    myfile.close()

def output_files(t, x, prim, cons, auxl, adding=True):
    output(t, x, prim, 'prim.dat', adding)
    output(t, x, cons, 'cons.dat', adding)
    output(t, x, auxl, 'auxl.dat', adding)

def output_info(t, x, info, adding=True):

    x = x - 0.5*DX

    info_dict = {
        'prim_l' : 0,
        'prim_r' : 1,
        'cons_l' : 2,
        'cons_r' : 3,
        'flux_l' : 4,
        'flux_r' : 5,
        'flux'   : 6,
    }

    for k, v in info_dict.iteritems():
        filestr = k + '.dat'
        output(t, x, info[v], filestr, adding)
