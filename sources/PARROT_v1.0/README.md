<br />
<div align="center">
  <a href="https://github.com/PARROT-reports/PARROT-v0">
    <img src="images/parrot.svg" alt="Logo">
  </a>

<h3 align="center">PARROT v1.0</h3>

  <p align="center">
    Polyglot Annotated Radiological Reports for Open Testing
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

PARROT is an collaborative initiative to create a multilingual open dataset of radiological reports on which to test LLMs. 
The aim of PARROT is to represent the diversity of languages and reporting styles to promote applicability of LLM-related research in non-English clinical settings. 
PARROT is not-for-profit and does not recieve any funding at the moment.

<!-- CONTEXT -->
## Context
<details>
<summary>Read the context</summary>  

  ### Context  
Large language models (LLMs) have shown promising capabilities for structuring, simplifying and correcting radiological reports (1–3). However, the lack of open datasets in languages other than English restricts research to using data that cannot be shared to comply with privacy policies (4). This shortcoming makes the external validation of those emerging technologies challenging, hindering their diffusion and application in non-English speaking countries (5). A multilingual, open archive of radiological reports annotated by experts could circumvent this issue, by allowing researchers to test models on clinically pertinent tasks in various languages. Here, we present the Polyglot Annotated Radiological Reports for Open Testing (PARROT) project, intended to enhance the representation of the diversity of radiological reports across centers and languages, offering researchers a different perspective for testing LLMs on medical data.

PARROT is intended as a collaborative dataset:  
Facilitating the access to realistic medical texts for the community  
Addressing the representation of non-English medical data for testing LLMs  
Assessing the ability of LLMs to generalize across diverse languages in clinical tasks
    
### 1. Why an open multilingual dataset?

Limitations of the MIMIC dataset: The exclusively English datasets on which LLMs are currently tested in radiology, such as the mono-centric MIMIC, do not capture the diversity of radiological reports across centers and languages, and thus may hinder the applicability of those results in non-English speaking countries (6). Models are already trained on the MIMIC database, raising the issue of training and testing the LLMs ability on the same dataset (7). 
Lack of multilingual alternatives: Because of the private nature of radiological reports, there exists currently no available dataset of radiological reports beyond English. An alternative could be to translate the reports from the MIMIC database in other language, but they would fail to convey the true diversity of pathologies, examinations and reporting styles across countries.
Rising need for diversity in benchmarks: The development of open-source lightweight models alleviates the financial barrier to accessing this technology, but makes the importance of diverse corpora on which to test them even more dire (8).
Need for benchmarking LLMs on clinically pertinent tasks: Datasets are often crawled from websites and left un-annotated, hindering the complexity and diversity of tasks on which to test models. As a consequence, LLMs are currently benchmarked on tasks that do not represent their actual usefulness in clinical settings (7).

### 2. What is PARROT?

PARROT is an annotated open dataset of fictional reports written by radiologists in their native language. To circumvent privacy issues, the reports are completely fictional and as such can be shared without limitation. Because they are written by experts in their native language, they are expected to capture authentically the diversity of reporting styles and cultural specificity. The reports are annotated for five different tasks (translation, structuration, measurement extraction, correction of errors, ICD-10 code assignment), and centralized in an open archive. PARROT is intended as a test dataset for LLMs, and should not be used for training.

### 3. How to participate?

Radiologists from diverse languages, backgrounds and seniority can create fictional reports for exam modalities of their choice. The reports should be written as .txt, .rtf or .docx files. The authors must to translate the reports to English and complete the .csv with annotations. No background in informatics, AI or LLM is needed. Students are encouraged to participate if they had some experience with radiology, e.g. through an internship. 

### 4. Potential challenges

Engagement: reaching out to a variety of radiologists will be a critical challenge for PARROT in order to achieve a critical mass of reports in various languages. As such, participants are welcomed to invite colleagues to join the initiative.
Scalability and maintenance: if PARROT is a success, the amount of time required to curate the database will become critical. As such, for step 2 of the project, financial support from institutions could become important, and tasks such as verifying reports, annotating them, and creating new tasks, could be crowd-sourced. At this stage of the project, we will actively seek for funding opportunities by national or international institutions (e.g., European Union, national research foundations) or industry partners. 
Broadening the scope: multilingual medical databases are rare and radiology reports do not encompass the entirety of contexts in which a LLM can be assessed in medicine. As such, physicians from other specialties will be welcomed to join the initiative in step 2 of the project.


