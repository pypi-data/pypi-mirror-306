"""
Useful constants for the PAGOS package, all as Quantity objects.
"""
from pagos.core import u as _u

"""
PHYSICAL CONSTANTS

These are generic quantities that will be used throughout the PAGOS package. They are
Quantity objects, so have a magnitude and unit.
"""
# Triple point of water
TPW = 273.15 * _u('K')
# Absolute zero
ABZ = _u.Quantity(-273.15, 'degC') # defined with _u.Quantity() because of nonmultiplicative degC
# Atmospheric pressure
PAT = 101325 * _u('Pa')
# Molar gas constant
MGC = 8.31446 * _u('J/mol/K')
# Specific heat of water at 0°C
#https://www.engineeringtoolbox.com/specific-heat-capacity-water-d_660.html
CPW = 4219.9 * _u('J/kg/K')
# Latent heat of fusion of water
LFW = 333.55e3 * _u('J/kg')


"""
WATER FUNCTION CONSTANTS
"""
# Density coefficients
GILL_82_COEFFS = dict(
a0 = 999.842594         * _u('kg/m^3'),
a1 = 0.06793952         * _u('kg/m^3/K'),
a2 = -0.00909529        * _u('kg/m^3/K^2'),
a3 = 0.0001001685       * _u('kg/m^3/K^3'),
a4 = -0.000001120083    * _u('kg/m^3/K^4'),
a5 = 0.000000006536332  * _u('kg/m^3/K^5'),
b0 = 0.824493           * _u('kg/m^3/permille'),
b1 = -0.0040899         * _u('kg/m^3/K/permille'),
b2 = 0.000076438        * _u('kg/m^3/K^2/permille'),
b3 = -0.00000082467     * _u('kg/m^3/K^3/permille'),
b4 = 0.0000000053875    * _u('kg/m^3/K^4/permille'),
c0 = -0.00572466        * _u('kg/m^3/permille^(3/2)'),
c1 = 0.00010227         * _u('kg/m^3/K/permille^(3/2)'),
c2 = -0.0000016546      * _u('kg/m^3/K^2/permille^(3/2)'),
d0 = 0.00048314         * _u('kg/m^3/permille^2')
)


"""
NON-NUMERICAL CONSTANTS
"""
# TODO do these belong here, or in core? Or in another file?
# names of gases, and groupings by properties
NOBLEGASES = ['He', 'Ne', 'Ar', 'Kr', 'Xe']
STABLETRANSIENTGASES = ['CFC11', 'CFC12', 'SF6']
BIOLOGICALGASES = ['N2']


"""
GAS FUNCTION CONSTANTS
"""
# gas abundances
ABUNDANCES = dict(He=5.24E-6, Ne=18.18E-6, Ar=0.934E-2, Kr=1.14E-6, Xe=0.087E-6, CFC11=218e-12, CFC12=488e-12, SF6=11.5e-12, N2=0.781)

# molar volumes in units of cm3/mol, referenced to 0 degC and 1 atm = 1013.25 mbar, except
# CFC11, whichreferenced to its boiling point of 297 K
# Sources: noble gases, Benson & Krause 1976; stable transient gases, NIST
# NOTE: cannot find them in Benson and Krause
# TODO more digits for CFCs
MOLAR_VOLUMES = dict(He=22425.8703182828*_u('cc/mol'), Ne=22424.8703182828*_u('cc/mol'), Ar=22392.5703182828*_u('cc/mol'), Kr=22352.8703182828*_u('cc/mol'), Xe=22256.9703182828*_u('cc/mol'),
                     SF6=22075.5738997*_u('cc/mol'), CFC11=23807*_u('cc/mol'), CFC12=21844*_u('cc/mol'),
                     N2=22403.8633496*_u('cc/mol'))

# coefficients from Jenkins et al. 2019 solubility formula for noble gases
NG_JENKINS_19_COEFFS = dict(
    He={'A1': -178.1424, 'A2': 217.5991, 'A3': 140.7506, 'A4': -23.01954, 'B1': -0.038129*_u('permille^-1'), 'B2': 0.01919*_u('permille^-1'),
        'B3': -0.0026898*_u('permille^-1'), 'C1': -0.00000255157*_u('permille^-2')},
    Ne={'A1': -274.1329, 'A2': 352.6201, 'A3': 226.9676, 'A4': -37.13393, 'B1': -0.06386*_u('permille^-1'), 'B2': 0.035326*_u('permille^-1'),
        'B3': -0.0053258*_u('permille^-1'), 'C1': 0.0000128233*_u('permille^-2')},
    Ar={'A1': -227.4607, 'A2': 305.4347, 'A3': 180.5278, 'A4': -27.9945, 'B1': -0.066942*_u('permille^-1'), 'B2': 0.037201*_u('permille^-1'),
        'B3': -0.0056364*_u('permille^-1'), 'C1': -5.30325E-06*_u('permille^-2')},
    Kr={'A1': -122.4694, 'A2': 153.5654, 'A3': 70.1969, 'A4': -8.52524, 'B1': -0.049522*_u('permille^-1'), 'B2': 0.024434*_u('permille^-1'),
        'B3': -0.0033968*_u('permille^-1'), 'C1': 4.19208E-06*_u('permille^-2')},
    Xe={'A1': -224.51, 'A2': 292.8234, 'A3': 157.6127, 'A4': -22.66895, 'B1': -0.084915*_u('permille^-1'), 'B2': 0.047996*_u('permille^-1'),
        'B3': -0.0073595*_u('permille^-1'), 'C1': 6.69292E-06*_u('permille^-2')}
)

