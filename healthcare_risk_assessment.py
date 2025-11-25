

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 80)
print("HEALTHCARE RISK ASSESSMENT SYSTEM")
print("South African NDOH Guidelines Implementation")
print("=" * 80)
print()

# SECTION 1: DATA LOADING AND PREPROCESSING


def load_conversations(file_path):
    """
    Load and parse WhatsApp-style healthcare conversations
    
    Parameters:
    -----------
    file_path : str
        Path to the conversation file
        
    Returns:
    --------
    list : List of conversation dictionaries
    """
    print("Loading conversations...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by conversation delimiter
    conversations = content.split("========== Conversation ==========")
    
    parsed_conversations = []
    
    for idx, conv in enumerate(conversations):
        if not conv.strip():
            continue
            
        messages = []
        lines = conv.strip().split('\n')
        
        for line in lines:
            # Match WhatsApp format: [date, time] User/AI: message
            match = re.match(r'\[(.*?)\] (User|AI): (.*)', line)
            if match:
                timestamp, sender, message = match.groups()
                messages.append({
                    'timestamp': timestamp,
                    'sender': sender,
                    'message': message
                })
        
        if messages:
            parsed_conversations.append({
                'conversation_id': idx + 1,
                'messages': messages,
                'user_messages': [m['message'] for m in messages if m['sender'] == 'User'],
                'full_text': ' '.join([m['message'] for m in messages if m['sender'] == 'User'])
            })
    
    print(f"✓ Loaded {len(parsed_conversations)} conversations")
    print()
    return parsed_conversations


# SECTION 2: HIV RISK ASSESSMENT


class HIVRiskAssessor:
    """
    HIV Risk Assessment based on South African NDOH HIV Testing Services Policy
    
    Key Risk Factors (SA NDOH Guidelines):
    - Unprotected sexual contact
    - Multiple partners
    - Partner concerns
    - STI symptoms
    - Pregnancy/breastfeeding
    - TB symptoms
    - Previous exposure
    - High-risk behaviors
    """
    
    def __init__(self):
        # Risk indicators based on SA NDOH HTS guidelines
        self.risk_keywords = {
            'high': {
                'unprotected': ['unprotected', 'no condom', 'without protection', 'unsafe sex'],
                'partner_risk': ['partner hiv', 'partner positive', 'partner infected', 
                               'multiple partners', 'new partner'],
                'exposure': ['exposure', 'exposed to', 'came in contact', 'needlestick'],
                'sti_symptoms': ['discharge', 'sores', 'genital pain', 'burning urination',
                               'genital ulcer', 'painful urination'],
                'pregnancy': ['pregnant', 'pregnancy', 'breastfeeding', 'antenatal']
            },
            'medium': {
                'testing': ['never tested', 'long time since test', 'should i test',
                          'need test', 'get tested'],
                'partner_concern': ['partner', 'worried about partner', 'concerned about partner',
                                  'should i tell partner'],
                'symptoms': ['fever', 'night sweats', 'weight loss', 'swollen glands',
                           'persistent cough', 'diarrhea', 'rash'],
                'behavioral': ['sex worker', 'inject drugs', 'sharing needles']
            },
            'low': {
                'general_health': ['feeling sick', 'not well', 'worried', 'stressed'],
                'prevention': ['how to prevent', 'stay safe', 'protect myself'],
                'information': ['what is hiv', 'how does', 'can i get']
            }
        }
        
        self.risk_weights = {
            'high': 3.0,
            'medium': 2.0,
            'low': 1.0
        }
    
    def calculate_risk_score(self, conversation_text):
        """
        Calculate HIV acquisition risk score (0-100)
        
        Parameters:
        -----------
        conversation_text : str
            Full conversation text
            
        Returns:
        --------
        dict : Risk assessment results
        """
        text_lower = conversation_text.lower()
        
        risk_factors = []
        total_score = 0
        max_possible_score = 0
        
        for risk_level, categories in self.risk_keywords.items():
            weight = self.risk_weights[risk_level]
            
            for category, keywords in categories.items():
                found_keywords = []
                for keyword in keywords:
                    if keyword in text_lower:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    category_score = weight * len(found_keywords)
                    total_score += category_score
                    risk_factors.append({
                        'category': category,
                        'risk_level': risk_level,
                        'keywords_found': found_keywords,
                        'score': category_score
                    })
                
                max_possible_score += weight * len(keywords)
        
        # Normalize to 0-100 scale
        if max_possible_score > 0:
            normalized_score = min(100, (total_score / max_possible_score) * 100)
        else:
            normalized_score = 0
        
        # Adjust score based on urgency indicators
        urgency_keywords = ['urgent', 'emergency', 'severe', 'very worried', 'scared']
        urgency_count = sum(1 for word in urgency_keywords if word in text_lower)
        normalized_score += urgency_count * 5
        normalized_score = min(100, normalized_score)
        
        return {
            'risk_score': round(normalized_score, 2),
            'risk_category': self._categorize_risk(normalized_score),
            'risk_factors': risk_factors,
            'total_indicators': len(risk_factors)
        }
    
    def _categorize_risk(self, score):
        """Categorize risk level based on score"""
        if score >= 60:
            return 'HIGH'
        elif score >= 30:
            return 'MEDIUM'
        else:
            return 'LOW'


# SECTION 3: MENTAL HEALTH RISK ASSESSMENT

class MentalHealthAssessor:
    """
    Mental Health Risk Assessment based on SA NDOH Mental Health Policy Framework
    
    Key Indicators (SA NDOH Guidelines):
    - Depression symptoms (PHQ-9 based)
    - Anxiety symptoms (GAD-7 based)
    - Stress indicators
    - Suicidal ideation
    - Substance use
    - Functional impairment
    """
    
    def __init__(self):
        # Based on SA NDOH Mental Health Policy Framework 2023-2030
        self.mental_health_indicators = {
            'depression': {
                'mood': ['sad', 'depressed', 'hopeless', 'worthless', 'empty',
                        'down', 'crying', 'tearful', 'no joy', 'no pleasure'],
                'interest': ['no interest', 'no motivation', 'dont care', 'nothing matters',
                           'lost interest', 'no energy'],
                'sleep': ['cant sleep', 'insomnia', 'sleep too much', 'oversleeping',
                         'waking up', 'nightmares'],
                'appetite': ['no appetite', 'not eating', 'lost weight', 'overeating',
                           'gained weight'],
                'concentration': ['cant focus', 'cant concentrate', 'memory problems',
                                'cant think', 'confused']
            },
            'anxiety': {
                'worry': ['worried', 'anxious', 'nervous', 'panic', 'fear',
                         'scared', 'frightened', 'terrified'],
                'physical': ['heart racing', 'sweating', 'trembling', 'shaking',
                           'chest pain', 'shortness of breath', 'dizzy'],
                'avoidance': ['avoiding', 'cant leave', 'stay home', 'hiding'],
                'restlessness': ['restless', 'on edge', 'tense', 'keyed up']
            },
            'severe_symptoms': {
                'suicidal': ['suicide', 'kill myself', 'end it', 'better off dead',
                           'want to die', 'self harm', 'hurt myself'],
                'psychotic': ['hearing voices', 'seeing things', 'paranoid',
                            'people watching', 'conspiracy'],
                'substance': ['drinking', 'alcohol', 'drugs', 'high', 'using']
            },
            'functional_impairment': {
                'work': ['cant work', 'lost job', 'fired', 'quit job', 'missing work'],
                'relationships': ['isolated', 'alone', 'no friends', 'family problems',
                                'relationship issues'],
                'daily_living': ['cant get up', 'stay in bed', 'dont shower',
                               'not taking care']
            },
            'stress': {
                'general': ['stressed', 'overwhelmed', 'pressure', 'burden',
                          'too much', 'cant cope'],
                'life_events': ['death', 'divorce', 'lost', 'trauma', 'abuse',
                              'violence', 'accident']
            }
        }
    
    def calculate_risk_score(self, conversation_text):
        """
        Calculate mental health risk score (0-100)
        
        Parameters:
        -----------
        conversation_text : str
            Full conversation text
            
        Returns:
        --------
        dict : Mental health assessment results
        """
        text_lower = conversation_text.lower()
        
        symptoms_found = defaultdict(list)
        severity_multiplier = 1.0
        
        # Check for severe symptoms (highest priority)
        severe_found = False
        for category, keywords in self.mental_health_indicators['severe_symptoms'].items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                symptoms_found[f'severe_{category}'].extend(found)
                severe_found = True
                severity_multiplier = 2.0
        
        # Check for depression symptoms
        depression_score = 0
        for category, keywords in self.mental_health_indicators['depression'].items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                symptoms_found[f'depression_{category}'].extend(found)
                depression_score += len(found)
        
        # Check for anxiety symptoms
        anxiety_score = 0
        for category, keywords in self.mental_health_indicators['anxiety'].items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                symptoms_found[f'anxiety_{category}'].extend(found)
                anxiety_score += len(found)
        
        # Check for functional impairment
        impairment_score = 0
        for category, keywords in self.mental_health_indicators['functional_impairment'].items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                symptoms_found[f'impairment_{category}'].extend(found)
                impairment_score += len(found)
        
        # Check for stress indicators
        stress_score = 0
        for category, keywords in self.mental_health_indicators['stress'].items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                symptoms_found[f'stress_{category}'].extend(found)
                stress_score += len(found)
        
        # Calculate total score
        total_indicators = len(symptoms_found)
        base_score = (depression_score * 3 + anxiety_score * 2.5 + 
                     impairment_score * 2 + stress_score * 1.5) * severity_multiplier
        
        # Normalize to 0-100
        normalized_score = min(100, base_score * 2)
        
        return {
            'risk_score': round(normalized_score, 2),
            'risk_category': self._categorize_risk(normalized_score, severe_found),
            'symptoms_found': dict(symptoms_found),
            'depression_indicators': depression_score,
            'anxiety_indicators': anxiety_score,
            'impairment_indicators': impairment_score,
            'severe_symptoms': severe_found,
            'total_indicators': total_indicators
        }
    
    def _categorize_risk(self, score, severe_symptoms):
        """Categorize mental health risk"""
        if severe_symptoms or score >= 70:
            return 'SEVERE'
        elif score >= 45:
            return 'MODERATE'
        elif score >= 20:
            return 'MILD'
        else:
            return 'MINIMAL'

# SECTION 4: TREATMENT RECOMMENDATIONS (SA NDOH GUIDELINES)

class TreatmentRecommender:
    """
    Generate treatment recommendations based on SA NDOH Guidelines
    """
    
    def __init__(self):
        self.hiv_recommendations = {
            'HIGH': {
                'urgency': 'URGENT - Within 24 hours',
                'testing': [
                    'Immediate HIV testing recommended at nearest facility',
                    'Consider HIV self-testing if unable to reach facility immediately',
                    'If recent exposure (<72 hours): PEP (Post-Exposure Prophylaxis) eligibility assessment',
                    'Follow SA NDOH HTS Policy 2016 guidelines'
                ],
                'counseling': [
                    'Pre-test counseling required',
                    'Partner notification services recommended',
                    'Risk reduction counseling'
                ],
                'referral': [
                    'Refer to nearest Primary Health Care (PHC) facility',
                    'Contact National AIDS Helpline: 0800 012 322',
                    'Consider referral for STI screening',
                    'If pregnant: Urgent PMTCT services'
                ],
                'prevention': [
                    'PrEP (Pre-Exposure Prophylaxis) assessment for ongoing risk',
                    'Condom provision and education',
                    'Partner testing recommendation'
                ]
            },
            'MEDIUM': {
                'urgency': 'Within 1 week',
                'testing': [
                    'HIV testing recommended',
                    'Schedule appointment at local clinic',
                    'Consider self-testing options',
                    'Regular testing every 3-6 months if ongoing risk'
                ],
                'counseling': [
                    'Pre-test counseling',
                    'Risk assessment and reduction strategies',
                    'Sexual health education'
                ],
                'referral': [
                    'PHC clinic referral',
                    'Community-based testing services',
                    'Mobile testing units'
                ],
                'prevention': [
                    'Assess PrEP eligibility',
                    'Condom access and education',
                    'STI prevention counseling'
                ]
            },
            'LOW': {
                'urgency': 'Routine - Within 1 month',
                'testing': [
                    'Consider HIV testing as part of routine health check',
                    'Testing recommended if never tested before',
                    'Annual testing recommended for sexually active adults'
                ],
                'counseling': [
                    'General HIV prevention education',
                    'Risk awareness counseling'
                ],
                'referral': [
                    'Local clinic for routine screening',
                    'Community health worker support available'
                ],
                'prevention': [
                    'Safe sex practices education',
                    'Regular condom use',
                    'Know your status campaign participation'
                ]
            }
        }
        
        self.mental_health_recommendations = {
            'SEVERE': {
                'urgency': 'EMERGENCY - Immediate intervention required',
                'assessment': [
                    'Immediate psychiatric evaluation required',
                    'Suicide risk assessment if ideation present',
                    'Safety planning essential',
                    'Consider involuntary admission if danger to self/others (Mental Health Care Act 17 of 2002)'
                ],
                'treatment': [
                    'Initiate pharmacotherapy (SSRIs as per SA NDOH PHC guidelines)',
                    'Consider: Fluoxetine 20mg daily (first-line for depression/anxiety)',
                    'Intensive psychological intervention',
                    'Crisis intervention',
                    'Possible hospitalization'
                ],
                'referral': [
                    'Emergency psychiatric services',
                    'District mental health services',
                    'Psychiatrist or clinical psychologist',
                    'SADAG Crisis Line: 0800 567 567 or 011 262 6396',
                    'Suicide Crisis Line: 0800 567 567'
                ],
                'support': [
                    'Family psychoeducation',
                    'Community mental health worker involvement',
                    'Case management',
                    'Disability grant assessment if applicable'
                ]
            },
            'MODERATE': {
                'urgency': 'Within 1-2 weeks',
                'assessment': [
                    'Comprehensive mental health assessment',
                    'PHQ-9 for depression / GAD-7 for anxiety screening',
                    'Functional impairment evaluation',
                    'Substance use screening'
                ],
                'treatment': [
                    'Psychological counseling (8-12 sessions recommended)',
                    'Consider pharmacotherapy: Fluoxetine 20mg daily',
                    'Evidence-based therapy: CBT or Interpersonal Therapy',
                    'Lay counselor intervention if available',
                    'Group therapy consideration'
                ],
                'referral': [
                    'PHC facility mental health services',
                    'Clinical psychologist or counselor',
                    'Lay counselor for depression management',
                    'SADAG support groups',
                    'Contact: SADAG 011 262 6396'
                ],
                'support': [
                    'Psychoeducation for patient and family',
                    'Stress management techniques',
                    'Sleep hygiene education',
                    'Social support activation'
                ]
            },
            'MILD': {
                'urgency': 'Within 1 month',
                'assessment': [
                    'Screening for depression/anxiety',
                    'Psychosocial stressor identification',
                    'Monitor symptom progression'
                ],
                'treatment': [
                    'Psychoeducation',
                    'Guided self-help',
                    'Lifestyle modifications',
                    'Watchful waiting with regular review',
                    'Problem-solving therapy'
                ],
                'referral': [
                    'Primary care counselor',
                    'Community mental health services',
                    'SADAG support resources',
                    'Online mental health resources'
                ],
                'support': [
                    'Physical activity promotion',
                    'Sleep hygiene',
                    'Stress reduction techniques',
                    'Social connection encouragement',
                    'Self-care strategies'
                ]
            },
            'MINIMAL': {
                'urgency': 'Routine monitoring',
                'assessment': [
                    'General mental health awareness',
                    'Stress management assessment',
                    'Wellness check'
                ],
                'treatment': [
                    'Mental health promotion',
                    'Stress management education',
                    'Resilience building',
                    'Prevention strategies'
                ],
                'referral': [
                    'No immediate referral needed',
                    'Resources: SADAG website www.sadag.org',
                    'Community support groups if interested'
                ],
                'support': [
                    'General wellness advice',
                    'Work-life balance',
                    'Healthy coping strategies',
                    'Regular self-monitoring'
                ]
            }
        }
    
    def generate_recommendations(self, hiv_assessment, mental_health_assessment):
        """
        Generate comprehensive treatment plan
        
        Parameters:
        -----------
        hiv_assessment : dict
            HIV risk assessment results
        mental_health_assessment : dict
            Mental health assessment results
            
        Returns:
        --------
        dict : Comprehensive treatment recommendations
        """
        hiv_risk = hiv_assessment['risk_category']
        mh_risk = mental_health_assessment['risk_category']
        
        recommendations = {
            'summary': {
                'hiv_risk': hiv_risk,
                'hiv_score': hiv_assessment['risk_score'],
                'mental_health_risk': mh_risk,
                'mental_health_score': mental_health_assessment['risk_score'],
                'integrated_care_needed': hiv_risk in ['HIGH', 'MEDIUM'] or mh_risk in ['SEVERE', 'MODERATE']
            },
            'hiv_plan': self.hiv_recommendations[hiv_risk],
            'mental_health_plan': self.mental_health_recommendations[mh_risk],
            'integrated_considerations': self._generate_integrated_care(hiv_risk, mh_risk)
        }
        
        return recommendations
    
    def _generate_integrated_care(self, hiv_risk, mh_risk):
        """Generate integrated care considerations"""
        considerations = []
        
        # SA NDOH recognizes strong link between HIV and mental health
        if hiv_risk in ['HIGH', 'MEDIUM'] and mh_risk in ['SEVERE', 'MODERATE']:
            considerations.extend([
                'INTEGRATED CARE APPROACH RECOMMENDED:',
                '- HIV and mental health are interconnected (SA NDOH Policy)',
                '- Mental health screening essential for HIV prevention/care',
                '- Depression/anxiety can affect HIV risk behavior and adherence',
                '- Coordinated care between HIV and mental health services',
                '- Community health worker involvement for both conditions',
                '- Support groups for dual diagnosis'
            ])
        
        if mh_risk == 'SEVERE':
            considerations.extend([
                'URGENT MENTAL HEALTH PRIORITY:',
                '- Mental health crisis may affect HIV-related decisions',
                '- Ensure psychological stability before HIV testing if possible',
                '- Post-test support critical if HIV positive',
                '- Coordinate mental health and HIV services'
            ])
        
        return considerations


# SECTION 5: ANALYSIS AND REPORTING

def analyze_conversations(conversations):
    """
    Perform comprehensive analysis of all conversations
    
    Parameters:
    -----------
    conversations : list
        List of parsed conversations
        
    Returns:
    --------
    DataFrame : Analysis results
    """
    print("Analyzing conversations...")
    print("-" * 80)
    
    hiv_assessor = HIVRiskAssessor()
    mh_assessor = MentalHealthAssessor()
    recommender = TreatmentRecommender()
    
    results = []
    
    for conv in conversations:
        conv_id = conv['conversation_id']
        text = conv['full_text']
        
        # Perform assessments
        hiv_assessment = hiv_assessor.calculate_risk_score(text)
        mh_assessment = mh_assessor.calculate_risk_score(text)
        recommendations = recommender.generate_recommendations(hiv_assessment, mh_assessment)
        
        results.append({
            'conversation_id': conv_id,
            'hiv_risk_score': hiv_assessment['risk_score'],
            'hiv_risk_category': hiv_assessment['risk_category'],
            'hiv_indicators': hiv_assessment['total_indicators'],
            'mh_risk_score': mh_assessment['risk_score'],
            'mh_risk_category': mh_assessment['risk_category'],
            'mh_depression': mh_assessment['depression_indicators'],
            'mh_anxiety': mh_assessment['anxiety_indicators'],
            'mh_severe': mh_assessment['severe_symptoms'],
            'integrated_care_needed': recommendations['summary']['integrated_care_needed'],
            'full_hiv_assessment': hiv_assessment,
            'full_mh_assessment': mh_assessment,
            'recommendations': recommendations
        })
    
    df = pd.DataFrame(results)
    
    print(f"✓ Analyzed {len(df)} conversations")
    print()
    
    return df

def generate_summary_statistics(df):
    """Generate summary statistics"""
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()
    
    print("HIV RISK DISTRIBUTION:")
    print("-" * 40)
    hiv_dist = df['hiv_risk_category'].value_counts()
    for category, count in hiv_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {category:10s}: {count:3d} ({percentage:5.1f}%)")
    print()
    
    print("MENTAL HEALTH RISK DISTRIBUTION:")
    print("-" * 40)
    mh_dist = df['mh_risk_category'].value_counts()
    for category, count in mh_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {category:10s}: {count:3d} ({percentage:5.1f}%)")
    print()
    
    print("RISK SCORES (Mean ± SD):")
    print("-" * 40)
    print(f"  HIV Risk Score:          {df['hiv_risk_score'].mean():.2f} ± {df['hiv_risk_score'].std():.2f}")
    print(f"  Mental Health Score:     {df['mh_risk_score'].mean():.2f} ± {df['mh_risk_score'].std():.2f}")
    print()
    
    print("INTEGRATED CARE NEEDS:")
    print("-" * 40)
    integrated = df['integrated_care_needed'].sum()
    print(f"  Conversations requiring integrated care: {integrated} ({(integrated/len(df)*100):.1f}%)")
    print()
    
    print("SEVERE CASES REQUIRING URGENT ATTENTION:")
    print("-" * 40)
    high_hiv = len(df[df['hiv_risk_category'] == 'HIGH'])
    severe_mh = len(df[df['mh_risk_category'] == 'SEVERE'])
    print(f"  HIGH HIV risk:           {high_hiv}")
    print(f"  SEVERE mental health:    {severe_mh}")
    print(f"  Total urgent cases:      {max(high_hiv + severe_mh, 0)}")
    print()

def create_visualizations(df):
    """Create visualization plots"""
    print("=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    print()
    
    fig = plt.figure(figsize=(16, 12))
    
    # 1. HIV Risk Distribution
    ax1 = plt.subplot(2, 3, 1)
    hiv_counts = df['hiv_risk_category'].value_counts()
    colors_hiv = {'HIGH': '#d62728', 'MEDIUM': '#ff7f0e', 'LOW': '#2ca02c'}
    ax1.bar(hiv_counts.index, hiv_counts.values, 
            color=[colors_hiv.get(x, '#1f77b4') for x in hiv_counts.index])
    ax1.set_title('HIV Risk Category Distribution', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Conversations')
    ax1.set_xlabel('Risk Category')
    for i, v in enumerate(hiv_counts.values):
        ax1.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    # 2. Mental Health Risk Distribution
    ax2 = plt.subplot(2, 3, 2)
    mh_counts = df['mh_risk_category'].value_counts()
    colors_mh = {'SEVERE': '#d62728', 'MODERATE': '#ff7f0e', 'MILD': '#ffdd57', 'MINIMAL': '#2ca02c'}
    ax2.bar(mh_counts.index, mh_counts.values,
            color=[colors_mh.get(x, '#1f77b4') for x in mh_counts.index])
    ax2.set_title('Mental Health Risk Distribution', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Conversations')
    ax2.set_xlabel('Risk Category')
    for i, v in enumerate(mh_counts.values):
        ax2.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    # 3. Risk Score Distribution
    ax3 = plt.subplot(2, 3, 3)
    ax3.hist(df['hiv_risk_score'], bins=20, alpha=0.5, label='HIV Risk', color='#1f77b4')
    ax3.hist(df['mh_risk_score'], bins=20, alpha=0.5, label='Mental Health Risk', color='#ff7f0e')
    ax3.set_title('Risk Score Distribution', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Risk Score (0-100)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    ax3.axvline(df['hiv_risk_score'].mean(), color='#1f77b4', linestyle='--', linewidth=2, label='HIV Mean')
    ax3.axvline(df['mh_risk_score'].mean(), color='#ff7f0e', linestyle='--', linewidth=2, label='MH Mean')
    
    # 4. Correlation Heatmap
    ax4 = plt.subplot(2, 3, 4)
    corr_data = df[['hiv_risk_score', 'mh_risk_score', 'hiv_indicators', 
                     'mh_depression', 'mh_anxiety']].corr()
    sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                ax=ax4, square=True, cbar_kws={'shrink': 0.8})
    ax4.set_title('Risk Factor Correlations', fontsize=12, fontweight='bold')
    
    # 5. Scatter: HIV vs Mental Health Risk
    ax5 = plt.subplot(2, 3, 5)
    scatter = ax5.scatter(df['hiv_risk_score'], df['mh_risk_score'], 
                         alpha=0.6, s=50, c=df['integrated_care_needed'],
                         cmap='RdYlGn_r', edgecolors='black', linewidth=0.5)
    ax5.set_xlabel('HIV Risk Score')
    ax5.set_ylabel('Mental Health Risk Score')
    ax5.set_title('HIV vs Mental Health Risk', fontsize=12, fontweight='bold')
    ax5.axhline(y=45, color='r', linestyle='--', alpha=0.3, label='MH Moderate Threshold')
    ax5.axvline(x=30, color='r', linestyle='--', alpha=0.3, label='HIV Medium Threshold')
    ax5.legend(loc='upper right', fontsize=8)
    plt.colorbar(scatter, ax=ax5, label='Integrated Care Needed')
    
    # 6. Indicator Counts
    ax6 = plt.subplot(2, 3, 6)
    indicator_data = {
        'HIV\nIndicators': df['hiv_indicators'].sum(),
        'Depression\nIndicators': df['mh_depression'].sum(),
        'Anxiety\nIndicators': df['mh_anxiety'].sum()
    }
    bars = ax6.bar(indicator_data.keys(), indicator_data.values(), 
                   color=['#1f77b4', '#ff7f0e', '#d62728'])
    ax6.set_title('Total Risk Indicators Found', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Total Count')
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/tendai/user-data/outputs/risk_assessment_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Visualizations saved to: /mnt/user-data/outputs/risk_assessment_analysis.png")
    print()
    
    return fig

def generate_detailed_report(df, sample_size=3):
    """Generate detailed report for sample conversations"""
    print("=" * 80)
    print(f"DETAILED CASE REPORTS (Sample: {sample_size} conversations)")
    print("=" * 80)
    print()
    
    # Select diverse sample: highest HIV risk, highest MH risk, and one moderate
    high_hiv_idx = df.nlargest(1, 'hiv_risk_score').index[0]
    high_mh_idx = df.nlargest(1, 'mh_risk_score').index[0]
    
    # Get a moderate case if exists
    moderate_df = df[(df['hiv_risk_score'] > 20) & (df['mh_risk_score'] > 20)]
    if len(moderate_df) > 0:
        moderate_idx = moderate_df.head(1).index[0]
        sample_indices = list(set([high_hiv_idx, high_mh_idx, moderate_idx]))
    else:
        # If no moderate cases, just get top 3 by total risk
        df['total_risk'] = df['hiv_risk_score'] + df['mh_risk_score']
        sample_indices = df.nlargest(sample_size, 'total_risk').index.tolist()
    
    sample_df = df.loc[sample_indices]
    
    for idx, row in sample_df.iterrows():
        print("-" * 80)
        print(f"CASE #{row['conversation_id']}")
        print("-" * 80)
        print()
        
        print("RISK ASSESSMENT:")
        print(f"  HIV Risk:            {row['hiv_risk_category']:10s} (Score: {row['hiv_risk_score']:.1f}/100)")
        print(f"  Mental Health Risk:  {row['mh_risk_category']:10s} (Score: {row['mh_risk_score']:.1f}/100)")
        print(f"  HIV Indicators:      {row['hiv_indicators']}")
        print(f"  Depression Signs:    {row['mh_depression']}")
        print(f"  Anxiety Signs:       {row['mh_anxiety']}")
        print(f"  Severe MH Symptoms:  {'Yes' if row['mh_severe'] else 'No'}")
        print()
        
        recs = row['recommendations']
        
        print("RECOMMENDED TREATMENT PLAN (SA NDOH Guidelines):")
        print()
        print("HIV MANAGEMENT:")
        print(f"  Urgency: {recs['hiv_plan']['urgency']}")
        print("  Testing Recommendations:")
        for rec in recs['hiv_plan']['testing'][:3]:
            print(f"    • {rec}")
        print("  Referral:")
        for ref in recs['hiv_plan']['referral'][:2]:
            print(f"    • {ref}")
        print()
        
        print("MENTAL HEALTH MANAGEMENT:")
        print(f"  Urgency: {recs['mental_health_plan']['urgency']}")
        print("  Assessment Needed:")
        for assess in recs['mental_health_plan']['assessment'][:3]:
            print(f"    • {assess}")
        print("  Treatment:")
        for treat in recs['mental_health_plan']['treatment'][:3]:
            print(f"    • {treat}")
        print()
        
        if recs['integrated_considerations']:
            print("INTEGRATED CARE CONSIDERATIONS:")
            for consideration in recs['integrated_considerations'][:5]:
                print(f"  {consideration}")
        print()
        print()

def save_results(df, file_path='/tendai/user-data/outputs/risk_assessment_results.csv'):
    """Save results to CSV"""
    # Prepare simplified dataframe for export
    export_df = df[['conversation_id', 'hiv_risk_score', 'hiv_risk_category',
                     'mh_risk_score', 'mh_risk_category', 'integrated_care_needed']].copy()
    
    export_df.to_csv(file_path, index=False)
    print(f"✓ Results saved to: {file_path}")
    print()

# ============================================================================
# SECTION 6: MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    # Load data
    conversations = load_conversations('/tendai/user-data/uploads/health_ai_whatsapp_100_conversations_long.txt')
    
    # Analyze conversations
    results_df = analyze_conversations(conversations)
    
    # Generate statistics
    generate_summary_statistics(results_df)
    
    # Create visualizations
    create_visualizations(results_df)
    
    # Generate detailed reports
    generate_detailed_report(results_df, sample_size=3)
    
    # Save results
    save_results(results_df)
    
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("Key Deliverables:")
    print("  1. Risk assessment scores for all 100 conversations")
    print("  2. Treatment recommendations based on SA NDOH guidelines")
    print("  3. Statistical analysis and visualizations")
    print("  4. Detailed case reports for high-risk conversations")
    print()
    print("Files Generated:")
    print("  • /tendai/user-data/outputs/risk_assessment_analysis.png")
    print("  • /tendai/user-data/outputs/risk_assessment_results.csv")
    print()
    print("=" * 80)
    print()
    
    return results_df

# Run the analysis
if __name__ == "__main__":
    results = main()
