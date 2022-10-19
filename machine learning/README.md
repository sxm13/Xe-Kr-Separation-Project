# For physical features-estimated  method:     

## By pore volume: 
$$ M=PV*ρ_l $$                     
##### :m: PV is the Helium pore volume. ${ρ_l}$ is the liquid density of adsorbate. We calculated PV by Zeo++ using He (radius=1.32 Å) (set number of MC samples per atom is 5000) as the probe molecule.
## By accessible surface area:                  
$$ S=Σ*N_m $$                                          
##### :m: ${N_m}$ is the SL of the monolayer. Σ is the area occupied by per mol of adsorbed molecules if are spread into a monolayer, which can be calculated as follows,
$$ Σ=N_A*ω_m $$          
##### :m: ${N_A}$ is Avogadro constant (6.0221*10 $^{23}$ ). ${ω_m}$ is the area occupied by per adsorbate molecule. The molecules of adsorption are arranged in a hexagonal dense stacking pattern has been demonstrated $^{1}$, so that
$$ ω_m={3^{1\over2}\over2^{2\over3}}*({M\overρ*N_A})^{2\over3} $$        
##### :m: M is the relative atomic mass and ρ is the adsorbate density. We calculated ASA by Zeo++ using Xe (radius=1.96 Å, S_Xe) and Kr (radius=1.845 Å, S_Kr) as the probe molecule (set number of MC samples per atom is 5000). Then we calculated ω_m of Xe and Kr and obtained ∑ of Xe and Kr. Finally, we got SL (i.e., N_m) by S divided by Σ.
##### :m: Among them, Xe and Kr have relative atomic masses of 131.3 and 83.8. The liquid densities of Xe and Kr are 3.520 g/cm3 and 2.413 g/cm3. 
