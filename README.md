# Healthcare Risk Assessment System
## HIV Acquisition & Mental Health Risk Scoring

---

##  Assessment Completion Summary

**Candidate:** Healthcare AI Developer  
**Date:** November 24, 2025  
**Time Spent:** ~3.5 hours

### Time Breakdown:
- Data exploration and understanding: 30 minutes
- Research on SA NDOH guidelines: 45 minutes
- Algorithm development and implementation: 90 minutes
- Testing and refinement: 45 minutes
- Documentation and presentation: 30 minutes

---

## Deliverables

This submission includes:

1. **Python Script**: `healthcare_risk_assessment.py`
   - Standalone executable script
   - Complete implementation of risk assessment system
   - Generates visualizations and reports

2. **Jupyter Notebook**: `healthcare_risk_assessment.ipynb`
   - Interactive presentation format
   - Step-by-step documentation
   - Includes explanations, code, and results
   - Ready for live presentation

3. **Analysis Results**: 
   - `risk_assessment_results.csv` - Risk scores for all 100 conversations
   - `risk_assessment_analysis.png` - Comprehensive visualizations
   - `notebook_visualizations.png` - Additional charts

4. **Documentation**: This README file

---

## System Overview

### Purpose
An automated risk assessment system that analyzes healthcare conversations to:
- Calculate HIV acquisition risk scores (0-100 scale)
- Assess mental health disorder risk (0-100 scale)
- Generate treatment recommendations based on South African NDOH guidelines
- Provide integrated care plans for comorbid conditions

### Clinical Guidelines Used
- **SA NDOH HIV Testing Services Policy (2016)**
- **SA NDOH Mental Health Policy Framework (2023-2030)**
- **Primary Care 101 (PC101) Guidelines**
- **Mental Health Care Act 17 of 2002**
- **SA National Strategic Plan for HIV, STIs and TB**

---

## Results Summary

### Dataset Analysis (100 Conversations)

**HIV Risk Distribution:**
- LOW: 100 conversations (100%)
- MEDIUM: 0 conversations (0%)
- HIGH: 0 conversations (0%)

**Mental Health Risk Distribution:**
- MINIMAL: 100 conversations (100%)
- MILD: 0 conversations (0%)
- MODERATE: 0 conversations (0%)
- SEVERE: 0 conversations (0%)

**Mean Risk Scores:**
- HIV Risk Score: 7.61 ± 2.71
- Mental Health Score: 3.00 ± 0.00

### Interpretation
The provided dataset consists of generic, synthetic conversations with minimal specific risk indicators. To demonstrate the system's full capability, the notebook includes demonstration cases with HIGH and SEVERE risk scenarios showing:
- Proper risk stratification
- Appropriate urgency determination
- Evidence-based treatment recommendations
- Integrated care planning

---

## Algorithm Methodology

### HIV Risk Assessment

**Risk Indicators (SA NDOH HTS Policy 2016):**

**HIGH RISK (3x weight):**
- Unprotected sexual contact
- Partner HIV status concerns
- Recent exposure events
- STI symptoms (discharge, ulcers, pain)
- Pregnancy/breastfeeding status

**MEDIUM RISK (2x weight):**
- Testing history gaps
- Partner concerns
- HIV-related symptoms (fever, night sweats, weight loss)
- High-risk behaviors (injection drug use)

**LOW RISK (1x weight):**
- General health concerns
- Prevention information seeking
- Educational queries

**Risk Categories:**
- HIGH (≥60): Urgent testing within 24 hours, PEP/PrEP assessment
- MEDIUM (30-59): Testing within 1 week, counseling services
- LOW (<30): Routine testing, prevention education

### Mental Health Risk Assessment

**Assessment Framework (SA NDOH Mental Health Policy 2023-2030):**

**Depression Indicators (PHQ-9 based):**
- Depressed mood (sadness, hopelessness, worthlessness)
- Loss of interest/pleasure (anhedonia)
- Sleep disturbances (insomnia, hypersomnia)
- Appetite changes (weight loss/gain)
- Concentration difficulties

**Anxiety Indicators (GAD-7 based):**
- Excessive worry and fear
- Physical symptoms (palpitations, sweating, trembling)
- Avoidance behaviors
- Restlessness and tension

