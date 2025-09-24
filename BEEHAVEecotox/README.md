
BEEHAVEecotox landscape extension - general information

The landscape extension of the BEEHAVEecotox model (Preuss et a. 2022) was developed in Netlogo 5.3.1, 
which can be downloaded for free: https://ccl.northwestern.edu/netlogo/5.3.1/

Once Netlogo is installed, the model file "BEEHAVE_ETOX_landscape.nlogo" can be opened and run.

For a general description of the BEEHAVE model and a manual see supplementary material in:
	Becher, M. A., Grimm, V., Thorbek, P., Horn, J., Kennedy, P. J., & Osborne, J. L. (2014). 
	BEEHAVE: a systems model of honeybee colony dynamics and foraging to explore multifactorial causes of colony failure. 
	Journal of Applied Ecology, 51(2), 470-482. 
	
	or at the BEEHAVE website: https://beehave-model.net/

The BEEHAVEetcotox model is published and described in detail in: 
	Preuss, T. G., Agatz, A., Goussen, B., Roeben, V., Rumkee, J., Zakharova, L., & Thorbek, P. (2022). 
	The BEEHAVEecotox Model—Integrating a Mechanistic Effect Module into the Honeybee Colony Model. 
	Environmental Toxicology and Chemistry, 41(11), 2870-2882.
	
Changes to the code made for this landscape extension version are described in "R2260099-1_ODD_Amendment_BEEHAVEecotox_lanscape_extension".

Instructions how to apply the new feature are given in "R2260099-2_Manual_BEEHAVEecotox_landscape_extension".

The model package comes with a selection of input files:
	A new substance input file, defining the properties of pesticides:
		- "SubstanceFile.txt": definition of 3 artificial pesticides
		
	Landscape input files in the old file format (365 lines for each food source defined):
		- "Input_2-1_FoodFlow.txt": simple landscape with 4 food sources
		- "Input_2-1_FoodFlow_RRes.txt": realistic landscape from Hertfordshire, UK, with 115 food sources
	
	Landscape input files in a new file format (single line for each food source defined):
		- "Sources_RedGreen.txt": 2 food sources & pesticide applications
		- "Sources_RedGreenBlueYellow.txt": 4 food sources & pesticide applications
		- "Sources_RRes.txt": like "Input_2-1_FoodFlow_RRes.txt" but in the new file format and with pesticide applications at all fields
		- "Sources_RRes_PPP-Blue.txt": like "Sources_RRes.txt", but with pesticide applications only at "blue" fields
		- "Sources_RRes_PPP-Red.txt": like "Sources_RRes.txt", but with pesticide applications only at "red" fields
		- "Sources_RRes_PPP-Yellow.txt": like "Sources_RRes.txt", but with pesticide applications only at "yellow" fields






## Terms of use of the software BEEHAVEecotox (2021)
BEEHAVEecotox (2021) is the implementation of an ecotoxicological module with the associated changes into the model BEEHAVE_BeeMapp2016, developed by Matthias Becher and colleagues (more information on this model is provided below).

This implementation is based on the software platform NetLogo (Wilensky 1999), and can be downloaded for free from https://github.com/BEEHAVE-Model/BEEHAVEecotox.

Please refer to the BEEHAVEecotox publication (Preuss et al., 2022) when using this version of the BEEHAVE model.

## Copyright and Licence Information for the software BEEHAVEecotox (2021):
Copyright 2021

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A copy of the GNU General Public License can be found at http://www.gnu.org/licenses/gpl.html or write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

## References
Becher, M. A., Grimm, V., Thorbek, P., Horn, J., Kennedy, P. J. & Osborne, J. L. (2014). BEEHAVE: a systems model of honeybee colony dynamics and foraging to explore multifactorial causes of colony failure. Journal of Applied Ecology, 51(2), 470-482.

Grimm, V., Berger, U., Bastiansen, F., Eliassen, S., Ginot, V., Giske, J., … & DeAngelis, D. L. (2006). A standard protocol for describing individual-based and agent-based models. Ecological modelling, 198(1-2), 115-126.

Grimm, V., Berger, U., DeAngelis, D. L., Polhill, J. G., Giske, J. & Railsback, S. F. (2010). The ODD protocol: a review and first update. Ecological modelling, 221(23), 2760-2768.

Grimm, V., Railsback, S. F., Vincenot, C. E., Berger, U., Gallagher, C., DeAngelis, D. L., … & Ayllón, D. (2020). The ODD protocol for describing agent-based and other simulation models: A second update to improve clarity, replication, and structural realism. Journal of Artificial Societies and Social Simulation, 23(2).

Preuss, T.G., Agatz, A., Goussen, B., Roeben, V., Rumkee, J., Zakharova, L. & Thorbek, P. (2022). The BEEHAVEecotox model - Integrating a mechanistic effect module into the honeybee colony model, Environmental Toxicology and Chemist, 41: 2870- 2882.

# Beehave_BeeMapp (2015)
## Terms of use of the software Beehave_BeeMapp (2015)
Beehave (2014) and Beehave_BeeMapp (2015) are implementations of the model BEEHAVE, developed by Matthias Becher and colleagues:

Becher, M.A., Grimm, V., Thorbek, P., Horn, J., Kennedy, P.J. & Osborne, J.L. (2014) BEEHAVE: A systems model of honeybee colony dynamics and foraging to explore multifactorial causes of colony failure. Journal of Applied Ecology.

This implementation is based on the software platform NetLogo (Wilensky 1999), and can be downloaded for free from http://beehave-model.net/.

## Copyright and Licence Information:
Copyright 2015 by Matthias Becher

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A copy of the GNU General Public License can be found at http://www.gnu.org/licenses/gpl.html or write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

## Recommendations when using BEEHAVE:
* Please refer to the BEEHAVE publication (Becher et al. 2014; see above) and the BEEHAVE website (http://beehave-model.net/) when using BEEHAVE.
* We recommend that any publication or report based on using BEEHAVE shall include, in the Supplementary Material, the very NetLogo file that was used to produce the corresponding figure, table, or other kinds of results, as well as the “Experiments” in the BehaviorSpace and all necessary input files (see Supplementary Material of Becher et al. 2013 as example).
* You might want to modify the NetLogo code implementing BEEHAVE, for example by adding further outputs, or running specific scenarios. To check whether you are still using the original version of BEEHAVE click the “Version Test” button, which runs the model under specific settings and defined random numbers and informs the user if the code was changed. Note that not all changes to the code can be detected by this test. If you changed the code, we recommend to document these changes in all detail and to provide a revised ODD model description in which the modified or added elements are highlighted.
















