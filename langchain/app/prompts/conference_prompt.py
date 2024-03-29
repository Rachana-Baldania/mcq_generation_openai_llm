from langchain.prompts import PromptTemplate


template = """Given the following abstracts presented at AACR 2023 conference, create a final answer with references ("SOURCES").
If you don't know the answer, just say that are Unable to find the answer. DON'T TRY TO MAKE UP AN ANSWER.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: tigit abstracts
=========
Content: Title: Preclinical pharmacology and safety studies of ZG005: an anti-PD-1\\/TIGIT bispecific mAb in a phase I clinical trial for advanced tumors\nSummary: The combination of ZG005 with chemotherapeutic-reagents, cisplatin and donafenib, enhanced their anti-tumor efficacies. PK\\/TK analyses indicate a prolonged ZG005 receptor occupancy over 80%, consistent with in vitro binding results that are attribute to the S228P mutation in the IgG4 hinge region to prevent Fab exchange and enhance stability. The IND application of ZG005 has been approved by both FDA and NMPA, and the molecule is currently in phase I clinical trials for advanced solid tumors at escalated dosing of 0.3~20 mg\\/kg, Q3W, via i.v. administration.\nPrimary Author: Bing Zhu1; Tongcheng Dai1; Ruifeng Liu1; Alfonso Suarez2; Tyler Liban2; Bin Zhang1; Margaret Karow2; Jackie Sheng2; Zelin Sheng1; Binhua Lv1\nLocation: Section 23; Poster Board #12\nAffiliation: 1Suzhou Zelgen Biopharmaceuticals Co., Ltd., Shanghai, China; 2Gensun Biopharma, Inc., Newbury Park, CA\nDate: 2023-04-19\nSession Title: PO.IM01.05. Immune Checkpoints\n
Source: 1498971
Content: Title: Emerging therapeutic strategies for KRAS-mutant NSCLC\nSummary: There is no abstract associated with this presentation.\nPrimary Author: Ferdinandos Skoulidis\nLocation: Valencia BC - Convention Center\nAffiliation: UT MD Anderson Cancer Center, Houston, TX\nDate: 2023-04-19\nSession Title: AOS03. Dharma Master Jiantai Advances in Lung Cancer Research Session: Advances in NSCLC - More Targets, More Drugs, and More Cell States to Consider\n
Source: 1428599
Content: Title: Heterogenous cellular responses to GITR and TIGIT immunotherapy in the human gastrointestinal tumor microenvironment\nSummary: TIGIT antagonist led to a wider reprogramming of the TME compared to the limited effects of GITR agonist. Our strategy identified mechanisms of action of immunotherapy and factors associated with response or resistance, which can aid in prioritization of targets and their clinical translation.\nPrimary Author: Anuja Sathe1; Carlos Ayala2; Xiangqi Bai1; Sue M. Grimes1; Andrew Shelton2; Byrne Lee2; Cindy Kin2; George Poultsides2; Hanlee P. Ji1\nLocation: Section 24; Poster Board #10\nAffiliation: 1Stanford University School of Medicine, Stanford, CA; 2Department of Surgery, Stanford University, Stanford, CA\nDate: 2023-04-18\nSession Title: PO.IM01.17. Determinants of Immunotherapeutic Effectiveness\n
Source: 1501730
=========
FINAL ANSWER: At the AACR 2023 conference, two abstracts were related to TIGIT. One abstract presented the preclinical pharmacology and safety studies of ZG005, an anti-PD-1/TIGIT bispecific antibody, in advanced tumors. The other abstract focused on heterogeneous cellular responses to TIGIT immunotherapy in the gastrointestinal tumor microenvironment.
SOURCES: [1498971, 1501730]

QUESTION: list natural language processing abstracts
=========
Content: Title: Selective targeting deacetylase 3 (HDAC3) and HDAC8 by PROTACs\nSummary: Based on this, we are further modifying the PROTACs to be selective for HDAC8. The HDAC3, HDAC8 selective degrader and HDAC3 and HDAC8 dual degrader we developed could be useful chemical probes to dissect the complex biological function of HDAC3 and HDAC8 and potential therapeutics for treating cancer.\nPrimary Author: Yufeng Xiao; Seth Hale; Nikee Awasthee; Xuan Zhang; Yi Liu; Zhiguang Huo; Dongwen Lyu; Lei Wang; Weizhou Zhang; Megan Mosteiro; Daiqing Liao; Guangrong Zheng\nLocation: Section 30; Poster Board #29\nAffiliation: University of Florida, Gainesville, FL\nDate: 2023-04-18\nSession Title: PO.CH01.05. High-throughput Screening, Lead Identification and Optimization, and in Silico Drug Discovery\n
Source: 1501073
Content: Title: Emerging therapeutic strategies for KRAS-mutant NSCLC\nSummary: There is no abstract associated with this presentation.\nPrimary Author: Ferdinandos Skoulidis\nLocation: Valencia BC - Convention Center\nDate: 2023-04-19\nprimary_product: None\nsecondary_product: None\n'
Source: 1928599
=========
FINAL ANSWER: Unable to find the answer.
SOURCES: []

QUESTION: {question}
=========
{summaries}

=========
FINAL ANSWER:"""

CONFERENCE_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