**Severe Symptoms (Priority flags):**
- Suicidal ideation/self-harm
- Psychotic symptoms
- Substance abuse

**Functional Impairment:**
- Work/school disruption
- Relationship problems
- Daily living difficulties

**Risk Categories:**
- SEVERE (≥70 or suicidal): Emergency psychiatric evaluation
- MODERATE (45-69): 1-2 week assessment, therapy + medication
- MILD (20-44): Within 1 month, counseling and monitoring
- MINIMAL (<20): Routine wellness, prevention

---

##  Treatment Recommendations

### HIV Management Plans

**HIGH RISK:**
- Urgency: Within 24 hours
- HIV testing at nearest facility or self-test
- PEP assessment if exposure <72 hours
- Partner notification services
- STI screening
- PMTCT services if pregnant

**MEDIUM RISK:**
- Urgency: Within 1 week
- Scheduled HIV testing
- Pre-test counseling
- Risk reduction strategies
- PrEP eligibility assessment

**LOW RISK:**
- Urgency: Routine (within 1 month)
- Annual testing for sexually active adults
- Prevention education
- General health screening

### Mental Health Management Plans

**SEVERE:**
- Urgency: EMERGENCY - Immediate
- Psychiatric evaluation
- Suicide risk assessment
- Safety planning
- Pharmacotherapy: Fluoxetine 20mg (first-line SSRI)
- Intensive psychological intervention
- Consider hospitalization
- Crisis lines: SADAG 0800 567 567

**MODERATE:**
- Urgency: 1-2 weeks
- Comprehensive assessment (PHQ-9/GAD-7)
- Individual/group counseling (8-12 sessions)
- Antidepressant consideration
- Evidence-based therapy (CBT/IPT)
- Lay counselor services

**MILD:**
- Urgency: Within 1 month
- Screening and monitoring
- Psychoeducation
- Guided self-help
- Lifestyle modifications
- Problem-solving therapy

**MINIMAL:**
- Routine monitoring
- Mental health promotion
- Stress management
- Wellness strategies

### Integrated Care
The system recognizes the bidirectional relationship between HIV and mental health (SA NDOH Mental Health Policy), providing:
- Coordinated care plans for comorbidities
- Community health worker involvement
- Support group referrals
- Holistic treatment approach

---

## 📞 Key Contact Information

**National Resources:**
- National AIDS Helpline: **0800 012 322**
- Mental Health Information Line: **0800 567 567**
- SADAG Crisis Line: **011 262 6396**
- Suicide Crisis Line: **0800 567 567**

---

## How to Use

### Running the Python Script:
```bash
python healthcare_risk_assessment.py
```

This will:
1. Load the conversation data
2. Analyze all conversations
3. Generate risk scores and recommendations
4. Create visualizations
5. Save results to CSV
6. Display summary statistics and detailed reports

### Using the Jupyter Notebook:
```bash
jupyter notebook healthcare_risk_assessment.ipynb
```

The notebook provides:
- Interactive analysis
- Step-by-step explanations
- Visual results
- Demonstration cases
- Ready for presentation

---

## Visualizations Generated

1. **HIV Risk Category Distribution** - Bar chart showing risk stratification
2. **Mental Health Risk Distribution** - Distribution across severity levels
3. **Risk Score Distribution** - Histogram of continuous scores
4. **Risk Factor Correlations** - Heatmap of indicator relationships
5. **HIV vs Mental Health Scatter** - Showing integrated care needs
6. **Total Indicators Found** - Bar chart of detected risk factors

---

##  System Strengths

1. **Evidence-Based**: Grounded in SA NDOH clinical guidelines
2. **Multi-Dimensional**: Assesses both HIV and mental health risks
3. **Actionable**: Provides specific, implementable recommendations
4. **Integrated**: Addresses comorbidity comprehensively
5. **Scalable**: Can process large volumes of conversations
6. **Transparent**: Clear scoring methodology and reasoning

---

##  Limitations and Future Enhancements