1. 	Adams LC, Truhn D, Busch F, et al. Leveraging GPT-4 for Post Hoc Transformation of Free-Text Radiology Reports into Structured Reporting: A Multilingual Feasibility Study. Radiology. 2023;230725. doi: 10.1148/radiol.230725.
2. 	Amin KS, Davis MA, Doshi R, Haims AH, Khosla P, Forman HP. Accuracy of ChatGPT, Google Bard, and Microsoft Bing for Simplifying                     Radiology Reports. Radiology. Radiological Society of North America; 2023;309(2):e232561. doi: 10.1148/radiol.232561.
3. 	Gertz RJ, Dratsch T, Bunck AC, et al. Potential of GPT-4 for Detecting Errors in Radiology Reports:                     Implications for Reporting Accuracy. Radiology. Radiological Society of North America; 2024;311(1):e232714. doi: 10.1148/radiol.232714.
4. 	Bressem KK, Papaioannou J-M, Grundmann P, et al. medBERT.de: A comprehensive German BERT model for the medical domain. Expert Systems with Applications. 2024;237:121598. doi: 10.1016/j.eswa.2023.121598.
5. 	Chang Y, Wang X, Wang J, et al. A Survey on Evaluation of Large Language Models. arXiv; 2023. http://arxiv.org/abs/2307.03109. Accessed May 4, 2024.
6. 	Yang Z, Mitra A, Kwon S, Yu H. ClinicalMamba: A Generative Clinical Language Model on Longitudinal Clinical Notes. arXiv; 2024. doi: 10.48550/arXiv.2403.05795.
7. 	Wornow M, Xu Y, Thapa R, et al. The shaky foundations of large language models and foundation models for electronic health records. npj Digit Med. Nature Publishing Group; 2023;6(1):1–10. doi: 10.1038/s41746-023-00879-8.
8. 	Making LLMs even more accessible with bitsandbytes, 4-bit quantization and QLoRA. . https://huggingface.co/blog/4bit-transformers-bitsandbytes. Accessed May 4, 2024.
</details>

<!-- DATASET -->
## The PARROT dataset

As of v1.0 (may 2025), PARROT consists of:
- 2,658 reports
- in 14 languages
- from 76 authors
- from 21 countries

## jsonl structure

PARROT v1.0 is released as a single .jsonl file (5.9MB), with the following structure:
```
data/
 └── PARROT_v1_0.jsonl              # one JSON per line
       ├─ no               : int   # report number
       ├─ language         : str   # report language
       ├─ modality         : str   # exam modality (CT, MRI, X-ray, etc)
       ├─ area             : str   # anatomical region (head, abdomen, chest, etc)
       ├─ report           : str   # original report
       ├─ translation      : str   # English translation
       ├─ report           : str   # original report
       ├─ icd              : str   # ICD-10 codes associated with the report
       ├─ contributor_code : str   # name of the author
       ├─ country          : str   # country of origin
       └─ subspecialty     : str   # two-letter code of the corresponding radiology subspecialties (NR: neuroradiology, GU: genito-urinary, etc)
```
## Use cases

PARROT is intended for testing, sharing ideas on use-cases of LLMs in radiology and medicine, and external validation of NLP approaches. Some use-cases are suggested in the `examples` section:
```
examples/
└── similar_reports.py           # for finding the most similar reports based on their embeddings with free-text queries
└── reports_vizualisation.py     # for creating an interactive maps of reports based on their embeddings
└── simplify_reports_ollama.py   # for simplifying reports with either a priavacy preserving model...
└── simplify_reports_openai.py   # ...or a cloud-based model
```

