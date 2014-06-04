from pandas import *

def insertRadialPos(df):
    radial=pow(pow(df['positions_0'],2) + pow(df['positions_1'],2),0.5)
    df['radial'] = Series(radial, index=df.index)

def insertCharBurnout(df):
    burnoutPerc = map(lambda Yash:max(Yash/0.92005-0.086897451,0),df['Yash(s)_0'])
    df['burnout'] = Series(burnoutPerc, index=df.index)

def insertParcelMass(df):
    massP = df['rho_0']*pow(df['d_0'],3)/6.0*3.141*df['nParticle_0']
    df['massParcel'] = Series(massP, index=df.index)

def insertParticleMass(df):
    massP = df['rho_0']*pow(df['d_0'],3)/6.0*3.141
    df['massParticle'] = Series(massP, index=df.index)

def calc_concentrations(name):
    CO  = (28.0, 2)
    CO2 = (44.0, 1) 
    H2O = (18.0, 4)
    O2  = (32.0, 5)
    TAR = (50.0, 3)
    N2  = (28.0, -1)

    time = str(max(name['sets'].keys()))
    thermo = 'centerLine_CO2Mean_COMean_CxHyOzMean_H2OMean_O2Mean_T_TMean_pdMean_pdPrime2Mean.xy_{}'
    d = name['sets'][time]

    def Y(spec, data):
        return data[thermo.format(spec[1])]
    
    YN2 = 1 - (Y(O2,d)+Y(CO,d)+Y(CO2,d)+Y(H2O,d)+Y(TAR,d))
    XN2 = YN2/N2[0]    
 
    def X(spec, data):
        return Y(spec, data)/spec[0]

    MW_MIX = 1/(X(CO,d) + X(CO2,d) + X(H2O,d) + X(O2,d) + X(TAR,d) + XN2)

    d['XCO_0'] = Y(CO,d)*MW_MIX/CO[0]
    d['XO2_0'] = Y(O2,d)*MW_MIX/O2[0]
    d['XN2_0'] = YN2*MW_MIX/N2[0]
    d['XCO2_0'] = Y(CO2,d)*MW_MIX/CO2[0]
    d['XH2O_0'] = Y(H2O,d)*MW_MIX/H2O[0]
    d['XTAR_0'] = Y(TAR,d)*MW_MIX/TAR[0]

def stateOverDist(Y, Dist, d, rho, n , charburnOut, limits):
    totN = len(Y)
    totMass = 0.0
    minDist= -0.21
    #deltaZ =  (max(Dist)-minDist)/49.0
    deltaZ =  (3.5-minDist)/99.0
    b=[]    # states vector
    for i in range(0,100):
        b.append([0.0,0.0,0.0,0.0,0.0,0.0])
        b[i][4]=float(i)*deltaZ  
    try:
        #for i in range(0,totN):
        for i,Yval in Y.iteritems():
            mass = float(rho[i])*pow(float(d[i]),3)/6.0*3.141*float(n[i])
            if mass > 1.0:
                mass = 0.0 # exclude akward particles for now
            totMass += mass
            j=int((Dist[i]-minDist)/deltaZ) 
            if Y[i]<=limits[0]: # nothing
                b[j][0]+=mass
            if Y[i]>limits[0] and Y[i]<limits[1]: # ongoing devol
                b[j][1]+=mass
            if Y[i]>=limits[1] and Y[i] < 1.0:  # ongoing char combustion
                b[j][2]+=mass
            if Y[i] ==1.0:      # fully burned
                b[j][3]+=mass
            b[j][5]+=mass*charburnOut[i]
    except:
        pass
    for i in range(0,100):
            massOfPos=b[i][0]+b[i][1]+b[i][2]+b[i][3]+1e-50
            b[i][5]=b[i][5]/massOfPos
    return b,totMass 
