The following repository was created in the context of a Master's thesis in Biomedical Engineering, at Instituto Superior Técnico (Lisboa, Portugal). The work itself was developed at the Technische Universität Berlin 
Zentrum für Astronomie und Astrophysik AG Astrobiologie, under the supervision of M.Sc. Max Riekeles. The thesis focused on studying the potential use of bacterial motility (and other optical parameters), in 2D and 3D 
microscopic images, as a novel biomonitoring approach for the detection of heavy metals and other contaminants in water. Therefore, multiple python script were implemented, most of which are provided in this repository. 

---

The detailed explanation regarding the scripts employed in the 2D processing of motility data (pre_processing.py and post_processing.py) is provided in the corresponding PDF file. 
The scripts involved in the processing of the 3D motility data (obtained with an off-axis Digital Holographic Microscope) are briefly described below: 

  (1) crop_holograms.py file - used for cropping the holograms, in an entire set of recordings (i.e., rec1, rec2,...), to a desired pixel size (default set to 1250 x 1250 pixels);
  (2) pre_processing_max_z.py file - employed for resizing and converting the max-z projections obtained from the reconstructed holograms (based on the equivalent function in the pre_processing.py script);
  (3) post_processing_max_z.py file - utilised for copying all of the MHIs obtained from the max-z projections (based on the equivalent function in the post_processing.py script).

---

The script developed for the calculation of the p-values and t-values (based on Welch's t-test) is also provided in this repository (p_t_value_tests.py). For non-parametric statistical tests, a script for the calculation 
of the p-values according to the Kruskal-Wallis H Test is provided.

---

All the scripts were developed with the help of AI.