<!-- CONTRIBUTORS -->
## Contributors
<details>
<summary>PARROT exists thanks to the active submissions of 76 authors.</summary>
Kokou Adambounou, Campus University Hospital Centre, Department of Radiology and Medical Imaging, Lome, Togo
Lisa Adams, Department of Diagnostic and Interventional Radiology, Klinikum rechts der Isar, TUM University Hospital, Technical University of Munich, Munich, Germany
Thibault Agripnidis, Interventional Radiology Section, Department of Medical Imaging, University Hospital Timone, AP-HM, 264 Rue Saint-Pierre, 13005, Marseille, France
Sung Soo Ahn, Department of Radiology and Research Institute of Radiological Science and Center for Clinical Imaging Data Science,Yonsei University College of Medicine, Seoul, South Korea
Radhia Ait Chalal, Department of Radiology, Bab El-Oued University Hospital, Algiers. Algeria
Tugba Akinci D'Antonoli, 1. Department of Diagnostic and Interventional Neuroradiology, University Hospital Basel, 2. Department of Pediatric Radiology, University Children’s Hospital Basel
Philippe Amouyel, 1. U1167 RID-AGE, Pasteur Institute of Lille, Inserm, Lille University, Lille, France, 2. Public Health – Epidemiology Department, Lille University Hospital Center, Lille, France
Henrik Andersson, Department of Medical Imaging and Physiology, Skåne University Hospital, 221 85, Lund, Sweden
Raphaël Bentegeac, 1. U1167 RID-AGE, Pasteur Institute of Lille, Inserm, Lille University, Lille, France, 2. Public Health – Epidemiology Department, Lille University Hospital Center, Lille, France
Claudio Benzoni, Institute of AI and Informatics in Medicine (AIIM), TUM University Hospital, Technical University of Munich, Munich, Germany
Antonino Andrea Blandino, Section of Radiology, Department of Biomedicine, Neuroscience and Advanced Diagnostics (BiND), University of Palermo, Via del Vespro 129, Palermo 90127, Italy
Felix Busch, School of Medicine and Health, Department of Diagnostic and Interventional Radiology, Klinikum rechts der Isar, TUM University Hospital, Technical University of Munich, Munich, Germany
Elif Can,  Department of Diagnostic and Interventional Radiology, Medical Center – University of Freiburg, Faculty of Medicine, University of Freiburg, Germany
Riccardo Cau, Department of Radiology, University of Cagliari, Cagliari, Italy
Armando Ugo Cavallo, Division of Radiology, Istituto Dermopatico dell’Immacolata (IDI) IRCCS, Rome, Italy
Christelle Chavihot, Department of Radiology, Hôpital Instruction des Armées, Libreville, Gabon
Erwin Chiquete, Department of Neurology, Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán, Mexico City, Mexico
Renato Cuocolo, Department of Medicine, Surgery and Dentistry, University of Salerno, Baronissi, Italy
Eugen Divjak, Department of Diagnostic and Interventional Radiology, University Hospital Dubrava, Avenija Gojka Suska 6, 10000 Zagreb, Croatia
Barbara Dziadkowiec-Macek, Department of Physiology and Pathophysiology, Wroclaw Medical University, Wroclaw, Poland
Armel Elogne, Department of Radiology, Hôpital militaire d’Abidjan, 28 BP 1303, Abidjan, Côte d’Ivoire
Salvatore Claudio Fanni, Department of Translational Research, Academic Radiology, University of Pisa, Pisa, Italy
Carlos Ferrarotti, Department of Diagnostic Imaging, Center for Medical Education and Clinical Research “Norberto Quirno” (CEMIC), Autonomous City of Buenos Aires, Argentina
Claudia Fossataro, Department of Ophthalmology, Catholic University "Sacro Cuore", Rome, Italy
Federica Fossataro, Department of Ophthalmology, ASST Fatebenefratelli Sacco, Milan, Italy
Ali Fuat Tekin, Department of Radiology, Basaksehir Cam & Sakura City Hospital, Istanbul 34480, Turkey
Michał Fułek, Department and Clinic of Diabetology, Hypertension and Internal Diseases, Institute of Internal Diseases, Wroclaw Medical University, Wroclaw, Poland
Katarzyna Fułek, Department and Clinic of Otolaryngology, Head and Neck Surgery, Wroclaw Medical University, 50-556 Wroclaw, Poland
Paweł Gać, Department of Radiology and Diagnostic Imaging, 4th Military Hospital, Wroclaw, Poland
Martyna Gachowska, Department and Clinic of Otolaryngology, Head and Neck Surgery, Wroclaw Medical University, 50-556 Wroclaw, Poland
Ignacio García-Juárez, Department of Gastroenterology, Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán, México DF, México
Marco Gatti, Department of Surgical Sciences, Radiology Unit, University of Turin, Turin, Italy
Natalia Gorelik, Department of Radiology, McGill University Health Center, Montreal, Quebec, Canada
Alexia Maria Goulianou, Department of Medical Imaging, University Hospital of Heraklion, 71110, Crete, Voutes, Greece
Feno Hasina Rabemanorintsoa, Department of Radiology, Morafeno Toamasina University Hospital, Toamasina, Madagascar
Aghiles Hamroun, 1. U1167 RID-AGE, Pasteur Institute of Lille, Inserm, Lille University, Lille, France, 2. Public Health – Epidemiology Department, Lille University Hospital Center, Lille, France
Nicolas Herinirina, Department of Radiology, Tanambao University Hospital, Antsiranana, Madagascar
Quentin Holay, Department of Radiology, Sainte-Anne Teaching military Hospital, Toulon, France
Gordana Ivanac, Department of Diagnostic and Interventional Radiology, University Hospital Dubrava, Avenija Gojka Suska 6, 10000 Zagreb, Croatia
Felipe Kitamura, Bunkerhill Health, San Francisco, CA; Department of Diagnostic Imaging, Universidade Federal de São Paulo (UNIFESP), São Paulo, Brazil
Michail E. Klontzas, Artificial Intelligence and Translational Imaging (ATI) Lab, Department of Radiology, School of Medicine, University of Crete, Heraklion, Greece
Anna Kompanowska, Department of Pediatrics, Klodzko County Hospital, Klodzko, Poland
Rafał Kompanowski, Orthopedics and Traumatology Department of the Musculoskeletal System, Specialist Medical Centre, Polanica-Zdroj, Poland
Krzysztof Kraik, Faculty of medicine, Wroclaw Medical University, Wroclaw, Poland
Dominik Krupka, Faculty of medicine, Wroclaw Medical University, Wroclaw, Poland
Grégory Kuchcinski, Department of Neuroradiology, Lille University Hospital, Salengro Hospital, Lille, France
Bastien Le Guellec, Department of Neuroradiology, Lille University Hospital, Salengro Hospital, Lille, France
Alexandre Lefèvre, Department of Radiology, Lille University Hospital, 59000 Lille, France
Tristan Lemke, Institute of Diagnostic and Interventional Radiology, Technical University of Munich, School of Medicine, Munich, Germany
Maximilian Lindholz, Department of Radiology, Charité University Hospital Berlin, Berlin, Germany
Piotr Macek, Department and Clinic of Diabetology, Hypertension and Internal Diseases, Institute of Internal Diseases, Wroclaw Medical University, Wroclaw, Poland
Marcus Makowski, Department of Diagnostic and Interventional Radiology, Technical University of Munich, Munich, Germany
Luigi Mannacio, Department of Advanced Biomedical Sciences, University of Naples Federico II, Naples, Italy
Aymen Meddeb, Department of Neuroradiology, Charité University Hospital Berlin, Berlin, Germany
Lukas Müller, Department of Diagnostic and Interventional Radiology, University Medical Center of the, Johannes Gutenberg-University Mainz , Langenbeckst. 1, 55131, Mainz, Germany
Antonio Natale, Department of Radiological and Hematological Sciences, Section of Radiology, Università Cattolica del Sacro Cuore, L.go Francesco Vito 1, 00168, Rome, Italy
Béatrice Nguema Edzang, Department of Radiology, Hôpital Instruction des Armées, Libreville, Gabon
Adriana Ojeda, Departamento de Neuroradiología,DMO,Rosario,Argentina
Yae Won Park, Department of Radiology and Research Institute of Radiological Science and Center for Clinical Imaging Data Science,Yonsei University College of Medicine, Seoul, South Korea
Federica Piccione, Department of Surgical Sciences, Radiology Unit, University of Turin, Turin, Italy
Andrea Ponsiglione, Department of Advanced Biomedical Sciences, University of Naples Federico II, Naples, Italy
Małgorzata Poręba, Department of Paralympic Sport Wroclaw University of Health and Sport Sciences, Wroclaw, Poland
Rafał Poręba, Department of Radiology and Diagnostic Imaging, 4th Military Hospital, Wroclaw, Poland
Philipp Prucker, Department of Diagnostic and Interventional Radiology, Technical University of Munich, School of Medicine and Health, Klinikum rechts der Isar, TUM University Hospital, Munich, Germany
Jean-Pierre Pruvo, Department of Neuroradiology, Lille University Hospital, Salengro Hospital, Lille, France
Alba Pugliesi, Division of Health Care Sciences Center for Clinical Research and Management Education Dresden, Dresden International University, Dresden, Germany
Vasileios Rafailidis, Department of Radiology, Aristotle University of Thessaloniki, School of Medicine, AHEPA University General Hospital, Thessaloniki, Greece
Katarzyna Resler, Department and Clinic of Otolaryngology, Head and Neck Surgery, Wroclaw Medical University, 50-556 Wroclaw, Poland
Jan Rotkegel, Faculty of medicine, Wroclaw Medical University, Wroclaw, Poland
Luca Saba, Department of Radiology, Azienda Ospedaliero Universitaria (A.O.U.), di Cagliari - Polo di Monserrato s.s. 554 Monserrato, Cagliari, Italy
Ezann Siebert, Department of Ophthalmology, Sir Charles Gairdner Hospital, Perth, Western Australia, Australia
Arnaldo Stanzione, Department of Advanced Biomedical Sciences, University of Naples Federico II, Naples, Italy
Liz Toapanta-Yanchapaxi, Department of Neurology, Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán, Mexico City, Mexico.
Matthaios Triantafyllou, Department of Medical Imaging, University Hospital of Heraklion, 71110, Crete, Voutes, Greece
Ekaterini Tsaoulia, Department of Radiology, Aristotle University of Thessaloniki, School of Medicine, AHEPA University General Hospital, Thessaloniki, Greece
Szymon Urban, Department of Cardiology, The Copper Health Center, Lubin, Poland
Evangelia Vassalou, Department of Radiology, University Hospital of Heraklion, Greece
Federica Vernuccio, Section of Radiology, Department of Biomedicine, Neuroscience and Advanced Diagnosis (Bi.N.D), University of Palermo, Palermo, 90127, Italy
Weilang Wang, Department of Radiology, Zhongda Hospital, Southeast University, 87 Ding Jiaqiao,Nanjing, P.R.China 210009
Johan Wassélius, Department of Medical Imaging and Physiology, Skåne University Hospital, 221 85, Lund, Sweden
Szymon Włodarczak, Department of Cardiology, The Copper Health Center, Lubin, Poland
Adrian Włodarczak, Department of Cardiology, The Copper Health Center, Lubin, Poland
Andrzej Wysocki, Department of Radiology and Diagnostic Imaging, 4th Military Hospital, Wroclaw, Poland
Lina Xu, Department of Radiology, Charité – Universitätsmedizin Berlin, Corporate Member of Freie Universität Berlin and Humboldt Universität zu Berlin, Berlin, Germany
Tomasz Zatoński, Department and Clinic of Otolaryngology, Head and Neck Surgery, Wroclaw Medical University, 50-556 Wroclaw, Poland
Shuhang Zhang, Department of Radiology, Zhongda Hospital, Southeast University, 87 Ding Jiaqiao,Nanjing, P.R.China 210009
Sebastian Ziegelmayer, Department of Diagnostic and Interventional Radiology, Klinikum rechts der Isar, TUM University Hospital, Technical University of Munich, Munich, Germany
</details>