# coefficients from Wanninkhof 1992 formula for Schmidt number. Xe values obtained by
# fitting curve from Jähne 1987 onto the Wanninkhof curve. These are values for Sc in
# freshwater.
WANNINKHOF_92_COEFFS = dict(
    He = {'A': 377.09, 'B': 19.154*_u('K^-1'), 'C': 0.50137*_u('K^-2'), 'D': 0.005669*_u('K^-3')},
    Ne = {'A': 764.00, 'B': 42.234*_u('K^-1'), 'C': 1.1581*_u('K^-2'), 'D': 0.013405*_u('K^-3')},
    Ar = {'A': 1759.7, 'B': 117.37*_u('K^-1'), 'C': 3.6959*_u('K^-2'), 'D': 0.046527*_u('K^-3')},
    Kr = {'A': 2032.7, 'B': 127.55*_u('K^-1'), 'C': 3.7621*_u('K^-2'), 'D': 0.045236*_u('K^-3')},
    Xe = {'A': 2589.7, 'B': 153.39*_u('K^-1'), 'C': 3.9570*_u('K^-2'), 'D': 0.039801*_u('K^-3')},
    SF6 = {'A': 3255.3, 'B': 217.13*_u('K^-1'), 'C': 6.8370*_u('K^-2'), 'D': 0.086070*_u('K^-3')},
    CFC11 = {'A': 3723.7, 'B': 248.37*_u('K^-1'), 'C': 7.8208*_u('K^-2'), 'D': 0.098455*_u('K^-3')},
    CFC12 = {'A': 3422.7, 'B': 228.30*_u('K^-1'), 'C': 7.1886*_u('K^-2'), 'D': 0.090496*_u('K^-3')},
    N2 = {'A': 1970.7, 'B': 131.45*_u('K^-1'), 'C': 4.1390*_u('K^-2'), 'D': 0.052106*_u('K^-3')}
)

# coefficients from the Jähne 1987 formula (Eyring formula) for Schmidt number. Ar was
# interpolated from Jähne 1987 and N2 is from Ferrel and Himmelblau 1967.
EYRING_36_COEFFS = dict(
    He = {'A': .00818*_u('cm^2/s'), 'Ea': 11.70*_u('kJ/mol')},
    Ne = {'A': .01608*_u('cm^2/s'), 'Ea': 14.84*_u('kJ/mol')},
    Ar = {'A': .02227*_u('cm^2/s'), 'Ea': 16.68*_u('kJ/mol')},
    Kr = {'A': .06393*_u('cm^2/s'), 'Ea': 20.20*_u('kJ/mol')},
    Xe = {'A': .09007*_u('cm^2/s'), 'Ea': 21.61*_u('kJ/mol')},
    N2 = {'A': .03412*_u('cm^2/s'), 'Ea': 18.50*_u('kJ/mol')}
)
# coefficients from Weiss and Kyser 1978 solubility formula for Kr
Kr_WEISSKYSER_78_COEFFS = dict(
    Kr={'A1':-57.2596, 'A2':87.4242, 'A3':22.9332, 'B1':-0.008723, 'B2':-0.002793, 'B3':0.0012398}
)

# coefficients from Warner and Weiss solubility formula for CFC-11 and CFC-12
CFC_WARNERWEISS_85_COEFFS = dict(
    CFC11={'a1': -232.0411, 'a2': 322.5546, 'a3': 120.4956, 'a4': -1.39165, 'b1': -0.146531*_u('permille^-1'), 'b2': 0.093621*_u('permille^-1'),
           'b3': -0.0160693*_u('permille^-1')},
    CFC12={'a1': -220.2120, 'a2': 301.8695, 'a3': 114.8533, 'a4': -1.39165, 'b1': -0.147718*_u('permille^-1'), 'b2': 0.093175*_u('permille^-1'),
           'b3': -0.0157340*_u('permille^-1')}
)

# coefficients from Bullister et al. 2002 solubility formula for SF6
SF6_BULLISTER_02_COEFFS = dict(
    SF6={'a1': -82.1639, 'a2': 120.152, 'a3': 30.6372, 'b1': 0.0293201*_u('permille^-1'), 'b2': -0.0351974*_u('permille^-1'), 'b3': 0.00740056*_u('permille^-1')}
)

# coefficients from Hamme and Emerson 2004 solubility formula for Ar, Ne and N2
ArNeN2_HAMMEEMERSON_04 = dict(
    N2={'A0': 6.42931, 'A1': 2.92704, 'A2': 4.32531, 'A3': 4.69149, 'B0': -7.44129e-3*_u('permille^-1'), 'B1': -8.02566e-3*_u('permille^-1'), 'B2': -1.46775e-2*_u('permille^-1')},
    # these next two are not used, Jenkins 2019 is more up-to-date
    Ne={'A0': 2.18156, 'A1': 1.29108, 'A2': 2.12504, 'A3': 0, 'B0': -5.94737e-3*_u('permille^-1'), 'B1': -5.13896e-3*_u('permille^-1'), 'B2':0*_u('permille^-1')},
    Ar={'A0': 2.79150, 'A1': 3.17609, 'A2': 4.13116, 'A3': 4.90379, 'B0': -6.96233e-3*_u('permille^-1'), 'B1': -7.66670e-3*_u('permille^-1'), 'B2': -1.16888e-2*_u('permille^-1')}
)

# ice fractionation coefficients for dissolved gases undergoing freezing from seawater to
# sea ice. NGs are from Loose et al. 2023. For salt, 0.3 was assumed according to
# Loose 2016. Others assumed to be 0 for now.
# TODO update these after review of the literature
ICE_FRACTIONATION_COEFFS = dict(He=1.33, Ne=0.83, Ar=0.49, Kr=0.4, Xe=0.5, SF6=0, CFC11=0, CFC12=0, S=0.3)
