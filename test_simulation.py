#!/usr/bin/env python3
"""
Test Script for Bangladesh Youth Employment Simulation Framework

This script runs basic validation tests to ensure the simulation framework
works correctly with realistic data.

Usage: python test_simulation.py
"""

import sys
import json
import time
from datetime import datetime

try:
    from simulation_framework import SimulationEngine, run_simulation_example
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install required dependencies with: pip install -r requirements.txt")
    sys.exit(1)

def test_basic_functionality():
    """Test basic simulation functionality"""
    print("Testing basic simulation functionality...")
    
    # Small test configuration
    test_config = {
        'simulation_months': 6,
        'num_youth_agents': 100,
        'num_employer_agents': 20,
        'monthly_training_capacity': 10,
        'scenario': 'test'
    }
    
    try:
        sim = SimulationEngine(test_config)
        print(f"✓ Simulation engine created successfully")
        print(f"  - Youth agents: {len(sim.youth_agents)}")
        print(f"  - Employer agents: {len(sim.employer_agents)}")
        
        # Test data loading
        assert len(sim.youth_demographics) > 0, "Youth demographics not loaded"
        assert len(sim.regional_data) > 0, "Regional data not loaded"
        assert len(sim.ai_skills_demand) > 0, "AI skills demand data not loaded"
        print(f"✓ Realistic data loaded successfully")
        
        # Test agent generation
        assert len(sim.youth_agents) == test_config['num_youth_agents'], "Incorrect number of youth agents"
        assert len(sim.employer_agents) == test_config['num_employer_agents'], "Incorrect number of employer agents"
        print(f"✓ Agent population generated correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_agent_attributes():
    """Test that agents have correct attributes"""
    print("\nTesting agent attributes...")
    
    test_config = {
        'simulation_months': 3,
        'num_youth_agents': 50,
        'num_employer_agents': 10,
        'monthly_training_capacity': 5,
        'scenario': 'test'
    }
    
    try:
        sim = SimulationEngine(test_config)
        
        # Test youth agent attributes
        youth = sim.youth_agents[0]
        required_attributes = [
            'id', 'age', 'gender', 'region', 'education_level',
            'employment_status', 'monthly_income', 'english_proficiency',
            'digital_literacy', 'ai_familiarity', 'traditional_skills',
            'ai_enhanced_skills', 'family_support', 'motivation_level'
        ]
        
        for attr in required_attributes:
            assert hasattr(youth, attr), f"Youth agent missing attribute: {attr}"
        
        # Test attribute ranges
        assert 0 <= youth.english_proficiency <= 1, "English proficiency out of range"
        assert 0 <= youth.digital_literacy <= 1, "Digital literacy out of range"
        assert 0 <= youth.ai_familiarity <= 1, "AI familiarity out of range"
        assert youth.age >= 25 and youth.age <= 35, "Age out of expected range"
        
        print(f"✓ Youth agent attributes validated")
        
        # Test employer agent attributes
        employer = sim.employer_agents[0]
        employer_attributes = [
            'id', 'type', 'region', 'industry', 'size',
            'monthly_job_openings', 'skill_requirements', 'salary_range'
        ]
        
        for attr in employer_attributes:
            assert hasattr(employer, attr), f"Employer agent missing attribute: {attr}"
        
        assert len(employer.skill_requirements) > 0, "Employer has no skill requirements"
        assert employer.salary_range[0] < employer.salary_range[1], "Invalid salary range"
        
        print(f"✓ Employer agent attributes validated")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent attributes test failed: {e}")
        return False

def test_simulation_execution():
    """Test that simulation runs without errors"""
    print("\nTesting simulation execution...")
    
    test_config = {
        'simulation_months': 3,
        'num_youth_agents': 50,
        'num_employer_agents': 10,
        'monthly_training_capacity': 5,
        'scenario': 'test'
    }
    
    try:
        start_time = time.time()
        sim = SimulationEngine(test_config)
        results = sim.run_simulation()
        end_time = time.time()
        
        # Test results structure
        required_results = [
            'simulation_months', 'total_youth_agents', 'final_employment_rate',
            'employment_rate_improvement', 'average_income_increase',
            'total_economic_impact', 'monthly_metrics'
        ]
        
        for key in required_results:
            assert key in results, f"Missing result key: {key}"
        
        # Test result values
        assert results['simulation_months'] == test_config['simulation_months']
        assert results['total_youth_agents'] == test_config['num_youth_agents']
        assert 0 <= results['final_employment_rate'] <= 100, "Employment rate out of range"
        assert len(results['monthly_metrics']) == test_config['simulation_months']
        
        execution_time = end_time - start_time
        print(f"✓ Simulation executed successfully in {execution_time:.2f} seconds")
        print(f"  - Final employment rate: {results['final_employment_rate']:.1f}%")
        print(f"  - Economic impact: {results['total_economic_impact']:,.0f} BDT")
        
        return True
        
    except Exception as e:
        print(f"✗ Simulation execution test failed: {e}")
        return False

def test_data_consistency():
    """Test data consistency and realistic values"""
    print("\nTesting data consistency...")
    
    test_config = {
        'simulation_months': 6,
        'num_youth_agents': 100,
        'num_employer_agents': 20,
        'monthly_training_capacity': 10,
        'scenario': 'test'
    }
    
    try:
        sim = SimulationEngine(test_config)
        
        # Test regional data consistency
        total_population = sum(data['population_25_35'] for data in sim.regional_data.values())
        expected_population = sim.youth_demographics['total_population_25_35']
        assert abs(total_population - expected_population) < 100000, "Regional population inconsistent"
        
        # Test skill demand data
        for skill, data in sim.ai_skills_demand.items():
            assert data['monthly_job_postings'] > 0, f"No job postings for {skill}"
            assert data['average_hourly_rate_usd'] > 0, f"Invalid hourly rate for {skill}"
            assert 0 <= data['skill_shortage_index'] <= 1, f"Invalid shortage index for {skill}"
        
        # Test agent distribution
        male_count = len([y for y in sim.youth_agents if y.gender == 'male'])
        female_count = len([y for y in sim.youth_agents if y.gender == 'female'])
        male_percentage = (male_count / len(sim.youth_agents)) * 100
        
        # Should be close to expected 51.2% male
        assert 45 <= male_percentage <= 57, f"Gender distribution unrealistic: {male_percentage:.1f}% male"
        
        print(f"✓ Data consistency validated")
        print(f"  - Population data consistent")
        print(f"  - Skills demand data valid")
        print(f"  - Agent distribution realistic ({male_percentage:.1f}% male)")
        
        return True
        
    except Exception as e:
        print(f"✗ Data consistency test failed: {e}")
        return False

def test_training_system():
    """Test training system functionality"""
    print("\nTesting training system...")
    
    test_config = {
        'simulation_months': 12,
        'num_youth_agents': 100,
        'num_employer_agents': 20,
        'monthly_training_capacity': 20,
        'scenario': 'test'
    }
    
    try:
        sim = SimulationEngine(test_config)
        
        # Run simulation and check training outcomes
        results = sim.run_simulation()
        
        # Check that some youth participated in training
        trained_youth = [y for y in sim.youth_agents if y.training_completion_rate > 0]
        assert len(trained_youth) > 0, "No youth participated in training"
        
        # Check skill improvement
        skill_improvements = []
        for youth in trained_youth:
            if youth.skill_development_history:
                initial_skills = youth.skill_development_history[0]
                skill_improvements.append(len(initial_skills.get('skills_updated', [])))
        
        assert len(skill_improvements) > 0, "No skill improvements recorded"
        
        # Check training completion rates are realistic
        completion_rates = [y.training_completion_rate for y in trained_youth]
        avg_completion = np.mean(completion_rates)
        assert 0.5 <= avg_completion <= 1.0, f"Unrealistic completion rate: {avg_completion:.2f}"
        
        print(f"✓ Training system validated")
        print(f"  - {len(trained_youth)} youth participated in training")
        print(f"  - Average completion rate: {avg_completion:.2f}")
        print(f"  - Skill improvements recorded: {len(skill_improvements)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Training system test failed: {e}")
        return False

def test_job_matching():
    """Test job matching functionality"""
    print("\nTesting job matching system...")
    
    test_config = {
        'simulation_months': 6,
        'num_youth_agents': 100,
        'num_employer_agents': 30,
        'monthly_training_capacity': 15,
        'scenario': 'test'
    }
    
    try:
        sim = SimulationEngine(test_config)
        results = sim.run_simulation()
        
        # Check employment outcomes
        employed_youth = [y for y in sim.youth_agents if 
                         y.employment_status in ['employed_formal', 'employed_informal']]
        
        assert len(employed_youth) > 0, "No youth found employment"
        
        # Check employment history
        youth_with_jobs = [y for y in sim.youth_agents if len(y.employment_history) > 0]
        assert len(youth_with_jobs) > 0, "No employment history recorded"
        
        # Check income progression
        youth_with_income = [y for y in sim.youth_agents if len(y.income_history) > 0]
        assert len(youth_with_income) > 0, "No income history recorded"
        
        # Check that employed youth have reasonable incomes
        employed_incomes = [y.monthly_income for y in employed_youth if y.monthly_income > 0]
        if employed_incomes:
            avg_income = np.mean(employed_incomes)
            assert avg_income > 10000, f"Average income too low: {avg_income:.0f} BDT"
            assert avg_income < 100000, f"Average income too high: {avg_income:.0f} BDT"
        
        print(f"✓ Job matching system validated")
        print(f"  - {len(employed_youth)} youth found employment")
        print(f"  - {len(youth_with_jobs)} youth have employment history")
        if employed_incomes:
            print(f"  - Average income: {np.mean(employed_incomes):,.0f} BDT")
        
        return True
        
    except Exception as e:
        print(f"✗ Job matching test failed: {e}")
        return False

def run_performance_test():
    """Test simulation performance with larger datasets"""
    print("\nRunning performance test...")
    
    test_config = {
        'simulation_months': 12,
        'num_youth_agents': 1000,
        'num_employer_agents': 100,
        'monthly_training_capacity': 50,
        'scenario': 'performance_test'
    }
    
    try:
        start_time = time.time()
        sim = SimulationEngine(test_config)
        setup_time = time.time() - start_time
        
        start_sim = time.time()
        results = sim.run_simulation()
        sim_time = time.time() - start_sim
        
        total_time = time.time() - start_time
        
        print(f"✓ Performance test completed")
        print(f"  - Setup time: {setup_time:.2f} seconds")
        print(f"  - Simulation time: {sim_time:.2f} seconds")
        print(f"  - Total time: {total_time:.2f} seconds")
        print(f"  - Agents processed: {len(sim.youth_agents):,} youth, {len(sim.employer_agents):,} employers")
        
        # Performance benchmarks
        if total_time < 30:  # Should complete in under 30 seconds
            print(f"  - Performance: GOOD (under 30 seconds)")
        elif total_time < 60:
            print(f"  - Performance: ACCEPTABLE (under 1 minute)")
        else:
            print(f"  - Performance: SLOW (over 1 minute)")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("Bangladesh Youth Employment Simulation Framework - Validation Tests")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Agent Attributes", test_agent_attributes),
        ("Simulation Execution", test_simulation_execution),
        ("Data Consistency", test_data_consistency),
        ("Training System", test_training_system),
        ("Job Matching", test_job_matching),
        ("Performance", run_performance_test)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        try:
            if test_func():
                passed_tests += 1
                print(f"\n✓ {test_name} PASSED")
            else:
                print(f"\n✗ {test_name} FAILED")
        except Exception as e:
            print(f"\n✗ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*70}")
    print(f"TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Simulation framework is ready for use.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)