### Current Limitations:
1. **Keyword-based approach**: Relies on lexical matching rather than deep semantic understanding
2. **Synthetic data**: Current dataset lacks diversity in risk indicators
3. **Clinical validation**: Requires validation with real patient data and clinician assessment

### Proposed Enhancements:
1. **Machine Learning Integration:**
   - NLP transformers (BERT, ClinicalBERT)
   - Deep learning risk prediction models
   - Context-aware semantic analysis

2. **Clinical Validation:**
   - Sensitivity/specificity analysis
   - ROC curve optimization
   - Comparison with gold-standard assessments

3. **Additional Features:**
   - Temporal tracking (symptom progression over time)
   - Demographic risk factors (age, gender, socioeconomic status)
   - Treatment adherence monitoring
   - Outcome tracking

4. **System Integration:**
   - EMR/EHR integration
   - Automated referral system
   - SMS/WhatsApp bot deployment
   - Real-time alerting for high-risk cases

---

## Ethical and Privacy Considerations

### POPIA Compliance:
- Data minimization
- Secure storage and transmission
- Anonymization of patient information
- Consent management

### Clinical Oversight:
- System as **decision support**, not replacement for clinical judgment
- Human-in-the-loop for high-risk cases
- Regular audits and quality assurance
- Continuous feedback and improvement

### Equity and Access:
- Language localization (11 official languages)
- Low-literacy adaptations
- USSD/SMS options for feature phone users
- Community health worker training

---

##  Technical Stack

**Languages & Libraries:**
- Python 3.12
- github copilot
- pandas (data manipulation)
- numpy (numerical operations)
- matplotlib & seaborn (visualization)
- re (text processing)

**Development Environment:**
- Jupyter Notebook
- Python scripts for production deployment

---

## Demonstration of Capability

While the provided dataset shows uniformly low risk scores due to its generic nature, the system successfully demonstrates:

1.  **Comprehensive risk assessment framework**
2.  **Evidence-based scoring algorithms**
3.  **Integration with SA NDOH guidelines**
5.  **Treatment recommendation generation**
6.  **Integrated care planning**
7.  **Professional documentation**

The notebook includes **demonstration cases** showing:
- HIGH HIV risk with appropriate urgent recommendations
- SEVERE mental health crisis with emergency protocols
- Integrated care for comorbid conditions

---

## Files Structure

```
outputs/
├── healthcare_risk_assessment.py          # Standalone Python script
├── healthcare_risk_assessment.ipynb       # Interactive Jupyter notebook
├── risk_assessment_results.csv            # Analysis results (100 conversations)
├── risk_assessment_analysis.png           # Comprehensive visualizations
├── notebook_visualizations.png            # Additional charts
└── README.md                              # This documentation file
```

---

##  Key Learnings and Insights

1. **HIV-Mental Health Comorbidity**: Strong evidence for integrated care approach in SA NDOH guidelines
2. **Risk Stratification**: Essential for resource allocation in resource-limited settings
3. **Cultural Context**: SA guidelines emphasize community health workers and support groups
4. **Accessibility**: Multiple contact points (helplines, clinics, mobile services)
5. **Prevention Focus**: Guidelines prioritize prevention alongside treatment

---

## Creative Elements Added

Beyond basic requirements, this submission includes:

1. **Comprehensive Documentation**: Detailed methodology and clinical rationale
2. **Dual Format**: Both script and notebook for different use cases
3. **Demonstration Cases**: Shows full system capability
4. **Visual Analytics**: Multiple visualization perspectives
5. **Integrated Care Framework**: Goes beyond siloed assessment
6. **Actionable Outputs**: Specific, implementable recommendations
7. **Professional Presentation**: Ready for stakeholder review

---

## Acknowledgments

This system is built on the foundation of evidence-based clinical guidelines developed by:
- South African National Department of Health (NDOH)
- South African Depression and Anxiety Group (SADAG)
- World Health Organization (WHO)
- South African HIV Clinicians Society

---

## Contact and Feedback

For questions about this implementation or suggestions for enhancement, please provide feedback through the assessment review process.

---

**Thank you for reviewing this submission. I look forward to discussing the system in detail during the interview.**

---

*Developed as part of the Healthcare AI Assessment*  
*November 2025*
