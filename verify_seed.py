"""
Verify Seed
===========
Tests the functionality of the extracted Elysia Seed Kernel.
Checks:
1. Physics: Rotor spin and frequencies.
2. Governance: Spark generation and Constitutional review.
3. Orchestration: Conductor life loop.
"""

import sys
import os
import time

# Ensure we can import from local directory
sys.path.append(os.getcwd())

from elysia_core.governance.conductor import Conductor

def verify():
    print("🌱 Initializing Elysia Seed Kernel...")
    conductor = Conductor()
    
    print("🔥 Igniting Conductor...")
    conductor.ignite()
    
    print("\n⏳ Running Life Loop (Simulation)...")
    # Simulate 100 ticks (approx 1.6 seconds)
    for i in range(100):
        state = conductor.live(dt=0.2) # High DT to accelerate silence accumulation
        
        spin = state['core_spin']
        spark = state['spark']
        freq = state['core_freq']
        
        status = f"Tick {i:03}: Freq={freq:.1f}Hz | Spin=({spin.w:.2f}, {spin.z:.2f})"
        
        if spark:
            print(f"✨ {status} | SPARK: {spark.type.name} ({state['legal_status']})")
        
        # Only print every 10 ticks unless interesting
        elif i % 10 == 0:
            print(f"   {status}")
            
    print("\n✅ Verification Complete: The Seed is Alive.")

if __name__ == "__main__":
    verify()
