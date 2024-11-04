# 🧪 PHCAL: pH Calculation 🤖
### Comprehensive Analysis of Acid-Base Equilibria Using MBE, CBE, and PBE

This package provides codes for the paper "Comprehensive Analysis of Acid-Base Equilibria Using MBE, CBE, and PBE". It includes tools to calculate pH values for various acid-base systems using Charge Balance Equation (CBE) and Proton Balance Equation (PBE) methods.

📄 Want to read the paper? [**Click here**](https://phcal.ericxin.eu/doc/doc.pdf)

🌐 Prefer the online version? [**Click here**](https://phcal.ericxin.eu)

## Usage Examples

### Example 1: Calculation of 0.01 M HCl

**Charge Balance Equation (CBE) Calculation**

```python
from phcal import *

HCl = CBE_Inert(charge=-1, conc=0.01)
pH = CBE_calc(HCl)
pH.pH_calc()

print(pH.pH)
```

**Proton Balance Equation (PBE) Calculation**

```python
from phcal import PBE_Inert
HCl = PBE_Inert(conc=0.01, proton=1, proton_ref=1)
# HCl = PBE_Acid(conc=0.01, Ka=100000, proton=1, proton_ref=1)
calc = PBE_calc(HCl)
calc.pH_calc()
print(calc.pH)
```

### Example 2: Calculation of 0.01 M (NH4)2(HPO4)

**Charge Balance Equation (CBE) Calculation**
```python
from phcal import PBE_Acid, PBE_calc
NH4 = Acid(charge=1, conc=0.01*3, pKa=9.25)
pKa = [1.97, 6.82, 12.5]
P = Acid(charge=0, conc=0.01, pKa=pKa)

pH = CBE_calc(NH4, P)
pH.pH_calc()

print(pH.pH)
```

**Proton Balance Equation (PBE) Calculation**
```python
from phcal import PBE_Acid, PBE_calc

NH4 = PBE_Acid(conc=0.01 * 3, pKa=9.25, proton=1, proton_ref=1)
pKa = [1.97, 6.82, 12.5]
P = PBE_Acid(conc=0.01, pKa=pKa, proton=3, proton_ref=0)
calc = PBE_calc(NH4, P)
calc.pH_calc()

print(calc.pH)
```

## Contact

If you have any questions or suggestions, please feel free to contact me at [me@ericxin.eu](mailto:me@ericxin.eu).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.