<!-- FAQ -->
## FAQ

### I am a radiologist, can I contribute to PARROT?

We would be pleased to include your reports in the next iterations of PARROT. Please contact contributeparrot@gmail.com or create a pull request to move forward.

### What will my reports become?

If you accept the data sharing agreement you will recieve by email, the reports will be shared publicly as part of PARROT database. Your reports will remain free for everyone to use, under CC BY-NC-SA 4.0 license.

### What do I get in return?

As soon as you submit 20 reports with valid translation and ICD codes, or 40 reports with translations without ICD codes, or 40 ICD codes for reports without codes, or any association, you will be invited to join the PARROT Consortium of Authors of the dataset.

### I have an interesting idea for a clinical task to test on PARROT, how can I contribute?

Great! PARROT is open-source, so you can start to annotate the dataset yourself, and engage other people to do so, either on the Discord server or via social media or by contacting contributeparrot@gmail.com

<!-- LICENSE -->
## License

PARROT is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/ 
This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format for noncommercial purposes only, and only so long as attribution is given to the creator. If you remix, adapt, or build upon the material, you must license the modified material under identical terms.

<!-- CONTACT -->
## Contact

contributeparrot@gmail.com

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
PARROT is a not-for-profit project imagined by Bastien Le Guellec (Lille, France) and Keno Bressem (Munich, Germany), with the support of Grégory Kuchcinki (Lille, France).
At the moment, it recieves no institutional funding. 
If your are an institution wishing to contribute to the project, please send an email to contributeparrot@gmail.com
