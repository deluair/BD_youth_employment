#!/usr/bin/env python3
"""
Bangladesh Youth Employment AI-Enhanced Simulation Framework

This framework provides comprehensive simulation capabilities for testing
and optimizing the AI-enhanced employment strategy using realistic data.

Author: AI-Enhanced Employment Framework Team
Version: 1.0
Date: 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import random
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

class AgentType(Enum):
    """Types of agents in the simulation"""
    YOUTH_UNEMPLOYED = "youth_unemployed"
    YOUTH_UNDEREMPLOYED = "youth_underemployed"
    EMPLOYER_LOCAL = "employer_local"
    EMPLOYER_INTERNATIONAL = "employer_international"
    TRAINING_PROVIDER = "training_provider"
    GOVERNMENT = "government"
    FAMILY_UNIT = "family_unit"

class Region(Enum):
    """Geographic regions in Bangladesh"""
    DHAKA = "dhaka"
    CHITTAGONG = "chittagong"
    SYLHET = "sylhet"
    RURAL_AREAS = "rural_areas"

class SkillLevel(Enum):
    """AI-enhanced skill proficiency levels"""
    NONE = 0
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class YouthAgent:
    """Individual youth agent with comprehensive attributes"""
    id: str
    age: int
    gender: str  # 'male' or 'female'
    region: Region
    education_level: str
    employment_status: str
    monthly_income: float  # BDT
    
    # Skills and capabilities
    english_proficiency: float  # 0-1 scale
    digital_literacy: float  # 0-1 scale
    ai_familiarity: float  # 0-1 scale
    
    # Social and cultural factors
    family_support: float  # 0-1 scale
    social_network_strength: float  # 0-1 scale
    cultural_constraints: float  # 0-1 scale (higher = more constraints)
    motivation_level: float  # 0-1 scale
    
    # Economic factors
    financial_resources: float  # BDT
    debt_burden: float  # BDT
    family_financial_pressure: float  # 0-1 scale
    
    # Fields with default values must come after non-default fields
    traditional_skills: Dict[str, float] = field(default_factory=dict)
    ai_enhanced_skills: Dict[str, float] = field(default_factory=dict)
    
    # Program participation
    program_participation: bool = False
    training_completion_rate: float = 0.0
    months_in_program: int = 0
    
    # Historical tracking
    employment_history: List[Dict] = field(default_factory=list)
    income_history: List[float] = field(default_factory=list)
    skill_development_history: List[Dict] = field(default_factory=list)

@dataclass
class EmployerAgent:
    """Employer agent representing demand side"""
    id: str
    type: str  # 'local', 'international', 'startup', 'enterprise'
    region: Region
    industry: str
    size: str  # 'small', 'medium', 'large'
    
    # Demand characteristics
    monthly_job_openings: int
    skill_requirements: Dict[str, float]
    salary_range: Tuple[float, float]  # BDT
    remote_work_capability: float  # 0-1 scale
    
    # AI adoption
    ai_integration_level: float  # 0-1 scale
    human_ai_collaboration_need: float  # 0-1 scale
    
    # Hiring preferences
    experience_preference: float  # 0-1 scale
    certification_importance: float  # 0-1 scale
    cultural_fit_importance: float  # 0-1 scale

class SimulationEngine:
    """Main simulation engine for the employment framework"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_month = 0
        self.max_months = config.get('simulation_months', 36)
        
        # Initialize data from realistic_data_module
        self.load_realistic_data()
        
        # Initialize agents
        self.youth_agents: List[YouthAgent] = []
        self.employer_agents: List[EmployerAgent] = []
        
        # Tracking variables
        self.monthly_metrics = []
        self.intervention_effects = {}
        self.policy_impacts = {}
        
        # Generate initial population
        self.generate_youth_population()
        self.generate_employer_population()
        
    def load_realistic_data(self):
        """Load realistic data parameters from the data module"""
        
        # Demographics data
        self.youth_demographics = {
            'total_population_25_35': 18_500_000,
            'male_percentage': 51.2,
            'female_percentage': 48.8,
            'urban_percentage': 38.2,
            'rural_percentage': 61.8,
            'education_distribution': {
                'no_formal_education': 8.3,
                'primary_complete': 15.7,
                'secondary_complete': 32.4,
                'higher_secondary': 28.1,
                'bachelor_degree': 12.8,
                'master_plus': 2.7
            }
        }
        
        # Regional data
        self.regional_data = {
            'dhaka': {
                'population_25_35': 3_200_000,
                'unemployment_rate': 14.2,
                'average_monthly_income': 28_500,
                'internet_penetration': 78.3,
                'english_proficiency_avg': 0.42,
                'ai_awareness': 0.35,
                'freelancing_participation': 8.7
            },
            'chittagong': {
                'population_25_35': 1_800_000,
                'unemployment_rate': 15.8,
                'average_monthly_income': 24_200,
                'internet_penetration': 71.5,
                'english_proficiency_avg': 0.38,
                'ai_awareness': 0.28,
                'freelancing_participation': 6.2
            },
            'sylhet': {
                'population_25_35': 950_000,
                'unemployment_rate': 18.3,
                'average_monthly_income': 21_800,
                'internet_penetration': 68.9,
                'english_proficiency_avg': 0.45,
                'ai_awareness': 0.31,
                'freelancing_participation': 9.1
            },
            'rural_areas': {
                'population_25_35': 12_550_000,
                'unemployment_rate': 22.7,
                'average_monthly_income': 16_400,
                'internet_penetration': 52.1,
                'english_proficiency_avg': 0.23,
                'ai_awareness': 0.15,
                'freelancing_participation': 2.8
            }
        }
        
        # Skills market data
        self.ai_skills_demand = {
            'prompt_engineering': {
                'monthly_job_postings': 2_340,
                'average_hourly_rate_usd': 28,
                'growth_rate_annual': 145,
                'skill_shortage_index': 0.73
            },
            'ai_content_creation': {
                'monthly_job_postings': 4_680,
                'average_hourly_rate_usd': 22,
                'growth_rate_annual': 89,
                'skill_shortage_index': 0.61
            },
            'data_annotation': {
                'monthly_job_postings': 6_120,
                'average_hourly_rate_usd': 15,
                'growth_rate_annual': 67,
                'skill_shortage_index': 0.45
            },
            'ai_customer_support': {
                'monthly_job_postings': 3_890,
                'average_hourly_rate_usd': 18,
                'growth_rate_annual': 78,
                'skill_shortage_index': 0.52
            },
            'human_ai_collaboration': {
                'monthly_job_postings': 1_560,
                'average_hourly_rate_usd': 35,
                'growth_rate_annual': 198,
                'skill_shortage_index': 0.84
            }
        }
        
        # Training outcomes
        self.training_outcomes = {
            'program_completion_rates': {
                'on_job_training': 78.3,
                'classroom_training': 82.1,
                'combined_training': 85.7,
                'online_training': 71.2
            },
            'employment_outcomes_6_months': {
                'on_job_training': 68.4,
                'classroom_training': 52.1,
                'combined_training': 73.8,
                'control_group': 52.4
            },
            'earnings_improvement': {
                'on_job_training': 23.0,
                'classroom_training': 15.2,
                'combined_training': 28.7,
                'control_group': 3.1
            }
        }
        
        # Economic multipliers
        self.economic_multipliers = {
            'direct_employment': 1.0,
            'indirect_employment': 1.42,
            'induced_employment': 0.78,
            'total_multiplier': 2.20,
            'sector_specific_multipliers': {
                'ai_services': 2.45,
                'digital_content': 1.98,
                'online_education': 2.12,
                'e_commerce_support': 1.87,
                'remote_consulting': 2.33
            }
        }
        
    def generate_youth_population(self):
        """Generate representative youth population based on realistic data"""
        
        num_agents = self.config.get('num_youth_agents', 10000)
        
        for i in range(num_agents):
            # Determine region based on population distribution
            region_prob = np.random.random()
            if region_prob < 0.173:  # 17.3% in Dhaka
                region = Region.DHAKA
            elif region_prob < 0.270:  # 9.7% in Chittagong
                region = Region.CHITTAGONG
            elif region_prob < 0.321:  # 5.1% in Sylhet
                region = Region.SYLHET
            else:  # 67.9% in rural areas
                region = Region.RURAL_AREAS
            
            # Determine gender
            gender = 'male' if np.random.random() < 0.512 else 'female'
            
            # Determine education level
            edu_rand = np.random.random() * 100
            if edu_rand < 8.3:
                education = 'no_formal_education'
            elif edu_rand < 24.0:
                education = 'primary_complete'
            elif edu_rand < 56.4:
                education = 'secondary_complete'
            elif edu_rand < 84.5:
                education = 'higher_secondary'
            elif edu_rand < 97.3:
                education = 'bachelor_degree'
            else:
                education = 'master_plus'
            
            # Determine employment status
            emp_rand = np.random.random() * 100
            if emp_rand < 23.4:
                employment_status = 'employed_formal'
            elif emp_rand < 65.2:
                employment_status = 'employed_informal'
            elif emp_rand < 82.0:
                employment_status = 'unemployed_seeking'
            elif emp_rand < 94.3:
                employment_status = 'underemployed'
            else:
                employment_status = 'not_in_labor_force'
            
            # Generate skills based on region and demographics
            regional_data = self.regional_data[region.value]
            
            # English proficiency with variation
            base_english = regional_data['english_proficiency_avg']
            english_proficiency = np.clip(np.random.normal(base_english, 0.15), 0, 1)
            
            # Digital literacy based on gender and region
            if region in [Region.DHAKA, Region.CHITTAGONG]:
                base_digital = 0.67 if gender == 'male' else 0.59
            else:
                base_digital = 0.34 if gender == 'male' else 0.22
            digital_literacy = np.clip(np.random.normal(base_digital, 0.12), 0, 1)
            
            # AI familiarity
            base_ai = regional_data['ai_awareness']
            ai_familiarity = np.clip(np.random.normal(base_ai, 0.08), 0, 1)
            
            # Social factors
            family_support = self._calculate_family_support(gender, region, education)
            social_network = np.random.beta(2, 5)  # Skewed towards lower values
            cultural_constraints = self._calculate_cultural_constraints(gender, region)
            motivation_level = np.random.beta(3, 2)  # Skewed towards higher values
            
            # Economic factors
            base_income = regional_data['average_monthly_income']
            if employment_status == 'unemployed_seeking':
                monthly_income = 0
            elif employment_status == 'underemployed':
                monthly_income = base_income * np.random.uniform(0.3, 0.6)
            else:
                monthly_income = base_income * np.random.uniform(0.7, 1.3)
            
            financial_resources = monthly_income * np.random.uniform(0.5, 3.0)
            debt_burden = financial_resources * np.random.uniform(0, 0.4)
            family_pressure = np.random.beta(2, 3) if monthly_income < base_income * 0.8 else np.random.beta(1, 4)
            
            # Create youth agent
            youth = YouthAgent(
                id=f"youth_{i:06d}",
                age=np.random.randint(25, 36),
                gender=gender,
                region=region,
                education_level=education,
                employment_status=employment_status,
                monthly_income=monthly_income,
                english_proficiency=english_proficiency,
                digital_literacy=digital_literacy,
                ai_familiarity=ai_familiarity,
                family_support=family_support,
                social_network_strength=social_network,
                cultural_constraints=cultural_constraints,
                motivation_level=motivation_level,
                financial_resources=financial_resources,
                debt_burden=debt_burden,
                family_financial_pressure=family_pressure
            )
            
            # Initialize skill sets
            youth.traditional_skills = self._generate_traditional_skills(youth)
            youth.ai_enhanced_skills = self._generate_ai_skills(youth)
            
            self.youth_agents.append(youth)
    
    def generate_employer_population(self):
        """Generate employer agents representing demand side"""
        
        num_employers = self.config.get('num_employer_agents', 1000)
        
        for i in range(num_employers):
            # Determine employer type and characteristics
            employer_type = np.random.choice(
                ['local', 'international', 'startup', 'enterprise'],
                p=[0.4, 0.3, 0.2, 0.1]
            )
            
            # Region distribution for employers
            if employer_type == 'international':
                region = np.random.choice([Region.DHAKA, Region.CHITTAGONG], p=[0.7, 0.3])
            else:
                region = np.random.choice(list(Region), p=[0.4, 0.25, 0.15, 0.2])
            
            # Industry distribution
            industry = np.random.choice([
                'technology', 'content_creation', 'customer_service',
                'education', 'consulting', 'e_commerce', 'marketing'
            ], p=[0.25, 0.18, 0.15, 0.12, 0.1, 0.12, 0.08])
            
            # Company size
            size = np.random.choice(['small', 'medium', 'large'], p=[0.6, 0.3, 0.1])
            
            # Job openings based on size and type
            if size == 'small':
                monthly_openings = np.random.poisson(2)
            elif size == 'medium':
                monthly_openings = np.random.poisson(8)
            else:
                monthly_openings = np.random.poisson(20)
            
            # Salary ranges based on industry and type
            base_salary = self._calculate_base_salary(employer_type, industry, region)
            salary_range = (base_salary * 0.8, base_salary * 1.5)
            
            # AI integration level
            ai_integration = np.random.beta(2, 3) if employer_type in ['startup', 'enterprise'] else np.random.beta(1, 4)
            
            # Skill requirements
            skill_requirements = self._generate_skill_requirements(industry, ai_integration)
            
            employer = EmployerAgent(
                id=f"employer_{i:04d}",
                type=employer_type,
                region=region,
                industry=industry,
                size=size,
                monthly_job_openings=monthly_openings,
                skill_requirements=skill_requirements,
                salary_range=salary_range,
                remote_work_capability=np.random.beta(3, 2) if employer_type == 'international' else np.random.beta(2, 3),
                ai_integration_level=ai_integration,
                human_ai_collaboration_need=ai_integration * np.random.uniform(0.7, 1.0),
                experience_preference=np.random.beta(2, 2),
                certification_importance=np.random.beta(3, 2),
                cultural_fit_importance=np.random.beta(2, 2)
            )
            
            self.employer_agents.append(employer)
    
    def _calculate_family_support(self, gender: str, region: Region, education: str) -> float:
        """Calculate family support probability based on demographics"""
        
        base_support = 0.6
        
        # Gender effect
        if gender == 'female':
            base_support *= 0.85
        
        # Region effect
        if region == Region.DHAKA:
            base_support *= 1.15
        elif region == Region.RURAL_AREAS:
            base_support *= 0.9
        
        # Education effect
        if education in ['bachelor_degree', 'master_plus']:
            base_support *= 1.2
        elif education in ['no_formal_education', 'primary_complete']:
            base_support *= 0.8
        
        return np.clip(np.random.normal(base_support, 0.15), 0, 1)
    
    def _calculate_cultural_constraints(self, gender: str, region: Region) -> float:
        """Calculate cultural constraints factor"""
        
        base_constraints = 0.3
        
        if gender == 'female':
            base_constraints *= 1.8
            
        if region == Region.RURAL_AREAS:
            base_constraints *= 1.5
        elif region == Region.DHAKA:
            base_constraints *= 0.7
        
        return np.clip(np.random.normal(base_constraints, 0.12), 0, 1)
    
    def _generate_traditional_skills(self, youth: YouthAgent) -> Dict[str, float]:
        """Generate traditional skill set for youth agent"""
        
        skills = {}
        skill_categories = [
            'graphic_design', 'web_development', 'content_writing',
            'digital_marketing', 'data_entry', 'video_editing',
            'translation', 'customer_service'
        ]
        
        for skill in skill_categories:
            # Base skill level influenced by education and digital literacy
            base_level = youth.digital_literacy * 0.6 + np.random.uniform(0, 0.4)
            
            # Education bonus
            if youth.education_level in ['bachelor_degree', 'master_plus']:
                base_level += 0.2
            elif youth.education_level in ['higher_secondary']:
                base_level += 0.1
            
            skills[skill] = np.clip(base_level, 0, 1)
        
        return skills
    
    def _generate_ai_skills(self, youth: YouthAgent) -> Dict[str, float]:
        """Generate AI-enhanced skill set for youth agent"""
        
        skills = {}
        ai_skill_categories = [
            'prompt_engineering', 'ai_content_creation', 'data_annotation',
            'ai_customer_support', 'human_ai_collaboration'
        ]
        
        for skill in ai_skill_categories:
            # Base AI skill influenced by AI familiarity and digital literacy
            base_level = (youth.ai_familiarity * 0.7 + youth.digital_literacy * 0.3) * 0.5
            
            # Add some randomness
            base_level += np.random.uniform(0, 0.3)
            
            skills[skill] = np.clip(base_level, 0, 1)
        
        return skills
    
    def _calculate_base_salary(self, employer_type: str, industry: str, region: Region) -> float:
        """Calculate base salary for employer"""
        
        regional_data = self.regional_data[region.value]
        base = regional_data['average_monthly_income']
        
        # Employer type multiplier
        type_multipliers = {
            'international': 2.5,
            'enterprise': 1.8,
            'startup': 1.4,
            'local': 1.0
        }
        
        # Industry multiplier
        industry_multipliers = {
            'technology': 1.6,
            'consulting': 1.4,
            'content_creation': 1.2,
            'marketing': 1.3,
            'education': 1.1,
            'customer_service': 1.0,
            'e_commerce': 1.2
        }
        
        return base * type_multipliers.get(employer_type, 1.0) * industry_multipliers.get(industry, 1.0)
    
    def _generate_skill_requirements(self, industry: str, ai_integration: float) -> Dict[str, float]:
        """Generate skill requirements for employer"""
        
        requirements = {}
        
        # Base requirements by industry
        industry_skills = {
            'technology': ['web_development', 'prompt_engineering', 'human_ai_collaboration'],
            'content_creation': ['content_writing', 'ai_content_creation', 'graphic_design'],
            'customer_service': ['customer_service', 'ai_customer_support', 'translation'],
            'education': ['content_writing', 'ai_content_creation', 'human_ai_collaboration'],
            'consulting': ['human_ai_collaboration', 'prompt_engineering', 'data_annotation'],
            'e_commerce': ['digital_marketing', 'ai_content_creation', 'customer_service'],
            'marketing': ['digital_marketing', 'ai_content_creation', 'data_annotation']
        }
        
        relevant_skills = industry_skills.get(industry, ['content_writing', 'customer_service'])
        
        for skill in relevant_skills:
            if 'ai_' in skill or skill in ['prompt_engineering', 'human_ai_collaboration']:
                # AI skills requirement influenced by AI integration level
                requirements[skill] = ai_integration * np.random.uniform(0.6, 1.0)
            else:
                # Traditional skills
                requirements[skill] = np.random.uniform(0.4, 0.8)
        
        return requirements
    
    def run_simulation(self) -> Dict[str, Any]:
        """Run the complete simulation"""
        
        print(f"Starting simulation with {len(self.youth_agents)} youth agents and {len(self.employer_agents)} employers")
        print(f"Simulation duration: {self.max_months} months")
        
        for month in range(self.max_months):
            self.current_month = month
            
            # Monthly simulation steps
            self.update_market_conditions()
            self.process_training_programs()
            self.match_jobs()
            self.update_agent_states()
            self.calculate_monthly_metrics()
            
            # Progress reporting
            if month % 6 == 0:
                print(f"Month {month}: {self.get_employment_rate():.1f}% employment rate")
        
        # Generate final results
        results = self.generate_results()
        
        print("\nSimulation completed!")
        print(f"Final employment rate: {results['final_employment_rate']:.1f}%")
        print(f"Average income increase: {results['average_income_increase']:.1f}%")
        print(f"Total economic impact: {results['total_economic_impact']:,.0f} BDT")
        
        return results
    
    def update_market_conditions(self):
        """Update market conditions for current month"""
        
        # Update AI skills demand based on growth rates
        for skill, data in self.ai_skills_demand.items():
            monthly_growth = (data['growth_rate_annual'] / 100) / 12
            data['monthly_job_postings'] *= (1 + monthly_growth)
            
            # Update hourly rates with market dynamics
            if data['skill_shortage_index'] > 0.7:
                data['average_hourly_rate_usd'] *= 1.02  # 2% monthly increase for high shortage
            elif data['skill_shortage_index'] < 0.3:
                data['average_hourly_rate_usd'] *= 0.99  # 1% monthly decrease for oversupply
    
    def process_training_programs(self):
        """Process training program participation and outcomes"""
        
        # Identify eligible youth for training programs
        eligible_youth = [
            youth for youth in self.youth_agents
            if not youth.program_participation and
            youth.employment_status in ['unemployed_seeking', 'underemployed'] and
            youth.motivation_level > 0.5
        ]
        
        # Program capacity constraints
        monthly_capacity = self.config.get('monthly_training_capacity', 500)
        
        # Select participants based on eligibility criteria
        participants = self.select_training_participants(eligible_youth, monthly_capacity)
        
        # Enroll participants
        for youth in participants:
            youth.program_participation = True
            youth.months_in_program = 1
        
        # Update existing participants
        for youth in self.youth_agents:
            if youth.program_participation:
                youth.months_in_program += 1
                self.update_training_progress(youth)
    
    def select_training_participants(self, eligible_youth: List[YouthAgent], capacity: int) -> List[YouthAgent]:
        """Select training participants based on prioritization criteria"""
        
        # Calculate priority scores
        scored_youth = []
        for youth in eligible_youth:
            score = self.calculate_training_priority_score(youth)
            scored_youth.append((youth, score))
        
        # Sort by priority score (higher is better)
        scored_youth.sort(key=lambda x: x[1], reverse=True)
        
        # Select top candidates within capacity
        selected = [youth for youth, score in scored_youth[:capacity]]
        
        return selected
    
    def calculate_training_priority_score(self, youth: YouthAgent) -> float:
        """Calculate priority score for training program selection"""
        
        score = 0.0
        
        # Motivation factor (30%)
        score += youth.motivation_level * 0.3
        
        # Family support factor (20%)
        score += youth.family_support * 0.2
        
        # Digital literacy baseline (20%)
        score += youth.digital_literacy * 0.2
        
        # Economic need factor (15%)
        if youth.employment_status == 'unemployed_seeking':
            score += 0.15
        elif youth.employment_status == 'underemployed':
            score += 0.10
        
        # Cultural constraints (negative factor) (10%)
        score += (1 - youth.cultural_constraints) * 0.1
        
        # Gender equity bonus (5%)
        if youth.gender == 'female':
            score += 0.05
        
        return score
    
    def update_training_progress(self, youth: YouthAgent):
        """Update training progress and skill development"""
        
        # Determine training type based on youth characteristics
        training_type = self.determine_training_type(youth)
        
        # Calculate completion probability
        completion_prob = self.calculate_completion_probability(youth, training_type)
        
        # Update completion rate
        youth.training_completion_rate = min(youth.months_in_program / 6, 1.0) * completion_prob
        
        # Skill development based on training progress
        if youth.training_completion_rate > 0.2:  # After 20% completion
            self.update_skills_from_training(youth, training_type)
        
        # Check for program completion
        if youth.months_in_program >= 6 and youth.training_completion_rate > 0.8:
            youth.program_participation = False
            self.record_training_completion(youth, training_type)
    
    def determine_training_type(self, youth: YouthAgent) -> str:
        """Determine appropriate training type for youth"""
        
        if youth.digital_literacy > 0.7 and youth.ai_familiarity > 0.3:
            return 'advanced_ai_collaboration'
        elif youth.digital_literacy > 0.5:
            return 'intermediate_ai_skills'
        else:
            return 'basic_ai_literacy'
    
    def calculate_completion_probability(self, youth: YouthAgent, training_type: str) -> float:
        """Calculate probability of training completion"""
        
        base_rates = {
            'basic_ai_literacy': 0.78,
            'intermediate_ai_skills': 0.71,
            'advanced_ai_collaboration': 0.65
        }
        
        base_prob = base_rates.get(training_type, 0.75)
        
        # Adjust based on individual factors
        adjustments = [
            youth.motivation_level * 0.2,
            youth.family_support * 0.15,
            (1 - youth.cultural_constraints) * 0.1,
            (1 - youth.family_financial_pressure) * 0.1,
            youth.digital_literacy * 0.1
        ]
        
        final_prob = base_prob + sum(adjustments) - 0.3  # Normalize
        return np.clip(final_prob, 0.1, 0.95)
    
    def update_skills_from_training(self, youth: YouthAgent, training_type: str):
        """Update youth skills based on training progress"""
        
        progress_factor = youth.training_completion_rate
        
        if training_type == 'basic_ai_literacy':
            # Improve basic AI skills
            for skill in ['ai_content_creation', 'data_annotation']:
                improvement = progress_factor * 0.3 * np.random.uniform(0.8, 1.2)
                youth.ai_enhanced_skills[skill] = min(youth.ai_enhanced_skills[skill] + improvement, 1.0)
            
            # Improve digital literacy
            youth.digital_literacy = min(youth.digital_literacy + progress_factor * 0.2, 1.0)
        
        elif training_type == 'intermediate_ai_skills':
            # Improve intermediate AI skills
            for skill in ['prompt_engineering', 'ai_customer_support', 'ai_content_creation']:
                improvement = progress_factor * 0.4 * np.random.uniform(0.8, 1.2)
                youth.ai_enhanced_skills[skill] = min(youth.ai_enhanced_skills[skill] + improvement, 1.0)
        
        elif training_type == 'advanced_ai_collaboration':
            # Improve advanced AI skills
            for skill in ['human_ai_collaboration', 'prompt_engineering']:
                improvement = progress_factor * 0.5 * np.random.uniform(0.8, 1.2)
                youth.ai_enhanced_skills[skill] = min(youth.ai_enhanced_skills[skill] + improvement, 1.0)
        
        # Record skill development
        youth.skill_development_history.append({
            'month': self.current_month,
            'training_type': training_type,
            'progress': progress_factor,
            'skills_updated': list(youth.ai_enhanced_skills.keys())
        })
    
    def record_training_completion(self, youth: YouthAgent, training_type: str):
        """Record training completion and apply final benefits"""
        
        # Final skill boost upon completion
        completion_bonus = 0.2
        
        for skill in youth.ai_enhanced_skills:
            youth.ai_enhanced_skills[skill] = min(youth.ai_enhanced_skills[skill] + completion_bonus, 1.0)
        
        # Improve other attributes
        youth.motivation_level = min(youth.motivation_level + 0.1, 1.0)
        youth.social_network_strength = min(youth.social_network_strength + 0.15, 1.0)
        
        # Record completion
        youth.employment_history.append({
            'month': self.current_month,
            'event': 'training_completed',
            'training_type': training_type,
            'completion_rate': youth.training_completion_rate
        })
    
    def match_jobs(self):
        """Match youth with available jobs"""
        
        # Get available youth (unemployed or underemployed)
        available_youth = [
            youth for youth in self.youth_agents
            if youth.employment_status in ['unemployed_seeking', 'underemployed']
        ]
        
        # Generate job opportunities for this month
        job_opportunities = self.generate_monthly_jobs()
        
        # Perform matching
        matches = self.perform_job_matching(available_youth, job_opportunities)
        
        # Apply matches
        for youth, job in matches:
            self.assign_job(youth, job)
    
    def generate_monthly_jobs(self) -> List[Dict[str, Any]]:
        """Generate job opportunities for the current month"""
        
        jobs = []
        
        for employer in self.employer_agents:
            # Number of jobs this month (Poisson distribution)
            num_jobs = np.random.poisson(employer.monthly_job_openings)
            
            for _ in range(num_jobs):
                # Generate job characteristics
                job = {
                    'employer_id': employer.id,
                    'employer_type': employer.type,
                    'industry': employer.industry,
                    'region': employer.region,
                    'skill_requirements': employer.skill_requirements.copy(),
                    'salary_min': employer.salary_range[0],
                    'salary_max': employer.salary_range[1],
                    'remote_work': np.random.random() < employer.remote_work_capability,
                    'ai_collaboration_required': np.random.random() < employer.human_ai_collaboration_need,
                    'experience_required': np.random.random() < employer.experience_preference,
                    'certification_required': np.random.random() < employer.certification_importance
                }
                
                jobs.append(job)
        
        return jobs
    
    def perform_job_matching(self, youth_list: List[YouthAgent], job_list: List[Dict[str, Any]]) -> List[Tuple[YouthAgent, Dict[str, Any]]]:
        """Perform job matching between youth and opportunities"""
        
        matches = []
        
        # Calculate match scores for all youth-job pairs
        match_scores = []
        
        for youth in youth_list:
            for job in job_list:
                score = self.calculate_match_score(youth, job)
                if score > 0.3:  # Minimum threshold
                    match_scores.append((youth, job, score))
        
        # Sort by match score (highest first)
        match_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Assign jobs (each youth and job can only be matched once)
        assigned_youth = set()
        assigned_jobs = set()
        
        for youth, job, score in match_scores:
            if youth.id not in assigned_youth and id(job) not in assigned_jobs:
                # Additional probability check based on market conditions
                hiring_prob = self.calculate_hiring_probability(youth, job, score)
                
                if np.random.random() < hiring_prob:
                    matches.append((youth, job))
                    assigned_youth.add(youth.id)
                    assigned_jobs.add(id(job))
        
        return matches
    
    def calculate_match_score(self, youth: YouthAgent, job: Dict[str, Any]) -> float:
        """Calculate match score between youth and job"""
        
        score = 0.0
        
        # Skill matching (50% weight)
        skill_match = 0.0
        total_requirements = 0
        
        for skill, required_level in job['skill_requirements'].items():
            total_requirements += 1
            
            # Check both traditional and AI-enhanced skills
            youth_skill_level = max(
                youth.traditional_skills.get(skill, 0),
                youth.ai_enhanced_skills.get(skill, 0)
            )
            
            if youth_skill_level >= required_level:
                skill_match += 1.0
            else:
                # Partial credit for close matches
                skill_match += youth_skill_level / required_level
        
        if total_requirements > 0:
            score += (skill_match / total_requirements) * 0.5
        
        # Geographic compatibility (15% weight)
        if job['remote_work'] or youth.region == job['region']:
            score += 0.15
        elif youth.region == Region.DHAKA and job['region'] in [Region.CHITTAGONG, Region.SYLHET]:
            score += 0.10  # Partial credit for urban mobility
        
        # Language requirements (15% weight)
        if job['employer_type'] == 'international':
            score += youth.english_proficiency * 0.15
        else:
            score += 0.15  # Local jobs don't require English
        
        # AI collaboration capability (10% weight)
        if job['ai_collaboration_required']:
            ai_collab_skill = youth.ai_enhanced_skills.get('human_ai_collaboration', 0)
            score += ai_collab_skill * 0.10
        else:
            score += 0.10
        
        # Experience factor (5% weight)
        if job['experience_required']:
            # Check employment history
            has_experience = len(youth.employment_history) > 0 or youth.employment_status != 'unemployed_seeking'
            score += 0.05 if has_experience else 0.02
        else:
            score += 0.05
        
        # Cultural fit (5% weight)
        cultural_fit = 1 - youth.cultural_constraints
        if job['employer_type'] == 'international':
            cultural_fit *= 1.2  # International employers may value cultural adaptability
        score += cultural_fit * 0.05
        
        return np.clip(score, 0, 1)
    
    def calculate_hiring_probability(self, youth: YouthAgent, job: Dict[str, Any], match_score: float) -> float:
        """Calculate probability of actual hiring given match score"""
        
        base_prob = match_score * 0.8  # Base probability from match score
        
        # Market conditions adjustment
        skill_shortage = 0
        for skill in job['skill_requirements']:
            if skill in self.ai_skills_demand:
                skill_shortage += self.ai_skills_demand[skill]['skill_shortage_index']
        
        if len(job['skill_requirements']) > 0:
            avg_shortage = skill_shortage / len(job['skill_requirements'])
            base_prob += avg_shortage * 0.2  # Higher shortage increases hiring probability
        
        # Competition factor (simplified)
        competition_factor = np.random.uniform(0.7, 1.0)
        base_prob *= competition_factor
        
        return np.clip(base_prob, 0.1, 0.9)
    
    def assign_job(self, youth: YouthAgent, job: Dict[str, Any]):
        """Assign job to youth and update their status"""
        
        # Calculate salary based on skills and negotiation
        salary = self.calculate_job_salary(youth, job)
        
        # Update youth employment status
        youth.employment_status = 'employed_formal' if job['employer_type'] in ['enterprise', 'international'] else 'employed_informal'
        youth.monthly_income = salary
        
        # Record employment event
        youth.employment_history.append({
            'month': self.current_month,
            'event': 'job_assigned',
            'employer_type': job['employer_type'],
            'industry': job['industry'],
            'salary': salary,
            'remote_work': job['remote_work'],
            'ai_collaboration': job['ai_collaboration_required']
        })
        
        # Update income history
        youth.income_history.append(salary)
        
        # Improve social network and motivation
        youth.social_network_strength = min(youth.social_network_strength + 0.1, 1.0)
        youth.motivation_level = min(youth.motivation_level + 0.05, 1.0)
    
    def calculate_job_salary(self, youth: YouthAgent, job: Dict[str, Any]) -> float:
        """Calculate salary for job assignment"""
        
        base_salary = (job['salary_min'] + job['salary_max']) / 2
        
        # Skill premium
        skill_premium = 0
        for skill, required_level in job['skill_requirements'].items():
            youth_skill = max(
                youth.traditional_skills.get(skill, 0),
                youth.ai_enhanced_skills.get(skill, 0)
            )
            if youth_skill > required_level:
                skill_premium += (youth_skill - required_level) * 0.1
        
        # AI skills premium
        ai_skills_avg = np.mean(list(youth.ai_enhanced_skills.values()))
        if ai_skills_avg > 0.6:
            skill_premium += 0.15
        
        # Experience premium
        if len(youth.employment_history) > 0:
            skill_premium += 0.05
        
        # Negotiation factor based on social network and motivation
        negotiation_factor = (youth.social_network_strength + youth.motivation_level) / 2
        
        final_salary = base_salary * (1 + skill_premium) * (0.9 + negotiation_factor * 0.2)
        
        return np.clip(final_salary, job['salary_min'], job['salary_max'] * 1.2)
    
    def update_agent_states(self):
        """Update agent states for the current month"""
        
        for youth in self.youth_agents:
            # Update financial resources
            youth.financial_resources += youth.monthly_income - youth.debt_burden * 0.1
            
            # Skill decay for unused skills (very small)
            for skill in youth.traditional_skills:
                youth.traditional_skills[skill] *= 0.999
            
            # AI skills improvement through usage (if employed in AI-related work)
            if youth.employment_status in ['employed_formal', 'employed_informal']:
                recent_job = youth.employment_history[-1] if youth.employment_history else None
                if recent_job and recent_job.get('ai_collaboration', False):
                    for skill in youth.ai_enhanced_skills:
                        youth.ai_enhanced_skills[skill] = min(youth.ai_enhanced_skills[skill] + 0.01, 1.0)
            
            # Update motivation based on employment status
            if youth.employment_status in ['employed_formal', 'employed_informal']:
                youth.motivation_level = min(youth.motivation_level + 0.02, 1.0)
            elif youth.employment_status == 'unemployed_seeking':
                youth.motivation_level = max(youth.motivation_level - 0.01, 0.1)
    
    def calculate_monthly_metrics(self):
        """Calculate and store monthly performance metrics"""
        
        # Employment metrics
        total_youth = len(self.youth_agents)
        employed = len([y for y in self.youth_agents if y.employment_status in ['employed_formal', 'employed_informal']])
        unemployed = len([y for y in self.youth_agents if y.employment_status == 'unemployed_seeking'])
        underemployed = len([y for y in self.youth_agents if y.employment_status == 'underemployed'])
        
        # Income metrics
        total_income = sum(y.monthly_income for y in self.youth_agents)
        avg_income = total_income / total_youth if total_youth > 0 else 0
        
        # Training metrics
        in_training = len([y for y in self.youth_agents if y.program_participation])
        completed_training = len([y for y in self.youth_agents if y.training_completion_rate >= 0.8])
        
        # Skills metrics
        avg_ai_skills = np.mean([np.mean(list(y.ai_enhanced_skills.values())) for y in self.youth_agents])
        avg_traditional_skills = np.mean([np.mean(list(y.traditional_skills.values())) for y in self.youth_agents])
        
        # Economic impact
        monthly_economic_impact = total_income * self.economic_multipliers['total_multiplier']
        
        metrics = {
            'month': self.current_month,
            'employment_rate': (employed / total_youth) * 100,
            'unemployment_rate': (unemployed / total_youth) * 100,
            'underemployment_rate': (underemployed / total_youth) * 100,
            'average_income': avg_income,
            'total_income': total_income,
            'in_training': in_training,
            'completed_training': completed_training,
            'avg_ai_skills': avg_ai_skills,
            'avg_traditional_skills': avg_traditional_skills,
            'economic_impact': monthly_economic_impact
        }
        
        self.monthly_metrics.append(metrics)
    
    def get_employment_rate(self) -> float:
        """Get current employment rate"""
        total = len(self.youth_agents)
        employed = len([y for y in self.youth_agents if y.employment_status in ['employed_formal', 'employed_informal']])
        return (employed / total) * 100 if total > 0 else 0
    
    def generate_results(self) -> Dict[str, Any]:
        """Generate comprehensive simulation results"""
        
        # Final metrics
        final_metrics = self.monthly_metrics[-1] if self.monthly_metrics else {}
        
        # Calculate improvements
        initial_metrics = self.monthly_metrics[0] if self.monthly_metrics else {}
        
        employment_improvement = final_metrics.get('employment_rate', 0) - initial_metrics.get('employment_rate', 0)
        income_improvement = ((final_metrics.get('average_income', 0) - initial_metrics.get('average_income', 1)) / 
                            max(initial_metrics.get('average_income', 1), 1)) * 100
        
        # Economic impact calculation
        total_economic_impact = sum(m['economic_impact'] for m in self.monthly_metrics)
        
        # Training effectiveness
        total_trained = sum(m['completed_training'] for m in self.monthly_metrics)
        training_employment_rate = 0
        if total_trained > 0:
            trained_youth = [y for y in self.youth_agents if y.training_completion_rate >= 0.8]
            employed_trained = [y for y in trained_youth if y.employment_status in ['employed_formal', 'employed_informal']]
            training_employment_rate = (len(employed_trained) / len(trained_youth)) * 100
        
        # Gender analysis
        male_employment = len([y for y in self.youth_agents if y.gender == 'male' and 
                             y.employment_status in ['employed_formal', 'employed_informal']])
        female_employment = len([y for y in self.youth_agents if y.gender == 'female' and 
                               y.employment_status in ['employed_formal', 'employed_informal']])
        total_male = len([y for y in self.youth_agents if y.gender == 'male'])
        total_female = len([y for y in self.youth_agents if y.gender == 'female'])
        
        male_employment_rate = (male_employment / total_male) * 100 if total_male > 0 else 0
        female_employment_rate = (female_employment / total_female) * 100 if total_female > 0 else 0
        
        # Regional analysis
        regional_results = {}
        for region in Region:
            region_youth = [y for y in self.youth_agents if y.region == region]
            region_employed = [y for y in region_youth if y.employment_status in ['employed_formal', 'employed_informal']]
            regional_results[region.value] = {
                'total_youth': len(region_youth),
                'employed': len(region_employed),
                'employment_rate': (len(region_employed) / len(region_youth)) * 100 if region_youth else 0,
                'avg_income': np.mean([y.monthly_income for y in region_youth]) if region_youth else 0
            }
        
        results = {
            'simulation_months': self.max_months,
            'total_youth_agents': len(self.youth_agents),
            'final_employment_rate': final_metrics.get('employment_rate', 0),
            'employment_rate_improvement': employment_improvement,
            'average_income_increase': income_improvement,
            'total_economic_impact': total_economic_impact,
            'total_youth_trained': total_trained,
            'training_employment_rate': training_employment_rate,
            'male_employment_rate': male_employment_rate,
            'female_employment_rate': female_employment_rate,
            'gender_gap': male_employment_rate - female_employment_rate,
            'regional_results': regional_results,
            'monthly_metrics': self.monthly_metrics,
            'final_ai_skills_avg': final_metrics.get('avg_ai_skills', 0),
            'skills_improvement': final_metrics.get('avg_ai_skills', 0) - initial_metrics.get('avg_ai_skills', 0)
        }
        
        return results
    
    def generate_visualizations(self, results: Dict[str, Any]):
        """Generate visualization plots for simulation results"""
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Bangladesh Youth Employment Simulation Results', fontsize=16, fontweight='bold')
        
        # 1. Employment Rate Over Time
        months = [m['month'] for m in results['monthly_metrics']]
        employment_rates = [m['employment_rate'] for m in results['monthly_metrics']]
        
        axes[0, 0].plot(months, employment_rates, linewidth=2, color='#2E8B57')
        axes[0, 0].set_title('Employment Rate Over Time')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Employment Rate (%)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Average Income Progression
        avg_incomes = [m['average_income'] for m in results['monthly_metrics']]
        
        axes[0, 1].plot(months, avg_incomes, linewidth=2, color='#4169E1')
        axes[0, 1].set_title('Average Monthly Income Progression')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].set_ylabel('Average Income (BDT)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Training Participation and Completion
        in_training = [m['in_training'] for m in results['monthly_metrics']]
        completed_training = [m['completed_training'] for m in results['monthly_metrics']]
        
        axes[0, 2].plot(months, in_training, label='In Training', linewidth=2, color='#FF6347')
        axes[0, 2].plot(months, completed_training, label='Completed Training', linewidth=2, color='#32CD32')
        axes[0, 2].set_title('Training Participation')
        axes[0, 2].set_xlabel('Month')
        axes[0, 2].set_ylabel('Number of Youth')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Skills Development
        ai_skills = [m['avg_ai_skills'] for m in results['monthly_metrics']]
        traditional_skills = [m['avg_traditional_skills'] for m in results['monthly_metrics']]
        
        axes[1, 0].plot(months, ai_skills, label='AI-Enhanced Skills', linewidth=2, color='#9370DB')
        axes[1, 0].plot(months, traditional_skills, label='Traditional Skills', linewidth=2, color='#CD853F')
        axes[1, 0].set_title('Skills Development Over Time')
        axes[1, 0].set_xlabel('Month')
        axes[1, 0].set_ylabel('Average Skill Level (0-1)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Regional Employment Comparison
        regions = list(results['regional_results'].keys())
        regional_rates = [results['regional_results'][r]['employment_rate'] for r in regions]
        
        bars = axes[1, 1].bar(regions, regional_rates, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[1, 1].set_title('Final Employment Rate by Region')
        axes[1, 1].set_ylabel('Employment Rate (%)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, rate in zip(bars, regional_rates):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                           f'{rate:.1f}%', ha='center', va='bottom')
        
        # 6. Gender Employment Comparison
        gender_data = ['Male', 'Female']
        gender_rates = [results['male_employment_rate'], results['female_employment_rate']]
        
        bars = axes[1, 2].bar(gender_data, gender_rates, color=['#87CEEB', '#FFB6C1'])
        axes[1, 2].set_title('Employment Rate by Gender')
        axes[1, 2].set_ylabel('Employment Rate (%)')
        
        # Add value labels on bars
        for bar, rate in zip(bars, gender_rates):
            axes[1, 2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                           f'{rate:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig

# Example usage and configuration
def run_simulation_example():
    """Example of how to run the simulation"""
    
    # Simulation configuration
    config = {
        'simulation_months': 36,
        'num_youth_agents': 10000,
        'num_employer_agents': 1000,
        'monthly_training_capacity': 500,
        'scenario': 'optimistic'  # 'conservative', 'optimistic', 'crisis'
    }
    
    # Create and run simulation
    sim = SimulationEngine(config)
    results = sim.run_simulation()
    
    # Generate visualizations
    sim.generate_visualizations(results)
    
    # Save results
    with open('simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    return results

    print("\n=== Bangladesh Youth Employment Simulation Results ===")
    print(f"Final Employment Rate: {results['final_employment_rate']:.1f}%")
    print(f"Employment Improvement: +{results['employment_rate_improvement']:.1f} percentage points")
    print(f"Average Income Increase: {results['average_income_increase']:.1f}%")
    print(f"Total Youth Trained: {results['total_youth_trained']:,}")
    print(f"Training Employment Rate: {results['training_employment_rate']:.1f}%")
    print(f"Gender Gap: {results['gender_gap']:.1f} percentage points")
    print(f"Total Economic Impact: {results['total_economic_impact']:,.0f} BDT")
    
    return results

# Scenario Testing Functions
def run_scenario_analysis():
    """Run multiple scenarios for comparison"""
    
    scenarios = {
        'conservative': {
            'simulation_months': 36,
            'num_youth_agents': 8000,
            'num_employer_agents': 800,
            'monthly_training_capacity': 300,
            'scenario': 'conservative'
        },
        'optimistic': {
            'simulation_months': 36,
            'num_youth_agents': 12000,
            'num_employer_agents': 1200,
            'monthly_training_capacity': 700,
            'scenario': 'optimistic'
        },
        'crisis': {
            'simulation_months': 36,
            'num_youth_agents': 6000,
            'num_employer_agents': 600,
            'monthly_training_capacity': 200,
            'scenario': 'crisis'
        }
    }
    
    scenario_results = {}
    
    for scenario_name, config in scenarios.items():
        print(f"\nRunning {scenario_name} scenario...")
        sim = SimulationEngine(config)
        results = sim.run_simulation()
        scenario_results[scenario_name] = results
        
        # Save individual scenario results
        with open(f'scenario_{scenario_name}_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    # Compare scenarios
    print("\n=== Scenario Comparison ===")
    print(f"{'Metric':<30} {'Conservative':<15} {'Optimistic':<15} {'Crisis':<15}")
    print("-" * 75)
    
    metrics = [
        ('Final Employment Rate (%)', 'final_employment_rate'),
        ('Income Increase (%)', 'average_income_increase'),
        ('Youth Trained', 'total_youth_trained'),
        ('Economic Impact (M BDT)', 'total_economic_impact')
    ]
    
    for metric_name, metric_key in metrics:
        values = []
        for scenario in ['conservative', 'optimistic', 'crisis']:
            value = scenario_results[scenario][metric_key]
            if metric_key == 'total_economic_impact':
                value = value / 1_000_000  # Convert to millions
            values.append(value)
        
        print(f"{metric_name:<30} {values[0]:<15.1f} {values[1]:<15.1f} {values[2]:<15.1f}")
    
    return scenario_results

# Policy Impact Testing
def test_policy_interventions():
    """Test different policy intervention scenarios"""
    
    base_config = {
        'simulation_months': 36,
        'num_youth_agents': 10000,
        'num_employer_agents': 1000,
        'monthly_training_capacity': 500,
        'scenario': 'baseline'
    }
    
    interventions = {
        'increased_capacity': {
            **base_config,
            'monthly_training_capacity': 1000,
            'intervention': 'doubled_training_capacity'
        },
        'enhanced_support': {
            **base_config,
            'family_support_boost': 0.2,
            'intervention': 'enhanced_family_support'
        },
        'ai_focus': {
            **base_config,
            'ai_skills_emphasis': 1.5,
            'intervention': 'ai_skills_focus'
        },
        'gender_targeted': {
            **base_config,
            'female_participation_boost': 0.3,
            'intervention': 'gender_targeted_programs'
        }
    }
    
    intervention_results = {}
    
    for intervention_name, config in interventions.items():
        print(f"\nTesting {intervention_name} intervention...")
        sim = SimulationEngine(config)
        results = sim.run_simulation()
        intervention_results[intervention_name] = results
    
    return intervention_results

if __name__ == "__main__":
    print("Bangladesh Youth Employment AI-Enhanced Simulation Framework")
    print("=" * 60)
    
    # Run basic simulation
    print("\n1. Running basic simulation...")
    basic_results = run_simulation_example()
    
    # Run scenario analysis
    print("\n2. Running scenario analysis...")
    scenario_results = run_scenario_analysis()
    
    # Run policy intervention testing
    print("\n3. Testing policy interventions...")
    intervention_results = test_policy_interventions()
    
    # Generate comprehensive report
    print("\n4. Generating comprehensive analysis report...")
    
    # Save all results
    comprehensive_results = {
        'basic_simulation': basic_results,
        'scenario_analysis': scenario_results,
        'policy_interventions': intervention_results,
        'metadata': {
            'simulation_date': datetime.now().isoformat(),
            'framework_version': '1.0',
            'total_simulations_run': 1 + len(scenario_results) + len(intervention_results)
        }
    }
    
    with open('comprehensive_simulation_results.json', 'w') as f:
        json.dump(comprehensive_results, f, indent=2, default=str)
    
    print("\n=== Simulation Framework Complete ===")
    print("Results saved to:")
    print("- simulation_results.json (basic simulation)")
    print("- scenario_*_results.json (individual scenarios)")
    print("- comprehensive_simulation_results.json (all results)")
    print("- simulation_results.png (visualizations)")
    
    print("\nFramework ready for policy analysis and decision support!")